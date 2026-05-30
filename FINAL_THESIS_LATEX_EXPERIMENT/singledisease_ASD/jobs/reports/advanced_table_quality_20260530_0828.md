# Advanced Table Quality Audit

Generated: 2026-05-30T08:28:11.226370

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
- **Build-log hbox horizontal-overflows**: 1429
- **under_width_allocated**: 295 tables
- **squeezed_column**: 223 tables
- **empty_cells**: 83 tables
- **right_side_empty**: 57 tables
- **width_imbalanced**: 35 tables
- **underused_column**: 35 tables
- **tall_column**: 31 tables
- **multi_page**: 14 tables
- **sparse_table**: 4 tables
- **very_multi_page**: 3 tables
- **placeholders**: 1 tables

## Issue #3 — Tables with RIGHT-SIDE EMPTY (last column nearly empty)

Count: **57** tables

| File:Line | Label | Cols | Col avg text lengths | Rec |
|---|---|---:|---|---|
| `chapters/chapter1_introduction.tex:562` | `tab:ch1_object_scope` | 3 | 2 | 46 | 11 | REBALANCE: last column avg 11 chars vs largest 46; narrow last column to p{1.5cm} or merge it with previous | WIDTH GAP: widths [1.0, 8.1, 4.1] differ by > 8x; use equal-space strategy |
| `chapters/chapter1_introduction.tex:620` | `tab:ch1_task_map` | 4 | 2 | 40 | 1 | 10 | REBALANCE: last column avg 10 chars vs largest 40; narrow last column to p{1.5cm} or merge it with previous | WIDTH GAP: widths [1.0, 7.0, 1.0, 3.6] differ by > 8x; use equal-space strategy |
| `chapters/chapter1_introduction.tex:1511` | `tab:problem_funnel_evidence` | 4 | 17 | 43 | 6 | 12 | REBALANCE: last column avg 12 chars vs largest 43; narrow last column to p{1.5cm} or merge it with previous |
| `chapters/chapter1_introduction.tex:2158` | `NOLABEL@chapters/chapter1_introduction.tex:2158` | 4 | 1 | 14 | 87 | 12 | REBALANCE: last column avg 12 chars vs largest 87; narrow last column to p{1.5cm} or merge it with previous |
| `chapters/chapter1_introduction.tex:2693` | `tab:b2c_mobile_screens` | 4 | 2 | 14 | 119 | 12 | REBALANCE: last column avg 12 chars vs largest 119; narrow last column to p{1.5cm} or merge it with previous | WIDTH GAP: widths [1.0, 2.4, 7.0, 2.2] differ by > 8x; use equal-space strategy |
| `chapters/chapter1_introduction.tex:2757` | `tab:b2c_user_forms` | 4 | 2 | 16 | 94 | 10 | REBALANCE: last column avg 10 chars vs largest 93; narrow last column to p{1.5cm} or merge it with previous |
| `chapters/chapter1_introduction.tex:2944` | `tab:report_types` | 4 | 2 | 15 | 88 | 9 | REBALANCE: last column avg 9 chars vs largest 88; narrow last column to p{1.5cm} or merge it with previous |
| `chapters/chapter1_introduction.tex:3094` | `tab:continuous_monitoring` | 4 | 2 | 14 | 105 | 10 | REBALANCE: last column avg 9 chars vs largest 105; narrow last column to p{1.5cm} or merge it with previous |
| `chapters/chapter1_introduction.tex:3357` | `tab:backend_db` | 4 | 2 | 1 | 99 | 10 | REBALANCE: last column avg 10 chars vs largest 99; narrow last column to p{1.5cm} or merge it with previous | WIDTH GAP: widths [1.0, 1.0, 8.1, 2.5] differ by > 8x; use equal-space strategy |
| `chapters/chapter1_introduction.tex:5173` | `tab:ch1_scorecard` | 3 | 16 | 31 | 5 | REBALANCE: last column avg 5 chars vs largest 31; narrow last column to p{1.5cm} or merge it with previous |
| `chapters/chapter2_literature.tex:1340` | `NOLABEL@chapters/chapter2_literature.tex:1340` | 4 | 22 | 35 | 21 | 5 | REBALANCE: last column avg 5 chars vs largest 35; narrow last column to p{1.5cm} or merge it with previous |
| `chapters/chapter2_literature.tex:2626` | `tab:ch2_scorecard` | 3 | 17 | 32 | 6 | REBALANCE: last column avg 6 chars vs largest 32; narrow last column to p{1.5cm} or merge it with previous |
| `chapters/chapter3_arch_executive_summary.tex:17` | `tab:arch_exec_summary` | 3 | 23 | 96 | 11 | REBALANCE: last column avg 11 chars vs largest 96; narrow last column to p{1.5cm} or merge it with previous |
| `chapters/chapter3_defence_prep_checklist.tex:18` | `tab:defence_prep_arch_checklist` | 4 | 2 | 49 | 1 | 15 | REBALANCE: last column avg 15 chars vs largest 49; narrow last column to p{1.5cm} or merge it with previous |
| `chapters/chapter3_research_methods.tex:92` | `NOLABEL@chapters/chapter3_research_methods.tex:92` | 2 | 43 | 13 | REBALANCE: last column avg 13 chars vs largest 43; narrow last column to p{1.5cm} or merge it with previous |
| `chapters/chapter3_research_methods.tex:1476` | `tab:primary_data_outcome_map` | 3 | 6 | 50 | 7 | REBALANCE: last column avg 7 chars vs largest 50; narrow last column to p{1.5cm} or merge it with previous |
| `chapters/chapter3_research_methods.tex:2547` | `tab:primary_analysis_sensitivity_bias` | 4 | 24 | 46 | 34 | 18 | REBALANCE: last column avg 18 chars vs largest 46; narrow last column to p{1.5cm} or merge it with previous |
| `chapters/chapter3_research_methods.tex:3566` | `tab:customer_smart_flow` | 4 | 1 | 23 | 46 | 17 | REBALANCE: last column avg 17 chars vs largest 46; narrow last column to p{1.5cm} or merge it with previous |
| `chapters/chapter3_research_methods.tex:8554` | `NOLABEL@chapters/chapter3_research_methods.tex:8554` | 5 | 12 | 48 | 11 | 5 | 14 | REBALANCE: last column avg 14 chars vs largest 48; narrow last column to p{1.5cm} or merge it with previous |
| `chapters/chapter3_research_methods.tex:10899` | `NOLABEL@chapters/chapter3_research_methods.tex:10899` | 4 | 18 | 48 | 28 | 10 | REBALANCE: last column avg 10 chars vs largest 48; narrow last column to p{1.5cm} or merge it with previous |
| `chapters/chapter3_research_methods.tex:11490` | `NOLABEL@chapters/chapter3_research_methods.tex:11490` | 3 | 11 | 125 | 13 | REBALANCE: last column avg 13 chars vs largest 125; narrow last column to p{1.5cm} or merge it with previous |
| `chapters/chapter3_research_methods.tex:11513` | `NOLABEL@chapters/chapter3_research_methods.tex:11513` | 3 | 2 | 84 | 9 | REBALANCE: last column avg 9 chars vs largest 84; narrow last column to p{1.5cm} or merge it with previous |
| `chapters/chapter3_research_methods.tex:11549` | `NOLABEL@chapters/chapter3_research_methods.tex:11549` | 4 | 4 | 54 | 10 | 7 | REBALANCE: last column avg 7 chars vs largest 54; narrow last column to p{1.5cm} or merge it with previous |
| `chapters/chapter3_research_methods.tex:11570` | `NOLABEL@chapters/chapter3_research_methods.tex:11570` | 4 | 11 | 32 | 5 | 7 | REBALANCE: last column avg 7 chars vs largest 32; narrow last column to p{1.5cm} or merge it with previous |
| `chapters/chapter3_research_methods.tex:12960` | `tab:ch3_decision_summary` | 3 | 38 | 176 | 16 | REBALANCE: last column avg 16 chars vs largest 175; narrow last column to p{1.5cm} or merge it with previous |
| `chapters/chapter4_analysis_findings.tex:500` | `tab:ch4_triangulation` | 4 | 14 | 15 | 96 | 16 | REBALANCE: last column avg 16 chars vs largest 96; narrow last column to p{1.5cm} or merge it with previous |
| `chapters/chapter4_analysis_findings.tex:922` | `tab:ch4_alignment` | 4 | 3 | 2 | 53 | 14 | REBALANCE: last column avg 14 chars vs largest 53; narrow last column to p{1.5cm} or merge it with previous | WIDTH GAP: widths [1.0, 1.0, 7.0, 3.6] differ by > 8x; use equal-space strategy |
| `chapters/chapter4_analysis_findings.tex:1582` | `NOLABEL@chapters/chapter4_analysis_findings.tex:1582` | 5 | 12 | 33 | 18 | 32 | 6 | REBALANCE: last column avg 6 chars vs largest 33; narrow last column to p{1.5cm} or merge it with previous |
| `chapters/chapter4_analysis_findings.tex:3834` | `NOLABEL@chapters/chapter4_analysis_findings.tex:3834` | 4 | 2 | 34 | 40 | 13 | REBALANCE: last column avg 13 chars vs largest 40; narrow last column to p{1.5cm} or merge it with previous |
| `chapters/chapter4_analysis_findings.tex:3909` | `NOLABEL@chapters/chapter4_analysis_findings.tex:3909` | 4 | 3 | 16 | 86 | 14 | REBALANCE: last column avg 14 chars vs largest 86; narrow last column to p{1.5cm} or merge it with previous |
| `chapters/chapter4_analysis_findings.tex:3931` | `NOLABEL@chapters/chapter4_analysis_findings.tex:3931` | 4 | 2 | 38 | 8 | 13 | REBALANCE: last column avg 13 chars vs largest 38; narrow last column to p{1.5cm} or merge it with previous |
| `chapters/chapter4_analysis_findings.tex:4039` | `NOLABEL@chapters/chapter4_analysis_findings.tex:4039` | 4 | 3 | 29 | 63 | 4 | REBALANCE: last column avg 4 chars vs largest 63; narrow last column to p{1.5cm} or merge it with previous |
| `chapters/chapter4_analysis_findings.tex:5044` | `NOLABEL@chapters/chapter4_analysis_findings.tex:5044` | 6 | 4 | 22 | 24 | 1 | 37 | 7 | REBALANCE: last column avg 7 chars vs largest 37; narrow last column to p{1.5cm} or merge it with previous |
| `chapters/chapter5_discussion_recommendations.tex:86` | `NOLABEL@chapters/chapter5_discussion_recommendations.tex:86` | 2 | 47 | 17 | REBALANCE: last column avg 17 chars vs largest 47; narrow last column to p{1.5cm} or merge it with previous |
| `chapters/chapter5_discussion_recommendations.tex:1759` | `NOLABEL@chapters/chapter5_discussion_recommendations.tex:1759` | 4 | 16 | 22 | 63 | 19 | REBALANCE: last column avg 19 chars vs largest 63; narrow last column to p{1.5cm} or merge it with previous |
| `chapters/chapter5_discussion_recommendations.tex:3217` | `NOLABEL@chapters/chapter5_discussion_recommendations.tex:3217` | 4 | 2 | 13 | 71 | 15 | REBALANCE: last column avg 15 chars vs largest 71; narrow last column to p{1.5cm} or merge it with previous |
| `chapters/chapter5_discussion_recommendations.tex:3271` | `NOLABEL@chapters/chapter5_discussion_recommendations.tex:3271` | 5 | 1 | 10 | 59 | 73 | 10 | REBALANCE: last column avg 10 chars vs largest 73; narrow last column to p{1.5cm} or merge it with previous |
| `chapters/chapter5_discussion_recommendations.tex:4716` | `NOLABEL@chapters/chapter5_discussion_recommendations.tex:4716` | 8 | 2 | 16 | 1 | 1 | 2 | 41 | 6 | 1 | REBALANCE: last column avg 1 chars vs largest 41; narrow last column to p{1.5cm} or merge it with previous |
| `chapters/chapter5_discussion_recommendations.tex:5231` | `NOLABEL@chapters/chapter5_discussion_recommendations.tex:5231` | 4 | 25 | 42 | 8 | 16 | REBALANCE: last column avg 16 chars vs largest 42; narrow last column to p{1.5cm} or merge it with previous |
| `chapters/chapter5_discussion_recommendations.tex:6363` | `tab:secondary_data_stack` | 3 | 4 | 47 | 9 | REBALANCE: last column avg 9 chars vs largest 47; narrow last column to p{1.5cm} or merge it with previous | WIDTH GAP: widths [1.0, 8.5, 3.7] differ by > 8x; use equal-space strategy |

## Issue #4 — Tables with TALL-COLUMN (one column has 3+ rows of text)

Count: **31** tables

| File:Line | Label | Cols | Col max text | Rec |
|---|---|---:|---|---|
| `chapters/chapter1_introduction.tex:4488` | `tab:tam_toe_rbv` | 5 | 6 | 321 | 96 | 120 | 136 | WIDEN COL 2 (max 321 chars) by NARROWING COL 1 (avg 3 chars) |
| `chapters/chapter3_research_methods.tex:5307` | `tab:remaining_ai_capability_matrix` | 6 | 33 | 276 | 236 | 236 | 131 | 242 | WIDEN COL 2 (max 276 chars) by NARROWING COL 1 (avg 15 chars) |
| `chapters/chapter3_research_methods.tex:4081` | `tab:ch3_b2b_b2c_questionnaire` | 5 | 251 | 85 | 21 | 3 | 3 | WIDEN COL 1 (max 251 chars) by NARROWING COL 4 (avg 0 chars) |
| `chapters/chapter3_research_methods.tex:5088` | `tab:decision_ai_decisions` | 4 | 34 | 230 | 162 | 101 | WIDEN COL 2 (max 230 chars) by NARROWING COL 1 (avg 25 chars) |
| `chapters/chapter5_discussion_recommendations.tex:1797` | `tab:ch5_rgaig_vs_peer_frameworks` | 6 | 41 | 48 | 51 | 45 | 45 | 215 | WIDEN COL 6 (max 215 chars) by NARROWING COL 1 (avg 18 chars) |
| `chapters/chapter3_research_methods.tex:4982` | `tab:data_needs_by_stage_audience` | 5 | 54 | 25 | 205 | 128 | 212 | WIDEN COL 5 (max 212 chars) by NARROWING COL 2 (avg 22 chars) |
| `chapters/chapter3_research_methods.tex:2733` | `tab:research_anatomy` | 6 | 3 | 182 | 119 | 100 | 148 | 58 | WIDEN COL 2 (max 182 chars) by NARROWING COL 1 (avg 2 chars) |
| `chapters/chapter5_discussion_recommendations.tex:6120` | `tab:management_decision_matrix` | 4 | 51 | 158 | 147 | 182 | WIDEN COL 4 (max 182 chars) by NARROWING COL 1 (avg 35 chars) |
| `appendices/M_operationalization_detail_p725.tex:257` | `tab:topic_objective_achievement_control` | 5 | 33 | 48 | 103 | 176 | 107 | WIDEN COL 4 (max 176 chars) by NARROWING COL 1 (avg 24 chars) |
| `chapters/chapter1_introduction.tex:3965` | `tab:doctoral_quality_chain` | 5 | 2 | 171 | 73 | 82 | 34 | WIDEN COL 2 (max 171 chars) by NARROWING COL 1 (avg 1 chars) |
| `chapters/chapter3_research_methods.tex:2775` | `tab:primary_iv_dv_framework` | 5 | 3 | 75 | 106 | 150 | 147 | WIDEN COL 4 (max 150 chars) by NARROWING COL 1 (avg 2 chars) |
| `chapters/chapter3_research_methods.tex:3729` | `tab:primary_analysis_cards` | 5 | 4 | 36 | 71 | 82 | 145 | WIDEN COL 5 (max 145 chars) by NARROWING COL 1 (avg 2 chars) |
| `chapters/chapter1_introduction.tex:923` | `tab:why_now` | 4 | 23 | 113 | 140 | 88 | WIDEN COL 3 (max 140 chars) by NARROWING COL 1 (avg 20 chars) |
| `chapters/chapter3_research_methods.tex:4386` | `tab:b2c_b2b_assessment_crosswalk` | 5 | 79 | 19 | 53 | 140 | 83 | WIDEN COL 4 (max 140 chars) by NARROWING COL 2 (avg 4 chars) |
| `chapters/chapter3_research_methods.tex:3787` | `tab:secondary_analysis_cards` | 5 | 4 | 26 | 85 | 87 | 133 | WIDEN COL 5 (max 133 chars) by NARROWING COL 1 (avg 1 chars) |
| `appendices/E_ch5_supp_p525_w1059.tex:797` | `tab:future_studies` | 4 | 2 | 127 | 131 | 123 | WIDEN COL 3 (max 131 chars) by NARROWING COL 1 (avg 1 chars) |
| `chapters/chapter1_introduction.tex:4407` | `tab:concept_to_analysis` | 5 | 33 | 50 | 37 | 8 | 123 | WIDEN COL 5 (max 123 chars) by NARROWING COL 4 (avg 6 chars) |
| `chapters/chapter3_research_methods.tex:2601` | `tab:primary_analysis_triangulation` | 4 | 29 | 100 | 123 | 46 | WIDEN COL 3 (max 123 chars) by NARROWING COL 1 (avg 23 chars) |
| `appendices/M_operationalization_detail_p725.tex:636` | `tab:smart_objectives` | 6 | 3 | 119 | 120 | 66 | 60 | 22 | WIDEN COL 3 (max 120 chars) by NARROWING COL 1 (avg 2 chars) |
| `chapters/chapter3_research_methods.tex:3931` | `tab:hybrid_analysis_cards` | 5 | 4 | 25 | 63 | 55 | 119 | WIDEN COL 5 (max 119 chars) by NARROWING COL 1 (avg 2 chars) |
| `chapters/chapter3_research_methods.tex:5375` | `tab:time_saving_metrics` | 5 | 23 | 95 | 101 | 45 | 117 | WIDEN COL 5 (max 117 chars) by NARROWING COL 1 (avg 19 chars) |
| `chapters/chapter3_research_methods.tex:967` | `tab:approach_summary` | 5 | 13 | 115 | 24 | 84 | 61 | WIDEN COL 2 (max 115 chars) by NARROWING COL 1 (avg 11 chars) |
| `chapters/chapter5_discussion_recommendations.tex:585` | `tab:ch5_recommendations_snapshot` | 6 | 3 | 115 | 23 | 38 | 13 | 8 | WIDEN COL 2 (max 115 chars) by NARROWING COL 1 (avg 2 chars) |
| `chapters/chapter3_research_methods.tex:5199` | `tab:ethical_ai_components` | 5 | 32 | 89 | 112 | 89 | 47 | WIDEN COL 3 (max 112 chars) by NARROWING COL 1 (avg 20 chars) |
| `chapters/chapter5_discussion_recommendations.tex:6815` | `tab:ch5_per_chapter_data_summary` | 5 | 3 | 102 | 112 | 8 | 86 | WIDEN COL 3 (max 112 chars) by NARROWING COL 1 (avg 1 chars) |
| `chapters/chapter3_microservice_ipo.tex:17` | `tab:microservice_ipo_contract` | 5 | 14 | 82 | 104 | 111 | 92 | WIDEN COL 4 (max 111 chars) by NARROWING COL 1 (avg 8 chars) |
| `chapters/chapter3_research_methods.tex:2888` | `tab:ethics_consent_anchor` | 5 | 5 | 110 | 100 | 99 | 53 | WIDEN COL 2 (max 110 chars) by NARROWING COL 1 (avg 2 chars) |
| `chapters/chapter5_discussion_recommendations.tex:1869` | `tab:conceptual_validation` | 5 | 9 | 107 | 75 | 50 | 10 | WIDEN COL 2 (max 107 chars) by NARROWING COL 1 (avg 7 chars) |
| `chapters/chapter3_research_methods.tex:6614` | `tab:ch3_partc_bootstrap` | 4 | 52 | 86 | 58 | 105 | WIDEN COL 4 (max 105 chars) by NARROWING COL 1 (avg 26 chars) |
| `chapters/chapter5_discussion_recommendations.tex:5855` | `tab:stakeholder_value_cards` | 5 | 28 | 61 | 105 | 30 | 48 | WIDEN COL 3 (max 105 chars) by NARROWING COL 1 (avg 17 chars) |
| `chapters/chapter3_research_methods.tex:5231` | `tab:governance_ai_kpis` | 4 | 27 | 78 | 82 | 102 | WIDEN COL 4 (max 102 chars) by NARROWING COL 1 (avg 18 chars) |

## Issue #5 — Tables that span 3+ pages (should be split into Part 1 / Part 2)

Count: **3** tables (> 50 rows — likely 3+ pages)

| File:Line | Label | Rows | Cols | Caption | Action |
|---|---|---:|---:|---|---|
| `chapters/chapter3_crossref_index.tex:15` | `tab:crossref_index_new` | 106 | 3 | Cross-Reference Index --- New Tables | SPLIT into Part 1 + Part 2 |
| `appendices/S_glossary.tex:11` | `tab:glossary_full` | 81 | 2 | Glossary of Acronyms and Key Terms | SPLIT into Part 1 + Part 2 |
| `appendices/I_brutal_feedback_p632_w64.tex:41` | `tab:brutal_appendices` | 55 | 10 | Per-Appendix Brutal Feedback | SPLIT into Part 1 + Part 2 |

## Issue #5b — Tables that span exactly 2 pages (acceptable, no action)

Count: **11**

## Issue #7 — Tables with WIDTH-IMBALANCE (column widths differ > 4x)

Count: **35** tables

| File:Line | Label | Cols | Widths (cm) | Rec |
|---|---|---:|---|---|
| `chapters/chapter3_research_methods.tex:7284` | `tab:master_rewrite_drafts` | 3 | 1.8 | 2.5 | 10.2 | WIDTH GAP: widths [1.8, 2.5, 10.2] differ by > 8x; use equal-space strategy |
| `chapters/chapter1_introduction.tex:3783` | `tab:main_objectives` | 3 | 1.0 | 9.5 | 1.0 | WIDTH GAP: widths [1.0, 9.5, 1.0] differ by > 8x; use equal-space strategy |
| `chapters/chapter3_crossref_index.tex:15` | `tab:crossref_index_new` | 3 | 1.0 | 9.5 | 1.0 | WIDTH GAP: widths [1.0, 9.5, 1.0] differ by > 8x; use equal-space strategy |
| `chapters/chapter3_examiner_qa.tex:17` | `tab:examiner_qa_architecture` | 3 | 1.0 | 9.5 | 2.5 | WIDTH GAP: widths [1.0, 9.5, 2.5] differ by > 8x; use equal-space strategy |
| `chapters/chapter3_research_methods.tex:3259` | `tab:b2c_research_gap_catalog` | 4 | 1.0 | 9.5 | 1.0 | 1.0 | WIDTH GAP: widths [1.0, 9.5, 1.0, 1.0] differ by > 8x; use equal-space strategy |
| `chapters/chapter3_research_methods.tex:3436` | `tab:b2b_research_gap_catalog` | 4 | 1.0 | 9.5 | 1.0 | 1.0 | WIDTH GAP: widths [1.0, 9.5, 1.0, 1.0] differ by > 8x; use equal-space strategy |
| `appendices/H_rgaig_architecture_p605_w1135.tex:960` | `tab:appo_audit_fields` | 2 | 1.0 | 9.5 | WIDTH GAP: widths [1.0, 9.5] differ by > 8x; use equal-space strategy |
| `appendices/M_operationalization_detail_p725.tex:426` | `tab:part_objectives` | 4 | 1.0 | 9.5 | 1.0 | 1.0 | WIDTH GAP: widths [1.0, 9.5, 1.0, 1.0] differ by > 8x; use equal-space strategy |
| `appendices/M_operationalization_detail_p725.tex:502` | `tab:research_objectives` | 3 | 1.0 | 9.5 | 2.7 | REBALANCE: last column avg 6 chars vs largest 69; narrow last column to p{1.5cm} or merge it with previous | WIDTH GAP: widths [1.0, 9.5, 2.7] differ by > 8x; use equal-space strategy |
| `appendices/M_operationalization_detail_p725.tex:678` | `tab:rq_mapping` | 3 | 1.0 | 9.5 | 1.0 | WIDTH GAP: widths [1.0, 9.5, 1.0] differ by > 8x; use equal-space strategy |
| `chapters/chapter4_analysis_findings.tex:5919` | `tab:ch4_partd_framework_quality` | 3 | 2.9 | 9.3 | 1.0 | WIDTH GAP: widths [2.9, 9.3, 1.0] differ by > 8x; use equal-space strategy |
| `appendices/H_rgaig_architecture_p605_w1135.tex:302` | `tab:appo_maturity_arch` | 3 | 1.0 | 3.0 | 9.2 | WIDTH GAP: widths [1.0, 3.0, 9.2] differ by > 8x; use equal-space strategy |
| `chapters/chapter5_discussion_recommendations.tex:4047` | `tab:ch5_final_verdict` | 3 | 2.4 | 2.0 | 9.0 | WIDTH GAP: widths [2.4, 2.0, 9.0] differ by > 8x; use equal-space strategy |
| `appendices/F_survey_instrument_p566_w1285.tex:1126` | `tab:survey_b2c_primary_addendum` | 3 | 1.0 | 9.0 | 3.2 | REBALANCE: last column avg 11 chars vs largest 85; narrow last column to p{1.5cm} or merge it with previous | WIDTH GAP: widths [1.0, 9.0, 3.2] differ by > 8x; use equal-space strategy |
| `chapters/chapter3_research_methods.tex:4458` | `tab:scale_design` | 3 | 3.6 | 8.6 | 1.0 | WIDTH GAP: widths [3.6, 8.6, 1.0] differ by > 8x; use equal-space strategy |
| `chapters/chapter4_analysis_findings.tex:533` | `tab:ch4_org_interpretation` | 3 | 1.0 | 3.7 | 8.5 | WIDTH GAP: widths [1.0, 3.7, 8.5] differ by > 8x; use equal-space strategy |
| `chapters/chapter5_discussion_recommendations.tex:6363` | `tab:secondary_data_stack` | 3 | 1.0 | 8.5 | 3.7 | REBALANCE: last column avg 9 chars vs largest 47; narrow last column to p{1.5cm} or merge it with previous | WIDTH GAP: widths [1.0, 8.5, 3.7] differ by > 8x; use equal-space strategy |
| `appendices/H_rgaig_architecture_p605_w1135.tex:335` | `tab:appo_gov_dimensions` | 3 | 3.7 | 8.5 | 1.0 | WIDTH GAP: widths [3.7, 8.5, 1.0] differ by > 8x; use equal-space strategy |
| `chapters/chapter1_introduction.tex:1709` | `tab:b2b_subproblems` | 3 | 1.0 | 3.9 | 8.3 | WIDTH GAP: widths [1.0, 3.9, 8.3] differ by > 8x; use equal-space strategy |
| `chapters/chapter3_research_methods.tex:401` | `tab:ch3_instrument_anchoring` | 3 | 3.9 | 8.3 | 1.0 | WIDTH GAP: widths [3.9, 8.3, 1.0] differ by > 8x; use equal-space strategy |
| `chapters/chapter1_introduction.tex:1746` | `tab:b2c_subproblems` | 3 | 1.0 | 4.0 | 8.2 | WIDTH GAP: widths [1.0, 4.0, 8.2] differ by > 8x; use equal-space strategy |
| `chapters/chapter1_introduction.tex:562` | `tab:ch1_object_scope` | 3 | 1.0 | 8.1 | 4.1 | REBALANCE: last column avg 11 chars vs largest 46; narrow last column to p{1.5cm} or merge it with previous | WIDTH GAP: widths [1.0, 8.1, 4.1] differ by > 8x; use equal-space strategy |
| `chapters/chapter1_introduction.tex:3357` | `tab:backend_db` | 4 | 1.0 | 1.0 | 8.1 | 2.5 | REBALANCE: last column avg 10 chars vs largest 99; narrow last column to p{1.5cm} or merge it with previous | WIDTH GAP: widths [1.0, 1.0, 8.1, 2.5] differ by > 8x; use equal-space strategy |
| `appendices/C_ch3_supp_p267_w1470.tex:1475` | `NOLABEL@appendices/C_ch3_supp_p267_w1470.tex:1475` | 3 | 1.6 | 4.6 | 8.0 | WIDTH GAP: widths [1.6, 4.6, 8.0] differ by > 8x; use equal-space strategy |
| `appendices/H_rgaig_architecture_p605_w1135.tex:39` | `tab:appo_tech_research_map` | 3 | 4.2 | 8.0 | 1.0 | WIDTH GAP: widths [4.2, 8.0, 1.0] differ by > 8x; use equal-space strategy |
| `appendices/D_ch4_supp_p390_w814.tex:317` | `tab:eval_explain_trust` | 3 | 4.4 | 7.8 | 1.0 | WIDTH GAP: widths [4.4, 7.8, 1.0] differ by > 8x; use equal-space strategy |
| `appendices/Q_drill_methodology.tex:55` | `tab:app_q_drill_anatomy` | 3 | 1.0 | 4.4 | 7.8 | WIDTH GAP: widths [1.0, 4.4, 7.8] differ by > 8x; use equal-space strategy |
| `appendices/F_survey_instrument_p566_w1285.tex:981` | `tab:survey_section_g` | 3 | 1.0 | 7.5 | 4.7 | WIDTH GAP: widths [1.0, 7.5, 4.7] differ by > 8x; use equal-space strategy |
| `appendices/F_survey_instrument_p566_w1285.tex:156` | `tab:survey_reliability_strategy` | 3 | 5.0 | 7.2 | 1.0 | WIDTH GAP: widths [5.0, 7.2, 1.0] differ by > 8x; use equal-space strategy |
| `chapters/chapter1_introduction.tex:620` | `tab:ch1_task_map` | 4 | 1.0 | 7.0 | 1.0 | 3.6 | REBALANCE: last column avg 10 chars vs largest 40; narrow last column to p{1.5cm} or merge it with previous | WIDTH GAP: widths [1.0, 7.0, 1.0, 3.6] differ by > 8x; use equal-space strategy |
| `chapters/chapter1_introduction.tex:2693` | `tab:b2c_mobile_screens` | 4 | 1.0 | 2.4 | 7.0 | 2.2 | REBALANCE: last column avg 12 chars vs largest 119; narrow last column to p{1.5cm} or merge it with previous | WIDTH GAP: widths [1.0, 2.4, 7.0, 2.2] differ by > 8x; use equal-space strategy |
| `chapters/chapter1_introduction.tex:3316` | `tab:knowledge_pipeline` | 4 | 1.0 | 2.6 | 7.0 | 2.0 | WIDTH GAP: widths [1.0, 2.6, 7.0, 2.0] differ by > 8x; use equal-space strategy |
| `chapters/chapter4_analysis_findings.tex:922` | `tab:ch4_alignment` | 4 | 1.0 | 1.0 | 7.0 | 3.6 | REBALANCE: last column avg 14 chars vs largest 53; narrow last column to p{1.5cm} or merge it with previous | WIDTH GAP: widths [1.0, 1.0, 7.0, 3.6] differ by > 8x; use equal-space strategy |
| `chapters/chapter5_discussion_recommendations.tex:648` | `tab:ch5_final_defence_checklist` | 4 | 1.0 | 7.0 | 3.6 | 1.0 | WIDTH GAP: widths [1.0, 7.0, 3.6, 1.0] differ by > 8x; use equal-space strategy |
| `appendices/C_ch3_supp_p267_w1470.tex:533` | `tab:mcp_tools` | 4 | 1.0 | 1.0 | 7.0 | 3.6 | REBALANCE: last column avg 11 chars vs largest 40; narrow last column to p{1.5cm} or merge it with previous | WIDTH GAP: widths [1.0, 1.0, 7.0, 3.6] differ by > 8x; use equal-space strategy |

## Build-Log Overflows (vbox bottom + hbox horizontal)

- **vbox bottom-overflows**: 7 pages with content past page-bottom

| Severity (pt too high) | Action |
|---:|---|
| 565.8 | reduce table size, add \clearpage, or \resizebox |
| 489.3 | reduce table size, add \clearpage, or \resizebox |
| 252.3 | reduce table size, add \clearpage, or \resizebox |
| 137.6 | reduce table size, add \clearpage, or \resizebox |
| 68.6 | reduce table size, add \clearpage, or \resizebox |
| 60.9 | reduce table size, add \clearpage, or \resizebox |
| 33.8 | reduce table size, add \clearpage, or \resizebox |

- **hbox horizontal-overflows**: 1429 cells exceed text-width

