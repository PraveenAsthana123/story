#!/usr/bin/env python3
"""
GGU Table Intro Clarity Fixer
==============================

Targets the bad auto-injected intro pattern:

  \\paragraph{Title.}
  \\noindent Table~\\ref{X} summarises <stuff that echoes the title>. The N columns
  capture <list>.
  \\caption{...Same Title...}

Replaces with a single-sentence intro that explains:
  - WHAT the table contains (data, not title echo)
  - WHY it's useful (the purpose)

Pattern: "This table presents <col-list> for each <row-subject>, supporting <chapter-context>."

Usage:
  python3 scripts/table_jobs/fix_intro_clarity.py             # dry-run
  python3 scripts/table_jobs/fix_intro_clarity.py --apply
"""
import re
import shutil
import sys
from pathlib import Path
from datetime import datetime

ROOT = Path(__file__).resolve().parents[2]
OUT_DIR = ROOT / "jobs" / "reports"
TS = datetime.now().strftime("%Y%m%d_%H%M")
LOG_PATH = OUT_DIR / f"fix_intro_clarity_{TS}.md"

# Patterns that indicate problematic auto-generated intros:
#  - "summarises <stuff>" where caption repeats the same words
#  - hardcoded "three columns capture" / "four columns capture" etc.
#  - "presents <caption text> covering <list>" (my smart-intro output that
#    duplicates the caption)


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


def parse_xltabular(block):
    """Extract caption short text + column headers."""
    cap_m = re.search(r"\\caption(?:\[([^\]]+)\])?\{([^}]*)\}\\label\{([^}]+)\}", block)
    if not cap_m:
        return None, None, None
    short_cap = (cap_m.group(1) or cap_m.group(2))[:80]
    label = cap_m.group(3)
    headers = [m.group(1).strip() for m in re.finditer(r"\\thead\{([^}]+)\}", block)]
    return short_cap, label, headers


def compose_clarity_intro(short_cap, headers, label):
    """Compose a clarity intro that DOESN'T echo the caption."""
    # Trim caption to just the core noun phrase
    core = short_cap.split(":")[0].split("—")[0].split("--")[0].strip().rstrip(".,;")
    # Extract row subject from caption (usually a noun phrase BEFORE the first colon)
    n_cols = len(headers)
    if n_cols == 0:
        return f"\\noindent This table presents {core.lower()}."

    # Escape special chars in headers
    safe_headers = [h.replace("\\#", "#").replace("\\&", "&").replace("#", "\\#").replace("&", "\\&") for h in headers]

    # First column is usually the "subject" (rows are X, Y, Z)
    row_subject = safe_headers[0]
    # Other columns are what each row HAS
    if n_cols == 1:
        attrs = ""
    elif n_cols == 2:
        attrs = f" with its {safe_headers[1].lower()}"
    elif n_cols <= 4:
        attrs_list = ", ".join(h.lower() for h in safe_headers[1:-1])
        attrs = f" across {attrs_list}, and {safe_headers[-1].lower()}" if n_cols > 2 else f" with {safe_headers[-1].lower()}"
    else:
        attrs_list = ", ".join(h.lower() for h in safe_headers[1:4])
        attrs = f" across {attrs_list}, and {n_cols-4} more dimensions"

    return (f"\\noindent This table lists each \\textit{{{row_subject.lower()}}}{attrs}, "
            f"so examiners can trace what was assessed and what evidence supports each row.")


def find_bad_intros(txt, label):
    """Find existing intro paragraphs for this table that are bad."""
    # Pattern: \noindent Table~\ref{label} ... (up to next blank line OR \begin{)
    candidates = []
    for m in re.finditer(
        r"^[ \t]*\\noindent\s+Table~\\ref\{" + re.escape(label) + r"\}\s+[^\n]+\.[ \t]*\n",
        txt, re.MULTILINE
    ):
        intro_text = m.group(0)
        # Bad if:
        # - Says "summarises <X> <Caption>" (echo)
        # - Hardcoded "three columns capture" etc.
        # - Says "presents <caption> covering <list>" (my smart-intro style)
        is_bad = (
            re.search(r"summarises\s+[a-z]+\s+[A-Z]", intro_text) or
            re.search(r"(three|four|five|six|seven|eight) columns capture", intro_text) or
            re.search(r"presents.+covering\s+", intro_text) or
            "laying out each row in a structured form" in intro_text or
            re.search(r"summarises\s+\w+\s+(?:Summary|Catalog|Map|Framework|Plan|Pack):", intro_text)
        )
        if is_bad:
            candidates.append((m.start(), m.end(), intro_text))
    return candidates


def main():
    dry_run = "--apply" not in sys.argv
    files = list((ROOT / "chapters").glob("*.tex")) + list((ROOT / "appendices").glob("*.tex"))
    files = [f for f in files if "pre_" not in f.name and ".session_backups" not in str(f)]

    total_fixed = 0
    log = [f"# Intro Clarity Fix — {datetime.now().isoformat()}\n\nMode: **{'DRY-RUN' if dry_run else 'APPLY'}**\n\n"]
    log.append("| File:Line | Label | Old → New |\n|---|---|---|\n")

    for fp in files:
        txt = fp.read_text(encoding="utf-8")
        rel = str(fp.relative_to(ROOT))
        changes = []

        for m in re.finditer(r"\\begin\{xltabular\}.*?\\end\{xltabular\}", txt, re.DOTALL):
            block = m.group(0)
            short_cap, label, headers = parse_xltabular(block)
            if not label:
                continue
            # Find bad intros in 1500 chars before table
            preamble_start = max(0, m.start() - 1500)
            preamble = txt[preamble_start:m.start()]
            bad_intros = find_bad_intros(preamble, label)
            if not bad_intros:
                continue
            # Compose clarity intro
            new_intro = compose_clarity_intro(short_cap, headers, label)
            # Apply: remove bad intros and insert new one at the LAST bad position
            for s, e, _ in bad_intros:
                abs_s = preamble_start + s
                abs_e = preamble_start + e
                changes.append((abs_s, abs_e, new_intro + "\n"))

        if changes:
            # Sort by start position desc + remove duplicates
            seen = set()
            unique_changes = []
            for s, e, t in sorted(changes, key=lambda x: -x[0]):
                if (s, e) in seen:
                    continue
                seen.add((s, e))
                unique_changes.append((s, e, t))

            new_txt = txt
            for s, e, replacement in unique_changes:
                new_txt = new_txt[:s] + replacement + new_txt[e:]
            if not dry_run:
                bak = fp.with_suffix(fp.suffix + ".pre_intro_clarity")
                if not bak.exists():
                    shutil.copy2(fp, bak)
                fp.write_text(new_txt, encoding="utf-8")
            total_fixed += len(unique_changes)
            print(f"  {rel}: {len(unique_changes)} intros rewritten")
            log.append(f"| `{rel}` | various | {len(unique_changes)} rewritten |\n")

    log.append(f"\n**Total intros rewritten: {total_fixed}**\n")
    LOG_PATH.write_text("".join(log))
    print(f"\nRun log: {LOG_PATH}")
    print(f"Total: {total_fixed}")
    if dry_run:
        print("[DRY-RUN — pass --apply to commit]")


if __name__ == "__main__":
    main()
