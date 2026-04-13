---
name: spec-to-ticket
version: 1.5.0
description: "Phase-2 Codexter skill: convert one SLC slice from specs into raw ticket files under tickets/, including compact diagram-first summaries plus agent-contract and evidence-checklist requirements for UI-bearing work."
---

# Spec-to-Ticket Skill

Use this as the second session in the Codexter workflow.

<!--
This skill is where product intent becomes executable ticket truth.
It should front-load testability and proof requirements so build and QA do not have to improvise later.
-->

## Job

Given `docs/specs/*.md`, pick exactly one SLC slice and convert it into actionable raw ticket files under `tickets/`.

## Rules

1. One SLC slice per planning pass.
2. One ticket = one build loop (default).
3. Default to the largest self-contained feature-sized ticket that still fits one build loop.
4. In greenfield work, keep endpoint, backend logic, UI, and tests together when they serve one coherent human-testable capability.
5. Split only when a real trigger applies: shared platform work reused by multiple future features; risky migration/backfill/rollout work; external dependency/provisioning work that can block independently; or unresolved feasibility that needs an investigation/proof step first.
6. When a split is needed, make dependency order explicit from the real boundary; do not split by schema/backend/UI layers just because they differ architecturally.
7. No implementation in this phase.
8. Write ticket files to `tickets/` with `status: todo`; do not use `docs/progress.md` as the primary board.
9. If the slice includes any UI, the ticket must define agent testability and QA shape before build starts.
10. If a UI flow is hard for an agent to access or stabilize, add testability instrumentation work into the slice instead of leaving QA to improvise.
11. Every non-trivial ticket should declare a `Test hook`; if none is needed, say `none needed` explicitly.
12. For material, cross-module, or architecture-facing tickets, include a compact `Diagram Summary` before the longer plan prose and follow `skills/diagramming/SKILL.md` plus `docs/specs/diagram-first-conventions.md` for style/taste.

## Inputs

- `docs/specs/*.md`
- optionally `docs/prd.md` for slice intent
- optionally `docs/TASTE.md` for shared UI doctrine
- `tickets/templates/ticket.md`

## Output

- `tickets/*.md` ticket files with:
  - goal
  - diagram-first approval summary for material work
  - acceptance criteria
  - dependencies
  - assignee
  - required evidence/backpressure
  - control fields for state movement
  - for UI-bearing tickets: `Agent Contract` + `Evidence checklist`
  - `User Evidence` placeholders

## UI-bearing Ticket Contract

<!--
The Agent Contract is the bridge between planning and autonomous execution.
If this block is vague, build and QA will reward-hack route completion instead of proving the intended UI.
-->

For any ticket that changes UI, canvas rendering, user-visible flows, or browser interaction, add a compact `Agent Contract` block.

Required fields:

- `Open`: launch path or command, plus stable route/deeplink if available
- `Test hook`: the cheapest deterministic proof surface, such as a CLI command, seed/reset path, debug route, fixture loader, sanity script, or `none needed`
- `Stabilize`: reset/seed path plus shortcuts/debug controls if determinism matters
- `Inspect`: required hooks, selectors, overlays, or DOM mirrors
- `Key screens/states`: the important surfaces QA must reach and compare
- `Taste refs`: the relevant visual doctrine from `docs/TASTE.md`, plus any local exception
- `Expected artifacts`: screenshots, snapshots, traces, or other proof
- `Delegate with`: ticket ID, ticket file path/section, recommended assignee, expected output artifact

Add a compact `Evidence checklist` below the `Agent Contract` for UI-bearing tickets.

<!--
Evidence should be declared up front so QA knows which artifacts must exist before the ticket can close.
Keep the list short; over-declaring proof makes the loop noisy.
-->

Good checklist items are concrete proof artifacts, for example:

- `Screenshot: default screen`
- `Screenshot: empty state`
- `Screenshot: modal open`
- `Snapshot: interaction state`
- `QA report linked`

The checklist should stay short and only include proof the ticket actually needs.

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
2. Start with the largest coherent self-contained feature ticket that would feel like one strong fullstack engineer assignment.
3. If that candidate no longer fits one build loop, justify the split with one of the hard triggers above instead of falling back to layer boundaries.
4. For each ticket, write concrete acceptance criteria, control fields, evidence requirements, and a `Test hook`.
5. For each material ticket, write a compact `Diagram Summary` with one top-level delta map; use `diagramming` for inline-signature, color/legend, and anti-bloat patterns.
6. For each UI-bearing ticket, add a compact `Agent Contract` block plus `Evidence checklist`.
7. If agentic testing looks weak, add instrumentation work into the ticket now instead of hoping QA can discover a path later.
8. Write the finished raw tickets into `tickets/` using the ticket template.
9. Before handoff, read `references/review.md` and tighten the ticket set until it passes those checks.

## Capability-First Examples

Keep together when the ticket still describes one human-testable capability.

- Greenfield ingestion feature: endpoint, parsing pipeline, chunking, embeddings, vector search, full-text search, basic operator UI, and tests can stay one ticket when the operator would validate them as one feature.
- New CRUD workflow: schema change, backend handlers, screens, validation, and tests can stay one ticket when they form one complete workflow.

Split when one of the explicit hard triggers makes the work stop being one coherent build loop.

- Split out shared platform work: the ingestion feature plus a reusable search abstraction for multiple future features should become at least two tickets.
- Split out migration/backfill work: the feature plus a risky migration of existing data or rollout/backfill plan should become at least two tickets.
- Split out external dependency setup: the feature plus vendor provisioning, IAM/webhook setup, or another separately blocking external dependency should become at least two tickets.
- Split out unresolved feasibility: a speculative retrieval or ranking approach that still needs proof should get an investigation/proof ticket before the main build ticket.

## Top Gotchas

1. Do not let UI tickets say "verify in browser" without stating how the agent reaches and inspects the screen.
2. Do not defer missing testability controls to QA if you can already see they are needed.
3. Do not leave testability implicit; a ticket should say what the agent runs or opens to prove the feature.
4. Do not write vague visual criteria like "looks good"; encode the key screens, states, and expected proof artifacts.
5. Do not split a coherent feature into schema/backend/UI tickets just because those layers differ.
6. Do not hide overflow scope in prose; if a real split trigger exists, spawn the follow-up ticket explicitly.
7. Do not use "one big feature ticket" as cover for multiple unrelated capabilities; the ticket must still read like one self-contained build loop.

## Templates

- Spec structure: `references/spec-template.md`
- Ticket structure: `references/ticket-template.md`
- SLC framing: `references/story-map-slc.md`
- Review guide: `references/review.md`
