# Evidence Quality

Use when reviewing collected proof: tests, logs, screenshots, traces, QA notes, repro steps, or any evidence packet.

Threshold: `4.0`
Hard gate: required for any overall `pass`

## Family Score Guide

- `1`: the artifacts do not credibly prove the claimed behavior
- `2`: some proof exists, but key claims still rely on inference, missing
  coverage, or contradictory artifacts
- `3`: the main claim is supported, but important proof is still thin, partial,
  or awkward to audit
- `4`: strong, traceable, and pass-worthy evidence with only minor gaps
- `5`: unusually persuasive, easy to audit, and hard to game

## Dimensions

- `sufficiency`
- `reproducibility`
- `traceability`
- `consistency`
- `inspectability`

### `sufficiency`

Inspect: whether the artifacts prove the main behavior plus the ticket's
important edge claims.

Ask:

- What important claim is still unproven?
- Are the artifacts covering only the happy path while stronger claims are being made?

### `reproducibility`

Inspect: commands, setup, inputs, outputs, and whether another reviewer could
recreate the evidence.

Ask:

- Could I replay what happened without guessing missing setup?
- Are the commands and observations tied together tightly enough to trust?

### `traceability`

Inspect: mapping from ticket claims or acceptance criteria to specific artifacts.

Ask:

- Can each important claim point to a concrete artifact?
- Where does the review still rely on narrative glue instead of direct mapping?

### `consistency`

Inspect: whether screenshots, logs, tests, and written conclusions agree.

Ask:

- Do any artifacts contradict the summary?
- Is the written claim stronger than the proof actually attached?
- Does a nearby doc, ticket note, or test output reveal claim inflation or stale proof?

### `inspectability`

Inspect: organization, readability, and how quickly a skeptical reviewer can
audit the packet.

Ask:

- Can a skeptical reviewer verify the result quickly?
- Is the packet organized for audit, or dumped in a way that hides weak spots?

## Evidence and Finding Cues

- Weak evidence usually looks like a correct-sounding summary with partial logs
  or screenshots that do not cover the claims being made.
- Ordinary evidence usually proves the main path but leaves edge states or
  ticket-to-artifact mapping somewhat loose.
- Strong evidence is traceable, replayable, and easy to audit.
- Exceptional evidence gives a skeptical reviewer very little room to doubt what
  happened.
- Findings should point to the exact unproven claim, missing artifact, or
  contradiction and tell the builder what proof to collect next.

## Desloppify Cues

When using the anti-slop playbook, search for:

- claims in the ticket or summary that are not backed by the attached artifact set
- screenshots/logs/tests that prove only the happy path while the prose claims broader coverage
- contradictions between QA notes and the review summary
- stale artifacts that predate the actual changed files or current ticket state

## Example Judgments

- `2.0` example:
  one screenshot proves the happy path, but the ticket also claims empty-state,
  error-path, and regression behavior that are not backed by any artifact.
- `3.0` example:
  the main command output and one or two screenshots are present, but mapping
  from ticket claims to artifacts is still loose and a reviewer has to infer too much.
- `4.0` example:
  each important claim points to a concrete test, log, screenshot, or repro
  step, and a skeptical reviewer can verify the packet quickly with only minor gaps.
- `5.0` example:
  the packet is traceable, replayable, well-organized, and persuasive enough
  that very little reviewer interpretation is required.

## Review Artifact Attachment

Attach this rubric in the linked review artifact when used:

- `score`
- `threshold`
- `pass`
- `dimension_scores`
- `findings`
- `next_action`
