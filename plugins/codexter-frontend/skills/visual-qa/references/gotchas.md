# Gotchas

- Do not judge a screen without the ticket's expected UI contract.
- Do not treat a successful route load as visual QA.
- Do not skip geometry assertions; most visible regressions are layout bugs.
- Do not ignore small-phone, landscape, reduced-motion, dynamic text, theme, or
  fixed-element overlap checks when they are relevant.
- Do not let screenshots pass when state coverage is missing.
- Do not invent the intended design when `docs/TASTE.md`, the ticket, or a
  design brief is missing.
