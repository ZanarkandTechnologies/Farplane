# Architecture

`review` is the TAS contract surface for tickets and completed work. It
selects rubric families, inspects the smallest useful changed and neighboring
surface, and writes a structured verdict.

Frontend review uses multiple lanes:

- `ui-quality` judges visible product quality, taste, and fit to intent.
- `frontend-guidelines` records source-fresh Web Interface Guidelines results
  from `web-design-guidelines`.
- `frontend-code-maintainability` judges React/component structure, file length,
  hooks, state ownership, comments, DRY, and testable seams.
- `visual-qa` judges rendered UI proof when screenshots or browser state are in
  scope.

Keep those lanes separate so agent reviews can be compared instead of averaged
into one vague UI TAS.
