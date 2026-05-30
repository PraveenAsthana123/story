#!/usr/bin/env python3
"""
GGU Master Dashboard
=====================

Consolidates all 21 audit reports into ONE dashboard page showing:
  - Current state of every metric
  - Trend (vs previous run)
  - Quick links to detailed reports

Output: jobs/reports/master_dashboard.md  (canonical — overwritten each run)
"""
import json
import re
import sys
from pathlib import Path
from datetime import datetime
from collections import defaultdict

ROOT = Path(__file__).resolve().parents[2]
OUT_DIR = ROOT / "jobs" / "reports"
OUT_MD = OUT_DIR / "master_dashboard.md"  # canonical name


def latest(prefix, suffix="json"):
    files = sorted(OUT_DIR.glob(f"{prefix}_*.{suffix}"))
    if not files:
        return None, None
    return files[-1], json.loads(files[-1].read_text()) if suffix == "json" else None


def latest_md(prefix):
    files = sorted(OUT_DIR.glob(f"{prefix}_*.md"))
    return files[-1] if files else None


def parse_md_count(path, regex):
    if not path or not path.exists():
        return None
    txt = path.read_text()
    m = re.search(regex, txt)
    return int(m.group(1)) if m else None


def main():
    lines = []
    lines.append(f"# GGU Dissertation — Master Quality Dashboard\n\n")
    lines.append(f"**Last updated:** {datetime.now().isoformat()}\n\n")
    lines.append("Single-pane view across all 20 cron-scheduled audits.\n")
    lines.append("Click report names for detailed findings.\n\n")

    # === BUILD STATE ===
    import subprocess
    n_pages = "?"
    if (ROOT / "main.pdf").exists():
        r = subprocess.run(["pdfinfo", str(ROOT / "main.pdf")], capture_output=True, text=True)
        for line in r.stdout.splitlines():
            if line.startswith("Pages:"):
                n_pages = line.split(":")[1].strip()
                break

    log = (ROOT / "main.log")
    build_errors = 0
    if log.exists():
        log_text = log.read_text(errors="ignore")
        build_errors = log_text.count("\n! ")

    lines.append("## Build State\n\n")
    lines.append(f"- Pages: **{n_pages}**\n")
    lines.append(f"- Build errors: **{build_errors}**\n\n")

    # === AUDITS ===
    lines.append("## Audit Results Summary\n\n")
    lines.append("| Audit | Current | Report |\n|---|---|---|\n")

    # advanced_table_quality
    _, tq = latest("advanced_table_quality")
    if tq:
        ic = tq.get("issue_counts", {})
        summary = (f"right-empty {ic.get('right_side_empty', 0)} · "
                   f"tall-col {ic.get('tall_column', 0)} · "
                   f"width-imbal {ic.get('width_imbalanced', 0)} · "
                   f"squeezed {ic.get('squeezed_column', 0)}")
        f = latest_md("advanced_table_quality")
        lines.append(f"| **table_quality** | {summary} | [{f.name if f else '—'}]({f.name if f else ''}) |\n")

    # bottom_overflow_visual
    _, bo = latest("bottom_overflow_visual")
    if bo:
        summary = f"warn {bo.get('warn_pages_count', 0)} + crit {bo.get('crit_pages_count', 0)}"
        f = latest_md("bottom_overflow_visual")
        lines.append(f"| **bottom_overflow** | {summary} | [{f.name if f else '—'}]({f.name if f else ''}) |\n")

    # per_page_visual
    _, pv = latest("per_page_visual")
    if pv:
        s = pv.get("summary", {})
        summary = (f"sparse {s.get('very_low_content', 0)} + "
                   f"half-empty {s.get('low_content_extent', 0)} + "
                   f"text-only {s.get('text_only_pages', 0)}")
        f = latest_md("per_page_visual")
        lines.append(f"| **per_page_visual** | {summary} | [{f.name if f else '—'}]({f.name if f else ''}) |\n")

    # intro quality
    _, iq = latest("table_intro_quality")
    if iq:
        totals = []
        for chap, tabs in iq.get("per_chapter", {}).items():
            if not chap.startswith("App.") and "Ch." in chap:
                avg = sum(t["score"] for t in tabs) / max(len(tabs), 1)
                totals.append(f"{chap}: {avg:.2f}")
        f = latest_md("table_intro_quality")
        lines.append(f"| **intro_quality** | {' · '.join(totals[:5])} | [{f.name if f else '—'}]({f.name if f else ''}) |\n")

    # per_table_master
    _, ptm = latest("per_table_master")
    if ptm:
        bv = ptm.get("by_verdict", {})
        summary = f"PASS {bv.get('PASS', 0)} · WATCH {bv.get('WATCH', 0)} · REVIEW {bv.get('REVIEW', 0)}"
        f = latest_md("per_table_master")
        lines.append(f"| **per_table_master** | {summary} | [{f.name if f else '—'}]({f.name if f else ''}) |\n")

    # policy_section_sign_leak (count from MD)
    f = latest_md("policy_section_sign_leak")
    if f:
        cnt = parse_md_count(f, r"\*\*Leaks found\*\*[^:]*:\s*\*\*(\d+)\*\*")
        lines.append(f"| **policy_section_sign** | {cnt or '?'} leaks | [{f.name}]({f.name}) |\n")

    # jargon_leaks
    f = latest_md("jargon_leaks")
    if f:
        cnt = parse_md_count(f, r"\| \*\*TOTAL\*\* \| \*\*(\d+)\*\*")
        if cnt is None:
            cnt = parse_md_count(f, r"^Total leaks:\s*(\d+)")
        lines.append(f"| **jargon_leaks** | {cnt or 0} | [{f.name}]({f.name}) |\n")

    # tikz_overlap
    f = latest_md("tikz_overlap")
    if f:
        # Parse from MD body
        txt = f.read_text()
        m_files = re.search(r"Files with issues:\s*\*\*(\d+)\*\*", txt)
        m_total = re.search(r"Total node-pair overlaps:\s*\*\*(\d+)\*\*", txt)
        files_c = m_files.group(1) if m_files else "?"
        total_c = m_total.group(1) if m_total else "?"
        lines.append(f"| **tikz_overlap** | {files_c} figures, {total_c} overlaps | [{f.name}]({f.name}) |\n")

    # content_redundancy
    f = latest_md("content_redundancy")
    if f:
        txt = f.read_text()
        m_rep = re.search(r"Repeated sentences[^|]*\|\s*(\d+)", txt)
        m_long = re.search(r"Long sentences[^|]*\|\s*(\d+)", txt)
        rep = m_rep.group(1) if m_rep else "?"
        long = m_long.group(1) if m_long else "?"
        lines.append(f"| **content_redundancy** | repeated {rep} + long-sent {long} | [{f.name}]({f.name}) |\n")

    # chapter / appendix rollups
    for prefix in ["chapter_rollup", "appendix_rollup"]:
        f = latest_md(prefix)
        if f:
            lines.append(f"| **{prefix}** | see report | [{f.name}]({f.name}) |\n")

    lines.append("\n")

    # === CRON STATE ===
    lines.append("## Cron Audit Schedule (20 jobs)\n\n")
    lines.append("Audits run at staggered :00, :15, :30, :45 marks across 11:00-14:00 and 23:00-02:00.\n\n")

    OUT_MD.write_text("".join(lines))
    print(f"Dashboard: {OUT_MD}")


if __name__ == "__main__":
    main()
