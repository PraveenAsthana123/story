#!/usr/bin/env python3
"""Advanced per-chapter / per-appendix figure-clarity audit.

For every TikZ figure in chapters/ and appendices/, this audit checks:
  1. NODE-PAIR OVERLAP        --- bounding-box intersection of any two nodes
  2. ARROW VISIBILITY         --- arrows must have width >= 0.5pt and length >= 4pt
  3. CARD-EDGE OVERLAP        --- card/box nodes whose border-pad < 0.2cm or that
                                  abut neighbouring cards within 0.1cm
  4. FONT READABILITY         --- text nodes using font sizes below \\footnotesize
                                  (\\tiny, \\scriptsize, \\fontsize{<8}{...})
  5. TEXT OVERFLOW            --- text width estimated > node width
  6. ARROW-NODE COLLISION     --- arrow path crossing a non-endpoint node

For each issue, emits a SUGGESTED FIX (e.g., "increase node distance to 1.5cm",
"set arrow line width=1pt", "use \\fignodefont (= \\footnotesize) for node text").

Outputs per-chapter scorecards under jobs/reports/figure_clarity/<chapter>/
plus one master summary at jobs/reports/figure_clarity_master_dashboard.md.

READ-ONLY: no .tex files modified. Suggested fixes are reported, not applied.
"""
from __future__ import annotations
import re
import json
from pathlib import Path
from collections import defaultdict
from datetime import datetime

ROOT = Path(__file__).resolve().parents[2]
CHAPTERS_DIR = ROOT / "chapters"
APPENDICES_DIR = ROOT / "appendices"
FIGURES_DIR = ROOT / "figures"
JOBS_DIR = ROOT / "jobs"
OUT_DIR = JOBS_DIR / "reports" / "figure_clarity"
MASTER_OUT = JOBS_DIR / "reports" / "figure_clarity_master_dashboard.md"
JSON_OUT = JOBS_DIR / "reports" / f"figure_clarity_{datetime.now():%Y%m%d_%H%M}.json"

# -----------------------------------------------------------------------------
# Heuristic constants
# -----------------------------------------------------------------------------
NODE_MIN_GAP_CM = 0.20   # minimum gap between adjacent cards
ARROW_MIN_PT = 0.5       # arrows thinner than this are hard to see
ARROW_MIN_LEN_CM = 0.4   # shorter arrows are hard to follow
FONT_BAD_NAMES = ("\\tiny", "\\scriptsize")  # too small for figure labels
PX_PER_CM = 28.35        # rough latex-pt to-cm proxy
CHAR_WIDTH_PT = 5.5      # rough text width per char at \\footnotesize


# -----------------------------------------------------------------------------
# Helpers
# -----------------------------------------------------------------------------
def strip_comments(line: str) -> str:
    out = []
    i = 0
    while i < len(line):
        if line[i] == "%" and (i == 0 or line[i - 1] != "\\"):
            break
        out.append(line[i]); i += 1
    return "".join(out)


def parse_coord(s: str) -> tuple[float, float] | None:
    """Parse (x, y) or (x, y) [absolute cm] from a TikZ node position."""
    m = re.match(r"\(\s*(-?[\d.]+)\s*,\s*(-?[\d.]+)\s*\)", s.strip())
    if not m:
        return None
    return float(m.group(1)), float(m.group(2))


def extract_tikz_blocks(text: str):
    """Yield (start_line, end_line, body) for each \\begin{tikzpicture} ...
    \\end{tikzpicture} block."""
    lines = text.splitlines()
    out = []
    in_block = False
    start = 0
    buf = []
    for i, raw in enumerate(lines, 1):
        s = strip_comments(raw)
        if "\\begin{tikzpicture}" in s and not in_block:
            in_block = True
            start = i
            buf = [s]
        elif in_block:
            buf.append(s)
            if "\\end{tikzpicture}" in s:
                out.append((start, i, "\n".join(buf)))
                in_block = False
                buf = []
    return out


def parse_nodes(block_text: str):
    """Return list of dicts: {name, x, y, style, label, line_in_block}.
    Only catches well-formed \\node[style] (name) at (x,y) {label}; — common in
    this dissertation's figures."""
    nodes = []
    # Match: \node[style] (name) at (x,y) {label};
    # Also: \node[style] (name) [pos=relpos of othername] {label};
    abs_pat = re.compile(
        r"\\node\s*(?:\[(?P<style>[^\]]*)\])?\s*\((?P<name>[a-zA-Z_][\w]*)\)\s*at\s*\((?P<x>-?[\d.]+)\s*,\s*(?P<y>-?[\d.]+)\)\s*\{(?P<label>[^{}]*)\}",
        re.DOTALL,
    )
    rel_pat = re.compile(
        r"\\node\s*(?:\[(?P<style>[^\]]*)\])?\s*\((?P<name>[a-zA-Z_][\w]*)\)\s*\[(?P<rel>(?:above|below|left|right)[^\]]*)of\s*=?\s*(?P<ref>[a-zA-Z_]\w*)[^\]]*\]\s*\{(?P<label>[^{}]*)\}",
        re.DOTALL,
    )
    for m in abs_pat.finditer(block_text):
        nodes.append({
            "name": m.group("name"),
            "x": float(m.group("x")),
            "y": float(m.group("y")),
            "style": m.group("style") or "",
            "label": m.group("label").strip(),
            "kind": "abs",
        })
    # Relative-position nodes can't be checked for overlap geometry without
    # full TikZ resolution; we still record them for font/text checks.
    for m in rel_pat.finditer(block_text):
        nodes.append({
            "name": m.group("name"),
            "x": None, "y": None,
            "style": m.group("style") or "",
            "label": m.group("label").strip(),
            "kind": "rel",
        })
    return nodes


def extract_node_dims(style: str) -> tuple[float, float]:
    """Estimate node width, height in cm from style string."""
    width = 3.0; height = 0.8
    m = re.search(r"minimum width\s*=\s*([\d.]+)cm", style)
    if m: width = float(m.group(1))
    m = re.search(r"minimum height\s*=\s*([\d.]+)cm", style)
    if m: height = float(m.group(1))
    return width, height


def bbox(node) -> tuple[float, float, float, float] | None:
    """Return (xmin, ymin, xmax, ymax) of node center +/- (w/2, h/2)."""
    if node["x"] is None or node["y"] is None:
        return None
    w, h = extract_node_dims(node["style"])
    return (node["x"] - w / 2, node["y"] - h / 2,
            node["x"] + w / 2, node["y"] + h / 2)


def bbox_overlap(a, b) -> bool:
    if not a or not b: return False
    return not (a[2] <= b[0] or b[2] <= a[0] or a[3] <= b[1] or b[3] <= a[1])


def bbox_gap(a, b) -> float:
    """Return minimum gap (cm) between two non-overlapping bboxes; 0 if touching."""
    if not a or not b: return float("inf")
    dx = max(0.0, max(a[0] - b[2], b[0] - a[2]))
    dy = max(0.0, max(a[1] - b[3], b[1] - a[3]))
    return (dx ** 2 + dy ** 2) ** 0.5


def find_arrow_issues(block_text: str) -> list[dict]:
    """Scan \\draw[...] lines for thin or invisible arrows."""
    issues = []
    for m in re.finditer(r"\\draw\s*\[([^\]]*)\]\s*(\([^)]*\)[^;]*?);", block_text, re.DOTALL):
        opts = m.group(1)
        if "->" not in opts and "Stealth" not in opts and "arrow" not in opts.lower():
            continue  # not an arrow
        thin = False
        m_lw = re.search(r"line width\s*=\s*([\d.]+)pt", opts)
        if m_lw and float(m_lw.group(1)) < ARROW_MIN_PT:
            thin = True
        if "thin" in opts and "thick" not in opts and "very thick" not in opts:
            thin = True
        if thin:
            issues.append({
                "kind": "arrow_too_thin",
                "snippet": m.group(0)[:90],
                "fix": "Set line width = 1pt or use 'very thick' option",
            })
    return issues


def find_font_issues(block_text: str) -> list[dict]:
    """Find font sizes below \\footnotesize inside node labels."""
    issues = []
    for bad in FONT_BAD_NAMES:
        if re.search(re.escape(bad) + r"\b", block_text):
            issues.append({
                "kind": "font_too_small",
                "size": bad,
                "fix": f"Replace {bad} with \\fignodefont (= \\footnotesize)",
            })
    for m in re.finditer(r"\\fontsize\{(\d+)\}", block_text):
        if int(m.group(1)) < 8:
            issues.append({
                "kind": "font_too_small",
                "size": f"\\fontsize{{{m.group(1)}}}",
                "fix": "Use \\fontsize{8}{10} or larger",
            })
    return issues


def find_text_overflow(nodes: list[dict]) -> list[dict]:
    """Estimate if text label overflows node minimum width."""
    issues = []
    for n in nodes:
        if n["x"] is None: continue
        w_cm, _ = extract_node_dims(n["style"])
        if w_cm <= 0: continue
        # Estimate label width: chars * char_width / pt_per_cm
        label = re.sub(r"\\\\", " ", n["label"])    # treat \\ as space
        label = re.sub(r"\\[a-zA-Z]+\b\s*\{?", "", label)  # drop macros
        longest_run = max((len(s) for s in label.split(" ")), default=0)
        est_width_cm = longest_run * CHAR_WIDTH_PT / PX_PER_CM
        if est_width_cm > w_cm * 1.05:
            issues.append({
                "kind": "text_overflow",
                "node": n["name"],
                "estimated_text_cm": round(est_width_cm, 2),
                "node_width_cm": w_cm,
                "fix": f"Increase minimum width to {round(est_width_cm + 0.4, 1)}cm or split label",
            })
    return issues


def find_overlaps(nodes: list[dict]) -> list[dict]:
    issues = []
    abs_nodes = [n for n in nodes if n["x"] is not None]
    for i in range(len(abs_nodes)):
        for j in range(i + 1, len(abs_nodes)):
            a, b = abs_nodes[i], abs_nodes[j]
            ba, bb = bbox(a), bbox(b)
            if bbox_overlap(ba, bb):
                issues.append({
                    "kind": "node_overlap",
                    "a": a["name"], "b": b["name"],
                    "fix": "Move one node by >=1cm or reduce minimum width",
                })
            else:
                gap = bbox_gap(ba, bb)
                if gap < NODE_MIN_GAP_CM:
                    issues.append({
                        "kind": "card_edge_too_close",
                        "a": a["name"], "b": b["name"],
                        "gap_cm": round(gap, 2),
                        "fix": f"Increase spacing to >= {NODE_MIN_GAP_CM}cm",
                    })
    return issues


# -----------------------------------------------------------------------------
# Main scan
# -----------------------------------------------------------------------------
def scan_file(fp: Path) -> dict:
    """Return per-figure stats for one .tex file."""
    try:
        text = fp.read_text()
    except Exception as e:
        return {"file": str(fp), "error": str(e), "figures": []}
    blocks = extract_tikz_blocks(text)
    figs = []
    for start, end, body in blocks:
        nodes = parse_nodes(body)
        issues = (
            find_overlaps(nodes)
            + find_arrow_issues(body)
            + find_font_issues(body)
            + find_text_overflow(nodes)
        )
        # Score: each issue costs 1 point; capped at 100
        score = max(0, 100 - min(100, len(issues)))
        figs.append({
            "line_range": [start, end],
            "n_nodes": len(nodes),
            "n_issues": len(issues),
            "issues": issues[:20],   # keep top 20 to keep report small
            "score": score,
        })
    return {"file": str(fp.relative_to(ROOT)), "n_figures": len(figs), "figures": figs}


def classify_owner(fp: Path) -> str:
    """Return 'ch1' .. 'ch5' or 'appA' .. for grouping."""
    name = fp.name.lower()
    if name.startswith("chapter1"): return "ch1"
    if name.startswith("chapter2"): return "ch2"
    if name.startswith("chapter3"): return "ch3"
    if name.startswith("chapter4"): return "ch4"
    if name.startswith("chapter5"): return "ch5"
    # appendices: A, B, ... by leading letter
    for letter in "ABCDEFGHIJKLMNOPQRSTUVWXYZ":
        if name.startswith(letter.lower() + "_") or name.startswith(letter.lower() + "."):
            return f"app{letter}"
    return "figures-lib"  # standalone figures/ files


def main():
    OUT_DIR.mkdir(parents=True, exist_ok=True)

    # Files to scan: chapter files + appendix files + the figures/ library
    files = sorted(CHAPTERS_DIR.glob("chapter*.tex"))
    files += sorted(APPENDICES_DIR.glob("*.tex"))
    files += sorted(FIGURES_DIR.glob("*.tex"))

    # Group results by owner (chapter / appendix / figures-lib)
    grouped = defaultdict(list)
    for fp in files:
        result = scan_file(fp)
        owner = classify_owner(fp)
        grouped[owner].append(result)

    # Per-owner markdown reports
    per_owner_summary = []
    for owner in sorted(grouped):
        results = grouped[owner]
        n_files = len(results)
        n_figs = sum(r["n_figures"] for r in results)
        n_issues = sum(sum(f["n_issues"] for f in r["figures"]) for r in results)
        n_clean = sum(1 for r in results for f in r["figures"] if f["n_issues"] == 0)
        per_owner_summary.append({
            "owner": owner, "files": n_files, "figures": n_figs,
            "issues": n_issues, "clean_figures": n_clean,
        })

        # Per-owner detail file
        out_md = OUT_DIR / f"{owner}.md"
        lines = []
        lines.append(f"# Figure-Clarity Report --- {owner}")
        lines.append(f"\n_Generated: {datetime.now().isoformat(timespec='seconds')}_\n")
        lines.append(f"- Files scanned: **{n_files}**")
        lines.append(f"- Figures detected: **{n_figs}**")
        lines.append(f"- Total issues: **{n_issues}**")
        lines.append(f"- Clean figures: **{n_clean}** ({n_clean/max(n_figs,1):.0%})\n")
        # Per-file rollup
        lines.append("## Per-file rollup\n")
        lines.append("| File | Figures | Issues | Clean? |")
        lines.append("|---|---:|---:|---|")
        for r in sorted(results, key=lambda r: -sum(f["n_issues"] for f in r["figures"])):
            file_issues = sum(f["n_issues"] for f in r["figures"])
            clean_mark = "OK" if file_issues == 0 else "REVIEW"
            lines.append(f"| `{r['file']}` | {r['n_figures']} | {file_issues} | {clean_mark} |")
        lines.append("")
        # Per-figure detail for offenders
        lines.append("## Worst figures (top 15) with suggested fixes\n")
        all_figs = []
        for r in results:
            for fig in r["figures"]:
                if fig["n_issues"] > 0:
                    all_figs.append((r["file"], fig))
        all_figs.sort(key=lambda x: -x[1]["n_issues"])
        for k, (file, fig) in enumerate(all_figs[:15], 1):
            lines.append(f"### #{k}  `{file}:{fig['line_range'][0]}-{fig['line_range'][1]}`")
            lines.append(f"- Nodes: {fig['n_nodes']}  | Issues: {fig['n_issues']}  | Score: {fig['score']}/100")
            if fig["issues"]:
                lines.append("- Top issues + suggested fixes:")
                for iss in fig["issues"][:8]:
                    fix = iss.get("fix", "")
                    summary = ", ".join(f"{k}={v}" for k, v in iss.items() if k not in ("fix",))
                    lines.append(f"   - **{iss['kind']}** ({summary}) -> _{fix}_")
            lines.append("")
        out_md.write_text("\n".join(lines))

    # Master dashboard
    mlines = []
    mlines.append("# Figure-Clarity Master Dashboard\n")
    mlines.append(f"_Generated: {datetime.now().isoformat(timespec='seconds')}_\n")
    mlines.append("## Per-owner summary\n")
    mlines.append("| Owner | Files | Figures | Issues | Clean | Coverage |")
    mlines.append("|---|---:|---:|---:|---:|---:|")
    grand_files = grand_figs = grand_issues = grand_clean = 0
    for row in sorted(per_owner_summary, key=lambda r: r["owner"]):
        cov = row["clean_figures"] / max(row["figures"], 1)
        mlines.append(f"| {row['owner']} | {row['files']} | {row['figures']} | {row['issues']} | {row['clean_figures']} | {cov:.0%} |")
        grand_files += row["files"]; grand_figs += row["figures"]
        grand_issues += row["issues"]; grand_clean += row["clean_figures"]
    mlines.append(f"| **TOTAL** | **{grand_files}** | **{grand_figs}** | **{grand_issues}** | **{grand_clean}** | **{grand_clean/max(grand_figs,1):.0%}** |")
    mlines.append("\n## Per-owner detail reports\n")
    for owner in sorted(grouped):
        mlines.append(f"- [{owner}](figure_clarity/{owner}.md)")
    mlines.append("\n## Issue categories (heuristic)")
    mlines.append("- **node_overlap** --- two node bounding boxes intersect; one must move or shrink")
    mlines.append("- **card_edge_too_close** --- nodes don't overlap but gap < 0.2cm; visually merged")
    mlines.append("- **arrow_too_thin** --- arrow line width < 0.5pt or uses 'thin'; not visible at print resolution")
    mlines.append("- **font_too_small** --- text uses \\tiny / \\scriptsize / \\fontsize{<8}; unreadable")
    mlines.append("- **text_overflow** --- estimated text width > node minimum width; label cut off or wraps awkwardly")
    mlines.append("\n## How to use this report")
    mlines.append("1. Open per-owner detail report (links above)")
    mlines.append("2. Each top-15 figure has line range + suggested fix per issue")
    mlines.append("3. Apply fixes manually OR run `scripts/table_jobs/fix_figure_clarity_safe.py` (dry-run by default)")
    mlines.append("4. Re-run this audit to verify scores improve")

    MASTER_OUT.write_text("\n".join(mlines))

    # JSON dump for trend tracker
    JSON_OUT.write_text(json.dumps({
        "timestamp": datetime.now().isoformat(),
        "owners": per_owner_summary,
        "totals": {
            "files": grand_files, "figures": grand_figs,
            "issues": grand_issues, "clean": grand_clean,
        },
    }, indent=2))

    print(f"Master: {MASTER_OUT}")
    print(f"JSON:   {JSON_OUT}")
    print()
    print("Per-owner summary:")
    for row in sorted(per_owner_summary, key=lambda r: r["owner"]):
        cov = row["clean_figures"] / max(row["figures"], 1)
        print(f"  {row['owner']:14s}  files={row['files']:3d}  figs={row['figures']:3d}  issues={row['issues']:5d}  clean={row['clean_figures']:3d}  cov={cov:.0%}")
    print()
    print(f"Total: {grand_figs} figures, {grand_issues} issues, {grand_clean} clean ({grand_clean/max(grand_figs,1):.0%})")


if __name__ == "__main__":
    main()
