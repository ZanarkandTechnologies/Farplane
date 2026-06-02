# Feature Scoring

Use this rubric to turn source features into decisions.

## Feature Candidate

```text
Feature:
Source:
Evidence:
User job:
Metric moved:
Transferable principle:
Local fit:
Risks:
Decision: adopt | adapt | reject | defer
Reason:
```

## Score Dimensions

Score each dimension 1-5:

- `user-value`: does it materially help the target user?
- `evidence-strength`: is the source credible and concrete?
- `transferability`: can this move into our repo without importing unrelated
  assumptions?
- `implementation-cost`: lower cost scores higher.
- `risk`: lower safety, maintenance, or complexity risk scores higher.
- `synergy`: does it combine cleanly with other adopted features?

## Decision Guide

- `adopt`: high value, strong evidence, good fit, low-to-medium cost.
- `adapt`: strong principle, but exact source shape does not fit local
  conventions.
- `reject`: weak fit, weak evidence, high risk, or poor metric alignment.
- `defer`: valuable but too large for the current slice.

For external skill implementations, never score "auto-sync upstream" as
`adopt`. The highest-confidence decision is still a local contract change that
preserves Farplane conventions.

## Required Output

Use a compact table:

| Feature | Source | Evidence | Scores | Decision | Reason |
| --- | --- | --- | --- | --- | --- |

Do not leave decisions as "maybe". Use `defer` when timing is the only reason
not to do it now.
