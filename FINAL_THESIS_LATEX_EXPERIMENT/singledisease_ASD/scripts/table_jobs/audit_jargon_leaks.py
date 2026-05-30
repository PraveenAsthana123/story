#!/usr/bin/env python3
"""
GGU CLAUDE.md Jargon Leak Audit
=================================

Detects internal CLAUDE.md vocabulary that leaked into user-facing
thesis text (drill, forensic substrate, operator, brutal rule, etc.).

Output: jobs/reports/jargon_leaks_YYYYMMDD_HHMM.md
"""
import re
import sys
from pathlib import Path
from datetime import datetime
from collections import defaultdict

ROOT = Path(__file__).resolve().parents[2]
OUT_DIR = ROOT / "jobs" / "reports"
TS = datetime.now().strftime("%Y%m%d_%H%M")
OUT_MD = OUT_DIR / f"jargon_leaks_{TS}.md"

JARGON_PATTERNS = {
    # "drill" excluded — Appendix Q "Drill Methodology" makes it a thesis term
    "forensic_substrate": r"forensic substrate",
    "brutal_rule": r"\bbrutal\s+(?:rule|review|lesson)\b",
    "per_global": r"\bper\s+(?:the\s+)?global\b",
    "CLAUDE_md": r"CLAUDE\.md|CLAUDE\s+Code|CLAUDE\s+policy",
    "operator_jargon": r"\boperator-prompted\b|\boperator\s+approval\b",
    # § followed by digit (not by \ref) — true policy-leak pattern
    "policy_section_number": r"§\d+(?:\.\d+)?(?!\s*\\ref)",
    # § followed by Capital letter (section name like §Reading Guide)
    "policy_section_name": r"§(?=[A-Z][a-z])",
    "compose_with_section": r"compose[ds]?\s+with\s+§\d+",
    "aligned_with_section": r"[Aa]ligned\s+with\s+§\d+",
}


def main():
    files = list((ROOT / "chapters").glob("*.tex")) + list((ROOT / "appendices").glob("*.tex"))
    files = [f for f in files if "pre_" not in f.name and ".session_backups" not in str(f)]

    findings = defaultdict(list)
    for fp in files:
        rel = str(fp.relative_to(ROOT))
        try:
            lines = fp.read_text().split("\n")
        except Exception:
            continue
        for lineno, line in enumerate(lines, 1):
            if line.strip().startswith("%"):
                continue
            for tag, pat in JARGON_PATTERNS.items():
                for m in re.finditer(pat, line):
                    ctx_start = max(0, m.start() - 25)
                    ctx_end = min(len(line), m.end() + 35)
                    ctx = line[ctx_start:ctx_end].strip()
                    findings[tag].append({
                        "file": rel, "line": lineno, "context": ctx,
                    })

    # Per-tag counts
    out = []
    out.append(f"# CLAUDE.md Jargon Leaks Audit — {datetime.now().isoformat()}\n\n")
    out.append("Policy: `~/.claude/policies/no-policy-leak-section-sign.md` + this audit\n\n")
    out.append("## Summary\n\n")
    out.append("| Jargon Tag | Count |\n|---|---:|\n")
    for tag in sorted(JARGON_PATTERNS.keys()):
        out.append(f"| {tag} | {len(findings[tag])} |\n")
    total = sum(len(v) for v in findings.values())
    out.append(f"| **TOTAL** | **{total}** |\n\n")

    if total:
        out.append("## Detail (top 100 per tag)\n\n")
        for tag in sorted(JARGON_PATTERNS.keys()):
            if not findings[tag]:
                continue
            out.append(f"### {tag} ({len(findings[tag])})\n\n")
            out.append("| File:Line | Context |\n|---|---|\n")
            for f in findings[tag][:50]:
                ctx = f["context"].replace("|", "\\|")
                out.append(f"| `{f['file']}:{f['line']}` | `{ctx}` |\n")
            out.append("\n")

    OUT_MD.write_text("".join(out))
    print(f"Report: {OUT_MD}")
    print(f"Total leaks: {total}")
    for tag in sorted(JARGON_PATTERNS.keys()):
        if findings[tag]:
            print(f"  {tag}: {len(findings[tag])}")


if __name__ == "__main__":
    main()
