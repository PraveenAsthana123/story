#!/usr/bin/env python3
"""
GGU Per-Page Table Issue Report
================================

Cross-references every TABLE in source with the PDF page it renders on,
and the build-log overflows that occurred near that page.

Output: jobs/reports/page_table_issues_YYYYMMDD_HHMM.md
A clear table:
  PDF page | Display page | Table | Cols | Width allocation | Issue | Why | Fix
"""
import re
import json
import sys
from pathlib import Path
from datetime import datetime

ROOT = Path(__file__).resolve().parents[2]
OUT_DIR = ROOT / "jobs" / "reports"
TS = datetime.now().strftime("%Y%m%d_%H%M")
OUT_MD = OUT_DIR / f"page_table_issues_{TS}.md"


def latest_audit_json():
    files = sorted(OUT_DIR.glob("advanced_table_quality_*.json"))
    return files[-1] if files else None


def parse_aux_labels():
    """Read main.aux to map table labels → PDF page number."""
    aux = ROOT / "main.aux"
    if not aux.exists():
        return {}
    spans = {}
    for m in re.finditer(r"\\newlabel\{(tab:[^}]+)\}\{\{[^}]*\}\{(\d+)\}", aux.read_text(errors="ignore")):
        spans[m.group(1)] = int(m.group(2))
    return spans


def parse_vbox_pages():
    """Parse main.log for Overfull \\vbox + the page that comes after each."""
    log = ROOT / "main.log"
    if not log.exists():
        return []
    log_text = log.read_text(errors="ignore")
    pos_pages = [(m.start(), int(m.group(1))) for m in re.finditer(r"\[(\d+)\]", log_text)]
    results = []
    for m in re.finditer(r"Overfull \\vbox \(([\d.]+)pt too high\)", log_text):
        pt = float(m.group(1))
        prev_pages = [p for sp, p in pos_pages if sp < m.start()]
        next_pages = [p for sp, p in pos_pages if sp > m.start()][:1]
        results.append({
            "too_high_pt": pt,
            "prev_page": prev_pages[-1] if prev_pages else None,
            "next_page": next_pages[0] if next_pages else None,
        })
    return results


def get_display_page(pdf_path, pdf_page):
    """Read the 'pageno: X of Y' footer to get displayed page number."""
    import subprocess
    try:
        r = subprocess.run(["pdftotext", "-f", str(pdf_page), "-l", str(pdf_page), str(pdf_path), "-"],
                           capture_output=True, text=True, timeout=10)
        m = re.search(r"pageno:\s*([0-9ivxlcdm]+)\s+of", r.stdout, re.IGNORECASE)
        return m.group(1) if m else None
    except Exception:
        return None


def diagnose_table(t):
    """Generate a human-readable diagnosis of a table's issues."""
    issues = t["issues"]
    widths = t["col_widths_cm"]
    avgs = t["col_avg_text_len"]
    maxes = t["col_max_text_len"]

    problems = []
    fixes = []

    # Identify wasted-space columns: col with low avg but allocated width > 3cm
    for i, (w, a) in enumerate(zip(widths, avgs)):
        if w and w >= 3.0 and a < 10:
            problems.append(f"Col{i+1} has {w:.1f}cm width but only {a:.0f} avg chars — wasted ~{w-1.5:.1f}cm")
            fixes.append(f"Narrow col{i+1} to p{{1.5cm}}")

    # Identify squeezed columns: col with high avg but narrow width
    for i, (w, a) in enumerate(zip(widths, avgs)):
        if w and a > 30 and a / w > 12:
            problems.append(f"Col{i+1} squeezed: {a:.0f} chars in {w:.1f}cm = {a/w:.0f} chars/cm (forces wrap)")
            fixes.append(f"Widen col{i+1} to p{{{max(2.5, a/8):.1f}cm}}")

    # Identify tall-row potential: max content of any cell > 200 chars (3+ wrapped lines)
    if any(m > 200 for m in maxes):
        worst = max(maxes)
        worst_idx = maxes.index(worst)
        ww = widths[worst_idx]
        if ww:
            problems.append(f"Col{worst_idx+1} has max {worst} chars in {ww:.1f}cm = {worst//40:.0f}+ lines per cell → tall rows")
            fixes.append(f"Consider widening col{worst_idx+1} or splitting content")

    # Per-row waste: short col + long col → each row inherits max height
    long_cols = [i for i, m in enumerate(maxes) if m > 150]
    short_cols = [i for i, a in enumerate(avgs) if a < 15]
    if long_cols and short_cols and len(long_cols) + len(short_cols) >= 2:
        problems.append(f"Mixed long+short cols: cols {[i+1 for i in long_cols]} have long content vs cols {[i+1 for i in short_cols]} short — rows inherit max height of long col, short cols show whitespace")
        fixes.append(f"Widen long col to reduce wrap (smaller max height → less wasted space in short cols)")

    return problems, fixes


def main():
    audit_json = latest_audit_json()
    if not audit_json:
        sys.exit("No audit JSON. Run audit_advanced_table_quality.py first.")
    data = json.loads(audit_json.read_text())
    tables = data["tables"]
    labels = parse_aux_labels()
    vbox_events = parse_vbox_pages()
    pdf_path = ROOT / "main.pdf"

    # Cross-reference: each table → page
    for t in tables:
        t["pdf_page"] = labels.get(t["label"])

    # Tables on pages with vbox overflow
    overflow_pages = set()
    for v in vbox_events:
        if v["prev_page"]:
            overflow_pages.add(v["prev_page"])
        if v["next_page"]:
            overflow_pages.add(v["next_page"])

    # Get display pageno for each vbox overflow
    for v in vbox_events:
        if v["next_page"]:
            v["display_page"] = get_display_page(pdf_path, v["next_page"])
        else:
            v["display_page"] = None

    # Build report
    lines = []
    lines.append("# Per-Page Table Issues Report\n\n")
    lines.append(f"Generated: {datetime.now().isoformat()}\n\n")
    lines.append("## Cause Explanation\n\n")
    lines.append("**Why tables waste vertical space:**\n\n")
    lines.append("In LaTeX `xltabular`/`longtable`, each row's HEIGHT equals the TALLEST cell in that row. When one column has long wrapped text (5+ lines) and another has 1 word (\"Yes\", \"H1\"), both columns occupy that same row height. Result: short-content cells show with 4-5 lines of WHITE SPACE around them. The table appears LONGER than the actual text content needs — \"table length > text length\".\n\n")
    lines.append("**Root causes of this pattern:**\n\n")
    lines.append("1. **Squeezed wide-content column** — column allocated < 6cm but contains 100+ chars per cell → wraps to 4-6 lines unnecessarily\n")
    lines.append("2. **Over-wide narrow-content column** — column allocated > 3cm but content is just 1-2 words → wastes 2+ cm that could go to wide-content col\n")
    lines.append("3. **No mixed-content awareness** — manual column widths don't account for the ratio of content lengths across columns\n\n")
    lines.append("**Fixes available:**\n\n")
    lines.append("- `fix_advanced_table_quality_v2.py` rebalances column widths using sqrt-weighted text-density\n")
    lines.append("- Narrow content columns get clamped to 1-1.5cm\n")
    lines.append("- Wide content columns get expanded to ~8 chars/cm density (optimal for \\footnotesize)\n\n")

    # Build-log overflow section
    lines.append(f"## Build-Log Bottom Overflows: {len(vbox_events)} pages affected\n\n")
    if vbox_events:
        lines.append("| PDF Page | Display Page | Severity (pt too high) | Likely Cause |\n")
        lines.append("|---:|---|---:|---|\n")
        for v in vbox_events:
            severity = v["too_high_pt"]
            cause = "Single tall row > page space (table cell ~ minor)" if severity < 200 else "Multi-row table can't fit (consider split or Part 1/Part 2)"
            lines.append(f"| {v['next_page'] or '?'} | {v['display_page'] or '?'} | {severity:.0f} | {cause} |\n")
        lines.append("\n")

    # Issue summary
    lines.append("## Issue Counts (current audit)\n\n")
    lines.append("| Issue | Count |\n|---|---:|\n")
    for k, v in sorted(data["issue_counts"].items(), key=lambda x: -x[1]):
        lines.append(f"| {k} | {v} |\n")
    lines.append("\n")

    # Per-page table-issue inventory: sorted by PDF page
    flagged_tables = [t for t in tables if any(
        isinstance(v, bool) and v for v in t["issues"].values()
    ) or any(isinstance(v, int) and v > 0 for v in t["issues"].values())]
    flagged_tables.sort(key=lambda t: t["pdf_page"] or 99999)

    lines.append(f"## Per-Page Table Inventory (flagged tables only)\n\n")
    lines.append(f"Total flagged tables: **{len(flagged_tables)}**\n\n")
    lines.append("| PDF Pg | Label | File:Line | Cols | Widths (cm) | Avg chars | Max chars | Issue | Why | Fix |\n")
    lines.append("|---:|---|---|---:|---|---|---|---|---|---|\n")
    for t in flagged_tables[:200]:
        widths_str = ", ".join(f"{w:.1f}" if w else "L" for w in t["col_widths_cm"])
        avgs_str = ", ".join(f"{a:.0f}" for a in t["col_avg_text_len"])
        maxes_str = ", ".join(str(m) for m in t["col_max_text_len"])
        issues_str = "; ".join(k for k, v in t["issues"].items() if isinstance(v, bool) and v)
        problems, fixes = diagnose_table(t)
        why = " | ".join(problems[:2])[:150] if problems else "—"
        fix = " | ".join(fixes[:2])[:120] if fixes else "—"
        lines.append(f"| {t['pdf_page'] or '?'} | `{t['label']}` | `{t['file']}:{t['line']}` | {t['n_cols']} | {widths_str} | {avgs_str} | {maxes_str} | {issues_str} | {why} | {fix} |\n")
    lines.append("\n")

    OUT_MD.write_text("".join(lines), encoding="utf-8")
    print(f"Report: {OUT_MD}")
    print(f"vbox overflow pages: {len(vbox_events)}")
    print(f"Flagged tables: {len(flagged_tables)}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
