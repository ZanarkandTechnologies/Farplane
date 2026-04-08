# Spec Contract

Use when reviewing a spec, ticket contract, or user-story slice before implementation.

Threshold: `4.0`

## Dimensions

- `story-coherence`
- `parallelization-fit`
- `slice-sizing`
- `acceptance-testability`
- `scope-clarity`

## Anchors

### `story-coherence`

- `1`: the user story does not make sense as one unit of work or solves the wrong problem
- `3`: the core story mostly makes sense, but some boundaries or intent still need inference
- `5`: the user story is coherent, aligned to the request, and easy to execute as written

### `parallelization-fit`

- `1`: the proposed parallelization is fake, conflicting, or hides critical-path dependencies
- `3`: some parallelization is plausible, but the split is not obviously the cleanest or safest
- `5`: the proposed parallelization is real, dependency-aware, and improves throughput without coordination churn

### `slice-sizing`

- `1`: the slice is too large, too fragmented, or impossible to finish safely in one loop
- `3`: the size is workable, but still carries some decomposition or overflow risk
- `5`: the slice is well-bounded for one implementation/review loop

### `acceptance-testability`

- `1`: success conditions are too vague to verify
- `3`: the main path is testable, but edge states or proof expectations remain loose
- `5`: acceptance criteria are concrete, observable, and hard to misread

### `scope-clarity`

- `1`: in-scope vs out-of-scope boundaries are missing enough to invite drift
- `3`: most boundaries exist, but some interpretation is still required
- `5`: non-goals, dependencies, and boundaries are explicit and enforceable

## Review Packet Attachment

Attach this rubric under the ticket `Review Packet` when used:

- `score`
- `threshold`
- `pass`
- `dimension_scores`
- `findings`
- `next_action`
