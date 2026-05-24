# Implementation Plan

Use when reviewing an implementation plan, technical approach, or execution sequence before code is written.

Threshold: `4.0`

## Family Score Guide

- `1`: a reviewer cannot trust the plan to produce the intended change safely
- `2`: the direction is partly visible, but sequencing, proof, or boundaries
  are still too thin to hand off with confidence
- `3`: understandable and workable, but still ordinary, inference-heavy, or
  carrying avoidable plan risk
- `4`: strong, pragmatic, and approval-ready with only minor caveats
- `5`: unusually clear, economical, and resistant to skeptical review

## Dimensions

- `human-readability`
- `bloatability`
- `modularity`
- `proof-clarity`
- `execution-order`
- `risk-clarity`
- `decision-tone`
- `autonomy-readiness`

### `human-readability`

Inspect: whether a human reviewer can scan the delta, flow, and proof path
quickly.

Ask:

- Can a reviewer understand the change without rereading the whole ticket?
- Is the plan doing clarity work, or making the reader decode dense prose?

### `bloatability`

Inspect: whether the plan is the minimum durable change or is padded with
speculative abstractions and ceremony.

Ask:

- Does the plan add abstraction because it is needed, or because it sounds architectural?
- Is there hidden multi-loop scope pretending to be one ticket, or is a
  coherent ticket being needlessly shrunk into a fake "part 1"?

### `modularity`

Inspect: touched areas, ownership boundaries, and whether responsibilities stay
localized.

Ask:

- Are touched areas justified and coherent?
- Would this plan tangle responsibilities or preserve clean ownership?

### `proof-clarity`

Inspect: whether the proof path is observable, concrete, and hard to game.

Ask:

- Would a reviewer know exactly what to check when the work is done?
- Are the proof points concrete enough to distinguish success from storytelling?

### `execution-order`

Inspect: sequencing, dependency awareness, and safety of the proposed order.

Ask:

- Does the order reduce risk and coordination churn?
- Is the plan trying to validate too late or in the wrong place?

### `risk-clarity`

Inspect: named weak assumptions, failure modes, containment, and rollback.

Ask:

- What could go wrong first, and is it named?
- If the approach fails, is rollback or containment obvious?

### `decision-tone`

Inspect: whether the plan speaks in decisive, execution-ready language rather
than timid possibilities.

Ask:

- Does the plan name the recommended path directly?
- Would a builder know what to do next without translating hedge words into a
  real instruction?

### `autonomy-readiness`

Inspect: whether a plan intended for `$ralph`, unattended execution, external
services, hard-to-QA UI, or long-running work names the inputs and gates that
would otherwise interrupt the run.

Ask:

- Are required user inputs, assets, credentials, compute, tools, QA risks, and
  human gates explicit?
- Does the plan say what the agent may decide autonomously and what must stop
  for approval?

## Evidence and Finding Cues

- Weak evidence usually looks like plausible implementation prose with no
  credible proof path or risk section.
- Ordinary evidence usually has a believable main path, but proof and rollback
  stay thin.
- Strong evidence makes the delta, order, and proof points easy to check.
- Strong evidence for autonomous work also names readiness blockers before the
  build starts instead of letting them surface mid-run.
- Strong evidence also makes the next action and chosen path sound decisive.
- Exceptional evidence teaches the approach clearly while still staying lean.
- Findings should name the missing proof point, sequencing hazard, or unearned
  abstraction instead of saying the plan needs "more detail."

## Example Judgments

- `2.0` example:
  the plan names touched files and a rough intention, but proof is "run tests"
  with no concrete checks, rollback is missing, and sequencing still assumes the
  implementer will figure out the risky parts.
- `3.0` example:
  the plan has a believable delta and execution order, but edge-case proof,
  ownership boundaries, or risk mitigation still require some inference.
- `4.0` example:
  the plan makes `Before -> After`, touched areas, proof points, and rollback
  easy to scan, and a reviewer can approve it without major caveats.
- `5.0` example:
  the plan is as clear as a strong internal design note while still staying
  lean; it explains the tradeoff, the order, and the proof path so well that
  very little interpretive judgment is left for the implementer.

## Review Artifact Attachment

Attach this rubric in the linked review artifact when used:

- `score`
- `threshold`
- `pass`
- `dimension_scores`
- `findings`
- `next_action`
