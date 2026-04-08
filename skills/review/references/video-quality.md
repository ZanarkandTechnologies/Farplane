# Video Quality

Use when reviewing recorded verification videos, loom-style walkthroughs, or storyboard/video deliverables.

Threshold: `3.5`

## Dimensions

- `legibility`
- `coverage`
- `pacing`
- `faithfulness`
- `verification-value`

## Anchors

### `legibility`

- `1`: key states or interactions are difficult to see
- `3`: mostly readable, with some rough framing or zoom decisions
- `5`: easy to read, pause, and inspect

### `coverage`

- `1`: the video skips the states that matter most
- `3`: main states are shown, but some verification-relevant coverage is absent
- `5`: it captures the important interactions and outcomes end to end

### `pacing`

- `1`: too rushed or too slow to support verification
- `3`: acceptable, but not yet optimized for reviewer comprehension
- `5`: paced for efficient understanding and inspection

### `faithfulness`

- `1`: editing or framing makes the state of the product ambiguous
- `3`: mostly faithful, with some ambiguity left
- `5`: clearly faithful to the product state and run sequence

### `verification-value`

- `1`: more marketing than proof
- `3`: somewhat useful for proof, but still secondary to other evidence
- `5`: directly useful as verification evidence

## Review Packet Attachment

Attach this rubric under the ticket `Review Packet` when used:

- `score`
- `threshold`
- `pass`
- `dimension_scores`
- `findings`
- `next_action`
