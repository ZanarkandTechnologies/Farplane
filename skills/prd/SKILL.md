---
name: prd
description: "Use for \"write the PRD\", \"how should this screen work\", \"this UI sucks\" or \"make the demo feel real\": a PRD, an operated-comparable workflow handoff, or a realism pack for impl-plan."
source: local
department: delivery
template_uses:
  skill-template: "0.6.5"
  skill-eval-task: "0.2.0"
allowed-tools: Read, Glob, Grep, Bash, Write, Edit
---

# PRD

## Context

Use this first when product intent, a screen's workflow, or a demo's realism is
unsettled: it writes the product spec (`docs/prd.md`), settles how a flow
should work from operated comparables, or makes a fake-feeling demo believable.
One pass runs one mode and stops at an accepted product artifact. It does not
own visual taste (`visual-design`), tickets or build sequencing (`impl-plan`),
or review of finished UI (`code-health` review mode).

## Skill Signature

```text
prd(intent, mode?: spec | workflow | realism) -> product_artifact + impl-plan handoff
reads: docs/prd.md, active ticket, docs/features/, docs/bootstrap-brief.md, current UI or demo data, supplied receipts
does: grounds the product decision, operates comparables or sources real artifacts, recommends one path
writes: docs/prd.md (spec), else the caller's ticket or response; no tickets
returns: PRD | workflow handoff | realism pack, with assumptions and the next owner
```

<!-- BEGIN FARPLANE_IMPORTANT_CHECKLIST -->
## Todo List

- [ ] **N1 — Read the current product surfaces and pick the mode.**
  `request -> mode + known audience, jobs, constraints | prospect | research`

  Rule: Read `docs/prd.md`, the active ticket, and `docs/features/` before
  asking anything; read `docs/MEMORY.md` only for a named question. Mode:
  new or changed product intent is `spec`; "how should this work", a broken
  screen, or an open IA/state question is `workflow`; a demo or MVP that feels
  fake is `realism`. Route ungrounded audiences, jobs, or friction to
  [prospect](../prospect/SKILL.md) and peer or market expectations to
  [research](../research/SKILL.md).

  Assert:
  - One mode and the source of each known fact are named before questions.
- [ ] **N2 — spec: write the PRD section by section.**
  `intent + surfaces -> docs/prd.md draft | prototype gate`

  Rule: Ask 6-10 questions tied to implementation decisions, then reduce the
  request with the global `reason(problem)` contract in
  [runtimes/AGENTS.md](../../runtimes/AGENTS.md)
  (objective, need, constraints, root cause, first viable slice, falsifier,
  non-goals). Fill audience, JTBD, user stories, constraints, non-goals, risks,
  first SLC slice, metric candidates, and `Autonomy Readiness` (inputs,
  credentials, compute, tools, QA surfaces, human gates). When
  `docs/bootstrap-brief.md` names a profile, load
  [project-profiles](../setup-advisor/references/project-profiles.md) for the
  component matrix, advice axes, selected directions, and prototype gates.

  Example: "metric for a better onboarding tone" -> `none mechanical`, not a
  sentiment score posing as proof.

  Assert:
  - Metric candidates are mechanical or say `none mechanical`.
  - The highest-risk assumption has a named prototype or PoC gate.
- [ ] **N3 — workflow: operate 2-4 comparables, or reuse a fresh receipt.**
  `open workflow -> Comparable Evidence Receipt | skipped reason | blocked receipt`

  Rule: For a material, unsettled, current, or SOTA workflow, operate 2-4
  direct products or established comparables in a browser (in-app Browser
  first, one tab per source). Record source URL, user job, operated sequence
  and states, evidence ref, access limit, and `adopt | adapt | reject`. Docs
  and web search are not operated evidence. If operation itself fails, record
  `browser_operation: blocked` with the exact error and mark the recommendation
  provisional. A supplied current receipt for the same job is validated and
  reused, not rerun. Tiny same-pattern fixes emit
  `comparable_research_skipped: <reason>`. Load
  [comparable-patterns](references/comparable-patterns.md).

  Example: Mobbin redirects to login -> record the wall, keep Page Flows rows.

  Assert:
  - Every comparable has a receipt row or an explicit access blocker.
  - No taste gallery counts as functional proof.
- [ ] **N4 — workflow: diagnose, subtract, and recommend one model.**
  `receipt + current UI -> diagnosis + one model + states + handoff`

  Rule: Diagnose a broken surface with
  [redesign-diagnosis](references/redesign-diagnosis.md) before proposing
  changes. Run the Steve Jobs Focus & Simplicity Pass: customer benefit, core
  action, what is removed or deferred, and the deliberate `no`, without
  dropping required states, accessibility, safety, or evidence. Compare three
  models, recommend one, and define screens, IA, interaction rules, data
  ranges, and empty, loading, partial, success, error, and recovery states.
  Draw a low-fi ASCII wireflow only when a state table cannot show the journey.

  Assert:
  - Exactly one recommended model; options sit in an appendix.
  - Visual taste is named as a gap for `visual-design`, not decided here.
- [ ] **N5 — realism: source real artifacts, then build the realism pack.**
  `fake-feeling demo -> operating hypothesis + slice + ladders + labelled data pack`

  Rule: Climb the source ladder: real-public > user-provided or
  local-supplied > synthetic only as a last resort, and
  label every artifact `real-public | user-provided | local-supplied |
  synthetic-fallback`. Infer the operator's day-to-day loop
  aggressively but never as verified client truth. When the demo makes a
  recommendation, a deterministic solver, rule, retrieval, or state transition
  owns the result; the LLM narrates it, never imitates the computation. Load
  [realism-pack](references/realism-pack.md) and score with
  [realism-rubric](references/realism-rubric.md).

  Example: a demo needs a building permit -> find a public permit PDF with a
  stable URL before generating a look-alike.

  Assert:
  - No real-data realism claim rests on synthetic artifacts.
  - The rubric pass rule holds before handoff.
- [ ] **N6 — Review, hand off to impl-plan, and stop.**
  `artifact -> reviewed artifact + impl-plan handoff | revise`

  Rule: Tighten a PRD until [review](references/review.md) passes; package
  workflow decisions with [implementation-handoff](references/implementation-handoff.md).
  A demo-bearing build or review handoff requires an expectation-check
  artifact: realistic data exercised, workflow exercised, observed result,
  mismatch notes, evidence, and the operator question. Keep the
  [project-lifecycle](../setup-advisor/references/project-lifecycle.md)
  boundary: hand off to [impl-plan](../impl-plan/SKILL.md) only after the
  artifact is accepted.

  Assert:
  - No ticket, branch, or code is created here.
<!-- END FARPLANE_IMPORTANT_CHECKLIST -->

## Gotchas

- Pinterest is not functional workflow proof: Pinterest, Savee, and aesthetic
  galleries route taste evidence to `visual-design` or `intelligest`; counting
  them as comparables ships a pretty flow nobody has proven.
- Relabelling docs or search snippets as an operated flow hides that no
  sequence was exercised; write `browser_operation: blocked` and keep the
  recommendation provisional instead.
- Solving a functional failure with styling: "make it cleaner" leaves the
  primary action buried; the handoff must name behaviour and states.
- A builder reporting "demo works" without an expectation check leaves Kenji
  to discover the mismatch in review.
- A look-alike permit or invoice, when a public one exists, reads as fake.

## Reference Map

- [prd-template](references/prd-template.md) - `docs/prd.md` structure and
  clarifying-question pattern.
- [requirements-discovery](references/requirements-discovery.md) - audience
  and JTBD interview prompts, acceptance-criteria rules.
- [review](references/review.md) - PRD must-pass and fail-if checks.
- [comparable-patterns](references/comparable-patterns.md) - source roles,
  what to extract, receipt and blocker shapes.
- [redesign-diagnosis](references/redesign-diagnosis.md) - why a current UI
  fails, ending in one redesign sentence.
- [implementation-handoff](references/implementation-handoff.md) - workflow
  handoff fields and emphasis by situation.
- [realism-pack](references/realism-pack.md) - operating ladder, source
  ladder, output shape, expectation-check artifact.
- [realism-rubric](references/realism-rubric.md) - seven dimensions and pass
  rules.

## Output

- `spec`: `docs/prd.md` with metric candidates, `Autonomy Readiness`, selected
  directions, and prototype gates; downstream tickets carry only honest
  mechanical metrics into their `Proof Contract`.
- `workflow`: users + stories, current diagnosis, Comparable Evidence Receipt
  (or skipped/blocked receipt), Focus & Simplicity Pass, recommendation,
  screens/states, interaction rules, optional wireflow, handoff, options
  appendix.
- `realism`: the realism pack with source provenance, rubric score, assumption
  ledger, and, when demo-bearing, the expectation-check requirement.
- Every mode ends with `next_owner: impl-plan | visual-design | none`.
