# Demo Quality

Use when reviewing a live demo script, narrated walkthrough, or interactive demonstration artifact.

Threshold: `3.5`

## Dimensions

- `fidelity`
- `realism`
- `workflow-coverage`
- `trustworthiness`
- `communication-clarity`

## Anchors

### `fidelity`

- `1`: the demo misrepresents the actual product
- `3`: mostly faithful, but still somewhat selective or incomplete
- `5`: honest and faithful to the current product state

### `realism`

- `1`: the flow is staged or fake enough to undermine trust
- `3`: plausible, but still polished around important rough edges
- `5`: realistic enough that a skeptical reviewer would believe it

### `workflow-coverage`

- `1`: the important user flow is barely shown
- `3`: the main path is shown, but key edges or outcomes are skipped
- `5`: the important workflow is covered in a way that supports verification

### `trustworthiness`

- `1`: the demo invites doubt rather than confidence
- `3`: generally believable, but still light on proof value
- `5`: it materially increases confidence in the shipped behavior

### `communication-clarity`

- `1`: the viewer cannot tell what is being shown or why it matters
- `3`: understandable, but somewhat cluttered or under-explained
- `5`: easy to follow and clearly tied to the ticket claims

## Review Packet Attachment

Attach this rubric under the ticket `Review Packet` when used:

- `score`
- `threshold`
- `pass`
- `dimension_scores`
- `findings`
- `next_action`
