---
name: spec-to-ticket
version: 1.5.0
description: "Turn one SLC spec slice into filesystem tickets with compact summaries, agent contracts, and evidence requirements."
tier: 3
group: coding
source: local
common_chains:
  after: ["impl-plan"]
---

# Spec-to-Ticket Skill

<!-- BEGIN FARPLANE_IMPORTANT_CHECKLIST -->
## Todo List

- [ ] Read the chosen spec slice and confirm it is small enough for one planning pass.
- [ ] Shape tickets through the native planning phase, but keep
  `spec-to-ticket` coding-ticket specific.
- [ ] Use the relevant [research](../research/SKILL.md) method when ticket
  scope depends on local baseline, examples, official behavior, peer norms, or
  implementation patterns.
- [ ] Carry the
  [first-principles-planning](../../docs/specs/first-principles-planning.md)
  basis into ticket boundaries: objective, need, assumptions, root cause,
  constraints, first viable slice, proof/falsification, tradeoffs, and
  non-goals.
- [ ] Start from the largest coherent self-contained feature ticket; do not split by schema/backend/UI layers just because those layers differ.
- [ ] Keep CRUD and other narrow operator workflows in one ticket by default.
- [ ] Split only when a hard trigger applies: shared platform reuse, migration/backfill/rollout risk, external dependency/provisioning, unresolved feasibility, or a real service/runtime boundary.
- [ ] For complex systems, make the first ticket leave behind a minimal end-to-end happy path plus a reusable proof surface instead of empty scaffolding.
- [ ] Group later follow-up tickets by shared proof surface or adjacent operator value, not one internal pipeline stage per ticket.
- [ ] Make `Done / Proof`, evidence needs, and control fields concrete in each
  ticket.
- [ ] If an `Agent Testability Brief` exists, carry its surfaces into the ticket contract instead of re-deriving them.
- [ ] If there is no richer testability brief yet but `docs/bootstrap-brief.md` has `Agent Experience / Testability`, use it as the fallback seed for the first UI-bearing or agentically hard ticket.
- [ ] If `docs/bootstrap-brief.md` or `docs/prd.md` names a project profile,
  load [project-profiles](../deep-init-project/references/project-profiles.md)
  and carry component matrix, selected directions, prototype gates, pipeline
  handoffs, and proof surfaces into ticket boundaries.
- [ ] Map PRD/spec work into project lifecycle ticket loops from
  [project-lifecycle](../deep-init-project/references/project-lifecycle.md):
  planner owner, executor owner, proof owner, and closeout owner.
- [ ] If a profile prototype gate names a real unresolved risk, create the
  PoC/proof ticket before full production tickets; do not make PoC tickets
  mechanically when the risk is already resolved.
- [ ] If a ticket includes UI, define the `Agent Contract` and testability
  shape up front.
- [ ] If the repo has `qa/cookbook/` and the slice is UI-bearing or agentically hard, seed or update the matching workflow entry.
- [ ] If determinism or agent access looks weak, turn that into explicit instrumentation work now instead of hoping QA can improvise later.
- [ ] Write the raw tickets into `tickets/` with the correct state fields.
- [ ] Tighten the result against the [review guide](./references/review.md) before handoff.
- [ ] Stop after ticket creation and do not implement the slice here.
<!-- END FARPLANE_IMPORTANT_CHECKLIST -->

Use this as the second session in the Farplane workflow.

`spec-to-ticket` is a Tier 3 Farplane coding-pipeline skill. It specializes the
native planning phase for turning code-oriented specs into proofable tickets.

<!--
This skill is where product intent becomes executable ticket truth.
It should front-load testability and proof requirements so build and QA do not have to improvise later.
-->

## Job

Given `docs/specs/*.md`, pick exactly one SLC slice and convert it into actionable raw ticket files under `tickets/`.

## Rules

1. One SLC slice per planning pass.
2. One ticket = one ambitious build loop (default), not one timid checkpoint.
3. Default to the largest self-contained feature-sized ticket that still fits one strong build-and-proof pass.
4. In greenfield work, keep endpoint, backend logic, UI, and tests together when they serve one coherent human-testable capability. CRUD workflows stay one ticket by default.
5. Split only when a real trigger applies: shared platform work reused by multiple future features; risky migration/backfill/rollout work; external dependency/provisioning work that can block independently; unresolved feasibility that needs an investigation/proof step first; or a real service/runtime boundary that will be independently owned or scaled.
6. When a split is needed, group work by proof surface, reusable foundation, or independently blocking boundary; do not split by schema/backend/UI layers or by individual pipeline stages just because those steps exist.
7. For complex systems, the first ticket should usually leave behind both a reusable proof surface and one minimal end-to-end happy path rather than scaffolding with no operator-visible proof.
8. No implementation in this phase.
9. Write ticket files to `tickets/` with `status: todo`; do not use `docs/progress.md` as the primary board.
10. If the slice includes any UI, the ticket must define agent testability and QA shape before build starts.
11. If a UI flow is hard for an agent to access or stabilize, add testability instrumentation work into the slice instead of leaving QA to improvise.
12. Every non-trivial ticket should declare a `Test hook`; if none is needed, say `none needed` explicitly.
13. When an `Agent Testability Brief` exists, carry its control accelerators, state probes, coordination views, and proof surfaces into the ticket contract instead of re-deriving them.
14. When `docs/bootstrap-brief.md` includes `Agent Experience / Testability` defaults and there is no richer `Agent Testability Brief`, use those defaults as the fallback source for the first UI-bearing or agentically hard ticket.
15. Carry mechanically meaningful metric candidates from the PRD or spec into
    each ticket's `Done / Proof`, and write `none mechanical` when a metric
    would be fake or subjective.
16. Carry run-readiness fields from the PRD, bootstrap brief, system design,
    taste brief, or agent testability brief into `Run Hints` for any ticket
    expected to run unattended, in a batch, or under `$ralph`.
16d. Add `Run Hints` for material, unattended, `$ralph`, or batchable work.
    These hints are advisory context for `$work`, not runtime authority.
    Include likely size, Goal recommendation, compute hint, proof weight,
    batchability, and why.
16a. When the bootstrap brief or PRD carries a `ProjectProfile`, use its
    component matrix, selected directions, prototype gates, pipeline handoffs,
    and proof surfaces to shape ticket boundaries.
16b. When a profile prototype gate names a real unresolved risk, create the
    PoC/proof ticket before broader production tickets. Do not create prototype
    tickets mechanically when the PRD already resolved the risk.
16c. Carry first-principles basis from the PRD or spec into ticket boundaries:
    objective, need, assumptions, root cause, constraints, first viable slice,
    proof/falsification, tradeoffs, and non-goals.
17. When the repo has `qa/cookbook/` and the slice is UI-bearing or agentically hard, seed or update a matching `qa/cookbook/<workflow>.md` entry so QA inherits the same fast-entry, stabilize, inspect, and proof surfaces as the ticket.
18. For material, cross-module, or architecture-facing tickets, include a compact `Diagram Summary` before the longer plan prose and follow `skills/diagramming/SKILL.md` for style/taste.

## Inputs

- `docs/specs/*.md`
- optionally `docs/specs/*-agent-testability.md` or `docs/specs/agent-testability-surfaces.md`
- optionally `docs/bootstrap-brief.md`
- optionally `docs/prd.md` for slice intent
- optionally `docs/specs/first-principles-planning.md` when shaping material
  ticket boundaries or preserving PRD/spec basis
- optionally `skills/deep-init-project/references/project-profiles.md` when a
  bootstrap or PRD profile is present
- optionally `docs/TASTE.md` for shared UI doctrine
- optionally `qa/cookbook/*.md` when the repo already keeps reusable QA workflows
- `tickets/templates/ticket.md`

## Output

- `tickets/*.md` ticket files with:
  - compact `Summary`, `Scope`, `Delta`, `Program`, `Map`, `Done / Proof`,
    `State`, `Links`, and sparse `Notes`
  - map-first approval summary for material work
  - done conditions
  - dependencies
  - assignee
  - required evidence/backpressure
  - `Done / Proof` with metric handles, caller-declared rubric families,
    required TAS gates, hard gates, checks, and required evidence obligations
  - `Run Hints` for `$work` admission when useful
  - control fields for state movement
  - for UI-bearing tickets: `Agent Contract`
  - when the repo has `qa/cookbook/` and the slice is UI-bearing or
    agentically hard: matching cookbook seed or update
  - `Run Hints` for any ticket whose execution might be delegated, looped, or
    drained by `$ralph`

## UI-bearing Ticket Contract

<!--
The Agent Contract is the bridge between planning and autonomous execution.
If this block is vague, build and QA will reward-hack route completion instead of proving the intended UI.
-->

For any ticket that changes UI, canvas rendering, user-visible flows, or browser interaction, add a compact `Agent Contract` block.

When an `Agent Testability Brief` exists, use it to fill these fields instead of inventing new testability doctrine from scratch.
If there is no richer testability brief yet but `docs/bootstrap-brief.md`
includes `Agent Experience / Testability`, use those bootstrap defaults as the
fallback source.

Required fields:

- `Open`: launch path or command, plus stable route/deeplink if available
- `Test hook`: the cheapest deterministic proof surface, such as a CLI command, seed/reset path, debug route, fixture loader, sanity script, or `none needed`
- `Stabilize`: reset/seed path plus shortcuts/debug controls if determinism matters
- `Inspect`: required hooks, selectors, overlays, or DOM mirrors
- `Key screens/states`: the important surfaces QA must reach and compare
- `QA cookbook`: matching `qa/cookbook/<workflow>.md` path when the repo keeps
  reusable QA workflows, otherwise `none yet`
- `Taste refs`: the relevant visual doctrine from `docs/TASTE.md`, plus any local exception
- `Expected artifacts`: screenshots, snapshots, traces, or other proof
- `Delegate with`: ticket ID, ticket file path/section, recommended assignee, expected output artifact

Declare required UI evidence in `Done / Proof` so QA knows which artifacts must
exist before the ticket can close. Keep the list short; over-declaring proof
makes the loop noisy. Good items are concrete proof artifacts, for example:

- `Screenshot: default screen`
- `Screenshot: empty state`
- `Screenshot: modal open`
- `Snapshot: interaction state`
- `QA report linked`

The evidence list should stay short and only include proof the ticket actually
needs.

If the UI is hard to test without extra controls, turn those controls into explicit ticket work. Typical examples:

- local CLI smoke commands or sanity scripts,
- pause/resume or step controls for games,
- debug overlays or DOM mirrors for canvas state,
- stable panel shortcuts,
- CLI helpers for repetitive launch/setup paths.

Default UI doctrine should live in `docs/TASTE.md`. Tickets should reference taste briefly instead of repeating long style prose. Only add ASCII when screen structure itself is hard to explain in words.

## Workflow

<!--
The core planning loop here is:
pick one slice, keep the largest coherent feature ticket you can, add proof/testability, then write real ticket files into tickets/.
-->

1. Read `docs/specs/*.md` and pick exactly one SLC slice.
2. Read the `Agent Testability Brief` when one exists and note the required control accelerators, state probes, coordination views, and proof surfaces for the chosen slice.
2a. When the source spec includes a conformance matrix from
    `docs/specs/spec-authoring-contract.md`, slice tickets around proofable
    requirements and carry the relevant `Profile`, `Proof`, and `Ticket` rows
    into the ticket's acceptance criteria and verification plan.
3. If there is no richer testability brief yet, read `docs/bootstrap-brief.md`
   and reuse its `Agent Experience / Testability` defaults for the first
   UI-bearing or agentically hard slice.
3a. If `docs/bootstrap-brief.md` or `docs/prd.md` names a project profile,
    carry the component matrix, selected directions, prototype gates, and
    pipeline handoffs into the ticket split.
3b. Carry the first-principles basis from the PRD/spec into the ticket split:
    objective, need, assumptions, root cause, constraints, first viable slice,
    proof/falsification, tradeoffs, and non-goals.
4. Start with the largest coherent self-contained feature ticket that would feel like one strong fullstack engineer or agent assignment.
4a. If a profile prototype gate remains unresolved, make the first ticket a
    tiny proof/PoC that removes the highest uncertainty and leaves a reusable
    proof surface behind.
5. If that candidate no longer fits one build loop, justify the split with one of the hard triggers above and choose the boundary that removes the most future friction while preserving strong proof.
6. For each ticket, write concrete done conditions, control fields, evidence
   requirements, and a `Test hook`.
7. For each material ticket, add a compact `Done / Proof` block that names
   mechanical metrics or `none mechanical`, caller-declared rubric families,
   required TAS gates, hard gates, checks, and required evidence artifacts.
8. For each material ticket, write a compact `Map` with one top-level delta
   diagram when useful; use `diagramming` for inline-signature, color/legend,
   and anti-bloat patterns.
9. For each UI-bearing or agentically hard ticket, add a compact
   `Agent Contract` block, carrying forward the brief or bootstrap surfaces
   when relevant.
10. For each `$ralph`-ready, batchable, or long-running ticket, add `Run Hints`
   with needed inputs/assets, credentials, compute, tools, QA risks, human
   gates, likely size, Goal recommendation, planning hint, proof weight,
   batchability, and no-batch reason when relevant.
11. If the repo has `qa/cookbook/` and the slice is UI-bearing or agentically hard, seed or update a matching `qa/cookbook/<workflow>.md` entry from the same `Open`, `Stabilize`, `Inspect`, and proof assumptions.
12. If agentic testing looks weak, add instrumentation work into the ticket now instead of hoping QA can discover a path later.
13. Write the finished raw tickets into `tickets/` using the ticket template.
14. Before handoff, read `references/review.md` and tighten the ticket set until it passes those checks.

## Ambition-Aware Sizing

Choose the split shape from complexity and proof structure, not from how many internal steps happen inside the system.

- Simple workflow or CRUD capability: keep the whole workflow in one ticket when one agent can change the schema, handlers, UI, validation, and proof in one pass.
- Compound capability with one main proof surface: keep the first ticket broad enough to ship a minimal end-to-end happy path plus the cheapest reusable proof harness, then group later adjacent expansions into a small number of follow-up tickets.
- Platform- or service-heavy system: split when a reusable foundation, risky migration, external blocker, or real service boundary would otherwise distort the main feature ticket.

The first ticket for a complex feature should remove the biggest uncertainty class, not just complete the first implementation step.

## Capability-First Examples

Keep together when the ticket still describes one human-testable capability.

- Greenfield ingestion feature: endpoint, parsing pipeline, chunking, embeddings, vector search, full-text search, basic operator UI, and tests can stay one ticket when the operator would validate them as one feature.
- New CRUD workflow: schema change, backend handlers, screens, validation, and tests can stay one ticket when they form one complete workflow.

Split when one of the explicit hard triggers makes the work stop being one coherent build loop.

- Split out shared platform work: the ingestion feature plus a reusable search abstraction for multiple future features should become at least two tickets.
- Split out migration/backfill work: the feature plus a risky migration of existing data or rollout/backfill plan should become at least two tickets.
- Split out external dependency setup: the feature plus vendor provisioning, IAM/webhook setup, or another separately blocking external dependency should become at least two tickets.
- Split out unresolved feasibility: a speculative retrieval or ranking approach that still needs proof should get an investigation/proof ticket before the main build ticket.
- Split out a real service boundary: if one part will be deployed, scaled, or owned as its own service, that can justify a separate ticket; do not invent a service split only for planning neatness.

## Complexity Examples

- CRUD admin flow: one ticket for schema, create/edit/delete handlers, form/table UI, validation, and proof.
- Complex ingestion system:
  - Ticket 1: one source -> parse -> persist -> observable proof path, plus the harness or debug surfaces needed to prove it cheaply.
  - Ticket 2: grouped reliability or enrichment work such as retries, dedupe, chunk tuning, and operator observability when those changes share the same proof surface.
  - Ticket 3: cloud hardening, backfill, vendor/IAM setup, or a separately deployed worker/service when those are independently blocking or scalable concerns.
- Avoid parse/chunk/embed/index/search as five tickets unless those are truly separate ownership or proof boundaries.

## Top Gotchas

1. Do not let UI tickets say "verify in browser" without stating how the agent reaches and inspects the screen.
2. Do not defer missing testability controls to QA if you can already see they are needed.
3. Do not leave testability implicit; a ticket should say what the agent runs or opens to prove the feature.
4. Do not write vague visual criteria like "looks good"; encode the key screens, states, and expected proof artifacts.
5. Do not mark tickets `$ralph`-ready when credentials, compute, external
   access, hard-to-QA surfaces, or human gates are still unnamed.
5a. Do not treat `Run Hints` as permission to start work.
    Tickets, cards, and `compute_target` remain context; explicit invocation
    starts execution.
6. Do not split a coherent feature into schema/backend/UI tickets just because those layers differ.
7. Do not split a complex pipeline into one ticket per internal step when one grouped foundation or expansion ticket would be more executable.
8. Do not let the first ticket be empty scaffolding; it should leave a reusable proof path behind.
9. Do not hide overflow scope in prose; if a real split trigger exists, spawn the follow-up ticket explicitly.
10. Do not use "one big feature ticket" as cover for multiple unrelated capabilities; the ticket must still read like one self-contained build loop.

## Templates

- Complex spec structure: `../../docs/specs/spec-authoring-contract.md`
- Spec structure: `references/spec-template.md`
- Ticket structure: `references/ticket-template.md`
- SLC framing: `references/story-map-slc.md`
- Review guide: `references/review.md`
