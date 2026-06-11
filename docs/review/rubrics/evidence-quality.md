# Evidence Quality

Use when reviewing collected proof: tests, logs, screenshots, traces, QA notes, repro steps, or any evidence packet.

Required TAS: `TAS-A`
Hard gate: required for any overall `pass`

## Family TAS Guide

- `TAS-C`: the artifacts do not credibly prove the claimed behavior
- `TAS-B`: some proof exists, but one or more required evidence checks fail in a
  repairable way
- `TAS-A`: strong, traceable, and pass-worthy evidence with only minor gaps
- `TAS-A`: unusually persuasive, easy to audit, and hard to game

## Checklist Modules

### Required Checks

- [ ] `main-claim-proven`: The artifacts prove the main behavior or claim under
  review, not only adjacent work.
- [ ] `important-edge-claims-proven`: Important edge, failure, regression, or
  state claims made by the task are backed by artifacts.
- [ ] `replayable`: Commands, setup, inputs, outputs, and observations are
  tied together tightly enough that another reviewer could replay or audit the
  result without guessing.
- [ ] `claim-artifact-map`: Each important ticket claim or acceptance criterion
  points to a concrete artifact.
- [ ] `summary-matches-proof`: Written conclusions do not exceed or contradict
  logs, screenshots, tests, or QA notes.
- [ ] `auditable-organization`: The packet is organized enough for a skeptical
  reviewer to verify the result quickly.

### Blocker Checks

- [ ] `missing-core-proof`: Core behavior is claimed but no credible artifact
  proves it.
- [ ] `contradictory-artifacts`: Artifacts contradict the review summary or one
  another in a way that changes the verdict.
- [ ] `stale-evidence`: Evidence predates the current changed files, ticket
  state, or relevant rerun.
- [ ] `claim-inflation`: The summary claims broader behavior than the attached
  evidence can support.

### Autonomy Evidence Checks

- [ ] `autonomy-inputs-visible`: Evidence for autonomous or `$ralph` work shows
  commands, tools, credentials/permission assumptions, QA surfaces, and stop
  reason.
- [ ] `qa-deferral-explicit`: Any deferred heavy QA is explicit and
  proportional to ticket risk.

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
- `checks`
- `failed_checks`
- `findings`
- `next_action`
