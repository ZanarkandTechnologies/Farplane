# Integration Readiness

Use when deciding whether work is actually safe to advance, merge, or hand off.

Threshold: `4.0`
Hard gate: required for any overall `pass`

## Dimensions

- `integration-safety`
- `contract-correctness`
- `dependency-readiness`
- `coupling-risk`
- `merge-readiness`

## Anchors

### `integration-safety`

- `1`: merging or advancing this work is obviously unsafe
- `3`: likely safe, but still carrying visible regression or rollout risk
- `5`: integration risk is well understood and acceptably low

### `contract-correctness`

- `1`: interfaces, schemas, or assumptions are broken or ambiguous
- `3`: contracts mostly hold, but some assumptions still need checking
- `5`: interfaces and assumptions look correct and stable

### `dependency-readiness`

- `1`: required dependencies or follow-on surfaces are not actually ready
- `3`: mostly ready, but still depending on some manual or implied coordination
- `5`: dependencies are resolved, explicit, and ready to advance

### `coupling-risk`

- `1`: hidden coupling or blast radius is high
- `3`: some coupling risk remains, but it appears manageable
- `5`: coupling is low or intentionally contained

### `merge-readiness`

- `1`: the work should not advance in its current state
- `3`: close to ready, but still needing one more focused pass
- `5`: ready to advance without reviewer caveats

## Review Packet Attachment

Attach this rubric under the ticket `Review Packet` when used:

- `score`
- `threshold`
- `pass`
- `dimension_scores`
- `findings`
- `next_action`
