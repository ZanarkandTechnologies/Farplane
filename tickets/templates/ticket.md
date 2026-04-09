---
ticket_id: TASK-XXXX
title: short title
phase: planning
status: review
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

## User Story
- `Actor:`
- `Need:`
- `Outcome:`

## User Pain / JTBD
- `Current pain:`
- `Why now:`

## Non-Goals
- `Do not solve:`

## High-Fidelity Example
- `Example flow/artifact:`

## What Good Looks Like
- `Quality bar:`

## Proof Target
- `Reviewer-visible proof:`

## Plan

### Pitch
- `Req:`
- `Bet:`
- `Win:`

### Recommendation
- `Best:`
- `Why:`
- `Tradeoff accepted:`

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

### Options Appendix
- `Option 1:`
- `Pros:`
- `Cons:`
- `Why not chosen:`
- `Option 2:`
- `Pros:`
- `Cons:`
- `Why not chosen:`
- `Option 3:`
- `Pros:`
- `Cons:`
- `Why not chosen:`

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
- `approval_required: true`, any active `blocked_by` entry, or an unresolved dependency that prevents the next step all imply `ready: false`.
- `next_action` is the authoritative current step. Explain it here if useful, but do not create a second state field.
- `last_verification` is the authoritative verification summary. Put detailed commands and observations in `Evidence`.
- when the user did not provide a take on a material choice, capture three viable options plus the recommended path in the plan instead of leaving the tradeoff implicit
- `User Story`, `User Pain / JTBD`, `Non-Goals`, `High-Fidelity Example`, `What Good Looks Like`, and `Proof Target` are required for material feature work, workflow/tooling changes, ambiguous implementation work, and any ticket where the implementer would otherwise need to infer desired behavior
- those sections may be short or omitted for trivial, narrowly localized fixes where the file, symbol, or error already anchors the work concretely

## Inspiration
- Optional: source links and a short note on which external idea, article, talk, or incident motivated this ticket.
- Keep at least one durable source URL here when the ticket was created from outside inspiration.

## Implementation Notes
- Touched areas:
- Reused patterns:
- Guardrails:

## Evidence
- [ ] Tests
- [ ] Typecheck
- [ ] Lint
- [ ] QA / manual verification

## Review Packet
- Scores use the anchored `1.0`-to-`5.0` rubric scale.
- `reviewed_at:` `YYYY-MM-DD HH:mm ±ZZZZ`
- `rubrics_used:` `[]`
- `overall_score:`
- `overall_threshold:`
- `overall_verdict:` `pass|revise|block`
- `rerun_required:` `true|false`
- `evidence_quality:` `pass|fail`
- `integration_readiness:` `pass|fail`
- `traceability:` `pass|fail`
- `freshness:` `pass|fail`
- `hard_gate_failures:` `[]`
- `blocking_findings:` `[]`
- `next_action:`

## Blockers
- none

## Handoff
- Current state:
- Resume from:

## Writeback
- Update this ticket as work progresses.
- If the ticket changes queue state, update `status` and `phase` in frontmatter. Do not move the file.
- When implementation and verification pass, move `phase` to `documenting`, write durable docs, then move the ticket into `tickets/archive/` or set `status: done` briefly if you intentionally keep a short-lived visible completion state first.
