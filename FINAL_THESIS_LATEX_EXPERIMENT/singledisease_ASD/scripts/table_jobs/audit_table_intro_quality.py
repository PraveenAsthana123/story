#!/usr/bin/env python3
"""
GGU Table Intro Quality Audit + Per-Chapter Scorer
====================================================

For every xltabular block, scores the table's introduction quality 1-5:

  5  HEADING + NON-STUB INTRO + TABLE                     (best)
  4  HEADING + good intro (intro inside caption is fine)
  3  HEADING-ONLY + table  OR  INTRO-ONLY + table
  2  No clear heading; table preceded by long generic intro
  1  Table dumped without context (no heading, no intro)

Also detects duplicated content (same `\ref{label}` mentioned 2+ times
in pre-table context).

Output: jobs/reports/table_intro_quality_YYYYMMDD_HHMM.md
        Per-chapter score aggregation + per-table detail
"""
import re
import json
import sys
from pathlib import Path
from datetime import datetime
from collections import defaultdict

ROOT = Path(__file__).resolve().parents[2]
OUT_DIR = ROOT / "jobs" / "reports"
OUT_DIR.mkdir(parents=True, exist_ok=True)
TS = datetime.now().strftime("%Y%m%d_%H%M")
OUT_MD = OUT_DIR / f"table_intro_quality_{TS}.md"
OUT_JSON = OUT_DIR / f"table_intro_quality_{TS}.json"

CHAPTERS = {
    "chapter1_introduction": "Ch.1 Introduction",
    "chapter2_literature": "Ch.2 Literature Review",
    "chapter3_research_methods": "Ch.3 Research Methods",
    "chapter4_analysis_findings": "Ch.4 Data Analysis",
    "chapter5_discussion_recommendations": "Ch.5 Discussion",
}


def score_intro(pre_context, label):
    """Score an intro 1-5 based on heading + intro presence + de-duplication."""
    # Count \ref{label} mentions in pre-context
    ref_mentions = len(re.findall(r"\\ref\{" + re.escape(label) + r"\}", pre_context))
    # Heading: \paragraph{...} or \subsection{...} in pre-context (last 500 chars)
    last_500 = pre_context[-500:]
    has_heading = bool(re.search(r"\\(?:paragraph|subsubsection|subsection|section)\*?\{[^}]+\}", last_500))
    # Intro paragraph: last non-empty line with > 60 chars
    lines = [l for l in last_500.splitlines() if l.strip() and not l.strip().startswith("%")]
    has_intro = False
    has_stub_intro = False
    for line in lines[-5:]:
        s = line.strip()
        if len(s) > 60 and not s.startswith("\\paragraph") and not s.startswith("\\section"):
            has_intro = True
            if "laying out each row in a structured form" in s:
                has_stub_intro = True

    # Score
    if has_heading and has_intro and not has_stub_intro and ref_mentions <= 1:
        return 5, "HEADING + non-stub intro + single ref"
    elif has_heading and has_intro and ref_mentions <= 1:
        return 4, "HEADING + intro (slightly stubby) + single ref"
    elif has_heading and has_intro and ref_mentions >= 2:
        return 3, "HEADING + intro + DUPLICATE refs"
    elif has_heading and not has_intro:
        return 3, "HEADING only (no body intro)"
    elif has_intro and not has_heading:
        return 2, "intro only (no heading)"
    elif has_stub_intro:
        return 2, "stub intro only"
    else:
        return 1, "no heading + no intro"


def main():
    results = defaultdict(list)
    files = list((ROOT / "chapters").glob("*.tex")) + list((ROOT / "appendices").glob("*.tex"))
    files = [f for f in files if "pre_" not in f.name and ".session_backups" not in str(f)]

    for fp in files:
        txt = fp.read_text(encoding="utf-8")
        rel = str(fp.relative_to(ROOT))
        # Map to chapter
        chap = "Other"
        for key, name in CHAPTERS.items():
            if key in fp.name:
                chap = name
                break
        if chap == "Other" and "appendices" in rel:
            chap = f"App. {fp.name.split('_')[0]}"

        for m in re.finditer(r"\\begin\{xltabular\}.*?\\label\{([^}]+)\}.*?\\end\{xltabular\}", txt, re.DOTALL):
            label = m.group(1)
            pre_context = txt[max(0, m.start() - 2000):m.start()]
            score, reason = score_intro(pre_context, label)
            line_no = txt[:m.start()].count("\n") + 1
            # Extract caption short
            cap_m = re.search(r"\\caption\[([^\]]+)\]", m.group(0))
            short_cap = cap_m.group(1)[:60] if cap_m else "?"
            results[chap].append({
                "file": rel,
                "line": line_no,
                "label": label,
                "caption_short": short_cap,
                "score": score,
                "reason": reason,
            })

    # Output
    OUT_JSON.write_text(json.dumps({
        "generated": datetime.now().isoformat(),
        "per_chapter": dict(results),
    }, indent=2))

    lines = ["# Table Intro Quality — Per-Chapter Scorecard\n\n"]
    lines.append(f"Generated: {datetime.now().isoformat()}\n\n")
    lines.append("Score 1-5 (higher = better):\n")
    lines.append("- 5: heading + non-stub intro + single ref (BEST)\n")
    lines.append("- 4: heading + intro + single ref\n")
    lines.append("- 3: heading + intro + duplicate refs  OR  heading only\n")
    lines.append("- 2: intro only (no heading)\n")
    lines.append("- 1: no heading + no intro\n\n")

    # Aggregate per chapter
    lines.append("## Chapter Summary\n\n")
    lines.append("| Chapter | Tables | Avg Score | Score≥4 | Score≤2 |\n")
    lines.append("|---|---:|---:|---:|---:|\n")
    grand_total = 0
    grand_sum = 0
    for chap in sorted(results.keys()):
        tabs = results[chap]
        avg = sum(t["score"] for t in tabs) / len(tabs)
        good = sum(1 for t in tabs if t["score"] >= 4)
        bad = sum(1 for t in tabs if t["score"] <= 2)
        lines.append(f"| {chap} | {len(tabs)} | {avg:.2f} | {good} | {bad} |\n")
        grand_total += len(tabs)
        grand_sum += sum(t["score"] for t in tabs)
    lines.append(f"| **TOTAL** | **{grand_total}** | **{grand_sum/grand_total:.2f}** | — | — |\n\n")

    # Per-chapter detail (top 30 lowest-score per chapter)
    for chap in sorted(results.keys()):
        tabs = results[chap]
        low = sorted([t for t in tabs if t["score"] <= 3], key=lambda x: x["score"])[:30]
        if not low:
            continue
        lines.append(f"## {chap} — Lowest-Scoring Tables (score ≤ 3)\n\n")
        lines.append("| Score | Label | File:Line | Caption | Reason |\n")
        lines.append("|---:|---|---|---|---|\n")
        for t in low:
            lines.append(f"| {t['score']} | `{t['label']}` | `{t['file']}:{t['line']}` | {t['caption_short']} | {t['reason']} |\n")
        lines.append("\n")

    OUT_MD.write_text("".join(lines))
    print(f"Report MD:   {OUT_MD}")
    print(f"Report JSON: {OUT_JSON}")
    for chap in sorted(results.keys()):
        tabs = results[chap]
        avg = sum(t["score"] for t in tabs) / len(tabs)
        print(f"  {chap}: {len(tabs)} tables, avg score {avg:.2f}")


if __name__ == "__main__":
    main()
