---
ticket_id: TASK-0005
title: add codexter passive runtime telemetry
phase: planning
status: blocked
owner: unassigned
priority: medium
depends_on:
  - TASK-0002
blocked_by: []
ready: false
approval_required: true
created_at: 2026-04-03T00:00:00Z
updated_at: 2026-04-03T06:00:00Z
next_action: keep this ticket in todo until a separate post-v1 ticket defines an explicit active-ticket selector for hooks and runtime metadata writes
last_verification: none
linked_docs: []
---

# TASK-0005: add codexter passive runtime telemetry

## Summary
Keep passive runtime telemetry out of the active rollout until the repo has an explicit, trustworthy active-ticket selector for hooks. This remains a downstream idea, not a v1 metadata feature.

## Scope
- In: explicit quarantine status, the missing-selector blocker, and re-entry conditions for any future passive telemetry slice
- Out: runtime bookkeeping, notify-driven writes, stop hooks, assisted continuation, auto-nudges, fallback watchers, tmux injection, autonomy modes, evaluator scoring, or any claim that this work is part of `TASK-0002`

## Plan

### Pitch
- `Req:` stop pretending passive telemetry is ready before the metadata system knows how a hook identifies the current active ticket
- `Bet:` park this in backlog until a future post-v1 slice defines and validates an explicit active-ticket selector
- `Win:` the current metadata system stays trustworthy instead of guessing at runtime truth

### B -> A
- `Before:` this ticket still sits in active review even though no canonical active-ticket selector exists for runtime hooks
- `After:` this ticket is parked in backlog with the missing-selector blocker made explicit
- `Outcome:` the v1 metadata contract can stand on its own without promising runtime behavior it cannot yet support safely

### Delta
- `Touch:` this ticket plus board/docs surfaces that explain the missing-selector boundary
- `Keep:` the idea as a downstream runtime follow-up only
- `Change:` move the work out of the active review lane and encode the blocker directly
- `Delete/Avoid:` avoid runtime implementation work or any implication that hooks may mutate ticket metadata safely in v1

### Core Flow
```pseudo
record that no canonical active-ticket selector exists yet
move the ticket out of active review
state the blocker explicitly in frontmatter and body
require a later post-v1 slice to define the selector before runtime writes are reconsidered
```

### Proof
- `P1:` this ticket no longer lives in `tickets/review/`
- `P2:` its frontmatter and body both say the same thing: passive telemetry is downstream and blocked on a missing active-ticket selector
- `P3:` the metadata contract docs explicitly state that v1 has no canonical hook/runtime selector
- `Risk:` future loops may try to revive telemetry by guessing the active ticket instead of defining selector rules first
- `Rollback:` none needed for v1; if revived later, rewrite this ticket from the parked state

### Plan Review
- `Refs:` `AGENTS.md`, `tickets/README.md`, `tickets/templates/ticket.md`, `tickets/done/TASK-0002-codexter-ticket-metadata-foundation.md`
- `Scope:` pass; board/doc coherence cleanup only
- `Proof:` pass; success is observable through the lane move and the explicit blocker
- `Guardrails:` pass; preserves ticket-first execution and avoids unsafe runtime guesses
- `Fixes:` removed the implication that telemetry is ready before selector design exists

### Delegation
- `Need:` `Not needed`
- `Why:` local board/doc coherence cleanup only
- `Artifact:` none

### Ticket Move
- `Now:` `tickets/todo/`
- `On approval:` remain parked until a future post-v1 slice defines an explicit active-ticket selector
- `Follow-ups:` if revived later, rewrite this as a fresh telemetry ticket instead of reusing active-review assumptions
- `Blocked in building?:` `yes`

### Ask
- `Ready: no`
- `Next:` leave this parked unless a future non-v1 decision explicitly defines how hooks identify the active ticket

## Acceptance Criteria
- [ ] AC-1: a future post-v1 decision explicitly defines a canonical active-ticket selector for runtime hooks
- [ ] AC-2: this ticket is rewritten as a fresh implementation slice instead of being implicitly reactivated
- [ ] AC-3: explicit approval is granted before the ticket re-enters `tickets/review/`

## Working Notes
- This ticket is intentionally parked because ticket metadata is now stronger than runtime hook selection logic. Runtime writes should not guess which active ticket they own.

## Implementation Notes
- Touched areas: this ticket plus the metadata-contract docs that now state the missing-selector boundary
- Reused patterns: canonical ticket dialect and explicit blocker semantics
- Guardrails: no runtime writes, no hidden control-plane behavior, no new selector guesses

## Evidence
- [ ] Tests
- [ ] Typecheck
- [ ] Lint
- [ ] QA / manual verification

## Blockers
- no canonical active-ticket selector exists for runtime hooks in v1

## Handoff
- Current state: parked backlog item only; not part of the active metadata rollout.
- Resume from: the v1 metadata contract and a future explicit selector design if the repo later re-opens passive telemetry.

## Writeback
- Update this ticket as work progresses.
- Move the ticket and update `tickets/INDEX.md` when its board state changes.
