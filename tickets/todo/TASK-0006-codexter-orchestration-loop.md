---
ticket_id: TASK-0006
title: make codexter orchestration loop explicit
phase: planning
status: blocked
owner: unassigned
priority: medium
depends_on:
  - TASK-0002
  - TASK-0003
  - TASK-0004
blocked_by:
  - TASK-0003
  - TASK-0004
ready: false
approval_required: true
created_at: 2026-04-03T00:00:00Z
updated_at: 2026-04-03T06:30:00Z
next_action: keep this ticket in todo until TASK-0003 and TASK-0004 have approved contracts, then move it to review
last_verification: none
linked_docs: []
---

# TASK-0006: make codexter orchestration loop explicit

## Summary
Turn Codexter's planner-like, builder-like, and evaluator-like pieces into one explicit planner -> builder -> evaluator workflow that advances by rounds and writes visible artifacts.

## Scope
- In: orchestration contract, round transitions, run/ticket linkage, and builder/evaluator handoff rules
- Out: durable multi-worker runtime, hidden continuation, or a second board system

## Plan

### Pitch
- `Req:` stop treating Codexter as a bag of parts and make its main long-task loop explicit
- `Bet:` reuse tickets, existing evaluators, and visible artifacts instead of inventing a second planning system
- `Win:` clearer execution flow, better retries, and easier resume/review

### B -> A
- `Before:` planning, implementation, and evaluation exist but are loosely composed
- `After:` one first-class loop defines how a short prompt becomes a spec, contract, build round, and evaluator result
- `Outcome:` Codexter becomes more complete as a harness without cloning OMX runtime complexity

### Delta
- `Touch:` orchestration docs/skills/prompts/contracts and ticket/evaluator handoff notes
- `Keep:` the ticket board, current evaluator specialization, and visible file-based artifacts
- `Change:` add explicit round semantics and handoff rules once the upstream contracts are stable
- `Delete/Avoid:` avoid hidden continuation, runtime orchestration state, or bypassing the ticket board

### Core Flow
```pseudo
start with discovery or planning
derive one executable contract
build one slice
evaluate with the shared scorecard
advance or fail the round with one visible next action
```

### Proof
- `P1:` one sample prompt can be traced through the full loop using files alone
- `P2:` failed evaluation yields a concrete next-round artifact instead of vague follow-up
- `Risk:` duplicating ticket flow instead of complementing it
- `Rollback:` keep the loop implicit until the upstream contracts are stable enough to consume cleanly

### Plan Review
- `Refs:` `TASK-0002`, `TASK-0003`, `TASK-0004`
- `Scope:` orchestration contract only
- `Proof:` pending upstream contracts
- `Guardrails:` preserve ticket-first execution
- `Fixes:` canonicalized this backlog ticket and made the blockers explicit

### Delegation
- `Need:` `Not needed`
- `Why:` core harness architecture slice should stay centralized
- `Artifact:` none

### Ask
- `Ready: no`
- `Next:` keep this ticket parked until the scorecard and discovery tickets are ready to feed one loop

### Ticket Move
- `Now:` `tickets/todo/`
- `On approval:` move to `tickets/review/` once the upstream contracts are ready
- `Follow-ups:` `TASK-0007` should consume this loop once it exists
- `Blocked in building?:` `yes`

## Acceptance Criteria
- [ ] AC-1: one explicit planner -> builder -> evaluator workflow is documented and actionable
- [ ] AC-2: tickets, evaluator outputs, and docs have clear roles in the loop
- [ ] AC-3: round advance/fail conditions are explicit and use evaluator outcomes

## Working Notes
- This ticket stays parked in `tickets/todo/` until the upstream contract tickets are stable enough to consume.
- The orchestration loop must extend the ticket-first board rather than bypass it with a second runtime state system.
- `TASK-0005` is intentionally not a structural blocker for the first orchestration contract while passive telemetry stays outside v1.

## Implementation Notes
- Touched areas: harness workflow docs/contracts/prompts/skills
- Reused patterns: existing ticket board and evaluator roles
- Guardrails: no auto-continue by default

## Evidence
- [ ] Tests
- [ ] Typecheck
- [ ] Lint
- [ ] QA / manual verification

## Blockers
- `TASK-0003`
- `TASK-0004`
- `TASK-0005`

## Handoff
- Current state: canonicalized backlog ticket; still parked until the scorecard and discovery contracts settle.
- Resume from: this ticket plus `TASK-0003` and `TASK-0004` once they are ready to feed a single orchestration loop.

## Writeback
- Update this ticket as work progresses.
- Move the ticket and update `tickets/INDEX.md` when its board state changes.
