# Frontend Guidelines Metric

Use this when review covers UI source files, rendered frontend work, or a
ticket that claims accessibility, interaction, responsive, form, animation, or
web-interface quality.

This is a bridge between the source-fresh `web-design-guidelines` skill and the
anchored `review` score contract. It is not a replacement for `ui-quality` or
`visual-qa`.

## Source Of Truth

Run `web-design-guidelines` against the changed UI files and let that skill
fetch the latest upstream command before judging.

Do not copy the upstream rules into this file. The value of this lane is that it
checks current web-interface expectations every review.

## When Required

Required for review when any of these are true:

- changed files include UI components, pages, forms, dialogs, navigation,
  animation, canvas wrappers, or user-visible layout
- the ticket claims accessibility, best-practice, interaction, or polish
- `frontend-craft` drove implementation
- `ui-quality` is selected and source files are available

Optional when the review only covers planning artifacts, screenshots without
source, backend/API code, or docs-only work.

## Review Flow

1. Identify the changed UI file set from the ticket, diff, or implementation
   summary.
2. Run `web-design-guidelines <file-or-pattern>` on that set.
3. Save or paste the guideline findings into the review evidence when useful.
4. Convert the result into a `frontend-guidelines` score using the scale below.
5. Attach the score beside `ui-quality`, not inside it.
6. Use serious guideline failures as evidence for `ui-quality`,
   `evidence-quality`, or `integration-readiness` when they affect trust.

## Score Guide

- `1.0`: no guideline audit was run for UI code, or the findings show severe
  accessibility/interaction failures that make the UI unsafe to ship
- `2.0`: audit ran, but multiple important findings remain across core controls,
  forms, navigation, focus, or animation
- `3.0`: audit ran and the UI is directionally acceptable, but unresolved
  findings still need a follow-up pass before strong confidence
- `4.0`: audit ran and only minor or well-justified findings remain
- `5.0`: audit ran cleanly, or remaining notes are explicitly non-applicable
  with convincing evidence

Default threshold: `4.0`.

## Artifact Shape

Add this object to the structured review result when the lane runs:

```json
{
  "name": "frontend-guidelines",
  "score": 4.0,
  "threshold": 4.0,
  "pass": true,
  "source": "web-design-guidelines",
  "files_checked": ["src/app/page.tsx"],
  "findings_count": 0,
  "findings": [],
  "next_action": "No guideline rework required."
}
```

If the lane is skipped, include:

```json
{
  "name": "frontend-guidelines",
  "skipped": true,
  "reason": "docs-only change; no UI source files changed"
}
```

## Alignment Metric

When comparing agent reviews, record both:

- the agent's normal `ui-quality` score
- this `frontend-guidelines` score

Large disagreement is useful signal:

- high `ui-quality`, low `frontend-guidelines`: the agent is overvaluing taste
  while missing accessibility or interface fundamentals
- low `ui-quality`, high `frontend-guidelines`: the UI may be standards-clean
  but visually generic, off-brand, or weak against intent
- both low: another implementation pass is needed
- both high: strongest frontend review confidence

## Finding Cues

Treat guideline findings as review evidence, not mere lint. Escalate when they
affect keyboard access, labels, focus visibility, destructive actions,
hydration safety, reduced motion, large-list performance, or source/rendered
state consistency.
