#!/usr/bin/env python3
"""
GGU Per-Appendix Rollup Audit
==============================

Same as chapter_rollup but breaks down by appendix letter (A-S).

Output: jobs/reports/appendix_rollup_YYYYMMDD_HHMM.md
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
OUT_MD = OUT_DIR / f"appendix_rollup_{TS}.md"


def latest(prefix):
    files = sorted(OUT_DIR.glob(f"{prefix}_*.json"))
    return json.loads(files[-1].read_text()) if files else None


def main():
    tq = latest("advanced_table_quality")
    iq = latest("table_intro_quality")
    bo = latest("bottom_overflow_visual")

    apx = defaultdict(lambda: {
        "n_tables": 0, "issues": defaultdict(int),
        "intro_sum": 0, "intro_n": 0, "intro_low": 0,
        "bottom_warn": 0, "bottom_crit": 0,
    })

    # Tables
    if tq:
        for t in tq["tables"]:
            if "appendices/" not in t["file"]:
                continue
            name = t["file"].split("/")[1].split("_")[0]
            apx[name]["n_tables"] += 1
            for k, v in t["issues"].items():
                if isinstance(v, bool) and v:
                    apx[name]["issues"][k] += 1
                elif isinstance(v, int) and v > 0:
                    apx[name]["issues"][k] += v

    # Intro quality
    if iq:
        for chap, tabs in iq["per_chapter"].items():
            if chap.startswith("App."):
                name = chap[5:].strip()
                for t in tabs:
                    apx[name]["intro_sum"] += t["score"]
                    apx[name]["intro_n"] += 1
                    if t["score"] <= 2:
                        apx[name]["intro_low"] += 1

    # Bottom overflow - need appendix page ranges
    aux = (ROOT / "main.aux").read_text(errors="ignore") if (ROOT / "main.aux").exists() else ""
    apx_ranges = []
    for m in re.finditer(r"\\@writefile\{toc\}\{\\contentsline\s*\{chapter\}\{[^}]*Appendix\s+([A-Z])[^}]*\}\{(\d+)\}", aux):
        apx_ranges.append((m.group(1), int(m.group(2))))
    apx_ranges.sort(key=lambda x: x[1])
    apx_ranges.append(("end", 99999))

    if bo:
        for p in bo["flagged_pages"]:
            for i, (name, start) in enumerate(apx_ranges[:-1]):
                end = apx_ranges[i + 1][1] - 1
                if start <= p["pdf_page"] <= end:
                    if p["severity"] == "critical":
                        apx[name]["bottom_crit"] += 1
                    else:
                        apx[name]["bottom_warn"] += 1
                    break

    # Render
    lines = []
    lines.append(f"# Per-Appendix Rollup Audit\n\n")
    lines.append(f"Generated: {datetime.now().isoformat()}\n\n")

    lines.append("## Appendix Summary\n\n")
    lines.append("| App | Tables | Issues | Intro Avg | Low-Score Intros | Bottom-Overflow (Warn+Crit) |\n")
    lines.append("|---|---:|---:|---:|---:|---:|\n")
    for name in sorted(apx.keys()):
        a = apx[name]
        if a["n_tables"] == 0 and a["bottom_warn"] + a["bottom_crit"] == 0:
            continue
        issues = sum(a["issues"].values())
        intro_avg = a["intro_sum"] / a["intro_n"] if a["intro_n"] else 0
        bo_total = a["bottom_warn"] + a["bottom_crit"]
        flag = ""
        if a["intro_low"] >= 5 or intro_avg < 3.5:
            flag += " ⚠"
        if bo_total >= 20:
            flag += " 🔥"
        lines.append(f"| App.{name} | {a['n_tables']} | {issues} | {intro_avg:.2f} | {a['intro_low']} | {bo_total}{flag} |\n")
    lines.append("\n⚠ = intro quality concern · 🔥 = high bottom-overflow\n\n")

    # Issue breakdown per appendix
    lines.append("## Per-Appendix Issue Type Breakdown\n\n")
    lines.append("| App | Right-Empty | Tall-Col | Width-Imbal | Squeezed | Underused | Under-Width |\n")
    lines.append("|---|---:|---:|---:|---:|---:|---:|\n")
    for name in sorted(apx.keys()):
        a = apx[name]
        if a["n_tables"] == 0:
            continue
        i = a["issues"]
        lines.append(f"| App.{name} | {i['right_side_empty']} | {i['tall_column']} | "
                     f"{i['width_imbalanced']} | {i['squeezed_column']} | {i['underused_column']} | "
                     f"{i['under_width_allocated']} |\n")
    lines.append("\n")

    OUT_MD.write_text("".join(lines))
    print(f"Report: {OUT_MD}")
    # Brief stdout summary
    print(f"\n{'App':>5} | {'Tables':>6} | {'Issues':>6} | {'Intro':>5} | {'BotOvf':>6}")
    print("-" * 50)
    for name in sorted(apx.keys()):
        a = apx[name]
        if a["n_tables"] == 0 and a["bottom_warn"] + a["bottom_crit"] == 0:
            continue
        issues = sum(a["issues"].values())
        intro_avg = a["intro_sum"] / a["intro_n"] if a["intro_n"] else 0
        bo_total = a["bottom_warn"] + a["bottom_crit"]
        print(f"App.{name:<2}| {a['n_tables']:>6} | {issues:>6} | {intro_avg:>5.2f} | {bo_total:>6}")


if __name__ == "__main__":
    main()
