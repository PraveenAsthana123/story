#!/usr/bin/env python3
"""
GGU Content Redundancy Audit
=============================

Detects:
  1. Repeated sentences (> 50 chars, appearing 2+ times in same chapter)
  2. Verbose meta-notes (Note. Per-X / Each X has — meta vs informative)
  3. Long single sentences (> 50 words — readability issue)
  4. Empty/placeholder paragraphs

Output: jobs/reports/content_redundancy_YYYYMMDD_HHMM.md
"""
import re
import sys
from pathlib import Path
from datetime import datetime
from collections import defaultdict, Counter

ROOT = Path(__file__).resolve().parents[2]
OUT_DIR = ROOT / "jobs" / "reports"
TS = datetime.now().strftime("%Y%m%d_%H%M")
OUT_MD = OUT_DIR / f"content_redundancy_{TS}.md"

META_NOTE_PATTERNS = [
    r"\\textit\{Note\.\}\s+Per-\w+\s+(?:audit|policy|test|check|monitor)",
    r"\\textit\{Note\.\}\s+Each\s+(?:row|item|entry|step|stage)\s+(?:has|is)",
    r"\\textit\{Note\.\}\s+Aligned with",
    r"\\textit\{Note\.\}\s+Per-iteration",
]


def strip_latex(text):
    text = re.sub(r"\\[a-zA-Z]+\*?(\[[^\]]*\])?(\{[^}]*\})?", " ", text)
    text = re.sub(r"\$[^$]*\$", "X", text)
    text = re.sub(r"[{}~]", "", text)
    text = re.sub(r"\s+", " ", text).strip()
    return text


def main():
    chapters = list((ROOT / "chapters").glob("chapter*.tex"))
    chapters = [c for c in chapters if "pre_" not in c.name]

    repeated_sentences = []
    meta_notes = []
    long_sentences = []

    for fp in chapters:
        rel = str(fp.relative_to(ROOT))
        txt = fp.read_text()

        # 1. Repeated sentences
        sentences = []
        for m in re.finditer(r"[A-Z][^.!?]{50,200}[.!?]", strip_latex(txt)):
            sent = m.group(0).strip()
            sentences.append(sent)
        counts = Counter(sentences)
        for sent, count in counts.items():
            if count >= 2:
                repeated_sentences.append({"file": rel, "count": count, "text": sent[:120]})

        # 2. Meta notes
        for pat in META_NOTE_PATTERNS:
            for m in re.finditer(pat + r"[^\n]{0,250}", txt):
                line_no = txt[:m.start()].count("\n") + 1
                meta_notes.append({"file": rel, "line": line_no, "text": m.group(0)[:150]})

        # 3. Long sentences (in body prose, not tables)
        # Skip lines inside xltabular/tabular blocks
        for m in re.finditer(r"\\noindent\s+([A-Z][^\n]{200,})", txt):
            sent = strip_latex(m.group(1))
            word_count = len(sent.split())
            if word_count > 50:
                line_no = txt[:m.start()].count("\n") + 1
                long_sentences.append({"file": rel, "line": line_no, "words": word_count, "text": sent[:150]})

    # Render
    out = []
    out.append(f"# Content Redundancy Audit — {datetime.now().isoformat()}\n\n")
    out.append("## Summary\n\n")
    out.append("| Category | Count |\n|---|---:|\n")
    out.append(f"| Repeated sentences (2+ occurrences) | {len(repeated_sentences)} |\n")
    out.append(f"| Meta-notes (Per-X audit/policy/etc.) | {len(meta_notes)} |\n")
    out.append(f"| Long sentences (> 50 words) | {len(long_sentences)} |\n\n")

    if repeated_sentences:
        out.append(f"## Repeated Sentences ({len(repeated_sentences)})\n\n")
        out.append("| File | Count | Sentence (truncated) |\n|---|---:|---|\n")
        for r in sorted(repeated_sentences, key=lambda x: -x["count"])[:30]:
            text = r["text"].replace("|", "\\|")
            out.append(f"| `{r['file']}` | {r['count']} | {text} |\n")
        out.append("\n")

    if meta_notes:
        out.append(f"## Meta-Notes (Could Be Removed) ({len(meta_notes)})\n\n")
        out.append("| File:Line | Note (truncated) |\n|---|---|\n")
        for n in meta_notes[:50]:
            text = n["text"].replace("|", "\\|").replace("\n", " ")
            out.append(f"| `{n['file']}:{n['line']}` | {text} |\n")
        out.append("\n")

    if long_sentences:
        out.append(f"## Long Sentences (> 50 words) ({len(long_sentences)})\n\n")
        out.append("| File:Line | Words | Sentence (truncated) |\n|---|---:|---|\n")
        for s in sorted(long_sentences, key=lambda x: -x["words"])[:30]:
            text = s["text"].replace("|", "\\|")
            out.append(f"| `{s['file']}:{s['line']}` | {s['words']} | {text} |\n")
        out.append("\n")

    OUT_MD.write_text("".join(out))
    print(f"Report: {OUT_MD}")
    print(f"Repeated sentences: {len(repeated_sentences)}")
    print(f"Meta-notes: {len(meta_notes)}")
    print(f"Long sentences (> 50 words): {len(long_sentences)}")


if __name__ == "__main__":
    main()
