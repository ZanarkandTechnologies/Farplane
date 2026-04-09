# Spec Contract

Use when reviewing a spec, ticket contract, or user-story slice before implementation.

Threshold: `4.0`

## Family Score Guide

- `1`: the contract solves the wrong problem, is incoherent as one unit of
  work, or is unsafe to execute
- `2`: the intended work is partly visible, but important scope, sequencing, or
  proof still depends on reviewer inference
- `3`: workable and directionally right, but still ordinary or caveated enough
  that a builder would need to infer some boundaries
- `4`: strong, clear, and approval-ready with only minor ambiguity left
- `5`: unusually crisp, testable, and resilient to skeptical review

## Dimensions

- `story-coherence`
- `parallelization-fit`
- `slice-sizing`
- `acceptance-testability`
- `scope-clarity`

### `story-coherence`

Inspect: actor, need, outcome, and whether the slice solves one coherent
problem.

Ask:

- Does this ticket describe one believable unit of user value?
- Would two competent implementers infer the same target behavior?

### `parallelization-fit`

Inspect: whether any proposed split is real, dependency-aware, and worth the
coordination cost.

Ask:

- Is the parallelization real, or is it fake concurrency hiding a critical path?
- Would the proposed split create coordination churn or merge conflicts?

### `slice-sizing`

Inspect: whether the ticket is small enough for one implementation/review loop
without becoming trivial or fragmented.

Ask:

- Can one builder/reviewer loop finish this safely?
- Is the slice too large, or artificially broken into micro-steps?

### `acceptance-testability`

Inspect: whether success criteria are observable, concrete, and resistant to
misreading.

Ask:

- Can a reviewer tell exactly what passing behavior looks like?
- Are important edge states or proof requirements missing?

### `scope-clarity`

Inspect: boundaries, dependencies, non-goals, and drift prevention.

Ask:

- Is in-scope versus out-of-scope explicit?
- Are dependency assumptions and non-goals strong enough to prevent drift?

## Evidence and Finding Cues

- Weak evidence usually looks like a plausible title plus loose prose that
  leaves actor, outcome, or boundaries implied.
- Ordinary evidence usually defines the main path but still leaves edge cases,
  proof shape, or split logic somewhat fuzzy.
- Strong evidence makes the slice, boundaries, and acceptance checks easy to
  restate without reinterpreting the ticket.
- Exceptional evidence makes the contract hard to misread and easy to execute
  across different implementers.
- Findings should name the missing boundary, testable behavior, or split error
  rather than saying the spec is merely "unclear."

## Review Packet Attachment

Attach this rubric under the ticket `Review Packet` when used:

- `score`
- `threshold`
- `pass`
- `dimension_scores`
- `findings`
- `next_action`
