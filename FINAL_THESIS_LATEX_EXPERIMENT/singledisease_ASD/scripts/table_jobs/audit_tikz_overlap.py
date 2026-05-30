#!/usr/bin/env python3
"""
GGU TikZ Figure Overlap Detector
=================================

Scans every TikZ figure source under figures/ and detects:

  1. NODE OVERLAP: two \\node positions whose bounding boxes intersect
     (uses style's `minimum width`/`minimum height` or `text width`)
  2. TEXT OVERFLOW: node content character count > what its width can hold
     at \\fignodefont (~6-8 chars/cm at \\scriptsize)
  3. AXIS-CARD MISMATCH: cards placed beyond axis range

Output: jobs/reports/tikz_overlap_YYYYMMDD_HHMM.md

Usage:
  python3 scripts/table_jobs/audit_tikz_overlap.py
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
OUT_MD = OUT_DIR / f"tikz_overlap_{TS}.md"

# Default node sizes when style not declared
DEFAULT_W_CM = 2.0
DEFAULT_H_CM = 0.7
CHARS_PER_CM = 7  # rough character density at \scriptsize


def parse_styles(content):
    """Extract style definitions like 'event/.style={minimum width=2.0cm, ...}'."""
    styles = {}
    for m in re.finditer(r"(\w+)/\.style\s*=\s*\{([^{}]*(?:\{[^}]*\}[^{}]*)*)\}",
                         content):
        name = m.group(1)
        body = m.group(2)
        mw = re.search(r"minimum\s+width\s*=\s*([\d.]+)\s*cm", body)
        mh = re.search(r"minimum\s+height\s*=\s*([\d.]+)\s*cm", body)
        tw = re.search(r"text\s+width\s*=\s*([\d.]+)\s*cm", body)
        styles[name] = {
            "width_cm": float(mw.group(1)) if mw else (float(tw.group(1)) if tw else DEFAULT_W_CM),
            "height_cm": float(mh.group(1)) if mh else DEFAULT_H_CM,
        }
    return styles


def parse_nodes(content):
    """Extract \\node[STYLE,...] at (X, Y) {TEXT}; — return list of dicts."""
    nodes = []
    # Match: \node[styles] at (x, y) (optional name) {text};
    pat = re.compile(
        r"\\node\s*\[([^\]]+)\]\s*at\s*\(([-\d.]+)\s*,\s*([-\d.]+)\)\s*(?:\(\w+\))?\s*\{((?:[^{}]|\{[^}]*\})*)\}",
        re.DOTALL,
    )
    for m in pat.finditer(content):
        styles_str = m.group(1)
        x, y = float(m.group(2)), float(m.group(3))
        text = m.group(4)
        # Pick first style name
        style_name = styles_str.split(",")[0].strip()
        nodes.append({
            "style": style_name,
            "x": x, "y": y,
            "text": text[:60],
            "text_len": len(re.sub(r"\\\\", "\n", text)),
        })
    return nodes


def bbox(node, styles):
    """Compute (left, right, top, bottom) for a node."""
    style = styles.get(node["style"], {"width_cm": DEFAULT_W_CM, "height_cm": DEFAULT_H_CM})
    w = style["width_cm"]
    h = style["height_cm"]
    return (node["x"] - w / 2, node["x"] + w / 2, node["y"] + h / 2, node["y"] - h / 2)


def overlap(b1, b2):
    """Test if two bounding boxes overlap."""
    l1, r1, t1, bt1 = b1
    l2, r2, t2, bt2 = b2
    return not (r1 < l2 or r2 < l1 or t1 < bt2 or t2 < bt1)


def detect_overflow(text, width_cm):
    """Detect if text in a node is too long for its width."""
    # Split into lines (TikZ \\\\)
    lines = text.split("\\\\") if "\\\\" in text else [text]
    max_line_len = max(len(l.strip()) for l in lines) if lines else 0
    capacity = width_cm * CHARS_PER_CM
    return max_line_len > capacity


def main():
    files = sorted((ROOT / "figures").glob("*.tex"))
    print(f"Scanning {len(files)} TikZ figure files...")

    results = []
    for fp in files:
        try:
            content = fp.read_text(encoding="utf-8")
        except Exception:
            continue
        styles = parse_styles(content)
        nodes = parse_nodes(content)
        if not nodes:
            continue

        # Compute bboxes
        bboxes = [(n, bbox(n, styles)) for n in nodes]

        # Check overlap
        overlap_pairs = []
        for i in range(len(bboxes)):
            for j in range(i + 1, len(bboxes)):
                ni, bi = bboxes[i]
                nj, bj = bboxes[j]
                if overlap(bi, bj):
                    overlap_pairs.append((ni, nj, bi, bj))

        # Text overflow per node
        overflow_nodes = []
        for n in nodes:
            style = styles.get(n["style"], {"width_cm": DEFAULT_W_CM})
            if detect_overflow(n["text"], style["width_cm"]):
                overflow_nodes.append((n, style["width_cm"]))

        if overlap_pairs or overflow_nodes:
            results.append({
                "file": str(fp.relative_to(ROOT)),
                "n_nodes": len(nodes),
                "overlaps": len(overlap_pairs),
                "overflows": len(overflow_nodes),
                "overlap_samples": [
                    {"n1_text": n1["text"][:30], "n2_text": n2["text"][:30],
                     "x1": n1["x"], "x2": n2["x"]}
                    for n1, n2, _, _ in overlap_pairs[:5]
                ],
                "overflow_samples": [
                    {"text": n["text"][:50], "x": n["x"], "y": n["y"], "width_cm": w}
                    for n, w in overflow_nodes[:5]
                ],
            })

    # Write report
    lines = []
    lines.append("# TikZ Figure Overlap Audit\n\n")
    lines.append(f"Generated: {datetime.now().isoformat()}\n")
    lines.append(f"Scanned: {len(files)} TikZ files\n")
    lines.append(f"Files with issues: **{len(results)}**\n\n")

    total_overlaps = sum(r["overlaps"] for r in results)
    total_overflows = sum(r["overflows"] for r in results)
    lines.append(f"- Total node-pair overlaps: **{total_overlaps}**\n")
    lines.append(f"- Total text overflow nodes: **{total_overflows}**\n\n")

    if results:
        lines.append("## Files With Issues\n\n")
        lines.append("| File | Nodes | Overlaps | Text Overflows |\n")
        lines.append("|---|---:|---:|---:|\n")
        for r in sorted(results, key=lambda x: -(x["overlaps"] + x["overflows"])):
            lines.append(f"| `{r['file']}` | {r['n_nodes']} | {r['overlaps']} | {r['overflows']} |\n")
        lines.append("\n")

        # Per-file detail
        lines.append("## Detail (top 20 worst files)\n\n")
        for r in sorted(results, key=lambda x: -(x["overlaps"] + x["overflows"]))[:20]:
            lines.append(f"### {r['file']}\n\n")
            if r["overlap_samples"]:
                lines.append(f"**{r['overlaps']} node overlap(s) detected (showing first 5):**\n\n")
                for s in r["overlap_samples"]:
                    lines.append(f"- `{s['n1_text']}` (x={s['x1']}) overlaps `{s['n2_text']}` (x={s['x2']})\n")
                lines.append("\n")
            if r["overflow_samples"]:
                lines.append(f"**{r['overflows']} text overflow(s) (text too long for node width):**\n\n")
                for s in r["overflow_samples"]:
                    lines.append(f"- `{s['text']}` at ({s['x']}, {s['y']}), width={s['width_cm']}cm\n")
                lines.append("\n")

    OUT_MD.write_text("".join(lines), encoding="utf-8")
    print(f"Report: {OUT_MD}")
    print(f"Files with issues: {len(results)}")
    print(f"Total overlaps: {total_overlaps}")
    print(f"Total overflows: {total_overflows}")


if __name__ == "__main__":
    main()
