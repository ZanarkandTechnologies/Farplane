# Tickets

Active work in Codexter lives in ticket files.

Think of each ticket like a local Notion page:

- **frontmatter** = fixed machine-readable properties
- **body** = flexible human-readable task memory
- **folder placement** = Kanban lane / lifecycle view

One source of truth per concern:

- frontmatter answers "what is this task and what is its current execution state?"
- body answers "what does this task need, what happened, and how do I resume it?"
- file path answers "which board lane is this ticket in right now?"
- `docs/` answers "what should survive after this ticket is gone?"

`tickets/INDEX.md` is a non-authoritative human summary. Agents and automation should read the ticket file and its folder path, not the index, to determine current truth.

## Ownership Model

- `tickets/` = active work visibility + active task metadata
- nearest folder `README.md` = local/module rationale
- `docs/MEMORY.md`, `docs/HISTORY.md`, `docs/TROUBLES.md` = durable memory after work is complete

Tickets are intentionally **ephemeral**. They are for active or recently active work, not long-term archives.

## Lanes

- `tickets/todo/` = backlog, parked work, or quarantined work that is not part of the current active rollout
- `tickets/review/` = active planning / approval surface
- `tickets/building/` = approved implementation and verification surface only

Completed work does not need to accumulate forever in a board lane.

Recommended lifecycle:

1. create ticket in `todo/`
2. move to `review/` for planning/approval
3. move to `building/` for implementation
4. when implementation + verification pass, set `phase: documenting`
5. write durable docs
6. archive/delete the ticket or move it to `done/` only if a short-lived done lane is useful

## Canonical Dialect

Active tickets in `tickets/review/` and `tickets/building/` must use the canonical frontmatter dialect from `tickets/templates/ticket.md`.
Use the same dialect in `tickets/todo/` as well so backlog tickets do not drift into a second schema.

Rules:

- no `lane` frontmatter field
- no `## Status` body block
- no second machine-readable metadata block in the body
- `next_action` is the one authoritative next-step field
- `last_verification` is the one authoritative verification-summary field
- body prose may explain those fields, but must not compete with them

## Frontmatter Contract

Keep frontmatter small and typed. It exists for routing, DAG readiness, and quick resume.

Required v1 fields:

```yaml
---
ticket_id: TASK-0002
title: short title
phase: planning
status: active
owner: codex
priority: medium
depends_on: []
blocked_by: []
ready: false
approval_required: true
created_at: 2026-04-03T00:00:00Z
updated_at: 2026-04-03T00:00:00Z
next_action: await approval to move this ticket to building
last_verification: none
linked_docs: []
---
```

Recommended meanings:

- `phase`: one of `planning`, `building`, `documenting`, `complete`, `failed`
- `status`: short operational state such as `active`, `blocked`, `complete`, `failed`
- `depends_on`: DAG inputs that must be complete first
- `blocked_by`: dynamic ticket-ID blockers not captured by dependency edges
- `ready`: whether the ticket is actually executable now
- `approval_required`: whether user approval is required before execution may continue
- `next_action`: one visible next step; this is authoritative
- `last_verification`: latest compact verification status; this is authoritative

Invariants:

- board lane lives in folder placement, not frontmatter
- frontmatter must stay fixed-width and predictable across tickets
- the H1 title should match `ticket_id` plus `title`
- if a ticket moves folders, update the file path and `tickets/INDEX.md`, not a `lane` field
- do not move a ticket to `tickets/building/` while `approval_required: true`, `blocked_by` is non-empty, or a required dependency is still unresolved for that slice
- use `tickets/todo/` for quarantined or deferred work instead of leaving out-of-scope work in active lanes

## State Matrix

| Field | Source of truth | Allowed values | Transition / invariant |
| --- | --- | --- | --- |
| `lane` | folder path | `todo`, `review`, `building`, optional short-lived `done` | Change lane by moving the file. Do not duplicate lane in frontmatter. `tickets/INDEX.md` may summarize the lane but is not authoritative. |
| `phase` | frontmatter | `planning`, `building`, `documenting`, `complete`, `failed` | `planning` before execution approval, `building` during implementation, `documenting` after verification passes and before durable writeback, terminal values only when leaving active lanes. |
| `status` | frontmatter | `active`, `blocked`, `complete`, `failed` | Active lanes normally use `active` or `blocked`. `blocked` means progress cannot continue until `blocked_by` is cleared. Terminal values pair with terminal `phase` values. |
| `depends_on` | frontmatter | `[]` or a short list of ticket IDs | Structural prerequisite edges. A ticket may sit in `todo/` or `review/` while these are unresolved, but it must not move to `tickets/building/` until the required upstream tickets have reached the needed checkpoint for this slice. |
| `ready` | frontmatter | `true`, `false` | `false` whenever `approval_required: true`, any `blocked_by` item exists, a required dependency prevents the recorded next step, or the next recorded step cannot be executed now. `true` means the agent can take `next_action` immediately in the current lane. |
| `blocked_by` | frontmatter | `[]` or a short list of ticket IDs | Immediate ticket blockers preventing `next_action`. Use this only for concrete ticket-ID blockers. Non-empty `blocked_by` requires `status: blocked` and `ready: false`. Non-ticket blockers belong in the body `## Blockers` section. |
| `approval_required` | frontmatter | `true`, `false` | Use `true` only for explicit approval gates. It implies `phase: planning` and `ready: false`. Clear it before or when moving the ticket to `tickets/building/`; do not leave approval-gated work in the building lane. |
| `updated_at` | frontmatter | UTC ISO 8601 timestamp | Update on every substantive ticket change, including frontmatter or body changes that affect active work state, evidence, blockers, or handoff. Never move backward in time. |
| `last_verification` | frontmatter | `none` or a compact summary string | Update only after actual verification. Use `none` when no verification has run yet. Keep full command notes in the body, but treat this field as the authoritative summary. |

Operational rule:

- `next_action` is the authoritative current step. Handoff and plan sections may add context, but they should not invent a second state field.
- `tickets/INDEX.md` should mirror file moves and lane changes for humans, but it never overrides the ticket file or folder path.
- `blocked_by` must contain only ticket IDs. Use the body `## Blockers` section for prose blockers, repo decisions, policy boundaries, or environmental notes.

## Validator

Use `python3 bin/check_ticket_metadata.py` to validate the ticket contract.

The validator currently checks:

- canonical frontmatter exists
- required fields exist
- `lane` is not duplicated in frontmatter
- `ticket_id` matches the filename
- `blocked_by` entries are ticket IDs only
- `approval_required: true` implies `ready: false`
- `status: blocked` implies `ready: false`
- tickets in `review/` or `building/` are not left in the legacy body dialect

The validator is intentionally small. It exists to catch trust-breaking drift, not to become a second orchestration system.

## Body Contract

The body is the task-local memory area.

Keep these sections:

- `Summary`
- `Scope`
- `Plan`
- `Acceptance Criteria`
- `Working Notes`
- `Implementation Notes`
- `Evidence`
- `Blockers`
- `Handoff`
- `Writeback`

Rules:

- task-local notes stay in the ticket while work is active
- durable cross-task lessons move to docs during `documenting`
- do not turn the ticket into a permanent design archive
- keep detailed verification commands and outputs in `Evidence`; keep the canonical summary in `last_verification`

## Anti-Goals

v1 intentionally does **not** include:

- separate per-ticket JSON state files
- `run_id`
- parallel run trees
- hidden automation
- auto-continue or auto-approval behavior
- assisted continuation or tracked stop-hook wiring
- a canonical hook/runtime active-ticket selector
- large metadata schemas

## V1 Runtime Boundary

The ticket metadata foundation is intentionally a **visible file contract**, not a runtime orchestration system.

That means v1 does **not** assume:

- a hook can always determine the current active ticket
- ticket frontmatter is safe to mutate automatically from every runtime context
- multiple active `building` tickets can be reconciled by guesswork

Until a separate downstream ticket defines and proves an explicit active-ticket selector, agents should treat ticket metadata as **human-visible source of truth first** and runtime-write target second.

## Example

```markdown
---
ticket_id: TASK-0002
title: add notion-style ticket metadata foundation
phase: planning
status: active
owner: codex
priority: high
depends_on:
  - TASK-0001
blocked_by: []
ready: false
approval_required: true
created_at: 2026-04-03T00:00:00Z
updated_at: 2026-04-03T12:30:00Z
next_action: await approval to move this ticket to building
last_verification: none
linked_docs:
  - docs/research/web-research/2026-04-02_run-artifacts-risk-analysis.md
---

# TASK-0002: add notion-style ticket metadata foundation

## Summary
Make the ticket itself the active task object.

## Working Notes
- Keep frontmatter fixed and compact.
- Keep lane out of frontmatter; the folder already says it.
- Keep durable lessons out of the ticket after completion.

## Handoff
- Current state: plan ready for approval
- Resume from: this ticket plus linked docs
```
