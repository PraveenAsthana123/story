#!/usr/bin/env python3
"""
GGU Advanced Table Quality FIXER v2 — handles L→p conversion
============================================================

v1 (fix_advanced_table_quality.py) could only narrow/widen columns that
were already explicit p{Xcm}. v2 ALSO converts L (auto-width) columns to
p{Xcm} so that:

  * Right-side-empty L columns get clamped to p{1.5cm}
  * Tall-column L columns get widened to p{N.NNcm} (most of textwidth)
  * All non-flagged L columns retain their auto-width behaviour

Strategy: equal-space allocation. Take total textwidth (~14.5cm with
\\tabcolsep), subtract all FIXED p{} widths, distribute remaining width
proportionally to the L columns based on each column's avg text length
(longer text → more width).

Modes:
  --dry-run   show what would change (default)
  --apply     write changes to disk + backup
  --only <substr>   filter files by substring

Usage:
  python3 scripts/table_jobs/fix_advanced_table_quality_v2.py
  python3 scripts/table_jobs/fix_advanced_table_quality_v2.py --apply
"""
import json
import re
import shutil
import sys
from pathlib import Path
from datetime import datetime

ROOT = Path(__file__).resolve().parents[2]
OUT_DIR = ROOT / "jobs" / "reports"
TS = datetime.now().strftime("%Y%m%d_%H%M")
LOG_PATH = OUT_DIR / f"fix_advanced_table_quality_v2_{TS}.md"

TEXTWIDTH_CM = 15.0
TABCOLSEP_PER_COL = 0.3   # 0.3cm padding per column edge (approx)
NARROW_FLOOR_CM = 1.5     # smallest column when narrowing right-empty
WIDE_CAP_CM = 9.5         # largest single column
MIN_L_CM = 1.5            # floor for any L→p conversion


def latest_audit_json():
    files = sorted(OUT_DIR.glob("advanced_table_quality_*.json"))
    if not files:
        sys.exit("No audit JSON. Run audit_advanced_table_quality.py first.")
    return files[-1]


def extract_brace_group(text, start):
    if start >= len(text) or text[start] != "{":
        return None, start
    depth, i = 1, start + 1
    while i < len(text) and depth > 0:
        if text[i] == "\\" and i + 1 < len(text):
            i += 2; continue
        if text[i] == "{": depth += 1
        elif text[i] == "}":
            depth -= 1
            if depth == 0:
                return text[start + 1:i], i + 1
        i += 1
    return None, i


# ============================================================================
# SPEC TOKEN PARSER
# ============================================================================
def parse_spec(spec):
    """Return ordered tokens: each is dict with 'kind' in (decorator, format, col)."""
    tokens = []
    i = 0
    while i < len(spec):
        c = spec[i]
        if c in " \t\n":
            i += 1; continue
        if c == "@":
            if i + 1 < len(spec) and spec[i + 1] == "{":
                _, j = extract_brace_group(spec, i + 1)
                tokens.append({"kind": "decorator", "raw": spec[i:j]})
                i = j; continue
        if c == ">":
            if i + 1 < len(spec) and spec[i + 1] == "{":
                _, j = extract_brace_group(spec, i + 1)
                tokens.append({"kind": "format", "raw": spec[i:j]})
                i = j; continue
        if c in "lcrLCRX":
            tokens.append({"kind": "col", "type": c, "raw": c, "width_cm": None})
            i += 1; continue
        if c == "p":
            br = spec.find("{", i)
            if br != -1:
                _, j = extract_brace_group(spec, br)
                width_str = spec[br + 1:j - 1].strip()
                wm = re.match(r"([\d.]+)cm", width_str)
                cm = float(wm.group(1)) if wm else None
                tokens.append({"kind": "col", "type": "p", "raw": spec[i:j], "width_cm": cm})
                i = j; continue
        i += 1
    return tokens


def col_tokens(tokens):
    return [t for t in tokens if t["kind"] == "col"]


def rebuild_spec(tokens):
    """Reassemble tokens preserving format-col adjacency (no space between them)."""
    out = []
    prev = None
    for t in tokens:
        if out:
            if prev == "col" and t["kind"] == "col":
                out.append(" ")
            elif prev == "col" and t["kind"] in ("decorator", "format"):
                out.append(" ")
            elif prev == "decorator" and t["kind"] in ("col", "decorator", "format"):
                out.append(" ")
        if t["kind"] == "col" and t["type"] == "p" and t.get("new_width_cm"):
            out.append(f"p{{{t['new_width_cm']:.1f}cm}}")
        elif t["kind"] == "col" and "new_type" in t:
            # L converted to p{Xcm}
            out.append(f"p{{{t['new_width_cm']:.1f}cm}}")
        else:
            out.append(t["raw"])
        prev = t["kind"]
    return "".join(out)


# ============================================================================
# THE FIX LOGIC (smart equal-space + L conversion)
# ============================================================================
def fix_table_colspec(spec, col_widths, col_avgs, col_maxes, issues, n_cols):
    """
    Return new colspec string OR None if no change.

    Strategy:
      1. Identify "heavy" col(s) (high avg text)
      2. Identify "empty" col(s) (low avg text, last position)
      3. Compute total available width: TEXTWIDTH - per-column padding
      4. Allocate widths: empty → MIN_L_CM, heavy → wider, rest → balanced
    """
    tokens = parse_spec(spec)
    cols = col_tokens(tokens)
    if len(cols) != n_cols:
        return None  # mismatch — abort

    # Compute total available width
    n = len(cols)
    available = TEXTWIDTH_CM - n * TABCOLSEP_PER_COL * 2  # 2 sides per col

    # Decide which cols need fixing
    fix_needed = (issues.get("right_side_empty") or issues.get("tall_column")
                  or issues.get("width_imbalanced"))
    if not fix_needed:
        return None

    # Identify column roles
    weights = list(col_avgs)  # use avg text as weight basis
    # Bump heavy cols (max > 100)
    for i, m in enumerate(col_maxes):
        if m > 100:
            weights[i] = max(weights[i] * 1.5, 50)

    # Cap empty trailing column to minimum
    new_widths = [None] * n
    if issues.get("right_side_empty") and weights[-1] < 10:
        new_widths[-1] = MIN_L_CM
        available -= MIN_L_CM
        weights[-1] = 0  # exclude from proportional allocation

    # Cap any column with avg < 5 chars to MIN
    for i, w in enumerate(weights):
        if w < 5 and new_widths[i] is None:
            new_widths[i] = MIN_L_CM
            available -= MIN_L_CM
            weights[i] = 0

    # Distribute remaining width proportionally to remaining columns by weight
    total_weight = sum(weights)
    if total_weight > 0 and available > 0:
        for i, w in enumerate(weights):
            if new_widths[i] is None and w > 0:
                share = (w / total_weight) * available
                new_widths[i] = max(MIN_L_CM, min(WIDE_CAP_CM, share))
    elif available > 0:
        # Equal share for all unassigned
        n_unassigned = sum(1 for w in new_widths if w is None)
        if n_unassigned > 0:
            equal_share = available / n_unassigned
            for i in range(n):
                if new_widths[i] is None:
                    new_widths[i] = max(MIN_L_CM, equal_share)

    # Annotate col tokens with new widths
    for i, col in enumerate(cols):
        if new_widths[i] is None:
            continue
        if col["type"] == "p":
            if abs((col["width_cm"] or 0) - new_widths[i]) < 0.05:
                continue
            col["new_width_cm"] = round(new_widths[i], 1)
        else:
            # L/X → convert to p{}
            col["new_type"] = "p"
            col["new_width_cm"] = round(new_widths[i], 1)

    # Check if any change happened
    if not any("new_width_cm" in c for c in cols):
        return None

    return rebuild_spec(tokens)


# ============================================================================
# FILE I/O — locate xltabular at line, replace brace-balanced colspec
# ============================================================================
def replace_colspec_in_file(file_text, line_no, new_colspec):
    lines = file_text.split("\n")
    if line_no - 1 >= len(lines):
        return None
    line = lines[line_no - 1]
    m = re.search(r"\\begin\{xltabular\}\s*", line)
    if not m:
        return None
    pos = m.end()
    if pos >= len(line) or line[pos] != "{":
        return None
    # Skip width arg
    _, j = extract_brace_group(line, pos)
    while j < len(line) and line[j] in " \t":
        j += 1
    if j >= len(line) or line[j] != "{":
        return None
    # Find colspec end
    _, k = extract_brace_group(line, j)
    new_line = line[:j] + "{" + new_colspec + "}" + line[k:]
    lines[line_no - 1] = new_line
    return "\n".join(lines)


# ============================================================================
# MAIN
# ============================================================================
def main():
    args = sys.argv[1:]
    dry_run = "--apply" not in args
    only_filter = None
    if "--only" in args:
        i = args.index("--only")
        if i + 1 < len(args):
            only_filter = args[i + 1]

    audit = json.loads(latest_audit_json().read_text())
    tables = audit["tables"]

    actionable = [t for t in tables if t["env_type"] == "xltabular" and (
        t["issues"]["right_side_empty"] or t["issues"]["tall_column"]
        or t["issues"]["width_imbalanced"])]

    if only_filter:
        actionable = [t for t in actionable if only_filter in t["file"]]

    print(f"Mode: {'DRY-RUN' if dry_run else 'APPLY'}")
    print(f"Actionable: {len(actionable)} / {len(tables)} tables")

    log = []
    log.append(f"# Advanced Table Fix v2 — {datetime.now().isoformat()}\n\n")
    log.append(f"Mode: **{'DRY-RUN' if dry_run else 'APPLY'}**\n\n")
    log.append("| File:Line | Label | Old colspec | New colspec | Issues |\n")
    log.append("|---|---|---|---|---|\n")

    by_file = {}
    for t in actionable:
        by_file.setdefault(t["file"], []).append(t)

    n_changed = 0
    for file, file_tables in by_file.items():
        fp = ROOT / file
        if not fp.exists():
            continue
        txt = fp.read_text(encoding="utf-8")
        changed_in_file = 0
        for t in sorted(file_tables, key=lambda x: -x["line"]):
            new_spec = fix_table_colspec(
                t["colspec"], t["col_widths_cm"],
                t["col_avg_text_len"], t["col_max_text_len"],
                t["issues"], t["n_cols"]
            )
            if not new_spec:
                continue
            new_txt = replace_colspec_in_file(txt, t["line"], new_spec)
            if not new_txt or new_txt == txt:
                continue
            txt = new_txt
            changed_in_file += 1
            issues_str = ", ".join(k for k, v in t["issues"].items() if isinstance(v, bool) and v)
            log.append(f"| `{file}:{t['line']}` | `{t['label']}` | `{t['colspec'][:40]}...` | `{new_spec[:60]}...` | {issues_str} |\n")
        if changed_in_file and not dry_run:
            bak = fp.with_suffix(fp.suffix + ".pre_advtable_v2")
            if not bak.exists():
                shutil.copy2(fp, bak)
            fp.write_text(txt, encoding="utf-8")
        if changed_in_file:
            print(f"  {file}: {changed_in_file} tables changed")
            n_changed += changed_in_file

    log.append(f"\n**Total tables changed: {n_changed}**\n")
    LOG_PATH.write_text("".join(log), encoding="utf-8")
    print(f"\nRun log: {LOG_PATH}")
    print(f"Total: {n_changed}")
    if dry_run:
        print("[DRY-RUN — pass --apply to commit]")
    return 0


if __name__ == "__main__":
    sys.exit(main())
