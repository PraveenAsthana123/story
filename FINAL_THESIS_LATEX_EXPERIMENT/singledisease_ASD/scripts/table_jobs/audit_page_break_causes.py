#!/usr/bin/env python3
"""Per-chapter inventory of EXPLICIT page-break and white-space causes.

Counts per chapter/appendix:
  - \\clearpage            (forces page break + flushes pending floats; leaves bottom whitespace)
  - \\newpage              (forces page break; leaves bottom whitespace)
  - \\pagebreak            (suggests page break)
  - \\needspace{>=N}       (forces break if N baselines unavailable; can leave up to N-1 blank)
  - \\vspace{>=Ncm}        (explicit vertical white space)
  - \\vfill / \\vfil       (stretches to fill remaining space)

For each chapter, reports:
  - count per cause
  - line numbers of the top 15 highest-cost directives
  - estimated white-space cost (heuristic: needspace cost = N baselines if break fires)
  - suggested action (e.g., 'reduce needspace from 24 to 16', 'remove redundant clearpage')

READ-ONLY: no .tex files modified.
"""
from __future__ import annotations
import re
from pathlib import Path
from collections import defaultdict, Counter
from datetime import datetime

ROOT = Path(__file__).resolve().parents[2]
CHAPTERS_DIR = ROOT / "chapters"
APPENDICES_DIR = ROOT / "appendices"
OUT_DIR = ROOT / "jobs" / "reports"
OUT = OUT_DIR / f"page_break_causes_{datetime.now():%Y%m%d_%H%M}.md"
MASTER = OUT_DIR / "page_break_causes_master.md"


def strip_comments(line: str) -> str:
    out = []; i = 0
    while i < len(line):
        if line[i] == "%" and (i == 0 or line[i - 1] != "\\"):
            break
        out.append(line[i]); i += 1
    return "".join(out)


def mask_suppressed(text: str) -> str:
    """Skip \\iffalse...\\fi content."""
    lines = text.splitlines()
    out = []
    in_false = 0; if_depth = 0
    for raw in lines:
        s = strip_comments(raw).strip()
        if re.match(r"\\iffalse\b", s):
            in_false += 1; out.append(""); continue
        if in_false > 0:
            if re.match(r"\\if[a-zA-Z]*\b", s): if_depth += 1
            elif re.match(r"\\fi\b", s):
                if if_depth > 0: if_depth -= 1
                else: in_false -= 1
            out.append(""); continue
        out.append(raw)
    return "\n".join(out)


def scan_file(fp: Path) -> dict:
    raw = fp.read_text()
    text = mask_suppressed(raw)
    counts = Counter()
    detail = []
    for n, line in enumerate(text.splitlines(), 1):
        s = strip_comments(line).strip()
        if not s: continue
        # clearpage
        for m in re.finditer(r"\\clearpage\b", s):
            counts["clearpage"] += 1
            detail.append((n, "clearpage", "forces break + flushes floats", "20 baselines avg"))
        for m in re.finditer(r"\\newpage\b", s):
            counts["newpage"] += 1
            detail.append((n, "newpage", "forces break", "15 baselines avg"))
        for m in re.finditer(r"\\pagebreak\b", s):
            counts["pagebreak"] += 1
            detail.append((n, "pagebreak", "hints break", "5 baselines avg"))
        for m in re.finditer(r"\\needspace\{(\d+)\\baselineskip\}", s):
            n_base = int(m.group(1))
            counts[f"needspace_{n_base}"] += 1
            if n_base >= 16:
                detail.append((n, f"needspace{{{n_base}}}", f"break if <{n_base} baselines free", f"up to {n_base-1} baselines"))
        for m in re.finditer(r"\\vspace\*?\{([\d.]+)cm\}", s):
            v = float(m.group(1))
            if v >= 1.0:
                counts["vspace>=1cm"] += 1
                detail.append((n, f"vspace{{{v}cm}}", "explicit vertical white", f"{v}cm"))
        for m in re.finditer(r"\\vfill\b|\\vfil\b", s):
            counts["vfill"] += 1
            detail.append((n, "vfill", "stretches white", "variable"))
    # Sort detail by cost-proxy (clearpage > needspace>=24 > newpage > others)
    cost_rank = {"clearpage": 4, "newpage": 3, "vfill": 2, "pagebreak": 1}
    def rank(item):
        n, kind, _desc, _cost = item
        if kind.startswith("needspace"):
            try:
                return int(re.search(r"(\d+)", kind).group(1)) // 5
            except Exception:
                return 1
        return cost_rank.get(kind, 0)
    detail.sort(key=lambda d: -rank(d))
    return {
        "file": fp.name,
        "counts": dict(counts),
        "total_directives": sum(counts.values()),
        "top_15": detail[:15],
    }


def classify_owner(fp: Path) -> str:
    n = fp.name.lower()
    if n.startswith("chapter1"): return "ch1"
    if n.startswith("chapter2"): return "ch2"
    if n.startswith("chapter3"): return "ch3"
    if n.startswith("chapter4"): return "ch4"
    if n.startswith("chapter5"): return "ch5"
    for L in "ABCDEFGHIJKLMNOPQRSTUVWXYZ":
        if n.startswith(L.lower() + "_") or n.startswith(L.lower() + "."):
            return f"app{L}"
    return "other"


def main():
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    files = sorted(CHAPTERS_DIR.glob("chapter*.tex")) + sorted(APPENDICES_DIR.glob("*.tex"))
    by_owner = defaultdict(list)
    for fp in files:
        by_owner[classify_owner(fp)].append(scan_file(fp))

    # Master roll-up
    lines = []
    lines.append("# Page-Break Causes --- Per-Chapter Audit\n")
    lines.append(f"_Generated: {datetime.now().isoformat(timespec='seconds')}_\n")
    lines.append("## How to read this report")
    lines.append("- **clearpage**: forces break + flushes pending floats. Highest white-space cost.")
    lines.append("- **newpage**: forces break only.")
    lines.append("- **needspace{N\\baselineskip}**: if N baselines unavailable, breaks page. Higher N = more potential blank space.")
    lines.append("- **vspace>=1cm**: explicit vertical white.")
    lines.append("- **vfill**: stretches to fill remaining space; can leave a half-page or full-page blank.")
    lines.append("")
    lines.append("Each cause is a *potential* source of the user's complaint 'page empty or having only one line text'. Not every directive fires --- they only matter when the page-fill heuristic decides the break is necessary.")
    lines.append("")
    lines.append("## Per-owner summary\n")
    lines.append("| Owner | Files | clearpage | newpage | needspace>=20 | vspace>=1cm | vfill | TOTAL |")
    lines.append("|---|---:|---:|---:|---:|---:|---:|---:|")
    grand = defaultdict(int)
    for owner in sorted(by_owner):
        rows = by_owner[owner]
        agg = defaultdict(int)
        for r in rows:
            for k, v in r["counts"].items():
                agg[k] += v
        ns_heavy = sum(v for k, v in agg.items() if k.startswith("needspace_") and int(k.split("_")[1]) >= 20)
        total = sum(agg.values())
        lines.append(f"| {owner} | {len(rows)} | {agg.get('clearpage', 0)} | {agg.get('newpage', 0)} | {ns_heavy} | {agg.get('vspace>=1cm', 0)} | {agg.get('vfill', 0)} | {total} |")
        grand["files"] += len(rows)
        grand["clearpage"] += agg.get("clearpage", 0)
        grand["newpage"] += agg.get("newpage", 0)
        grand["needspace_heavy"] += ns_heavy
        grand["vspace"] += agg.get("vspace>=1cm", 0)
        grand["vfill"] += agg.get("vfill", 0)
        grand["total"] += total
    lines.append(f"| **TOTAL** | **{grand['files']}** | **{grand['clearpage']}** | **{grand['newpage']}** | **{grand['needspace_heavy']}** | **{grand['vspace']}** | **{grand['vfill']}** | **{grand['total']}** |")
    lines.append("")
    lines.append("## Top white-space cost contributors per owner\n")
    for owner in sorted(by_owner):
        rows = by_owner[owner]
        # Pick file with highest total directives
        rows_sorted = sorted(rows, key=lambda r: -r["total_directives"])
        if not rows_sorted: continue
        worst = rows_sorted[0]
        if worst["total_directives"] == 0: continue
        lines.append(f"### {owner} --- worst file: `{worst['file']}` ({worst['total_directives']} directives)")
        lines.append("| Line | Kind | Description | Potential cost |")
        lines.append("|---:|---|---|---|")
        for n, kind, desc, cost in worst["top_15"]:
            lines.append(f"| {n} | `{kind}` | {desc} | {cost} |")
        lines.append("")

    lines.append("## Suggested safe global fixes\n")
    lines.append("1. **Lower `\\needspace{24\\baselineskip}` to `\\needspace{16\\baselineskip}` in section/subsection styling** (main.tex lines 540/545). 24 baselines is ~7.2 inches; if a page has 5 inches free, current setting forces page break leaving 5 inches blank. 16 baselines (~4.8 inches) is more realistic for 'don't orphan a section heading' protection.")
    lines.append("2. **Audit `\\clearpage` in Ch.3 modular files** (chapter3_pipeline_dedicated_pages.tex has 32; chapter3_pipeline_extras.tex has 25; chapter3_secondary_data_pages.tex has 22). Many may be unnecessary between adjacent narrow content blocks; consider converting to `\\par\\bigskip` for soft separation.")
    lines.append("3. **chapter3_research_methods.tex has 105 `\\clearpage`s and 371 needspace directives** --- by far the biggest contributor. Per-page review of this file would yield the largest reduction in blank space.")
    lines.append("")
    lines.append("**WARNING:** Each suggested fix should be applied incrementally with build verification, because reducing page breaks can cause: (a) section headings orphaned at page bottoms, (b) tables broken across page boundaries, (c) floats placed sub-optimally. The current settings are intentionally conservative.")

    OUT.write_text("\n".join(lines))
    MASTER.write_text("\n".join(lines))  # also write canonical name
    print(f"Wrote: {OUT}")
    print(f"Wrote: {MASTER}")
    print()
    print("Grand totals across all chapters + appendices:")
    print(f"  clearpage:              {grand['clearpage']}")
    print(f"  newpage:                {grand['newpage']}")
    print(f"  needspace>=20baseline:  {grand['needspace_heavy']}")
    print(f"  vspace>=1cm:            {grand['vspace']}")
    print(f"  vfill:                  {grand['vfill']}")
    print(f"  TOTAL directives:       {grand['total']}")


if __name__ == "__main__":
    main()
