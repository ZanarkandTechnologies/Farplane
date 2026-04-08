# Debloatability

Use when reviewing cleanup, simplification, runtime reduction, or dead-surface removal work.

Threshold: `4.0`

## Dimensions

- `dead-surface-removal`
- `compatibility-cleanup`
- `duplication-reduction`
- `clarity-improvement`
- `deletion-safety`

## Anchors

### `dead-surface-removal`

- `1`: dead code or stale surfaces remain untouched despite being obvious
- `3`: some cleanup happened, but meaningful dead surface still remains
- `5`: stale surfaces were removed aggressively and safely

### `compatibility-cleanup`

- `1`: obsolete compatibility layers still dominate the shape of the change
- `3`: the worst baggage is reduced, but some legacy drag remains
- `5`: compatibility layers now exist only where they still earn their keep

### `duplication-reduction`

- `1`: duplicate logic/docs/contracts remain scattered
- `3`: some duplication is reduced, but not fully normalized
- `5`: duplicate surfaces are consolidated into one clear source of truth

### `clarity-improvement`

- `1`: the cleanup did not make the system easier to understand
- `3`: some clarity improved, but the new shape is only modestly better
- `5`: the simplification materially improves legibility for the next engineer

### `deletion-safety`

- `1`: deletions are risky, under-verified, or likely to break hidden callers
- `3`: deletions seem safe, but evidence is still somewhat thin
- `5`: deletions are well-bounded and explicitly proven safe

## Review Packet Attachment

Attach this rubric under the ticket `Review Packet` when used:

- `score`
- `threshold`
- `pass`
- `dimension_scores`
- `findings`
- `next_action`
