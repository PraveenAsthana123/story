# Bottom Overflow Visual Audit

Generated: 2026-05-30T11:45:02.091121

Detects pages where content's max Y position exceeds page-bottom thresholds.
US Letter page = 792pt. Body text should end by ~720pt.
- WARNING: any text with Y > 740.0pt (encroaching footer)
- CRITICAL: any text with Y > 760.0pt (visibly past margin)

## Summary

- Total pages: 0
- WARNING (Y > 740.0): **0** pages
- CRITICAL (Y > 760.0): **0** pages

## Pages With Overflow (top 200, by severity)

