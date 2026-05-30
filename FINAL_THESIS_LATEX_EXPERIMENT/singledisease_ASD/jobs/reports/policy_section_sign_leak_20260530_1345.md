# Policy Section-Sign (§) Leak Audit — 2026-05-30T13:45:20.398473

Policy: `~/.claude/policies/no-policy-leak-section-sign.md`

## Summary

- **Leaks found** (unwanted §<num>): **1**
- Legitimate uses (ISO/IEC/RFC/EU/Article + §\ref): 136

## Per-File Leak Counts

| File | Leak Count |
|---|---:|
| `chapters/chapter5_discussion_recommendations.tex` | 1 |

## Top 100 Leaks (file:line — context)

| File:Line | Context |
|---|---|
| `chapters/chapter5_discussion_recommendations.tex:1015` | `(per Hallucination Detection §): outputs with confidence $< 0.7$ are` |
