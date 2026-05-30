#!/usr/bin/env python3
"""
GGU Per-Chapter Rollup Audit
==============================

Aggregates ALL audit findings (tables, figures, pages, overflows, intros)
into a single per-chapter scorecard.

Reads latest of each audit JSON:
  - advanced_table_quality_*.json    → table issues per chapter
  - bottom_overflow_visual_*.json    → bottom-overflow pages per chapter
  - per_page_visual_*.json           → sparse pages per chapter
  - table_intro_quality_*.json       → intro quality per chapter
  - tikz_overlap_*.json (if exists)  → figure overlaps per chapter

Output: jobs/reports/chapter_rollup_YYYYMMDD_HHMM.md
"""
import json
import re
import sys
from pathlib import Path
from datetime import datetime
from collections import defaultdict

ROOT = Path(__file__).resolve().parents[2]
OUT_DIR = ROOT / "jobs" / "reports"
TS = datetime.now().strftime("%Y%m%d_%H%M")
OUT_MD = OUT_DIR / f"chapter_rollup_{TS}.md"

CHAPTERS = {
    "chapter1": "Ch.1 Introduction",
    "chapter2": "Ch.2 Literature Review",
    "chapter3": "Ch.3 Research Methods",
    "chapter4": "Ch.4 Data Analysis",
    "chapter5": "Ch.5 Discussion",
}


def latest_json(prefix):
    files = sorted(OUT_DIR.glob(f"{prefix}_*.json"))
    return json.loads(files[-1].read_text()) if files else None


def map_chapter(file_path):
    """Map file path to chapter name."""
    for key, name in CHAPTERS.items():
        if key in file_path:
            return name
    if "appendices/" in file_path:
        # Map appendix file to its parent chapter
        # A_ch1 -> Ch.1, B_ch1 -> Ch.1, C_ch3 -> Ch.3, D_ch4 -> Ch.4, E_ch5 -> Ch.5
        m = re.search(r"appendices/(\w+)_ch(\d)", file_path)
        if m:
            return CHAPTERS.get(f"chapter{m.group(2)}", f"App. {m.group(1)}")
        m = re.search(r"appendices/([A-Z])_", file_path)
        if m:
            return f"App. {m.group(1)}"
    return "Other"


def map_page_to_chapter(pdf_page, page_chapter_ranges):
    """Map a PDF page to its chapter using main.aux chapter ranges."""
    for ch_name, (start, end) in page_chapter_ranges.items():
        if start <= pdf_page <= end:
            return ch_name
    return "Other"


def get_chapter_page_ranges():
    """Parse main.aux to find page range per chapter."""
    aux = ROOT / "main.aux"
    if not aux.exists():
        return {}
    text = aux.read_text(errors="ignore")
    # Find \@writefile{toc}{\contentsline {chapter}{...}{PAGE}{...}}
    ranges = {}
    chapters_with_page = []
    for m in re.finditer(r"\\@writefile\{toc\}\{\\contentsline\s*\{chapter\}\{[^}]*\\numberline\s*\{(\d+)\}([^}]*)\}\{(\d+)\}",
                         text):
        ch_num = int(m.group(1))
        title = m.group(2).strip()
        page = int(m.group(3))
        chapters_with_page.append((ch_num, title, page))
    chapters_with_page.sort()
    for i, (num, title, start) in enumerate(chapters_with_page):
        end = chapters_with_page[i + 1][2] - 1 if i + 1 < len(chapters_with_page) else 99999
        ch_name = CHAPTERS.get(f"chapter{num}", f"Ch.{num} {title[:30]}")
        ranges[ch_name] = (start, end)
    return ranges


def main():
    page_ranges = get_chapter_page_ranges()

    # Initialize per-chapter buckets
    buckets = defaultdict(lambda: {
        "table_count": 0,
        "table_right_empty": 0,
        "table_tall_col": 0,
        "table_width_imbal": 0,
        "table_squeezed": 0,
        "table_underused": 0,
        "table_under_width_alloc": 0,
        "intro_score_sum": 0,
        "intro_score_n": 0,
        "intro_low_score": 0,  # tables with score <= 2
        "page_sparse": 0,
        "page_half_empty": 0,
        "page_bottom_overflow_warn": 0,
        "page_bottom_overflow_crit": 0,
        "figure_overlaps": 0,
    })

    # Tables
    table_audit = latest_json("advanced_table_quality")
    if table_audit:
        for t in table_audit["tables"]:
            ch = map_chapter(t["file"])
            buckets[ch]["table_count"] += 1
            i = t["issues"]
            if i.get("right_side_empty"): buckets[ch]["table_right_empty"] += 1
            if i.get("tall_column"): buckets[ch]["table_tall_col"] += 1
            if i.get("width_imbalanced"): buckets[ch]["table_width_imbal"] += 1
            if i.get("squeezed_column"): buckets[ch]["table_squeezed"] += 1
            if i.get("underused_column"): buckets[ch]["table_underused"] += 1
            if i.get("under_width_allocated"): buckets[ch]["table_under_width_alloc"] += 1

    # Intro quality
    intro_audit = latest_json("table_intro_quality")
    if intro_audit:
        for ch_name, tabs in intro_audit["per_chapter"].items():
            for t in tabs:
                buckets[ch_name]["intro_score_sum"] += t["score"]
                buckets[ch_name]["intro_score_n"] += 1
                if t["score"] <= 2:
                    buckets[ch_name]["intro_low_score"] += 1

    # Pages
    page_audit = latest_json("per_page_visual")
    if page_audit and page_ranges:
        for p in page_audit["pages"]:
            ch = map_page_to_chapter(p["pdf_page"], page_ranges)
            if "sparse_page" in p["flags"]:
                buckets[ch]["page_sparse"] += 1
            if "half_empty_page" in p["flags"]:
                buckets[ch]["page_half_empty"] += 1

    # Bottom overflow
    bo_audit = latest_json("bottom_overflow_visual")
    if bo_audit and page_ranges:
        for p in bo_audit["flagged_pages"]:
            ch = map_page_to_chapter(p["pdf_page"], page_ranges)
            if p["severity"] == "critical":
                buckets[ch]["page_bottom_overflow_crit"] += 1
            else:
                buckets[ch]["page_bottom_overflow_warn"] += 1

    # Figures (TikZ overlaps - from MD report since no JSON)
    tikz_files = sorted(OUT_DIR.glob("tikz_overlap_*.md"))
    if tikz_files:
        latest_tikz = tikz_files[-1].read_text()
        # Parse: | `figures/X` | nodes | overlaps | overflows |
        for m in re.finditer(r"\|\s*`(figures/[^`]+)`\s*\|\s*\d+\s*\|\s*(\d+)\s*\|", latest_tikz):
            # Figures don't have a clear chapter — assume by name or default to "Other"
            ch = "Figures"  # we'll lump all figures together
            buckets[ch]["figure_overlaps"] += int(m.group(2))

    # Render report
    lines = []
    lines.append(f"# Per-Chapter Rollup Audit\n\n")
    lines.append(f"Generated: {datetime.now().isoformat()}\n\n")
    lines.append("Aggregates findings from ALL audit scripts into a single per-chapter scorecard.\n\n")

    lines.append("## Chapter Summary\n\n")
    lines.append("| Chapter | Tables | Issue% | Intro avg | Bottom-Overflow | Sparse Pages |\n")
    lines.append("|---|---:|---:|---:|---:|---:|\n")
    grand = defaultdict(int)
    for ch in sorted(buckets.keys()):
        b = buckets[ch]
        if b["table_count"] == 0 and b["page_sparse"] == 0:
            continue
        n = b["table_count"]
        issues = (b["table_right_empty"] + b["table_tall_col"] + b["table_width_imbal"]
                  + b["table_squeezed"] + b["table_underused"] + b["table_under_width_alloc"])
        issue_pct = (issues / max(n, 1)) * 100 if n else 0
        intro_avg = b["intro_score_sum"] / b["intro_score_n"] if b["intro_score_n"] else 0
        bo = b["page_bottom_overflow_warn"] + b["page_bottom_overflow_crit"]
        sparse = b["page_sparse"]
        lines.append(f"| {ch} | {n} | {issue_pct:.0f}% | {intro_avg:.2f} | {bo} | {sparse} |\n")
        grand["tables"] += n
        grand["issues"] += issues
        grand["bo"] += bo
        grand["sparse"] += sparse
    lines.append(f"| **TOTAL** | **{grand['tables']}** | — | — | **{grand['bo']}** | **{grand['sparse']}** |\n\n")

    # Per-chapter table issue detail
    lines.append("## Per-Chapter Table Issue Breakdown\n\n")
    lines.append("| Chapter | Tables | Right-Empty | Tall-Col | Width-Imbal | Squeezed | Underused | Under-Width |\n")
    lines.append("|---|---:|---:|---:|---:|---:|---:|---:|\n")
    for ch in sorted(buckets.keys()):
        b = buckets[ch]
        if b["table_count"] == 0:
            continue
        lines.append(f"| {ch} | {b['table_count']} | {b['table_right_empty']} | {b['table_tall_col']} | "
                     f"{b['table_width_imbal']} | {b['table_squeezed']} | {b['table_underused']} | "
                     f"{b['table_under_width_alloc']} |\n")
    lines.append("\n")

    # Per-chapter page issue detail
    lines.append("## Per-Chapter Page Issue Breakdown\n\n")
    lines.append("| Chapter | Pages | Sparse | Half-Empty | Bottom-Overflow Warn | Bottom-Overflow Critical |\n")
    lines.append("|---|---:|---:|---:|---:|---:|\n")
    for ch in sorted(buckets.keys()):
        b = buckets[ch]
        if b["page_sparse"] == 0 and b["page_bottom_overflow_warn"] == 0:
            continue
        total = b["page_sparse"] + b["page_half_empty"]
        lines.append(f"| {ch} | — | {b['page_sparse']} | {b['page_half_empty']} | "
                     f"{b['page_bottom_overflow_warn']} | {b['page_bottom_overflow_crit']} |\n")
    lines.append("\n")

    OUT_MD.write_text("".join(lines))
    print(f"Report: {OUT_MD}")
    print(f"\n{lines[3]}", end="")
    for ch in sorted(buckets.keys()):
        b = buckets[ch]
        if b["table_count"] == 0 and b["page_sparse"] == 0:
            continue
        issues = sum(b[k] for k in ["table_right_empty", "table_tall_col", "table_width_imbal",
                                     "table_squeezed", "table_underused", "table_under_width_alloc"])
        intro_avg = b["intro_score_sum"] / b["intro_score_n"] if b["intro_score_n"] else 0
        bo = b["page_bottom_overflow_warn"] + b["page_bottom_overflow_crit"]
        print(f"  {ch:30s} | tables: {b['table_count']:4d} | issues: {issues:4d} | "
              f"intro_avg: {intro_avg:.2f} | bottom-overflow: {bo:3d}")


if __name__ == "__main__":
    main()
