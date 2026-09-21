---
title: Business Strategy Review Contract
status: active
owner: review-offer | review-leads | review-model
created_at: 2026-09-20
updated_at: 2026-09-20
---

# Business Strategy Review Contract

The `review-offer`, `review-leads`, and `review-model` skills return the same
decision shape so their domain judgments remain comparable without collapsing
the business into one score.

```text
Decision:
Binding constraint:
Why now:
Before -> After -> Illustrative example:

Criterion cards[]:
  criterion:
  applicability: required now | assessable | candidate later | not currently required
  grade: 0 unknown | 1 absent/fragile | 2 partial | 3 effective | not graded
  confidence: low | medium | high
  before:
  evidence:
  consequence:
  after:
  illustrative example:
  closest source trajectory:
    source before:
    source move:
    source after/result:
  trajectory decision: adapt | reject | investigate
  transfer reason:
  priority reason:

Next experiment:
  hypothesis:
  cohort and timebox:
  primary variable:
  success signal:
  guardrail:
  positive branch:
  negative branch:

Alternatives:
Evidence gaps:
```

Applicability controls whether grading is meaningful. `not currently required`
is not a weak grade. `0 unknown` means the criterion matters or is assessable,
but the evidence is missing. Never total grades by default; dependencies and a
binding constraint determine the recommendation.

The review returns advice and an evidence test. It does not mutate a tracked
strategy artifact, admit work to the board, contact customers, publish, change
prices, or spend money without the owning project workflow and authority gate.
