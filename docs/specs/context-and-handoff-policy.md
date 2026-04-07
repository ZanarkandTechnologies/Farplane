# Context And Handoff Policy

Date: 2026-04-07

## Goal

Define the visible progress-surface, reset/resume handoff, documenting, and
archive rules for the spec-first Codexter loop.

The intent is simple:

- tickets stay authoritative
- runtime state stays lightweight
- fresh sessions can resume from visible artifacts without hidden memory

## Progress Surface

### Ticket

The ticket is the canonical durable surface.

It must carry:

- frontmatter queue/execution state
- summary and scope
- current plan
- acceptance criteria
- evidence status
- blockers
- handoff notes
- next action
- last verification

### Runtime State

`.ralph/state/current-run.json` is runtime-only.

It may carry:

- active ticket id/path
- active phase
- active session or pane id
- latest worker result
- latest judge/hook verdict
- latest hook summary

It must not become the durable source of:

- scope
- acceptance criteria
- blocker truth
- final handoff instructions

### Transcript

The transcript is disposable.

It is useful evidence, but it is not the canonical resume surface.

## Stay / Reset / Resume Rules

Stay in the same session when:

- the ticket is still the same
- the next action is obvious
- no deliberate human handoff/reset is needed

Prepare a deliberate reset/resume only after the ticket is updated with:

- `next_action`
- `last_verification`
- current blocker state
- any new evidence references
- a short `Handoff` note saying where to resume

Do not rely on chat memory alone for deliberate resume.

## Handoff Requirements

Before ending a ticket session that may need resume, update:

- frontmatter:
  - `phase`
  - `status`
  - `ready`
  - `blocked_by`
  - `next_action`
  - `last_verification`
  - `linked_docs`
- body:
  - `Evidence`
  - `Blockers`
  - `Handoff`

The `Handoff` section should always answer:

- current state
- what remains
- where to resume first

## Documenting Phase

Use `phase: documenting` after implementation and verification are complete but
before the ticket is archived.

That phase exists to:

- move durable lessons into `docs/`
- update linked specs/readmes/contracts
- make the archive copy readable without reopening the whole transcript

Do not archive directly from active implementation work when durable writeback is
still missing.

## Archive Rules

Move a ticket to `tickets/archive/` only when one of these is true:

1. implementation/documentation is complete and the ticket is no longer active
2. the ticket is a completed exploratory or smoke/runtime ticket
3. the ticket is superseded and explicitly no longer the active slice

Before archive:

- `status` should be `done` or `failed`
- `phase` should reflect terminal state such as `complete` or `failed`
- `Writeback` and `Handoff` should be coherent
- durable docs should already be linked from `linked_docs` when applicable

Archive is history, not hot execution state.

Do not use archived tickets as the normal active progress surface.
