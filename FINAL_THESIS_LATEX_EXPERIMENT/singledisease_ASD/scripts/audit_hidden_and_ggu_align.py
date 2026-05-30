#!/usr/bin/env python3
"""Read-only audit: (1) hidden content inside \\iffalse...\\fi blocks
per chapter, (2) GGU DBA template alignment check per chapter.

No .tex files are modified. Outputs a markdown report.
"""
import re
import sys
from pathlib import Path
from collections import defaultdict
from datetime import datetime

ROOT = Path(__file__).resolve().parents[1]
CHAPTERS_DIR = ROOT / "chapters"
OUT = ROOT.parent / "GGU_ALIGNMENT_AND_HIDDEN_REPORT_2026_05_30.md"

# Map chapter-id -> (display label, file basename or basenames, GGU required topics)
CH_FILES = {
    1: ("Chapter 1: Introduction",
        ["chapter1_introduction.tex"],
        [
            "Background",
            "Purpose",
            "Problem Statement",
            "Aim and Objectives",
            "Research Questions",
            "Hypothesis",
            "Context of the Contributing Organizations",
            "Significant contributions from the investigation",
            "Scope and assumptions",
            "Limitations",
            "Thesis Outline",
        ]),
    2: ("Chapter 2: Review of Literature",
        ["chapter2_literature.tex"],
        [
            "Overview of Related Literature",
            "Key Themes in the Literature",
            "Strengths and Limitations of Previous Research",
            "Identification of Research Gaps",
            "Critical Analysis of Gaps and Challenges",
            "Unresolved Issues in the Literature",
            "Limitations of Existing Studies",
            "Areas for Further Exploration",
            "Summary of Key Insights from Literature",
            "How the Study Contributes to Existing Knowledge",
            "Justification for Research Approach",
        ]),
    3: ("Chapter 3: Research Methods",
        sorted(p.name for p in CHAPTERS_DIR.glob("chapter3_*.tex")),
        [
            "Research Strategy and Research Design",
            "Research Approach",
            "Research Process",
            "Data Sources",
            "Data Collection Strategies",
            "Sampling Strategies",
            "Data Analysis Techniques",
            "Limitations of Methodology",
            "Ethical and Regulatory Considerations",
            "Evaluation Metrics",
            "Conclusion",
        ]),
    4: ("Chapter 4: Report on Data Analysis and Findings",
        ["chapter4_analysis_findings.tex"],
        [
            "Thematic Analysis of Collected Data",
            "Key Findings",
            "Quantitative and Qualitative Insights",
            "Integration with Existing Systems",
            "Findings in the context",
            "Contribution of the study",
            "Ethical and Regulatory Considerations",
        ]),
    5: ("Chapter 5: Discussion, Recommendation and Areas of further research",
        ["chapter5_discussion_recommendations.tex"],
        [
            "Interpretation of Findings",
            "Implications for Business and Practice",
            "Implications for Policy and Regulation",
            "Limitations of the Study",
            "Summary of Key Findings",
            "Recommendations and Areas of further research",
        ]),
}


def strip_comments(line: str) -> str:
    out = []
    i = 0
    while i < len(line):
        if line[i] == "%" and (i == 0 or line[i - 1] != "\\"):
            break
        out.append(line[i])
        i += 1
    return "".join(out)


def find_iffalse_blocks(text: str):
    """Return list of dicts: {start_line, end_line, n_lines, n_words,
    first_heading, sample_first_line, sample_last_line, kind}.
    Handles nested \\if*/\\fi within \\iffalse blocks."""
    lines = text.splitlines()
    blocks = []
    i = 0
    n = len(lines)
    while i < n:
        stripped = strip_comments(lines[i]).strip()
        m_open = re.match(r"\\iffalse\b", stripped)
        if not m_open:
            i += 1
            continue
        # Found start of an iffalse block at line i+1 (1-indexed)
        start_line = i + 1
        depth = 1
        j = i + 1
        block_lines = []
        while j < n and depth > 0:
            s = strip_comments(lines[j]).strip()
            if re.match(r"\\if[a-zA-Z]*\b", s):
                depth += 1
            elif re.match(r"\\fi\b", s):
                depth -= 1
                if depth == 0:
                    end_line = j + 1
                    break
            block_lines.append(lines[j])
            j += 1
        else:
            end_line = j  # EOF without matching \fi
        n_lines = len(block_lines)
        joined = " ".join(strip_comments(l).strip() for l in block_lines if strip_comments(l).strip())
        n_words = len(joined.split())
        # Capture first non-blank meaningful line and first heading inside
        first_real = next((strip_comments(l).strip() for l in block_lines
                           if strip_comments(l).strip()), "")
        # Find first heading inside
        first_head = None
        for l in block_lines:
            ls = strip_comments(l).strip()
            mh = re.match(r"\\(chapter|section|subsection|subsubsection|paragraph)\*?(?:\[[^\]]*\])?\{([^}]*)\}", ls)
            if mh:
                first_head = (mh.group(1), mh.group(2).strip())
                break
        # Classify what kind of content is hidden
        kinds = []
        body = "\n".join(block_lines)
        if re.search(r"\\begin\{(?:table|xltabular|tabularx|tabular|longtable)\}", body):
            kinds.append("table(s)")
        if re.search(r"\\begin\{(?:figure|tikzpicture)\}", body):
            kinds.append("figure(s)")
        if re.search(r"\\(?:sub)*section\*?\{", body):
            kinds.append("subsection(s)")
        if re.search(r"\\begin\{(?:enumerate|itemize|description)\}", body):
            kinds.append("list(s)")
        if not kinds and n_words > 20:
            kinds.append("prose")
        if not kinds:
            kinds.append("minor")
        blocks.append({
            "start_line": start_line,
            "end_line": end_line,
            "n_lines": n_lines,
            "n_words": n_words,
            "first_heading": first_head,
            "first_real_line": first_real[:160],
            "kinds": ", ".join(kinds),
        })
        i = end_line
    return blocks


def mask_suppressed(text: str) -> str:
    """Replace \\iffalse...\\fi content with blank lines (line numbers preserved)."""
    lines = text.splitlines()
    out = []
    in_false = 0
    if_depth = 0
    for raw in lines:
        s = strip_comments(raw).strip()
        if re.match(r"\\iffalse\b", s):
            in_false += 1
            out.append("")
            continue
        if in_false > 0:
            if re.match(r"\\if[a-zA-Z]*\b", s):
                if_depth += 1
            elif re.match(r"\\fi\b", s):
                if if_depth > 0:
                    if_depth -= 1
                else:
                    in_false -= 1
            out.append("")
            continue
        out.append(raw)
    return "\n".join(out)


def extract_headings(text: str):
    """List of (line_no, level, text). Operates on un-masked text;
    use mask_suppressed first if you want only active headings."""
    out = []
    for n, raw in enumerate(text.splitlines(), 1):
        s = strip_comments(raw).strip()
        m = re.match(r"\\(chapter|section|subsection|subsubsection|paragraph)\*?(?:\[[^\]]*\])?\{([^}]*)\}", s)
        if m:
            out.append((n, m.group(1), m.group(2).strip()))
    return out


def fuzzy_match_required(required: str, headings):
    """Check if the GGU-required topic is present in any heading.
    Strategy: case-insensitive substring match on stripped, alpha-only
    tokens; require at least 60% of required's tokens be present in
    the heading."""
    req_tokens = [t.lower() for t in re.findall(r"[A-Za-z]{3,}", required)]
    if not req_tokens:
        return None
    best = None
    best_score = 0.0
    for n, level, txt in headings:
        head_tokens = set(t.lower() for t in re.findall(r"[A-Za-z]{3,}", txt))
        matched = sum(1 for t in req_tokens if t in head_tokens)
        score = matched / max(len(req_tokens), 1)
        if score > best_score:
            best_score = score
            best = (n, level, txt, score)
    if best_score >= 0.6:
        return best
    return None


def main():
    blocks_per_ch = {}
    headings_active_per_ch = {}
    for ch_num, (label, files, _required) in CH_FILES.items():
        all_blocks = []
        all_active_heads = []
        for fn in files:
            fp = CHAPTERS_DIR / fn
            if not fp.exists():
                continue
            raw = fp.read_text()
            blocks = find_iffalse_blocks(raw)
            for b in blocks:
                b["file"] = fn
            all_blocks.extend(blocks)
            masked = mask_suppressed(raw)
            heads = extract_headings(masked)
            for h in heads:
                all_active_heads.append((fn,) + h)
        blocks_per_ch[ch_num] = all_blocks
        headings_active_per_ch[ch_num] = all_active_heads

    lines = []
    lines.append("# GGU DBA Template Alignment + Hidden Content Audit")
    lines.append("")
    lines.append(f"**Generated:** {datetime.now().isoformat(timespec='seconds')}")
    lines.append("**Status:** READ-ONLY audit. No `.tex` files modified, no content removed or moved.")
    lines.append("**Source-of-truth template:** GGU DBA Dissertation Thesis Preparation Guidelines (provided PDF)")
    lines.append("")
    lines.append("## What this report contains")
    lines.append("1. **Hidden Content per Chapter** --- every `\\iffalse...\\fi` suppressed block in the chapter source, with line range, size, kind of content, and first inner heading if any.")
    lines.append("2. **GGU Template Alignment per Chapter** --- for each GGU-required topic, whether it is present in the chapter's active (rendered) headings, and the closest match found.")
    lines.append("3. **Summary** --- per-chapter coverage % + total hidden words.")
    lines.append("")
    lines.append("Hidden content does NOT appear in the rendered PDF. If any hidden block is GGU-required, the chapter compliance gap is real and visible to an examiner reading the PDF.")
    lines.append("")

    # === Per-chapter sections ===
    total_hidden_blocks = 0
    total_hidden_words = 0
    coverage_summary = []

    for ch_num, (label, files, required) in CH_FILES.items():
        lines.append(f"## {label}")
        lines.append("")
        lines.append(f"**Files scanned:** {len(files)} (`{', '.join(files)}`)")
        lines.append("")

        # ----- Hidden content
        blocks = blocks_per_ch[ch_num]
        n_blocks = len(blocks)
        n_words = sum(b["n_words"] for b in blocks)
        total_hidden_blocks += n_blocks
        total_hidden_words += n_words
        lines.append(f"### Hidden content (`\\iffalse...\\fi` blocks)")
        lines.append("")
        lines.append(f"- Blocks: **{n_blocks}**")
        lines.append(f"- Total suppressed words: **{n_words:,}**")
        lines.append("")
        if n_blocks == 0:
            lines.append("_No hidden blocks in this chapter._")
        else:
            lines.append("| # | File | Lines | Words | Kind | First inner heading | Preview |")
            lines.append("|---|---|---|---:|---|---|---|")
            for k, b in enumerate(sorted(blocks, key=lambda b: -b["n_words"])[:40], 1):
                head_str = ""
                if b["first_heading"]:
                    head_str = f"`\\{b['first_heading'][0]}{{{b['first_heading'][1][:60]}}}`"
                else:
                    head_str = "_(none)_"
                preview = b["first_real_line"].replace("|", "\\|")[:80]
                lines.append(f"| {k} | `{b['file']}:{b['start_line']}-{b['end_line']}` | {b['end_line']-b['start_line']+1} | {b['n_words']:,} | {b['kinds']} | {head_str} | _{preview}..._ |")
            if n_blocks > 40:
                lines.append(f"| ... | _+{n_blocks - 40} more blocks, smaller_ | | | | | |")
        lines.append("")

        # ----- GGU alignment
        lines.append(f"### GGU template alignment ({len(required)} required topics)")
        lines.append("")
        active_heads = headings_active_per_ch[ch_num]
        # Build a heading list with location info
        heads_for_match = [(n, lvl, txt) for (fn, n, lvl, txt) in active_heads]
        present_count = 0
        lines.append("| GGU required topic | Present? | Closest match | Match score |")
        lines.append("|---|---|---|---:|")
        for req in required:
            m = fuzzy_match_required(req, heads_for_match)
            if m:
                present_count += 1
                n_h, lvl_h, txt_h, score = m
                lines.append(f"| {req} | YES | `\\{lvl_h}{{{txt_h[:70]}}}` | {score:.0%} |")
            else:
                # show best partial (best score even if below threshold)
                best = None
                best_score = 0.0
                req_tokens = [t.lower() for t in re.findall(r"[A-Za-z]{3,}", req)]
                for nh, lvlh, txth in heads_for_match:
                    head_tokens = set(t.lower() for t in re.findall(r"[A-Za-z]{3,}", txth))
                    s = sum(1 for t in req_tokens if t in head_tokens) / max(len(req_tokens), 1)
                    if s > best_score:
                        best_score = s
                        best = (nh, lvlh, txth)
                near_str = f"_(best partial: `\\{best[1]}{{{best[2][:60]}}}` @ {best_score:.0%})_" if best else "_(no near match)_"
                lines.append(f"| {req} | **NO** | {near_str} | {best_score:.0%} |")
        coverage_pct = present_count / len(required)
        lines.append("")
        lines.append(f"**Coverage:** {present_count} / {len(required)} required topics found ({coverage_pct:.0%}).")
        lines.append("")
        coverage_summary.append((ch_num, label, present_count, len(required), coverage_pct, n_blocks, n_words))

    # === Summary
    lines.append("## Cross-Chapter Summary")
    lines.append("")
    lines.append("| Chapter | GGU coverage | Hidden blocks | Hidden words |")
    lines.append("|---|---:|---:|---:|")
    for ch, label, p, t, pct, nb, nw in coverage_summary:
        lines.append(f"| Ch.{ch} | {p}/{t} ({pct:.0%}) | {nb} | {nw:,} |")
    lines.append("")
    lines.append(f"**Total hidden blocks across all chapters:** {total_hidden_blocks}")
    lines.append(f"**Total hidden words across all chapters:** {total_hidden_words:,}")
    lines.append("")
    lines.append("### How to read the alignment column")
    lines.append("- **YES** = GGU-required topic is present in the active (rendered) chapter headings at >=60% token match.")
    lines.append("- **NO** = no heading matched at >=60%; the chapter may still cover the topic in body prose rather than as a named heading, but examiner-scannability is reduced.")
    lines.append("")
    lines.append("### How to read the hidden-content table")
    lines.append("- 'Kind' tells you what type of content is inside the suppressed block (table, figure, prose, list).")
    lines.append("- 'First inner heading' is the first `\\section/subsection/...` *inside* the suppressed block (if any). If present, it means a once-named section is now invisible to the examiner.")
    lines.append("- High-word blocks marked 'prose' are the most likely candidates for review --- they were once written content, are now hidden, and may still be valuable.")

    OUT.write_text("\n".join(lines))
    print(f"Wrote: {OUT}")
    print(f"  - Total hidden blocks: {total_hidden_blocks}")
    print(f"  - Total hidden words : {total_hidden_words:,}")
    for ch, label, p, t, pct, nb, nw in coverage_summary:
        print(f"  - Ch.{ch} GGU coverage: {p}/{t} ({pct:.0%})  | hidden: {nb} blocks / {nw:,} words")


if __name__ == "__main__":
    main()
