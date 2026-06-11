# Gotchas

- Do not assign TAS before reading the ticket.
- Do not let a clean standards audit replace rendered visual QA.
- Do not let a beautiful screenshot hide source-level accessibility or focus
  failures.
- Do not merge `ui-quality` and `frontend-guidelines`; keep both TAS verdicts visible
  for metric comparison.
- Do not let a visually acceptable UI pass frontend source review when the main
  component, provider, or dialog has become a hard-to-maintain god file.
- Do not approve weak evidence just because the implementation looks plausible.
