# Context And Handoff Policy

Date: 2026-04-07

## Goal

Define the visible progress-surface, reset/resume handoff, documenting, and
archive rules for the spec-first Farplane loop.

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
- evidence status
- blockers
- next action
- last verification

`last_verification` should stay a one-line current verdict. Detailed proof
belongs in the ticket `Evidence` section.

### Runtime State

`.farplane/state/sessions/{session_id}.json` is the preferred runtime lane surface
when hook `session_id` is available.

`.farplane/state/current-run.json` is the runtime-only compatibility state.

It may carry:

- active claim for the current ticket/run/session
- human-readable session alias such as `session_name`
- delegated worker identity such as `worker_name`
- delegated main artifact path and latest `grounding_summary`
- delegated wait/checkpoint timing such as `worker_started_at`, `last_checkpoint_at`, and `checkpoint_summary`
- active ticket id/path
- active phase
- active session or pane id
- active run-state path
- latest captured current-turn user intent
- latest intent-alignment result
- latest worker result
- latest judge/hook verdict
- latest hook summary
- advisory backpressure status derived from stale delegated waits

Lookup precedence should be:

1. explicit run-state selector for a managed lane
2. hook `session_id` mapped to a session state file
3. `.farplane/state/current-run.json`

It must not become the durable source of:

- scope
- acceptance criteria
- blocker truth
- final handoff instructions
- the human-facing board claim alias; that belongs on the ticket when the claim is explicit

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
- body:
  - `Refs` when durable linked docs changed
  - `Evidence`
  - `Blockers`

If extra resume context is still needed after frontmatter plus evidence/blockers,
add a short `Notes` entry instead of a dedicated handoff template.

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
- durable docs and proof links should already be visible from `Refs` and
  `Evidence` when applicable

Archive is history, not hot execution state.

Do not use archived tickets as the normal active progress surface.
