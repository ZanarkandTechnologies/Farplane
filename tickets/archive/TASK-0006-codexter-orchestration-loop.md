---
ticket_id: TASK-0006
title: define spec-first execution loop
phase: complete
status: done
owner: codex
priority: medium
depends_on:
  - TASK-0003
blocked_by:
  - TASK-0003
ready: true
approval_required: false
created_at: 2026-04-03T00:00:00Z
updated_at: 2026-04-07T00:00:00Z
next_action: archived; consume this loop from follow-on tickets such as TASK-0022 and TASK-0007 rather than keeping this contract ticket active
last_verification: spec-first-execution-loop.md and orchestrator-subagent-loop.md now define the canonical planner -> build -> qa -> review -> stop flow at the contract level
linked_docs:
  - docs/specs/spec-first-execution-loop.md
  - docs/specs/orchestrator-subagent-loop.md
  - tickets/TASK-0003-codexter-evaluator-scorecard.md
---

# TASK-0006: define spec-first execution loop

## Summary
Turn the current staged model into one explicit spec-first execution loop with clear boundaries between planning, build, QA, review, and Stop-hook gating.

## Scope
- In: orchestration contract, phase transitions, spec/work-package linkage, and handoff rules between `ralplan`, `ralph`, QA, review, and the Stop hook
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
- `Now:` `tickets/`
- `On approval:` move to `tickets/` once the upstream contracts are ready
- `Follow-ups:` `TASK-0007` should consume this loop once it exists
- `Blocked in building?:` `yes`

## Acceptance Criteria
- [x] AC-1: one explicit spec -> work package -> plan -> build -> qa -> review -> stop workflow is documented and actionable
- [x] AC-2: specs, work packages, progress surfaces, QA outputs, and review outputs have clear separate roles
- [x] AC-3: continuation, block, and completion conditions are explicit and use the review-gate contract from TASK-0003

## Working Notes
- This ticket stays parked in `tickets/` until the upstream contract tickets are stable enough to consume.
- The orchestration loop must extend the ticket-first board rather than bypass it with a second runtime state system.
- `TASK-0005` is intentionally not a structural blocker for the first orchestration contract while passive telemetry stays outside v1.

## Implementation Notes
- Touched areas: harness workflow docs/contracts/prompts/skills
- Reused patterns: existing ticket board and evaluator roles
- Guardrails: no auto-continue by default

## Evidence
- [ ] Tests
- [x] Typecheck
- [ ] Lint
- [x] QA / manual verification
- Validation details:
  - `python3 -m py_compile bin/check_ticket_metadata.py`
  - reviewed `docs/specs/spec-first-execution-loop.md`
  - reviewed `docs/specs/orchestrator-subagent-loop.md`
  - confirmed the contract now matches the active queue shape

## Blockers
- none

## Handoff
- Current state: the spec-first execution loop and orchestrator subagent pattern are now both written down as canonical docs.
- Resume from: this ticket, `docs/specs/spec-first-execution-loop.md`, `docs/specs/orchestrator-subagent-loop.md`, and the next implementation slice for the orchestrator behavior.

## Writeback
- Update this ticket as work progresses.
- Update `status` and `phase` in frontmatter when queue state changes.
