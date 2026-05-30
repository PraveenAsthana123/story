# Quality Issues --- Consolidated Per-Chapter Report

**Date:** 2026-05-30
**Status:** READ-ONLY audit. No `.tex` files modified, no content moved or removed.
**Build state:** main.pdf at 2,214 pages, 0 errors, 0 multiply-defined, 0 undefined citations, 0 overfull vbox.

This report consolidates findings from three new audits + the existing per-page-visual audit. All four are now installed on cron for twice-daily monitoring.

---

## TL;DR --- The four real quality issues across the dissertation

| # | Issue | Scope | Severity | Where to look |
|---|---|---|---|---|
| 1 | **Empty / sparse pages** (large blank bottom) | 1,214 of 2,214 pages flagged (55%) | HIGH | Per-page visual audit + page-break-causes audit |
| 2 | **Right-side overflow** (tables/figures not full width) | 28 critical + 35 warn = 63 pages | MEDIUM | Right-side-space audit |
| 3 | **Figure clarity** (node overlap, arrow visibility, text overflow) | 85 issues across 261 figures (83% clean) | MEDIUM | Figure-clarity per-chapter audit |
| 4 | **TikZ overlap** (existing audit) | 1,086 overlaps + 100 text overflows across 34 of 87 figure files | MEDIUM | TikZ overlap audit |

The user-referenced pages (156, 168, 245, 306, 401, 402, 427, 431, 481, 493, 502 of 2140) all fall under issues #1 or #2 above --- mostly **empty-bottom pages** caused by the chapter's heavy use of `\clearpage` and `\needspace{>=20\baselineskip}` directives.

---

## Root cause analysis

### Why so many sparse / empty-bottom pages?

I counted explicit page-break and white-space directives per chapter (after masking `\iffalse` suppressed content):

| Owner | `\clearpage` | `\newpage` | `\needspace{>=20}` | TOTAL |
|---|---:|---:|---:|---:|
| Ch.1 | 3 | 0 | 126 | 129 |
| Ch.2 | 3 | 0 | 76 | 79 |
| **Ch.3 (16 modular files)** | **231** | **0** | **374** | **605** |
| &nbsp;&nbsp;`chapter3_research_methods.tex` | 105 | 0 | 371 | 476 |
| &nbsp;&nbsp;`chapter3_pipeline_dedicated_pages.tex` | 32 | 0 | 0 | 32 |
| &nbsp;&nbsp;`chapter3_pipeline_extras.tex` | 25 | 0 | 0 | 25 |
| &nbsp;&nbsp;`chapter3_secondary_data_pages.tex` | 22 | 0 | 0 | 22 |
| Ch.4 | 3 | 0 | 243 | 246 |
| Ch.5 | 3 | 0 | 215 | 218 |
| **Grand total** | **272** | **0** | **1,224** | **1,539** |

**Why this matters:**
- Each `\clearpage` flushes pending floats AND forces a page break. If only 3 inches of content remain on the page when triggered, you lose 5+ inches at the bottom.
- Each `\needspace{20\baselineskip}` (~6 inches) checks if 6 inches are free at the current position; if not, it forces a break. Pages where only 4 inches were free lose those 4 inches.
- The section/subsection styling at [main.tex:540 + 545](FINAL_THESIS_LATEX_EXPERIMENT/singledisease_ASD/main.tex#L540) uses `\needspace{24\baselineskip}` (~7.2 inches) --- conservative, fires often.

`\raggedbottom` is already set (line 292) so the empty space appears naturally instead of being stretched, but the page-break directives are what cause the blank space in the first place.

### Why right-side overflow on 63 pages?

The right-side-space audit found pages where the right-most content ink stops more than 2 inches before the text-area right margin (523pt on A4). Likely causes per affected page:
- Table colspec uses fixed `p{Ncm}` columns that don't sum to `\textwidth`
- Figure rendered inside a narrower `minipage`
- Centred content with insufficient width

The earlier `\LTleft = 0.5in -> 0pt` fix (commit `c6050b2`) addressed table LEFT alignment but not all tables fully fill the textwidth (some have fixed `p{cm}` columns that sum to less).

### Why figure clarity issues?

The new per-chapter figure-clarity audit found 85 issues across 261 figures:

| Owner | Files | Figures | Issues | Clean | Coverage |
|---|---:|---:|---:|---:|---:|
| Ch.1 | 1 | 24 | 2 | 22 | **92%** |
| Ch.2 | 1 | 12 | 2 | 10 | 83% |
| Ch.3 | 16 | 43 | 11 | 35 | 81% |
| **Ch.4** | 1 | 23 | 16 | 18 | **78%** (worst) |
| Ch.5 | 1 | 27 | 4 | 23 | 85% |
| Appendices | ~20 | ~15 | ~14 | ~8 | varies |
| Figures library | 88 | 78 | 17 | 70 | 90% |
| **Total** | **130** | **261** | **85** | **216** | **83%** |

Ch.4 is the worst at 78% clean --- 16 issues across 23 figures. Worst-offending files (from existing TikZ overlap audit):
- `figures/fig_instrument_score_distributions.tex` --- 907 node overlaps + 3 text overflows
- `figures/mobile_app_wireframes.tex` --- 100 overlaps + 19 text overflows
- `figures/fig_band_power_cohort_bars.tex` --- 43 overlaps + 1 text overflow
- `figures/fig_headline_numbers_tile.tex` --- 10 overlaps + 18 text overflows

---

## What I built (read-only monitoring infrastructure)

### Three new audit scripts

| Script | Purpose | Output |
|---|---|---|
| [`audit_figure_clarity_per_chapter.py`](singledisease_ASD/scripts/table_jobs/audit_figure_clarity_per_chapter.py) | Per-chapter figure quality (node overlap, arrow visibility, card edge, font readability, text overflow) | `jobs/reports/figure_clarity_master_dashboard.md` + per-owner sub-reports |
| [`audit_page_break_causes.py`](singledisease_ASD/scripts/table_jobs/audit_page_break_causes.py) | Per-chapter inventory of `\clearpage` / `\newpage` / `\needspace>=N` / `\vspace>=1cm` / `\vfill` with line numbers + suggested fixes | `jobs/reports/page_break_causes_master.md` |
| [`audit_right_side_space.py`](singledisease_ASD/scripts/table_jobs/audit_right_side_space.py) | Per-page right-side gap measurement (A4-aware, masks page header/footer) | `jobs/reports/right_side_space_master.md` |

### Cron schedule (installed)

```
30 11 * * *   audit_figure_clarity_per_chapter.py
35 11 * * *   audit_page_break_causes.py
40 11 * * *   audit_right_side_space.py
30 23 * * *   audit_figure_clarity_per_chapter.py
35 23 * * *   audit_page_break_causes.py
40 23 * * *   audit_right_side_space.py
```

These run alongside the existing 12 audits on cron. Logs at `jobs/logs/quality_monitoring.log`.

---

## Recommended next actions (in priority order)

Each is a separate "fix" task that I will only execute on your explicit go-ahead per the standing "no remove/move at this stage" rule.

1. **Lower `\needspace{24\baselineskip}` -> `\needspace{16\baselineskip}` in main.tex section styling** (lines 540 + 545). One 2-line global edit. Estimated impact: reduces empty-bottom pages by ~30-40% by allowing section headings to land closer to the page bottom before forcing a break. RISK: ~10-20 section headings may orphan (sit alone at page bottom with body on next page). Mitigation: visually check before/after.

2. **Audit individual `\clearpage` in Ch.3 modular files** (32 in pipeline_dedicated_pages, 25 in pipeline_extras, 22 in secondary_data_pages, 105 in research_methods). Many are between adjacent narrow tables/figures and can become `\par\bigskip` (soft separation) without losing visual structure. RISK: tables may share a page; need to verify the reading flow isn't damaged.

3. **Convert remaining narrow-width tables to use X columns** (right-side gap fix). The audit identifies the 63 affected pages; per-page colspec edits would close the right-side gap. Mechanical work, low risk if done one-at-a-time.

4. **Per-figure clarity fixes for the top 4 worst offenders** (`fig_instrument_score_distributions`, `mobile_app_wireframes`, `fig_band_power_cohort_bars`, `fig_headline_numbers_tile`). These figures need TikZ node-spacing + font-size adjustments. Higher-effort but localized.

---

## Quick-glance grades

| Quality dimension | Current | Target |
|---|---|---|
| Build cleanliness (errors / overfull / multi-def) | 0 / 0 / 0 | 0 / 0 / 0 (maintain) |
| Empty-bottom pages | 55% of pages | < 25% |
| Right-side overflow | 63 pages | 0 critical |
| Figure clarity coverage | 83% | > 95% |
| Per-chapter Ch.4 figure clarity | 78% (worst) | > 95% |
| GGU template alignment (manual) | ~91% avg | 100% |
| Distinction Pack presence | Yes (Appendix V) | Maintained |
| Front-matter Executive Summary | Yes | Maintained |
| Per-chapter Three-Questions landing | Yes | Maintained |

---

## Files generated this turn

- Scripts: 3 new audits + 1 cron installer
- Reports: `jobs/reports/figure_clarity_master_dashboard.md`, `jobs/reports/page_break_causes_master.md`, `jobs/reports/right_side_space_master.md`
- This consolidated report: `QUALITY_ISSUES_CONSOLIDATED_REPORT_2026_05_30.md`

## What I have NOT touched
- Zero `.tex` files modified by this turn
- Zero content moved or removed
- Zero figures redrawn
- Zero pages rebalanced

All edits are pending your "fix" go-ahead per recommendation list above.
