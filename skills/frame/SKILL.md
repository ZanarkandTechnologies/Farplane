---
name: frame
description: "Use for \"I have an idea\", \"what should we build\", \"brainstorm\" or \"are we aligned\": separate symptom from problem, widen options, pick the smallest build, play it back for correction."
source: local
template_uses:
  skill-template: "0.6.5"
allowed-tools: Read, Glob, Grep
---

# Frame

## Context

Use this when the operator says "I have an idea", "I want to build X", "we
need a Y", "brainstorm this", "are we aligned?", or "play back what we're
building", and before a PRD, MVP brief, ticket, or plan exists. It stops the
first named artifact from becoming the product by default, and it shows the
operator what the agent thinks is being built so they can correct it.

Modes change emphasis, not the output: `diagnose` (default) runs N1, N3, N4
and N5; `widen` adds N2; `playback` leads with N4 from what the discussion
already settled. A paused task's history, tests, or next steps belong to
`recap-task`; choosing among options that are already real belongs to `advise`.

## Skill Signature

```text
frame(idea_or_request, context?, mode?: diagnose | widen | playback, ensemble?: auto | max)
  -> problem_frame + recommended_boundary + playback_view + correction_questions[1..3] + next_owner
reads: the conversation, supplied notes, tickets, docs, and local context
does: splits symptom from problem, widens options when unclear, picks the smallest boundary, plays it back
writes: none, or the caller-owned ticket, PRD, or brief when one already exists
returns: the frame, one proposed visual, 1-3 correction questions, and the next owner
```

<!-- BEGIN FARPLANE_IMPORTANT_CHECKLIST -->
## Todo List

- [ ] **N1 — Split the symptom from the real problem.**
  `idea_or_request -> requested_artifact + problem_candidates + actor/job/stakes + classed_constraints | already_framed`

  Rule: The requested artifact is evidence, not the build target. Label each
  fact `reported`, `observed`, `inferred`, or `unknown`. Ask why the current
  workflow exists and class every constraint `hard`, `soft`, `inherited`,
  `obsolete`, or `unknown`; strip the inherited and obsolete ones to state the
  irreducible job. Keep two frames when the cause is unclear.

  Example: `"we need a pricing calculator" -> quotes are slow and wrong because
  inputs, approvals, and cost rules are scattered -> calculator is one option`

  Example: `74-day onboarding, tweaks reach 72 -> reset to the irreducible job,
  not a 3% improvement`

  Assert:
  - The requested artifact and the problem statement are separate lines.
  - Unknowns stay unknown; no client fact is invented to complete the frame.
  - An input that already names actor, job, stakes, and boundary is validated
    briefly and routed forward, not re-derived.

- [ ] **N2 — Widen the option space only when it is unclear.**
  `frame + mode -> 2-4 candidate directions + strongest tradeoffs | skipped`

  Rule: Run when the mode is `widen`, the operator says brainstorm, or several
  first slices are plausible; skip when one direction is obvious. Contrast
  current reality with a first-principles rebuild, then add at most the lane
  that cuts the actual uncertainty: customer/data/action for an operational
  loop, issue tree for root causes or workstreams, working-backwards PRFAQ for
  a product bet ([widening lanes](references/widening-lanes.md)). Use
  `ensemble` only when asked: `auto` picks three personas from
  [ensemble.yaml](ensemble.yaml) by focus, `max` uses all; synthesis keeps
  dissent and the frame's output shape.

  Example: `"brainstorm it like two famous founders" -> first-principles operator +
  systems reinvention archetypes, never imitation of real people`

  Assert:
  - Directions differ in boundary or mechanism, not wording.
  - No lane runs as ceremony; ensemble mode does not pass into child calls.

- [ ] **N3 — Recommend the smallest boundary that solves the problem.**
  `frame + directions -> boundary ladder comparison + recommended rung | open decision + evidence needed`

  Rule: Place options on the ladder manual service -> tool (calculator,
  dashboard, assistant) -> product (workflow slice, system of record) ->
  platform, and say why the rungs beside the pick are too small or too large.
  A higher rung needs evidence that the lower one fails. When user reality or
  current practice could move the rung, keep the frame provisional and name
  the evidence and its owner.

  Example: `nonprofit "pitch a full ops platform" + no coordination evidence
  -> one shared incident view or a run-by-hand service; platform deferred`

  Assert:
  - At least two rungs are compared with too-small or too-large reasons.
  - The pick or the open decision names the exact evidence that would move it.

- [ ] **N4 — Play it back in the view that answers the verification question.**
  `frame + boundary + operator_question -> one proposed visual + visible uncertainty | task_recap_route`

  Rule: Choose the view from what the operator must verify, not from the
  product's parts: `journey`, `ui-screen-flow`, `lifecycle`,
  `system-boundary`, `before-after-example`, or `comparison-table`
  ([visual templates](references/visual-templates.md)). Architecture is the
  wrong view for what users see. Fill one template with the discussion's own
  nouns, label it proposed, and show contradictions as open nodes. A request
  for task status, tests, or next steps is not a playback; send it to the
  task recap shortcut.

  Example: `dashboard redesign + "what will the lead see?" -> ui-screen-flow,
  even though backend services were discussed; "what changed?" ->
  before-after-example`

  Assert:
  - One visual, marked proposed, with no ASCII duplicate or second view.
  - UI flows show visible content, actions, and the loading, empty, error, or
    success states that matter.

- [ ] **N5 — Ask the riskiest corrections and name the next owner.**
  `playback -> 1-3 correction questions + next_owner`

  Rule: Ask only questions whose answer would change the frame, the rung, or
  the view, riskiest mismatch first. Route accepted product scope to `prd`, UI
  or workflow uncertainty to `functional-ui`, agency or client MVPs to
  `solution-shaping`, an accepted build slice to `impl-plan`, unknown user
  reality to `customer-research`, and a current-practice gap to
  `competitor-research`. Create no tickets and write no code.

  Assert:
  - One to three questions, and one named next owner.
  - The requested artifact reads as evidence, not automatically as the answer.
<!-- END FARPLANE_IMPORTANT_CHECKLIST -->

## Templates

```text
Requested:            <artifact as asked, source status>
Symptom -> problem:   <pain, decision, delay, or cost behind the request>
Actor / job / stakes:
Constraints:          <each tagged hard | soft | inherited | obsolete | unknown>
Directions:           <only when widened>
Boundary:             manual service | tool | product | platform -> <pick + why>
Playback:             <one proposed visual>
Correction questions: <1-3>
Next owner:
```

## Gotchas

- Building the named artifact because it was named: a calculator request
  becomes a calculator that encodes stale pricing rules nobody owns.
- Turning every operational complaint into an ERP, dashboard, or AI agent.
- A polished diagram that quietly picks one side of a contradiction reads as
  agreement the operator never gave.

## Reference Map

- [widening lanes](references/widening-lanes.md) — load in N2 when a lane or
  ensemble mode is selected.
- [ensemble.yaml](ensemble.yaml) — load only for `ensemble: auto | max`.
- [visual templates](references/visual-templates.md) — load in N4 after the
  verification question is known.
- [static calculator example](examples/static-calculator/example.md) — golden
  trace for the symptom split and boundary restraint.

## Output

Return the frame in the template shape, one proposed visual, one to three
correction questions, and the next owner, in chat. Write it into a ticket, PRD,
or brief only when the caller already owns that file.
