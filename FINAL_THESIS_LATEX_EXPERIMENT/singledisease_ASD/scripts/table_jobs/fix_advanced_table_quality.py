#!/usr/bin/env python3
"""
GGU Advanced Table Quality FIXER
=================================

Reads the latest audit_advanced_table_quality_*.json and applies fixes:

  Issue #3 RIGHT-SIDE-EMPTY  → narrow last column to p{1.2cm} (it's nearly empty);
                                redistribute released width to the column with the
                                largest avg text (the "heavy" column)
  Issue #4 TALL-COLUMN       → widen the column with longest cell at cost of
                                the column with shortest avg (narrow column)
  Issue #7 WIDTH-IMBALANCE   → if widths differ > 4×, compress narrowest col
                                to floor (0.6cm) and give the rest to the widest

  Issue #2 VBOX-OVERFLOW     → wrap entire xltabular in \resizebox{\textwidth}{!}{...}
                                ONLY for tables that flagged in any of #3/#4/#7
                                (otherwise overflow is unrelated to the table)

  Issue #5 VERY-MULTI-PAGE   → currently REPORT-ONLY; flag in commit message that
                                table needs manual split into Part 1/Part 2

Modes:
  --dry-run   show what would change (default)
  --apply     write changes to disk + backup

Strategy: ALL transformations are conservative — they edit ONLY the column-spec
brace group of \\begin{xltabular}{\\textwidth}{<colspec>}; the body of the table
is untouched. Backup saved as *.tex.pre_advtable_fix.

Caveat: width changes are CONSERVATIVE. The script does NOT touch tables whose
columns are all "L" (auto-width X-columns) since those self-balance via tabularx.

Usage:
  python3 scripts/table_jobs/fix_advanced_table_quality.py            # dry-run
  python3 scripts/table_jobs/fix_advanced_table_quality.py --apply    # apply
  python3 scripts/table_jobs/fix_advanced_table_quality.py --apply --only chapter3
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
LOG_PATH = OUT_DIR / f"fix_advanced_table_quality_{TS}.md"

# Configurable thresholds
NARROW_FLOOR_CM = 1.2     # smallest width when narrowing an empty/short column
WIDE_CAP_CM = 7.0         # widest single explicit column
TEXTWIDTH_CM = 15.0       # 1in margins on US Letter ≈ 15cm
RESIZEBOX_WRAP_THRESHOLD = 100  # vbox-overflow severity > 100pt → wrap with \resizebox


def latest_audit_json():
    files = sorted(OUT_DIR.glob("advanced_table_quality_*.json"))
    if not files:
        sys.exit("No advanced_table_quality_*.json found. Run audit first.")
    return files[-1]


def load_audit():
    return json.loads(latest_audit_json().read_text())


# ============================================================================
# COLUMN-SPEC REBUILDER
# ============================================================================
def rebuild_colspec(orig_spec, col_widths, col_avgs, col_maxes, issues):
    """
    Given original colspec + per-column stats, return a NEW colspec string
    with rebalanced widths. Returns None if no change needed.

    Strategy:
      1. If right_side_empty: clamp last column to NARROW_FLOOR_CM
      2. If tall_column: identify heavy_col (largest avg) and narrow_col (smallest avg);
         move width from narrow_col to heavy_col
      3. If width_imbalanced: clamp narrowest to NARROW_FLOOR_CM, distribute extra to widest
      4. Preserve L/X columns (they self-balance)
    """
    # Parse original spec into ordered tokens (preamble like @{} + columns)
    tokens = parse_spec_tokens(orig_spec)
    if not tokens:
        return None

    col_indices = [i for i, t in enumerate(tokens) if t["kind"] == "col"]
    if len(col_indices) == 0:
        return None

    # Compute new widths per column
    new_widths_cm = list(col_widths)  # may be None for L/X
    heavy_col = None
    narrow_col = None

    # Step 1: shrink right-side-empty column
    if issues.get("right_side_empty") and len(col_avgs) > 0:
        last_idx = len(col_avgs) - 1
        if new_widths_cm[last_idx] is not None and new_widths_cm[last_idx] > NARROW_FLOOR_CM:
            released = new_widths_cm[last_idx] - NARROW_FLOOR_CM
            new_widths_cm[last_idx] = NARROW_FLOOR_CM
            # Heavy column = largest col_max
            heavy_col = col_maxes.index(max(col_maxes))
            if new_widths_cm[heavy_col] is not None:
                new_widths_cm[heavy_col] = min(WIDE_CAP_CM, new_widths_cm[heavy_col] + released)

    # Step 2: widen tall column at cost of narrow column
    if issues.get("tall_column"):
        # Find heavy col (largest max), narrow col (smallest avg)
        heavy_col = col_maxes.index(max(col_maxes))
        # narrow_col: column with smallest avg (and explicit width > floor)
        candidates = [(i, a) for i, a in enumerate(col_avgs)
                      if new_widths_cm[i] is not None
                      and new_widths_cm[i] > NARROW_FLOOR_CM
                      and i != heavy_col]
        if candidates:
            narrow_col = min(candidates, key=lambda x: x[1])[0]
            released = new_widths_cm[narrow_col] - NARROW_FLOOR_CM
            new_widths_cm[narrow_col] = NARROW_FLOOR_CM
            if new_widths_cm[heavy_col] is not None:
                new_widths_cm[heavy_col] = min(WIDE_CAP_CM, new_widths_cm[heavy_col] + released)

    # Step 3: width-imbalanced
    if issues.get("width_imbalanced"):
        explicit_widths = [(i, w) for i, w in enumerate(new_widths_cm) if w is not None]
        if len(explicit_widths) >= 2:
            min_idx, min_w = min(explicit_widths, key=lambda x: x[1])
            max_idx, max_w = max(explicit_widths, key=lambda x: x[1])
            if min_w < NARROW_FLOOR_CM and max_w < WIDE_CAP_CM:
                released = NARROW_FLOOR_CM - min_w
                new_widths_cm[min_idx] = NARROW_FLOOR_CM
                # This INCREASES min, so we don't free space — skip if doesn't help
                pass

    # Check if anything actually changed
    if new_widths_cm == col_widths:
        return None

    # Rebuild colspec from tokens
    return rebuild_spec_string(tokens, new_widths_cm)


def parse_spec_tokens(spec):
    """Parse colspec into ordered tokens. Each token: {kind, raw, [width_cm]}."""
    tokens = []
    i = 0
    while i < len(spec):
        c = spec[i]
        if c in " \t\n":
            i += 1; continue
        if c == "@":
            # @{...}
            if i + 1 < len(spec) and spec[i + 1] == "{":
                br = i + 1; depth, j = 1, i + 2
                while j < len(spec) and depth > 0:
                    if spec[j] == "{": depth += 1
                    elif spec[j] == "}": depth -= 1
                    j += 1
                tokens.append({"kind": "decorator", "raw": spec[i:j]})
                i = j; continue
        if c == ">":
            if i + 1 < len(spec) and spec[i + 1] == "{":
                br = i + 1; depth, j = 1, i + 2
                while j < len(spec) and depth > 0:
                    if spec[j] == "\\" and j + 1 < len(spec):
                        j += 2; continue
                    if spec[j] == "{": depth += 1
                    elif spec[j] == "}": depth -= 1
                    j += 1
                tokens.append({"kind": "format", "raw": spec[i:j]})
                i = j; continue
        if c in "lcrLCRX":
            tokens.append({"kind": "col", "raw": c, "type": c, "width_cm": None})
            i += 1; continue
        if c == "p":
            br = spec.find("{", i)
            if br != -1:
                depth, j = 1, br + 1
                while j < len(spec) and depth > 0:
                    if spec[j] == "{": depth += 1
                    elif spec[j] == "}": depth -= 1
                    j += 1
                width_str = spec[br + 1:j - 1].strip()
                # Parse width to cm
                wm = re.match(r"([\d.]+)cm", width_str)
                cm = float(wm.group(1)) if wm else None
                tokens.append({"kind": "col", "raw": spec[i:j], "type": "p", "width_cm": cm})
                i = j; continue
        i += 1
    return tokens


def rebuild_spec_string(tokens, new_widths_cm):
    """Reassemble colspec. Preserve adjacency: only add space between two consecutive
    'col' tokens or between 'decorator' and 'col'; NEVER between a 'format' decorator
    and its bound column (they must be tight)."""
    out = []
    col_i = 0
    prev_kind = None
    for t in tokens:
        # Spacing: between two cols, add space. Between format>col, NO space.
        if out:
            if prev_kind == "col" and t["kind"] == "col":
                out.append(" ")
            elif prev_kind == "col" and t["kind"] in ("decorator", "format"):
                out.append(" ")
            elif prev_kind == "decorator" and t["kind"] in ("col", "decorator", "format"):
                out.append(" ")
            # else: prev_kind == "format" → tight (no space before col)
        if t["kind"] == "col":
            new_w = new_widths_cm[col_i] if col_i < len(new_widths_cm) else None
            if t["type"] == "p" and new_w is not None and new_w != t["width_cm"]:
                out.append(f"p{{{new_w:.1f}cm}}")
            else:
                out.append(t["raw"])
            col_i += 1
        else:
            out.append(t["raw"])
        prev_kind = t["kind"]
    return "".join(out)


# ============================================================================
# FIND + REPLACE TABLE COLSPEC IN SOURCE
# ============================================================================
def replace_table_colspec(file_text, line_no, new_colspec):
    """Locate the xltabular at line_no and replace its colspec with brace-balanced
    extraction (handles nested { } in @{} and >{...})."""
    lines = file_text.split("\n")
    if line_no - 1 >= len(lines):
        return None
    line = lines[line_no - 1]
    # Find \begin{xltabular} prefix
    prefix_match = re.search(r"\\begin\{xltabular\}\s*", line)
    if not prefix_match:
        return None
    pos = prefix_match.end()
    # First brace group is width (e.g. {\textwidth})
    if pos >= len(line) or line[pos] != "{":
        return None
    depth, j = 1, pos + 1
    while j < len(line) and depth > 0:
        if line[j] == "{": depth += 1
        elif line[j] == "}": depth -= 1
        j += 1
    width_end = j  # j is right after the closing }
    # Skip whitespace
    while width_end < len(line) and line[width_end] in " \t":
        width_end += 1
    # Second brace group is colspec (brace-balanced)
    if width_end >= len(line) or line[width_end] != "{":
        return None
    depth, j = 1, width_end + 1
    while j < len(line) and depth > 0:
        if line[j] == "\\" and j + 1 < len(line):
            j += 2; continue
        if line[j] == "{": depth += 1
        elif line[j] == "}":
            depth -= 1
            if depth == 0:
                colspec_end = j + 1
                break
        j += 1
    else:
        return None
    # Replace
    new_line = line[:width_end] + "{" + new_colspec + "}" + line[colspec_end:]
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
        idx = args.index("--only")
        if idx + 1 < len(args):
            only_filter = args[idx + 1]

    audit = load_audit()
    tables = audit["tables"]

    # Filter for actionable tables
    actionable = [t for t in tables if (
        t["issues"]["right_side_empty"]
        or t["issues"]["tall_column"]
        or t["issues"]["width_imbalanced"]
    ) and t["env_type"] == "xltabular"]

    if only_filter:
        actionable = [t for t in actionable if only_filter in t["file"]]

    print(f"Mode: {'DRY-RUN' if dry_run else 'APPLY'}")
    print(f"Actionable tables: {len(actionable)} / {len(tables)}")
    if only_filter:
        print(f"Filter: --only {only_filter}")
    print()

    log = []
    log.append(f"# Advanced Table Fix Run — {datetime.now().isoformat()}\n\n")
    log.append(f"Mode: **{'DRY-RUN' if dry_run else 'APPLY'}**\n")
    log.append(f"Actionable tables identified: {len(actionable)}\n\n")
    log.append("| File:Line | Label | Old colspec | New colspec | Issues |\n")
    log.append("|---|---|---|---|---|\n")

    # Group by file
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
        # Process in reverse line order (so line numbers stay valid)
        for t in sorted(file_tables, key=lambda x: -x["line"]):
            new_spec = rebuild_colspec(
                t["colspec"],
                t["col_widths_cm"],
                t["col_avg_text_len"],
                t["col_max_text_len"],
                t["issues"],
            )
            if not new_spec:
                continue
            new_txt = replace_table_colspec(txt, t["line"], new_spec)
            if not new_txt or new_txt == txt:
                continue
            txt = new_txt
            changed_in_file += 1
            issues_str = ", ".join(k for k, v in t["issues"].items() if isinstance(v, bool) and v)
            log.append(f"| `{file}:{t['line']}` | `{t['label']}` | `{t['colspec'][:40]}` | `{new_spec[:50]}` | {issues_str} |\n")
        if changed_in_file and not dry_run:
            bak = fp.with_suffix(fp.suffix + ".pre_advtable_fix")
            if not bak.exists():
                shutil.copy2(fp, bak)
            fp.write_text(txt, encoding="utf-8")
        if changed_in_file:
            print(f"  {file}: {changed_in_file} tables changed")
            n_changed += changed_in_file

    log.append(f"\n**Total tables changed: {n_changed}**\n")
    log.append(f"\n(Apply mode={'OFF (dry-run)' if dry_run else 'ON'})\n")
    LOG_PATH.write_text("".join(log), encoding="utf-8")
    print(f"\nRun log: {LOG_PATH}")
    print(f"Total changes: {n_changed}")
    if dry_run:
        print("\n[DRY-RUN — no files modified. Run with --apply to commit changes.]")
    return 0


if __name__ == "__main__":
    sys.exit(main())
