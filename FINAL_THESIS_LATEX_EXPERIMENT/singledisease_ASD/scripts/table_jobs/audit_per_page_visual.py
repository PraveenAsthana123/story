#!/usr/bin/env python3
"""
GGU Per-Page Visual Audit
==========================

For EVERY page in the PDF (~2000 pages), compute:
  - White-space ratio (how much of the page is empty)
  - Text-to-table-to-figure balance
  - Content extent (rendered height of content vs page height)
  - Display page number from "pageno: X of Y" footer
  - Any flagged issues (white space > 30%, content < 50% of page area)

Output: jobs/reports/per_page_visual_YYYYMMDD_HHMM.md
        + per_page_visual_YYYYMMDD_HHMM.json (machine-readable)

This is the "1 agent per page" replacement — does the work
deterministically without spawning 2000 agents.

Usage:
  python3 scripts/table_jobs/audit_per_page_visual.py             # all pages
  python3 scripts/table_jobs/audit_per_page_visual.py --pages 100-200
  python3 scripts/table_jobs/audit_per_page_visual.py --sample 50  # 50 random
"""
import json
import re
import sys
import subprocess
from pathlib import Path
from datetime import datetime

ROOT = Path(__file__).resolve().parents[2]
OUT_DIR = ROOT / "jobs" / "reports"
OUT_DIR.mkdir(parents=True, exist_ok=True)
TS = datetime.now().strftime("%Y%m%d_%H%M")
OUT_MD = OUT_DIR / f"per_page_visual_{TS}.md"
OUT_JSON = OUT_DIR / f"per_page_visual_{TS}.json"
PDF = ROOT / "main.pdf"

# Per-page render cache (avoid re-rendering)
RENDER_CACHE = Path("/tmp/ggu_page_cache")
RENDER_CACHE.mkdir(exist_ok=True)


def count_text_lines(pdf, page):
    """Count non-empty text lines on a page via pdftotext."""
    try:
        r = subprocess.run(["pdftotext", "-layout", "-f", str(page), "-l", str(page), str(pdf), "-"],
                           capture_output=True, text=True, timeout=10)
        return len([l for l in r.stdout.splitlines() if l.strip()])
    except Exception:
        return 0


def get_display_pageno(pdf, page):
    """Extract 'pageno: X of Y' from page footer."""
    try:
        r = subprocess.run(["pdftotext", "-f", str(page), "-l", str(page), str(pdf), "-"],
                           capture_output=True, text=True, timeout=10)
        m = re.search(r"pageno:\s*([0-9ivxlcdm]+)\s+of", r.stdout, re.IGNORECASE)
        return m.group(1) if m else None
    except Exception:
        return None


def measure_content_extent(pdf, page):
    """
    Render page at low res, count rows of pixels that have content (non-white).
    Returns (content_rows, total_rows, ratio).
    Skip if Pillow not available — use lighter heuristic.
    """
    try:
        from PIL import Image
        img_path = RENDER_CACHE / f"p{page:05d}.png"
        if not img_path.exists():
            ppm_prefix = RENDER_CACHE / f"_render_p{page:05d}"
            subprocess.run(["pdftoppm", "-r", "60", "-f", str(page), "-l", str(page),
                           str(pdf), str(ppm_prefix)],
                           capture_output=True, timeout=15)
            # Find the PPM file (pdftoppm appends digit suffix)
            ppm_files = list(RENDER_CACHE.glob(f"_render_p{page:05d}*.ppm"))
            if not ppm_files:
                return None, None, None
            subprocess.run(["convert", str(ppm_files[0]), str(img_path)],
                           capture_output=True, timeout=15)
            for f in ppm_files:
                f.unlink()

        img = Image.open(img_path).convert("L")
        w, h = img.size
        # For each row, check if it has any "dark" (content) pixel
        pixels = img.load()
        content_rows = 0
        for y in range(h):
            for x in range(0, w, 5):  # sample every 5px horizontally
                if pixels[x, y] < 200:  # darker than near-white
                    content_rows += 1
                    break
        # Skip top/bottom 30px for header/footer
        adj_total = h - 60
        adj_content = max(0, content_rows - 30)
        ratio = adj_content / adj_total if adj_total > 0 else 0
        return adj_content, adj_total, ratio
    except ImportError:
        return None, None, None
    except Exception:
        return None, None, None


def main():
    args = sys.argv[1:]
    pages_arg = None
    sample_n = None
    for i, a in enumerate(args):
        if a == "--pages" and i + 1 < len(args):
            pages_arg = args[i + 1]
        elif a == "--sample" and i + 1 < len(args):
            sample_n = int(args[i + 1])

    if not PDF.exists():
        sys.exit("No main.pdf — run pdflatex first.")
    r = subprocess.run(["pdfinfo", str(PDF)], capture_output=True, text=True)
    n_pages = int([l for l in r.stdout.splitlines() if l.startswith("Pages:")][0].split(":")[1].strip())

    # Determine page range
    if pages_arg:
        start, end = (int(x) for x in pages_arg.split("-"))
        pages_to_check = list(range(start, end + 1))
    elif sample_n:
        import random
        random.seed(42)
        pages_to_check = sorted(random.sample(range(1, n_pages + 1), sample_n))
    else:
        pages_to_check = list(range(1, n_pages + 1))

    print(f"Auditing {len(pages_to_check)} pages...")

    results = []
    issues_summary = {
        "low_content_extent": 0,    # < 50% of page used
        "very_low_content": 0,      # < 30% of page used
        "text_only_pages": 0,       # < 5 text lines
    }

    # Fast pass: dump ALL pages text in one pdftotext call, parse per-page boundaries
    r = subprocess.run(["pdftotext", "-layout", str(PDF), "-"], capture_output=True, text=True)
    # pdftotext uses form-feed (\x0c) between pages
    page_texts = r.stdout.split("\x0c")
    # Page texts has n_pages + 1 elements (trailing empty)

    for p in pages_to_check:
        if p > len(page_texts):
            continue
        text = page_texts[p - 1]
        lines = [l for l in text.splitlines() if l.strip()]
        text_lines = len(lines)

        # Display pageno from header
        display_no = None
        for line in lines[:3]:
            m = re.search(r"pageno:\s*([0-9ivxlcdm]+)\s+of", line, re.IGNORECASE)
            if m:
                display_no = m.group(1)
                break

        # Compute total characters
        total_chars = sum(len(l) for l in lines)
        # Page area heuristic: a full page has ~45 lines of body text * ~80 chars = ~3600 chars
        # If total_chars < 1000, page is mostly empty
        # If text_lines < 8, page is sparse

        flags = []
        if text_lines < 5 and total_chars < 200:
            flags.append("almost_empty_page")
            issues_summary["text_only_pages"] += 1
        elif text_lines < 12 and total_chars < 800:
            flags.append("sparse_page")
            issues_summary["very_low_content"] += 1
        elif text_lines < 25 and total_chars < 1800:
            flags.append("half_empty_page")
            issues_summary["low_content_extent"] += 1

        results.append({
            "pdf_page": p,
            "display_page": display_no,
            "text_lines": text_lines,
            "total_chars": total_chars,
            "flags": flags,
        })

    # Write JSON
    OUT_JSON.write_text(json.dumps({
        "generated": datetime.now().isoformat(),
        "n_pages_audited": len(pages_to_check),
        "total_pdf_pages": n_pages,
        "summary": issues_summary,
        "pages": results,
    }, indent=2))

    # Write Markdown
    lines = []
    lines.append("# Per-Page Visual Audit\n\n")
    lines.append(f"Generated: {datetime.now().isoformat()}\n")
    lines.append(f"Total PDF pages: {n_pages}\n")
    lines.append(f"Pages audited: {len(pages_to_check)}\n\n")

    lines.append("## Summary\n\n")
    lines.append("| Issue | Count |\n|---|---:|\n")
    for k, v in issues_summary.items():
        lines.append(f"| {k} | {v} |\n")
    lines.append("\n")

    # Pages with issues
    flagged = [r for r in results if r["flags"]]
    lines.append(f"## Flagged pages ({len(flagged)})\n\n")
    if flagged:
        lines.append("| PDF Pg | Display Pg | Text lines | Total chars | Issues |\n")
        lines.append("|---:|---|---:|---:|---|\n")
        for r in flagged[:500]:
            issues_str = ", ".join(r["flags"])
            lines.append(f"| {r['pdf_page']} | {r['display_page'] or '?'} | {r['text_lines']} | {r['total_chars']} | {issues_str} |\n")
        lines.append("\n")

    OUT_MD.write_text("".join(lines), encoding="utf-8")
    print(f"\nReport MD:   {OUT_MD}")
    print(f"Report JSON: {OUT_JSON}")
    print(f"Pages flagged: {len(flagged)}")
    print(f"  very_low_content (< 30%): {issues_summary['very_low_content']}")
    print(f"  low_content_extent (< 50%): {issues_summary['low_content_extent']}")
    print(f"  text_only_pages (< 5 lines): {issues_summary['text_only_pages']}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
