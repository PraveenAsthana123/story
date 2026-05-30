#!/usr/bin/env python3
"""Per-page right-side white-space audit.

For every PDF page, measures how far the right-most content ink extends from
the right page margin. Pages where the right-side gap is unusually large
indicate:
  - tables/figures NOT spanning full text width (right-edge gap)
  - tables that are too narrow (didn't use tabularx/xltabular with X)
  - text blocks that wrap early
  - centered content that leaves both sides empty

Uses `pdftotext -bbox-layout` to extract per-word bounding boxes per page.

Output: jobs/reports/right_side_space_<TS>.md  +  canonical _master.md
JSON: jobs/reports/right_side_space_<TS>.json (for trend tracker)

READ-ONLY: no .tex files modified, no PDF re-rendered.
"""
from __future__ import annotations
import re
import json
import subprocess
import sys
from pathlib import Path
from collections import defaultdict
from datetime import datetime

ROOT = Path(__file__).resolve().parents[2]
PDF = ROOT / "main.pdf"
OUT_DIR = ROOT / "jobs" / "reports"

# Page geometry: project uses A4 (595.28 x 841.89 pt) per pdftotext bbox.
# 1-inch margin -> text right edge at 595.28 - 72 = ~523pt.
RIGHT_TEXT_EDGE_PT = 523.0
# Tolerance: gap less than this is acceptable (e.g., justified text endings)
ACCEPTABLE_GAP_PT = 36.0      # ~0.5 inch
WARN_GAP_PT = 72.0            # 1 inch
CRITICAL_GAP_PT = 144.0       # 2 inches


def extract_pages_bbox(pdf: Path):
    """Yield (page_num, list_of_(xmin, ymin, xmax, ymax, text)) per page."""
    proc = subprocess.run(
        ["pdftotext", "-bbox-layout", str(pdf), "-"],
        capture_output=True, text=True, check=False,
    )
    if proc.returncode != 0:
        print(f"pdftotext failed: {proc.stderr[:300]}", file=sys.stderr)
        sys.exit(1)
    xml = proc.stdout
    # pdftotext -bbox-layout emits <page width="..." height="..."> without
    # a number attribute. Enumerate pages by appearance order.
    page_pat = re.compile(r"<page\b[^>]*>(.*?)</page>", re.DOTALL)
    word_pat = re.compile(
        r"<word[^>]*xMin=\"([\d.]+)\"[^>]*yMin=\"([\d.]+)\"[^>]*xMax=\"([\d.]+)\"[^>]*yMax=\"([\d.]+)\"[^>]*>([^<]*)</word>",
        re.DOTALL,
    )
    for pnum, pm in enumerate(page_pat.finditer(xml), 1):
        body = pm.group(1)
        words = []
        for wm in word_pat.finditer(body):
            xmin = float(wm.group(1)); ymin = float(wm.group(2))
            xmax = float(wm.group(3)); ymax = float(wm.group(4))
            text = wm.group(5).strip()
            # Skip page header/footer band (top/bottom ~30pt)
            if ymin < 50 or ymax > 740:
                continue
            words.append((xmin, ymin, xmax, ymax, text))
        yield pnum, words


def assess_page(words):
    """Return dict of metrics for one page.

    - right_edge_max_pt: the max xMax across all body words
    - right_gap_pt: 540 - right_edge_max_pt (positive = unused right space)
    - n_rows_short: count of distinct y-rows where xMax < right_edge_minus 1in
    - sample_short_y: y-coords of the first 5 short rows
    """
    if not words:
        return {"empty": True}
    # Build per-row max-xMax: group words by integer y (snap to 8pt buckets)
    row_max = defaultdict(float)
    for x0, y0, x1, y1, _t in words:
        bucket = int(y0 / 8) * 8
        row_max[bucket] = max(row_max[bucket], x1)
    right_edges = list(row_max.values())
    if not right_edges:
        return {"empty": True}
    overall_right = max(right_edges)
    overall_gap = RIGHT_TEXT_EDGE_PT - overall_right
    # Count rows whose right-edge is more than 1 inch short of text edge
    short_rows = [(y, RIGHT_TEXT_EDGE_PT - x)
                  for y, x in row_max.items()
                  if RIGHT_TEXT_EDGE_PT - x > WARN_GAP_PT]
    # Pages with mostly-justified text will have most rows aligned to within
    # 0-20pt of the right edge; the LAST line of each paragraph is often
    # short. So we look at the RATIO of short rows, not just count.
    short_pct = len(short_rows) / max(len(row_max), 1)
    severity = "ok"
    if overall_gap > CRITICAL_GAP_PT:
        severity = "critical"
    elif short_pct > 0.40 and overall_gap > WARN_GAP_PT:
        severity = "warn"
    elif overall_gap > WARN_GAP_PT:
        severity = "watch"
    return {
        "empty": False,
        "n_rows": len(row_max),
        "overall_right_pt": round(overall_right, 1),
        "overall_gap_pt": round(overall_gap, 1),
        "short_rows": len(short_rows),
        "short_pct": round(short_pct, 2),
        "severity": severity,
    }


def main():
    if not PDF.exists():
        sys.exit(f"PDF not found at {PDF}")
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    ts = datetime.now().strftime("%Y%m%d_%H%M")
    out_md = OUT_DIR / f"right_side_space_{ts}.md"
    out_json = OUT_DIR / f"right_side_space_{ts}.json"
    master = OUT_DIR / "right_side_space_master.md"

    print(f"Auditing right-side space across pages of {PDF.name}...")
    page_metrics = []
    for pnum, words in extract_pages_bbox(PDF):
        m = assess_page(words)
        m["page"] = pnum
        page_metrics.append(m)

    n_pages = len(page_metrics)
    by_sev = defaultdict(list)
    for m in page_metrics:
        if m.get("empty"): by_sev["empty"].append(m["page"]); continue
        by_sev[m["severity"]].append(m)

    lines = []
    lines.append(f"# Right-Side Space Audit (per page)\n")
    lines.append(f"_Generated: {datetime.now().isoformat(timespec='seconds')}_\n")
    lines.append(f"- Pages scanned: **{n_pages}**")
    lines.append(f"- Critical (right gap > 2in): **{len(by_sev['critical'])}**")
    lines.append(f"- Warn (>1in gap AND >40% rows short): **{len(by_sev['warn'])}**")
    lines.append(f"- Watch (>1in gap): **{len(by_sev['watch'])}**")
    lines.append(f"- OK (<1in gap): **{len(by_sev['ok'])}**")
    lines.append(f"- Empty: **{len(by_sev['empty'])}**")
    lines.append("")
    lines.append("## Thresholds")
    lines.append("- Text-area right edge: 540pt (US-Letter, 1in margins)")
    lines.append("- Acceptable gap (last-line of justified paragraph): up to 36pt (~0.5in)")
    lines.append("- Watch: gap >72pt (~1in)")
    lines.append("- Warn: gap >72pt AND >40% rows on page are short")
    lines.append("- Critical: gap >144pt (~2in) --- table or figure clearly not full-width")
    lines.append("")
    lines.append("## Top 50 critical/warn pages (worst first)")
    bad = by_sev["critical"] + by_sev["warn"] + by_sev["watch"]
    bad.sort(key=lambda m: -m["overall_gap_pt"])
    lines.append("| Page | Severity | Right edge (pt) | Right gap (pt) | Rows total | Short rows | Short % |")
    lines.append("|---:|---|---:|---:|---:|---:|---:|")
    for m in bad[:50]:
        lines.append(f"| {m['page']} | {m['severity']} | {m['overall_right_pt']} | {m['overall_gap_pt']} | {m['n_rows']} | {m['short_rows']} | {m['short_pct']:.0%} |")
    lines.append("")
    lines.append("## How to interpret")
    lines.append("- A **critical** page with > 2in right gap almost always indicates a TABLE or FIGURE that did NOT span the full text width.")
    lines.append("- A **warn** page with high short-row% indicates many lines wrap early --- usually a narrow tabularx/xltabular content column or a centred minipage.")
    lines.append("- An OK page can still have its LAST LINE short (justified paragraphs); that is normal typography, not a defect.")
    lines.append("")
    lines.append("## How to fix")
    lines.append("- For tables: ensure `\\begin{xltabular}{\\textwidth}{...}` (width = `\\textwidth`) and at least one `X` column or `>{\\raggedright\\arraybackslash}p{cm}+L` last-column pattern.")
    lines.append("- For figures: ensure `\\begin{figure}` is NOT wrapped in `\\begin{minipage}{0.5\\textwidth}`; use the full text width.")
    lines.append("- For minipages: change width to `\\textwidth` unless side-by-side layout is intentional.")
    lines.append("- After fix, re-run this audit. The 'critical' count should drop.")

    out_md.write_text("\n".join(lines))
    master.write_text("\n".join(lines))
    out_json.write_text(json.dumps({
        "timestamp": datetime.now().isoformat(),
        "pages_scanned": n_pages,
        "by_severity": {k: len(v) for k, v in by_sev.items()},
        "critical_pages": [m["page"] for m in by_sev["critical"]],
        "warn_pages": [m["page"] for m in by_sev["warn"]],
        "watch_pages": [m["page"] for m in by_sev["watch"]],
    }, indent=2))

    print(f"Report MD:   {out_md}")
    print(f"Report JSON: {out_json}")
    print(f"Pages flagged: critical={len(by_sev['critical'])}  warn={len(by_sev['warn'])}  watch={len(by_sev['watch'])}  ok={len(by_sev['ok'])}")


if __name__ == "__main__":
    main()
