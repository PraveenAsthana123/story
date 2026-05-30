#!/usr/bin/env python3
"""Read-only duplicate-detection audit for the dissertation.

Scans chapter .tex files and reports:
  1. Repeated SECTION/SUBSECTION HEADINGS (3+ occurrences of same heading text)
  2. Repeated CAPTION TEXT (3+ occurrences) -- usually a copy-paste indicator
  3. Repeated CONCEPT MENTIONS per chapter (RGAIG, governance maturity, etc.) --
     gives a density signal; cross-chapter recurrence is INTENTIONAL per
     the dissertation design pattern but extreme local density flags a
     candidate for editorial trimming
  4. NEAR-IDENTICAL paragraphs (Jaccard similarity >= 0.85 on token sets)
     across DIFFERENT chapters -- the strongest signal of true duplication

Each finding is tagged:
  [INTENTIONAL] -- known design pattern (signature diagram, P/S/H
                   methodology parallelism, recurring framework anchor)
  [PROBABLE-OK] -- normal concept recurrence
  [INVESTIGATE] -- worth a human eye

Output: ../DUPLICATE_AUDIT_REPORT_2026_05_30.md
No .tex files are modified.
"""
import re
import sys
from pathlib import Path
from collections import defaultdict, Counter
from datetime import datetime

ROOT = Path(__file__).resolve().parents[1]
CHAPTERS_DIR = ROOT / "chapters"
APPENDICES_DIR = ROOT / "appendices"
OUT = ROOT.parent / "DUPLICATE_AUDIT_REPORT_2026_05_30.md"

# Patterns that are INTENTIONAL by design (signature anchors, parallel structure)
INTENTIONAL_HEADINGS_RE = [
    re.compile(r"signature diagrams?", re.I),
    re.compile(r"examiner summary", re.I),
    re.compile(r"three questions this chapter answers", re.I),
    re.compile(r"template compliance additions", re.I),
    re.compile(r"GGU.*compliance", re.I),
    # Ch.3 P/S/H parallelism: same subheading reused per stream is OK
    re.compile(r"^primary data", re.I),
    re.compile(r"^secondary data", re.I),
    re.compile(r"^hybrid data", re.I),
    re.compile(r"data preparation", re.I),
    re.compile(r"data collection", re.I),
    re.compile(r"preprocessing", re.I),
]

# Concepts whose recurrence across chapters is BY DESIGN
INTENTIONAL_CONCEPTS = {
    "RGAIG", "governance maturity", "explainability", "trust",
    "adoption readiness", "PLS-SEM", "TAM",
    "ASD", "EEG", "responsible AI", "B2C", "B2B", "SHAP",
}

CHAPTER_FILES = sorted(CHAPTERS_DIR.glob("chapter*.tex"))


def strip_comments(line: str) -> str:
    """Remove LaTeX comments (% to EOL, except \\%)."""
    out = []
    i = 0
    while i < len(line):
        if line[i] == "%" and (i == 0 or line[i - 1] != "\\"):
            break
        out.append(line[i])
        i += 1
    return "".join(out)


def mask_suppressed_blocks(text: str) -> str:
    """Replace content inside \\iffalse...\\fi blocks with blank lines so the
    line numbers stay stable but the suppressed content is invisible to
    downstream extractors. Handles nested \\if/\\fi by counting depth."""
    lines = text.splitlines()
    out = []
    in_false = 0  # depth counter for \iffalse blocks
    if_depth = 0  # generic \if depth (only matters for nesting inside iffalse)
    for raw in lines:
        stripped = strip_comments(raw).strip()
        # Detect start of an \iffalse block at the start of in_false counter
        if re.match(r"\\iffalse\b", stripped):
            in_false += 1
            out.append("")  # blank line, preserves line numbering
            continue
        if in_false > 0:
            # Track nested \if* so \fi pairs match correctly
            if re.match(r"\\if[a-zA-Z]*\b", stripped):
                if_depth += 1
            elif re.match(r"\\fi\b", stripped):
                if if_depth > 0:
                    if_depth -= 1
                else:
                    in_false -= 1
            out.append("")  # blank out suppressed line
            continue
        out.append(raw)
    return "\n".join(out)


def extract_headings(text: str):
    """Return list of (line_no, level, heading_text) tuples."""
    headings = []
    for n, raw in enumerate(text.splitlines(), 1):
        line = strip_comments(raw).strip()
        m = re.match(r"\\(chapter|section|subsection|subsubsection|paragraph)\*?(?:\[[^\]]*\])?\{([^}]*)\}", line)
        if m:
            level, txt = m.group(1), m.group(2).strip()
            headings.append((n, level, txt))
    return headings


def extract_captions(text: str):
    """Return list of (line_no, caption_text) tuples for \\caption[short]{long} or \\caption{long}."""
    caps = []
    for n, raw in enumerate(text.splitlines(), 1):
        line = strip_comments(raw)
        m = re.search(r"\\caption(?:\[[^\]]*\])?\{([^}]+)\}", line)
        if m:
            caps.append((n, m.group(1).strip().rstrip(".")))
    return caps


def count_concept_mentions(text: str):
    """Return Counter of intentional concept mentions."""
    cnt = Counter()
    for concept in INTENTIONAL_CONCEPTS:
        # word-boundary case-insensitive
        rx = re.compile(rf"\b{re.escape(concept)}\b", re.I)
        cnt[concept] = len(rx.findall(text))
    return cnt


def tokenize_for_jaccard(para: str):
    """Lowercase, keep alphanumeric tokens length >= 4."""
    return set(w for w in re.findall(r"[a-zA-Z]{4,}", para.lower()))


def extract_paragraphs(text: str, min_words=30):
    """Return list of (line_no, paragraph_text) for prose paragraphs.

    Skip if the paragraph contains LaTeX block-environment markers
    (\\begin{table}, \\begin{tikzpicture}, etc.).
    """
    paras = []
    cur_lines = []
    cur_start = 1
    for n, raw in enumerate(text.splitlines(), 1):
        stripped = strip_comments(raw).rstrip()
        if not stripped:
            if cur_lines:
                joined = " ".join(cur_lines).strip()
                if (len(joined.split()) >= min_words
                    and not any(
                        m in joined
                        for m in ("\\begin{table}", "\\begin{tikzpicture}",
                                  "\\begin{xltabular}", "\\caption[",
                                  "\\toprule", "\\midrule")
                    )):
                    paras.append((cur_start, joined))
                cur_lines = []
            continue
        if not cur_lines:
            cur_start = n
        cur_lines.append(stripped)
    if cur_lines:
        joined = " ".join(cur_lines).strip()
        if len(joined.split()) >= min_words:
            paras.append((cur_start, joined))
    return paras


def tag_heading(text: str) -> str:
    for rx in INTENTIONAL_HEADINGS_RE:
        if rx.search(text):
            return "INTENTIONAL"
    return "INVESTIGATE"


def main():
    if not CHAPTER_FILES:
        sys.exit(f"No chapter files found in {CHAPTERS_DIR}")

    # Collect data per file. Mask \iffalse...\fi blocks so suppressed
    # content does NOT register as duplicate (it isn't rendered).
    file_data = {}
    for fp in CHAPTER_FILES:
        raw_text = fp.read_text()
        text = mask_suppressed_blocks(raw_text)
        file_data[fp] = {
            "text": text,
            "headings": extract_headings(text),
            "captions": extract_captions(text),
            "concepts": count_concept_mentions(text),
            "paragraphs": extract_paragraphs(text),
        }

    # === 1. Repeated headings ===
    heading_index = defaultdict(list)  # heading_text -> [(file, line, level)]
    for fp, data in file_data.items():
        for n, level, txt in data["headings"]:
            heading_index[txt.lower()].append((fp.name, n, level, txt))

    repeated_headings = {k: v for k, v in heading_index.items() if len(v) >= 3}

    # === 2. Repeated captions ===
    caption_index = defaultdict(list)
    for fp, data in file_data.items():
        for n, txt in data["captions"]:
            caption_index[txt.lower()].append((fp.name, n, txt))
    repeated_captions = {k: v for k, v in caption_index.items() if len(v) >= 2}

    # === 3. Concept density ===
    concept_per_file = {}
    for fp, data in file_data.items():
        concept_per_file[fp.name] = data["concepts"]

    # === 4. Cross-chapter near-identical paragraphs (Jaccard >= 0.85) ===
    # Only compare paragraphs across DIFFERENT files
    file_paras = [(fp.name, n, p, tokenize_for_jaccard(p))
                  for fp, data in file_data.items()
                  for n, p in data["paragraphs"]]
    near_dups = []
    n = len(file_paras)
    for i in range(n):
        f_i, ln_i, p_i, t_i = file_paras[i]
        if len(t_i) < 10:
            continue
        for j in range(i + 1, n):
            f_j, ln_j, p_j, t_j = file_paras[j]
            if f_i == f_j:
                continue
            if len(t_j) < 10:
                continue
            inter = len(t_i & t_j)
            union = len(t_i | t_j)
            if union == 0:
                continue
            jacc = inter / union
            if jacc >= 0.85:
                near_dups.append((jacc, f_i, ln_i, f_j, ln_j, p_i[:140], p_j[:140]))
    near_dups.sort(reverse=True, key=lambda r: r[0])

    # === Write report ===
    out_lines = []
    out_lines.append(f"# Duplicate Audit Report --- Read-Only")
    out_lines.append(f"")
    out_lines.append(f"Generated: {datetime.now().isoformat(timespec='seconds')}")
    out_lines.append(f"Scope: {len(file_data)} chapter files under `chapters/`")
    out_lines.append(f"Status: **AUDIT ONLY** --- no `.tex` files modified by this script")
    out_lines.append("")
    out_lines.append("## Legend")
    out_lines.append("- `[INTENTIONAL]` --- known design pattern (signature anchors, P/S/H methodology parallelism, recurring framework refs). Leave as is.")
    out_lines.append("- `[INVESTIGATE]` --- not in the known design pattern catalogue. Worth a human eye before any edit.")
    out_lines.append("")

    # ---- Section 1: Repeated headings
    out_lines.append("## 1. Repeated Headings (3+ occurrences of same heading text)")
    out_lines.append("")
    if not repeated_headings:
        out_lines.append("_None found._")
    else:
        out_lines.append(f"Found **{len(repeated_headings)} repeated heading text(s)**.")
        out_lines.append("")
        out_lines.append("| Tag | Heading text | Files / lines |")
        out_lines.append("|---|---|---|")
        for txt_lower, occurrences in sorted(repeated_headings.items(), key=lambda kv: -len(kv[1])):
            tag = tag_heading(occurrences[0][3])
            files_lines = "; ".join(f"`{f}:{n}` ({lvl})" for f, n, lvl, _ in occurrences)
            display = occurrences[0][3][:80]
            out_lines.append(f"| `{tag}` | {display} | {files_lines} |")
    out_lines.append("")

    # ---- Section 2: Repeated captions
    out_lines.append("## 2. Repeated Caption Text (2+ occurrences)")
    out_lines.append("")
    if not repeated_captions:
        out_lines.append("_None found._")
    else:
        out_lines.append(f"Found **{len(repeated_captions)} repeated caption text(s)**.")
        out_lines.append("Captions are usually unique per table/figure; repeats may indicate a copy-paste opportunity for editing.")
        out_lines.append("")
        out_lines.append("| Caption text | Files / lines |")
        out_lines.append("|---|---|")
        for txt_lower, occurrences in sorted(repeated_captions.items(), key=lambda kv: -len(kv[1])):
            files_lines = "; ".join(f"`{f}:{n}`" for f, n, _ in occurrences)
            display = occurrences[0][2][:80]
            out_lines.append(f"| {display} | {files_lines} |")
    out_lines.append("")

    # ---- Section 3: Concept density per chapter (informational)
    out_lines.append("## 3. Concept Mention Density per Chapter (informational)")
    out_lines.append("")
    out_lines.append("Cross-chapter recurrence is the dissertation's design pattern (Ch.1 introduces, Ch.2 justifies, etc.). Use this table to spot **extreme local density** within a single chapter, which can signal repetition worth editorial trimming.")
    out_lines.append("")
    header = ["File"] + sorted(INTENTIONAL_CONCEPTS)
    out_lines.append("| " + " | ".join(header) + " |")
    out_lines.append("|" + "---|" * len(header))
    for fp_name in sorted(concept_per_file):
        cnts = concept_per_file[fp_name]
        row = [fp_name] + [str(cnts[c]) for c in sorted(INTENTIONAL_CONCEPTS)]
        out_lines.append("| " + " | ".join(row) + " |")
    out_lines.append("")

    # ---- Section 4: Cross-chapter near-identical paragraphs
    out_lines.append("## 4. Near-Identical Paragraphs Across Different Chapters (Jaccard >= 0.85)")
    out_lines.append("")
    if not near_dups:
        out_lines.append("_None found._")
    else:
        out_lines.append(f"Found **{len(near_dups)} cross-file near-identical paragraph pair(s)** at Jaccard token-set similarity >= 0.85.")
        out_lines.append("Same paragraph appearing in two chapters is the strongest signal of true accidental duplication.")
        out_lines.append("")
        # Show top 30 only
        for k, (jacc, f_i, ln_i, f_j, ln_j, snip_i, snip_j) in enumerate(near_dups[:30], 1):
            out_lines.append(f"### Pair {k} --- Jaccard {jacc:.2f}")
            out_lines.append(f"- `{f_i}:{ln_i}`: _{snip_i}..._")
            out_lines.append(f"- `{f_j}:{ln_j}`: _{snip_j}..._")
            out_lines.append("")
        if len(near_dups) > 30:
            out_lines.append(f"_(+ {len(near_dups) - 30} more pairs; only top 30 shown.)_")
    out_lines.append("")

    # ---- Summary
    out_lines.append("## Summary")
    out_lines.append("")
    out_lines.append(f"- Repeated headings (3+): **{len(repeated_headings)}**")
    out_lines.append(f"- Repeated captions (2+): **{len(repeated_captions)}**")
    out_lines.append(f"- Cross-chapter near-identical paragraphs (Jaccard >= 0.85): **{len(near_dups)}**")
    out_lines.append("")
    out_lines.append("**Recommendation.** Items tagged `[INTENTIONAL]` should remain unchanged (design pattern). Items tagged `[INVESTIGATE]` and near-identical paragraph pairs are the candidates for a human-led editorial pass, **not for automatic removal**.")

    OUT.write_text("\n".join(out_lines))
    print(f"Wrote: {OUT}")
    print(f"  - {len(repeated_headings)} repeated heading texts")
    print(f"  - {len(repeated_captions)} repeated caption texts")
    print(f"  - {len(near_dups)} cross-file near-identical paragraph pairs")


if __name__ == "__main__":
    main()
