---
ticket_id: TASK-0025
title: capture turn-start intent for stop-hook alignment
phase: planning
status: review
owner: codex
priority: high
depends_on: []
blocked_by: []
ready: true
approval_required: false
created_at: 2026-04-08T00:00:00Z
updated_at: 2026-04-08T00:00:00Z
next_action: define how turn-start user input is captured, normalized, stored in runtime state, and compared against stop-hook completion decisions
last_verification: none
linked_docs: []
---

# TASK-0025: capture turn-start intent for stop-hook alignment

## Summary
Record the user’s current-turn intent at the start of a turn so the Stop hook can later compare worker output against what the user actually asked for in this turn, not stale prior-session context.

## Scope
- In:
  - turn-start capture surface
  - normalized intent summary
  - runtime state fields for user-turn intent
  - stop-hook comparison against current assistant output and active ticket
- Out:
  - full autonomous planning changes
  - queue-wide orchestration redesign

## Plan

### Pitch
- `Req:` stop stale-turn drift by grounding stop-hook review in the actual user input from the start of the turn
- `Bet:` a small turn-start capture artifact plus stop-hook mismatch checks is enough to catch most “answering the wrong thing” failures
- `Win:` the hook can block or reroute outputs that no longer match the user’s current request

### B -> A
- `Before:` stop-hook decisions rely on ticket state and the latest assistant output, but not a canonical capture of the user’s current-turn intent
- `After:` runtime state contains the latest user-turn intent summary and stop-hook compares assistant output against that state before continuing or routing
- `Outcome:` same-ticket continuation becomes less likely to drift from the current user ask

### Delta
- `Touch:` hook payload/state contract, runtime state schema, stop-hook comparison logic, and docs describing turn-start intent capture
- `Keep:` ticket-first execution model and small runtime state
- `Change:` add explicit user-turn intent capture and mismatch detection
- `Delete/Avoid:` avoid hidden transcript heuristics or large per-turn state archives

### Core Flow
```pseudo
capture user input at turn start
resolve active ticket and mode
store raw user text plus normalized intent summary in runtime state
when stop hook runs:
  read last user intent
  compare assistant output vs current-turn intent and ticket plan
  if mismatch:
    block or continue with corrective instruction
  else:
    continue normal review/orchestrator routing
```

### Proof
- `P1:` stop-hook can access the last user-turn intent without re-reading the whole transcript
- `P2:` a clearly stale or off-intent assistant response is blocked or corrected instead of silently continuing
- `Risk:` intent normalization could become fuzzy and over-opinionated
- `Rollback:` keep the captured raw user text and let the hook fall back to ticket-only routing if normalization proves unreliable

### Plan Review
- `Refs:` stop-hook routing, context-and-handoff policy, current run-state schema, and active impl/orchestrator surfaces
- `Scope:` bounded to turn-start intent capture and stop-hook alignment checks
- `Proof:` success is observable in runtime state plus stop-hook decisions on mismatched outputs
- `Guardrails:` no hidden autonomous planning; keep state lightweight
- `Fixes:` none

### Delegation
- `Need:` `Not needed`
- `Why:` runtime-state and stop-hook contract slice is small and centralized
- `Artifact:` none

### Ask
- `Ready: yes`
- `Next:` plan the exact state fields, hook integration point, and mismatch rules

### Ticket Move
- `Now:` `tickets/`
- `On approval:` move to active planning/building work
- `Follow-ups:` none yet
- `Blocked in building?:` `no`

## Acceptance Criteria
- [ ] AC-1: a turn-start capture surface records the latest user input for the active session/turn
- [ ] AC-2: runtime state stores both raw user input and a normalized intent summary
- [ ] AC-3: stop-hook compares assistant output against current-turn intent before deciding continue/orchestrate
- [ ] AC-4: clear mismatch cases result in block or corrective continuation instead of silent acceptance

## Working Notes
- This is intended to reduce “answering from stale session context” failures.
- Keep the state minimal and tied to the active session/turn, not a full transcript mirror.

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
- `reviewed_at:`
- `rubrics_used:`
- `overall_score:`
- `overall_verdict:`
- `rerun_required:`
- `blocking_findings:`
- `next_action:`

## Blockers
- none

## Handoff
- Current state: idea captured as a ticket; not yet planned in detail
- Resume from: this ticket, stop-hook state handling, and the run-state schema/docs

## Writeback
- Update this ticket as work progresses.
- If the ticket changes queue state, update `status` and `phase` in frontmatter. Do not move the file.
- When implementation and verification pass, move `phase` to `documenting`, write durable docs, then move the ticket into `tickets/archive/` or set `status: done` briefly if you intentionally keep a short-lived visible completion state first.
