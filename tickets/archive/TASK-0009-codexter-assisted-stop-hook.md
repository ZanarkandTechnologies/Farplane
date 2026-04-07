---
ticket_id: TASK-0009
title: quarantine assisted stop-hook continuation outside v1
phase: planning
status: blocked
owner: unassigned
priority: low
depends_on:
  - TASK-0008
blocked_by: []
ready: false
approval_required: true
created_at: 2026-04-03T00:00:00Z
updated_at: 2026-04-03T06:30:00Z
next_action: keep this ticket out of review and building until the repo explicitly re-opens post-v1 autonomy work and approves a separate assisted-continuation scope
last_verification: none
linked_docs: []
---

# TASK-0009: quarantine assisted stop-hook continuation outside v1

## Summary
Preserve this idea only as deferred backlog. It is not part of the current ticket-metadata rollout because the repo-level v1 decision explicitly keeps assisted continuation outside the feature.

## Scope
- In: explicit quarantine status, re-entry conditions, and backlog-only documentation that keeps this work from contaminating the active board
- Out: `hooks.json`, stop hooks, continuation heuristics, install wiring, notifier changes, or any implementation work

## Plan

### Pitch
- `Req:` remove hook/autonomy work from the active metadata rollout without losing the record that the idea exists
- `Bet:` rewrite this as a blocked todo ticket with explicit re-entry conditions instead of leaving it as an active building feature
- `Win:` the active board becomes trustworthy again and the v1 anti-goals stop fighting the current rollout

### B -> A
- `Before:` `TASK-0009` appeared as active/building work even though the current repo decision keeps assisted continuation and autonomy work outside v1
- `After:` `TASK-0009` is a quarantined backlog ticket in `tickets/` with a clear blocker and no active implementation scope
- `Outcome:` metadata work can proceed without implying that hook/autonomy implementation is part of the same rollout

### Delta
- `Touch:` this ticket and `tickets/README.md`
- `Keep:` the idea as a traceable backlog item only
- `Change:` remove active-build status and replace it with explicit deferred/quarantined status
- `Delete/Avoid:` avoid preserving misleading build-state metadata, hook implementation notes, or feature-proof language in the active board

### Core Flow
```pseudo
take the ticket out of active execution state
reset it to the canonical backlog dialect
record the repo-level v1 blocker explicitly
require future re-scoping and explicit approval before any new implementation work
```

### Proof
- `P1:` the ticket no longer lives in `tickets/`
- `P2:` its frontmatter and body now say the same thing: this is deferred backlog, not active work
- `P3:` the board index mirrors the move without becoming authoritative
- `Risk:` future loops could silently re-activate this work without changing the repo-level v1 boundary first
- `Rollback:` none needed for v1; if this work becomes valid later, rewrite the ticket from this parked state instead of restoring the old building record

### Plan Review
- `Refs:` `AGENTS.md`, `tickets/README.md`, `tickets/templates/ticket.md`, `tickets/TASK-0002-codexter-ticket-metadata-foundation.md`, `tickets/TASK-0008-codexter-autonomy-modes.md`
- `Scope:` pass; ticket-coherence cleanup only
- `Proof:` pass; success is visible in the lane move plus the rewritten metadata/body
- `Guardrails:` pass; no code or runtime work is added here
- `Fixes:` removed a direct contradiction with the repo-level v1 boundary and the active metadata rollout

### Delegation
- `Need:` `Not needed`
- `Why:` this is a local board-cleanup rewrite only
- `Artifact:` none

### Ask
- `Ready: no`
- `Next:` leave this ticket parked unless the repo explicitly changes the v1 boundary and wants a new post-v1 scope

### Ticket Move
- `Now:` `tickets/`
- `On approval:` remain parked until a future non-v1 decision exists
- `Follow-ups:` if revived later, rewrite this as a fresh implementation ticket instead of restoring the old build notes
- `Blocked in building?:` `yes`

## Acceptance Criteria
- [ ] AC-1: the repo explicitly changes the v1 boundary to permit assisted continuation or autonomy work
- [ ] AC-2: this work is rewritten as a separate post-v1 implementation slice instead of being reactivated implicitly
- [ ] AC-3: explicit approval is granted before the ticket re-enters `tickets/`

## Working Notes
- Earlier hook-oriented notes were intentionally removed because they made the active board less trustworthy.
- Keeping this in `tickets/` is the quarantine mechanism; it should not be treated as part of the current rollout.

## Implementation Notes
- Touched areas: this ticket plus the board index only
- Reused patterns: canonical ticket dialect, explicit blockers, and lane-as-truth board rules
- Guardrails: no hooks, no autonomy implementation, no hidden continuation behavior

## Evidence
- [x] QA / manual verification
- Verification details:
  - confirmed the ticket moved from `tickets/` to `tickets/`
  - confirmed the frontmatter/body now describe deferred scope only
  - confirmed `tickets/README.md` mirrors the move

## Blockers
- repo decision: assisted continuation and autonomy work are outside v1 of the ticket metadata feature

## Handoff
- Current state: quarantined backlog item only; not part of the active metadata rollout.
- Resume from: the repo-level v1 boundary and `TASK-0008` only if a future loop deliberately re-opens post-v1 autonomy work.

## Writeback
- Update this ticket as work progresses.
- Update `status` and `phase` in frontmatter when queue state changes.
