# Integration Readiness

Use when deciding whether work is actually safe to advance, merge, or hand off.

Required TAS: `TAS-A`
Hard gate: required for any overall `pass`

## Family TAS Guide

- `TAS-C`: advancing this work would be obviously unsafe or incoherent
- `TAS-B`: the change might work, but trust is still too low because dependencies,
  contracts, or blast radius remain materially unresolved
- `TAS-B`: close to ready and directionally sound, but still carrying visible
  readiness caveats
- `TAS-A`: strong, safe enough to advance, and pass-worthy with only minor caveats
- `TAS-A`: unusually well-contained, low-risk, and easy to hand off or merge

## Dimensions

- `integration-safety`
- `contract-correctness`
- `dependency-readiness`
- `coupling-risk`
- `merge-readiness`

### `integration-safety`

Inspect: regression risk, rollout safety, and the consequences of advancing now.

Ask:

- What is the most likely breakage if this lands today?
- Is the risk understood and acceptably contained?

### `contract-correctness`

Inspect: interfaces, schemas, assumptions, and compatibility with neighboring
surfaces.

Ask:

- Are interfaces and assumptions actually correct, or only unchallenged?
- Is there a schema or contract edge that still depends on luck?
- Which neighboring file or doc defines the same contract, and does it still agree?

### `dependency-readiness`

Inspect: whether required upstream/downstream pieces are ready and explicit.

Ask:

- What other surface has to be true for this to work?
- Is that dependency real and ready, or just assumed?

### `coupling-risk`

Inspect: blast radius, hidden coupling, and whether this change is localized.

Ask:

- Did this change quietly increase coupling or coordination burden?
- Is the blast radius obvious and acceptable?

### `merge-readiness`

Inspect: whether a skeptical reviewer would actually allow the work to advance.

Ask:

- What would still make a reviewer say "one more pass first"?
- Is there any unresolved issue that should stop advancement today?

## Evidence and Finding Cues

- Weak evidence usually looks like "it seems fine" without explicit dependency
  or contract review.
- Ordinary evidence usually suggests the change is close, but still leaves some
  handoff or merge caveats visible.
- Strong evidence makes safety, dependencies, and readiness easy to defend.
- Exceptional evidence keeps blast radius low and handoff confidence high.
- Findings should name the unresolved dependency, unsafe assumption, or coupling
  risk that keeps the work out of a passing band.

## Desloppify Cues

When using the anti-slop playbook, search for:

- a related schema, type, or config file that still encodes the old rule
- a dependency assumption that exists only in prose, not in verified repo state
- a migration or compatibility path that was updated in one layer only
- a merge blocker hidden in neighboring docs, tests, or entrypoints

## Example Judgments

- `TAS-B` example:
  the feature appears to work locally, but it depends on an undocumented schema
  assumption, a manual coordination step, or a neighboring surface that has not
  actually been verified.
- `TAS-B` example:
  the change is probably safe, but one dependency, rollout caveat, or hidden
  coupling concern still makes "one more pass first" the safer call.
- `TAS-A` example:
  dependencies are explicit, contracts look correct, blast radius is understood,
  and a reviewer could defend advancing the change with only minor caveats.
- `TAS-A` example:
  the work is unusually well-contained, easy to merge or hand off, and leaves
  very little uncertainty about safety or neighboring impact.

## Review Artifact Attachment

Attach this rubric in the linked review artifact when used:

- `tas`
- `required_tas`
- `pass`
- `checks`
- `failed_checks`
- `findings`
- `next_action`
