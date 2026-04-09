# Debloatability

Use when reviewing cleanup, simplification, runtime reduction, or dead-surface removal work.

Threshold: `4.0`

## Family Score Guide

- `1`: the cleanup is unsafe, cosmetic, or leaves the main dead weight intact
- `2`: some simplification happened, but meaningful drag, duplication, or risk
  still remains
- `3`: worthwhile cleanup, but still ordinary enough that important clutter or
  uncertainty remains
- `4`: strong simplification and pass-worthy cleanup with only minor caveats
- `5`: unusually effective, safe, and clarity-improving reduction of dead weight

## Dimensions

- `dead-surface-removal`
- `compatibility-cleanup`
- `duplication-reduction`
- `clarity-improvement`
- `deletion-safety`

### `dead-surface-removal`

Inspect: whether obvious dead code or stale surfaces were actually removed.

Ask:

- What dead surface was left behind?
- Did the cleanup target meaningful drag or only easy cosmetic wins?

### `compatibility-cleanup`

Inspect: obsolete fallback layers, stale adapters, and old paths that no longer
earn their keep.

Ask:

- Which compatibility layer is still justified?
- Which one remains only because nobody deleted it yet?

### `duplication-reduction`

Inspect: repeated logic, docs, contracts, or wrappers that should collapse into
one source of truth.

Ask:

- What duplication was removed?
- Where is the system still paying for multiple copies of the same idea?

### `clarity-improvement`

Inspect: whether the system is easier to understand after the cleanup.

Ask:

- Is the new shape materially easier to reason about?
- Did deletion improve legibility, or only line count?

### `deletion-safety`

Inspect: verification for removed surfaces and hidden-caller risk.

Ask:

- What proves the deletion is safe?
- Could there be hidden callers or assumptions still depending on the removed surface?

## Evidence and Finding Cues

- Weak evidence usually looks like line deletion without proof that the deleted
  surface was actually stale.
- Ordinary evidence usually removes some clutter but leaves core duplication or
  compatibility drag behind.
- Strong evidence removes meaningful weight and proves the deletion is safe.
- Exceptional evidence materially improves legibility while shrinking surface
  area.
- Findings should name the dead surface that remains or the safety proof that is
  still missing.

## Review Packet Attachment

Attach this rubric under the ticket `Review Packet` when used:

- `score`
- `threshold`
- `pass`
- `dimension_scores`
- `findings`
- `next_action`
