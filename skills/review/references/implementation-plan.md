# Implementation Plan

Use when reviewing an implementation plan, technical approach, or execution sequence before code is written.

Threshold: `4.0`

## Dimensions

- `human-readability`
- `bloatability`
- `modularity`
- `proof-clarity`
- `execution-order`
- `risk-clarity`

## Anchors

### `human-readability`

- `1`: a human reader cannot quickly tell what will happen
- `3`: the plan is understandable, but still somewhat dense or awkward to scan
- `5`: the plan is fast to read, logically ordered, and obvious to a human reviewer

### `bloatability`

- `1`: the plan is bloated with unnecessary abstraction, ceremony, or speculative scope
- `3`: mostly lean, but still carrying some avoidable structure
- `5`: sharply focused on the minimum durable change that solves the request

### `modularity`

- `1`: the plan encourages tangled responsibilities or unclear boundaries
- `3`: modularity is mostly preserved, but some boundaries remain fuzzy
- `5`: module boundaries and ownership are explicit and clean

### `proof-clarity`

- `1`: there is no believable proof path
- `3`: verification exists in outline, but proof expectations are still thin
- `5`: the proof path is concrete, economical, and hard to game

### `execution-order`

- `1`: sequencing is unsafe, incoherent, or ignores dependencies
- `3`: the sequence is workable, but not obviously the clearest route
- `5`: the order is dependency-aware, pragmatic, and easy to execute

### `risk-clarity`

- `1`: major risks and weak assumptions are hidden
- `3`: main risks are mentioned, but mitigation is still thin
- `5`: weak assumptions, failure modes, and rollback points are explicit

## Review Packet Attachment

Attach this rubric under the ticket `Review Packet` when used:

- `score`
- `threshold`
- `pass`
- `dimension_scores`
- `findings`
- `next_action`
