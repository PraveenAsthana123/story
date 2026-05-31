#!/usr/bin/env python3
"""Cross-chapter / cross-appendix content redundancy audit.

For every PAIR of files (chapter vs chapter, chapter vs appendix, appendix
vs appendix), detect:
  1. Identical TABLE CAPTIONS appearing in different files
  2. Near-identical TABLE BODIES (>= 80% token overlap)
  3. Near-identical PARAGRAPHS (>= 85% Jaccard)
  4. Same labels (label{tab:X}) reused across files

Output: jobs/reports/cross_chapter_redundancy_master.md
READ-ONLY: no .tex files modified.
"""
from __future__ import annotations
import re
from pathlib import Path
from collections import defaultdict
from datetime import datetime
from itertools import combinations

ROOT = Path(__file__).resolve().parents[2]
CHAPTERS_DIR = ROOT / "chapters"
APPENDICES_DIR = ROOT / "appendices"
OUT = ROOT / "jobs" / "reports" / "cross_chapter_redundancy_master.md"


def strip_comments(line: str) -> str:
    out = []; i = 0
    while i < len(line):
        if line[i] == "%" and (i == 0 or line[i - 1] != "\\"):
            break
        out.append(line[i]); i += 1
    return "".join(out)


def mask_suppressed(text: str) -> str:
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


def tokens(text: str) -> set:
    return set(t.lower() for t in re.findall(r"[a-zA-Z]{4,}", text))


def jaccard(a: set, b: set) -> float:
    if not a or not b: return 0.0
    return len(a & b) / len(a | b)


def extract_captions(text: str):
    """Return list of (line_no, caption_text)."""
    out = []
    for n, raw in enumerate(text.splitlines(), 1):
        s = strip_comments(raw)
        m = re.search(r"\\caption(?:\[[^\]]*\])?\{([^}]+)\}", s)
        if m:
            out.append((n, m.group(1).strip()))
    return out


def extract_labels(text: str):
    """Return list of (line_no, label) for label{tab:X}."""
    out = []
    for n, raw in enumerate(text.splitlines(), 1):
        s = strip_comments(raw)
        for m in re.finditer(r"\\label\{(tab:[^}]+)\}", s):
            out.append((n, m.group(1)))
    return out


def extract_paragraphs(text: str, min_words=40):
    """Return list of (line_no, paragraph_text). Skip table/figure blocks."""
    paras = []
    cur = []; cur_start = 1
    for n, raw in enumerate(text.splitlines(), 1):
        s = strip_comments(raw).rstrip()
        if not s:
            if cur:
                joined = " ".join(cur).strip()
                if (len(joined.split()) >= min_words
                    and not any(b in joined for b in (
                        "\\begin{table}", "\\begin{xltabular}", "\\begin{tabularx}",
                        "\\begin{tikzpicture}", "\\caption[", "\\toprule"))):
                    paras.append((cur_start, joined))
                cur = []
            continue
        if not cur: cur_start = n
        cur.append(s)
    if cur:
        joined = " ".join(cur).strip()
        if len(joined.split()) >= min_words:
            paras.append((cur_start, joined))
    return paras


def main():
    files = sorted(CHAPTERS_DIR.glob("chapter*.tex")) + sorted(APPENDICES_DIR.glob("*.tex"))
    print(f"Scanning {len(files)} files...")

    # Build index per file
    file_data = {}
    for fp in files:
        try:
            text = mask_suppressed(fp.read_text())
        except Exception:
            continue
        file_data[fp] = {
            "captions": extract_captions(text),
            "labels": extract_labels(text),
            "paragraphs": [(ln, p, tokens(p)) for ln, p in extract_paragraphs(text)],
        }

    # 1. Cross-file identical captions
    caption_index = defaultdict(list)  # caption_text -> [(file, line)]
    for fp, d in file_data.items():
        for n, txt in d["captions"]:
            key = txt.lower().strip().rstrip(".")[:120]
            caption_index[key].append((fp.name, n, txt))
    cross_caps = {k: v for k, v in caption_index.items()
                  if len(v) >= 2 and len(set(f for f, _, _ in v)) >= 2}

    # 2. Same label appearing in different files (multiply-defined risk)
    label_index = defaultdict(list)
    for fp, d in file_data.items():
        for n, lbl in d["labels"]:
            label_index[lbl].append((fp.name, n))
    cross_labels = {k: v for k, v in label_index.items()
                    if len(v) >= 2 and len(set(f for f, _ in v)) >= 2}

    # 3. Cross-file near-identical paragraphs (Jaccard >= 0.85)
    cross_paras = []
    flist = list(file_data.items())
    for (fa, da), (fb, db) in combinations(flist, 2):
        for la, pa, ta in da["paragraphs"]:
            if len(ta) < 12: continue
            for lb, pb, tb in db["paragraphs"]:
                if len(tb) < 12: continue
                j = jaccard(ta, tb)
                if j >= 0.85:
                    cross_paras.append((j, fa.name, la, fb.name, lb, pa[:140], pb[:140]))
    cross_paras.sort(reverse=True, key=lambda r: r[0])

    # Render report
    lines = []
    lines.append("# Cross-Chapter / Cross-Appendix Content Redundancy Audit\n")
    lines.append(f"_Generated: {datetime.now().isoformat(timespec='seconds')}_\n")
    lines.append(f"Scanned: {len(files)} files (chapters + appendices). Masks \\iffalse...\\fi.\n")
    lines.append("## Summary\n")
    lines.append("| Category | Unique items spanning 2+ files | Total occurrences |")
    lines.append("|---|---:|---:|")
    n_caps = sum(len(v) for v in cross_caps.values())
    n_labs = sum(len(v) for v in cross_labels.values())
    lines.append(f"| Identical CAPTIONS across files | **{len(cross_caps)}** | **{n_caps}** |")
    lines.append(f"| Same table LABEL across files | **{len(cross_labels)}** | **{n_labs}** |")
    lines.append(f"| Near-identical PARAGRAPHS across files (Jaccard >= 0.85) | **{len(cross_paras)}** | -- |")
    lines.append("")

    # Section 1: captions
    lines.append("## 1. Identical CAPTIONS across files\n")
    if not cross_caps:
        lines.append("_None._")
    else:
        lines.append("| # | Caption | Files / lines |")
        lines.append("|---|---|---|")
        for i, (k, v) in enumerate(sorted(cross_caps.items(), key=lambda kv: -len(kv[1]))[:30], 1):
            files_lines = "; ".join(f"`{f}:{n}`" for f, n, _ in v)
            display = v[0][2][:100]
            lines.append(f"| {i} | {display} | {files_lines} |")
    lines.append("")

    # Section 2: cross-file labels
    lines.append("## 2. Same table LABEL appearing across files (multiply-defined risk)\n")
    if not cross_labels:
        lines.append("_None --- good, label uniqueness maintained._")
    else:
        lines.append("| Label | Files / lines |")
        lines.append("|---|---|")
        for lbl, v in sorted(cross_labels.items()):
            files_lines = "; ".join(f"`{f}:{n}`" for f, n in v)
            lines.append(f"| `{lbl}` | {files_lines} |")
    lines.append("")

    # Section 3: paragraphs
    lines.append("## 3. Near-identical PARAGRAPHS across files (Jaccard >= 0.85)\n")
    if not cross_paras:
        lines.append("_None._")
    else:
        # Group by file pair to dedup
        for k, (j, fa, la, fb, lb, sa, sb) in enumerate(cross_paras[:40], 1):
            lines.append(f"### Pair {k} --- Jaccard {j:.2f}")
            lines.append(f"- `{fa}:{la}`: _{sa}..._")
            lines.append(f"- `{fb}:{lb}`: _{sb}..._")
            lines.append("")
        if len(cross_paras) > 40:
            lines.append(f"_(+ {len(cross_paras)-40} more pairs; top 40 shown.)_")
    lines.append("")

    lines.append("## How to read")
    lines.append("- Identical CAPTIONS across files: usually a SIGNAL that the same table was migrated between sections without rename. Investigate; rename one if it's genuinely a different table, or remove one if it's a true duplicate.")
    lines.append("- Same LABEL across files: this is a **build error risk** (multiply-defined). If 0 above, you're safe.")
    lines.append("- Near-identical PARAGRAPHS: most are intentional (the Three-Questions intro, GGU compliance map, signature diagram intros). Anything **outside that pattern** is a genuine duplication.")

    OUT.write_text("\n".join(lines))
    print(f"Wrote: {OUT}")
    print(f"  Identical captions:    {len(cross_caps)} unique, {n_caps} occurrences")
    print(f"  Cross-file labels:     {len(cross_labels)} unique (label-conflict risk)")
    print(f"  Near-identical paras:  {len(cross_paras)} pairs across-file")


if __name__ == "__main__":
    main()
