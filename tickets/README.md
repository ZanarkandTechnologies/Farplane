# Tickets

Active work lives in `tickets/TASK-*.md`.

One source of truth per concern:

- frontmatter = queue state and execution state
- body = plan, evidence, blockers, and handoff
- `.harness/state/` = live runtime state
- `docs/` = durable knowledge after the ticket is done
- transcript = disposable context, not the canonical resume surface

## Canonical Layout

```text
tickets/
  TASK-0001-example.md
  TASK-0002-example.md
  archive/
    TASK-0000-finished-example.md
  templates/
    ticket.md
```

No lane folders. No hand-maintained board file. The ticket itself is the board card.

## Lifecycle

1. create the ticket in `tickets/`
2. set `status: todo` or `status: review`
3. after approval, set `status: building`
4. when implementation and verification pass, set `phase: documenting`
5. write durable docs
6. move the ticket into `tickets/archive/` when it is no longer active, or set `status: done` briefly if you intentionally want a short-lived visible completion state before archiving

## Progress Surface Policy

- the ticket is the canonical durable progress surface
- `.harness/state/` is runtime-only and may track active claim/lane/session/verdict state
- transcripts are useful evidence but are not the canonical resume surface
- deliberate reset/resume requires the ticket to carry a clear `next_action`,
  `last_verification`, and `Handoff` note

## Canonical Frontmatter

```yaml
---
ticket_id: TASK-0002
title: short title
phase: planning
status: review
owner: codex
claimed_by: agent-03  # optional active session claim alias
priority: medium
depends_on: []
blocked_by: []
ready: false
approval_required: true
created_at: 2026-04-03T00:00:00Z
updated_at: 2026-04-03T00:00:00Z
next_action: await approval to set status: building
last_verification: none
linked_docs: []
---
```

## Field Meanings

- `phase`: `planning`, `building`, `documenting`, `complete`, `failed`
- `status`: `todo`, `review`, `building`, `blocked`, `done`, `failed`
- `owner`: broad work owner, not a live session id
- `claimed_by`: optional human-facing active claim alias for the current live session, such as `agent-03`
- `depends_on`: structural prerequisites
- `blocked_by`: concrete ticket-ID blockers only
- `ready`: whether `next_action` can be executed now
- `approval_required`: explicit approval gate
- `next_action`: the one authoritative next step
- `last_verification`: the authoritative verification summary

## Invariants

- no `lane` field
- no `## Status` body block
- the H1 matches `ticket_id` and `title`
- do not store raw transport-level runtime ids such as `session_id` in ticket frontmatter
- do not set `status: building` while `approval_required: true`
- do not set `status: building` while `blocked_by` is non-empty
- do not invent a second machine-readable state block in the body

## Validator

Run:

```bash
python3 tickets/scripts/check_ticket_metadata.py
```

The validator intentionally only checks the flat `tickets/TASK-*.md` surface.

## Body Contract

Keep these sections:

- `Summary`
- `Scope`
- `User Story` when the work is material or ambiguous
- `User Pain / JTBD` when the work is material or ambiguous
- `Non-Goals` when the work is material or ambiguous
- `High-Fidelity Example` when the work is material or ambiguous
- `What Good Looks Like` when the work is material or ambiguous
- `Proof Target` when the work is material or ambiguous
- `Plan`
- `Acceptance Criteria`
- `Working Notes`
- `Inspiration` when the ticket comes from an external source, article, talk, incident, or benchmark
- `Implementation Notes`
- `Evidence`
- `Review Packet`
- `Blockers`
- `Handoff`
- `Writeback`

Task-local notes stay in the ticket while work is active. Durable lessons move to `docs/` during `documenting`.
When a ticket is inspired by an external source, store the durable source URL in an `Inspiration` section in the body instead of relying on chat history.

Canonical policy references:

- [context-and-handoff-policy.md](/Users/kenjipcx/coding-harness/Codexter/docs/specs/context-and-handoff-policy.md)
- [runtime-surface spec](/Users/kenjipcx/coding-harness/Codexter/docs/specs/runtime-surface.md)
