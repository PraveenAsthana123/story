#!/usr/bin/env python3
"""
GGU Policy Section-Sign Leak Audit
====================================

Detects unwanted §<num> references (from CLAUDE.md policy section numbers
like §38, §47.6) that leaked into user-facing deliverable text.

Allowed: ISO/IEC/RFC/HIPAA/EU/Article §<num>, and §\\ref{...}
Flagged:  "per global §X", "Aligned with §X", "(§X note)" etc.

Output: jobs/reports/policy_section_sign_leak_YYYYMMDD_HHMM.md
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
OUT_MD = OUT_DIR / f"policy_section_sign_leak_{TS}.md"

# Standards prefixes — § after these is LEGITIMATE
LEGIT_PREFIXES = ["ISO", "IEC", "RFC", "HIPAA", "GDPR", "EU AI Act", "Article", "Art.", "ASTM", "FDA", "PMBOK"]


def is_legit(line, pos):
    """Return True if the § at `pos` in `line` is preceded by a standards prefix."""
    before = line[max(0, pos - 30):pos]
    for p in LEGIT_PREFIXES:
        if re.search(r"\b" + re.escape(p) + r"\s+\d*\s*$", before):
            return True
    # Or followed by \ref{...}
    after = line[pos:pos + 15]
    if after.startswith("§\\ref"):
        return True
    return False


def main():
    files = list((ROOT / "chapters").glob("*.tex")) + list((ROOT / "appendices").glob("*.tex"))
    files = [f for f in files if "pre_" not in f.name and ".session_backups" not in str(f)]

    leaks = []
    total_legit = 0
    for fp in files:
        rel = str(fp.relative_to(ROOT))
        try:
            lines = fp.read_text().split("\n")
        except Exception:
            continue
        for lineno, line in enumerate(lines, 1):
            if line.strip().startswith("%"):
                continue  # skip comment lines
            for m in re.finditer(r"§", line):
                pos = m.start()
                if is_legit(line, pos):
                    total_legit += 1
                    continue
                # Capture 20-char context for the leak
                ctx_start = max(0, pos - 30)
                ctx_end = min(len(line), pos + 40)
                ctx = line[ctx_start:ctx_end].strip()
                leaks.append({
                    "file": rel, "line": lineno,
                    "context": ctx,
                })

    # Group by file
    by_file = defaultdict(int)
    for l in leaks:
        by_file[l["file"]] += 1

    # Render
    out = []
    out.append(f"# Policy Section-Sign (§) Leak Audit — {datetime.now().isoformat()}\n\n")
    out.append(f"Policy: `~/.claude/policies/no-policy-leak-section-sign.md`\n\n")
    out.append("## Summary\n\n")
    out.append(f"- **Leaks found** (unwanted §<num>): **{len(leaks)}**\n")
    out.append(f"- Legitimate uses (ISO/IEC/RFC/EU/Article + §\\ref): {total_legit}\n\n")

    if by_file:
        out.append("## Per-File Leak Counts\n\n")
        out.append("| File | Leak Count |\n|---|---:|\n")
        for f, c in sorted(by_file.items(), key=lambda x: -x[1]):
            out.append(f"| `{f}` | {c} |\n")
        out.append("\n")

    if leaks:
        out.append("## Top 100 Leaks (file:line — context)\n\n")
        out.append("| File:Line | Context |\n|---|---|\n")
        for l in leaks[:100]:
            ctx = l["context"].replace("|", "\\|")
            out.append(f"| `{l['file']}:{l['line']}` | `{ctx}` |\n")

    OUT_MD.write_text("".join(out))
    print(f"Report: {OUT_MD}")
    print(f"Leaks: {len(leaks)} | Legitimate uses: {total_legit}")
    if leaks:
        print(f"\nFiles with most leaks:")
        for f, c in sorted(by_file.items(), key=lambda x: -x[1])[:5]:
            print(f"  {f}: {c}")


if __name__ == "__main__":
    main()
