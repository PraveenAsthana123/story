#!/usr/bin/env python3
"""
GGU Per-Table Master Audit
============================

ONE row per table consolidating ALL checks (replaces "1 agent per table"):
  - Column quality (right-empty, tall-col, width-imbal, squeezed, underused, under-width)
  - Intro quality + smartness score
  - Bottom-overflow proximity (is this table on a bottom-overflow page?)
  - Heading-caption duplicate
  - Overall PASS/REVIEW/FAIL verdict

Output: jobs/reports/per_table_master_YYYYMMDD_HHMM.{md,json}
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
OUT_MD = OUT_DIR / f"per_table_master_{TS}.md"
OUT_JSON = OUT_DIR / f"per_table_master_{TS}.json"


def latest(prefix):
    files = sorted(OUT_DIR.glob(f"{prefix}_*.json"))
    return json.loads(files[-1].read_text()) if files else None


def main():
    tq = latest("advanced_table_quality")
    if not tq:
        sys.exit("Run advanced_table_quality first.")

    # Get table → page map from main.aux
    aux = (ROOT / "main.aux").read_text(errors="ignore") if (ROOT / "main.aux").exists() else ""
    label_pages = {}
    for m in re.finditer(r"\\newlabel\{(tab:[^}]+)\}\{\{[^}]*\}\{(\d+)\}", aux):
        label_pages[m.group(1)] = int(m.group(2))

    # Get bottom-overflow pages
    bo = latest("bottom_overflow_visual")
    overflow_pages = set()
    if bo:
        for p in bo["flagged_pages"]:
            overflow_pages.add(p["pdf_page"])

    # Get intro quality per table (via label)
    iq = latest("table_intro_quality")
    intro_by_label = {}
    if iq:
        for chap, tabs in iq["per_chapter"].items():
            for t in tabs:
                intro_by_label[t["label"]] = t["score"]

    # Build per-table master record
    master = []
    for t in tq["tables"]:
        label = t["label"]
        page = label_pages.get(label)
        i = t["issues"]
        n_issues = sum(1 for k, v in i.items() if (isinstance(v, bool) and v) or (isinstance(v, int) and v > 0))
        bottom_overflow = page in overflow_pages if page else False
        intro_score = intro_by_label.get(label, 0)

        # Overall verdict
        critical = bool(i.get("right_side_empty") or i.get("squeezed_column") or i.get("very_multi_page"))
        if bottom_overflow or critical or intro_score <= 2:
            verdict = "REVIEW"
        elif n_issues == 0 and intro_score >= 4:
            verdict = "PASS"
        else:
            verdict = "WATCH"

        master.append({
            "label": label,
            "file": t["file"],
            "line": t["line"],
            "page": page,
            "n_cols": t["n_cols"],
            "n_rows": t["n_rows"],
            "n_issues": n_issues,
            "issues": [k for k, v in i.items() if (isinstance(v, bool) and v)],
            "intro_score": intro_score,
            "bottom_overflow": bottom_overflow,
            "verdict": verdict,
        })

    # Aggregate
    verdict_counts = defaultdict(int)
    for m in master:
        verdict_counts[m["verdict"]] += 1

    # Write JSON
    OUT_JSON.write_text(json.dumps({
        "generated": datetime.now().isoformat(),
        "total": len(master),
        "by_verdict": dict(verdict_counts),
        "tables": master,
    }, indent=2))

    # Render MD
    lines = []
    lines.append(f"# Per-Table Master Audit — {datetime.now().isoformat()}\n\n")
    lines.append(f"Total tables: **{len(master)}**\n\n")
    lines.append("| Verdict | Count |\n|---|---:|\n")
    for v, c in sorted(verdict_counts.items()):
        lines.append(f"| {v} | {c} |\n")
    lines.append("\n")

    # REVIEW tables (highest priority)
    review = sorted([m for m in master if m["verdict"] == "REVIEW"],
                    key=lambda x: (-x["n_issues"], -x["intro_score"]))
    lines.append(f"## REVIEW Tables ({len(review)} — needs human attention)\n\n")
    lines.append("| Page | Label | n_cols | n_rows | Issues | Intro | Bot.Ovf | Issue Tags |\n")
    lines.append("|---:|---|---:|---:|---:|---:|---|---|\n")
    for m in review[:200]:
        bo_flag = "🔥" if m["bottom_overflow"] else ""
        tags = ", ".join(m["issues"][:3])[:60]
        lines.append(f"| {m['page'] or '?'} | `{m['label']}` | {m['n_cols']} | {m['n_rows']} | "
                     f"{m['n_issues']} | {m['intro_score']} | {bo_flag} | {tags} |\n")
    lines.append("\n")

    OUT_MD.write_text("".join(lines))
    print(f"Report MD:   {OUT_MD}")
    print(f"Report JSON: {OUT_JSON}")
    print(f"\nTotal tables: {len(master)}")
    for v, c in sorted(verdict_counts.items()):
        print(f"  {v}: {c}")


if __name__ == "__main__":
    main()
