#!/usr/bin/env python3
"""
GGU Smart Table Intro Generator
================================

For every xltabular block, ensures the visual hierarchy:

  [paragraph heading]
  [1-2 line auto-composed intro: "This table presents X, covering A, B, C."]
  [xltabular with caption]

Uses caption short-text + column headers to compose intro.
Skips tables that already have a non-stub intro paragraph (≥ 60 chars and
not the old "below presents ... laying out each row" boilerplate).

Usage:
  python3 scripts/table_jobs/fix_smart_table_intros.py             # dry-run
  python3 scripts/table_jobs/fix_smart_table_intros.py --apply
"""
import re
import shutil
import sys
from pathlib import Path
from datetime import datetime

ROOT = Path(__file__).resolve().parents[2]
OUT_DIR = ROOT / "jobs" / "reports"
OUT_DIR.mkdir(parents=True, exist_ok=True)
TS = datetime.now().strftime("%Y%m%d_%H%M")
LOG_PATH = OUT_DIR / f"fix_smart_table_intros_{TS}.md"


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


def parse_table(block):
    """Extract caption short text + thead column titles from a table block."""
    # Caption: \caption[short]{long}\label{X}
    cap_m = re.search(r"\\caption\[([^\]]+)\]\{[^}]*\}\\label\{([^}]+)\}", block)
    if not cap_m:
        cap_m = re.search(r"\\caption\{([^}]+)\}\\label\{([^}]+)\}", block)
        if not cap_m:
            return None, None, None
        short_cap, label = cap_m.group(1), cap_m.group(2)
    else:
        short_cap, label = cap_m.group(1), cap_m.group(2)

    # Extract \thead{...} entries
    headers = []
    for m in re.finditer(r"\\thead\{([^}]+)\}", block):
        h = m.group(1).strip()
        h = re.sub(r"\\#", "#", h)
        h = re.sub(r"\\&", "&", h)
        h = re.sub(r"\\\\", " / ", h)
        h = h.replace("$\\geq$", "≥").replace("$\\leq$", "≤")
        headers.append(h)

    return short_cap.strip(), label, headers


def compose_intro(short_cap, headers, ref_label):
    """Compose a sentence describing the table."""
    # Trim caption: strip trailing period
    cap = short_cap.rstrip(".")
    # Trim caption common suffixes like ", Methods, Examples, and Clinical Relevance"
    cap = re.sub(r"\s*[,:].*$", "", cap)

    if not headers:
        return f"\\noindent Table~\\ref{{{ref_label}}} presents {cap.lower()}."

    n = len(headers)
    if n <= 4:
        cols_str = ", ".join(headers[:-1]) + " and " + headers[-1] if n > 1 else headers[0]
    else:
        cols_str = ", ".join(headers[:3]) + f", and {n-3} more"

    return (f"\\noindent Table~\\ref{{{ref_label}}} presents {cap.lower()}, "
            f"covering {cols_str}.")


def find_existing_intro(txt, table_start):
    """Find if there's an existing intro paragraph within 5 non-empty lines before table_start.
    Returns the intro line's span if found and acceptable, else None."""
    # Look backwards from table_start for non-empty lines that mention \ref{<this table>}
    lookback = txt[max(0, table_start - 1500):table_start]
    lines = lookback.splitlines()
    # Check last 8 non-empty content lines
    content = [l for l in lines if l.strip() and not l.strip().startswith("%")]
    for line in content[-8:]:
        if "\\ref" in line and ("presents" in line.lower() or "shows" in line.lower() or "table" in line.lower()):
            if len(line.strip()) > 60 and "laying out each row in a structured form" not in line:
                return True  # good existing intro
    return False


def is_xltabular(block):
    return block.startswith("\\begin{xltabular}")


def main():
    dry_run = "--apply" not in sys.argv

    files = list((ROOT / "chapters").glob("*.tex")) + list((ROOT / "appendices").glob("*.tex"))
    files = [f for f in files if "pre_" not in f.name and ".session_backups" not in str(f)]

    total_added = 0
    total_skipped = 0
    log = [f"# Smart Table Intro Generation — {datetime.now().isoformat()}\n\n"]
    log.append(f"Mode: **{'DRY-RUN' if dry_run else 'APPLY'}**\n\n")
    log.append("| File:Line | Label | Action | Composed intro |\n|---|---|---|---|\n")

    for fp in files:
        txt = fp.read_text(encoding="utf-8")
        rel = str(fp.relative_to(ROOT))
        changes = []  # (insert_pos, new_text, label)

        for m in re.finditer(r"\\begin\{xltabular\}.*?\\end\{xltabular\}", txt, re.DOTALL):
            block = m.group(0)
            short_cap, label, headers = parse_table(block)
            if not label:
                continue

            # Find the start of the surrounding wrapper {\tablestripes\tablefontsize
            # or \needspace just before this table
            preamble_start = m.start()
            # Walk back past {\tablestripes... and \needspace... to find proper insert point
            lookback = txt[max(0, preamble_start - 200):preamble_start]
            wrap_pat = re.search(r"\{\\tablestripes\\tablefontsize\s*\n(\s*\\needspace\{[^}]+\}\s*\n)?\s*$",
                                lookback)
            if wrap_pat:
                # Insert BEFORE the wrapper
                insert_pos = preamble_start - (len(lookback) - wrap_pat.start())
            else:
                insert_pos = preamble_start

            # Skip if good existing intro
            if find_existing_intro(txt, insert_pos):
                total_skipped += 1
                continue

            intro = compose_intro(short_cap, headers, label)
            new_text = f"\n{intro}\n\n"
            changes.append((insert_pos, new_text, label, intro))

        # Apply changes in reverse order
        if changes:
            new_txt = txt
            for ins, txt_to_add, label, intro in reversed(changes):
                new_txt = new_txt[:ins] + txt_to_add + new_txt[ins:]
                line_no = txt[:ins].count("\n") + 1
                log.append(f"| `{rel}:{line_no}` | `{label}` | added | {intro[:80]} |\n")
            if not dry_run:
                bak = fp.with_suffix(fp.suffix + ".pre_smart_intro")
                if not bak.exists():
                    shutil.copy2(fp, bak)
                fp.write_text(new_txt, encoding="utf-8")
            total_added += len(changes)
            print(f"  {rel}: +{len(changes)} smart intros (skipped {total_skipped})")

    log.append(f"\n**Total added: {total_added}** | Skipped (already-good intros): {total_skipped}\n")
    LOG_PATH.write_text("".join(log), encoding="utf-8")
    print(f"\nRun log: {LOG_PATH}")
    print(f"Added: {total_added} | Skipped: {total_skipped}")
    if dry_run:
        print("[DRY-RUN — pass --apply to commit]")


if __name__ == "__main__":
    main()
