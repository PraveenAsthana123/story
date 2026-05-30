#!/usr/bin/env python3
"""
GGU Bottom Overflow Visual Detector
====================================

Detects pages where content (text or table) extends near or past
the page's bottom margin — even if LaTeX's `Overfull \\vbox` warning
didn't fire (LaTeX has tolerance; visual overflow can occur within tolerance).

Uses pdftotext with -bbox-layout to get Y coordinates of each text element,
then flags pages where the lowest text element is below the expected
bottom-margin Y threshold.

US Letter page = 792pt tall; 1in (72pt) margin top + bottom = text area ends
at ~720pt. Content below 740pt is "running into footer area" = overflow.

Output: jobs/reports/bottom_overflow_visual_YYYYMMDD_HHMM.md
"""
import re
import json
import sys
import subprocess
from pathlib import Path
from datetime import datetime

ROOT = Path(__file__).resolve().parents[2]
OUT_DIR = ROOT / "jobs" / "reports"
OUT_DIR.mkdir(parents=True, exist_ok=True)
TS = datetime.now().strftime("%Y%m%d_%H%M")
OUT_MD = OUT_DIR / f"bottom_overflow_visual_{TS}.md"
OUT_JSON = OUT_DIR / f"bottom_overflow_visual_{TS}.json"
PDF = ROOT / "main.pdf"

# US Letter PDF: 612pt wide x 792pt tall (8.5 x 11 inches)
# Body text area with 1in margins: ~72pt top + 720pt bottom
# Content with Y > 740pt = encroaching footer area
# Content with Y > 760pt = clearly past page bottom
WARN_Y_THRESHOLD = 740.0  # warning level
CRIT_Y_THRESHOLD = 760.0  # critical level


def get_max_y_per_page(pdf):
    """Run pdftotext -bbox-layout once, parse per-page max Y from <word> elements."""
    r = subprocess.run(["pdftotext", "-bbox-layout", str(pdf), "-"],
                       capture_output=True, text=True, timeout=120)
    html = r.stdout
    # Per <page> block extract all <word ... y2="...">
    page_max_y = []
    page_num = 0
    for page_match in re.finditer(r"<page[^>]*>(.*?)</page>", html, re.DOTALL):
        page_num += 1
        block = page_match.group(1)
        ys = [float(m.group(1)) for m in re.finditer(r'<word[^>]*yMax="([\d.]+)"', block)]
        if not ys:
            page_max_y.append((page_num, 0.0))
        else:
            page_max_y.append((page_num, max(ys)))
    return page_max_y


def get_display_pageno(pdf, page):
    try:
        r = subprocess.run(["pdftotext", "-f", str(page), "-l", str(page), str(pdf), "-"],
                           capture_output=True, text=True, timeout=5)
        m = re.search(r"pageno:\s*([0-9ivxlcdm]+)\s+of", r.stdout, re.IGNORECASE)
        return m.group(1) if m else None
    except Exception:
        return None


def main():
    if not PDF.exists():
        sys.exit("No main.pdf")
    print("Reading bbox layout (one batch call)...")
    page_max_y = get_max_y_per_page(PDF)
    print(f"Analyzed {len(page_max_y)} pages")

    warn_pages = []
    crit_pages = []
    for page_num, max_y in page_max_y:
        if max_y > CRIT_Y_THRESHOLD:
            crit_pages.append((page_num, max_y))
        elif max_y > WARN_Y_THRESHOLD:
            warn_pages.append((page_num, max_y))

    # Get display pagenos for flagged pages
    print(f"Resolving display pagenos for {len(warn_pages) + len(crit_pages)} flagged pages...")
    flagged_with_display = []
    for page, y in warn_pages + crit_pages:
        flagged_with_display.append({
            "pdf_page": page,
            "max_y": round(y, 1),
            "display_page": get_display_pageno(PDF, page),
            "severity": "critical" if y > CRIT_Y_THRESHOLD else "warning",
        })
    flagged_with_display.sort(key=lambda x: -x["max_y"])

    # Write JSON
    OUT_JSON.write_text(json.dumps({
        "generated": datetime.now().isoformat(),
        "n_pages": len(page_max_y),
        "warn_pages_count": len(warn_pages),
        "crit_pages_count": len(crit_pages),
        "total_flagged": len(warn_pages) + len(crit_pages),
        "warn_threshold_y": WARN_Y_THRESHOLD,
        "crit_threshold_y": CRIT_Y_THRESHOLD,
        "flagged_pages": flagged_with_display,
    }, indent=2))

    # Write MD
    lines = []
    lines.append("# Bottom Overflow Visual Audit\n\n")
    lines.append(f"Generated: {datetime.now().isoformat()}\n\n")
    lines.append("Detects pages where content's max Y position exceeds page-bottom thresholds.\n")
    lines.append(f"US Letter page = 792pt. Body text should end by ~720pt.\n")
    lines.append(f"- WARNING: any text with Y > {WARN_Y_THRESHOLD}pt (encroaching footer)\n")
    lines.append(f"- CRITICAL: any text with Y > {CRIT_Y_THRESHOLD}pt (visibly past margin)\n\n")
    lines.append("## Summary\n\n")
    lines.append(f"- Total pages: {len(page_max_y)}\n")
    lines.append(f"- WARNING (Y > {WARN_Y_THRESHOLD}): **{len(warn_pages)}** pages\n")
    lines.append(f"- CRITICAL (Y > {CRIT_Y_THRESHOLD}): **{len(crit_pages)}** pages\n\n")

    lines.append("## Pages With Overflow (top 200, by severity)\n\n")
    if flagged_with_display:
        lines.append("| PDF Pg | Display Pg | Max Y (pt) | Severity |\n")
        lines.append("|---:|---|---:|---|\n")
        for p in flagged_with_display[:200]:
            lines.append(f"| {p['pdf_page']} | {p['display_page'] or '?'} | {p['max_y']} | {p['severity']} |\n")

    OUT_MD.write_text("".join(lines), encoding="utf-8")
    print(f"Report MD:   {OUT_MD}")
    print(f"Report JSON: {OUT_JSON}")
    print(f"Total flagged: {len(warn_pages) + len(crit_pages)}")
    print(f"  WARNING (Y > {WARN_Y_THRESHOLD}): {len(warn_pages)}")
    print(f"  CRITICAL (Y > {CRIT_Y_THRESHOLD}): {len(crit_pages)}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
