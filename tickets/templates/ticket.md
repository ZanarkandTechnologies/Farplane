---
ticket_id: TASK-XXXX
title: short title
phase: planning
status: active
owner: unassigned
priority: medium
depends_on: []
blocked_by: []
ready: false
approval_required: true
created_at: 2026-04-03T00:00:00Z
updated_at: 2026-04-03T00:00:00Z
next_action: define the one current step and keep it in this field
last_verification: none
linked_docs: []
---

# TASK-XXXX: title

## Summary
Short description of the next smallest executable slice.

## Scope
- In:
- Out:

## Plan

### Pitch
- `Req:`
- `Bet:`
- `Win:`

### B -> A
- `Before:`
- `After:`
- `Outcome:`

### Delta
- `Touch:`
- `Keep:`
- `Change:`
- `Delete/Avoid:`

### Core Flow
```pseudo
inspect current state
apply smallest safe delta
validate changed surfaces
update docs/evidence
```

### Proof
- `P1:`
- `P2:`
- `Risk:`
- `Rollback:`

### Plan Review
- `Refs:`
- `Scope:`
- `Proof:`
- `Guardrails:`
- `Fixes:`

### Delegation
- `Need:`
- `Why:`
- `Artifact:`

### Ask
- `Ready: yes|no`
- `Next:`

### Ticket Move
- `Now:`
- `On approval:`
- `Follow-ups:`
- `Blocked in building?:`

## Acceptance Criteria
- [ ] AC-1
- [ ] AC-2

## Working Notes
- Active task-local memory only. Durable cross-task lessons move to docs on completion.
- Board lane comes from the ticket's folder path, not frontmatter.
- `approval_required: true`, any active `blocked_by` entry, or an unresolved dependency that prevents the next step all imply `ready: false`.
- `next_action` is the authoritative current step. Explain it here if useful, but do not create a second state field.
- `last_verification` is the authoritative verification summary. Put detailed commands and observations in `Evidence`.

## Implementation Notes
- Touched areas:
- Reused patterns:
- Guardrails:

## Evidence
- [ ] Tests
- [ ] Typecheck
- [ ] Lint
- [ ] QA / manual verification

## Blockers
- none

## Handoff
- Current state:
- Resume from:

## Writeback
- Update this ticket as work progresses.
- If the ticket changes board state, move the file and update `tickets/INDEX.md` as a human summary.
- When implementation and verification pass, move `phase` to `documenting`, write durable docs, then archive/delete the ticket or move it out of active lanes.
