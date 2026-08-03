# Delegate Frontend Skill Rules

- Keep this skill thin; the generic machinery belongs in `delegate-cli`.
- Use existing frontend skills to settle UX, visual taste, and landing-page
  shape before running an external builder.
- External builders return runnable output and deterministic QA artifacts.
  Route operated browser proof through the coordinating Codex `qa-tester`, then
  use `visual-qa`, `review`, and `web-design-guidelines` when source review
  applies.
