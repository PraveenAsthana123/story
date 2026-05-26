---
layout: default
title: DBA Doctoral Submission — Praveen K Asthana
---

# DBA Doctoral Submission

**Author:** Praveen K Asthana  
**Programme:** Doctorate in Business Administration (Generative AI)  
**Institution:** Golden Gate University, San Francisco  
**Doctoral Supervisor:** C. Ranjeeth Kumar  
**Co-Supervisor / Chair:** Sumitra Padmanabhan  
**Submission Target:** June 2026

---

## Title

> **A Governance Framework for Responsible Explainable AI-Assisted Retrospective EEG-Based Neuropsychiatric Decision Support Under Human Clinical Oversight**

### Subtitle

> *Integrating Generative AI, Retrieval-Augmented Generation, and Continuous Monitoring for Clinical and Consumer Healthcare Applications*

---

## Six Deliverables

Read in numbered order. Each link opens the PDF in your browser; no download required.

### 1. [Topic Proposal v2.1 (Enhanced)](1_topic_proposal.pdf) — 39 pages
Committee-facing proposal: scope, problem, solution, methodology overview, GGU Ch.1+Ch.2 bullet coverage, substantive Literature Review excerpt, named supervisor + co-supervisor.

### 2. [Dissertation v3 (GGU-Strict)](2_dissertation_proposal.pdf) — 78 pages
GGU-strict skeleton (47 bullets covered) + **40 enhanced sections** (E1–E40): figures, tables, agentic AI, infrastructure, RAI/XAI/Fairness/Bias/Outlier/Interpretable/Portable, NIST AI RMF + ISO/IEC 42001, SMART aim, C4 architecture, 23-step pipeline, B2B+B2C, 5-pillar model integrity, MLOps + 12-tier testing, falsifiable hypotheses. 50-entry References + Acknowledgements + GGU↔main-thesis cross-ref.

### 3. [Main Dissertation (Full Thesis)](3_main_dissertation_full_thesis.pdf) — 1127 pages
Complete doctoral dissertation: 5 chapters + 14 appendices + 23-step ASD pipeline flowchart in Ch.3 + full Acknowledgements naming both supervisors + 424-entry references.bib.

### 4. [ASD Literature Review (Standalone)](4_asd_literature_review.pdf) — 10 pages
Consolidated companion to the dissertation: PRISMA cascade (2,847 → 156 papers) + 6 themes (Classical ML / DL / Connectivity+Multimodal / Feature Optimisation / Early Detection / Governance+Trust) + 50 citations **including the candidate's own 2025 ICSIT publication** + 5 gaps G1–G5 with RGAIG closure mechanism.

### 5. [RGAIG ASD Clinical Questionnaire](5_asd_questionnaire.pdf) — 6 pages
Primary data instrument: **B2C track** (Sections A–F, 48 items: Demographics + Behavioural + Psychological + Social + Diagnostic + AI Acceptance) + **B2B track** (Sections G–I, 21 items: Governance Maturity + HITL Effectiveness + Operational Integration). Variable map: 6 IVs + 6 DVs + 1 Mediator + 2 Moderators → H1–H5. HIPAA / GDPR / DPDP-compliant consent.

### 6. [Chapter 2 Flow Document — ASD-Specific](6_ch2_flow_document_asd.pdf) — 7 pages
ASD-specific Ch.2 walkthrough: chapter claim + journey map + PRISMA cascade + 6 themes + **9 theoretical foundations** (4 technical + 5 organisational) + 5 hypotheses with falsifiability decision criteria + SWOT + CMM maturity of biomedical AI + RTAI ethics + critical contradictions in the literature.

---

## Cross-Deliverable Alignment

| Aspect | 1 | 2 | 3 | 4 | 5 | 6 |
|---|---|---|---|---|---|---|
| Title + subtitle | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ |
| Supervisor names | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ |
| Literature review | ✓ | ✓ | ✓ | ✓ (full) | — | ✓ |
| Hypotheses H1–H5 (falsifiable) | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ |
| PRISMA cascade | — | ✓ | ✓ | ✓ | — | ✓ |
| References [1]–[50] | partial | ✓ | ✓ (424 main bib) | ✓ | — | implied |
| B2C + B2B framing | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ |

---

## Reading Order for Examiners

1. **Start with [`1_topic_proposal.pdf`](1_topic_proposal.pdf)** (39 pp) for the one-glance scope.
2. **Then [`2_dissertation_proposal.pdf`](2_dissertation_proposal.pdf)** (78 pp) for the GGU-strict skeleton + 40 enhanced sections.
3. **Then [`3_main_dissertation_full_thesis.pdf`](3_main_dissertation_full_thesis.pdf)** (1127 pp) for the complete evidence + appendices.
4. **Supporting [`4_asd_literature_review.pdf`](4_asd_literature_review.pdf)** (10 pp) for the standalone lit review.
5. **Supporting [`5_asd_questionnaire.pdf`](5_asd_questionnaire.pdf)** (6 pp) for the primary-data instrument.
6. **Supporting [`6_ch2_flow_document_asd.pdf`](6_ch2_flow_document_asd.pdf)** (7 pp) for the ASD-specific Ch.2 walkthrough.

---

## Framework Implementation — 6 Portals + 1 Mobile App

The RGAIG framework is **implemented and operational**, not merely theoretical. The reference implementation spans six web portals and a cross-platform mobile companion, demonstrating practitioner relevance + technical feasibility (the dissertation's DBA-grade contribution). Source for these portals is maintained outside this repository for size reasons; the inventory below documents what exists.

| # | Portal / App | Technology | Purpose | Hosting model |
|---|---|---|---|---|
| 1 | **[RGAIG_PORTAL](portal/)** ← LIVE | Vanilla HTML + CSS + JS | Framework dashboard: [`index.html`](portal/index.html) + [`admin.html`](portal/admin.html) + [`asd.html`](portal/asd.html) + [`architecture.html`](portal/architecture.html) + [`survey.html`](portal/survey.html) | **Deployed to `/portal/` on GitHub Pages** |
| 2 | **rgaig-asd-app** | Python (Flask + FastAPI) + RAG engine + agentic backend | Live agentic ASD screening reference impl with planner / decomposer / policy / council patterns (per dissertation §E23) | Server (local / cloud) |
| 3 | **rgaig-survey** | React + TypeScript SPA (Create React App) | Modern typed survey frontend for B2C + B2B questionnaire delivery | Static after build (Netlify / Vercel / Pages) |
| 4 | **survey_app** | Python Flask + SQLite + Jinja templates | B2C / B2B / SUS survey deployment with persistence (`survey_b2c.html`, `survey_pro.html`, `survey_sus.html`, `dashboard.html`) | Server with DB |
| 5 | **dc_aibf_app** | Flutter (Android + iOS + Web targets) | Cross-platform mobile RGAIG companion for caregiver-side capture | App stores / web build |
| 6 | **Legacy HTML portals** (THESIS_PORTAL, THESIS_MAIN_PORTAL, DATA_CERTIFICATION_PORTAL) | Static HTML | Earlier thesis-navigation surfaces; retained for traceability | Static (legacy, in `OLD/` archive) |

### Per-portal feature inventory

- **RGAIG_PORTAL/** — `index.html`, `admin.html`, `asd.html`, `architecture.html` + `architecture.pdf`, `survey.html`, `css/`, `js/`
- **rgaig-asd-app/** — `api_backend.py`, `app.py`, `asd_server.py`, `rag_engine.py`, `agents/`, `backend/`, `frontend/`, `frontend-asd/`, `data/`
- **rgaig-survey/** — React `src/` (components), `public/`, `package.json`, `tsconfig.json`
- **survey_app/** — `app.py`, `database.py`, `scoring.py`, `survey_data.db`, `templates/` (8 HTML pages), `static/`
- **dc_aibf_app/** — Flutter `lib/`, `pubspec.yaml`, multi-platform build targets

### What this means for examiners

The dissertation's RGAIG framework (deliverable 2 §E1–E40) is grounded in a working reference implementation. The 6 portals + mobile app demonstrate:

1. **Agentic AI in production** (rgaig-asd-app with planner + decomposer + policy + council per dissertation §E23)
2. **B2C + B2B questionnaire delivery** (rgaig-survey + survey_app implementing the instrument from deliverable 5)
3. **Multi-platform reach** (dc_aibf_app Flutter cross-platform for caregiver mobile capture)
4. **Cross-deliverable consistency** — every portal embodies the same B2C-primary, B2B-supporting framing as the thesis

---

## Source Materials

LaTeX sources, markdown manuscripts, supplementary materials, drafts, version history, the 6 portals + mobile-app source code, and the candidate's research-network publications are maintained in a separate working directory and are not published to this repository. Only the six committee-facing deliverables above are tracked here.

---

**Repository:** [https://github.com/PraveenAsthana123/story](https://github.com/PraveenAsthana123/story)

*Last updated: {{ site.time | date: "%Y-%m-%d" }}*
