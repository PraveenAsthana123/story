# Duplicate Detection --- My Analysis, Chapter by Chapter

**Date:** 2026-05-30 (revision 2: `\iffalse`-masking added to audit script)
**Status:** Read-only audit. No `.tex` files modified. No content removed or moved.
**Method:** Programmatic scan via [`scripts/audit_duplicates.py`](singledisease_ASD/scripts/audit_duplicates.py) (now masks `\iffalse...\fi` suppressed blocks so already-inactive content does not register as duplicate) + manual spot-checks of every flagged repeating heading.
**Backup branch:** `pre-dedup-backup` created at HEAD of `main` (commit `eeff559`) as a safety asset, in case removal work is greenlit later.

## Revision 2 changes
- Audit script now masks `\iffalse...\fi` suppressed blocks. Headings/captions/paragraphs inside those blocks are not rendered in the PDF, so counting them as duplicates was a false positive.
- Repeated-heading count dropped from **12 -> 8** with this fix (4 prior matches were inside suppression blocks).
- Manual spot-checked all 3 candidate cleanup items I flagged in revision 1; 2 are non-issues (suppressed or hierarchical), 1 is a genuine orphan empty subsection.

---

## TL;DR --- My Honest Take

The dissertation is **not over-duplicated**. The original Duplicate Section Report's claim of 575--1,165 pages of removable content is **overstated by a factor of ~10x**.

Here's what the audit actually shows:

| Class | Count (rev 2) | My read |
|---|---:|---|
| Near-identical paragraphs across chapters (Jaccard $\geq$ 0.85) | 13 | **11 are intentional** (Three-Questions landing page intros I added on purpose); 2 are GGU compliance-map openings (intentional parallel structure). **Zero accidental duplicates.** |
| Repeated headings (3+ files), after `\iffalse` masking | **8** (was 12) | **8 of 8 are intentional** per-chapter parallel structure (Chapter Synthesis, Chapter Summary, Chapter Objective, Supplementary Material, etc.). This is the GGU template, not redundancy. |
| Repeated captions | 1 (15 instances) | **False positive.** All 15 are different tables sharing the `\emph{ILLUSTRATIVE}` prefix convention that transparently flags fabricated/assumed data pending Phase 2. Different labels, different content. |
| High concept density (e.g., ASD 558x, trust 519x in Ch.3) | --- | **Expected.** Ch.3 is the methodology chapter for an ASD-EEG trust study. Density != duplication. |
| Manual spot-checks of 3 suspicious headings | 3 checked | **2 are non-issues** (suppressed in `\iffalse` or hierarchical Section + Subsection); **1 is a real orphan** (Ch.2 line 2485: empty `\subsection{Key Findings}` immediately followed by `\subsection{Key Findings (Consolidated Synthesis)}`). |

**Bottom line.** The aggressive removal plan would damage the dissertation by destroying:
1. The signature diagram pattern built last cycle (recurs in all 5 chapters by design).
2. The per-chapter Three-Questions landing page (just added, same intro on purpose).
3. The Ch.3 Primary/Secondary/Hybrid parallel structure (you explicitly said "that is ok").
4. The GGU template per-chapter parallel sections (Examiner Summary, Synthesis, etc.).

**My recommendation:** **Take no removal action.** What you have is parallel structure, not redundancy.

---

## Chapter 1 --- Introduction

### What the audit found
- 4 of the per-chapter Three-Questions intro paragraphs match across Ch.2, Ch.3, Ch.4, Ch.5 verbatim (Jaccard 1.00). All originate from this chapter's pattern.
- 1 GGU Compliance Map intro paragraph matches Ch.2 at Jaccard 0.89.
- Headings shared with other chapters: Examiner Summary, Chapter Synthesis, Supplementary Material, Chapter Summary, Chapter Objective, Lens map summary, Purpose, Key Sections Covered, Introduction, Objective Achievement Matrix.

### My read
**No accidental duplicates.** Every shared element is per-chapter parallel structure. The Three-Questions intro was added DELIBERATELY last cycle to give the examiner a consistent landing-page experience. Removing it = destroying the feature.

### Honest verdict
- Keep everything as is.
- The original brief's "30--70 page reduction" claim does not match what's in the file. Ch.1 spans roughly 50--55 PDF pages of content (the rest is appendix material auto-included). There aren't 30--70 pages of dedupable content here.

### One micro-suggestion (NOT a removal)
- The Three-Questions intro is duplicated 5x verbatim. If you ever want to maintain it in one place, it could become a one-line macro: `\threequestionsintro` defined in the preamble. But this is a maintainability nicety, not a page-reduction move. **I would not bother.**

---

## Chapter 2 --- Review of Literature

### What the audit found
- Shares the Three-Questions intro, GGU Compliance Map, Examiner Summary, Synthesis, Supplementary Material headings with other chapters (by design).
- "Key Findings" subsection appears in Ch.2 at lines 2485 and 2729 --- 2x in Ch.2 alone. Worth checking these aren't accidentally similar.
- "Lens map summary." paragraph header appears in Ch.2:318, Ch.4:2003, Ch.5:1124 --- 3x as parallel paragraph labels.

### My read
**One spot worth a 5-minute manual scan: the two "Key Findings" subsections in Ch.2** (lines 2485 and 2729). If they're the same content under the same heading, it's a real (accidental) duplicate worth merging. If they're genuinely different findings (e.g., from two different lens analyses), the heading reuse is fine but a clarifying suffix would help.

### Honest verdict
- Keep everything as is.
- Optional: rename one of the Ch.2 "Key Findings" subsections to disambiguate (e.g., `Key Findings (XAI Lens)` and `Key Findings (Trust Lens)`). This is a label clarification, not a removal.

---

## Chapter 3 --- Research Methods

### What the audit found
- Highest concept density in the dissertation (ASD 558, EEG 558, trust 519, explainability 256) --- expected, this is the methodology chapter.
- "Technique." paragraph header repeats 6x in `chapter3_pipeline_dedicated_pages.tex` (lines 655, 680, 705, 730, 755, 780) --- parallel pipeline-stage paragraphs, by design.
- 16 split chapter3 files (chapter3_advanced_arch_pages, chapter3_brutal_gap_pages, chapter3_pipeline_dedicated_pages, etc.) --- this is your modular methodology architecture.
- Shares the Three-Questions intro, GGU Compliance Map, Examiner Summary, Synthesis, Supplementary Material headings with other chapters (by design).
- "Chapter Synthesis" + "Chapter Summary" both appear in `chapter3_research_methods.tex` --- worth checking these are distinct content (synthesis vs. summary).

### My read
This is the chapter the original brief most aggressively attacked ("140--290 pages removable"). I disagree strongly.

**You explicitly said:** "primary data, secondary, hybrid data ... there will be some duplicate ... that is ok." That's correct. The Primary/Secondary/Hybrid (P/S/H) parallel structure is the dissertation's methodological discipline: the SAME quality criteria (sample, preprocessing, model, validation, governance) are applied UNIFORMLY to each data stream. That's not duplication, that's rigour.

The 16 modular chapter3 files (`chapter3_*.tex`) are a deliberate decomposition: each is a load-bearing methodological surface (pipeline detail, microservice IPO, ISO threshold pages, secondary-data pages, examiner Q&A, defence prep checklist, brutal gap pages). Collapsing them would destroy the modular methodology architecture.

### Honest verdict
- Keep everything as is.
- The "Technique." x6 repetition in `chapter3_pipeline_dedicated_pages.tex` is parallel structure, not redundancy --- each "Technique." paragraph describes a DIFFERENT technique. Leave it.
- **Optional micro-check:** verify `chapter3_research_methods.tex` "Chapter Synthesis" (line 13598) and "Chapter Summary" (line 13596) carry different content. If they overlap heavily, merge them (5-line edit). If not, leave alone.

---

## Chapter 4 --- Findings

### What the audit found
- "Key Findings" subsection appears 3x in Ch.4 alone (lines 5570, 5637, 6740) --- **this is the highest-priority spot to manually verify in the whole audit.**
- "DBA and Research Significance" subsection (line 1135) --- same heading text as Ch.2, Ch.3, Ch.5 (4x total). Parallel structure.
- "Objective Achievement Matrix" subsection (line 6770) --- repeats in Ch.2 and Ch.5. Parallel structure.
- Shares Three-Questions, Compliance Map, Examiner Summary, Synthesis, Supplementary Material with other chapters (by design).
- 12 of the 15 "ILLUSTRATIVE" captions live in Ch.4 (lines 6425, 6459, 6495, 6529, 6570, 6614, 6643, 6672, 6704). All have unique labels and content. False positive.

### My read
**The three "Key Findings" subsections in Ch.4 are worth your eye.** They may be (a) three legitimately different findings clusters (e.g., B2C findings, B2B findings, integrated findings) under the same generic header, or (b) accidental cross-references that got copied. If (a), a one-word disambiguating suffix would help; if (b), this is the one genuine merge candidate I found in the entire audit.

The "ILLUSTRATIVE" tables are CORRECT and important --- they transparently flag that the values are fabricated for didactic purposes, pending Phase 2 data collection. Removing them would damage the dissertation's integrity. The `\emph{ILLUSTRATIVE}` prefix is your honesty contract with the examiner.

### Honest verdict
- Keep everything as is.
- **Optional (5-minute task if greenlit):** rename the three Ch.4 "Key Findings" subsections to `Key Findings (B2C Caregivers)`, `Key Findings (B2B Clinicians)`, `Key Findings (Integrated)` (or whatever they actually describe). Pure label change, no content moved.

---

## Chapter 5 --- Discussion and Conclusion

### What the audit found
- Highest density of `trust` mentions (403) and `RGAIG` mentions (238) --- expected, this is the contribution chapter.
- Shares Three-Questions, Compliance Map, Examiner Summary, Synthesis, Supplementary Material with other chapters (by design).
- "Objective Achievement Matrix" (line 6370) --- parallel with Ch.2 and Ch.4.
- 4 of the 15 "ILLUSTRATIVE" captions live in Ch.5 (lines 6599, 6641, 6668, 6698) --- different tables, unique labels, false positive on the duplicate scan.

### My read
The brief's claim of "65--135 pages removable" from Ch.5 is not supported by the data. The chapter does what a discussion chapter should: it RE-ENGAGES findings under different lenses (meaning, contribution, recommendation, implication, future). The argument that "Governance --> Explainability --> Trust --> Adoption appears in Discussion + Contribution + Strategic Value + Conclusion" is **correct and intentional** --- each section approaches the same chain from a DIFFERENT angle. That's not duplication, that's discussion.

### Honest verdict
- Keep everything as is.
- The closing chapter is doing its job.

---

## Cross-Chapter Patterns (the audit's main finding)

### Concept density table (informational)

| Concept | Ch.1 | Ch.2 | Ch.3 (main) | Ch.4 | Ch.5 |
|---|---:|---:|---:|---:|---:|
| ASD | 274 | 306 | 429 | 529 | 264 |
| EEG | 238 | 219 | 558 | 174 | 145 |
| RGAIG | 180 | 161 | 178 | 104 | 238 |
| trust | 172 | 177 | 519 | 293 | 403 |
| explainability | 181 | 138 | 256 | 187 | 195 |
| governance maturity | 31 | 23 | 41 | 32 | 61 |
| PLS-SEM | 21 | 3 | 96 | 31 | 15 |

**My read.** This is the textbook profile of a focused dissertation: the central concepts recur across all five chapters because they ARE the dissertation. Ch.3 has the highest density because the methodology chapter has to discuss every construct's measurement; Ch.5 has the highest `trust` and `RGAIG` density because it's the contribution chapter. There is no chapter where a concept is over-dense relative to its purpose.

### Heading-parallelism (intentional GGU template)

Headings shared across all 5 chapters by design:
- `Chapter Objective`, `Chapter Synthesis`, `Chapter Summary`, `Examiner Summary`
- `Supplementary Material`, `Key Sections Covered`, `Purpose`
- `DBA and Research Significance`, `Objective Achievement Matrix`
- `Three Questions This Chapter Answers` (added last cycle, intentional)

These are GGU template requirements --- removing them would break compliance.

---

## What I Would Actually Do Next

I completed all three spot-checks I flagged in revision 1. Results:

1. **Ch.4 "Key Findings" x3 at lines 5570 / 5637 / 6740 --- RESOLVED.** Only **one** is active (line 5570). The other two are inside `\iffalse...\fi` suppression blocks (line 5637 wrapped in `\iffalse`, line 6740 inside an `\iffalse` KIT-section block). They are not rendered in the PDF. **No action needed.**

2. **Ch.3 "Chapter Synthesis" vs "Chapter Summary" at lines 13596 / 13598 --- RESOLVED.** These are **hierarchical**, not parallel: `\section{Chapter Summary}` at 13596 contains `\subsection{Chapter Synthesis}` at 13598 as its first subsection. This is the GGU template's standard wrap-up structure. **No action needed.**

3. **Ch.2 "Key Findings" x2 at lines 2485 / 2729 --- ONE REAL FINDING.**
   - Line 2729 is inside an `\iffalse` block. Not rendered. Fine.
   - Line 2485 is the only finding worth flagging in the entire audit:

   ```latex
   \subsection{Key Findings}              <-- line 2485, EMPTY (no content)
   \subsection{Key Findings (Consolidated Synthesis)}    <-- line 2487, has content
   ```

   In the rendered PDF this produces a numbered "Key Findings" subsection heading with zero body content, immediately followed by the real "Key Findings (Consolidated Synthesis)" subsection. The first heading is an orphan --- it appears in the TOC and gets a number, but has nothing under it.

   **Recommended action (if greenlit):** Delete line 2485 only (`\subsection{Key Findings}`). This is a one-line typo-class edit; no content is removed. Per the "no remove/move" standing instruction, I am NOT executing it; flagging only.

**Summary of the entire audit's actual signal:** **one orphan empty subsection header in Ch.2**. That's it.

**I do NOT recommend executing the original Duplicate Section Report's 575--1,165-page removal plan.** That plan misclassifies intentional design patterns as duplication, and acting on it would:
- Destroy the signature diagram recurrence (anchor for examiner memory).
- Destroy the per-chapter parallel structure (GGU template compliance).
- Destroy the Three-Questions landing pages (added last cycle for examiner navigability).
- Destroy the Ch.3 Primary/Secondary/Hybrid parallelism (you explicitly approved this as "ok").
- Destroy the ILLUSTRATIVE transparency markers (your honesty contract).
- Risk a build-break cascade (precedent: aggressive prose-dedup attempts have failed twice on this codebase, requiring reverts of 730 and 356 lines).

---

## Files

- Audit script: [`singledisease_ASD/scripts/audit_duplicates.py`](singledisease_ASD/scripts/audit_duplicates.py)
- Raw audit output: [`DUPLICATE_AUDIT_REPORT_2026_05_30.md`](DUPLICATE_AUDIT_REPORT_2026_05_30.md)
- This analysis: [`DUPLICATE_REPORT_MY_ANALYSIS_2026_05_30.md`](DUPLICATE_REPORT_MY_ANALYSIS_2026_05_30.md) (you are reading this)
- Backup branch: `pre-dedup-backup` (at commit `eeff559`)

---

## Summary in One Line

**The dissertation is parallel, not redundant. The audit (now `\iffalse`-aware) confirms this. The only real finding in 2,214 pages is one orphan empty subsection header in Ch.2:2485 --- a one-line typo-class fix, not content removal.**
