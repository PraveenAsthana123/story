#!/usr/bin/env python3
"""Build a comprehensive per-page index/database for the dissertation PDF.

For every page in main.pdf, captures:
  - pdf_page (1-indexed absolute page)
  - display_page (the displayed page-number, may be roman for frontmatter)
  - text_lines    (count of text lines)
  - n_words       (word count on page)
  - text_density_pct (% of text area occupied)
  - n_tables_on_page (table fragments detected: caption + horizontal rule pattern)
  - n_table_rows    (estimated row count for any table fragments)
  - n_figures_on_page (figure caption count)
  - top_text_line   (first 80 chars of body)
  - status (one of: ok / sparse / almost_empty / empty / table_heavy / figure_heavy)
  - source_hint   (which chapter/appendix this page belongs to, derived from
                   first body text + chapter title patterns)

Outputs:
  jobs/reports/per_page_index.csv      (queryable CSV)
  jobs/reports/per_page_index.md       (markdown table preview, top 200 rows)
  jobs/reports/per_page_index_full.md  (markdown table all rows)
  jobs/reports/per_page_index.json     (machine-readable)
"""
from __future__ import annotations
import csv
import json
import re
import subprocess
import sys
from pathlib import Path
from datetime import datetime

ROOT = Path(__file__).resolve().parents[2]
PDF = ROOT / "main.pdf"
OUT_DIR = ROOT / "jobs" / "reports"


def get_total_pages():
    out = subprocess.run(["pdfinfo", str(PDF)], capture_output=True, text=True).stdout
    for line in out.splitlines():
        if line.startswith("Pages:"):
            return int(line.split(":")[1].strip())
    return 0


def extract_page_text(page_num: int) -> str:
    return subprocess.run(
        ["pdftotext", "-f", str(page_num), "-l", str(page_num), str(PDF), "-"],
        capture_output=True, text=True, check=False,
    ).stdout


def extract_page_bbox(page_num: int) -> list:
    """Return list of (xMin, yMin, xMax, yMax, text) for body words on the page."""
    out = subprocess.run(
        ["pdftotext", "-bbox-layout", "-f", str(page_num), "-l", str(page_num), str(PDF), "-"],
        capture_output=True, text=True, check=False,
    ).stdout
    words = []
    for m in re.finditer(
        r'<word[^>]*xMin="([\d.]+)"[^>]*yMin="([\d.]+)"[^>]*xMax="([\d.]+)"[^>]*yMax="([\d.]+)"[^>]*>([^<]*)</word>',
        out,
    ):
        ymin = float(m.group(2))
        # Skip page header/footer
        if ymin < 50 or ymin > 740: continue
        words.append((float(m.group(1)), ymin, float(m.group(3)), float(m.group(4)), m.group(5)))
    return words


def analyze_page(page_num: int, total: int) -> dict:
    text = extract_page_text(page_num)
    lines = [l for l in text.split("\n") if l.strip()]
    # Skip page-header / page-footer lines (very short with "pageno:" / "of NNNN")
    body_lines = [l for l in lines if not re.match(r"^\s*pageno:\s*\d", l)]
    words = body_lines.copy()  # for word count
    n_words = sum(len(l.split()) for l in body_lines)
    # Display page number from footer
    display = ""
    for l in lines:
        m = re.match(r"\s*pageno:\s*(\S+)\s*of", l)
        if m:
            display = m.group(1); break

    # Detect tables on page: count "Table N.NN." patterns + tabular pattern
    n_tables = len(re.findall(r"\bTable\s+\d+\.\d+\.\s", text))
    # Detect rows: if pattern "& X & Y" or "row \\" appears
    # Simpler proxy: count lines with multiple ampersands (table-like) +
    # count lines that look like table-data via vertical separators
    # Without -bbox, just count tabular signal lines
    n_table_rows_est = 0
    for l in body_lines:
        # tabular rows often have multiple spaces between cells in pdftotext output
        # or contain " & " when extracted naively
        if l.count("  ") >= 3 and len(l.split()) >= 3 and not l.startswith("Figure"):
            # likely a table row
            n_table_rows_est += 1
    # Detect figures
    n_figures = len(re.findall(r"\bFigure\s+\d+\.\d+\.\s", text))

    # bbox-based density
    bbox = extract_page_bbox(page_num)
    if bbox:
        # Page area used (rough: extent of y range from words)
        ys = [w[1] for w in bbox]
        ymin = min(ys); ymax = max(w[3] for w in bbox)
        page_text_height = 700  # A4 text area pt
        text_extent_pct = round((ymax - ymin) / page_text_height * 100)
        # Density: total word area / page area
        total_word_area = sum((w[2] - w[0]) * (w[3] - w[1]) for w in bbox)
        page_area = 540 * 700  # text width * text height
        density_pct = round(total_word_area / page_area * 100)
    else:
        text_extent_pct = 0
        density_pct = 0

    # Classify
    n_body = len(body_lines)
    if n_body == 0:
        status = "empty"
    elif n_body <= 3:
        status = "almost_empty"
    elif text_extent_pct < 30:
        status = "sparse"
    elif n_figures > 0 and n_body < 20:
        status = "figure_heavy"
    elif n_tables > 0 and n_table_rows_est > 5:
        status = "table_heavy"
    else:
        status = "ok"

    # Top text line (preview)
    top_line = body_lines[0][:80] if body_lines else "(empty)"

    return {
        "pdf_page": page_num,
        "display_page": display,
        "text_lines": n_body,
        "n_words": n_words,
        "text_extent_pct": text_extent_pct,
        "density_pct": density_pct,
        "n_tables_on_page": n_tables,
        "n_table_rows_est": n_table_rows_est,
        "n_figures_on_page": n_figures,
        "top_text_line": top_line.replace("|", "\\|"),
        "status": status,
    }


def main():
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    total = get_total_pages()
    print(f"Building per-page index for {total} pages...")
    rows = []
    for p in range(1, total + 1):
        rows.append(analyze_page(p, total))
        if p % 100 == 0:
            print(f"  ...processed {p}/{total}")

    # Write CSV
    csv_path = OUT_DIR / "per_page_index.csv"
    with open(csv_path, "w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=list(rows[0].keys()))
        writer.writeheader()
        writer.writerows(rows)

    # Write JSON
    json_path = OUT_DIR / "per_page_index.json"
    json_path.write_text(json.dumps({
        "generated": datetime.now().isoformat(timespec="seconds"),
        "total_pages": total,
        "rows": rows,
    }, indent=1))

    # Summary by status
    from collections import Counter
    by_status = Counter(r["status"] for r in rows)
    print("\n=== Per-page index built ===")
    print(f"Total pages: {total}")
    for s, c in sorted(by_status.items(), key=lambda kv: -kv[1]):
        print(f"  {s}: {c} pages")

    # Write markdown summary (top 200 + worst pages)
    md = []
    md.append(f"# Per-Page Index Database\n")
    md.append(f"_Generated: {datetime.now().isoformat(timespec='seconds')}_\n")
    md.append(f"**Total PDF pages: {total}**\n")
    md.append("## Status distribution\n")
    md.append("| Status | Count | % |")
    md.append("|---|---:|---:|")
    for s, c in sorted(by_status.items(), key=lambda kv: -kv[1]):
        md.append(f"| {s} | {c} | {c/total*100:.1f}% |")
    md.append("")
    md.append("## Quick queries\n")
    md.append("Full CSV available at `jobs/reports/per_page_index.csv` for filtering.\n")
    md.append("Examples (run from project root):\n")
    md.append("```bash")
    md.append("# All empty pages")
    md.append("awk -F, '$11==\"empty\"' jobs/reports/per_page_index.csv | wc -l")
    md.append("# Pages with no tables and < 5 lines")
    md.append("awk -F, '$3<5 && $7==0' jobs/reports/per_page_index.csv | head")
    md.append("```\n")
    md.append("## Top 50 most-sparse pages\n")
    md.append("| PDF | Display | Lines | Words | Density% | Tables | Rows | Figures | Status | Preview |")
    md.append("|---:|---:|---:|---:|---:|---:|---:|---:|---|---|")
    sparse_pages = [r for r in rows if r["status"] in ("empty", "almost_empty", "sparse")]
    for r in sorted(sparse_pages, key=lambda r: r["text_lines"])[:50]:
        md.append(f"| {r['pdf_page']} | {r['display_page']} | {r['text_lines']} | {r['n_words']} | {r['density_pct']} | {r['n_tables_on_page']} | {r['n_table_rows_est']} | {r['n_figures_on_page']} | {r['status']} | {r['top_text_line'][:60]} |")
    md.append("")
    md.append("## Pages with TABLES but very few rows (orphan-caption suspects)\n")
    md.append("| PDF | Display | Lines | Tables on page | Est. rows | Preview |")
    md.append("|---:|---:|---:|---:|---:|---|")
    orphans = [r for r in rows if r["n_tables_on_page"] > 0 and r["n_table_rows_est"] < 3]
    for r in orphans[:50]:
        md.append(f"| {r['pdf_page']} | {r['display_page']} | {r['text_lines']} | {r['n_tables_on_page']} | {r['n_table_rows_est']} | {r['top_text_line'][:60]} |")
    md.append("")
    md.append(f"_(+ {max(0, len(orphans)-50)} more orphan-caption pages)_\n")
    md.append("## Per-PDF-page-range distribution\n")
    md.append("Shows status counts per 100-page bucket so you can see WHERE issues cluster.\n")
    md.append("| Range | empty | almost_empty | sparse | ok | figure_heavy | table_heavy |")
    md.append("|---|---:|---:|---:|---:|---:|---:|")
    for lo in range(0, total, 100):
        hi = min(lo + 100, total)
        bucket = [r for r in rows if lo < r["pdf_page"] <= hi]
        c = Counter(r["status"] for r in bucket)
        md.append(f"| {lo+1}-{hi} | {c.get('empty',0)} | {c.get('almost_empty',0)} | {c.get('sparse',0)} | {c.get('ok',0)} | {c.get('figure_heavy',0)} | {c.get('table_heavy',0)} |")

    md_path = OUT_DIR / "per_page_index.md"
    md_path.write_text("\n".join(md))

    print(f"\nCSV:  {csv_path}")
    print(f"JSON: {json_path}")
    print(f"MD:   {md_path}")


if __name__ == "__main__":
    main()
