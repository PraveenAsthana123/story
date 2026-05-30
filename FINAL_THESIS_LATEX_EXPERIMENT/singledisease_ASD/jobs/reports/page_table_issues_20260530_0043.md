# Per-Page Table Issues Report

Generated: 2026-05-30T00:43:17.352154

## Cause Explanation

**Why tables waste vertical space:**

In LaTeX `xltabular`/`longtable`, each row's HEIGHT equals the TALLEST cell in that row. When one column has long wrapped text (5+ lines) and another has 1 word ("Yes", "H1"), both columns occupy that same row height. Result: short-content cells show with 4-5 lines of WHITE SPACE around them. The table appears LONGER than the actual text content needs — "table length > text length".

**Root causes of this pattern:**

1. **Squeezed wide-content column** — column allocated < 6cm but contains 100+ chars per cell → wraps to 4-6 lines unnecessarily
2. **Over-wide narrow-content column** — column allocated > 3cm but content is just 1-2 words → wastes 2+ cm that could go to wide-content col
3. **No mixed-content awareness** — manual column widths don't account for the ratio of content lengths across columns

**Fixes available:**

- `fix_advanced_table_quality_v2.py` rebalances column widths using sqrt-weighted text-density
- Narrow content columns get clamped to 1-1.5cm
- Wide content columns get expanded to ~8 chars/cm density (optimal for \footnotesize)

## Build-Log Bottom Overflows: 7 pages affected

| PDF Page | Display Page | Severity (pt too high) | Likely Cause |
|---:|---|---:|---|
| 61 | lix | 689 | Multi-row table can't fit (consider split or Part 1/Part 2) |
| 507 | 443 | 76 | Single tall row > page space (table cell ~ minor) |
| 512 | 448 | 116 | Single tall row > page space (table cell ~ minor) |
| 517 | 453 | 295 | Multi-row table can't fit (consider split or Part 1/Part 2) |
| 899 | 835 | 155 | Single tall row > page space (table cell ~ minor) |
| 1596 | 1532 | 87 | Single tall row > page space (table cell ~ minor) |
| 1600 | 1536 | 517 | Multi-row table can't fit (consider split or Part 1/Part 2) |

## Issue Counts (current audit)

| Issue | Count |
|---|---:|
| empty_cells | 71 |
| right_side_empty | 54 |
| width_imbalanced | 32 |
| tall_column | 25 |
| multi_page | 13 |
| sparse_table | 4 |
| very_multi_page | 3 |
| placeholders | 1 |

## Per-Page Table Inventory (flagged tables only)

Total flagged tables: **167**

| PDF Pg | Label | File:Line | Cols | Widths (cm) | Avg chars | Max chars | Issue | Why | Fix |
|---:|---|---|---:|---|---|---|---|---|---|
| 28 | `tab:ch1_object_scope` | `chapters/chapter1_introduction.tex:562` | 3 | 1.0, 8.1, 4.1 | 2, 46, 11 | 3, 69, 17 | right_side_empty; width_imbalanced | — | — |
| 30 | `tab:ch1_task_map` | `chapters/chapter1_introduction.tex:620` | 4 | 1.0, 7.1, 1.0, 3.5 | 2, 36, 4, 9 | 3, 57, 30, 20 | right_side_empty; width_imbalanced | Col4 has 3.5cm width but only 9 avg chars — wasted ~2.0cm | Narrow col4 to p{1.5cm} |
| 67 | `tab:b2b_subproblems` | `chapters/chapter1_introduction.tex:1709` | 3 | 1.0, 3.9, 8.3 | 5, 23, 102 | 5, 34, 130 | width_imbalanced | Col3 squeezed: 102 chars in 8.3cm = 12 chars/cm (forces wrap) | Widen col3 to p{12.8cm} |
| 68 | `tab:b2c_subproblems` | `chapters/chapter1_introduction.tex:1746` | 3 | 1.0, 4.0, 8.2 | 5, 23, 96 | 5, 40, 129 | width_imbalanced | — | — |
| 83 | `tab:b2c_mobile_screens` | `chapters/chapter1_introduction.tex:2693` | 4 | 1.0, 2.4, 7.0, 2.2 | 2, 14, 118, 12 | 3, 17, 145, 15 | right_side_empty; width_imbalanced | Col3 squeezed: 118 chars in 7.0cm = 17 chars/cm (forces wrap) | Widen col3 to p{14.7cm} |
| 83 | `tab:b2c_user_forms` | `chapters/chapter1_introduction.tex:2757` | 4 | 1.0, 2.7, 6.7, 2.2 | 2, 16, 94, 10 | 3, 21, 122, 14 | right_side_empty | Col3 squeezed: 94 chars in 6.7cm = 14 chars/cm (forces wrap) | Widen col3 to p{11.7cm} |
| 84 | `tab:report_types` | `chapters/chapter1_introduction.tex:2944` | 4 | 1.0, 2.7, 6.7, 2.2 | 2, 15, 88, 9 | 3, 19, 106, 13 | right_side_empty | Col3 squeezed: 88 chars in 6.7cm = 13 chars/cm (forces wrap) | Widen col3 to p{11.0cm} |
| 84 | `tab:continuous_monitoring` | `chapters/chapter1_introduction.tex:3094` | 4 | 1.0, 2.6, 6.9, 2.1 | 2, 14, 105, 10 | 3, 18, 155, 10 | right_side_empty | Col3 squeezed: 105 chars in 6.9cm = 15 chars/cm (forces wrap) | Mixed long+short cols: cols [3] have long content vs cols [1, 2, 4] short — rows inher | Widen col3 to p{13.2cm} | Widen long col to reduce wrap (smaller max height → less wasted space in short cols) |
| 86 | `tab:knowledge_pipeline` | `chapters/chapter1_introduction.tex:3316` | 4 | 1.0, 2.6, 7.0, 2.0 | 2, 16, 113, 9 | 2, 19, 155, 14 | width_imbalanced | Col3 squeezed: 113 chars in 7.0cm = 16 chars/cm (forces wrap) | Mixed long+short cols: cols [3] have long content vs cols [1, 4] short — rows inherit  | Widen col3 to p{14.1cm} | Widen long col to reduce wrap (smaller max height → less wasted space in short cols) |
| 86 | `tab:backend_db` | `chapters/chapter1_introduction.tex:3357` | 4 | 1.0, 1.0, 8.1, 2.5 | 2, 1, 99, 10 | 3, 14, 127, 13 | right_side_empty; width_imbalanced | Col3 squeezed: 99 chars in 8.1cm = 12 chars/cm (forces wrap) | Widen col3 to p{12.4cm} |
| 92 | `tab:main_objectives` | `chapters/chapter1_introduction.tex:3783` | 3 | 1.0, 9.5, 1.0 | 2, 84, 2 | 2, 115, 4 | width_imbalanced | — | — |
| 101 | `tab:tam_toe_rbv` | `chapters/chapter1_introduction.tex:4488` | 5 | 1.0, 3.1, 2.4, 2.8, 2.8 | 3, 101, 60, 81, 83 | 6, 321, 96, 120, 136 | tall_column | Col2 squeezed: 101 chars in 3.1cm = 33 chars/cm (forces wrap) | Col3 squeezed: 60 chars in 2.4cm = 25 chars/cm (forces wrap) | Widen col2 to p{12.6cm} | Widen col3 to p{7.4cm} |
| 122 | `tab:ch1_scorecard` | `chapters/chapter1_introduction.tex:5173` | 3 | 4.5, 6.2, 2.5 | 16, 31, 5 | 22, 43, 6 | right_side_empty | — | — |
| 159 | `tab:lit_limitations` | `chapters/chapter2_literature.tex:572` | 8 | 3.0, L, L, L, L, L, L, L | 19, 1, 1, 1, 1, 1, 1, 40 | 26, 4, 4, 5, 5, 8, 4, 47 |  | — | — |
| 242 | `tab:ch2_scorecard` | `chapters/chapter2_literature.tex:2626` | 3 | 4.4, 6.2, 2.6 | 17, 32, 6 | 22, 42, 6 | right_side_empty | — | — |
| 258 | `tab:research_variables` | `chapters/chapter3_research_methods.tex:6848` | 4 | 1.0, 3.7, 6.9, 1.0 | 0, 17, 62, 4 | 4, 24, 141, 17 |  | — | — |
| 258 | `tab:master_rewrite_drafts` | `chapters/chapter3_research_methods.tex:7284` | 3 | 1.8, 2.5, 10.2 | 9, 18, 448 | 9, 25, 896 | width_imbalanced | Col3 squeezed: 448 chars in 10.2cm = 44 chars/cm (forces wrap) | Col3 has max 896 chars in 10.2cm = 22+ lines per cell → tall rows | Widen col3 to p{56.0cm} | Consider widening col3 or splitting content |
| 260 | `tab:arch_exec_summary` | `chapters/chapter3_arch_executive_summary.tex:17` | 3 | 3.5, 6.9, 2.8 | 23, 91, 14 | 32, 154, 78 | right_side_empty | Col2 squeezed: 91 chars in 6.9cm = 13 chars/cm (forces wrap) | Mixed long+short cols: cols [2] have long content vs cols [3] short — rows inherit max  | Widen col2 to p{11.4cm} | Widen long col to reduce wrap (smaller max height → less wasted space in short cols) |
| 317 | `tab:statistical_analysis_list` | `chapters/chapter3_pipeline_extras.tex:566` | 2 | 3.2, L | 19, 57 | 32, 95 | multi_page | — | — |
| 384 | `tab:iso_audit_runbook` | `chapters/chapter3_iso_audit_runbook.tex:18` | 5 | 3.0, 4.5, 1.8, 1.5, 1.5 | 31, 46, 19, 16, 12 | 49, 68, 49, 29, 30 | multi_page | — | — |
| 439 | `tab:crossref_index_new` | `chapters/chapter3_crossref_index.tex:15` | 3 | 4.4, L, 3.6 | 0, 26, 0 | 5, 50, 11 | multi_page; very_multi_page; sparse_table | Col1 has 4.4cm width but only 0 avg chars — wasted ~2.9cm | Col3 has 3.6cm width but only 0 avg chars — wasted ~2.1cm | Narrow col1 to p{1.5cm} | Narrow col3 to p{1.5cm} |
| 448 | `tab:examiner_qa_architecture` | `chapters/chapter3_examiner_qa.tex:17` | 3 | 1.0, 8.6, 3.6 | 2, 325, 57 | 3, 437, 441 | tall_column; width_imbalanced | Col2 squeezed: 325 chars in 8.6cm = 38 chars/cm (forces wrap) | Col3 squeezed: 57 chars in 3.6cm = 16 chars/cm (forces wrap) | Widen col2 to p{40.6cm} | Widen col3 to p{7.1cm} |
| 453 | `tab:defence_prep_arch_checklist` | `chapters/chapter3_defence_prep_checklist.tex:18` | 4 | 1.0, 7.0, 1.0, 3.6 | 2, 48, 4, 13 | 2, 68, 51, 25 | right_side_empty; width_imbalanced | — | — |
| 459 | `tab:microservice_ipo_contract` | `chapters/chapter3_microservice_ipo.tex:17` | 5 | 2.0, 2.6, 2.8, 2.9, 2.7 | 8, 64, 72, 77, 65 | 14, 82, 104, 111, 92 | tall_column | Col2 squeezed: 64 chars in 2.6cm = 25 chars/cm (forces wrap) | Col3 squeezed: 72 chars in 2.8cm = 26 chars/cm (forces wrap) | Widen col2 to p{8.0cm} | Widen col3 to p{9.0cm} |
| 462 | `tab:arch_iteration_changelog` | `chapters/chapter3_arch_changelog.tex:18` | 4 | 1.0, 6.1, 3.5, 2.0 | 1, 60, 20, 6 | 4, 145, 60, 18 |  | — | — |
| 469 | `tab:ch3_instrument_anchoring` | `chapters/chapter3_research_methods.tex:401` | 3 | 3.9, 8.3, 1.0 | 25, 111, 2 | 36, 197, 5 | width_imbalanced | Col2 squeezed: 111 chars in 8.3cm = 13 chars/cm (forces wrap) | Mixed long+short cols: cols [2] have long content vs cols [3] short — rows inherit max | Widen col2 to p{13.8cm} | Widen long col to reduce wrap (smaller max height → less wasted space in short cols) |
| 473 | `tab:ch3_statistical_plan` | `chapters/chapter3_research_methods.tex:533` | 4 | 1.0, 3.2, 6.2, 2.2 | 1, 18, 69, 8 | 2, 26, 97, 18 | right_side_empty | — | — |
| 510 | `tab:primary_data_outcome_map` | `chapters/chapter3_research_methods.tex:1476` | 3 | 2.7, 7.6, 2.9 | 6, 50, 7 | 12, 76, 12 | right_side_empty | — | — |
| 532 | `tab:primary_flow` | `chapters/chapter3_research_methods.tex:1983` | 4 | 1.0, 3.0, 5.9, 2.7 | 2, 16, 66, 14 | 5, 23, 104, 21 | right_side_empty | — | — |
| 613 | `tab:research_anatomy` | `chapters/chapter3_research_methods.tex:2733` | 6 | 1.0, 2.5, 2.0, 2.0, 2.1, 2.0 | 2, 123, 69, 80, 90, 64 | 3, 182, 99, 100, 148, 116 | tall_column | Col2 squeezed: 123 chars in 2.5cm = 49 chars/cm (forces wrap) | Col3 squeezed: 69 chars in 2.0cm = 34 chars/cm (forces wrap) | Widen col2 to p{15.4cm} | Widen col3 to p{8.6cm} |
| 617 | `tab:primary_iv_dv_framework` | `chapters/chapter3_research_methods.tex:2775` | 5 | 1.0, 2.0, 2.4, 3.4, 3.3 | 2, 33, 52, 103, 100 | 3, 75, 106, 150, 147 | tall_column | Col2 squeezed: 33 chars in 2.0cm = 16 chars/cm (forces wrap) | Col3 squeezed: 52 chars in 2.4cm = 22 chars/cm (forces wrap) | Widen col2 to p{4.1cm} | Widen col3 to p{6.5cm} |
| 627 | `tab:ethics_consent_anchor` | `chapters/chapter3_research_methods.tex:2888` | 5 | 1.0, 2.9, 3.0, 2.8, 2.4 | 2, 62, 67, 60, 43 | 5, 110, 93, 99, 94 | tall_column | Col2 squeezed: 62 chars in 2.9cm = 21 chars/cm (forces wrap) | Col3 squeezed: 67 chars in 3.0cm = 22 chars/cm (forces wrap) | Widen col2 to p{7.8cm} | Widen col3 to p{8.4cm} |
| 656 | `tab:b2c_research_gap_catalog` | `chapters/chapter3_research_methods.tex:3259` | 4 | 1.0, 9.5, 1.0, 1.0 | 2, 54, 4, 3 | 3, 69, 10, 9 | width_imbalanced | — | — |
| 665 | `tab:b2b_research_gap_catalog` | `chapters/chapter3_research_methods.tex:3436` | 4 | 1.0, 7.2, 3.4, 1.0 | 2, 47, 10, 3 | 3, 74, 59, 9 | width_imbalanced | — | — |
| 669 | `tab:customer_smart_flow` | `chapters/chapter3_research_methods.tex:3566` | 4 | 1.0, 3.6, 5.0, 3.0 | 1, 23, 46, 17 | 4, 32, 53, 27 | right_side_empty | — | — |
| 675 | `tab:iv_dv_master_reference` | `chapters/chapter3_research_methods.tex:3661` | 6 | 3.2, 1.5, 1.0, 1.0, 1.0, L | 17, 6, 1, 1, 1, 28 | 33, 15, 3, 3, 12, 51 | multi_page | — | — |
| 699 | `tab:ch3_b2b_b2c_questionnaire` | `chapters/chapter3_research_methods.tex:4081` | 5 | 1.5, 6.5, 1.5, 1.5, 1.5 | 3, 72, 16, 0, 0 | 6, 299, 21, 3, 3 | multi_page | Col2 has max 299 chars in 6.5cm = 7+ lines per cell → tall rows | Mixed long+short cols: cols [2] have long content vs cols [1, 4, 5] short — rows inh | Consider widening col2 or splitting content | Widen long col to reduce wrap (smaller max height → less wasted space in s |
| 703 | `tab:ch3_analysis_methods_xstream` | `chapters/chapter3_research_methods.tex:4149` | 5 | 3.5, L, 1.0, 1.3, 1.0 | 25, 21, 3, 2, 1 | 52, 37, 23, 9, 6 |  | — | — |
| 709 | `tab:ch3_todo_status_xstream` | `chapters/chapter3_research_methods.tex:4259` | 5 | 3.0, 1.5, 1.5, 1.5, L | 21, 1, 2, 2, 16 | 35, 7, 9, 6, 37 |  | — | — |
| 719 | `tab:scale_design` | `chapters/chapter3_research_methods.tex:4458` | 3 | 3.6, 8.6, 1.0 | 10, 59, 4 | 17, 79, 5 | width_imbalanced | — | — |
| 761 | `tab:remaining_ai_capability_matrix` | `chapters/chapter3_research_methods.tex:5307` | 6 | 2.0, 2.4, 2.1, 2.0, 2.0, 2.2 | 15, 156, 122, 106, 105, 131 | 33, 276, 236, 236, 191, 242 | tall_column | Col2 squeezed: 156 chars in 2.4cm = 65 chars/cm (forces wrap) | Col3 squeezed: 122 chars in 2.1cm = 58 chars/cm (forces wrap) | Widen col2 to p{19.4cm} | Widen col3 to p{15.2cm} |
| 956 | `tab:mcp_tools` | `appendices/C_ch3_supp_p267_w1470.tex:533` | 4 | 1.0, 1.0, 7.0, 3.6 | 5, 1, 40, 11 | 11, 9, 58, 14 | right_side_empty; width_imbalanced | — | — |
| 968 | `tab:responsible_ai_summary` | `appendices/C_ch3_supp_p267_w1470.tex:881` | 4 | 2.0, 2.5, L, L | 1, 14, 48, 39 | 17, 23, 63, 54 |  | — | — |
| 974 | `tab:eeg_existing_failures` | `appendices/C_ch3_supp_p267_w1470.tex:1061` | 3 | 3.5, 6.3, 3.5 | 20, 64, 20 | 27, 95, 24 | right_side_empty | — | — |
| 1002 | `tab:asd_questionnaire_blueprint` | `chapters/chapter3_research_methods.tex:4327` | 5 | 1.6, 0.9, L, 0.6, 2.0 | 11, 7, 31, 4, 22 | 17, 9, 43, 5, 25 |  | — | — |
| 1002 | `tab:asd_questionnaire_blueprint` | `appendices/C_ch3_supp_p267_w1470.tex:1672` | 5 | 2.4, 1.5, 5.3, 1.5, 1.5 | 14, 7, 31, 4, 2 | 23, 10, 43, 5, 15 |  | — | — |
| 1004 | `tab:pd_questionnaire_blueprint` | `chapters/chapter3_research_methods.tex:4423` | 5 | 1.6, 0.9, L, 0.6, 2.0 | 12, 7, 31, 4, 19 | 16, 9, 42, 5, 22 |  | — | — |
| 1004 | `tab:pd_questionnaire_blueprint` | `appendices/C_ch3_supp_p267_w1470.tex:1701` | 5 | 2.5, 1.5, 5.2, 1.5, 1.5 | 15, 8, 31, 4, 2 | 23, 10, 42, 5, 15 |  | — | — |
| 1007 | `tab:eeg_40step_pipeline` | `appendices/C_ch3_supp_p267_w1470.tex:1762` | 5 | L, 2.1, L, L, L | 2, 13, 31, 23, 23 | 2, 18, 50, 44, 40 | multi_page | — | — |
| 1023 | `tab:thesis_objective_alignment` | `appendices/C_ch3_supp_p267_w1470.tex:2233` | 7 | 3.0, 1.7, 1.8, 2.0, 1.8, 2.1, 2.6 | 36, 11, 14, 14, 13, 16, 8 | 55, 15, 22, 26, 19, 25, 16 | right_side_empty | Col1 squeezed: 36 chars in 3.0cm = 12 chars/cm (forces wrap) | Widen col1 to p{4.6cm} |
| 1039 | `tab:appc_partd_reference_full` | `appendices/C_ch3_supp_p267_w1470.tex:4054` | 3 | 5.8, 3.2, 4.2 | 10, 27, 36 | 19, 54, 56 |  | — | — |
| 1080 | `tab:ch4_triangulation` | `chapters/chapter4_analysis_findings.tex:500` | 4 | 2.1, 2.2, 5.0, 3.2 | 14, 16, 79, 32 | 19, 38, 111, 120 | tall_column | Col3 squeezed: 79 chars in 5.0cm = 16 chars/cm (forces wrap) | Widen col3 to p{9.9cm} |
| 1082 | `tab:ch4_org_interpretation` | `chapters/chapter4_analysis_findings.tex:533` | 3 | 1.0, 3.7, 8.5 | 2, 35, 179 | 3, 55, 255 | width_imbalanced | Col3 squeezed: 179 chars in 8.5cm = 21 chars/cm (forces wrap) | Col3 has max 255 chars in 8.5cm = 6+ lines per cell → tall rows | Widen col3 to p{22.4cm} | Consider widening col3 or splitting content |
| 1088 | `tab:ch4_findings_snapshot` | `chapters/chapter4_analysis_findings.tex:616` | 6 | 0.6, L, 1.4, 1.1, 1.3, 1.3 | 2, 38, 5, 21, 22, 17 | 2, 67, 8, 47, 50, 42 |  | — | — |
| 1089 | `tab:ch4_model_performance_snapshot` | `chapters/chapter4_analysis_findings.tex:646` | 7 | 2.6, 1.0, 0.8, 1.0, 1.1, 1.2, L | 12, 4, 4, 4, 5, 2, 14 | 19, 6, 4, 7, 7, 4, 20 |  | — | — |
| 1096 | `tab:ch4_hybrid_findings_summary` | `chapters/chapter4_analysis_findings.tex:774` | 4 | 1.0, 4.2, 5.3, 2.1 | 3, 62, 100, 16 | 4, 86, 151, 70 | right_side_empty | Col2 squeezed: 62 chars in 4.2cm = 15 chars/cm (forces wrap) | Col3 squeezed: 100 chars in 5.3cm = 19 chars/cm (forces wrap) | Widen col2 to p{7.7cm} | Widen col3 to p{12.5cm} |
| 1128 | `tab:ch4_partb_ivdv_results` | `chapters/chapter4_analysis_findings.tex:1939` | 6 | 2.5, 2.5, 1.8, 1.5, 1.2, L | 14, 12, 10, 7, 4, 14 | 19, 18, 14, 18, 12, 24 |  | — | — |
| 1208 | `tab:kpi_evidence_realised` | `chapters/chapter4_analysis_findings.tex:6154` | 5 | 2.2, 3.4, 1.9, 2.6, L | 17, 24, 13, 24, 18 | 21, 36, 24, 32, 33 |  | — | — |
| 1235 | `tab:appd_mediation_detail` | `appendices/D_ch4_supp_p390_w814.tex:117` | 7 | 3.6, 2.0, 1.0, 1.0, 1.0, 1.0, 2.0 | 170, 23, 4, 4, 4, 1, 46 | 338, 23, 4, 4, 4, 1, 46 | tall_column | Col1 squeezed: 170 chars in 3.6cm = 47 chars/cm (forces wrap) | Col7 squeezed: 46 chars in 2.0cm = 23 chars/cm (forces wrap) | Widen col1 to p{21.2cm} | Widen col7 to p{5.8cm} |
| 1243 | `tab:eval_explain_trust` | `appendices/D_ch4_supp_p390_w814.tex:317` | 3 | 4.4, 7.8, 1.0 | 28, 88, 5 | 39, 116, 12 | width_imbalanced | — | — |
| 1269 | `tab:ch4_alignment` | `chapters/chapter4_analysis_findings.tex:922` | 4 | 1.0, 1.0, 7.0, 3.6 | 3, 2, 46, 12 | 3, 3, 88, 22 | right_side_empty; width_imbalanced | — | — |
| 1269 | `tab:ch4_alignment` | `appendices/D_ch4_supp_p390_w814.tex:1345` | 4 | 0.5, 0.4, L, 2.8 | 3, 2, 40, 7 | 3, 3, 71, 13 | right_side_empty | — | — |
| 1297 | `tab:appd_partd_framework_quality_full` | `appendices/D_ch4_supp_p390_w814.tex:2334` | 5 | 6.4, 1.9, 1.6, 1.5, 1.5 | 12, 15, 13, 5, 10 | 23, 25, 35, 20, 16 |  | — | — |
| 1328 | `tab:ch5_final_defence_checklist` | `chapters/chapter5_discussion_recommendations.tex:648` | 4 | 1.0, 7.0, 3.6, 1.0 | 1, 46, 12, 3 | 2, 95, 18, 3 | width_imbalanced | — | — |
| 1350 | `tab:final_evidence_decision` | `appendices/L_technical_ops_p685.tex:1254` | 3 | 6.3, 4.7, 2.2 | 48, 27, 6 | 73, 35, 8 | right_side_empty | — | — |
| 1380 | `tab:contributions_summary` | `chapters/chapter5_discussion_recommendations.tex:2259` | 3 | L, L, L | 4, 38, 35 | 15, 50, 44 |  | — | — |
| 1398 | `tab:stakeholder_value` | `chapters/chapter5_discussion_recommendations.tex:2932` | 4 | L, L, L, L | 6, 12, 34, 25 | 15, 19, 44, 39 |  | — | — |
| 1415 | `tab:consent_protocol` | `chapters/chapter5_discussion_recommendations.tex:3615` | 5 | 1.0, 2.2, 4.7, 2.0, 2.6 | 1, 28, 130, 12, 41 | 2, 34, 169, 22, 183 | tall_column | Col3 squeezed: 130 chars in 4.7cm = 28 chars/cm (forces wrap) | Col5 squeezed: 41 chars in 2.6cm = 16 chars/cm (forces wrap) | Widen col3 to p{16.2cm} | Widen col5 to p{5.1cm} |
| 1425 | `tab:ch5_partd_combined_verdict` | `chapters/chapter5_discussion_recommendations.tex:3816` | 6 | 2.2, L, L, L, L, L | 14, 3, 8, 10, 28, 7 | 18, 17, 36, 10, 52, 7 |  | — | — |
| 1433 | `tab:ch5_final_verdict` | `chapters/chapter5_discussion_recommendations.tex:4047` | 3 | 2.8, 2.0, 8.4 | 11, 6, 101 | 14, 8, 244 | width_imbalanced | Col3 has max 244 chars in 8.4cm = 6+ lines per cell → tall rows | Mixed long+short cols: cols [3] have long content vs cols [1, 2] short — rows inheri | Consider widening col3 or splitting content | Widen long col to reduce wrap (smaller max height → less wasted space in s |
| 1441 | `tab:ch5_assessment_framework` | `chapters/chapter5_discussion_recommendations.tex:4250` | 6 | 2.0, 2.5, 2.0, 1.5, 1.5, L | 7, 10, 11, 2, 7, 10 | 9, 13, 13, 3, 18, 11 |  | — | — |
| 1449 | `tab:claims_boundary` | `chapters/chapter5_discussion_recommendations.tex:4414` | 3 | L, L, L | 2, 34, 32 | 10, 53, 46 |  | — | — |
| 1478 | `tab:hospital_npv_phase2` | `chapters/chapter5_discussion_recommendations.tex:5894` | 5 | 3.0, 2.0, 2.0, 2.0, L | 29, 6, 12, 7, 36 | 42, 10, 36, 9, 57 |  | — | — |
| 1512 | `tab:smart_e_contract` | `chapters/chapter5_discussion_recommendations.tex:6306` | 3 | 1.2, 3.2, L | 1, 10, 53 | 1, 14, 91 |  | — | — |
| 1521 | `tab:ch5_hybrid_convergence_assumed` | `chapters/chapter5_discussion_recommendations.tex:6470` | 7 | 0.7, 1.2, 1.2, 1.2, 1.2, 2.4, L | 3, 5, 3, 4, 1, 9, 13 | 3, 32, 9, 5, 5, 13, 34 |  | — | — |
| 1538 | `tab:ch5_per_chapter_data_summary` | `chapters/chapter5_discussion_recommendations.tex:6815` | 5 | 1.0, 3.2, 3.4, 2.1, 2.2 | 1, 59, 66, 26, 28 | 3, 85, 102, 112, 44 | tall_column | Col2 squeezed: 59 chars in 3.2cm = 18 chars/cm (forces wrap) | Col3 squeezed: 66 chars in 3.4cm = 20 chars/cm (forces wrap) | Widen col2 to p{7.4cm} | Widen col3 to p{8.3cm} |
| 1548 | `tab:dash_workflow_visual_purpose` | `appendices/E_ch5_supp_p525_w1059.tex:101` | 3 | 3.4, 6.4, 3.4 | 17, 61, 18 | 25, 74, 26 | right_side_empty | — | — |
| 1561 | `tab:app_ch5_audit_pillars` | `appendices/E_ch5_supp_p525_w1059.tex:417` | 4 | L, L, L, L | 2, 22, 3, 63 | 6, 41, 10, 94 |  | — | — |
| 1593 | `tab:adoption_kpi_framework` | `appendices/E_ch5_supp_p525_w1059.tex:1445` | 4 | 1.5, L, 2.1, L | 5, 24, 9, 19 | 11, 36, 17, 26 |  | — | — |
| 1593 | `tab:adoption_kpi_framework` | `appendices/L_technical_ops_p685.tex:671` | 4 | 1.2, L, 1.6, L | 5, 25, 9, 22 | 11, 36, 17, 36 |  | — | — |
| 1616 | `tab:survey_reliability_strategy` | `appendices/F_survey_instrument_p566_w1285.tex:156` | 3 | 4.3, 6.2, 2.7 | 18, 37, 7 | 21, 54, 41 | right_side_empty | — | — |
| 1646 | `tab:survey_section_d_algo` | `appendices/F_survey_instrument_p566_w1285.tex:632` | 7 | 1.0, 3.0, 2.8, 1.0, 1.0, 1.0, 1.0 | 2, 77, 65, 1, 1, 1, 1 | 2, 170, 191, 1, 1, 1, 2 | tall_column | Col2 squeezed: 77 chars in 3.0cm = 26 chars/cm (forces wrap) | Col3 squeezed: 65 chars in 2.8cm = 23 chars/cm (forces wrap) | Widen col2 to p{9.7cm} | Widen col3 to p{8.1cm} |
| 1652 | `tab:survey_section_d_reg` | `appendices/F_survey_instrument_p566_w1285.tex:737` | 7 | 1.0, 3.3, 2.5, 1.0, 1.0, 1.0, 1.0 | 3, 102, 57, 1, 1, 1, 1 | 3, 195, 167, 1, 1, 1, 2 | tall_column | Col2 squeezed: 102 chars in 3.3cm = 31 chars/cm (forces wrap) | Col3 squeezed: 57 chars in 2.5cm = 23 chars/cm (forces wrap) | Widen col2 to p{12.7cm} | Widen col3 to p{7.1cm} |
| 1655 | `tab:survey_section_e_diag` | `appendices/F_survey_instrument_p566_w1285.tex:770` | 7 | 1.0, 3.1, 2.7, 1.0, 1.0, 1.0, 1.0 | 2, 90, 65, 1, 1, 1, 1 | 2, 207, 192, 1, 1, 1, 2 | tall_column | Col2 squeezed: 90 chars in 3.1cm = 29 chars/cm (forces wrap) | Col3 squeezed: 65 chars in 2.7cm = 24 chars/cm (forces wrap) | Widen col2 to p{11.2cm} | Widen col3 to p{8.1cm} |
| 1669 | `tab:survey_section_g` | `appendices/F_survey_instrument_p566_w1285.tex:981` | 3 | 1.0, 7.7, 4.5 | 2, 191, 66 | 2, 483, 217 | width_imbalanced | Col2 squeezed: 191 chars in 7.7cm = 25 chars/cm (forces wrap) | Col3 squeezed: 66 chars in 4.5cm = 15 chars/cm (forces wrap) | Widen col2 to p{23.9cm} | Widen col3 to p{8.3cm} |
| 1679 | `tab:survey_b2c_primary_addendum` | `appendices/F_survey_instrument_p566_w1285.tex:1126` | 3 | 1.0, 9.0, 3.2 | 4, 85, 11 | 5, 140, 13 | right_side_empty; width_imbalanced | — | — |
| 1686 | `tab:survey_analysis_full` | `appendices/F_survey_instrument_p566_w1285.tex:1290` | 4 | 1.0, 3.1, 5.7, 2.8 | 1, 22, 73, 18 | 2, 34, 110, 31 | right_side_empty | Col3 squeezed: 73 chars in 5.7cm = 13 chars/cm (forces wrap) | Widen col3 to p{9.1cm} |
| 1716 | `tab:appo_tech_research_map` | `appendices/H_rgaig_architecture_p605_w1135.tex:39` | 3 | 4.2, 8.0, 1.0 | 21, 80, 5 | 36, 105, 8 | width_imbalanced | — | — |
| 1727 | `tab:appo_maturity_arch` | `appendices/H_rgaig_architecture_p605_w1135.tex:302` | 3 | 1.0, 3.0, 9.2 | 1, 10, 91 | 3, 15, 127 | width_imbalanced | Col2 has 3.0cm width but only 10 avg chars — wasted ~1.5cm | Narrow col2 to p{1.5cm} |
| 1729 | `tab:appo_gov_dimensions` | `appendices/H_rgaig_architecture_p605_w1135.tex:335` | 3 | 3.7, 8.5, 1.0 | 12, 62, 5 | 15, 81, 8 | width_imbalanced | — | — |
| 1737 | `tab:appo_principles` | `appendices/H_rgaig_architecture_p605_w1135.tex:464` | 3 | 1.0, 4.6, 7.6 | 5, 25, 68 | 10, 38, 171 | width_imbalanced | Mixed long+short cols: cols [3] have long content vs cols [1] short — rows inherit max height of long col, short cols show whitespace | Widen long col to reduce wrap (smaller max height → less wasted space in short cols) |
| 1758 | `tab:appo_audit_fields` | `appendices/H_rgaig_architecture_p605_w1135.tex:960` | 2 | 4.0, L | 0, 36 | 5, 103 |  | Col1 has 4.0cm width but only 0 avg chars — wasted ~2.5cm | Narrow col1 to p{1.5cm} |
| 1768 | `tab:appo_dr` | `appendices/H_rgaig_architecture_p605_w1135.tex:1204` | 4 | 2.7, 6.0, 1.0, 2.9 | 7, 34, 4, 8 | 9, 49, 7, 18 | right_side_empty | — | — |
| 1805 | `tab:appj_accessibility` | `appendices/J_human_centered_ecosystem_p680.tex:163` | 3 | 3.0, 6.9, 3.3 | 12, 63, 14 | 20, 91, 61 | right_side_empty | — | — |
| 1809 | `tab:appj_consent` | `appendices/J_human_centered_ecosystem_p680.tex:252` | 3 | 3.4, 6.2, 3.6 | 15, 48, 16 | 20, 65, 45 | right_side_empty | — | — |
| 1818 | `tab:appj_value` | `appendices/J_human_centered_ecosystem_p680.tex:453` | 3 | 2.9, 6.7, 3.5 | 9, 50, 14 | 14, 68, 21 | right_side_empty | — | — |
| 1854 | `tab:governance_safety` | `appendices/L_technical_ops_p685.tex:419` | 3 | 3.7, 6.3, 3.2 | 15, 44, 11 | 25, 57, 14 | right_side_empty | — | — |
| 1872 | `tab:eeg_adopt_pilot_defer` | `appendices/L_technical_ops_p685.tex:938` | 2 | 9.1, 4.7 | 59, 16 | 96, 34 | right_side_empty | — | — |
| 1878 | `tab:b2b_decision` | `appendices/L_technical_ops_p685.tex:1196` | 4 | L, L, L, L | 13, 26, 38, 28 | 20, 48, 58, 52 |  | — | — |
| 1879 | `tab:b2c_decision` | `appendices/L_technical_ops_p685.tex:1223` | 4 | 2.0, 4.5, 4.4, 1.7 | 14, 31, 30, 12 | 20, 49, 38, 12 |  | — | — |
| 1908 | `tab:part_objectives` | `appendices/M_operationalization_detail_p725.tex:426` | 4 | 1.0, 9.5, 1.0, 1.0 | 2, 49, 2, 3 | 2, 62, 6, 9 | width_imbalanced | — | — |
| 1929 | `tab:appendix_n_timeline` | `appendices/N_indian_cohort_acquisition_p1090.tex:230` | 4 | 1.0, 3.0, 6.2, 2.5 | 1, 17, 73, 12 | 4, 25, 144, 17 | right_side_empty | — | — |
| 1943 | `tab:app_n_scorecard` | `appendices/O_governance_training_program.tex:99` | 5 | 0.6, L, 2.0, 1.4, 1.0 | 2, 25, 17, 8, 8 | 2, 50, 33, 14, 14 | multi_page | — | — |
| 1952 | `tab:app_n_authorisation` | `appendices/O_governance_training_program.tex:273` | 3 | 4.4, 6.0, 2.8 | 18, 33, 7 | 27, 172, 17 | right_side_empty | Mixed long+short cols: cols [2] have long content vs cols [3] short — rows inherit max height of long col, short cols show whitespace | Widen long col to reduce wrap (smaller max height → less wasted space in short cols) |
| 2002 | `tab:app_q_drill_anatomy` | `appendices/Q_drill_methodology.tex:55` | 3 | 1.0, 4.4, 7.8 | 1, 23, 72 | 2, 40, 120 | width_imbalanced | — | — |
| 2009 | `tab:app_r_arch` | `appendices/R_pipeline_reference_code.tex:24` | 2 | 3.4, L | 12, 50 | 28, 125 |  | — | — |
| 2011 | `tab:app_r_signatures` | `appendices/R_pipeline_reference_code.tex:57` | 5 | 1.2, 3.0, 2.6, 2.6, L | 2, 0, 0, 0, 25 | 2, 13, 10, 11, 34 | sparse_table | Col2 has 3.0cm width but only 0 avg chars — wasted ~1.5cm | Narrow col2 to p{1.5cm} |
| 2014 | `tab:app_r_phase5_stub` | `appendices/R_pipeline_reference_code.tex:103` | 2 | 3.4, L | 18, 13 | 33, 122 |  | — | — |
| 2016 | `tab:app_r_orchestrator` | `appendices/R_pipeline_reference_code.tex:142` | 2 | 3.4, L | 15, 14 | 29, 67 | sparse_table | — | — |
| 2018 | `tab:glossary_full` | `appendices/S_glossary.tex:11` | 2 | 2.6, L | 5, 66 | 17, 144 | multi_page; very_multi_page | — | — |
| ? | `NOLABEL@chapters/chapter1_introduction.tex:75` | `chapters/chapter1_introduction.tex:75` | 2 | L, L | 46, 29 | 63, 54 |  | — | — |
| ? | `NOLABEL@chapters/chapter1_introduction.tex:2158` | `chapters/chapter1_introduction.tex:2158` | 4 | 0.6, 3.0, L, 2.5 | 1, 14, 87, 12 | 2, 21, 120, 15 | right_side_empty | — | — |
| ? | `tab:doctoral_quality_chain` | `chapters/chapter1_introduction.tex:3965` | 5 | 1.0, 2.6, 3.1, 3.3, 2.0 | 1, 40, 55, 64, 23 | 2, 171, 73, 82, 34 | tall_column | Col2 squeezed: 40 chars in 2.6cm = 15 chars/cm (forces wrap) | Col3 squeezed: 55 chars in 3.1cm = 18 chars/cm (forces wrap) | Widen col2 to p{4.9cm} | Widen col3 to p{6.9cm} |
| ? | `NOLABEL@chapters/chapter2_literature.tex:74` | `chapters/chapter2_literature.tex:74` | 2 | L, L | 40, 20 | 75, 48 |  | — | — |
| ? | `NOLABEL@chapters/chapter2_literature.tex:1008` | `chapters/chapter2_literature.tex:1008` | 5 | 2.5, 3.0, L, L, L | 10, 9, 38, 4, 84 | 14, 22, 175, 4, 92 | tall_column | Col2 has 3.0cm width but only 9 avg chars — wasted ~1.5cm | Mixed long+short cols: cols [3] have long content vs cols [1, 2, 4] short — rows inherit m | Narrow col2 to p{1.5cm} | Widen long col to reduce wrap (smaller max height → less wasted space in short cols) |
| ? | `NOLABEL@chapters/chapter2_literature.tex:1068` | `chapters/chapter2_literature.tex:1068` | 5 | 2.3, L, L, L, L | 8, 105, 0, 0, 0 | 8, 105, 0, 0, 0 | right_side_empty; tall_column | — | — |
| ? | `NOLABEL@chapters/chapter2_literature.tex:1401` | `chapters/chapter2_literature.tex:1401` | 4 | 2.5, L, L, L | 3, 31, 16, 0 | 6, 54, 16, 0 | right_side_empty | — | — |
| ? | `NOLABEL@chapters/chapter2_literature.tex:1469` | `chapters/chapter2_literature.tex:1469` | 3 | L, L, L | 19, 197, 0 | 19, 197, 0 | right_side_empty; tall_column | Mixed long+short cols: cols [2] have long content vs cols [3] short — rows inherit max height of long col, short cols show whitespace | Widen long col to reduce wrap (smaller max height → less wasted space in short cols) |
| ? | `NOLABEL@chapters/chapter3_research_methods.tex:92` | `chapters/chapter3_research_methods.tex:92` | 2 | L, L | 43, 13 | 84, 35 | right_side_empty | — | — |
| ? | `NOLABEL@chapters/chapter3_research_methods.tex:1412` | `chapters/chapter3_research_methods.tex:1412` | 2 | L, L | 73, 31 | 134, 54 |  | — | — |
| ? | `NOLABEL@chapters/chapter3_research_methods.tex:1542` | `chapters/chapter3_research_methods.tex:1542` | 2 | L, L | 75, 25 | 123, 48 |  | — | — |
| ? | `NOLABEL@chapters/chapter3_research_methods.tex:1681` | `chapters/chapter3_research_methods.tex:1681` | 2 | L, L | 107, 26 | 163, 64 |  | — | — |
| ? | `NOLABEL@chapters/chapter3_research_methods.tex:8508` | `chapters/chapter3_research_methods.tex:8508` | 4 | 1.6, 3.5, 2.8, L | 8, 26, 17, 63 | 14, 36, 19, 83 |  | — | — |
| ? | `NOLABEL@chapters/chapter3_research_methods.tex:9208` | `chapters/chapter3_research_methods.tex:9208` | 5 | 0.6, 3.5, L, 1.8, L | 2, 45, 44, 20, 10 | 3, 79, 67, 40, 14 | right_side_empty | Col2 squeezed: 45 chars in 3.5cm = 13 chars/cm (forces wrap) | Widen col2 to p{5.7cm} |
| ? | `NOLABEL@chapters/chapter3_research_methods.tex:9903` | `chapters/chapter3_research_methods.tex:9903` | 4 | 2.2, 2.0, L, L | 1, 10, 32, 42 | 8, 14, 55, 66 |  | — | — |
| ? | `NOLABEL@chapters/chapter3_research_methods.tex:10042` | `chapters/chapter3_research_methods.tex:10042` | 6 | 1.4, 1.8, L, L, 1.5, 1.8 | 6, 333, 0, 0, 0, 0 | 6, 333, 0, 0, 0, 0 | tall_column | Col2 squeezed: 333 chars in 1.8cm = 185 chars/cm (forces wrap) | Col2 has max 333 chars in 1.8cm = 8+ lines per cell → tall rows | Widen col2 to p{41.6cm} | Consider widening col2 or splitting content |
| ? | `NOLABEL@chapters/chapter3_research_methods.tex:10899` | `chapters/chapter3_research_methods.tex:10899` | 4 | 2.5, L, 2.5, 2.5 | 17, 48, 26, 16 | 22, 60, 34, 50 | right_side_empty | — | — |
| ? | `NOLABEL@chapters/chapter3_research_methods.tex:11349` | `chapters/chapter3_research_methods.tex:11349` | 4 | 0.8, L, 3.8, 1.2 | 2, 67, 60, 55 | 2, 104, 128, 84 | tall_column | Col3 squeezed: 60 chars in 3.8cm = 16 chars/cm (forces wrap) | Col4 squeezed: 55 chars in 1.2cm = 46 chars/cm (forces wrap) | Widen col3 to p{7.5cm} | Widen col4 to p{6.9cm} |
| ? | `NOLABEL@chapters/chapter3_research_methods.tex:11462` | `chapters/chapter3_research_methods.tex:11462` | 3 | 3.5, L, L | 19, 38, 79 | 26, 138, 87 | tall_column | — | — |
| ? | `NOLABEL@chapters/chapter3_research_methods.tex:11490` | `chapters/chapter3_research_methods.tex:11490` | 3 | 2.2, L, 2.5 | 11, 125, 13 | 16, 150, 18 | right_side_empty | — | — |
| ? | `NOLABEL@chapters/chapter3_research_methods.tex:11513` | `chapters/chapter3_research_methods.tex:11513` | 3 | L, L, L | 2, 84, 9 | 3, 102, 16 | right_side_empty | — | — |
| ? | `NOLABEL@chapters/chapter3_research_methods.tex:11549` | `chapters/chapter3_research_methods.tex:11549` | 4 | L, L, L, L | 4, 54, 10, 7 | 6, 71, 13, 7 | right_side_empty | — | — |
| ? | `NOLABEL@chapters/chapter3_research_methods.tex:11897` | `chapters/chapter3_research_methods.tex:11897` | 3 | 1.5, 3.0, L | 1, 16, 78 | 8, 27, 106 |  | — | — |
| ? | `NOLABEL@chapters/chapter4_analysis_findings.tex:74` | `chapters/chapter4_analysis_findings.tex:74` | 2 | L, L | 36, 19 | 148, 52 |  | — | — |
| ? | `NOLABEL@chapters/chapter4_analysis_findings.tex:813` | `chapters/chapter4_analysis_findings.tex:813` | 4 | L, L, L, L | 12, 14, 23, 9 | 17, 23, 57, 23 |  | — | — |
| ? | `NOLABEL@chapters/chapter4_analysis_findings.tex:1469` | `chapters/chapter4_analysis_findings.tex:1469` | 6 | 3.1, L, 2.5, 2.5, L, L | 10, 3, 14, 16, 22, 23 | 19, 6, 22, 20, 97, 26 |  | — | — |
| ? | `NOLABEL@chapters/chapter4_analysis_findings.tex:1521` | `chapters/chapter4_analysis_findings.tex:1521` | 6 | 3.1, L, L, L, 1.8, L | 10, 3, 2, 6, 7, 15 | 19, 6, 5, 18, 13, 17 |  | — | — |
| ? | `NOLABEL@chapters/chapter4_analysis_findings.tex:1582` | `chapters/chapter4_analysis_findings.tex:1582` | 5 | 2.5, 2.5, 2.0, L, L | 12, 33, 18, 32, 6 | 18, 94, 30, 48, 6 | right_side_empty | Col2 squeezed: 33 chars in 2.5cm = 13 chars/cm (forces wrap) | Widen col2 to p{4.1cm} |
| ? | `NOLABEL@chapters/chapter4_analysis_findings.tex:2369` | `chapters/chapter4_analysis_findings.tex:2369` | 6 | L, L, L, L, L, L | 11, 3, 2, 2, 3, 13 | 19, 6, 3, 3, 5, 46 |  | — | — |
| ? | `NOLABEL@chapters/chapter4_analysis_findings.tex:3909` | `chapters/chapter4_analysis_findings.tex:3909` | 4 | 0.8, 1.4, L, 2.8 | 3, 15, 49, 18 | 3, 17, 105, 25 | right_side_empty | — | — |
| ? | `NOLABEL@chapters/chapter4_analysis_findings.tex:3931` | `chapters/chapter4_analysis_findings.tex:3931` | 4 | L, L, 1.4, L | 2, 38, 8, 13 | 2, 48, 9, 31 | right_side_empty | — | — |
| ? | `NOLABEL@chapters/chapter4_analysis_findings.tex:4563` | `chapters/chapter4_analysis_findings.tex:4563` | 7 | 0.8, 1.0, 0.5, 0.8, 0.9, 0.5, L | 1, 6, 2, 12, 5, 4, 8 | 7, 10, 2, 89, 5, 4, 54 |  | — | — |
| ? | `NOLABEL@chapters/chapter4_analysis_findings.tex:5155` | `chapters/chapter4_analysis_findings.tex:5155` | 5 | L, L, L, L, L | 10, 14, 3, 4, 3 | 19, 51, 4, 4, 4 |  | — | — |
| ? | `NOLABEL@chapters/chapter5_discussion_recommendations.tex:86` | `chapters/chapter5_discussion_recommendations.tex:86` | 2 | L, L | 45, 18 | 123, 38 |  | — | — |
| ? | `NOLABEL@chapters/chapter5_discussion_recommendations.tex:3217` | `chapters/chapter5_discussion_recommendations.tex:3217` | 4 | 0.6, 2.0, L, 2.8 | 2, 13, 66, 13 | 6, 17, 101, 20 | right_side_empty | — | — |
| ? | `NOLABEL@chapters/chapter5_discussion_recommendations.tex:3271` | `chapters/chapter5_discussion_recommendations.tex:3271` | 5 | 0.4, 2.5, L, L, 2.2 | 1, 10, 59, 73, 10 | 2, 16, 72, 85, 11 | right_side_empty | — | — |
| ? | `NOLABEL@chapters/chapter5_discussion_recommendations.tex:3460` | `chapters/chapter5_discussion_recommendations.tex:3460` | 5 | 0.3, 1.6, 3.2, 4.0, L | 1, 18, 45, 20, 18 | 2, 23, 60, 39, 34 | right_side_empty | Col3 squeezed: 45 chars in 3.2cm = 14 chars/cm (forces wrap) | Widen col3 to p{5.7cm} |
| ? | `NOLABEL@chapters/chapter5_discussion_recommendations.tex:4716` | `chapters/chapter5_discussion_recommendations.tex:4716` | 8 | L, L, L, L, L, L, L, L | 2, 16, 1, 1, 2, 41, 7, 1 | 3, 21, 1, 1, 3, 55, 14, 4 | right_side_empty | — | — |
| ? | `tab:app_gan_model_params` | `appendices/C_ch3_supp_p267_w1470.tex:216` | 4 | 2.1, 2.0, 3.7, 5.0 | 12, 9, 37, 69 | 20, 10, 136, 111 | tall_column | Col4 squeezed: 69 chars in 5.0cm = 14 chars/cm (forces wrap) | Widen col4 to p{8.6cm} |
| ? | `NOLABEL@appendices/C_ch3_supp_p267_w1470.tex:1475` | `appendices/C_ch3_supp_p267_w1470.tex:1475` | 3 | 1.6, 4.6, 8.0 | 9, 30, 222 | 9, 51, 364 | width_imbalanced; multi_page | Col3 squeezed: 222 chars in 8.0cm = 28 chars/cm (forces wrap) | Col3 has max 364 chars in 8.0cm = 9+ lines per cell → tall rows | Widen col3 to p{27.7cm} | Consider widening col3 or splitting content |
| ? | `NOLABEL@appendices/C_ch3_supp_p267_w1470.tex:2935` | `appendices/C_ch3_supp_p267_w1470.tex:2935` | 4 | 3.5, L, 2.0, L | 12, 9, 37, 69 | 20, 10, 136, 111 | tall_column | Col3 squeezed: 37 chars in 2.0cm = 18 chars/cm (forces wrap) | Widen col3 to p{4.6cm} |
| ? | `NOLABEL@appendices/C_ch3_supp_p267_w1470.tex:3228` | `appendices/C_ch3_supp_p267_w1470.tex:3228` | 5 | 0.4, 2.8, 2.5, L, 2.2 | 1, 20, 20, 46, 10 | 2, 42, 30, 59, 24 | right_side_empty | — | — |
| ? | `NOLABEL@appendices/C_data_certificates_p267_w384.tex:341` | `appendices/C_data_certificates_p267_w384.tex:341` | 2 | 6.0, 6.0 | 20, 3 | 37, 5 |  | Col2 has 6.0cm width but only 3 avg chars — wasted ~4.5cm | Narrow col2 to p{1.5cm} |
| ? | `NOLABEL@appendices/D_ch4_supp_p390_w814.tex:1862` | `appendices/D_ch4_supp_p390_w814.tex:1862` | 4 | 3.5, L, L, 2.0 | 4, 3, 4, 8 | 19, 9, 11, 8 | multi_page; sparse_table | Col1 has 3.5cm width but only 4 avg chars — wasted ~2.0cm | Narrow col1 to p{1.5cm} |
| ? | `NOLABEL@appendices/D_ch4_supp_p390_w814.tex:1986` | `appendices/D_ch4_supp_p390_w814.tex:1986` | 10 | 1.4, L, L, L, L, L, L, L, L, L | 3, 4, 4, 4, 3, 3, 3, 2, 2, 3 | 5, 5, 5, 5, 5, 5, 5, 4, 5, 4 |  | — | — |
| ? | `NOLABEL@appendices/E_ch5_supp_p525_w1059.tex:1613` | `appendices/E_ch5_supp_p525_w1059.tex:1613` | 8 | L, L, L, L, L, L, L, L | 2, 16, 1, 1, 2, 41, 7, 1 | 3, 21, 1, 1, 3, 55, 14, 4 | right_side_empty | — | — |
| ? | `tab:ai_figs_ch1` | `appendices/I_ai_decl_detail_p632_w127.tex:36` | 5 | 1.2, 2.6, 3.0, 1.0, L | 2, 0, 21, 3, 47 | 2, 5, 22, 3, 54 |  | — | — |
| ? | `tab:ai_figs_ch2` | `appendices/I_ai_decl_detail_p632_w127.tex:74` | 5 | 1.2, 2.6, 3.0, 1.0, L | 2, 1, 19, 3, 43 | 2, 5, 22, 3, 54 |  | — | — |
| ? | `tab:ai_figs_ch3` | `appendices/I_ai_decl_detail_p632_w127.tex:100` | 5 | 1.2, 2.6, 3.0, 1.0, L | 2, 0, 22, 3, 48 | 2, 5, 31, 7, 55 | multi_page | — | — |
| ? | `tab:ai_figs_ch4` | `appendices/I_ai_decl_detail_p632_w127.tex:149` | 5 | 1.2, 2.6, 3.0, 1.0, L | 2, 0, 19, 3, 48 | 2, 5, 22, 3, 54 |  | — | — |
| ? | `tab:ai_figs_ch5` | `appendices/I_ai_decl_detail_p632_w127.tex:183` | 5 | 1.2, 2.6, 3.0, 1.0, L | 2, 0, 21, 3, 47 | 2, 5, 22, 3, 54 |  | — | — |
| ? | `tab:brutal_appendices` | `appendices/I_brutal_feedback_p632_w64.tex:41` | 10 | 3.0, 1.5, 1.5, 1.5, 1.5, 1.5, 1.5, 1.5, 1.5, L | 18, 2, 3, 1, 3, 1, 4, 3, 1, 22 | 26, 4, 5, 4, 5, 4, 5, 7, 5, 30 | multi_page; very_multi_page | — | — |
| ? | `tab:examiner_readiness` | `appendices/I_examiner_readiness_p632_w28.tex:20` | 4 | 1.5, 3.4, 6.2, 1.5 | 3, 21, 37, 6 | 4, 31, 63, 36 | multi_page | — | — |
| ? | `NOLABEL@appendices/L_technical_ops_p685.tex:460` | `appendices/L_technical_ops_p685.tex:460` | 5 | 0.4, 1.8, L, 1.8, 1.8 | 1, 16, 90, 16, 99 | 2, 23, 193, 26, 201 | tall_column | Col5 squeezed: 99 chars in 1.8cm = 55 chars/cm (forces wrap) | Col5 has max 201 chars in 1.8cm = 5+ lines per cell → tall rows | Widen col5 to p{12.3cm} | Consider widening col5 or splitting content |
| ? | `tab:research_objectives` | `appendices/M_operationalization_detail_p725.tex:502` | 3 | 1.0, 9.5, 2.7 | 2, 69, 6 | 3, 91, 7 | right_side_empty; width_imbalanced | — | — |
| ? | `tab:smart_objectives` | `appendices/M_operationalization_detail_p725.tex:635` | 6 | 1.0, 2.4, 2.4, 2.1, 2.2, 2.0 | 2, 58, 55, 41, 47, 16 | 3, 119, 87, 61, 60, 25 | tall_column | Col2 squeezed: 58 chars in 2.4cm = 24 chars/cm (forces wrap) | Col3 squeezed: 55 chars in 2.4cm = 23 chars/cm (forces wrap) | Widen col2 to p{7.2cm} | Widen col3 to p{6.8cm} |
| ? | `tab:rq_mapping` | `appendices/M_operationalization_detail_p725.tex:677` | 3 | 1.0, 9.5, 1.0 | 3, 108, 4 | 4, 167, 11 | width_imbalanced | Mixed long+short cols: cols [2] have long content vs cols [1, 3] short — rows inherit max height of long col, short cols show whitespace | Widen long col to reduce wrap (smaller max height → less wasted space in short cols) |

