# Demo Quality

Use when reviewing a live demo script, narrated walkthrough, or interactive demonstration artifact.

Threshold: `3.5`

## Family Score Guide

- `1`: the demo misrepresents the product or is too staged to trust
- `2`: the demo shows something real, but still feels selective, under-proven,
  or confusing enough that confidence remains low
- `3`: believable and directionally useful, but still incomplete as reviewer
  evidence
- `4`: strong, trustworthy, and useful for review with only minor caveats
- `5`: unusually faithful, realistic, and verification-friendly

## Dimensions

- `fidelity`
- `realism`
- `workflow-coverage`
- `trustworthiness`
- `communication-clarity`

### `fidelity`

Inspect: whether the demo is honest about the actual product state.

Ask:

- Is the demo showing the real product behavior rather than a polished illusion?
- Are any key limitations being hidden?

### `realism`

Inspect: whether the demonstrated flow resembles how a real user or operator
would actually use the product.

Ask:

- Does this feel like a real workflow or a carefully staged best-case path?
- Are rough edges selectively avoided?

### `workflow-coverage`

Inspect: whether the important flow and outcomes are shown end to end.

Ask:

- Does the demo cover the workflow the ticket claims to improve?
- What important branch or outcome is still missing?

### `trustworthiness`

Inspect: whether the demo increases trust or leaves important doubts.

Ask:

- Would a skeptical reviewer believe this demonstration?
- Does the demo materially improve confidence, or just look polished?

### `communication-clarity`

Inspect: whether the viewer can follow what is being shown and why it matters.

Ask:

- Can the viewer tell what changed and why it matters?
- Is the walkthrough cluttered, rushed, or under-explained?

## Evidence and Finding Cues

- Weak evidence usually looks like a polished presentation that proves little.
- Ordinary evidence usually shows the main path but leaves some important review
  value on the table.
- Strong evidence feels faithful, realistic, and easy to map back to ticket claims.
- Exceptional evidence is both convincing as a demo and useful as verification.
- Findings should name the staged moment, missing workflow, or misleading
  omission rather than saying the demo needs "more polish."

## Review Artifact Attachment

Attach this rubric in the linked review artifact when used:

- `score`
- `threshold`
- `pass`
- `dimension_scores`
- `findings`
- `next_action`
