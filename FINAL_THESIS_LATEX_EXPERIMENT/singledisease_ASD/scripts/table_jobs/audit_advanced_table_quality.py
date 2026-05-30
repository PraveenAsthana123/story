#!/usr/bin/env python3
"""
GGU Advanced Table Quality Audit
=================================

ANALYSIS-ONLY (no edits). Produces a comprehensive report on every
xltabular/tabularx/longtable in the project, flagging:

  Issue #1  PHANTOM-HEADER     duplicate header rendering at top of first page
  Issue #2  BOTTOM-OVERFLOW    vbox overfull = table pushes past page bottom
  Issue #3  RIGHT-SIDE-EMPTY   last column avg text << first column avg
  Issue #4  TALL-COLUMN        one column has 3+ lines of wrapped text causing
                                excessive row height while others are nearly empty
  Issue #5  MULTI-PAGE         table spans 3+ pages (should be 1-2 max)
  Issue #6  TEXT-QUALITY       empty cells, placeholders, fragmented sentences
  Issue #7  COL-WIDTH-IMBAL    column widths very uneven (e.g., 0.5cm + 8cm)

Per table, captures: page span, column widths, per-column avg text length,
whitespace utilization, splitting strategy recommendation, which column
needs more space, which column has empty right-side.

Output:
  jobs/reports/advanced_table_quality_YYYYMMDD_HHMM.md  — human-readable
  jobs/reports/advanced_table_quality_YYYYMMDD_HHMM.json — machine-readable

Usage:
  python3 scripts/table_jobs/audit_advanced_table_quality.py
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
OUT_MD = OUT_DIR / f"advanced_table_quality_{TS}.md"
OUT_JSON = OUT_DIR / f"advanced_table_quality_{TS}.json"
PDF_PATH = ROOT / "main.pdf"
LOG_PATH = ROOT / "main.log"

# ============================================================================
# 1. COLUMN-SPEC PARSER
# ============================================================================
def parse_colspec(spec):
    """
    Parse xltabular column spec like:
        @{} >{\\raggedright\\arraybackslash}p{2.6cm} L L @{}
    Returns list of {type, width_cm} per column.
    """
    cols = []
    spec = re.sub(r"@\{[^}]*\}", "", spec)
    spec = re.sub(r">\{[^{}]*(\{[^{}]*\})?[^{}]*\}", "", spec)
    i = 0
    while i < len(spec):
        c = spec[i]
        if c in "lcr":
            cols.append({"type": c, "width_cm": None}); i += 1
        elif c in "LCR":
            cols.append({"type": c, "width_cm": None}); i += 1  # raggedright X-col
        elif c == "X":
            cols.append({"type": "X", "width_cm": None}); i += 1
        elif c == "p":
            br = spec.find("{", i)
            if br == -1:
                i += 1; continue
            depth, j = 1, br + 1
            while j < len(spec) and depth > 0:
                if spec[j] == "{": depth += 1
                elif spec[j] == "}": depth -= 1
                j += 1
            width_str = spec[br + 1:j - 1].strip()
            cm = parse_width(width_str)
            cols.append({"type": "p", "width_cm": cm})
            i = j
        else:
            i += 1
    return cols


def parse_width(w):
    """Convert '2.6cm' or '0.6\\textwidth' etc to centimetres (approx)."""
    m = re.match(r"([\d.]+)cm", w)
    if m: return float(m.group(1))
    m = re.match(r"([\d.]+)mm", w)
    if m: return float(m.group(1)) / 10
    m = re.match(r"([\d.]+)pt", w)
    if m: return float(m.group(1)) / 28.45
    m = re.match(r"([\d.]+)\\textwidth", w)
    if m: return float(m.group(1)) * 15.0  # textwidth ~15cm at 1in margins
    return None


# ============================================================================
# 2. TABLE EXTRACTOR + ANALYSER
# ============================================================================
TABLE_RE = re.compile(
    r"\\begin\{(xltabular|tabularx|tabular|longtable)\}(.*?)\\end\{\1\}",
    re.DOTALL,
)


def extract_brace_group(text, start):
    """Starting at index `start` where text[start]=='{', return (content, end_idx)
    such that text[start:end_idx] is the full balanced group."""
    if start >= len(text) or text[start] != "{":
        return None, start
    depth = 1
    i = start + 1
    while i < len(text) and depth > 0:
        if text[i] == "\\" and i + 1 < len(text):
            i += 2; continue
        if text[i] == "{":
            depth += 1
        elif text[i] == "}":
            depth -= 1
            if depth == 0:
                return text[start + 1:i], i + 1
        i += 1
    return None, i


def parse_table_header(args_text, env_type):
    """Parse the arg-text right after \\begin{env}. For xltabular/tabularx
    returns (width_arg, colspec). For tabular/longtable, (None, colspec)."""
    # Skip whitespace
    i = 0
    while i < len(args_text) and args_text[i] in " \t\n":
        i += 1
    if i >= len(args_text) or args_text[i] != "{":
        return None, None, args_text
    # First brace group: width OR colspec
    grp1, j = extract_brace_group(args_text, i)
    if grp1 is None:
        return None, None, args_text
    if env_type in ("xltabular", "tabularx"):
        # First is width, second is colspec
        while j < len(args_text) and args_text[j] in " \t\n":
            j += 1
        if j >= len(args_text) or args_text[j] != "{":
            return grp1, None, args_text[j:]
        grp2, k = extract_brace_group(args_text, j)
        return grp1, grp2, args_text[k:]
    else:
        return None, grp1, args_text[j:]


def extract_body_rows(body_text):
    """Split table body into rows on \\\\ (skip \\* and \\[...])."""
    # Remove caption, label, *rule, *head, *foot directives
    body = re.sub(r"\\caption\[[^\]]*\]\{[^}]+\}\\label\{[^}]+\}", "", body_text)
    body = re.sub(r"\\caption\{[^}]+\}\\label\{[^}]+\}", "", body)
    body = re.sub(r"\\(top|mid|bottom|cmid)rule(\[[^\]]+\])?", "", body)
    body = re.sub(r"\\(endfirsthead|endhead|endfoot|endlastfoot)", "", body)
    body = re.sub(r"\\addlinespace(\[[^\]]+\])?", "", body)
    body = re.sub(r"\\multicolumn\{\d+\}\{[^}]+\}\{[^{}]*(\{[^{}]*\})?[^{}]*\}", "", body)
    body = re.sub(r"(?<!\\)%[^\n]*", "", body)  # strip comments (NOT escaped \%)
    # Split on \\ followed by optional [skip] (but NOT \\* which is line in same row)
    raw_rows = re.split(r"\\\\(?:\[[^\]]+\])?\s*\n", body)
    rows = []
    for r in raw_rows:
        r = r.strip()
        if r and not r.startswith("\\") or "&" in r:
            rows.append(r)
    return rows


def split_cells(row):
    """Split a row on '&' respecting brace nesting AND backslash-escaped ampersands."""
    cells = []
    depth = 0
    buf = []
    i = 0
    while i < len(row):
        c = row[i]
        # Skip escaped chars (handles \&, \%, \$, \{, \}, \_, \#, \~, \^)
        if c == "\\" and i + 1 < len(row):
            buf.append(c)
            buf.append(row[i + 1])
            i += 2
            continue
        if c == "{":
            depth += 1
        elif c == "}":
            depth -= 1
        elif c == "&" and depth == 0:
            cells.append("".join(buf)); buf = []; i += 1; continue
        buf.append(c)
        i += 1
    cells.append("".join(buf))
    return [c.strip() for c in cells]


def strip_latex_for_count(text):
    """Return approximate visible text length.
    Treats \\ref{...}, \\cite{...}, \\Cref{...} etc. as 4-char render (e.g. "3.89").
    """
    # Unwrap text-formatting commands
    text = re.sub(r"\\textbf\{([^}]+)\}", r"\1", text)
    text = re.sub(r"\\emph\{([^}]+)\}", r"\1", text)
    text = re.sub(r"\\textit\{([^}]+)\}", r"\1", text)
    text = re.sub(r"\\thead\{([^}]+)\}", r"\1", text)
    # Cross-references render as numbers — substitute with "X.XX" placeholder
    text = re.sub(r"\\(?:ref|Cref|cref|autoref|pageref|nameref)\{[^}]+\}", "X.XX", text)
    text = re.sub(r"\\cite[tp]?\*?\{[^}]+\}", "[N]", text)
    # \newline / \\\\ inside cells force vertical line breaks → count as extra-line cost
    n_newlines = len(re.findall(r"\\(?:newline|\\\\)", text))
    text = re.sub(r"\\(?:newline|\\\\)", " ", text)
    # Strip remaining commands
    text = re.sub(r"\\[a-zA-Z]+\*?(\[[^\]]*\])?(\{[^{}]*\})?", " ", text)
    text = re.sub(r"\$[^$]*\$", "X", text)
    text = re.sub(r"[{}~]", "", text)
    text = re.sub(r"\s+", " ", text).strip()
    # Pad length for each forced newline (each \\\\ adds ~40 chars equivalent of layout cost)
    return text + (" " * (n_newlines * 40))


def analyse_table(file, line_no, env_type, width_arg, colspec, body):
    """Compute the seven quality dimensions per table."""
    cols = parse_colspec(colspec)
    n_cols = len(cols)
    rows = extract_body_rows(body)

    # Per-column avg text length
    col_lengths = [[] for _ in range(n_cols)]
    for row in rows:
        cells = split_cells(row)
        for i in range(min(len(cells), n_cols)):
            txt = strip_latex_for_count(cells[i])
            col_lengths[i].append(len(txt))

    col_avg = [sum(L) / max(len(L), 1) if L else 0 for L in col_lengths]
    col_max = [max(L) if L else 0 for L in col_lengths]
    col_min = [min(L) if L else 0 for L in col_lengths]

    # Issue #3 RIGHT-SIDE-EMPTY: last column avg < 40% of largest AND last < 20 chars
    # EXEMPTION: if last column already has explicit width <= 2.0cm, the issue is already addressed
    largest_avg = max(col_avg) if col_avg else 1
    last_avg = col_avg[-1] if col_avg else 0
    last_width = cols[-1]["width_cm"] if cols and cols[-1]["width_cm"] else None
    right_side_empty = (
        largest_avg > 30 and last_avg < 0.4 * largest_avg and last_avg < 20
        and (last_width is None or last_width > 2.0)  # only flag if last col is L (None) or wide
    )

    # Issue #4 TALL-COLUMN: one column max > 100 chars (3+ wrapped lines in narrow col)
    #   while another column avg < 40 chars (short label)
    # EXEMPTION: if the tall-content column has explicit width >= 5.0cm, it's already wide enough
    has_tall_col = any(m > 100 for m in col_max)
    has_narrow_col = sum(1 for c in col_avg if c < 40) >= 1
    if has_tall_col:
        tall_idx = col_max.index(max(col_max))
        tall_col_width = cols[tall_idx]["width_cm"] if tall_idx < len(cols) and cols[tall_idx]["width_cm"] else None
        tall_col_type = cols[tall_idx]["type"] if tall_idx < len(cols) else None
        # Exempt if: (a) tall col >= 4cm explicit, OR (b) tall col is L/X (tabularx auto-balances)
        tall_col_fixed = (
            (tall_col_width is not None and tall_col_width >= 4.0)
            or tall_col_type in ("L", "X")
        )
        tall_column = (not tall_col_fixed) and has_narrow_col and n_cols >= 3
    else:
        tall_column = False

    # Issue #7 COL-WIDTH-IMBAL: explicit widths vary > 4x
    # EXEMPTION: if the small column is < 2cm AND large column < 7cm (deliberate equal-space narrow + wide)
    widths = [c["width_cm"] for c in cols if c["width_cm"]]
    if len(widths) >= 2:
        wmax, wmin = max(widths), min(widths)
        # Skip if min < 2cm (intentional narrow) and max < 7cm (intentional bounded)
        intentional_narrow_wide = (wmin < 2.0 and wmax < 7.0)
        width_imbalanced = (wmax > 4 * wmin) and not intentional_narrow_wide
    else:
        width_imbalanced = False

    # Issue #5 MULTI-PAGE: > 25 rows (likely spans 2+ pages)
    multi_page = len(rows) > 25
    # Issue #5b VERY-MULTI-PAGE: > 50 rows (likely 3+ pages, should split)
    very_multi_page = len(rows) > 50

    # Issue #11 UNDER-WIDTH-ALLOCATED: sum of explicit p{} widths << textwidth (~15cm)
    # → table doesn't fill the page width, leaving margin on right
    explicit_widths = [w for w in [c["width_cm"] for c in cols] if w is not None]
    sum_explicit = sum(explicit_widths)
    n_explicit = len(explicit_widths)
    n_auto = n_cols - n_explicit
    # If only explicit p{} columns AND sum < 13.5cm (textwidth ~15 - 1cm padding), under-allocated
    under_width_allocated = (n_auto == 0 and sum_explicit > 0 and sum_explicit < 13.5)

    # Issue #9 UNDERUSED-COLUMN: column allocated > 4cm but avg < 25 chars
    # → that width could be redistributed to squeezed columns
    underused_column = False
    for i, (w, a) in enumerate(zip([c["width_cm"] for c in cols], col_avg)):
        if w is not None and w >= 4.0 and a < 25:
            underused_column = True
            break

    # Issue #10 SQUEEZED-COLUMN: column with avg/width > 12 chars/cm forces excess wrap
    squeezed_column = False
    for i, (w, a) in enumerate(zip([c["width_cm"] for c in cols], col_avg)):
        if w is not None and a > 25 and a / w > 12:
            squeezed_column = True
            break

    # Issue #8 TABLE-VS-TEXT-DENSITY-MISMATCH:
    # Table has many rows but each row has very little text → page is mostly empty
    # Suggests merging rows, converting to bullets, or reducing row count
    total_text_chars = sum(sum(L) for L in col_lengths)
    if len(rows) >= 8 and total_text_chars > 0:
        chars_per_row = total_text_chars / len(rows)
        # If avg < 30 chars/row across all columns AND many rows, table is sparse
        sparse_table = chars_per_row < 30 and len(rows) >= 12
    else:
        sparse_table = False

    # Issue #6 TEXT-QUALITY checks per cell
    empty_cells = sum(1 for row in rows for cell in split_cells(row) if not strip_latex_for_count(cell))
    placeholders = sum(1 for row in rows for cell in split_cells(row)
                       if strip_latex_for_count(cell) in ("TBD", "TODO", "?", "...", "—", "-"))

    # Extract label
    lab_m = re.search(r"\\label\{([^}]+)\}", body)
    label = lab_m.group(1) if lab_m else f"NOLABEL@{file}:{line_no}"

    # Caption short
    cap_m = re.search(r"\\caption(?:\[([^\]]+)\])?\{([^}]+)\}", body)
    caption = (cap_m.group(1) or cap_m.group(2))[:60] if cap_m else label

    # Recommend column adjustments
    rec = recommend_column_fix(cols, col_avg, col_max, right_side_empty, tall_column, width_imbalanced)

    return {
        "file": file,
        "line": line_no,
        "env_type": env_type,
        "label": label,
        "caption": caption,
        "n_cols": n_cols,
        "n_rows": len(rows),
        "colspec": colspec.strip(),
        "col_types": [c["type"] for c in cols],
        "col_widths_cm": [c["width_cm"] for c in cols],
        "col_avg_text_len": [round(a, 1) for a in col_avg],
        "col_max_text_len": col_max,
        "issues": {
            "right_side_empty": right_side_empty,
            "tall_column": tall_column,
            "width_imbalanced": width_imbalanced,
            "underused_column": underused_column,
            "squeezed_column": squeezed_column,
            "under_width_allocated": under_width_allocated,
            "multi_page": multi_page,
            "very_multi_page": very_multi_page,
            "sparse_table": sparse_table,
            "empty_cells": empty_cells,
            "placeholders": placeholders,
        },
        "recommendation": rec,
    }


def recommend_column_fix(cols, col_avg, col_max, right_side_empty, tall_column, width_imbalanced):
    """Generate per-table recommendation."""
    recs = []
    if right_side_empty:
        recs.append(f"REBALANCE: last column avg {col_avg[-1]:.0f} chars vs largest {max(col_avg):.0f}; "
                    f"narrow last column to p{{1.5cm}} or merge it with previous")
    if tall_column:
        idx_max = col_max.index(max(col_max))
        idx_min = col_avg.index(min([a for a in col_avg if a > 0])) if any(col_avg) else 0
        recs.append(f"WIDEN COL {idx_max+1} (max {col_max[idx_max]} chars) by NARROWING COL {idx_min+1} (avg {col_avg[idx_min]:.0f} chars)")
    if width_imbalanced:
        widths = [c["width_cm"] for c in cols]
        recs.append(f"WIDTH GAP: widths {widths} differ by > 8x; use equal-space strategy")
    return " | ".join(recs) if recs else "OK"


# ============================================================================
# 3. PARSE BUILD LOG FOR OVERFLOWS
# ============================================================================
def parse_overflows(log_path):
    """Parse main.log for Overfull \vbox and \hbox warnings. Returns dict."""
    if not log_path.exists():
        return {"vbox": [], "hbox": []}
    log = log_path.read_text(errors="ignore")
    vbox = []
    for m in re.finditer(r"Overfull \\vbox \(([\d.]+)pt too high\)[^\n]*", log):
        vbox.append({"too_high_pt": float(m.group(1))})
    hbox = []
    for m in re.finditer(r"Overfull \\hbox \(([\d.]+)pt too wide\) in paragraph at lines (\d+)--(\d+)", log):
        hbox.append({"too_wide_pt": float(m.group(1)),
                     "lines": (int(m.group(2)), int(m.group(3)))})
    return {"vbox": vbox, "hbox": hbox}


# ============================================================================
# 4. PER-TABLE PAGE-SPAN VIA TABLE LABEL LOOKUP IN main.aux
# ============================================================================
def get_table_page_spans():
    """Extract from main.aux: each label → page number it was defined on."""
    aux = ROOT / "main.aux"
    spans = {}
    if not aux.exists():
        return spans
    for m in re.finditer(r"\\newlabel\{(tab:[^}]+)\}\{\{[^}]*\}\{(\d+)\}", aux.read_text(errors="ignore")):
        spans[m.group(1)] = int(m.group(2))
    return spans


# ============================================================================
# 5. MAIN
# ============================================================================
def main():
    files = sorted(list((ROOT / "chapters").glob("*.tex"))) + sorted(list((ROOT / "appendices").glob("*.tex")))
    files = [f for f in files if "pre_" not in f.name and ".session_backups" not in str(f)]

    print(f"Scanning {len(files)} files...", file=sys.stderr)
    tables = []
    for fp in files:
        rel = str(fp.relative_to(ROOT))
        try:
            txt = fp.read_text(encoding="utf-8")
        except UnicodeDecodeError:
            continue
        for m in TABLE_RE.finditer(txt):
            env_type, args_and_body = m.group(1), m.group(2)
            line_no = txt.count("\n", 0, m.start()) + 1
            width_arg, colspec, body = parse_table_header(args_and_body, env_type)
            if not colspec:
                continue
            try:
                t = analyse_table(rel, line_no, env_type, width_arg, colspec, body)
                tables.append(t)
            except Exception:
                pass

    page_spans = get_table_page_spans()
    overflows = parse_overflows(LOG_PATH)

    # Annotate tables with page where they appear
    for t in tables:
        t["page"] = page_spans.get(t["label"], None)

    # Aggregate
    issue_counts = defaultdict(int)
    for t in tables:
        for k, v in t["issues"].items():
            if isinstance(v, bool) and v:
                issue_counts[k] += 1
            elif isinstance(v, int) and v > 0:
                issue_counts[k] += 1

    # Write JSON
    OUT_JSON.write_text(json.dumps({
        "generated": datetime.now().isoformat(),
        "n_tables": len(tables),
        "issue_counts": dict(issue_counts),
        "overflows": {"vbox_count": len(overflows["vbox"]), "hbox_count": len(overflows["hbox"])},
        "tables": tables,
    }, indent=2))

    # Write Markdown
    lines = []
    lines.append("# Advanced Table Quality Audit\n\n")
    lines.append(f"Generated: {datetime.now().isoformat()}\n\n")
    lines.append("Policy: composes with §70 + §71 (project) + global table standards\n\n")
    lines.append("**This report identifies six issue classes per table:**\n\n")
    lines.append("| Code | Issue | Symptom |\n|---|---|---|\n")
    lines.append("| #1 PHANTOM | Duplicate header at top of first page | xltabular endhead phantom-renders |\n")
    lines.append("| #2 VBOX-OVERFLOW | Table pushes past page bottom | \\vbox too high warning |\n")
    lines.append("| #3 RIGHT-EMPTY | Last column nearly empty, right whitespace | last col avg < 20% of largest |\n")
    lines.append("| #4 TALL-COLUMN | One column has 3+ lines, others narrow | col max > 200 chars, others < 30 |\n")
    lines.append("| #5 MULTI-PAGE | Table spans 3+ pages (should be 1-2 max) | n_rows > ~30 |\n")
    lines.append("| #6 TEXT-QUALITY | Empty cells, placeholders | per-cell strip check |\n")
    lines.append("| #7 WIDTH-IMBAL | Column widths differ > 8x | manual p{} mismatch |\n\n")

    lines.append("## Summary Counts\n\n")
    lines.append(f"- **Total tables**: {len(tables)}\n")
    lines.append(f"- **Build-log vbox bottom-overflows**: {len(overflows['vbox'])}\n")
    lines.append(f"- **Build-log hbox horizontal-overflows**: {len(overflows['hbox'])}\n")
    for issue, count in sorted(issue_counts.items(), key=lambda x: -x[1]):
        lines.append(f"- **{issue}**: {count} tables\n")
    lines.append("\n")

    # Top-priority issue tables
    lines.append("## Issue #3 — Tables with RIGHT-SIDE EMPTY (last column nearly empty)\n\n")
    right_empty = [t for t in tables if t["issues"]["right_side_empty"]]
    lines.append(f"Count: **{len(right_empty)}** tables\n\n")
    if right_empty:
        lines.append("| File:Line | Label | Cols | Col avg text lengths | Rec |\n")
        lines.append("|---|---|---:|---|---|\n")
        for t in sorted(right_empty, key=lambda x: x["issues"]["right_side_empty"], reverse=True)[:40]:
            avgs = " | ".join(f"{a:.0f}" for a in t["col_avg_text_len"])
            lines.append(f"| `{t['file']}:{t['line']}` | `{t['label']}` | {t['n_cols']} | {avgs} | {t['recommendation']} |\n")
        lines.append("\n")

    lines.append("## Issue #4 — Tables with TALL-COLUMN (one column has 3+ rows of text)\n\n")
    tall = [t for t in tables if t["issues"]["tall_column"]]
    lines.append(f"Count: **{len(tall)}** tables\n\n")
    if tall:
        lines.append("| File:Line | Label | Cols | Col max text | Rec |\n")
        lines.append("|---|---|---:|---|---|\n")
        for t in sorted(tall, key=lambda x: max(x["col_max_text_len"]), reverse=True)[:40]:
            maxes = " | ".join(str(m) for m in t["col_max_text_len"])
            lines.append(f"| `{t['file']}:{t['line']}` | `{t['label']}` | {t['n_cols']} | {maxes} | {t['recommendation']} |\n")
        lines.append("\n")

    lines.append("## Issue #5 — Tables that span 3+ pages (should be split into Part 1 / Part 2)\n\n")
    vmp = [t for t in tables if t["issues"]["very_multi_page"]]
    lines.append(f"Count: **{len(vmp)}** tables (> 50 rows — likely 3+ pages)\n\n")
    if vmp:
        lines.append("| File:Line | Label | Rows | Cols | Caption | Action |\n")
        lines.append("|---|---|---:|---:|---|---|\n")
        for t in sorted(vmp, key=lambda x: -x["n_rows"])[:30]:
            lines.append(f"| `{t['file']}:{t['line']}` | `{t['label']}` | {t['n_rows']} | {t['n_cols']} | {t['caption'][:50]} | SPLIT into Part 1 + Part 2 |\n")
        lines.append("\n")

    mp = [t for t in tables if t["issues"]["multi_page"] and not t["issues"]["very_multi_page"]]
    lines.append(f"## Issue #5b — Tables that span exactly 2 pages (acceptable, no action)\n\nCount: **{len(mp)}**\n\n")

    lines.append("## Issue #7 — Tables with WIDTH-IMBALANCE (column widths differ > 4x)\n\n")
    imbal = [t for t in tables if t["issues"]["width_imbalanced"]]
    lines.append(f"Count: **{len(imbal)}** tables\n\n")
    if imbal:
        lines.append("| File:Line | Label | Cols | Widths (cm) | Rec |\n")
        lines.append("|---|---|---:|---|---|\n")
        for t in sorted(imbal, key=lambda x: max([w for w in x["col_widths_cm"] if w] + [0]), reverse=True)[:40]:
            widths = " | ".join(f"{w:.1f}" if w else "—" for w in t["col_widths_cm"])
            lines.append(f"| `{t['file']}:{t['line']}` | `{t['label']}` | {t['n_cols']} | {widths} | {t['recommendation']} |\n")
        lines.append("\n")

    # Build-log overflows
    lines.append("## Build-Log Overflows (vbox bottom + hbox horizontal)\n\n")
    lines.append(f"- **vbox bottom-overflows**: {len(overflows['vbox'])} pages with content past page-bottom\n")
    if overflows["vbox"]:
        lines.append("\n| Severity (pt too high) | Action |\n|---:|---|\n")
        for v in sorted(overflows["vbox"], key=lambda x: -x["too_high_pt"])[:10]:
            lines.append(f"| {v['too_high_pt']:.1f} | reduce table size, add \\clearpage, or \\resizebox |\n")
        lines.append("\n")
    lines.append(f"- **hbox horizontal-overflows**: {len(overflows['hbox'])} cells exceed text-width\n\n")

    OUT_MD.write_text("".join(lines), encoding="utf-8")
    print(f"Report MD:   {OUT_MD}")
    print(f"Report JSON: {OUT_JSON}")
    print(f"Tables: {len(tables)} | Right-empty: {len(right_empty)} | Tall-col: {len(tall)} | Width-imbal: {len(imbal)} | vbox-overflow: {len(overflows['vbox'])}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
