# Advanced Table Quality Audit

Generated: 2026-05-30T00:37:07.038738

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
- **Build-log hbox horizontal-overflows**: 1231
- **empty_cells**: 71 tables
- **right_side_empty**: 54 tables
- **width_imbalanced**: 32 tables
- **tall_column**: 25 tables
- **multi_page**: 13 tables
- **sparse_table**: 4 tables
- **very_multi_page**: 3 tables
- **placeholders**: 1 tables

## Issue #3 — Tables with RIGHT-SIDE EMPTY (last column nearly empty)

Count: **54** tables

| File:Line | Label | Cols | Col avg text lengths | Rec |
|---|---|---:|---|---|
| `chapters/chapter1_introduction.tex:562` | `tab:ch1_object_scope` | 3 | 2 | 46 | 11 | REBALANCE: last column avg 11 chars vs largest 46; narrow last column to p{1.5cm} or merge it with previous | WIDTH GAP: widths [1.0, 8.1, 4.1] differ by > 8x; use equal-space strategy |
| `chapters/chapter1_introduction.tex:620` | `tab:ch1_task_map` | 4 | 2 | 36 | 4 | 9 | REBALANCE: last column avg 9 chars vs largest 36; narrow last column to p{1.5cm} or merge it with previous | WIDTH GAP: widths [1.0, 7.1, 1.0, 3.5] differ by > 8x; use equal-space strategy |
| `chapters/chapter1_introduction.tex:2158` | `NOLABEL@chapters/chapter1_introduction.tex:2158` | 4 | 1 | 14 | 87 | 12 | REBALANCE: last column avg 12 chars vs largest 87; narrow last column to p{1.5cm} or merge it with previous |
| `chapters/chapter1_introduction.tex:2693` | `tab:b2c_mobile_screens` | 4 | 2 | 14 | 118 | 12 | REBALANCE: last column avg 12 chars vs largest 118; narrow last column to p{1.5cm} or merge it with previous | WIDTH GAP: widths [1.0, 2.4, 7.0, 2.2] differ by > 8x; use equal-space strategy |
| `chapters/chapter1_introduction.tex:2757` | `tab:b2c_user_forms` | 4 | 2 | 16 | 94 | 10 | REBALANCE: last column avg 10 chars vs largest 93; narrow last column to p{1.5cm} or merge it with previous |
| `chapters/chapter1_introduction.tex:2944` | `tab:report_types` | 4 | 2 | 15 | 88 | 9 | REBALANCE: last column avg 9 chars vs largest 88; narrow last column to p{1.5cm} or merge it with previous |
| `chapters/chapter1_introduction.tex:3094` | `tab:continuous_monitoring` | 4 | 2 | 14 | 105 | 10 | REBALANCE: last column avg 9 chars vs largest 105; narrow last column to p{1.5cm} or merge it with previous |
| `chapters/chapter1_introduction.tex:3357` | `tab:backend_db` | 4 | 2 | 1 | 99 | 10 | REBALANCE: last column avg 10 chars vs largest 99; narrow last column to p{1.5cm} or merge it with previous | WIDTH GAP: widths [1.0, 1.0, 8.1, 2.5] differ by > 8x; use equal-space strategy |
| `chapters/chapter1_introduction.tex:5173` | `tab:ch1_scorecard` | 3 | 16 | 31 | 5 | REBALANCE: last column avg 5 chars vs largest 31; narrow last column to p{1.5cm} or merge it with previous |
| `chapters/chapter2_literature.tex:1068` | `NOLABEL@chapters/chapter2_literature.tex:1068` | 5 | 8 | 105 | 0 | 0 | 0 | REBALANCE: last column avg 0 chars vs largest 105; narrow last column to p{1.5cm} or merge it with previous | WIDEN COL 2 (max 105 chars) by NARROWING COL 1 (avg 8 chars) |
| `chapters/chapter2_literature.tex:1401` | `NOLABEL@chapters/chapter2_literature.tex:1401` | 4 | 3 | 31 | 16 | 0 | REBALANCE: last column avg 0 chars vs largest 31; narrow last column to p{1.5cm} or merge it with previous |
| `chapters/chapter2_literature.tex:1469` | `NOLABEL@chapters/chapter2_literature.tex:1469` | 3 | 19 | 197 | 0 | REBALANCE: last column avg 0 chars vs largest 197; narrow last column to p{1.5cm} or merge it with previous | WIDEN COL 2 (max 197 chars) by NARROWING COL 1 (avg 19 chars) |
| `chapters/chapter2_literature.tex:2626` | `tab:ch2_scorecard` | 3 | 17 | 32 | 6 | REBALANCE: last column avg 6 chars vs largest 32; narrow last column to p{1.5cm} or merge it with previous |
| `chapters/chapter3_arch_executive_summary.tex:17` | `tab:arch_exec_summary` | 3 | 23 | 91 | 14 | REBALANCE: last column avg 14 chars vs largest 91; narrow last column to p{1.5cm} or merge it with previous |
| `chapters/chapter3_defence_prep_checklist.tex:18` | `tab:defence_prep_arch_checklist` | 4 | 2 | 48 | 4 | 13 | REBALANCE: last column avg 13 chars vs largest 48; narrow last column to p{1.5cm} or merge it with previous | WIDTH GAP: widths [1.0, 7.0, 1.0, 3.6] differ by > 8x; use equal-space strategy |
| `chapters/chapter3_research_methods.tex:92` | `NOLABEL@chapters/chapter3_research_methods.tex:92` | 2 | 43 | 13 | REBALANCE: last column avg 13 chars vs largest 43; narrow last column to p{1.5cm} or merge it with previous |
| `chapters/chapter3_research_methods.tex:533` | `tab:ch3_statistical_plan` | 4 | 1 | 18 | 69 | 8 | REBALANCE: last column avg 8 chars vs largest 69; narrow last column to p{1.5cm} or merge it with previous |
| `chapters/chapter3_research_methods.tex:1476` | `tab:primary_data_outcome_map` | 3 | 6 | 50 | 7 | REBALANCE: last column avg 7 chars vs largest 50; narrow last column to p{1.5cm} or merge it with previous |
| `chapters/chapter3_research_methods.tex:1983` | `tab:primary_flow` | 4 | 2 | 16 | 66 | 14 | REBALANCE: last column avg 14 chars vs largest 66; narrow last column to p{1.5cm} or merge it with previous |
| `chapters/chapter3_research_methods.tex:3566` | `tab:customer_smart_flow` | 4 | 1 | 23 | 46 | 17 | REBALANCE: last column avg 17 chars vs largest 46; narrow last column to p{1.5cm} or merge it with previous |
| `chapters/chapter3_research_methods.tex:9208` | `NOLABEL@chapters/chapter3_research_methods.tex:9208` | 5 | 2 | 45 | 44 | 20 | 10 | REBALANCE: last column avg 10 chars vs largest 45; narrow last column to p{1.5cm} or merge it with previous |
| `chapters/chapter3_research_methods.tex:10899` | `NOLABEL@chapters/chapter3_research_methods.tex:10899` | 4 | 17 | 48 | 26 | 16 | REBALANCE: last column avg 16 chars vs largest 48; narrow last column to p{1.5cm} or merge it with previous |
| `chapters/chapter3_research_methods.tex:11490` | `NOLABEL@chapters/chapter3_research_methods.tex:11490` | 3 | 11 | 125 | 13 | REBALANCE: last column avg 13 chars vs largest 125; narrow last column to p{1.5cm} or merge it with previous |
| `chapters/chapter3_research_methods.tex:11513` | `NOLABEL@chapters/chapter3_research_methods.tex:11513` | 3 | 2 | 84 | 9 | REBALANCE: last column avg 9 chars vs largest 84; narrow last column to p{1.5cm} or merge it with previous |
| `chapters/chapter3_research_methods.tex:11549` | `NOLABEL@chapters/chapter3_research_methods.tex:11549` | 4 | 4 | 54 | 10 | 7 | REBALANCE: last column avg 7 chars vs largest 54; narrow last column to p{1.5cm} or merge it with previous |
| `chapters/chapter4_analysis_findings.tex:774` | `tab:ch4_hybrid_findings_summary` | 4 | 3 | 62 | 100 | 16 | REBALANCE: last column avg 16 chars vs largest 100; narrow last column to p{1.5cm} or merge it with previous |
| `chapters/chapter4_analysis_findings.tex:922` | `tab:ch4_alignment` | 4 | 3 | 2 | 46 | 12 | REBALANCE: last column avg 12 chars vs largest 46; narrow last column to p{1.5cm} or merge it with previous | WIDTH GAP: widths [1.0, 1.0, 7.0, 3.6] differ by > 8x; use equal-space strategy |
| `chapters/chapter4_analysis_findings.tex:1582` | `NOLABEL@chapters/chapter4_analysis_findings.tex:1582` | 5 | 12 | 33 | 18 | 32 | 6 | REBALANCE: last column avg 6 chars vs largest 33; narrow last column to p{1.5cm} or merge it with previous |
| `chapters/chapter4_analysis_findings.tex:3909` | `NOLABEL@chapters/chapter4_analysis_findings.tex:3909` | 4 | 3 | 15 | 49 | 18 | REBALANCE: last column avg 18 chars vs largest 49; narrow last column to p{1.5cm} or merge it with previous |
| `chapters/chapter4_analysis_findings.tex:3931` | `NOLABEL@chapters/chapter4_analysis_findings.tex:3931` | 4 | 2 | 38 | 8 | 13 | REBALANCE: last column avg 13 chars vs largest 38; narrow last column to p{1.5cm} or merge it with previous |
| `chapters/chapter5_discussion_recommendations.tex:3217` | `NOLABEL@chapters/chapter5_discussion_recommendations.tex:3217` | 4 | 2 | 13 | 66 | 13 | REBALANCE: last column avg 13 chars vs largest 66; narrow last column to p{1.5cm} or merge it with previous |
| `chapters/chapter5_discussion_recommendations.tex:3271` | `NOLABEL@chapters/chapter5_discussion_recommendations.tex:3271` | 5 | 1 | 10 | 59 | 73 | 10 | REBALANCE: last column avg 10 chars vs largest 73; narrow last column to p{1.5cm} or merge it with previous |
| `chapters/chapter5_discussion_recommendations.tex:3460` | `NOLABEL@chapters/chapter5_discussion_recommendations.tex:3460` | 5 | 1 | 18 | 45 | 20 | 18 | REBALANCE: last column avg 18 chars vs largest 45; narrow last column to p{1.5cm} or merge it with previous |
| `chapters/chapter5_discussion_recommendations.tex:4716` | `NOLABEL@chapters/chapter5_discussion_recommendations.tex:4716` | 8 | 2 | 16 | 1 | 1 | 2 | 41 | 7 | 1 | REBALANCE: last column avg 1 chars vs largest 41; narrow last column to p{1.5cm} or merge it with previous |
| `appendices/C_ch3_supp_p267_w1470.tex:533` | `tab:mcp_tools` | 4 | 5 | 1 | 40 | 11 | REBALANCE: last column avg 11 chars vs largest 40; narrow last column to p{1.5cm} or merge it with previous | WIDTH GAP: widths [1.0, 1.0, 7.0, 3.6] differ by > 8x; use equal-space strategy |
| `appendices/C_ch3_supp_p267_w1470.tex:1061` | `tab:eeg_existing_failures` | 3 | 20 | 64 | 20 | REBALANCE: last column avg 20 chars vs largest 64; narrow last column to p{1.5cm} or merge it with previous |
| `appendices/C_ch3_supp_p267_w1470.tex:2233` | `tab:thesis_objective_alignment` | 7 | 36 | 11 | 14 | 14 | 13 | 16 | 8 | REBALANCE: last column avg 8 chars vs largest 37; narrow last column to p{1.5cm} or merge it with previous |
| `appendices/C_ch3_supp_p267_w1470.tex:3228` | `NOLABEL@appendices/C_ch3_supp_p267_w1470.tex:3228` | 5 | 1 | 20 | 20 | 46 | 10 | REBALANCE: last column avg 10 chars vs largest 46; narrow last column to p{1.5cm} or merge it with previous |
| `appendices/D_ch4_supp_p390_w814.tex:1345` | `tab:ch4_alignment` | 4 | 3 | 2 | 40 | 7 | REBALANCE: last column avg 7 chars vs largest 40; narrow last column to p{1.5cm} or merge it with previous |
| `appendices/E_ch5_supp_p525_w1059.tex:101` | `tab:dash_workflow_visual_purpose` | 3 | 17 | 61 | 18 | REBALANCE: last column avg 18 chars vs largest 61; narrow last column to p{1.5cm} or merge it with previous |

## Issue #4 — Tables with TALL-COLUMN (one column has 3+ rows of text)

Count: **25** tables

| File:Line | Label | Cols | Col max text | Rec |
|---|---|---:|---|---|
| `chapters/chapter3_examiner_qa.tex:17` | `tab:examiner_qa_architecture` | 3 | 3 | 437 | 441 | WIDEN COL 3 (max 441 chars) by NARROWING COL 1 (avg 2 chars) | WIDTH GAP: widths [1.0, 8.6, 3.6] differ by > 8x; use equal-space strategy |
| `appendices/D_ch4_supp_p390_w814.tex:117` | `tab:appd_mediation_detail` | 7 | 338 | 23 | 4 | 4 | 4 | 1 | 46 | WIDEN COL 1 (max 338 chars) by NARROWING COL 6 (avg 1 chars) |
| `chapters/chapter3_research_methods.tex:10042` | `NOLABEL@chapters/chapter3_research_methods.tex:10042` | 6 | 6 | 333 | 0 | 0 | 0 | 0 | WIDEN COL 2 (max 333 chars) by NARROWING COL 1 (avg 6 chars) |
| `chapters/chapter1_introduction.tex:4488` | `tab:tam_toe_rbv` | 5 | 6 | 321 | 96 | 120 | 136 | WIDEN COL 2 (max 321 chars) by NARROWING COL 1 (avg 3 chars) |
| `chapters/chapter3_research_methods.tex:5307` | `tab:remaining_ai_capability_matrix` | 6 | 33 | 276 | 236 | 236 | 191 | 242 | WIDEN COL 2 (max 276 chars) by NARROWING COL 1 (avg 15 chars) |
| `appendices/F_survey_instrument_p566_w1285.tex:770` | `tab:survey_section_e_diag` | 7 | 2 | 207 | 192 | 1 | 1 | 1 | 2 | WIDEN COL 2 (max 207 chars) by NARROWING COL 4 (avg 1 chars) |
| `appendices/L_technical_ops_p685.tex:460` | `NOLABEL@appendices/L_technical_ops_p685.tex:460` | 5 | 2 | 23 | 193 | 26 | 201 | WIDEN COL 5 (max 201 chars) by NARROWING COL 1 (avg 1 chars) |
| `chapters/chapter2_literature.tex:1469` | `NOLABEL@chapters/chapter2_literature.tex:1469` | 3 | 19 | 197 | 0 | REBALANCE: last column avg 0 chars vs largest 197; narrow last column to p{1.5cm} or merge it with previous | WIDEN COL 2 (max 197 chars) by NARROWING COL 1 (avg 19 chars) |
| `appendices/F_survey_instrument_p566_w1285.tex:737` | `tab:survey_section_d_reg` | 7 | 3 | 195 | 167 | 1 | 1 | 1 | 2 | WIDEN COL 2 (max 195 chars) by NARROWING COL 4 (avg 1 chars) |
| `appendices/F_survey_instrument_p566_w1285.tex:632` | `tab:survey_section_d_algo` | 7 | 2 | 170 | 191 | 1 | 1 | 1 | 2 | WIDEN COL 3 (max 191 chars) by NARROWING COL 4 (avg 1 chars) |
| `chapters/chapter5_discussion_recommendations.tex:3615` | `tab:consent_protocol` | 5 | 2 | 34 | 169 | 22 | 183 | WIDEN COL 5 (max 183 chars) by NARROWING COL 1 (avg 1 chars) |
| `chapters/chapter3_research_methods.tex:2733` | `tab:research_anatomy` | 6 | 3 | 182 | 99 | 100 | 148 | 116 | WIDEN COL 2 (max 182 chars) by NARROWING COL 1 (avg 2 chars) |
| `chapters/chapter2_literature.tex:1008` | `NOLABEL@chapters/chapter2_literature.tex:1008` | 5 | 14 | 22 | 175 | 4 | 92 | WIDEN COL 3 (max 175 chars) by NARROWING COL 4 (avg 4 chars) |
| `chapters/chapter1_introduction.tex:3965` | `tab:doctoral_quality_chain` | 5 | 2 | 171 | 73 | 82 | 34 | WIDEN COL 2 (max 171 chars) by NARROWING COL 1 (avg 1 chars) |
| `chapters/chapter3_research_methods.tex:2775` | `tab:primary_iv_dv_framework` | 5 | 3 | 75 | 106 | 150 | 147 | WIDEN COL 4 (max 150 chars) by NARROWING COL 1 (avg 2 chars) |
| `chapters/chapter3_research_methods.tex:11462` | `NOLABEL@chapters/chapter3_research_methods.tex:11462` | 3 | 26 | 138 | 87 | WIDEN COL 2 (max 138 chars) by NARROWING COL 1 (avg 19 chars) |
| `appendices/C_ch3_supp_p267_w1470.tex:216` | `tab:app_gan_model_params` | 4 | 20 | 10 | 136 | 111 | WIDEN COL 3 (max 136 chars) by NARROWING COL 2 (avg 9 chars) |
| `appendices/C_ch3_supp_p267_w1470.tex:2935` | `NOLABEL@appendices/C_ch3_supp_p267_w1470.tex:2935` | 4 | 20 | 10 | 136 | 111 | WIDEN COL 3 (max 136 chars) by NARROWING COL 2 (avg 9 chars) |
| `chapters/chapter3_research_methods.tex:11349` | `NOLABEL@chapters/chapter3_research_methods.tex:11349` | 4 | 2 | 104 | 128 | 84 | WIDEN COL 3 (max 128 chars) by NARROWING COL 1 (avg 2 chars) |
| `chapters/chapter4_analysis_findings.tex:500` | `tab:ch4_triangulation` | 4 | 19 | 38 | 111 | 120 | WIDEN COL 4 (max 120 chars) by NARROWING COL 1 (avg 14 chars) |
| `appendices/M_operationalization_detail_p725.tex:635` | `tab:smart_objectives` | 6 | 3 | 119 | 87 | 61 | 60 | 25 | WIDEN COL 2 (max 119 chars) by NARROWING COL 1 (avg 2 chars) |
| `chapters/chapter5_discussion_recommendations.tex:6815` | `tab:ch5_per_chapter_data_summary` | 5 | 3 | 85 | 102 | 112 | 44 | WIDEN COL 4 (max 112 chars) by NARROWING COL 1 (avg 1 chars) |
| `chapters/chapter3_microservice_ipo.tex:17` | `tab:microservice_ipo_contract` | 5 | 14 | 82 | 104 | 111 | 92 | WIDEN COL 4 (max 111 chars) by NARROWING COL 1 (avg 8 chars) |
| `chapters/chapter3_research_methods.tex:2888` | `tab:ethics_consent_anchor` | 5 | 5 | 110 | 93 | 99 | 94 | WIDEN COL 2 (max 110 chars) by NARROWING COL 1 (avg 2 chars) |
| `chapters/chapter2_literature.tex:1068` | `NOLABEL@chapters/chapter2_literature.tex:1068` | 5 | 8 | 105 | 0 | 0 | 0 | REBALANCE: last column avg 0 chars vs largest 105; narrow last column to p{1.5cm} or merge it with previous | WIDEN COL 2 (max 105 chars) by NARROWING COL 1 (avg 8 chars) |

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

Count: **32** tables

| File:Line | Label | Cols | Widths (cm) | Rec |
|---|---|---:|---|---|
| `chapters/chapter3_research_methods.tex:7284` | `tab:master_rewrite_drafts` | 3 | 1.8 | 2.5 | 10.2 | WIDTH GAP: widths [1.8, 2.5, 10.2] differ by > 8x; use equal-space strategy |
| `chapters/chapter1_introduction.tex:3783` | `tab:main_objectives` | 3 | 1.0 | 9.5 | 1.0 | WIDTH GAP: widths [1.0, 9.5, 1.0] differ by > 8x; use equal-space strategy |
| `chapters/chapter3_research_methods.tex:3259` | `tab:b2c_research_gap_catalog` | 4 | 1.0 | 9.5 | 1.0 | 1.0 | WIDTH GAP: widths [1.0, 9.5, 1.0, 1.0] differ by > 8x; use equal-space strategy |
| `appendices/M_operationalization_detail_p725.tex:426` | `tab:part_objectives` | 4 | 1.0 | 9.5 | 1.0 | 1.0 | WIDTH GAP: widths [1.0, 9.5, 1.0, 1.0] differ by > 8x; use equal-space strategy |
| `appendices/M_operationalization_detail_p725.tex:502` | `tab:research_objectives` | 3 | 1.0 | 9.5 | 2.7 | REBALANCE: last column avg 6 chars vs largest 69; narrow last column to p{1.5cm} or merge it with previous | WIDTH GAP: widths [1.0, 9.5, 2.7] differ by > 8x; use equal-space strategy |
| `appendices/M_operationalization_detail_p725.tex:677` | `tab:rq_mapping` | 3 | 1.0 | 9.5 | 1.0 | WIDTH GAP: widths [1.0, 9.5, 1.0] differ by > 8x; use equal-space strategy |
| `appendices/H_rgaig_architecture_p605_w1135.tex:302` | `tab:appo_maturity_arch` | 3 | 1.0 | 3.0 | 9.2 | WIDTH GAP: widths [1.0, 3.0, 9.2] differ by > 8x; use equal-space strategy |
| `appendices/F_survey_instrument_p566_w1285.tex:1126` | `tab:survey_b2c_primary_addendum` | 3 | 1.0 | 9.0 | 3.2 | REBALANCE: last column avg 11 chars vs largest 85; narrow last column to p{1.5cm} or merge it with previous | WIDTH GAP: widths [1.0, 9.0, 3.2] differ by > 8x; use equal-space strategy |
| `chapters/chapter3_examiner_qa.tex:17` | `tab:examiner_qa_architecture` | 3 | 1.0 | 8.6 | 3.6 | WIDEN COL 3 (max 441 chars) by NARROWING COL 1 (avg 2 chars) | WIDTH GAP: widths [1.0, 8.6, 3.6] differ by > 8x; use equal-space strategy |
| `chapters/chapter3_research_methods.tex:4458` | `tab:scale_design` | 3 | 3.6 | 8.6 | 1.0 | WIDTH GAP: widths [3.6, 8.6, 1.0] differ by > 8x; use equal-space strategy |
| `chapters/chapter4_analysis_findings.tex:533` | `tab:ch4_org_interpretation` | 3 | 1.0 | 3.7 | 8.5 | WIDTH GAP: widths [1.0, 3.7, 8.5] differ by > 8x; use equal-space strategy |
| `appendices/H_rgaig_architecture_p605_w1135.tex:335` | `tab:appo_gov_dimensions` | 3 | 3.7 | 8.5 | 1.0 | WIDTH GAP: widths [3.7, 8.5, 1.0] differ by > 8x; use equal-space strategy |
| `chapters/chapter5_discussion_recommendations.tex:4047` | `tab:ch5_final_verdict` | 3 | 2.8 | 2.0 | 8.4 | WIDTH GAP: widths [2.8, 2.0, 8.4] differ by > 8x; use equal-space strategy |
| `chapters/chapter1_introduction.tex:1709` | `tab:b2b_subproblems` | 3 | 1.0 | 3.9 | 8.3 | WIDTH GAP: widths [1.0, 3.9, 8.3] differ by > 8x; use equal-space strategy |
| `chapters/chapter3_research_methods.tex:401` | `tab:ch3_instrument_anchoring` | 3 | 3.9 | 8.3 | 1.0 | WIDTH GAP: widths [3.9, 8.3, 1.0] differ by > 8x; use equal-space strategy |
| `chapters/chapter1_introduction.tex:1746` | `tab:b2c_subproblems` | 3 | 1.0 | 4.0 | 8.2 | WIDTH GAP: widths [1.0, 4.0, 8.2] differ by > 8x; use equal-space strategy |
| `chapters/chapter1_introduction.tex:562` | `tab:ch1_object_scope` | 3 | 1.0 | 8.1 | 4.1 | REBALANCE: last column avg 11 chars vs largest 46; narrow last column to p{1.5cm} or merge it with previous | WIDTH GAP: widths [1.0, 8.1, 4.1] differ by > 8x; use equal-space strategy |
| `chapters/chapter1_introduction.tex:3357` | `tab:backend_db` | 4 | 1.0 | 1.0 | 8.1 | 2.5 | REBALANCE: last column avg 10 chars vs largest 99; narrow last column to p{1.5cm} or merge it with previous | WIDTH GAP: widths [1.0, 1.0, 8.1, 2.5] differ by > 8x; use equal-space strategy |
| `appendices/C_ch3_supp_p267_w1470.tex:1475` | `NOLABEL@appendices/C_ch3_supp_p267_w1470.tex:1475` | 3 | 1.6 | 4.6 | 8.0 | WIDTH GAP: widths [1.6, 4.6, 8.0] differ by > 8x; use equal-space strategy |
| `appendices/H_rgaig_architecture_p605_w1135.tex:39` | `tab:appo_tech_research_map` | 3 | 4.2 | 8.0 | 1.0 | WIDTH GAP: widths [4.2, 8.0, 1.0] differ by > 8x; use equal-space strategy |
| `appendices/D_ch4_supp_p390_w814.tex:317` | `tab:eval_explain_trust` | 3 | 4.4 | 7.8 | 1.0 | WIDTH GAP: widths [4.4, 7.8, 1.0] differ by > 8x; use equal-space strategy |
| `appendices/Q_drill_methodology.tex:55` | `tab:app_q_drill_anatomy` | 3 | 1.0 | 4.4 | 7.8 | WIDTH GAP: widths [1.0, 4.4, 7.8] differ by > 8x; use equal-space strategy |
| `appendices/F_survey_instrument_p566_w1285.tex:981` | `tab:survey_section_g` | 3 | 1.0 | 7.7 | 4.5 | WIDTH GAP: widths [1.0, 7.7, 4.5] differ by > 8x; use equal-space strategy |
| `appendices/H_rgaig_architecture_p605_w1135.tex:464` | `tab:appo_principles` | 3 | 1.0 | 4.6 | 7.6 | WIDTH GAP: widths [1.0, 4.6, 7.6] differ by > 8x; use equal-space strategy |
| `chapters/chapter3_research_methods.tex:3436` | `tab:b2b_research_gap_catalog` | 4 | 1.0 | 7.2 | 3.4 | 1.0 | WIDTH GAP: widths [1.0, 7.2, 3.4, 1.0] differ by > 8x; use equal-space strategy |
| `chapters/chapter1_introduction.tex:620` | `tab:ch1_task_map` | 4 | 1.0 | 7.1 | 1.0 | 3.5 | REBALANCE: last column avg 9 chars vs largest 36; narrow last column to p{1.5cm} or merge it with previous | WIDTH GAP: widths [1.0, 7.1, 1.0, 3.5] differ by > 8x; use equal-space strategy |
| `chapters/chapter1_introduction.tex:2693` | `tab:b2c_mobile_screens` | 4 | 1.0 | 2.4 | 7.0 | 2.2 | REBALANCE: last column avg 12 chars vs largest 118; narrow last column to p{1.5cm} or merge it with previous | WIDTH GAP: widths [1.0, 2.4, 7.0, 2.2] differ by > 8x; use equal-space strategy |
| `chapters/chapter1_introduction.tex:3316` | `tab:knowledge_pipeline` | 4 | 1.0 | 2.6 | 7.0 | 2.0 | WIDTH GAP: widths [1.0, 2.6, 7.0, 2.0] differ by > 8x; use equal-space strategy |
| `chapters/chapter3_defence_prep_checklist.tex:18` | `tab:defence_prep_arch_checklist` | 4 | 1.0 | 7.0 | 1.0 | 3.6 | REBALANCE: last column avg 13 chars vs largest 48; narrow last column to p{1.5cm} or merge it with previous | WIDTH GAP: widths [1.0, 7.0, 1.0, 3.6] differ by > 8x; use equal-space strategy |
| `chapters/chapter4_analysis_findings.tex:922` | `tab:ch4_alignment` | 4 | 1.0 | 1.0 | 7.0 | 3.6 | REBALANCE: last column avg 12 chars vs largest 46; narrow last column to p{1.5cm} or merge it with previous | WIDTH GAP: widths [1.0, 1.0, 7.0, 3.6] differ by > 8x; use equal-space strategy |
| `chapters/chapter5_discussion_recommendations.tex:648` | `tab:ch5_final_defence_checklist` | 4 | 1.0 | 7.0 | 3.6 | 1.0 | WIDTH GAP: widths [1.0, 7.0, 3.6, 1.0] differ by > 8x; use equal-space strategy |
| `appendices/C_ch3_supp_p267_w1470.tex:533` | `tab:mcp_tools` | 4 | 1.0 | 1.0 | 7.0 | 3.6 | REBALANCE: last column avg 11 chars vs largest 40; narrow last column to p{1.5cm} or merge it with previous | WIDTH GAP: widths [1.0, 1.0, 7.0, 3.6] differ by > 8x; use equal-space strategy |

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

- **hbox horizontal-overflows**: 1231 cells exceed text-width

