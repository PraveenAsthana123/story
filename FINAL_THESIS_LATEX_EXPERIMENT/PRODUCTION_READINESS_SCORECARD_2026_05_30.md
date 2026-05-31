# Production-Readiness Scorecard

_Generated: 2026-05-30T23:58:55_

## Build State

| Metric | Value |
|---|---|
| Total pages | **1981** |
| PDF file size | 5556003 bytes |
| Errors | 0 |
| Multiply-defined labels | 0 |
| Undefined citations | 0 |
| Overfull \vbox | 7 |

## Quality Dimensions

| # | Dimension | Headline | Detail report |
|---|---|---|---|
| 1 | **Page density** | 240 of 1981 pages flagged (12.1%) -- ok=1713, sparse=122, almost_empty=99, figure_heavy=28, empty=19 | [per_page_index.md](per_page_index.md) |
| 2 | **Table width** | 0 narrow tables (all 75 prior narrows fixed via extracolsep) | -- |
| 3 | **Figure clarity** | 85/261 figure issues | [figure_clarity_master_dashboard.md](figure_clarity_master_dashboard.md) |
| 4 | **Right-side overflow** | critical=2, warn=1 | [right_side_space_master.md](right_side_space_master.md) |
| 5 | **Page-break causes** | 168 directives total (1981 pages) | [page_break_causes_master.md](page_break_causes_master.md) |
| 6 | **Repetition (aggressive)** | 115 duplicate occurrences | [repetition_aggressive_master.md](repetition_aggressive_master.md) |
| 7 | **Cross-chapter redundancy** | [see report] | [cross_chapter_redundancy_master.md](cross_chapter_redundancy_master.md) |

## Cumulative Improvement (since 2026-05-30 baseline)

| Metric | Baseline | Now | Delta |
|---|---:|---:|---:|
| Total pages | 2,214 | **1981** | -233 (-10.5%) |
| Sparse pages | 1,214 | **240** | -- |
| Narrow tables | 75 | **0** | -75 (100%) |
| Phantom headers (longtable) | many | **0** | all fixed |
| Build errors | -- | **0** | maintained |

## Monitoring Cron Schedule

All audits scheduled twice daily (11:xx + 23:xx):

```
30 11/23   audit_figure_clarity_per_chapter.py
35 11/23   audit_page_break_causes.py
40 11/23   audit_right_side_space.py
45 11/23   audit_repetition_aggressive.py
50 11/23   build_per_page_index.py
```

Plus the existing 12 audits (table quality, intro quality, bottom overflow, per-page visual, tikz overlap, jargon leaks, content redundancy, etc.) on the main cron schedule.

## How to query

```bash
# Pages with only orphan caption (table on page but few rows)
awk -F, '$7>0 && $8<3' jobs/reports/per_page_index.csv

# Pages with no content (truly empty)
awk -F, '$11=="empty"' jobs/reports/per_page_index.csv

# Pages with > 50 rows (long tables)
awk -F, '$8>50' jobs/reports/per_page_index.csv
```