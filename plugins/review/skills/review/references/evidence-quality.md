# Evidence Quality

Use when reviewing collected proof: tests, logs, screenshots, traces, QA notes, repro steps, or any evidence packet.

Required TAS: `TAS-A`
Hard gate: required for any overall `pass`

## Family TAS Guide

- `TAS-C`: the artifacts do not credibly prove the claimed behavior
- `TAS-B`: some proof exists, but key claims still rely on inference, missing
  coverage, or contradictory artifacts
- `TAS-B`: the main claim is supported, but important proof is still thin, partial,
  or awkward to audit
- `TAS-A`: strong, traceable, and pass-worthy evidence with only minor gaps
- `TAS-A`: unusually persuasive, easy to audit, and hard to game

## Dimensions

- `sufficiency`
- `reproducibility`
- `traceability`
- `consistency`
- `inspectability`
- `autonomy-readiness`

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

### `autonomy-readiness`

Inspect: whether evidence for autonomous or `$ralph` work proves that blockers
and human gates were identified before execution.

Ask:

- Does the evidence show the required commands, tools, credentials/permission
  assumptions, QA surfaces, and stop reason?
- If heavy QA was deferred to batch/release QA, is that deferral explicit and
  proportional to the ticket risk?

## Evidence and Finding Cues

- Weak evidence usually looks like a correct-sounding summary with partial logs
  or screenshots that do not cover the claims being made.
- Ordinary evidence usually proves the main path but leaves edge states or
  ticket-to-artifact mapping somewhat loose.
- Strong evidence is traceable, replayable, and easy to audit.
- Strong `$ralph` evidence includes selector output, skipped-ticket reasons,
  stop conditions, and the QA ring chosen for the ticket.
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

- `TAS-B` example:
  one screenshot proves the happy path, but the ticket also claims empty-state,
  error-path, and regression behavior that are not backed by any artifact.
- `TAS-B` example:
  the main command output and one or two screenshots are present, but mapping
  from ticket claims to artifacts is still loose and a reviewer has to infer too much.
- `TAS-A` example:
  each important claim points to a concrete test, log, screenshot, or repro
  step, and a skeptical reviewer can verify the packet quickly with only minor gaps.
- `TAS-A` example:
  the packet is traceable, replayable, well-organized, and persuasive enough
  that very little reviewer interpretation is required.

## Review Artifact Attachment

Attach this rubric in the linked review artifact when used:

- `tas`
- `required_tas`
- `pass`
- `dimension_tas`
- `findings`
- `next_action`
