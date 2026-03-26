---
name: spec-to-ticket
version: 1.3.0
description: "Phase-2 Ralph skill: convert one SLC slice from specs into raw ticket files under tickets/todo/, including compact agent-contract and evidence-checklist requirements for UI-bearing work."
---

# Spec-to-Ticket Skill

Use this as the second session in the Ralph workflow.

<!--
This skill is where product intent becomes executable ticket truth.
It should front-load testability and proof requirements so build and QA do not have to improvise later.
-->

## Job

Given `docs/specs/*.md`, pick exactly one SLC slice and convert it into actionable raw ticket files under `tickets/todo/`.

## Rules

1. One SLC slice per planning pass.
2. One ticket = one build loop (default).
3. Dependency order: schema -> backend -> UI -> integration.
4. No implementation in this phase.
5. Write ticket files to `tickets/todo/`; do not use `docs/progress.md` as the primary board.
6. If the slice includes any UI, the ticket must define agent testability and QA shape before build starts.
7. If a UI flow is hard for an agent to access or stabilize, add testability instrumentation work into the slice instead of leaving QA to improvise.
8. Every non-trivial ticket should declare a `Test hook`; if none is needed, say `none needed` explicitly.

## Inputs

- `docs/specs/*.md`
- optionally `docs/prd.md` for slice intent
- optionally `docs/TASTE.md` for shared UI doctrine
- `tickets/templates/ticket.md`

## Output

- `tickets/todo/*.md` ticket files with:
  - goal
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
pick one slice, split it, add proof/testability, then write real ticket files into tickets/todo/.
-->

1. Read `docs/specs/*.md` and pick exactly one SLC slice.
2. Split the slice into dependency-ordered tickets.
3. For each ticket, write concrete acceptance criteria, control fields, evidence requirements, and a `Test hook`.
4. For each UI-bearing ticket, add a compact `Agent Contract` block plus `Evidence checklist`.
5. If agentic testing looks weak, add instrumentation work into the ticket now instead of hoping QA can discover a path later.
6. If the slice is too large, split it into multiple smaller tickets in `tickets/todo/` immediately.
7. Write the finished raw tickets into `tickets/todo/` using the ticket template.
8. Before handoff, read `references/review.md` and tighten the ticket set until it passes those checks.

## Top 3 Gotchas

1. Do not let UI tickets say "verify in browser" without stating how the agent reaches and inspects the screen.
2. Do not defer missing testability controls to QA if you can already see they are needed.
3. Do not leave testability implicit; a ticket should say what the agent runs or opens to prove the feature.
4. Do not write vague visual criteria like "looks good"; encode the key screens, states, and expected proof artifacts.
4. Do not hide overflow scope in prose; spawn a follow-up ticket instead.

## Templates

- Spec structure: `references/spec-template.md`
- Ticket structure: `references/ticket-template.md`
- SLC framing: `references/story-map-slc.md`
- Review guide: `references/review.md`
