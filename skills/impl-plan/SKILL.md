---
name: impl-plan
version: 2.6.0
description: "Turn one ticket into a before/after implementation plan with code maps, ordered edits, verification, and audit notes."
tier: 3
group: coding
source: local
common_chains:
  after: ["impl"]
allowed-tools: Read, Glob, Grep
---

# Impl Plan

<!-- BEGIN FARPLANE_IMPORTANT_CHECKLIST -->
## Todo List

- [ ] Read the active ticket first, then read the relevant PRD, specs, memory, troubles, lessons, and nearby code.
- [ ] Treat this skill as `PlanTicket<CodingTicket>` inside the
  [project-lifecycle](../deep-init-project/references/project-lifecycle.md).
- [ ] Plan through the native planning phase, but keep `impl-plan`
  coding-ticket specific.
- [ ] Use the relevant [research](../research/SKILL.md) method when expected
  behavior depends on local baseline, official behavior, examples, or peer
  norms.
- [ ] Use [research:gap](../research/SKILL.md#researchgap) when missing or
  partial code work needs current-state gap and production expectation.
- [ ] Use [research:parity](../research/SKILL.md#researchparity) when external
  peer norms need to be established before local scope.
- [ ] Preserve the
  [first-principles-planning](../../docs/specs/first-principles-planning.md)
  basis for material work: objective, need, assumptions, root cause,
  constraints, first viable slice, proof/falsification, tradeoffs, and
  non-goals.
- [ ] Decide whether the whole selected ticket can stay whole or whether a
  real boundary forces a split first.
- [ ] If an `Agent Testability Brief` exists, carry its surfaces into the proof and execution plan.
- [ ] Write or refine the ticket `Done / Proof` block: done conditions,
  concrete checks, manual checks, review rubric/TAS gates, hard gates, required
  evidence, and optional autoresearch session path.
- [ ] Compare 3 viable options only when a real material choice exists, then recommend one clearly.
- [ ] Keep the output in the canonical ticket-body shape instead of inventing a `Human` / `Agent` split.
- [ ] Make the `Map` section carry visual before/after flow, changed callable seams, and typed data movement when that improves trust.
- [ ] Add separate `Signature delta`, `Type Sketch`, or `Typed flow example` detail only when the map cannot stay readable without it.
- [ ] Add a compact `Program` whenever the build has more than one
  non-trivial step.
- [ ] Use decisive action language in the recommendation and ordered steps.
- [ ] Make proof concrete and observable rather than generic.
- [ ] Keep metrics and rubrics distinct: metrics are mechanical signals; rubrics are review judgment frames.
- [ ] If the change is high-risk or contentious, run the `--consensus` version of this skill.
- [ ] Run the native planning phase challenge/review shape before claiming
  the plan is ready.
- [ ] Pitch the full-ticket plan to the user for approval and revise it before
  build starts.
- [ ] Keep planning separate from implementation and leave the ticket in `review` until approval exists.
<!-- END FARPLANE_IMPORTANT_CHECKLIST -->

Use this for per-ticket implementation planning after a bounded ticket already
exists.

`impl-plan` is a Tier 3 Farplane coding-pipeline skill. It specializes the
native planning phase for code tickets; it is not a universal Tier 2 planning
interface for every application domain.

`impl-plan` remains the one public planner:

- default mode: detailed, action-oriented ticket planning
- `--consensus`: Planner/Architect/Critic loop for higher-risk or more
  contentious work

Discovery still belongs to `brainstorm`, `deep-interview`, `prd`, and
`spec-to-ticket`. `impl-plan` is not the broad intake surface.

`$work` may call `impl-plan` after Work Admission decides that a selected work
unit is material enough to need file-map-first planning. Tiny direct work can
bypass `impl-plan`; vague epics should route back to PRD, system design, or
`spec-to-ticket` before this skill runs.

<!-- MEM-0007 decision: planning output should be approval-first and compact: pitch, before->after, delta, core flow, proof, ask. -->
<!-- MEM-0008 decision: root AGENTS should stay repo-only and terse; skill internals belong in skills, not repo contract text. -->
<!-- MEM-0030 decision: material plans may use one top-level Mermaid delta map when flow or ownership is not obvious from files and signatures alone. -->
<!-- MEM-0031 decision: impl-plan should stay compact and file-map-first: change, why, touched files, signature deltas, blast radius, and verification. -->
<!-- MEM-0050 decision: impl-plan must align with the canonical single-surface ticket template and make typed data flow explicit when it materially affects trust. -->
<!-- MEM-0062 decision: compact chat does not mean thin planning; impl-plan should be detailed and action-oriented enough that a builder can execute the ticket without inventing the missing order or tone. -->
<!-- Local decision: impl-plan output should organize around Delta, Program, Map, Done / Proof, State, Links, and sparse Notes; diagrams may carry inline signatures and typed flow, while bulky execution detail, review, and evidence move to sidecars or artifacts. -->

When this skill needs diagram taste or pattern depth, reuse
`skills/diagramming/SKILL.md` instead of inventing a second diagram style here.

When the architecture itself is still under-specified, or the plan would have
to invent entities, storage ownership, or runtime boundaries, stop and use
`deep-system-design` before finishing the plan. `impl-plan` owns a detailed
call-and-data shape sketch, not a full system-design interview.

## Intent

This skill should produce one detailed plan in the canonical ticket-body shape,
not parallel documents for different readers.

After spec work has already been decomposed into modular tickets, the selected
ticket is the planning boundary by default. Plan the whole ticket, not a safer
"first slice," unless a real blocker, proof boundary, safety issue, or
explicit follow-up ticket makes narrower scope real.

The highest-signal plan answers:

- what changes and why now
- what the before/after delta is
- where it lives: touched files, inspected files, changed seams, and key data
  movement
- for incomplete feature work: what production-grade capability looks like and
  what the repo is still missing
- blast radius: callers, systems, workflows, or edges that could break
- how to verify it: done conditions, tests, checks, strongest proof, review
  rubric gates, hard gates, and required artifacts in `Done / Proof`

If the plan leaves the builder inventing execution steps or the next concrete
move, it is too thin.

## Modes

- **Default:** detailed, action-oriented planning in the canonical
  ticket-body shape, centered on a compact before/after delta and one visual
  map when that makes the execution path easier to understand
- **`--consensus`:** run the former `ralplan` challenge loop with
  Planner/Architect/Critic before presenting the final plan
- **`--interactive`:** consensus mode only; present the draft and final plan
  for user approval
- **`--deliberate`:** consensus mode only; add pre-mortem and expanded test
  planning for higher-risk work

## Core Prompt Wording

0a. Study `@docs/prd.md` for outcomes + constraints.
0b. Study `@docs/specs/*` for spec truth, including any `Agent Testability Brief` when present.
0b1. Study `@docs/specs/first-principles-planning.md` when the ticket is
material, product-shaping, ambiguous, or missing/partial feature work.
0b2. For complex runtime/service specs, use
`@docs/specs/spec-authoring-contract.md` to distinguish PRD, system-spec, and
ticket responsibilities; do not push system-spec state machines or conformance
matrices into the ticket plan unless the ticket needs the specific proof row.
0c. Study the active ticket in `@tickets/*` first; if none exists, inspect
`@tickets/*`.
0d. Study `@docs/MEMORY.md` for durable constraints.
0e. Study `@docs/TROUBLES.md` for raw repeated planning/execution misses and
`@docs/LESSONS.md` for distilled prevention rules when present.
0f. Search the codebase before assuming anything is missing.
0g. When repo-local context cannot define expected feature scope, ground the
target with the best available installed research surfaces: comparable
codebases, official docs, standards, or repo-search/doc MCPs when available.

## Pre-context Intake

Before finalizing the plan or handing off to execution:

1. Reuse the active ticket, linked docs, and canonical specs as the planning
   context surface.
2. When an `Agent Testability Brief` exists, preserve its control accelerators,
   state probes, coordination views, and proof surfaces in the plan instead of
   inventing testability doctrine again.
2a. Preserve the ticket's first-principles basis: objective, need,
    assumptions, root cause, constraints, first viable slice,
    proof/falsification, tradeoffs, and non-goals. If the basis is missing for
    material work, tighten the ticket or route back to PRD/spec before
    execution.
3. Preserve or create a ticket-level `Done / Proof` block for material tickets:
   honest mechanical metrics when available, `none mechanical` when not,
   caller-declared review rubric families, required TAS gates, hard gates,
   reviewer handoff fields when durable review is needed, required proof, and
   optional autoresearch session path.
4. Preserve any `Run Hints` fields from the ticket, PRD, bootstrap brief,
   system design, taste brief, or agent-testability brief; for `$ralph` or
   long-running execution, name missing inputs, permissions, compute, tools, QA
   risks, proof weight, and human gates before handoff.
4a. Preserve only current `Run Hints` when a ticket needs `$work` admission
    context; do not carry old readiness sections into rewritten tickets.
5. Read enough nearby code to name real files, seams, signatures, and typed
   data shapes instead of inventing them.
6. In Farplane itself, do **not** create hidden sidecar context snapshots; the
   active repo contract is tickets, linked docs, and mode state.
7. If intent is still vague, use `deep-interview --quick`.
8. If system shape is still vague, use `deep-system-design`.
9. If the repo does not yet implement the target capability clearly enough to
   scope the work, run [research:gap](../research/SKILL.md#researchgap) before
   finalizing the ticket plan. When the open question is what peer products,
   standards, or repos include, run
   [research:parity](../research/SKILL.md#researchparity) first.

Do not hand off to execution while the plan still depends on avoidable
unknowns.

## Trigger Conditions

- user asks for a plan, proposal, implementation approach, or approval-ready
  change summary
- feature/refactor work needs a human yes/no before changing a ticket from
  `status: review` to `status: building`
- request is large enough that the code shape, file touch points, or proof
  should be made explicit before implementation
- execution surfaces redirect a vague implementation request into planning first
- `$work` admits a material ticket and selects `planning: impl_plan`

## Workflow (Default Mode)

1. **Scope:** treat the selected ticket as the execution ambition by default.
   Keep the approved coherent ticket intact unless it clearly hides multiple
   independent build loops or a real split boundary emerged.
2. **Split check:** split only when proof, reuse, blocking risk, external
   dependency, or runtime ownership genuinely improves; do not force a split
   just because the work will span multiple commits, feels safer, or could be
   shipped incrementally.
3. **Compare:** show 3 viable options with bounded pros/cons only when the user
   did not already provide a take on a real material choice.
4. **Recommend:** state the best option and the tradeoff being accepted.
5. **Gap check when needed:** for missing or partial feature work, define the
   current state, production expectation, missing gaps, grounding references,
   and recommended now/later boundary.
6. **Done / Proof:** for material tickets, write or refine the ticket's compact
   `Done / Proof` block with done conditions, checks, manual proof, review
   rubric/TAS gates, hard gates, and required evidence. Use `none mechanical`
   when a numeric metric would be dishonest; use `autoresearch-plan` only when
   repeated metric experiments are warranted.
7. **Build one detailed task program:** use the compact ticket sections and
   make `Delta`, `Program`, `Map`, and `Done / Proof` explicit enough that the
   builder does not have to invent the sequence. Use a sidecar `plan.md` only
   when the technical sequence is too long, volatile, or independently useful.
8. **Review + handoff:** run the plan through the quality gate, fix weak spots
   before handoff, then end with a decisive readiness call and next move.

## Workflow (`--consensus` Mode)

Consensus mode preserves the former `ralplan` behavior inside this one skill.

1. Planner drafts one detailed file-grounded plan.
2. Architect reviews for steelman antithesis, tradeoff tension, and synthesis.
3. Critic evaluates for option quality, signature clarity, type-flow clarity,
   risk clarity, and concrete verification.
4. If Critic does not approve, revise and repeat the Architect -> Critic loop.
5. Present the final consensus-backed plan.

Use consensus mode when:

- the change is high risk, ambiguous, or architecturally contentious
- the user explicitly wants stronger challenge before implementation
- the handoff to execution would otherwise rely on untested judgment calls

## Core Decision Branches

- **Low risk / obvious fit:** keep the whole plan lean, but still state the
  concrete action sequence plainly; text-only is okay if the change is truly
  localized.
- **Material / cross-module:** require a clear map when visual shape makes the
  flow, ownership, changed seams, or typed data path easier to understand.
- **Interface-heavy / data-shape-heavy:** put inline signatures and typed flow
  in the map first; add fallback detail only when the map cannot stay readable.
- **High ambiguity / risk:** add only the extra sections that reduce ambiguity.
- **High risk / architectural tension:** prefer `--consensus`.
- **Linked `Agent Testability Brief`:** carry it into proof/testability
  sections instead of re-deriving shortcuts, probes, or coordination surfaces
  ad hoc.
- **Multi-commit work:** acceptable when the ticket is still one coherent
  build-and-proof loop; split only when a real boundary appears.
- **Already modularized tickets:** assume ticketization already did the
  decomposition work; default to planning full-ticket completion instead of a
  smaller internal phase.
- **Docs-only / rule-text-only:** no specialized QA delegation.

## Plan Shape

Use the compact ticket-body shape:

- `Summary`
- `Scope`
- `Delta`
- `Program`
- `Map`
- `Done / Proof`
- `State`
- `Links`
- `Notes`
- optional `Gap Analysis`
- optional `Agent Contract`
- optional `Run Hints`
- optional `Citations`

`Delta` is the approval core of the ticket and should include:

1. `Before`
2. `After`
3. `Why now`
4. `First-principles basis`
   - objective, need, assumptions, root cause, constraints, first viable slice,
     proof/falsification, tradeoff, and non-goals when material

`Map` is the comprehension core of the ticket and should include:

1. one Mermaid delta diagram when the work is material, cross-module, or easier
   to understand visually
2. inline signatures in nodes or edges when callable seams matter, using
   `file / symbol(input): output` where readable
3. one numbered typed-flow path inside the diagram when structs, payloads, or
   state evolve across boundaries
4. a short `Touch` / `Inspect` list when the diagram cannot cleanly carry file
   grounding
5. separate `Signature delta`, `Type Sketch`, or `Typed flow example` blocks
   only when the map would become crowded or ambiguous

`Program` is the action core of the ticket. It should show variables, skill or
operation calls, and outputs in compact pseudocode:

```text
vars:
  target =

program:
  ground(vars) -> current_state
  change(current_state) -> artifact_delta
  verify(done_when, proof) -> evidence
```

`Done / Proof` is the proof core of the plan and should include concrete done
conditions, checks, manual checks, review focus, rubric/TAS gates, human gates,
and required evidence. The ticket stores required evidence handles; execution
outputs belong in artifacts or `progress.md`, not duplicated in the ticket.

Create a sidecar `plan.md` only when the technical build plan is too long for a
skimmable ticket, deeply implementation-specific, likely to change
independently, or useful as a handoff artifact separate from the task contract.

`Notes` should stay sparse: only real blast radius, risks, rollback,
citations, blockers, or follow-up boundaries.

## Applicability Rule

- **Map required by default for material work:** use a Mermaid delta diagram
  when visual shape makes the plan easier to understand, especially for
  feature, workflow/tooling, ambiguous, cross-module, ownership, or typed data
  changes.
- **Callable seams belong in `Map` first:** use inline signatures in diagram
  nodes or edges when trust depends on seeing real code seams. Add a separate
  `Signature delta` only when the visual map would become crowded.
- **Typed flow belongs in `Map` first:** use a numbered typed path in the
  diagram when structs, objects, payloads, or state evolve across boundaries.
  Add a separate `Type Sketch` or `Typed flow example` only when data shape is
  the main risk and needs more room.
- **Gap Analysis required:** missing or partially implemented feature work,
  parity work, or tickets whose scope depends on external expectations rather
  than an already-clear local implementation.
- **Options considered required only for real forks:** include options only
  when the planner chose among materially different viable paths.
- **Run Hints belong upstream:** preserve existing readiness fields from the
  spec or ticket, but in the impl plan reduce them to testability, human gates,
  blockers, compute hints, and proof weight unless the ticket is intended for
  `$ralph`, unattended execution, external services, hard-to-QA
  UI/motion/simulation, or deploy/spend/destructive boundaries.
- **Done / Proof compact by default:** for material, review-sensitive,
  agentically hard, or ticketed build work, name done conditions, metric or
  `none mechanical`, review rubrics/TAS gates, hard gates, and required proof.
  Keep detailed execution evidence in artifacts or `progress.md`, not in the
  ticket body.
- **Citations inline by default:** cite sources only when they affect the plan.
  Use a `Citations` line or section only when multiple references matter.
- **Evidence is ticket-owned:** do not include a planning `Evidence` section
  unless the user explicitly asks for audit detail; plan review can be a
  one-line readiness note.
- **Text-only allowed:** trivial, single-bug, or narrowly localized fixes where
  the file, symbol, or error already anchors the work concretely.

## Top Gotchas

1. Do not implement; this skill is plan-only.
2. Do not duplicate the same idea across summary, delta, map, criteria, and
   verification.
3. Do not skip first-principles basis for material work; objective, root cause,
   assumptions, first slice, proof, tradeoff, and non-goals should be visible.
4. Do not hide the key interfaces in prose when inline diagram signatures would
   prove understanding faster.
5. Do not split callable seams, type sketches, and typed examples into separate
   sections when one readable visual map can carry the same before/after delta.
6. Do not leave the builder inferring the execution sequence when the ticket is
   material enough to need an explicit order of operations.
7. Do not preallocate empty review output inside the input ticket.
8. Do not introduce separate done, verification, or proof sections when one
   `Done / Proof` block can carry the same contract.
9. Do not confuse metrics with rubrics: metrics are mechanical signals,
   rubrics are review judgment frames. Put both in `Done / Proof` when
   they matter.
10. Do not include option comparison when there was no real material fork.
11. Do not guess at "production-ready" scope from intuition alone when
   comparable products, codebases, or official docs can ground it.
12. Do not rewrite a coherent ticket into "part 1" or "first slice" just
    because that feels safer than planning the full ticket.
13. Do not use timid language like "maybe", "might", or "could" where the plan
    should be making a recommendation or naming an execution step.
14. Do not hand off a `$ralph`-eligible ticket with vague run-hint fields; name
    the blockers or keep the ticket gated.
15. Do not include `Evidence` as planning boilerplate; evidence belongs in
    artifacts, `progress.md`, or concise `State`/`Links` pointers unless audit
    detail is explicitly requested.

## Efficiency Rules

- Lead with the delta and map, not the appendix.
- If the user did not provide a take, default to consultative guidance instead
  of neutral mirroring.
- Prefer clear action language over hedging.
- Reuse the `diagramming` skill's compact delta-map patterns and put changed
  signatures or typed flow into the map when that improves skimmability.
- Reuse existing modules; justify every new file or abstraction in one line.
- If planning reveals overflow scope, split it into new `tickets/` follow-ups
  instead of stretching one ticket.
- Do not force the richer sections onto trivial localized fixes when the work
  is already concrete from code context.

## Plan Quality Gate

Before returning the plan, run these checks against the drafted output:

1. **Reference coverage**
   - Did the plan actually use the relevant PRD, spec, ticket, memory,
     troubles, lessons, and local code context?
   - If a source was skipped, is that omission safe and explicit?
2. **Scope discipline**
   - Is this still one coherent build-and-proof loop?
   - If not, is the split boundary real and explicit rather than just
     commit-count driven?
   - If the ticket was already modularized from the spec, does the plan still
     target the whole ticket instead of inventing a narrower first pass?
3. **Recommendation quality**
   - If a real material choice existed, did the plan compare real options
     instead of cosmetic variants?
   - Is the chosen path clearly recommended, not merely listed?
   - If no options are listed, is that because no real fork existed?
4. **Map usefulness**
   - For material work, does the map make the before/after flow, ownership, or
     changed seams easier to skim?
   - If no map is present, are the delta and build steps clearly enough?
5. **Signature usefulness**
   - Are the real callable seams visible in the map or in a compact fallback
     signature list?
   - Would the seams convince a reviewer that the planner understands the
     codebase?
6. **Type-flow usefulness**
   - If typed data matters, does the map show a believable representative
     payload or state path?
   - Did we avoid turning the plan into a schema dump?
7. **Proof quality**
   - Are the checks concrete and observable?
   - Would a reviewer know exactly how to tell success from failure?
   - Does the compact `Done / Proof` block name mechanical metrics or `none
     mechanical`, review rubric gates, hard gates, and required proof without
     duplicating post-build evidence?
   - If no metric exists, does it honestly say `Metrics: none mechanical`
     instead of inventing a proxy?
8. **Risk clarity**
   - Is the main risk named?
   - Is rollback or containment clear enough for the size of the change?
9. **Gap grounding**
   - If the work depends on external expectations, does the plan show what is
     currently missing and what comparable implementations prove should exist?
   - Are the references concrete instead of hand-wavy product intuition?
10. **Narrative usefulness**
   - If optional sections are present, do they actually reduce ambiguity?
   - Are they concrete rather than decorative or duplicated filler?
   - Does the plan speak in decisive action language instead of hedged
     possibilities?
   - Are refs/citations present only when they ground a claim or decision?
   - Is evidence omitted unless audit detail was explicitly requested?
11. **Architecture boundary**
   - If the plan still depends on invented entities, storage ownership, or
     runtime boundaries, did we stop and route to `deep-system-design`?

If any check fails, tighten the plan before presenting it. The final output
should show the review result, not the draft that failed it.

## References

- [prompts/plan.md](prompts/plan.md)
- [references/template.md](references/template.md)
- [references/examples.md](references/examples.md)
- [references/review.md](references/review.md)

## Final Check

Before handoff, read `references/review.md` and tighten the plan until it passes
