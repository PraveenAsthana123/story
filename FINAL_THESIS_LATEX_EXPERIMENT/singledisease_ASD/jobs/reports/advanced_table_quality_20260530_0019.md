# Advanced Table Quality Audit

Generated: 2026-05-30T00:19:01.636783

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
- **Build-log hbox horizontal-overflows**: 1528
- **tall_column**: 226 tables
- **width_imbalanced**: 191 tables
- **right_side_empty**: 187 tables
- **empty_cells**: 72 tables
- **multi_page**: 13 tables
- **very_multi_page**: 3 tables
- **placeholders**: 1 tables

## Issue #3 — Tables with RIGHT-SIDE EMPTY (last column nearly empty)

Count: **187** tables

| File:Line | Label | Cols | Col avg text lengths | Rec |
|---|---|---:|---|---|
| `chapters/chapter1_introduction.tex:562` | `tab:ch1_object_scope` | 3 | 2 | 46 | 6 | REBALANCE: last column avg 6 chars vs largest 46; narrow last column to p{1.5cm} or merge it with previous | WIDTH GAP: widths [1.5, 9.5, 1.5] differ by > 8x; use equal-space strategy |
| `chapters/chapter1_introduction.tex:620` | `tab:ch1_task_map` | 4 | 2 | 36 | 4 | 5 | REBALANCE: last column avg 5 chars vs largest 36; narrow last column to p{1.5cm} or merge it with previous | WIDTH GAP: widths [1.5, 8.1, 1.5, 1.5] differ by > 8x; use equal-space strategy |
| `chapters/chapter1_introduction.tex:1003` | `tab:research_positioning` | 5 | 2 | 46 | 78 | 57 | 6 | REBALANCE: last column avg 6 chars vs largest 78; narrow last column to p{1.5cm} or merge it with previous |
| `chapters/chapter1_introduction.tex:1295` | `tab:as_is_to_be` | 5 | 5 | 21 | 16 | 33 | 12 | REBALANCE: last column avg 12 chars vs largest 33; narrow last column to p{1.5cm} or merge it with previous |
| `chapters/chapter1_introduction.tex:2158` | `NOLABEL@chapters/chapter1_introduction.tex:2158` | 4 | 1 | 14 | 87 | 12 | REBALANCE: last column avg 12 chars vs largest 87; narrow last column to p{1.5cm} or merge it with previous | WIDEN COL 3 (max 120 chars) by NARROWING COL 1 (avg 1 chars) | WIDTH GAP: widths [0.6, 3.0, None, 2.5] differ by > 8x; use equal-space strategy |
| `chapters/chapter1_introduction.tex:2280` | `tab:problem_decomposition` | 5 | 2 | 3 | 18 | 54 | 9 | REBALANCE: last column avg 9 chars vs largest 54; narrow last column to p{1.5cm} or merge it with previous |
| `chapters/chapter1_introduction.tex:2693` | `tab:b2c_mobile_screens` | 4 | 2 | 14 | 118 | 12 | REBALANCE: last column avg 12 chars vs largest 118; narrow last column to p{1.5cm} or merge it with previous | WIDEN COL 3 (max 145 chars) by NARROWING COL 1 (avg 2 chars) | WIDTH GAP: widths [1.5, 1.5, 9.5, 1.5] differ by > 8x; use equal-space strategy |
| `chapters/chapter1_introduction.tex:2757` | `tab:b2c_user_forms` | 4 | 2 | 16 | 94 | 10 | REBALANCE: last column avg 10 chars vs largest 93; narrow last column to p{1.5cm} or merge it with previous | WIDEN COL 3 (max 122 chars) by NARROWING COL 1 (avg 2 chars) | WIDTH GAP: widths [1.5, 1.5, 8.6, 1.5] differ by > 8x; use equal-space strategy |
| `chapters/chapter1_introduction.tex:2944` | `tab:report_types` | 4 | 2 | 15 | 88 | 9 | REBALANCE: last column avg 9 chars vs largest 88; narrow last column to p{1.5cm} or merge it with previous | WIDEN COL 3 (max 106 chars) by NARROWING COL 1 (avg 2 chars) | WIDTH GAP: widths [1.5, 1.5, 8.6, 1.5] differ by > 8x; use equal-space strategy |
| `chapters/chapter1_introduction.tex:3094` | `tab:continuous_monitoring` | 4 | 2 | 14 | 105 | 10 | REBALANCE: last column avg 9 chars vs largest 105; narrow last column to p{1.5cm} or merge it with previous | WIDEN COL 3 (max 155 chars) by NARROWING COL 1 (avg 2 chars) | WIDTH GAP: widths [1.5, 1.5, 8.8, 1.5] differ by > 8x; use equal-space strategy |
| `chapters/chapter1_introduction.tex:3316` | `tab:knowledge_pipeline` | 4 | 2 | 16 | 113 | 9 | REBALANCE: last column avg 9 chars vs largest 113; narrow last column to p{1.5cm} or merge it with previous | WIDEN COL 3 (max 155 chars) by NARROWING COL 1 (avg 2 chars) | WIDTH GAP: widths [1.5, 1.5, 8.8, 1.5] differ by > 8x; use equal-space strategy |
| `chapters/chapter1_introduction.tex:3357` | `tab:backend_db` | 4 | 2 | 1 | 99 | 10 | REBALANCE: last column avg 10 chars vs largest 99; narrow last column to p{1.5cm} or merge it with previous | WIDEN COL 3 (max 127 chars) by NARROWING COL 2 (avg 1 chars) | WIDTH GAP: widths [1.5, 1.5, 8.1, 1.5] differ by > 8x; use equal-space strategy |
| `chapters/chapter1_introduction.tex:3416` | `tab:research_approach` | 5 | 2 | 14 | 74 | 83 | 6 | REBALANCE: last column avg 6 chars vs largest 83; narrow last column to p{1.5cm} or merge it with previous | WIDEN COL 4 (max 128 chars) by NARROWING COL 1 (avg 2 chars) |
| `chapters/chapter1_introduction.tex:3783` | `tab:main_objectives` | 3 | 2 | 84 | 2 | REBALANCE: last column avg 2 chars vs largest 84; narrow last column to p{1.5cm} or merge it with previous | WIDEN COL 2 (max 115 chars) by NARROWING COL 3 (avg 2 chars) | WIDTH GAP: widths [1.5, 9.5, 1.5] differ by > 8x; use equal-space strategy |
| `chapters/chapter1_introduction.tex:3922` | `tab:research_process` | 5 | 1 | 17 | 89 | 74 | 5 | REBALANCE: last column avg 5 chars vs largest 89; narrow last column to p{1.5cm} or merge it with previous | WIDEN COL 3 (max 126 chars) by NARROWING COL 1 (avg 1 chars) |
| `chapters/chapter1_introduction.tex:3996` | `tab:variable_taxonomy` | 5 | 5 | 19 | 80 | 48 | 12 | REBALANCE: last column avg 12 chars vs largest 80; narrow last column to p{1.5cm} or merge it with previous | WIDEN COL 3 (max 147 chars) by NARROWING COL 1 (avg 5 chars) | WIDTH GAP: widths [1.5, 1.5, 6.3, 2.5, 1.5] differ by > 8x; use equal-space strategy |
| `chapters/chapter1_introduction.tex:4517` | `tab:statistical_methods` | 4 | 10 | 69 | 120 | 12 | REBALANCE: last column avg 12 chars vs largest 120; narrow last column to p{1.5cm} or merge it with previous | WIDEN COL 3 (max 155 chars) by NARROWING COL 1 (avg 10 chars) | WIDTH GAP: widths [1.5, 3.2, 8.4, 1.5] differ by > 8x; use equal-space strategy |
| `chapters/chapter1_introduction.tex:5173` | `tab:ch1_scorecard` | 3 | 16 | 31 | 5 | REBALANCE: last column avg 5 chars vs largest 31; narrow last column to p{1.5cm} or merge it with previous | WIDTH GAP: widths [4.0, 7.7, 1.5] differ by > 8x; use equal-space strategy |
| `chapters/chapter1_introduction.tex:5303` | `tab:ch1_kit_objectives` | 3 | 27 | 76 | 6 | REBALANCE: last column avg 6 chars vs largest 76; narrow last column to p{1.5cm} or merge it with previous | WIDEN COL 2 (max 161 chars) by NARROWING COL 3 (avg 6 chars) | WIDTH GAP: widths [2.2, 9.5, 1.5] differ by > 8x; use equal-space strategy |
| `chapters/chapter2_literature.tex:1068` | `NOLABEL@chapters/chapter2_literature.tex:1068` | 5 | 8 | 105 | 0 | 0 | 0 | REBALANCE: last column avg 0 chars vs largest 105; narrow last column to p{1.5cm} or merge it with previous | WIDEN COL 2 (max 105 chars) by NARROWING COL 1 (avg 8 chars) |
| `chapters/chapter2_literature.tex:1401` | `NOLABEL@chapters/chapter2_literature.tex:1401` | 4 | 3 | 31 | 16 | 0 | REBALANCE: last column avg 0 chars vs largest 31; narrow last column to p{1.5cm} or merge it with previous |
| `chapters/chapter2_literature.tex:1469` | `NOLABEL@chapters/chapter2_literature.tex:1469` | 3 | 19 | 197 | 0 | REBALANCE: last column avg 0 chars vs largest 197; narrow last column to p{1.5cm} or merge it with previous | WIDEN COL 2 (max 197 chars) by NARROWING COL 1 (avg 19 chars) |
| `chapters/chapter2_literature.tex:2626` | `tab:ch2_scorecard` | 3 | 17 | 32 | 6 | REBALANCE: last column avg 6 chars vs largest 32; narrow last column to p{1.5cm} or merge it with previous | WIDTH GAP: widths [4.0, 7.7, 1.5] differ by > 8x; use equal-space strategy |
| `chapters/chapter3_arch_changelog.tex:18` | `tab:arch_iteration_changelog` | 4 | 1 | 60 | 20 | 6 | REBALANCE: last column avg 6 chars vs largest 60; narrow last column to p{1.5cm} or merge it with previous | WIDEN COL 2 (max 145 chars) by NARROWING COL 1 (avg 1 chars) | WIDTH GAP: widths [1.5, 7.9, 1.7, 1.5] differ by > 8x; use equal-space strategy |
| `chapters/chapter3_arch_executive_summary.tex:17` | `tab:arch_exec_summary` | 3 | 23 | 91 | 10 | REBALANCE: last column avg 10 chars vs largest 91; narrow last column to p{1.5cm} or merge it with previous | WIDEN COL 2 (max 154 chars) by NARROWING COL 3 (avg 10 chars) | WIDTH GAP: widths [1.7, 9.5, 1.5] differ by > 8x; use equal-space strategy |
| `chapters/chapter3_defence_prep_checklist.tex:18` | `tab:defence_prep_arch_checklist` | 4 | 2 | 48 | 4 | 8 | REBALANCE: last column avg 8 chars vs largest 48; narrow last column to p{1.5cm} or merge it with previous | WIDTH GAP: widths [1.5, 8.1, 1.5, 1.5] differ by > 8x; use equal-space strategy |
| `chapters/chapter3_iso_audit_runbook.tex:18` | `tab:iso_audit_runbook` | 5 | 31 | 46 | 19 | 16 | 12 | REBALANCE: last column avg 12 chars vs largest 46; narrow last column to p{1.5cm} or merge it with previous |
| `chapters/chapter3_research_methods.tex:92` | `NOLABEL@chapters/chapter3_research_methods.tex:92` | 2 | 43 | 13 | REBALANCE: last column avg 13 chars vs largest 43; narrow last column to p{1.5cm} or merge it with previous |
| `chapters/chapter3_research_methods.tex:401` | `tab:ch3_instrument_anchoring` | 3 | 25 | 108 | 2 | REBALANCE: last column avg 2 chars vs largest 108; narrow last column to p{1.5cm} or merge it with previous | WIDEN COL 2 (max 194 chars) by NARROWING COL 3 (avg 2 chars) | WIDTH GAP: widths [1.5, 9.5, 1.5] differ by > 8x; use equal-space strategy |
| `chapters/chapter3_research_methods.tex:533` | `tab:ch3_statistical_plan` | 4 | 1 | 18 | 69 | 8 | REBALANCE: last column avg 8 chars vs largest 69; narrow last column to p{1.5cm} or merge it with previous | WIDTH GAP: widths [1.5, 2.0, 7.6, 1.5] differ by > 8x; use equal-space strategy |
| `chapters/chapter3_research_methods.tex:997` | `tab:combined_methodology_flow` | 5 | 9 | 45 | 38 | 18 | 17 | REBALANCE: last column avg 17 chars vs largest 45; narrow last column to p{1.5cm} or merge it with previous |
| `chapters/chapter3_research_methods.tex:1476` | `tab:primary_data_outcome_map` | 3 | 6 | 50 | 5 | REBALANCE: last column avg 5 chars vs largest 50; narrow last column to p{1.5cm} or merge it with previous | WIDTH GAP: widths [1.5, 9.5, 1.5] differ by > 8x; use equal-space strategy |
| `chapters/chapter3_research_methods.tex:1720` | `tab:hybrid_data_reference_catalog` | 4 | 4 | 32 | 20 | 6 | REBALANCE: last column avg 6 chars vs largest 32; narrow last column to p{1.5cm} or merge it with previous |
| `chapters/chapter3_research_methods.tex:1949` | `tab:primary_computed_output` | 7 | 44 | 3 | 3 | 3 | 4 | 4 | 9 | REBALANCE: last column avg 9 chars vs largest 44; narrow last column to p{1.5cm} or merge it with previous | WIDEN COL 1 (max 231 chars) by NARROWING COL 2 (avg 3 chars) |
| `chapters/chapter3_research_methods.tex:1983` | `tab:primary_flow` | 4 | 2 | 16 | 65 | 14 | REBALANCE: last column avg 14 chars vs largest 65; narrow last column to p{1.5cm} or merge it with previous | WIDEN COL 3 (max 101 chars) by NARROWING COL 1 (avg 2 chars) | WIDTH GAP: widths [1.5, 1.5, 8.5, 1.5] differ by > 8x; use equal-space strategy |
| `chapters/chapter3_research_methods.tex:3029` | `tab:research_objective_catalog` | 6 | 2 | 58 | 44 | 3 | 10 | 13 | REBALANCE: last column avg 13 chars vs largest 58; narrow last column to p{1.5cm} or merge it with previous |
| `chapters/chapter3_research_methods.tex:3059` | `tab:research_gap_catalog` | 6 | 2 | 48 | 23 | 7 | 3 | 3 | REBALANCE: last column avg 3 chars vs largest 48; narrow last column to p{1.5cm} or merge it with previous |
| `chapters/chapter3_research_methods.tex:3144` | `tab:value_roi_kpi_impact` | 6 | 2 | 49 | 19 | 24 | 31 | 12 | REBALANCE: last column avg 12 chars vs largest 49; narrow last column to p{1.5cm} or merge it with previous |
| `chapters/chapter3_research_methods.tex:3203` | `tab:b2c_sub_problem_catalog` | 5 | 5 | 2 | 34 | 35 | 3 | REBALANCE: last column avg 3 chars vs largest 35; narrow last column to p{1.5cm} or merge it with previous |
| `chapters/chapter3_research_methods.tex:3232` | `tab:b2c_research_objective_catalog` | 4 | 2 | 50 | 41 | 3 | REBALANCE: last column avg 3 chars vs largest 50; narrow last column to p{1.5cm} or merge it with previous |

## Issue #4 — Tables with TALL-COLUMN (one column has 3+ rows of text)

Count: **226** tables

| File:Line | Label | Cols | Col max text | Rec |
|---|---|---:|---|---|
| `chapters/chapter3_research_methods.tex:7284` | `tab:master_rewrite_drafts` | 3 | 9 | 25 | 896 | WIDEN COL 3 (max 896 chars) by NARROWING COL 1 (avg 9 chars) | WIDTH GAP: widths [1.8, 2.5, 10.2] differ by > 8x; use equal-space strategy |
| `appendices/F_survey_instrument_p566_w1285.tex:981` | `tab:survey_section_g` | 3 | 2 | 483 | 217 | WIDEN COL 2 (max 483 chars) by NARROWING COL 1 (avg 2 chars) | WIDTH GAP: widths [1.5, 8.7, 3.0] differ by > 8x; use equal-space strategy |
| `chapters/chapter3_examiner_qa.tex:17` | `tab:examiner_qa_architecture` | 3 | 3 | 437 | 441 | WIDEN COL 3 (max 441 chars) by NARROWING COL 1 (avg 2 chars) | WIDTH GAP: widths [1.5, 9.5, 1.5] differ by > 8x; use equal-space strategy |
| `chapters/chapter3_research_methods.tex:10042` | `NOLABEL@chapters/chapter3_research_methods.tex:10042` | 6 | 6 | 422 | 0 | 0 | 0 | 0 | REBALANCE: last column avg 0 chars vs largest 422; narrow last column to p{1.5cm} or merge it with previous | WIDEN COL 2 (max 422 chars) by NARROWING COL 1 (avg 6 chars) |
| `appendices/C_ch3_supp_p267_w1470.tex:1475` | `NOLABEL@appendices/C_ch3_supp_p267_w1470.tex:1475` | 3 | 9 | 51 | 364 | WIDEN COL 3 (max 364 chars) by NARROWING COL 1 (avg 9 chars) | WIDTH GAP: widths [1.6, 4.6, 8.0] differ by > 8x; use equal-space strategy |
| `appendices/D_ch4_supp_p390_w814.tex:117` | `tab:appd_mediation_detail` | 7 | 338 | 23 | 4 | 4 | 4 | 1 | 46 | WIDEN COL 1 (max 338 chars) by NARROWING COL 6 (avg 1 chars) |
| `appendices/N_indian_cohort_acquisition_p1090.tex:317` | `tab:appendix_n_compensation_reward` | 3 | 62 | 334 | 156 | WIDEN COL 2 (max 334 chars) by NARROWING COL 1 (avg 31 chars) | WIDTH GAP: widths [1.5, 8.2, 3.9] differ by > 8x; use equal-space strategy |
| `chapters/chapter3_research_methods.tex:11056` | `NOLABEL@chapters/chapter3_research_methods.tex:11056` | 5 | 2 | 21 | 325 | 94 | 118 | WIDEN COL 3 (max 325 chars) by NARROWING COL 1 (avg 1 chars) | WIDTH GAP: widths [0.4, 2.0, None, None, 1.5] differ by > 8x; use equal-space strategy |
| `chapters/chapter1_introduction.tex:4488` | `tab:tam_toe_rbv` | 5 | 6 | 321 | 96 | 120 | 133 | WIDEN COL 2 (max 321 chars) by NARROWING COL 1 (avg 3 chars) |
| `appendices/N_indian_cohort_acquisition_p1090.tex:64` | `tab:appendix_n_what_quantitative` | 4 | 30 | 65 | 321 | 105 | WIDEN COL 3 (max 321 chars) by NARROWING COL 1 (avg 16 chars) | WIDTH GAP: widths [1.5, 1.5, 8.7, 2.3] differ by > 8x; use equal-space strategy |
| `chapters/chapter3_research_methods.tex:1170` | `tab:asd_23step_expanded` | 4 | 2 | 36 | 311 | 67 | WIDEN COL 3 (max 311 chars) by NARROWING COL 1 (avg 2 chars) | WIDTH GAP: widths [1.5, 1.5, 9.2, 1.5] differ by > 8x; use equal-space strategy |
| `appendices/M_operationalization_detail_p725.tex:57` | `tab:examiner_traceability_pack` | 4 | 21 | 310 | 162 | 25 | REBALANCE: last column avg 15 chars vs largest 157; narrow last column to p{1.5cm} or merge it with previous | WIDEN COL 2 (max 310 chars) by NARROWING COL 1 (avg 11 chars) | WIDTH GAP: widths [1.5, 7.8, 4.0, 1.5] differ by > 8x; use equal-space strategy |
| `chapters/chapter3_research_methods.tex:4081` | `tab:ch3_b2b_b2c_questionnaire` | 5 | 6 | 296 | 21 | 3 | 3 | REBALANCE: last column avg 0 chars vs largest 72; narrow last column to p{1.5cm} or merge it with previous | WIDEN COL 2 (max 296 chars) by NARROWING COL 4 (avg 0 chars) | WIDTH GAP: widths [1.5, 6.5, 1.5, 1.5, 1.5] differ by > 8x; use equal-space strategy |
| `appendices/C_ch3_supp_p267_w1470.tex:4054` | `tab:appc_partd_reference_full` | 3 | 283 | 54 | 56 | WIDEN COL 1 (max 283 chars) by NARROWING COL 1 (avg 24 chars) |
| `chapters/chapter3_research_methods.tex:5307` | `tab:remaining_ai_capability_matrix` | 6 | 33 | 276 | 236 | 236 | 191 | 242 | WIDEN COL 2 (max 276 chars) by NARROWING COL 1 (avg 15 chars) |
| `appendices/D_ch4_supp_p390_w814.tex:2334` | `tab:appd_partd_framework_quality_full` | 5 | 267 | 25 | 35 | 20 | 16 | WIDEN COL 1 (max 267 chars) by NARROWING COL 4 (avg 5 chars) | WIDTH GAP: widths [6.4, 1.9, 1.6, 1.5, 1.5] differ by > 8x; use equal-space strategy |
| `appendices/C_ch3_supp_p267_w1470.tex:788` | `tab:8phase_overview` | 5 | 2 | 21 | 4 | 265 | 70 | WIDEN COL 4 (max 265 chars) by NARROWING COL 1 (avg 1 chars) | WIDTH GAP: widths [0.5, 2.2, 0.6, None, 3.2] differ by > 8x; use equal-space strategy |
| `chapters/chapter1_introduction.tex:728` | `tab:chapter_phase_alignment` | 5 | 22 | 260 | 29 | 19 | 59 | WIDEN COL 2 (max 260 chars) by NARROWING COL 4 (avg 9 chars) |
| `appendices/F_survey_instrument_p566_w1285.tex:1102` | `tab:survey_section_h_patient` | 7 | 2 | 257 | 2 | 1 | 1 | 1 | 2 | REBALANCE: last column avg 1 chars vs largest 155; narrow last column to p{1.5cm} or merge it with previous | WIDEN COL 2 (max 257 chars) by NARROWING COL 4 (avg 1 chars) |
| `chapters/chapter3_companion_deliverables.tex:19` | `tab:companion_deliverables` | 3 | 35 | 256 | 52 | WIDEN COL 2 (max 256 chars) by NARROWING COL 3 (avg 24 chars) | WIDTH GAP: widths [1.5, 9.5, 1.5] differ by > 8x; use equal-space strategy |
| `chapters/chapter4_analysis_findings.tex:533` | `tab:ch4_org_interpretation` | 3 | 3 | 55 | 255 | WIDEN COL 3 (max 255 chars) by NARROWING COL 1 (avg 2 chars) | WIDTH GAP: widths [1.5, 1.5, 9.5] differ by > 8x; use equal-space strategy |
| `appendices/F_survey_instrument_p566_w1285.tex:955` | `tab:survey_section_f_halluc` | 7 | 2 | 254 | 2 | 1 | 1 | 1 | 2 | REBALANCE: last column avg 1 chars vs largest 153; narrow last column to p{1.5cm} or merge it with previous | WIDEN COL 2 (max 254 chars) by NARROWING COL 4 (avg 1 chars) |
| `chapters/chapter5_discussion_recommendations.tex:370` | `tab:ch5_managerial_implications` | 3 | 38 | 252 | 35 | WIDEN COL 2 (max 252 chars) by NARROWING COL 1 (avg 23 chars) | WIDTH GAP: widths [1.5, 9.5, 1.5] differ by > 8x; use equal-space strategy |
| `chapters/chapter5_discussion_recommendations.tex:814` | `tab:ch5_hybrid_discussion_synthesis` | 3 | 11 | 170 | 251 | WIDEN COL 3 (max 251 chars) by NARROWING COL 1 (avg 8 chars) | WIDTH GAP: widths [1.5, 6.0, 6.9] differ by > 8x; use equal-space strategy |
| `chapters/chapter5_discussion_recommendations.tex:4047` | `tab:ch5_final_verdict` | 3 | 14 | 8 | 244 | WIDEN COL 3 (max 244 chars) by NARROWING COL 2 (avg 6 chars) | WIDTH GAP: widths [1.5, 1.5, 9.5] differ by > 8x; use equal-space strategy |
| `chapters/chapter2_literature.tex:541` | `tab:lit_contradictions` | 3 | 43 | 243 | 213 | WIDEN COL 2 (max 243 chars) by NARROWING COL 1 (avg 30 chars) | WIDTH GAP: widths [1.5, 7.6, 4.4] differ by > 8x; use equal-space strategy |
| `chapters/chapter3_research_methods.tex:5058` | `tab:generative_ai_report_types` | 3 | 49 | 146 | 241 | WIDEN COL 3 (max 241 chars) by NARROWING COL 1 (avg 33 chars) | WIDTH GAP: widths [1.5, 4.6, 7.7] differ by > 8x; use equal-space strategy |
| `appendices/C_ch3_supp_p267_w1470.tex:832` | `tab:10pillars` | 5 | 2 | 24 | 4 | 241 | 70 | WIDEN COL 4 (max 241 chars) by NARROWING COL 1 (avg 1 chars) | WIDTH GAP: widths [0.5, 2.0, 0.6, None, 3.2] differ by > 8x; use equal-space strategy |
| `chapters/chapter4_analysis_findings.tex:5919` | `tab:ch4_partd_framework_quality` | 3 | 22 | 238 | 181 | WIDEN COL 2 (max 238 chars) by NARROWING COL 1 (avg 16 chars) | WIDTH GAP: widths [1.5, 7.5, 4.9] differ by > 8x; use equal-space strategy |
| `chapters/chapter3_research_methods.tex:12960` | `tab:ch3_decision_summary` | 3 | 54 | 236 | 201 | WIDEN COL 2 (max 236 chars) by NARROWING COL 1 (avg 40 chars) | WIDTH GAP: widths [1.5, 8.6, 3.1] differ by > 8x; use equal-space strategy |
| `chapters/chapter3_research_methods.tex:1949` | `tab:primary_computed_output` | 7 | 231 | 4 | 4 | 4 | 4 | 6 | 12 | REBALANCE: last column avg 9 chars vs largest 44; narrow last column to p{1.5cm} or merge it with previous | WIDEN COL 1 (max 231 chars) by NARROWING COL 2 (avg 3 chars) |
| `appendices/F_survey_instrument_p566_w1285.tex:805` | `tab:survey_section_e_wf` | 7 | 2 | 231 | 2 | 1 | 1 | 1 | 2 | REBALANCE: last column avg 1 chars vs largest 159; narrow last column to p{1.5cm} or merge it with previous | WIDEN COL 2 (max 231 chars) by NARROWING COL 4 (avg 1 chars) |
| `chapters/chapter3_research_methods.tex:332` | `tab:ch3_mixed_methods_justification` | 3 | 54 | 230 | 190 | WIDEN COL 2 (max 230 chars) by NARROWING COL 1 (avg 28 chars) | WIDTH GAP: widths [1.5, 7.0, 5.4] differ by > 8x; use equal-space strategy |
| `chapters/chapter3_research_methods.tex:5088` | `tab:decision_ai_decisions` | 4 | 34 | 230 | 162 | 101 | WIDEN COL 2 (max 230 chars) by NARROWING COL 1 (avg 25 chars) |
| `chapters/chapter5_discussion_recommendations.tex:4290` | `NOLABEL@chapters/chapter5_discussion_recommendations.tex:4290` | 4 | 41 | 14 | 230 | 148 | WIDEN COL 3 (max 230 chars) by NARROWING COL 2 (avg 9 chars) |
| `appendices/F_survey_instrument_p566_w1285.tex:361` | `tab:survey_section_a` | 3 | 3 | 107 | 226 | WIDEN COL 3 (max 226 chars) by NARROWING COL 1 (avg 2 chars) | WIDTH GAP: widths [1.5, 4.7, 7.0] differ by > 8x; use equal-space strategy |
| `appendices/F_survey_instrument_p566_w1285.tex:920` | `tab:survey_section_f_xai` | 7 | 2 | 223 | 2 | 1 | 1 | 1 | 2 | REBALANCE: last column avg 1 chars vs largest 149; narrow last column to p{1.5cm} or merge it with previous | WIDEN COL 2 (max 223 chars) by NARROWING COL 4 (avg 1 chars) |
| `appendices/F_survey_instrument_p566_w1285.tex:1067` | `tab:survey_section_h_fusion` | 7 | 2 | 223 | 2 | 1 | 1 | 1 | 2 | REBALANCE: last column avg 1 chars vs largest 147; narrow last column to p{1.5cm} or merge it with previous | WIDEN COL 2 (max 223 chars) by NARROWING COL 4 (avg 1 chars) |
| `appendices/F_survey_instrument_p566_w1285.tex:1032` | `tab:survey_section_h_eeg` | 7 | 2 | 220 | 2 | 1 | 1 | 1 | 2 | REBALANCE: last column avg 1 chars vs largest 152; narrow last column to p{1.5cm} or merge it with previous | WIDEN COL 2 (max 220 chars) by NARROWING COL 4 (avg 1 chars) |
| `chapters/chapter2_literature.tex:1721` | `tab:synth_pipeline_automation` | 3 | 26 | 219 | 142 | WIDEN COL 2 (max 219 chars) by NARROWING COL 1 (avg 17 chars) | WIDTH GAP: widths [1.5, 7.1, 5.5] differ by > 8x; use equal-space strategy |

## Issue #5 — Tables that span 3+ pages (should be split into Part 1 / Part 2)

Count: **3** tables (> 50 rows — likely 3+ pages)

| File:Line | Label | Rows | Cols | Caption | Action |
|---|---|---:|---:|---|---|
| `chapters/chapter3_crossref_index.tex:15` | `tab:crossref_index_new` | 106 | 3 | Cross-Reference Index --- New Tables | SPLIT into Part 1 + Part 2 |
| `appendices/S_glossary.tex:11` | `tab:glossary_full` | 81 | 2 | Glossary of Acronyms and Key Terms | SPLIT into Part 1 + Part 2 |
| `appendices/I_brutal_feedback_p632_w64.tex:41` | `tab:brutal_appendices` | 55 | 10 | Per-Appendix Brutal Feedback | SPLIT into Part 1 + Part 2 |

## Issue #5b — Tables that span exactly 2 pages (acceptable, no action)

Count: **10**

## Issue #7 — Tables with WIDTH-IMBALANCE (column widths differ > 4x)

Count: **191** tables

| File:Line | Label | Cols | Widths (cm) | Rec |
|---|---|---:|---|---|
| `chapters/chapter3_research_methods.tex:7284` | `tab:master_rewrite_drafts` | 3 | 1.8 | 2.5 | 10.2 | WIDEN COL 3 (max 896 chars) by NARROWING COL 1 (avg 9 chars) | WIDTH GAP: widths [1.8, 2.5, 10.2] differ by > 8x; use equal-space strategy |
| `chapters/chapter1_introduction.tex:562` | `tab:ch1_object_scope` | 3 | 1.5 | 9.5 | 1.5 | REBALANCE: last column avg 6 chars vs largest 46; narrow last column to p{1.5cm} or merge it with previous | WIDTH GAP: widths [1.5, 9.5, 1.5] differ by > 8x; use equal-space strategy |
| `chapters/chapter1_introduction.tex:1709` | `tab:b2b_subproblems` | 3 | 1.5 | 1.5 | 9.5 | WIDEN COL 3 (max 130 chars) by NARROWING COL 1 (avg 5 chars) | WIDTH GAP: widths [1.5, 1.5, 9.5] differ by > 8x; use equal-space strategy |
| `chapters/chapter1_introduction.tex:1746` | `tab:b2c_subproblems` | 3 | 1.5 | 1.6 | 9.5 | WIDEN COL 3 (max 129 chars) by NARROWING COL 1 (avg 5 chars) | WIDTH GAP: widths [1.5, 1.6, 9.5] differ by > 8x; use equal-space strategy |
| `chapters/chapter1_introduction.tex:2693` | `tab:b2c_mobile_screens` | 4 | 1.5 | 1.5 | 9.5 | 1.5 | REBALANCE: last column avg 12 chars vs largest 118; narrow last column to p{1.5cm} or merge it with previous | WIDEN COL 3 (max 145 chars) by NARROWING COL 1 (avg 2 chars) | WIDTH GAP: widths [1.5, 1.5, 9.5, 1.5] differ by > 8x; use equal-space strategy |
| `chapters/chapter1_introduction.tex:3783` | `tab:main_objectives` | 3 | 1.5 | 9.5 | 1.5 | REBALANCE: last column avg 2 chars vs largest 84; narrow last column to p{1.5cm} or merge it with previous | WIDEN COL 2 (max 115 chars) by NARROWING COL 3 (avg 2 chars) | WIDTH GAP: widths [1.5, 9.5, 1.5] differ by > 8x; use equal-space strategy |
| `chapters/chapter1_introduction.tex:5303` | `tab:ch1_kit_objectives` | 3 | 2.2 | 9.5 | 1.5 | REBALANCE: last column avg 6 chars vs largest 76; narrow last column to p{1.5cm} or merge it with previous | WIDEN COL 2 (max 161 chars) by NARROWING COL 3 (avg 6 chars) | WIDTH GAP: widths [2.2, 9.5, 1.5] differ by > 8x; use equal-space strategy |
| `chapters/chapter3_arch_executive_summary.tex:17` | `tab:arch_exec_summary` | 3 | 1.7 | 9.5 | 1.5 | REBALANCE: last column avg 10 chars vs largest 91; narrow last column to p{1.5cm} or merge it with previous | WIDEN COL 2 (max 154 chars) by NARROWING COL 3 (avg 10 chars) | WIDTH GAP: widths [1.7, 9.5, 1.5] differ by > 8x; use equal-space strategy |
| `chapters/chapter3_companion_deliverables.tex:19` | `tab:companion_deliverables` | 3 | 1.5 | 9.5 | 1.5 | WIDEN COL 2 (max 256 chars) by NARROWING COL 3 (avg 24 chars) | WIDTH GAP: widths [1.5, 9.5, 1.5] differ by > 8x; use equal-space strategy |
| `chapters/chapter3_examiner_qa.tex:17` | `tab:examiner_qa_architecture` | 3 | 1.5 | 9.5 | 1.5 | WIDEN COL 3 (max 441 chars) by NARROWING COL 1 (avg 2 chars) | WIDTH GAP: widths [1.5, 9.5, 1.5] differ by > 8x; use equal-space strategy |
| `chapters/chapter3_research_methods.tex:401` | `tab:ch3_instrument_anchoring` | 3 | 1.5 | 9.5 | 1.5 | REBALANCE: last column avg 2 chars vs largest 108; narrow last column to p{1.5cm} or merge it with previous | WIDEN COL 2 (max 194 chars) by NARROWING COL 3 (avg 2 chars) | WIDTH GAP: widths [1.5, 9.5, 1.5] differ by > 8x; use equal-space strategy |
| `chapters/chapter3_research_methods.tex:1476` | `tab:primary_data_outcome_map` | 3 | 1.5 | 9.5 | 1.5 | REBALANCE: last column avg 5 chars vs largest 50; narrow last column to p{1.5cm} or merge it with previous | WIDTH GAP: widths [1.5, 9.5, 1.5] differ by > 8x; use equal-space strategy |
| `chapters/chapter3_research_methods.tex:4458` | `tab:scale_design` | 3 | 1.7 | 9.5 | 1.5 | REBALANCE: last column avg 4 chars vs largest 59; narrow last column to p{1.5cm} or merge it with previous | WIDTH GAP: widths [1.7, 9.5, 1.5] differ by > 8x; use equal-space strategy |
| `chapters/chapter3_thematic_xref.tex:19` | `tab:thematic_xref_matrix` | 2 | 9.5 | 1.5 | REBALANCE: last column avg 8 chars vs largest 33; narrow last column to p{1.5cm} or merge it with previous | WIDTH GAP: widths [9.5, 1.5] differ by > 8x; use equal-space strategy |
| `chapters/chapter4_analysis_findings.tex:533` | `tab:ch4_org_interpretation` | 3 | 1.5 | 1.5 | 9.5 | WIDEN COL 3 (max 255 chars) by NARROWING COL 1 (avg 2 chars) | WIDTH GAP: widths [1.5, 1.5, 9.5] differ by > 8x; use equal-space strategy |
| `chapters/chapter5_discussion_recommendations.tex:370` | `tab:ch5_managerial_implications` | 3 | 1.5 | 9.5 | 1.5 | WIDEN COL 2 (max 252 chars) by NARROWING COL 1 (avg 23 chars) | WIDTH GAP: widths [1.5, 9.5, 1.5] differ by > 8x; use equal-space strategy |
| `chapters/chapter5_discussion_recommendations.tex:4047` | `tab:ch5_final_verdict` | 3 | 1.5 | 1.5 | 9.5 | WIDEN COL 3 (max 244 chars) by NARROWING COL 2 (avg 6 chars) | WIDTH GAP: widths [1.5, 1.5, 9.5] differ by > 8x; use equal-space strategy |
| `appendices/C_ch3_supp_p267_w1470.tex:1027` | `tab:eeg_workflow_governance` | 3 | 1.5 | 9.5 | 1.5 | REBALANCE: last column avg 5 chars vs largest 88; narrow last column to p{1.5cm} or merge it with previous | WIDEN COL 2 (max 128 chars) by NARROWING COL 3 (avg 5 chars) | WIDTH GAP: widths [1.5, 9.5, 1.5] differ by > 8x; use equal-space strategy |
| `appendices/D_ch4_supp_p390_w814.tex:317` | `tab:eval_explain_trust` | 3 | 2.1 | 9.5 | 1.5 | REBALANCE: last column avg 5 chars vs largest 88; narrow last column to p{1.5cm} or merge it with previous | WIDEN COL 2 (max 116 chars) by NARROWING COL 3 (avg 5 chars) | WIDTH GAP: widths [2.1, 9.5, 1.5] differ by > 8x; use equal-space strategy |
| `appendices/D_ch4_supp_p390_w814.tex:1090` | `tab:expert_comments` | 3 | 1.5 | 1.5 | 9.5 | WIDEN COL 3 (max 146 chars) by NARROWING COL 2 (avg 11 chars) | WIDTH GAP: widths [1.5, 1.5, 9.5] differ by > 8x; use equal-space strategy |
| `appendices/D_supp_tables_p390_w17.tex:205` | `tab:eeg_frequency_bands` | 4 | 1.5 | 1.5 | 1.5 | 9.5 | WIDEN COL 4 (max 211 chars) by NARROWING COL 2 (avg 6 chars) | WIDTH GAP: widths [1.5, 1.5, 1.5, 9.5] differ by > 8x; use equal-space strategy |
| `appendices/E_ch5_supp_p525_w1059.tex:49` | `tab:dash_research_ui_map` | 3 | 1.7 | 9.5 | 1.5 | REBALANCE: last column avg 6 chars vs largest 94; narrow last column to p{1.5cm} or merge it with previous | WIDEN COL 2 (max 126 chars) by NARROWING COL 3 (avg 6 chars) | WIDTH GAP: widths [1.7, 9.5, 1.5] differ by > 8x; use equal-space strategy |
| `appendices/F_survey_instrument_p566_w1285.tex:1126` | `tab:survey_b2c_primary_addendum` | 3 | 1.5 | 9.5 | 1.5 | REBALANCE: last column avg 11 chars vs largest 85; narrow last column to p{1.5cm} or merge it with previous | WIDEN COL 2 (max 140 chars) by NARROWING COL 1 (avg 4 chars) | WIDTH GAP: widths [1.5, 9.5, 1.5] differ by > 8x; use equal-space strategy |
| `appendices/H_rgaig_architecture_p605_w1135.tex:39` | `tab:appo_tech_research_map` | 3 | 1.8 | 9.5 | 1.5 | REBALANCE: last column avg 5 chars vs largest 80; narrow last column to p{1.5cm} or merge it with previous | WIDEN COL 2 (max 105 chars) by NARROWING COL 3 (avg 5 chars) | WIDTH GAP: widths [1.8, 9.5, 1.5] differ by > 8x; use equal-space strategy |
| `appendices/H_rgaig_architecture_p605_w1135.tex:302` | `tab:appo_maturity_arch` | 3 | 1.5 | 1.5 | 9.5 | WIDEN COL 3 (max 127 chars) by NARROWING COL 1 (avg 1 chars) | WIDTH GAP: widths [1.5, 1.5, 9.5] differ by > 8x; use equal-space strategy |
| `appendices/H_rgaig_architecture_p605_w1135.tex:335` | `tab:appo_gov_dimensions` | 3 | 1.8 | 9.5 | 1.5 | REBALANCE: last column avg 5 chars vs largest 62; narrow last column to p{1.5cm} or merge it with previous | WIDTH GAP: widths [1.8, 9.5, 1.5] differ by > 8x; use equal-space strategy |
| `appendices/M_operationalization_detail_p725.tex:502` | `tab:research_objectives` | 3 | 1.5 | 9.5 | 1.5 | REBALANCE: last column avg 6 chars vs largest 69; narrow last column to p{1.5cm} or merge it with previous | WIDTH GAP: widths [1.5, 9.5, 1.5] differ by > 8x; use equal-space strategy |
| `appendices/M_operationalization_detail_p725.tex:677` | `tab:rq_mapping` | 3 | 1.5 | 9.5 | 1.5 | REBALANCE: last column avg 4 chars vs largest 108; narrow last column to p{1.5cm} or merge it with previous | WIDEN COL 2 (max 167 chars) by NARROWING COL 1 (avg 3 chars) | WIDTH GAP: widths [1.5, 9.5, 1.5] differ by > 8x; use equal-space strategy |
| `appendices/N_indian_cohort_acquisition_p1090.tex:170` | `tab:appendix_n_compliance` | 3 | 2.1 | 1.5 | 9.5 | WIDEN COL 3 (max 130 chars) by NARROWING COL 2 (avg 7 chars) | WIDTH GAP: widths [2.1, 1.5, 9.5] differ by > 8x; use equal-space strategy |
| `appendices/Q_drill_methodology.tex:55` | `tab:app_q_drill_anatomy` | 3 | 1.5 | 2.1 | 9.5 | WIDEN COL 3 (max 120 chars) by NARROWING COL 1 (avg 1 chars) | WIDTH GAP: widths [1.5, 2.1, 9.5] differ by > 8x; use equal-space strategy |
| `appendices/H_rgaig_architecture_p605_w1135.tex:464` | `tab:appo_principles` | 3 | 1.5 | 2.3 | 9.4 | WIDEN COL 3 (max 171 chars) by NARROWING COL 1 (avg 5 chars) | WIDTH GAP: widths [1.5, 2.3, 9.4] differ by > 8x; use equal-space strategy |
| `appendices/K_b2b_operational_governance_triad_p695.tex:441` | `tab:appk_triad_failure_modes` | 4 | 1.7 | 1.5 | 1.5 | 9.4 | WIDEN COL 4 (max 107 chars) by NARROWING COL 3 (avg 7 chars) | WIDTH GAP: widths [1.7, 1.5, 1.5, 9.4] differ by > 8x; use equal-space strategy |
| `chapters/chapter2_literature.tex:2480` | `tab:lit_synthesis_consolidated` | 3 | 1.5 | 9.3 | 3.0 | WIDEN COL 2 (max 143 chars) by NARROWING COL 1 (avg 16 chars) | WIDTH GAP: widths [1.5, 9.3, 3.0] differ by > 8x; use equal-space strategy |
| `chapters/chapter3_research_methods.tex:468` | `tab:ch3_bias_mitigation` | 3 | 1.5 | 9.3 | 2.7 | WIDEN COL 2 (max 107 chars) by NARROWING COL 1 (avg 15 chars) | WIDTH GAP: widths [1.5, 9.3, 2.7] differ by > 8x; use equal-space strategy |
| `appendices/J_human_centered_ecosystem_p680.tex:163` | `tab:appj_accessibility` | 3 | 1.8 | 9.3 | 2.1 | REBALANCE: last column avg 14 chars vs largest 63; narrow last column to p{1.5cm} or merge it with previous | WIDTH GAP: widths [1.8, 9.3, 2.1] differ by > 8x; use equal-space strategy |
| `chapters/chapter3_research_methods.tex:1170` | `tab:asd_23step_expanded` | 4 | 1.5 | 1.5 | 9.2 | 1.5 | WIDEN COL 3 (max 311 chars) by NARROWING COL 1 (avg 2 chars) | WIDTH GAP: widths [1.5, 1.5, 9.2, 1.5] differ by > 8x; use equal-space strategy |
| `chapters/chapter1_introduction.tex:958` | `tab:significance` | 3 | 1.5 | 9.0 | 3.8 | WIDEN COL 2 (max 163 chars) by NARROWING COL 1 (avg 8 chars) | WIDTH GAP: widths [1.5, 9.0, 3.8] differ by > 8x; use equal-space strategy |
| `chapters/chapter1_introduction.tex:4213` | `tab:measurement_errors` | 3 | 1.5 | 3.3 | 9.0 | WIDEN COL 3 (max 169 chars) by NARROWING COL 1 (avg 17 chars) | WIDTH GAP: widths [1.5, 3.3, 9.0] differ by > 8x; use equal-space strategy |
| `chapters/chapter1_introduction.tex:4554` | `tab:domain_role_hierarchy` | 4 | 1.5 | 1.5 | 1.5 | 9.0 | WIDEN COL 4 (max 114 chars) by NARROWING COL 1 (avg 4 chars) | WIDTH GAP: widths [1.5, 1.5, 1.5, 9.0] differ by > 8x; use equal-space strategy |
| `appendices/J_human_centered_ecosystem_p680.tex:453` | `tab:appj_value` | 3 | 1.7 | 9.0 | 2.5 | REBALANCE: last column avg 14 chars vs largest 50; narrow last column to p{1.5cm} or merge it with previous | WIDTH GAP: widths [1.7, 9.0, 2.5] differ by > 8x; use equal-space strategy |

## Build-Log Overflows (vbox bottom + hbox horizontal)

- **vbox bottom-overflows**: 7 pages with content past page-bottom

| Severity (pt too high) | Action |
|---:|---|
| 688.7 | reduce table size, add \clearpage, or \resizebox |
| 516.9 | reduce table size, add \clearpage, or \resizebox |
| 295.0 | reduce table size, add \clearpage, or \resizebox |
| 155.1 | reduce table size, add \clearpage, or \resizebox |
| 116.2 | reduce table size, add \clearpage, or \resizebox |
| 86.5 | reduce table size, add \clearpage, or \resizebox |
| 76.5 | reduce table size, add \clearpage, or \resizebox |

- **hbox horizontal-overflows**: 1528 cells exceed text-width

