#!/usr/bin/env python3
"""Read-only audit: for each chapter, classify every ACTIVE (rendered)
heading as either:
  GGU-REQUIRED  --- matches a GGU template required topic at >=60% tokens
  META          --- intentional navigation/structure I added (Examiner Summary,
                    Signature Diagrams, Three Questions, Compliance Map,
                    Template Compliance Additions, Executive Tables, etc.)
  EXTRA-CONTENT --- genuine additional content beyond the GGU template

Outputs: ../GGU_EXTRA_HEADINGS_REPORT_2026_05_30.md
No .tex files are modified.
"""
import re
import sys
from pathlib import Path
from collections import defaultdict
from datetime import datetime

ROOT = Path(__file__).resolve().parents[1]
CHAPTERS_DIR = ROOT / "chapters"
OUT = ROOT.parent / "GGU_EXTRA_HEADINGS_REPORT_2026_05_30.md"

CH_FILES = {
    1: ("Chapter 1: Introduction",
        ["chapter1_introduction.tex"],
        ["Background", "Purpose", "Problem Statement", "Aim and Objectives",
         "Research Questions", "Hypothesis", "Context of the Contributing Organizations",
         "Significant contributions from the investigation", "Scope and assumptions",
         "Limitations", "Thesis Outline"]),
    2: ("Chapter 2: Review of Literature",
        ["chapter2_literature.tex"],
        ["Overview of Related Literature", "Key Themes in the Literature",
         "Strengths and Limitations of Previous Research", "Identification of Research Gaps",
         "Critical Analysis of Gaps and Challenges", "Unresolved Issues in the Literature",
         "Limitations of Existing Studies", "Areas for Further Exploration",
         "Summary of Key Insights from Literature",
         "How the Study Contributes to Existing Knowledge",
         "Justification for Research Approach"]),
    3: ("Chapter 3: Research Methods",
        sorted(p.name for p in CHAPTERS_DIR.glob("chapter3_*.tex")),
        ["Research Strategy and Research Design", "Research Approach",
         "Research Process", "Data Sources", "Data Collection Strategies",
         "Sampling Strategies", "Data Analysis Techniques",
         "Limitations of Methodology", "Ethical and Regulatory Considerations",
         "Evaluation Metrics", "Conclusion"]),
    4: ("Chapter 4: Report on Data Analysis and Findings",
        ["chapter4_analysis_findings.tex"],
        ["Thematic Analysis of Collected Data", "Key Findings",
         "Quantitative and Qualitative Insights", "Integration with Existing Systems",
         "Findings in the context", "Contribution of the study",
         "Ethical and Regulatory Considerations"]),
    5: ("Chapter 5: Discussion, Recommendation and Areas of further research",
        ["chapter5_discussion_recommendations.tex"],
        ["Interpretation of Findings", "Implications for Business and Practice",
         "Implications for Policy and Regulation", "Limitations of the Study",
         "Summary of Key Findings",
         "Recommendations and Areas of further research"]),
}

# Patterns that classify a heading as META (intentional navigation/structure)
META_PATTERNS = [
    (re.compile(r"examiner summary", re.I), "Examiner Summary"),
    (re.compile(r"signature diagrams?", re.I), "Signature Diagrams"),
    (re.compile(r"three questions this chapter", re.I), "Three-Questions Landing"),
    (re.compile(r"GGU.*compliance|compliance map", re.I), "GGU Compliance Map"),
    (re.compile(r"template compliance additions", re.I), "Template Compliance Pack"),
    (re.compile(r"executive table:", re.I), "Executive Summary Table"),
    (re.compile(r"chapter \d+ ", re.I), "Chapter-titled meta"),
    (re.compile(r"key sections covered", re.I), "Key Sections Covered (KIT)"),
    (re.compile(r"^chapter \w+$", re.I), "Chapter title"),
    (re.compile(r"chapter (synthesis|summary|objective|kit|recap)", re.I), "Chapter wrap-up"),
    (re.compile(r"lens map summary", re.I), "Lens Map Summary"),
    (re.compile(r"sequence flow|flow document", re.I), "GGU sequence flow"),
    (re.compile(r"defensibility (pack|note|matrix)", re.I), "Defensibility Pack"),
    (re.compile(r"DBA and research significance", re.I), "DBA Significance Block"),
    (re.compile(r"objective achievement matrix", re.I), "Objective Achievement Matrix"),
    (re.compile(r"supplementary material", re.I), "Supplementary Material pointer"),
    (re.compile(r"key findings$", re.I), "Key Findings (GGU + meta overlap)"),  # both
    (re.compile(r"introduction$", re.I), "Section/Chapter Introduction"),
    (re.compile(r"^purpose$", re.I), "Purpose (GGU)"),  # both
    (re.compile(r"GGU DBA", re.I), "GGU Reference"),
]


def strip_comments(line: str) -> str:
    out = []
    i = 0
    while i < len(line):
        if line[i] == "%" and (i == 0 or line[i - 1] != "\\"):
            break
        out.append(line[i])
        i += 1
    return "".join(out)


def mask_suppressed(text: str) -> str:
    """Replace \\iffalse...\\fi content with blank lines."""
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


def extract_active_headings(text: str):
    """Returns list of (line_no, level, text) for non-suppressed headings.
    Includes section + subsection levels only (skip subsubsection/paragraph
    noise to keep the report scannable)."""
    masked = mask_suppressed(text)
    out = []
    for n, raw in enumerate(masked.splitlines(), 1):
        s = strip_comments(raw).strip()
        m = re.match(r"\\(chapter|section|subsection)\*?(?:\[[^\]]*\])?\{([^}]*)\}", s)
        if m:
            out.append((n, m.group(1), m.group(2).strip()))
    return out


def fuzzy_score(required: str, heading: str) -> float:
    req_tokens = [t.lower() for t in re.findall(r"[A-Za-z]{3,}", required)]
    head_tokens = set(t.lower() for t in re.findall(r"[A-Za-z]{3,}", heading))
    if not req_tokens:
        return 0.0
    return sum(1 for t in req_tokens if t in head_tokens) / len(req_tokens)


def classify_heading(heading_text: str, ggu_required: list[str]) -> tuple[str, str]:
    """Return (category, detail).
    category in {'GGU-REQUIRED', 'META', 'EXTRA-CONTENT'}
    detail = matched topic name or meta pattern label
    """
    # Check META first (some meta patterns are also GGU-overlapping; ambiguous
    # ones tagged in the pattern label).
    for rx, label in META_PATTERNS:
        if rx.search(heading_text):
            # If this is also a GGU-required topic name, prefer GGU tag.
            for req in ggu_required:
                if fuzzy_score(req, heading_text) >= 0.6:
                    return ("GGU-REQUIRED", req)
            return ("META", label)
    # Check GGU-REQUIRED
    best_req = None
    best_score = 0.0
    for req in ggu_required:
        s = fuzzy_score(req, heading_text)
        if s > best_score:
            best_score = s
            best_req = req
    if best_score >= 0.6:
        return ("GGU-REQUIRED", best_req)
    # Default: EXTRA-CONTENT
    return ("EXTRA-CONTENT", "")


def main():
    lines = []
    lines.append("# Additional (Beyond-GGU) Headings --- Per Chapter Audit")
    lines.append("")
    lines.append(f"**Generated:** {datetime.now().isoformat(timespec='seconds')}")
    lines.append("**Status:** READ-ONLY. No `.tex` files modified, no content moved or removed.")
    lines.append("**Source-of-truth template:** GGU DBA Dissertation Thesis Preparation Guidelines (PDF you provided)")
    lines.append("")
    lines.append("## Classification key")
    lines.append("- **GGU-REQUIRED** --- heading matches a GGU template topic at >=60% token overlap. Required by template.")
    lines.append("- **META** --- intentional navigation/structure heading (Examiner Summary, Signature Diagrams, Three-Questions Landing, GGU Compliance Map, Template Compliance Additions, Executive Tables, Chapter Synthesis, Defensibility Pack, etc.). Added on purpose for examiner navigability.")
    lines.append("- **EXTRA-CONTENT** --- additional substantive content beyond GGU template and beyond META navigation. These are the headings that EXPAND the dissertation's scope past the template baseline.")
    lines.append("")
    lines.append("Only `\\chapter`, `\\section`, and `\\subsection` levels are listed (subsubsections + paragraphs are excluded to keep the report scannable).")
    lines.append("")

    summary_rows = []
    for ch_num, (label, files, required) in CH_FILES.items():
        # Collect all active headings
        all_heads = []  # list of (fn, line, level, text)
        for fn in files:
            fp = CHAPTERS_DIR / fn
            if not fp.exists():
                continue
            txt = fp.read_text()
            for (n, lvl, t) in extract_active_headings(txt):
                all_heads.append((fn, n, lvl, t))

        # Classify
        ggu, meta, extra = [], [], []
        for fn, n, lvl, t in all_heads:
            cat, detail = classify_heading(t, required)
            entry = (fn, n, lvl, t, detail)
            if cat == "GGU-REQUIRED":
                ggu.append(entry)
            elif cat == "META":
                meta.append(entry)
            else:
                extra.append(entry)

        total = len(all_heads)
        summary_rows.append((ch_num, label, total, len(ggu), len(meta), len(extra)))

        lines.append(f"## {label}")
        lines.append("")
        lines.append(f"**Files scanned:** {len(files)} file(s); **active headings:** {total}")
        lines.append("")
        lines.append(f"- GGU-REQUIRED headings: **{len(ggu)}**")
        lines.append(f"- META (navigation) headings: **{len(meta)}**")
        lines.append(f"- EXTRA-CONTENT headings: **{len(extra)}**")
        lines.append("")

        # META section
        lines.append(f"### META headings in {label} ({len(meta)})")
        if not meta:
            lines.append("_None._")
        else:
            lines.append("| # | Level | Heading | Meta type | File:line |")
            lines.append("|---|---|---|---|---|")
            for k, (fn, n, lvl, t, detail) in enumerate(meta, 1):
                short_t = t[:70] + ("..." if len(t) > 70 else "")
                lines.append(f"| {k} | {lvl} | {short_t} | {detail} | `{fn}:{n}` |")
        lines.append("")

        # EXTRA-CONTENT section
        lines.append(f"### EXTRA-CONTENT headings in {label} ({len(extra)})")
        lines.append("")
        lines.append("These are the headings that go BEYOND the GGU template baseline AND beyond the META navigation structure. They represent the dissertation's actual content expansion.")
        lines.append("")
        if not extra:
            lines.append("_None --- chapter strictly follows GGU template + META navigation._")
        else:
            # Group by level for readability
            by_level = defaultdict(list)
            for entry in extra:
                by_level[entry[2]].append(entry)
            for lvl in ["chapter", "section", "subsection"]:
                if lvl not in by_level:
                    continue
                lines.append(f"#### {lvl.title()}-level extras ({len(by_level[lvl])})")
                lines.append("| # | Heading | File:line |")
                lines.append("|---|---|---|")
                for k, (fn, n, _l, t, _d) in enumerate(by_level[lvl], 1):
                    short_t = t[:90] + ("..." if len(t) > 90 else "")
                    lines.append(f"| {k} | {short_t} | `{fn}:{n}` |")
                lines.append("")

        lines.append("---")
        lines.append("")

    # Summary
    lines.append("## Cross-Chapter Summary")
    lines.append("")
    lines.append("| Chapter | Active headings | GGU-required | META | EXTRA-CONTENT |")
    lines.append("|---|---:|---:|---:|---:|")
    grand_total = grand_ggu = grand_meta = grand_extra = 0
    for ch, label, t, g, m, e in summary_rows:
        lines.append(f"| Ch.{ch} | {t} | {g} | {m} | {e} |")
        grand_total += t; grand_ggu += g; grand_meta += m; grand_extra += e
    lines.append(f"| **TOTAL** | **{grand_total}** | **{grand_ggu}** | **{grand_meta}** | **{grand_extra}** |")
    lines.append("")
    lines.append(f"**Reading the totals:**")
    lines.append(f"- {grand_ggu} of {grand_total} active headings ({grand_ggu/max(grand_total,1):.0%}) map to GGU template topics.")
    lines.append(f"- {grand_meta} of {grand_total} ({grand_meta/max(grand_total,1):.0%}) are intentional navigation/structure (Examiner Summary, Signature Diagrams, Three-Questions, Compliance Map, etc.) --- added on purpose for examiner navigability.")
    lines.append(f"- {grand_extra} of {grand_total} ({grand_extra/max(grand_total,1):.0%}) are EXTRA-CONTENT --- substantive content beyond what GGU strictly requires.")
    lines.append("")
    lines.append("**What 'EXTRA-CONTENT' means in practice.** Every dissertation needs more headings than the GGU template's bullet list, because the template lists topic areas, not the actual section structure. The EXTRA-CONTENT count is the number of substantive subsections the dissertation has added to develop those topic areas. High count = thorough; very high count = potentially over-elaborated. The per-chapter tables above let you scan whether each extra carries its weight.")

    OUT.write_text("\n".join(lines))
    print(f"Wrote: {OUT}")
    for ch, label, t, g, m, e in summary_rows:
        print(f"  Ch.{ch}: {t} active headings | {g} GGU-req | {m} META | {e} EXTRA-CONTENT")


if __name__ == "__main__":
    main()
