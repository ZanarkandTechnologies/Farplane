# Delegate Frontend Skill Rules

- Keep this skill thin; the generic machinery belongs in `delegate-cli`.
- Use existing frontend skills to settle UX, visual taste, and landing-page
  shape before running an external builder.
- Route runnable user-visible output through mounted `agent-browser` evidence,
  then `visual-qa`, `review`, and `web-design-guidelines` when source review
  applies.
