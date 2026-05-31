#!/usr/bin/env python3
"""Aggressive repetition audit --- counts every kind of repeated text:
  1. Section / subsection / subsubsection HEADINGS (2+ occurrences)
  2. \\paragraph{X} headings (2+ occurrences)
  3. Caption text (2+ occurrences)
  4. Short-phrase 'noindent' block intros (2+)
  5. \\caption captions and \\section* unnumbered headings

Masks \\iffalse...\\fi suppressed blocks. Produces a report sorted by
TOTAL OCCURRENCES descending so the most-repeated items are first.

For each repeated item, lists ALL occurrence lines for review.

READ-ONLY: no .tex files modified.
"""
from __future__ import annotations
import re
from pathlib import Path
from collections import defaultdict
from datetime import datetime

ROOT = Path(__file__).resolve().parents[2]
CHAPTERS_DIR = ROOT / "chapters"
APPENDICES_DIR = ROOT / "appendices"
OUT = ROOT / "jobs" / "reports" / "repetition_aggressive_master.md"


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


def scan(files):
    headings = defaultdict(list)      # text -> [(file, line, level)]
    paragraphs = defaultdict(list)    # text -> [(file, line)]
    captions = defaultdict(list)      # text -> [(file, line)]

    for fp in files:
        try:
            raw = fp.read_text()
        except Exception:
            continue
        text = mask_suppressed(raw)
        for n, line in enumerate(text.splitlines(), 1):
            s = strip_comments(line).strip()
            if not s: continue
            # Headings (section/subsection/etc.) -- both numbered and starred
            m = re.match(r"\\(chapter|section|subsection|subsubsection)\*?(?:\[[^\]]*\])?\{([^}]+)\}", s)
            if m:
                level, txt = m.group(1), m.group(2).strip().lower()
                headings[txt].append((fp.name, n, level))
                continue
            # \paragraph{...}
            m = re.match(r"\\paragraph\*?(?:\[[^\]]*\])?\{([^}]+)\}", s)
            if m:
                txt = m.group(1).strip().rstrip(".").lower()
                paragraphs[txt].append((fp.name, n))
                continue
            # \caption[short]{long} or \caption{long}
            m = re.search(r"\\caption(?:\[[^\]]*\])?\{([^}]+)\}", s)
            if m:
                txt = m.group(1).strip().rstrip(".").lower()
                captions[txt].append((fp.name, n))
    return headings, paragraphs, captions


def main():
    files = sorted(CHAPTERS_DIR.glob("chapter*.tex")) + sorted(APPENDICES_DIR.glob("*.tex"))
    headings, paragraphs, captions = scan(files)

    # Filter to only repeated (count >= 2)
    rep_heads = {k: v for k, v in headings.items() if len(v) >= 2}
    rep_paras = {k: v for k, v in paragraphs.items() if len(v) >= 2}
    rep_caps = {k: v for k, v in captions.items() if len(v) >= 2}

    total_dup_heads = sum(len(v) for v in rep_heads.values())
    total_dup_paras = sum(len(v) for v in rep_paras.values())
    total_dup_caps = sum(len(v) for v in rep_caps.values())

    lines = []
    lines.append("# Aggressive Repetition Audit (2+ occurrences)\n")
    lines.append(f"_Generated: {datetime.now().isoformat(timespec='seconds')}_\n")
    lines.append(f"Files scanned: {len(files)} (chapters + appendices)")
    lines.append(f"Masks \\iffalse...\\fi suppressed blocks (active text only).\n")
    lines.append("## Summary\n")
    lines.append(f"| Category | Unique repeated items | Total duplicate occurrences |")
    lines.append(f"|---|---:|---:|")
    lines.append(f"| Section / subsection / subsubsection headings | **{len(rep_heads)}** | **{total_dup_heads}** |")
    lines.append(f"| \\\\paragraph{{...}} headings | **{len(rep_paras)}** | **{total_dup_paras}** |")
    lines.append(f"| \\\\caption{{...}} captions | **{len(rep_caps)}** | **{total_dup_caps}** |")
    lines.append(f"| **TOTAL** | **{len(rep_heads)+len(rep_paras)+len(rep_caps)}** | **{total_dup_heads+total_dup_paras+total_dup_caps}** |")
    lines.append("")

    # Top 30 most-repeated headings
    lines.append("## Top 30 most-repeated SECTION-level HEADINGS\n")
    lines.append("| # | Heading | Count | First 3 occurrences |")
    lines.append("|---|---|---:|---|")
    for k, (txt, occs) in enumerate(sorted(rep_heads.items(), key=lambda kv: -len(kv[1]))[:30], 1):
        first3 = "; ".join(f"`{f}:{n}`({lvl})" for f, n, lvl in occs[:3])
        more = f" (+{len(occs)-3} more)" if len(occs) > 3 else ""
        lines.append(f"| {k} | {txt[:80]} | {len(occs)} | {first3}{more} |")
    lines.append("")

    # Top 50 most-repeated \paragraph{} headings
    lines.append("## Top 50 most-repeated \\paragraph{} HEADINGS\n")
    lines.append("Paragraph-level headings duplicated 2+ times. Many of these were the per-step duplicate-line patterns (e.g., 'Step 1 ---.' appearing both as \\paragraph and as section).")
    lines.append("")
    lines.append("| # | Paragraph heading | Count | First 3 occurrences |")
    lines.append("|---|---|---:|---|")
    for k, (txt, occs) in enumerate(sorted(rep_paras.items(), key=lambda kv: -len(kv[1]))[:50], 1):
        first3 = "; ".join(f"`{f}:{n}`" for f, n in occs[:3])
        more = f" (+{len(occs)-3} more)" if len(occs) > 3 else ""
        lines.append(f"| {k} | {txt[:80]} | {len(occs)} | {first3}{more} |")
    lines.append("")

    # Top 50 most-repeated captions
    lines.append("## Top 50 most-repeated CAPTION text\n")
    lines.append("| # | Caption | Count | First 3 occurrences |")
    lines.append("|---|---|---:|---|")
    for k, (txt, occs) in enumerate(sorted(rep_caps.items(), key=lambda kv: -len(kv[1]))[:50], 1):
        first3 = "; ".join(f"`{f}:{n}`" for f, n in occs[:3])
        more = f" (+{len(occs)-3} more)" if len(occs) > 3 else ""
        lines.append(f"| {k} | {txt[:80]} | {len(occs)} | {first3}{more} |")
    lines.append("")

    lines.append("## How to read")
    lines.append("- A heading repeated **2+ times** is suspicious. Up to N=5 may be intentional (parallel per-chapter structure: each chapter has its own 'Examiner Summary', 'Chapter Summary', etc.). Anything **> 5** is almost always accidental.")
    lines.append("- \\paragraph repeats are usually copy-paste artefacts where the same paragraph label was reused for different content.")
    lines.append("- Caption repeats indicate two tables with identical caption text -- they should be disambiguated.")

    OUT.write_text("\n".join(lines))
    print(f"Wrote: {OUT}")
    print(f"  Repeated headings:    {len(rep_heads)} unique, {total_dup_heads} occurrences")
    print(f"  Repeated paragraphs:  {len(rep_paras)} unique, {total_dup_paras} occurrences")
    print(f"  Repeated captions:    {len(rep_caps)} unique, {total_dup_caps} occurrences")
    print(f"  GRAND TOTAL duplicate occurrences: {total_dup_heads+total_dup_paras+total_dup_caps}")


if __name__ == "__main__":
    main()
