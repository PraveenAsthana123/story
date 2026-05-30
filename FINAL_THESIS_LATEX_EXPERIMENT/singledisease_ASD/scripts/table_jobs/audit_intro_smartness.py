#!/usr/bin/env python3
"""
GGU Intro Smartness Audit
==========================

Scores each clarity-intro for SMARTNESS:
  5  Meaningful row-subject + grammatical + describes table well
  4  Generic but grammatical
  3  Has minor grammar issues (singular/plural)
  2  Uses placeholder subject like "#" or "id" or "row"
  1  Empty / missing / malformed

Output: jobs/reports/intro_smartness_YYYYMMDD_HHMM.md
"""
import re
import json
import sys
from pathlib import Path
from datetime import datetime
from collections import defaultdict

ROOT = Path(__file__).resolve().parents[2]
OUT_DIR = ROOT / "jobs" / "reports"
TS = datetime.now().strftime("%Y%m%d_%H%M")
OUT_MD = OUT_DIR / f"intro_smartness_{TS}.md"


def score(intro):
    """Score an intro 1-5 for smartness."""
    if not intro or len(intro) < 30:
        return 1, "missing/too-short"
    # Check for placeholder row-subject
    if re.search(r"lists each \\textit\{(?:#|\\#|id|row|item)\}", intro, re.IGNORECASE):
        return 2, "placeholder row-subject (#, id, row, item)"
    # Grammar: "1 more dimensions" should be singular
    if "1 more dimensions" in intro:
        return 3, "grammar: 1 dimensions (should be dimension)"
    # Generic fallback
    if "presents " in intro.lower() and "covering" in intro.lower():
        return 4, "generic 'presents...covering' template"
    if "This table" in intro and "across" in intro:
        return 5, "meaningful clarity-intro"
    return 4, "other valid intro"


def main():
    files = list((ROOT / "chapters").glob("*.tex")) + list((ROOT / "appendices").glob("*.tex"))
    files = [f for f in files if "pre_" not in f.name and ".session_backups" not in str(f)]

    scores = defaultdict(list)
    for fp in files:
        rel = str(fp.relative_to(ROOT))
        txt = fp.read_text()
        # Find clarity-style intros
        for m in re.finditer(
            r"\\noindent\s+(?:This table[^\n]+|Table~\\ref\{[^}]+\}[^\n]+)\.",
            txt
        ):
            intro = m.group(0)
            s, reason = score(intro)
            line_no = txt[:m.start()].count("\n") + 1
            scores[rel].append({
                "line": line_no, "intro": intro[:120],
                "score": s, "reason": reason,
            })

    # Aggregate + render
    lines = []
    lines.append(f"# Intro Smartness Audit — {datetime.now().isoformat()}\n\n")
    lines.append("Score 1-5: 5=meaningful · 4=generic · 3=grammar issue · 2=placeholder · 1=missing\n\n")

    grand_total = 0
    grand_sum = 0
    lines.append("## Per-File Summary\n\n")
    lines.append("| File | Intros | Avg | Score≤2 |\n|---|---:|---:|---:|\n")
    for fp, intros in sorted(scores.items()):
        if not intros:
            continue
        avg = sum(i["score"] for i in intros) / len(intros)
        low = sum(1 for i in intros if i["score"] <= 2)
        lines.append(f"| `{fp}` | {len(intros)} | {avg:.2f} | {low} |\n")
        grand_total += len(intros)
        grand_sum += sum(i["score"] for i in intros)
    lines.append(f"\n**Total intros: {grand_total} | Avg score: {grand_sum/max(grand_total,1):.2f}**\n\n")

    # Worst intros
    all_intros = []
    for fp, intros in scores.items():
        for i in intros:
            all_intros.append({**i, "file": fp})
    worst = sorted(all_intros, key=lambda x: x["score"])[:60]
    lines.append("## Worst 60 Intros (lowest score)\n\n")
    lines.append("| Score | File:Line | Reason | Intro |\n|---:|---|---|---|\n")
    for i in worst:
        intro_short = i["intro"][:80].replace("\n", " ").replace("|", "\\|")
        lines.append(f"| {i['score']} | `{i['file']}:{i['line']}` | {i['reason']} | {intro_short} |\n")

    OUT_MD.write_text("".join(lines))
    print(f"Report: {OUT_MD}")
    print(f"Total intros: {grand_total} | Avg score: {grand_sum/max(grand_total,1):.2f}")
    print(f"Score 1: {sum(1 for i in all_intros if i['score']==1)}")
    print(f"Score 2: {sum(1 for i in all_intros if i['score']==2)}")
    print(f"Score 3: {sum(1 for i in all_intros if i['score']==3)}")
    print(f"Score 4: {sum(1 for i in all_intros if i['score']==4)}")
    print(f"Score 5: {sum(1 for i in all_intros if i['score']==5)}")


if __name__ == "__main__":
    main()
