# Why pages are 70% empty --- Chapter 3 / 4 / 5 diagnostic

**Date:** 2026-05-30
**Build:** 1,981 pages (down from 2,214 baseline = -233pp, -10.5%)
**Status:** READ-ONLY diagnostic. Report only; no `.tex` files modified.

## Per-chapter sparse-page distribution (current state)

| Chapter | Total pages | Flagged sparse | % | Almost-empty (<= 5 lines) | Half-empty (< 50% content) |
|---|---:|---:|---:|---:|---:|
| Ch.1 | ~175 | 83 | 47% | 4 | 66 |
| Ch.2 | ~200 | 43 | 21% | 4 | 36 |
| **Ch.3** | ~625 | **243** | **39%** | **22** | **169** |
| **Ch.4** | ~350 | **170** | **49%** | **12** | **128** |
| **Ch.5** | ~250 | **156** | **62%** | **18** | **107** |
| Appendices | ~282 | 164 | 58% | 14 | 104 |
| **TOTAL** | 1,981 | **884** | **45%** | **78** | **623** |

**Worst by absolute count: Ch.3 (243 sparse pages).**
**Worst by percentage: Ch.5 (62% sparse).**

## Why are pages empty when there's no full-page table next?

There are FIVE common causes. Each requires a different fix.

### Cause 1: Section/subsection heading at page bottom (still ~30% of cases)

LaTeX won't put a section heading at the very bottom of a page (would be orphaned). The `\needspace{N\baselineskip}` directive checks if N baselines are free; if not, the heading moves to the next page, leaving N baselines empty at the bottom.

**Already mitigated in 7 waves of fixes** (24 → 16 → 12 baselines globally). Cannot go much lower without orphaning headings.

**Remaining instances**: when a section starts within 12 baselines of page bottom, it still triggers a break. Hard to eliminate further without breaking heading orphan protection.

### Cause 2: `\iffalse...\fi` suppressed content (audit: 321 blocks, 85,258 hidden words)

Many sections were once written with full body content, then suppressed via `\iffalse...\fi` leaving only the section heading + a 3-4 line summary intro. The summary is too short to fill the page, but the next `\subsection` or `\paragraph` brings a `\needspace` directive that forces a break.

**This is the biggest remaining cause for Ch.5 specifically.** Many discussion subsections were consolidated into the Distinction Pack (Appendix V) with thin summaries left in the chapter body.

**Possible fix (NOT executed per "no remove/move" rule):** consolidate adjacent thin subsections into one parent subsection. Removes the per-subsection `\needspace` trigger.

### Cause 3: Table caption rendered alone (orphan caption)

`\begin{xltabular}` reserves vertical space for the FULL table at the point of insertion. If insufficient space remains on the current page, the table moves to the next page BUT the `\caption{}` may render at the original location.

**Why this still happens despite `\needspace` lowering**: some tables genuinely don't fit in 12 remaining baselines + the placement algorithm splits caption from body.

**Possible fix:** wrap caption inside table body using `\caption*{...}` or force exact-here placement with the `H` float specifier. Risky to apply globally.

### Cause 4: Float `[!htbp]` placed at top of next page

Tables/figures using `[!htbp]` (here/top/bottom/page) may move to top of the next page, leaving the current page's bottom empty.

**This is structural typography**: rebalancing requires per-figure manual placement, not a global rule.

### Cause 5: `\clearpage` between thin content blocks (168 remain after Wave 6)

Remaining `\clearpage` directives are mostly structural — before `\subsection` major divisions in Ch.3 modular files. Each forces a page break. If the previous content ended on line 5 of 28 available, 23 baselines are lost.

**Already mitigated**: 104 `\clearpage` directives converted to `\par\bigskip` in Waves 3 + 6. Remaining 168 are structural.

## Per-chapter top sparse-page clusters

| Chapter | Worst 100-page range | Sparse count in range |
|---|---|---:|
| Ch.3 | 700-800 | ~40 |
| Ch.3 | 800-900 | ~38 |
| Ch.3 | 900-1000 | ~35 |
| Ch.4 | 1200-1300 | ~45 |
| Ch.4 | 1300-1400 | ~42 |
| Ch.5 | 1500-1600 | ~50 |
| Ch.5 | 1600-1700 | ~48 |

The Ch.5 1500-1700 range is the highest-density sparse cluster — likely because Ch.5 has many subsections that were heavily trimmed (content moved to Distinction Pack).

## What can still be safely fixed

| Action | Risk | Estimated impact |
|---|---|---|
| Lower `\needspace` further (12 -> 8) | **HIGH** -- many orphaned section headings | -20 to -40 pages |
| Convert remaining 168 `\clearpage` to soft separators | **MEDIUM** -- may break logical chapter divisions | -10 to -30 pages |
| Convert `[!htbp]` to `[H]` (force here) on tables | **MEDIUM** -- may cause overfull vbox warnings | -5 to -15 pages |
| Consolidate thin subsections under one parent | **MEDIUM** -- restructure, not pure formatting | -20 to -50 pages |
| Use `\flushbottom` instead of `\raggedbottom` | **LOW** but minimal impact (stretches gaps, doesn't eliminate them) | 0 |
| Accept current state | none | 0 |

## What CANNOT be safely fixed

- Chapter title pages (always centered with whitespace by design)
- Appendix title pages (same)
- Pages immediately following a multi-page table (the table ends mid-page; next paragraph starts fresh)
- `\iffalse...\fi` blocks (per "no remove content" rule)

## My recommendation

The dissertation is at a reasonable steady state:
- Started: 2,214 pages with 1,214 sparse (55% of pages)
- Now: 1,981 pages with 884 sparse (45% of pages)
- Reduction: -233 pages (-10.5%), sparse-page reduction -27%

Further compression has diminishing returns and carries layout risk. The remaining sparse pages are largely structural artefacts of the dissertation's modular design (small dedicated-page subsections in Ch.3, consolidated thin subsections in Ch.5 with content moved to Appendix V).

If you accept the current state, the dissertation is in its strongest published form. If you want to push further, the lowest-risk next move is consolidating thin Ch.5 subsections under their parent sections — but that's structural editing, not formatting, and requires your explicit go-ahead per the "no remove/move" rule.
