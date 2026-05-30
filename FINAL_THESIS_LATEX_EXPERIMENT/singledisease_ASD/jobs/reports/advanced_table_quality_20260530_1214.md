# Advanced Table Quality Audit

Generated: 2026-05-30T12:14:51.222558

Policy: composes with §70 + §71 (project) + global table standards

**This report identifies six issue classes per table:**

| Code | Issue | Symptom |
|---|---|---|
| #1 PHANTOM | Duplicate header at top of first page | xltabular endhead phantom-renders |
| #2 VBOX-OVERFLOW | Table pushes past page bottom | \vbox too high warning |
| #3 RIGHT-EMPTY | Last column nearly empty, right whitespace | last col avg < 20% of largest |
| #4 TALL-COLUMN | One column has 3+ lines, others narrow | col max > 200 chars, others < 30 |
| #5 MULTI-PAGE | Table spans 3+ pages (should be 1-2 max) | n_rows > ~30 |
| #6 TEXT-QUALITY | Empty cells, placeholders | per-cell strip check |
| #7 WIDTH-IMBAL | Column widths differ > 8x | manual p{} mismatch |

## Summary Counts

- **Total tables**: 1158
- **Build-log vbox bottom-overflows**: 7
- **Build-log hbox horizontal-overflows**: 1280
- **squeezed_column**: 205 tables
- **empty_cells**: 83 tables
- **width_imbalanced**: 79 tables
- **right_side_empty**: 62 tables
- **underused_column**: 60 tables
- **under_width_allocated**: 17 tables
- **multi_page**: 14 tables
- **tall_column**: 12 tables
- **sparse_table**: 4 tables
- **very_multi_page**: 3 tables
- **placeholders**: 1 tables

## Issue #3 — Tables with RIGHT-SIDE EMPTY (last column nearly empty)

Count: **62** tables

| File:Line | Label | Cols | Col avg text lengths | Rec |
|---|---|---:|---|---|
| `chapters/chapter1_introduction.tex:558` | `tab:ch1_object_scope` | 3 | 2 | 46 | 11 | REBALANCE: last column avg 11 chars vs largest 46; narrow last column to p{1.5cm} or merge it with previous | WIDTH GAP: widths [1.0, 8.9, 4.4] differ by > 8x; use equal-space strategy |
| `chapters/chapter1_introduction.tex:616` | `tab:ch1_task_map` | 4 | 2 | 40 | 1 | 10 | REBALANCE: last column avg 10 chars vs largest 40; narrow last column to p{1.5cm} or merge it with previous | WIDTH GAP: widths [1.0, 8.1, 1.0, 4.1] differ by > 8x; use equal-space strategy |
| `chapters/chapter1_introduction.tex:1496` | `tab:problem_funnel_evidence` | 4 | 17 | 43 | 6 | 12 | REBALANCE: last column avg 12 chars vs largest 43; narrow last column to p{1.5cm} or merge it with previous |
| `chapters/chapter1_introduction.tex:2139` | `NOLABEL@chapters/chapter1_introduction.tex:2139` | 4 | 1 | 14 | 87 | 12 | REBALANCE: last column avg 12 chars vs largest 87; narrow last column to p{1.5cm} or merge it with previous |
| `chapters/chapter1_introduction.tex:2259` | `tab:problem_decomposition` | 5 | 2 | 3 | 18 | 54 | 10 | REBALANCE: last column avg 10 chars vs largest 54; narrow last column to p{1.5cm} or merge it with previous |
| `chapters/chapter1_introduction.tex:2669` | `tab:b2c_mobile_screens` | 4 | 2 | 14 | 119 | 12 | REBALANCE: last column avg 12 chars vs largest 119; narrow last column to p{1.5cm} or merge it with previous | WIDTH GAP: widths [1.0, 2.7, 7.9, 2.5] differ by > 8x; use equal-space strategy |
| `chapters/chapter1_introduction.tex:2733` | `tab:b2c_user_forms` | 4 | 2 | 16 | 94 | 10 | REBALANCE: last column avg 10 chars vs largest 93; narrow last column to p{1.5cm} or merge it with previous | WIDTH GAP: widths [1.0, 3.1, 7.6, 2.5] differ by > 8x; use equal-space strategy |
| `chapters/chapter1_introduction.tex:2920` | `tab:report_types` | 4 | 2 | 15 | 88 | 9 | REBALANCE: last column avg 9 chars vs largest 88; narrow last column to p{1.5cm} or merge it with previous | WIDTH GAP: widths [1.0, 3.1, 7.6, 2.4] differ by > 8x; use equal-space strategy |
| `chapters/chapter1_introduction.tex:3070` | `tab:continuous_monitoring` | 4 | 2 | 14 | 105 | 10 | REBALANCE: last column avg 9 chars vs largest 105; narrow last column to p{1.5cm} or merge it with previous | WIDTH GAP: widths [1.0, 2.9, 7.9, 2.4] differ by > 8x; use equal-space strategy |
| `chapters/chapter1_introduction.tex:3333` | `tab:backend_db` | 4 | 2 | 1 | 99 | 10 | REBALANCE: last column avg 10 chars vs largest 99; narrow last column to p{1.5cm} or merge it with previous | WIDTH GAP: widths [1.0, 1.0, 9.2, 2.9] differ by > 8x; use equal-space strategy |
| `chapters/chapter1_introduction.tex:5137` | `tab:ch1_scorecard` | 3 | 16 | 31 | 5 | REBALANCE: last column avg 5 chars vs largest 31; narrow last column to p{1.5cm} or merge it with previous |
| `chapters/chapter2_literature.tex:1331` | `NOLABEL@chapters/chapter2_literature.tex:1331` | 4 | 22 | 35 | 21 | 5 | REBALANCE: last column avg 5 chars vs largest 35; narrow last column to p{1.5cm} or merge it with previous |
| `chapters/chapter2_literature.tex:2598` | `tab:ch2_scorecard` | 3 | 17 | 32 | 6 | REBALANCE: last column avg 6 chars vs largest 32; narrow last column to p{1.5cm} or merge it with previous |
| `chapters/chapter3_arch_executive_summary.tex:18` | `tab:arch_exec_summary` | 3 | 23 | 96 | 11 | REBALANCE: last column avg 11 chars vs largest 96; narrow last column to p{1.5cm} or merge it with previous |
| `chapters/chapter3_defence_prep_checklist.tex:19` | `tab:defence_prep_arch_checklist` | 4 | 2 | 49 | 1 | 15 | REBALANCE: last column avg 15 chars vs largest 49; narrow last column to p{1.5cm} or merge it with previous | WIDTH GAP: widths [1.0, 7.8, 1.0, 4.3] differ by > 8x; use equal-space strategy |
| `chapters/chapter3_research_methods.tex:92` | `NOLABEL@chapters/chapter3_research_methods.tex:92` | 2 | 43 | 13 | REBALANCE: last column avg 13 chars vs largest 43; narrow last column to p{1.5cm} or merge it with previous |
| `chapters/chapter3_research_methods.tex:985` | `tab:combined_methodology_flow` | 5 | 9 | 43 | 38 | 22 | 17 | REBALANCE: last column avg 17 chars vs largest 43; narrow last column to p{1.5cm} or merge it with previous |
| `chapters/chapter3_research_methods.tex:1463` | `tab:primary_data_outcome_map` | 3 | 6 | 50 | 7 | REBALANCE: last column avg 7 chars vs largest 50; narrow last column to p{1.5cm} or merge it with previous |
| `chapters/chapter3_research_methods.tex:2542` | `tab:primary_analysis_sensitivity_bias` | 4 | 24 | 46 | 34 | 18 | REBALANCE: last column avg 18 chars vs largest 46; narrow last column to p{1.5cm} or merge it with previous |
| `chapters/chapter3_research_methods.tex:3568` | `tab:customer_smart_flow` | 4 | 1 | 23 | 46 | 17 | REBALANCE: last column avg 17 chars vs largest 46; narrow last column to p{1.5cm} or merge it with previous |
| `chapters/chapter3_research_methods.tex:8544` | `NOLABEL@chapters/chapter3_research_methods.tex:8544` | 5 | 12 | 48 | 11 | 5 | 14 | REBALANCE: last column avg 14 chars vs largest 48; narrow last column to p{1.5cm} or merge it with previous |
| `chapters/chapter3_research_methods.tex:10881` | `NOLABEL@chapters/chapter3_research_methods.tex:10881` | 4 | 18 | 48 | 28 | 10 | REBALANCE: last column avg 10 chars vs largest 48; narrow last column to p{1.5cm} or merge it with previous |
| `chapters/chapter3_research_methods.tex:11472` | `NOLABEL@chapters/chapter3_research_methods.tex:11472` | 3 | 11 | 125 | 13 | REBALANCE: last column avg 13 chars vs largest 125; narrow last column to p{1.5cm} or merge it with previous |
| `chapters/chapter3_research_methods.tex:11495` | `NOLABEL@chapters/chapter3_research_methods.tex:11495` | 3 | 2 | 84 | 9 | REBALANCE: last column avg 9 chars vs largest 84; narrow last column to p{1.5cm} or merge it with previous |
| `chapters/chapter3_research_methods.tex:11531` | `NOLABEL@chapters/chapter3_research_methods.tex:11531` | 4 | 4 | 54 | 10 | 7 | REBALANCE: last column avg 7 chars vs largest 54; narrow last column to p{1.5cm} or merge it with previous |
| `chapters/chapter3_research_methods.tex:11552` | `NOLABEL@chapters/chapter3_research_methods.tex:11552` | 4 | 11 | 32 | 5 | 7 | REBALANCE: last column avg 7 chars vs largest 32; narrow last column to p{1.5cm} or merge it with previous |
| `chapters/chapter3_research_methods.tex:12955` | `tab:ch3_decision_summary` | 3 | 38 | 176 | 16 | REBALANCE: last column avg 16 chars vs largest 175; narrow last column to p{1.5cm} or merge it with previous |
| `chapters/chapter4_analysis_findings.tex:495` | `tab:ch4_triangulation` | 4 | 14 | 15 | 96 | 16 | REBALANCE: last column avg 16 chars vs largest 96; narrow last column to p{1.5cm} or merge it with previous |
| `chapters/chapter4_analysis_findings.tex:914` | `tab:ch4_alignment` | 4 | 3 | 2 | 53 | 14 | REBALANCE: last column avg 14 chars vs largest 53; narrow last column to p{1.5cm} or merge it with previous | WIDTH GAP: widths [1.0, 1.0, 8.0, 4.2] differ by > 8x; use equal-space strategy |
| `chapters/chapter4_analysis_findings.tex:1567` | `NOLABEL@chapters/chapter4_analysis_findings.tex:1567` | 5 | 12 | 33 | 18 | 32 | 6 | REBALANCE: last column avg 6 chars vs largest 33; narrow last column to p{1.5cm} or merge it with previous |
| `chapters/chapter4_analysis_findings.tex:3813` | `NOLABEL@chapters/chapter4_analysis_findings.tex:3813` | 4 | 2 | 34 | 40 | 13 | REBALANCE: last column avg 13 chars vs largest 40; narrow last column to p{1.5cm} or merge it with previous |
| `chapters/chapter4_analysis_findings.tex:3888` | `NOLABEL@chapters/chapter4_analysis_findings.tex:3888` | 4 | 3 | 16 | 86 | 14 | REBALANCE: last column avg 14 chars vs largest 86; narrow last column to p{1.5cm} or merge it with previous |
| `chapters/chapter4_analysis_findings.tex:3910` | `NOLABEL@chapters/chapter4_analysis_findings.tex:3910` | 4 | 2 | 38 | 8 | 13 | REBALANCE: last column avg 13 chars vs largest 38; narrow last column to p{1.5cm} or merge it with previous |
| `chapters/chapter4_analysis_findings.tex:4018` | `NOLABEL@chapters/chapter4_analysis_findings.tex:4018` | 4 | 3 | 29 | 63 | 4 | REBALANCE: last column avg 4 chars vs largest 63; narrow last column to p{1.5cm} or merge it with previous |
| `chapters/chapter4_analysis_findings.tex:5018` | `NOLABEL@chapters/chapter4_analysis_findings.tex:5018` | 6 | 4 | 22 | 24 | 1 | 37 | 7 | REBALANCE: last column avg 7 chars vs largest 37; narrow last column to p{1.5cm} or merge it with previous |
| `chapters/chapter5_discussion_recommendations.tex:86` | `NOLABEL@chapters/chapter5_discussion_recommendations.tex:86` | 2 | 47 | 17 | REBALANCE: last column avg 17 chars vs largest 47; narrow last column to p{1.5cm} or merge it with previous |
| `chapters/chapter5_discussion_recommendations.tex:1749` | `NOLABEL@chapters/chapter5_discussion_recommendations.tex:1749` | 4 | 16 | 22 | 63 | 19 | REBALANCE: last column avg 19 chars vs largest 63; narrow last column to p{1.5cm} or merge it with previous |
| `chapters/chapter5_discussion_recommendations.tex:3203` | `NOLABEL@chapters/chapter5_discussion_recommendations.tex:3203` | 4 | 2 | 13 | 71 | 15 | REBALANCE: last column avg 15 chars vs largest 71; narrow last column to p{1.5cm} or merge it with previous |
| `chapters/chapter5_discussion_recommendations.tex:3257` | `NOLABEL@chapters/chapter5_discussion_recommendations.tex:3257` | 5 | 1 | 10 | 59 | 73 | 10 | REBALANCE: last column avg 10 chars vs largest 73; narrow last column to p{1.5cm} or merge it with previous |
| `chapters/chapter5_discussion_recommendations.tex:4696` | `NOLABEL@chapters/chapter5_discussion_recommendations.tex:4696` | 8 | 2 | 16 | 1 | 1 | 2 | 41 | 6 | 1 | REBALANCE: last column avg 1 chars vs largest 41; narrow last column to p{1.5cm} or merge it with previous |

## Issue #4 — Tables with TALL-COLUMN (one column has 3+ rows of text)

Count: **12** tables

| File:Line | Label | Cols | Col max text | Rec |
|---|---|---:|---|---|
| `chapters/chapter1_introduction.tex:4458` | `tab:tam_toe_rbv` | 5 | 6 | 321 | 96 | 120 | 136 | WIDEN COL 2 (max 321 chars) by NARROWING COL 1 (avg 3 chars) |
| `chapters/chapter3_research_methods.tex:5311` | `tab:remaining_ai_capability_matrix` | 6 | 33 | 276 | 236 | 236 | 131 | 242 | WIDEN COL 2 (max 276 chars) by NARROWING COL 1 (avg 15 chars) |
| `chapters/chapter3_research_methods.tex:4085` | `tab:ch3_b2b_b2c_questionnaire` | 5 | 251 | 85 | 21 | 3 | 3 | WIDEN COL 1 (max 251 chars) by NARROWING COL 4 (avg 0 chars) |
| `chapters/chapter5_discussion_recommendations.tex:1786` | `tab:ch5_rgaig_vs_peer_frameworks` | 6 | 41 | 48 | 51 | 45 | 45 | 215 | WIDEN COL 6 (max 215 chars) by NARROWING COL 1 (avg 18 chars) |
| `chapters/chapter3_research_methods.tex:2731` | `tab:research_anatomy` | 6 | 3 | 182 | 119 | 100 | 148 | 58 | WIDEN COL 2 (max 182 chars) by NARROWING COL 1 (avg 2 chars) |
| `chapters/chapter1_introduction.tex:3938` | `tab:doctoral_quality_chain` | 5 | 2 | 171 | 73 | 82 | 34 | WIDEN COL 2 (max 171 chars) by NARROWING COL 1 (avg 1 chars) |
| `chapters/chapter3_research_methods.tex:4395` | `tab:b2c_b2b_assessment_crosswalk` | 5 | 79 | 19 | 53 | 140 | 83 | WIDEN COL 4 (max 140 chars) by NARROWING COL 2 (avg 4 chars) |
| `appendices/M_operationalization_detail_p725.tex:629` | `tab:smart_objectives` | 6 | 3 | 119 | 120 | 66 | 60 | 22 | WIDEN COL 3 (max 120 chars) by NARROWING COL 1 (avg 2 chars) |
| `chapters/chapter3_research_methods.tex:5379` | `tab:time_saving_metrics` | 5 | 23 | 95 | 101 | 45 | 117 | WIDEN COL 5 (max 117 chars) by NARROWING COL 1 (avg 19 chars) |
| `chapters/chapter3_research_methods.tex:5204` | `tab:ethical_ai_components` | 5 | 32 | 89 | 112 | 89 | 47 | WIDEN COL 3 (max 112 chars) by NARROWING COL 1 (avg 20 chars) |
| `chapters/chapter3_microservice_ipo.tex:18` | `tab:microservice_ipo_contract` | 5 | 14 | 82 | 104 | 111 | 92 | WIDEN COL 4 (max 111 chars) by NARROWING COL 1 (avg 8 chars) |
| `chapters/chapter3_research_methods.tex:2887` | `tab:ethics_consent_anchor` | 5 | 5 | 110 | 100 | 99 | 53 | WIDEN COL 2 (max 110 chars) by NARROWING COL 1 (avg 2 chars) |

## Issue #5 — Tables that span 3+ pages (should be split into Part 1 / Part 2)

Count: **3** tables (> 50 rows — likely 3+ pages)

| File:Line | Label | Rows | Cols | Caption | Action |
|---|---|---:|---:|---|---|
| `chapters/chapter3_crossref_index.tex:16` | `tab:crossref_index_new` | 106 | 3 | Cross-Reference Index --- New Tables | SPLIT into Part 1 + Part 2 |
| `appendices/S_glossary.tex:11` | `tab:glossary_full` | 81 | 2 | Glossary of Acronyms and Key Terms | SPLIT into Part 1 + Part 2 |
| `appendices/I_brutal_feedback_p632_w64.tex:41` | `tab:brutal_appendices` | 55 | 10 | Per-Appendix Brutal Feedback | SPLIT into Part 1 + Part 2 |

## Issue #5b — Tables that span exactly 2 pages (acceptable, no action)

Count: **11**

## Issue #7 — Tables with WIDTH-IMBALANCE (column widths differ > 4x)

Count: **79** tables

| File:Line | Label | Cols | Widths (cm) | Rec |
|---|---|---:|---|---|
| `chapters/chapter3_research_methods.tex:7274` | `tab:master_rewrite_drafts` | 3 | 1.8 | 2.5 | 10.2 | WIDTH GAP: widths [1.8, 2.5, 10.2] differ by > 8x; use equal-space strategy |
| `chapters/chapter1_introduction.tex:3757` | `tab:main_objectives` | 3 | 1.0 | 9.5 | 1.0 | WIDTH GAP: widths [1.0, 9.5, 1.0] differ by > 8x; use equal-space strategy |
| `chapters/chapter3_crossref_index.tex:16` | `tab:crossref_index_new` | 3 | 1.0 | 9.5 | 1.0 | WIDTH GAP: widths [1.0, 9.5, 1.0] differ by > 8x; use equal-space strategy |
| `chapters/chapter3_examiner_qa.tex:18` | `tab:examiner_qa_architecture` | 3 | 1.0 | 9.5 | 2.7 | WIDTH GAP: widths [1.0, 9.5, 2.7] differ by > 8x; use equal-space strategy |
| `chapters/chapter3_research_methods.tex:3259` | `tab:b2c_research_gap_catalog` | 4 | 1.0 | 9.5 | 1.0 | 1.0 | WIDTH GAP: widths [1.0, 9.5, 1.0, 1.0] differ by > 8x; use equal-space strategy |
| `chapters/chapter3_research_methods.tex:3439` | `tab:b2b_research_gap_catalog` | 4 | 1.0 | 9.5 | 1.0 | 1.0 | WIDTH GAP: widths [1.0, 9.5, 1.0, 1.0] differ by > 8x; use equal-space strategy |
| `chapters/chapter4_analysis_findings.tex:5888` | `tab:ch4_partd_framework_quality` | 3 | 3.2 | 9.5 | 1.0 | WIDTH GAP: widths [3.2, 9.5, 1.0] differ by > 8x; use equal-space strategy |
| `chapters/chapter4_analysis_findings.tex:6232` | `tab:ch4_b2c_problem_score` | 5 | 1.0 | 9.5 | 1.0 | 1.0 | 1.0 | WIDTH GAP: widths [1.0, 9.5, 1.0, 1.0, 1.0] differ by > 8x; use equal-space strategy |
| `chapters/chapter5_discussion_recommendations.tex:4029` | `tab:ch5_final_verdict` | 3 | 2.6 | 2.0 | 9.5 | WIDTH GAP: widths [2.6, 2.0, 9.5] differ by > 8x; use equal-space strategy |
| `appendices/F_survey_instrument_p566_w1285.tex:1123` | `tab:survey_b2c_primary_addendum` | 3 | 1.0 | 9.5 | 3.5 | REBALANCE: last column avg 11 chars vs largest 85; narrow last column to p{1.5cm} or merge it with previous | WIDTH GAP: widths [1.0, 9.5, 3.5] differ by > 8x; use equal-space strategy |
| `appendices/H_rgaig_architecture_p605_w1135.tex:296` | `tab:appo_maturity_arch` | 3 | 1.0 | 3.3 | 9.5 | WIDTH GAP: widths [1.0, 3.3, 9.5] differ by > 8x; use equal-space strategy |
| `appendices/H_rgaig_architecture_p605_w1135.tex:944` | `tab:appo_audit_fields` | 2 | 1.0 | 9.5 | WIDTH GAP: widths [1.0, 9.5] differ by > 8x; use equal-space strategy |
| `appendices/M_operationalization_detail_p725.tex:419` | `tab:part_objectives` | 4 | 1.0 | 9.5 | 1.0 | 1.0 | WIDTH GAP: widths [1.0, 9.5, 1.0, 1.0] differ by > 8x; use equal-space strategy |
| `appendices/M_operationalization_detail_p725.tex:495` | `tab:research_objectives` | 3 | 1.0 | 9.5 | 3.0 | REBALANCE: last column avg 6 chars vs largest 69; narrow last column to p{1.5cm} or merge it with previous | WIDTH GAP: widths [1.0, 9.5, 3.0] differ by > 8x; use equal-space strategy |
| `appendices/M_operationalization_detail_p725.tex:670` | `tab:rq_mapping` | 3 | 1.0 | 9.5 | 1.0 | WIDTH GAP: widths [1.0, 9.5, 1.0] differ by > 8x; use equal-space strategy |
| `chapters/chapter3_research_methods.tex:4466` | `tab:scale_design` | 3 | 3.9 | 9.4 | 1.0 | WIDTH GAP: widths [3.9, 9.4, 1.0] differ by > 8x; use equal-space strategy |
| `chapters/chapter4_analysis_findings.tex:6266` | `tab:ch4_b2b_problem_score` | 5 | 1.0 | 9.4 | 1.0 | 1.0 | 1.5 | WIDTH GAP: widths [1.0, 9.4, 1.0, 1.0, 1.5] differ by > 8x; use equal-space strategy |
| `chapters/chapter5_discussion_recommendations.tex:6344` | `tab:secondary_data_stack` | 3 | 1.0 | 9.4 | 4.0 | REBALANCE: last column avg 9 chars vs largest 47; narrow last column to p{1.5cm} or merge it with previous | WIDTH GAP: widths [1.0, 9.4, 4.0] differ by > 8x; use equal-space strategy |
| `chapters/chapter4_analysis_findings.tex:527` | `tab:ch4_org_interpretation` | 3 | 1.0 | 4.1 | 9.3 | WIDTH GAP: widths [1.0, 4.1, 9.3] differ by > 8x; use equal-space strategy |
| `appendices/H_rgaig_architecture_p605_w1135.tex:328` | `tab:appo_gov_dimensions` | 3 | 4.0 | 9.3 | 1.0 | WIDTH GAP: widths [4.0, 9.3, 1.0] differ by > 8x; use equal-space strategy |
| `chapters/chapter1_introduction.tex:3333` | `tab:backend_db` | 4 | 1.0 | 1.0 | 9.2 | 2.9 | REBALANCE: last column avg 10 chars vs largest 99; narrow last column to p{1.5cm} or merge it with previous | WIDTH GAP: widths [1.0, 1.0, 9.2, 2.9] differ by > 8x; use equal-space strategy |
| `chapters/chapter3_research_methods.tex:398` | `tab:ch3_instrument_anchoring` | 3 | 4.3 | 9.1 | 1.0 | WIDTH GAP: widths [4.3, 9.1, 1.0] differ by > 8x; use equal-space strategy |
| `chapters/chapter1_introduction.tex:1693` | `tab:b2b_subproblems` | 3 | 1.0 | 4.3 | 9.0 | WIDTH GAP: widths [1.0, 4.3, 9.0] differ by > 8x; use equal-space strategy |
| `chapters/chapter1_introduction.tex:558` | `tab:ch1_object_scope` | 3 | 1.0 | 8.9 | 4.4 | REBALANCE: last column avg 11 chars vs largest 46; narrow last column to p{1.5cm} or merge it with previous | WIDTH GAP: widths [1.0, 8.9, 4.4] differ by > 8x; use equal-space strategy |
| `chapters/chapter1_introduction.tex:1729` | `tab:b2c_subproblems` | 3 | 1.0 | 4.4 | 8.9 | WIDTH GAP: widths [1.0, 4.4, 8.9] differ by > 8x; use equal-space strategy |
| `appendices/C_ch3_supp_p267_w1470.tex:1027` | `tab:eeg_workflow_governance` | 3 | 3.9 | 8.9 | 1.5 | WIDTH GAP: widths [3.9, 8.9, 1.5] differ by > 8x; use equal-space strategy |
| `appendices/H_rgaig_architecture_p605_w1135.tex:38` | `tab:appo_tech_research_map` | 3 | 4.6 | 8.8 | 1.0 | WIDTH GAP: widths [4.6, 8.8, 1.0] differ by > 8x; use equal-space strategy |
| `chapters/chapter3_research_methods.tex:12606` | `tab:task_flow_actor` | 6 | 1.0 | 8.7 | 1.0 | 1.0 | 1.0 | 1.0 | WIDTH GAP: widths [1.0, 8.7, 1.0, 1.0, 1.0, 1.0] differ by > 8x; use equal-space strategy |
| `chapters/chapter1_introduction.tex:3292` | `tab:knowledge_pipeline` | 4 | 1.0 | 3.2 | 8.5 | 1.5 | WIDTH GAP: widths [1.0, 3.2, 8.5, 1.5] differ by > 8x; use equal-space strategy |
| `appendices/D_ch4_supp_p390_w814.tex:311` | `tab:eval_explain_trust` | 3 | 4.8 | 8.5 | 1.0 | WIDTH GAP: widths [4.8, 8.5, 1.0] differ by > 8x; use equal-space strategy |
| `appendices/D_supp_tables_p390_w17.tex:205` | `tab:eeg_frequency_bands` | 4 | 2.0 | 2.0 | 2.0 | 8.5 | WIDTH GAP: widths [2.0, 2.0, 2.0, 8.5] differ by > 8x; use equal-space strategy |
| `appendices/E_ch5_supp_p525_w1059.tex:48` | `tab:dash_research_ui_map` | 3 | 4.3 | 8.5 | 1.5 | WIDTH GAP: widths [4.3, 8.5, 1.5] differ by > 8x; use equal-space strategy |
| `appendices/Q_drill_methodology.tex:57` | `tab:app_q_drill_anatomy` | 3 | 1.0 | 4.9 | 8.5 | WIDTH GAP: widths [1.0, 4.9, 8.5] differ by > 8x; use equal-space strategy |
| `chapters/chapter1_introduction.tex:5267` | `tab:ch1_kit_objectives` | 3 | 4.7 | 8.2 | 1.5 | WIDTH GAP: widths [4.7, 8.2, 1.5] differ by > 8x; use equal-space strategy |
| `appendices/F_survey_instrument_p566_w1285.tex:978` | `tab:survey_section_g` | 3 | 1.0 | 8.2 | 5.2 | WIDTH GAP: widths [1.0, 8.2, 5.2] differ by > 8x; use equal-space strategy |
| `chapters/chapter1_introduction.tex:616` | `tab:ch1_task_map` | 4 | 1.0 | 8.1 | 1.0 | 4.1 | REBALANCE: last column avg 10 chars vs largest 40; narrow last column to p{1.5cm} or merge it with previous | WIDTH GAP: widths [1.0, 8.1, 1.0, 4.1] differ by > 8x; use equal-space strategy |
| `appendices/D_ch4_supp_p390_w814.tex:159` | `tab:appd_cmb_tests` | 3 | 5.3 | 8.1 | 1.0 | WIDTH GAP: widths [5.3, 8.1, 1.0] differ by > 8x; use equal-space strategy |
| `chapters/chapter3_arch_changelog.tex:19` | `tab:arch_iteration_changelog` | 4 | 1.0 | 8.0 | 3.6 | 1.5 | WIDTH GAP: widths [1.0, 8.0, 3.6, 1.5] differ by > 8x; use equal-space strategy |
| `chapters/chapter4_analysis_findings.tex:914` | `tab:ch4_alignment` | 4 | 1.0 | 1.0 | 8.0 | 4.2 | REBALANCE: last column avg 14 chars vs largest 53; narrow last column to p{1.5cm} or merge it with previous | WIDTH GAP: widths [1.0, 1.0, 8.0, 4.2] differ by > 8x; use equal-space strategy |
| `chapters/chapter5_discussion_recommendations.tex:643` | `tab:ch5_final_defence_checklist` | 4 | 1.0 | 8.0 | 4.1 | 1.0 | WIDTH GAP: widths [1.0, 8.0, 4.1, 1.0] differ by > 8x; use equal-space strategy |

## Build-Log Overflows (vbox bottom + hbox horizontal)

- **vbox bottom-overflows**: 7 pages with content past page-bottom

| Severity (pt too high) | Action |
|---:|---|
| 565.8 | reduce table size, add \clearpage, or \resizebox |
| 429.7 | reduce table size, add \clearpage, or \resizebox |
| 252.3 | reduce table size, add \clearpage, or \resizebox |
| 137.6 | reduce table size, add \clearpage, or \resizebox |
| 68.6 | reduce table size, add \clearpage, or \resizebox |
| 60.9 | reduce table size, add \clearpage, or \resizebox |
| 33.8 | reduce table size, add \clearpage, or \resizebox |

- **hbox horizontal-overflows**: 1280 cells exceed text-width

