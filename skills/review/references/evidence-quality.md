# Evidence Quality

Use when reviewing collected proof: tests, logs, screenshots, traces, QA notes, repro steps, or any evidence packet.

Threshold: `4.0`
Hard gate: required for any overall `pass`

## Dimensions

- `sufficiency`
- `reproducibility`
- `traceability`
- `consistency`
- `inspectability`

## Anchors

### `sufficiency`

- `1`: the artifacts do not prove the core claims
- `3`: the main claim is somewhat supported, but important proof is still missing
- `5`: the artifacts fully support the important claims without hand-waving

### `reproducibility`

- `1`: a reviewer cannot reconstruct what was run or observed
- `3`: replay is possible, but some setup or steps are missing
- `5`: commands, setup, and outputs are clear enough to replay quickly

### `traceability`

- `1`: acceptance criteria cannot be mapped to evidence
- `3`: some claims map cleanly, but others still require inference
- `5`: every important claim is directly traceable to a specific artifact

### `consistency`

- `1`: artifacts contradict each other or contradict the written claims
- `3`: mostly consistent, with a few loose or underspecified spots
- `5`: artifacts and conclusions line up cleanly

### `inspectability`

- `1`: evidence is hard to read, skim, or audit
- `3`: inspectable with effort, but not organized for skeptical review
- `5`: a skeptical reviewer can verify the claim quickly from the packet

## Review Packet Attachment

Attach this rubric under the ticket `Review Packet` when used:

- `score`
- `threshold`
- `pass`
- `dimension_scores`
- `findings`
- `next_action`
