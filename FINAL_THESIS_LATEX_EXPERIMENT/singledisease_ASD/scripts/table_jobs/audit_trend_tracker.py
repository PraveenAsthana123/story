#!/usr/bin/env python3
"""
GGU Trend Tracker
===================

Snapshots key quality metrics each run + diffs vs previous snapshot.
Shows whether the dissertation is improving or regressing over time.

State file: jobs/reports/trend_history.jsonl (append-only, one line per run)
Output:     jobs/reports/trend_dashboard.md (canonical, overwritten)
"""
import json
import re
import sys
import subprocess
from pathlib import Path
from datetime import datetime

ROOT = Path(__file__).resolve().parents[2]
OUT_DIR = ROOT / "jobs" / "reports"
STATE = OUT_DIR / "trend_history.jsonl"
OUT_MD = OUT_DIR / "trend_dashboard.md"


def latest_json(prefix):
    files = sorted(OUT_DIR.glob(f"{prefix}_*.json"))
    return json.loads(files[-1].read_text()) if files else None


def latest_md(prefix):
    files = sorted(OUT_DIR.glob(f"{prefix}_*.md"))
    return files[-1].read_text() if files else None


def parse_md(text, regex, default=0):
    if not text:
        return default
    m = re.search(regex, text)
    return int(m.group(1)) if m else default


def main():
    # Collect current metrics
    now = datetime.now().isoformat()
    metrics = {"timestamp": now}

    # Pages + errors
    pdf = ROOT / "main.pdf"
    if pdf.exists():
        r = subprocess.run(["pdfinfo", str(pdf)], capture_output=True, text=True)
        for line in r.stdout.splitlines():
            if line.startswith("Pages:"):
                metrics["pages"] = int(line.split(":")[1].strip())
                break
    log = ROOT / "main.log"
    if log.exists():
        log_text = log.read_text(errors="ignore")
        metrics["build_errors"] = log_text.count("\n! ")
        metrics["vbox_overflow_count"] = len(re.findall(r"Overfull \\vbox", log_text))
        metrics["hbox_overflow_count"] = len(re.findall(r"Overfull \\hbox", log_text))

    # Table quality
    tq = latest_json("advanced_table_quality")
    if tq:
        ic = tq.get("issue_counts", {})
        metrics["table_right_empty"] = ic.get("right_side_empty", 0)
        metrics["table_tall_column"] = ic.get("tall_column", 0)
        metrics["table_width_imbalanced"] = ic.get("width_imbalanced", 0)
        metrics["table_squeezed"] = ic.get("squeezed_column", 0)
        metrics["table_under_width"] = ic.get("under_width_allocated", 0)

    # Bottom overflow
    bo = latest_json("bottom_overflow_visual")
    if bo:
        metrics["bottom_overflow_warn"] = bo.get("warn_pages_count", 0)
        metrics["bottom_overflow_crit"] = bo.get("crit_pages_count", 0)

    # Per-page sparse
    pv = latest_json("per_page_visual")
    if pv:
        s = pv.get("summary", {})
        metrics["page_sparse"] = s.get("very_low_content", 0)
        metrics["page_half_empty"] = s.get("low_content_extent", 0)

    # Per-table master
    ptm = latest_json("per_table_master")
    if ptm:
        bv = ptm.get("by_verdict", {})
        metrics["table_pass"] = bv.get("PASS", 0)
        metrics["table_watch"] = bv.get("WATCH", 0)
        metrics["table_review"] = bv.get("REVIEW", 0)

    # Leak counts
    metrics["policy_section_sign_leaks"] = parse_md(latest_md("policy_section_sign_leak"),
                                                     r"\*\*Leaks found\*\*[^:]*:\s*\*\*(\d+)\*\*")
    metrics["jargon_leaks"] = parse_md(latest_md("jargon_leaks"),
                                        r"^Total leaks:\s*(\d+)", 0)

    # Content redundancy
    cr = latest_md("content_redundancy")
    if cr:
        m_rep = re.search(r"Repeated sentences[^|]*\|\s*(\d+)", cr)
        m_long = re.search(r"Long sentences[^|]*\|\s*(\d+)", cr)
        metrics["repeated_sentences"] = int(m_rep.group(1)) if m_rep else 0
        metrics["long_sentences"] = int(m_long.group(1)) if m_long else 0

    # Append to history
    with STATE.open("a") as f:
        f.write(json.dumps(metrics) + "\n")

    # Load history for trend
    history = []
    if STATE.exists():
        with STATE.open() as f:
            for line in f:
                line = line.strip()
                if line:
                    history.append(json.loads(line))

    # Render trend dashboard
    lines = []
    lines.append(f"# Quality Trend Dashboard\n\n")
    lines.append(f"Updated: {now}\n\n")
    lines.append(f"History: {len(history)} snapshots in `trend_history.jsonl`\n\n")

    if len(history) < 2:
        lines.append("_Only 1 snapshot so far — need ≥ 2 for trend comparison._\n")
        OUT_MD.write_text("".join(lines))
        print(f"Dashboard: {OUT_MD}")
        return

    # Current vs previous + first (oldest)
    current = history[-1]
    previous = history[-2]
    first = history[0]

    keys = sorted(set(current.keys()) - {"timestamp"})
    lines.append("## Metric Trend (Current vs Previous vs First Snapshot)\n\n")
    lines.append("| Metric | First | Previous | Current | Δ Prev | Δ First |\n")
    lines.append("|---|---:|---:|---:|---:|---:|\n")
    for k in keys:
        c = current.get(k, "—")
        p = previous.get(k, "—")
        f = first.get(k, "—")
        try:
            dp = int(c) - int(p)
            df = int(c) - int(f)
            dp_str = f"{dp:+d}" if dp != 0 else "—"
            df_str = f"{df:+d}" if df != 0 else "—"
        except (ValueError, TypeError):
            dp_str = df_str = "—"
        lines.append(f"| `{k}` | {f} | {p} | **{c}** | {dp_str} | {df_str} |\n")

    OUT_MD.write_text("".join(lines))
    print(f"Dashboard: {OUT_MD}")
    print(f"\nKey trends (current vs previous):")
    for k in ["pages", "build_errors", "table_review", "bottom_overflow_crit", "jargon_leaks"]:
        if k in current and k in previous:
            try:
                d = int(current[k]) - int(previous[k])
                arrow = "↑" if d > 0 else ("↓" if d < 0 else "→")
                print(f"  {k}: {previous[k]} → {current[k]} {arrow}{abs(d)}")
            except (ValueError, TypeError):
                pass


if __name__ == "__main__":
    main()
