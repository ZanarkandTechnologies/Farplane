---
ticket_id: TASK-0039
title: fix stop-hook smoke eval regressions
phase: complete
status: done
owner: codex
priority: high
depends_on: []
blocked_by: []
ready: true
approval_required: false
created_at: 2026-04-08T17:53:50Z
updated_at: 2026-04-08T18:03:03Z
next_action: archived after restoring the smoke-eval fixture contracts and the ticket `updated_at` field needed by stale review-packet timestamp gating
last_verification: `python3 -m unittest discover -s bin -p 'test_*.py'`, `python3 -m py_compile bin/stop_hook.py bin/test_stop_hook.py experiments/run_ralph_smoke_evals.py`, `git diff --check`, and `python3 experiments/run_ralph_smoke_evals.py` passed
linked_docs:
  - docs/specs/context-and-handoff-policy.md
  - docs/specs/spec-first-execution-loop.md
---

# TASK-0039: fix stop-hook smoke eval regressions

## Summary
Repair the current stop-hook smoke-eval regressions by isolating the `hook_plan_payload` fixture state and restoring stale review-packet timestamp checks.

## Scope
- In:
  - the `hook_plan_payload` fixture setup in `experiments/run_ralph_smoke_evals.py`
  - `load_ticket()` support for `updated_at` so stale review-packet timestamps can gate completion again
  - ticket/writeback for the smoke-eval repair
- Out:
  - stop-hook semantic changes
  - broader runtime or agent-surface redesign

## Plan

### Pitch
- `Req:` make the failing smoke eval reflect current intended stop-hook behavior instead of contaminated fixture state and a missing ticket timestamp field
- `Bet:` reseeding a clean planning `current-run.json` before `hook_plan_payload` plus restoring `updated_at` in `load_ticket()` is enough to clear the current regressions
- `Win:` the smoke suite passes without weakening the newer relevance-first stop-hook gate

### B -> A
- `Before:` `hook_plan_payload` can inherit stale `last_user_turn` state, and stale review-packet timestamp fixtures cannot trip the gate because `updated_at` is missing from normalized ticket data
- `After:` the planning smoke case uses a fresh fixture, and `review_packet_gate()` can compare `reviewed_at` against ticket `updated_at` again
- `Outcome:` the eval tests real stop-hook behavior instead of fixture leakage or loader omissions

### Delta
- `Touch:` `experiments/run_ralph_smoke_evals.py`, `bin/stop_hook.py`, and focused stop-hook unit coverage
- `Keep:` current stop-hook runtime behavior
- `Change:` make the `hook_plan_payload` scenario hermetic
- `Delete/Avoid:` runtime rollback or disabling intent-alignment checks

### Core Flow
```pseudo
run mismatch scenarios
reset current-run to a clean planning fixture
invoke hook_plan_payload against the planning fixture
assert the planning path advances into building
load tickets with frontmatter `updated_at`
assert stale review-packet timestamps force `repeat_ralph`
```

### Proof
- `P1:` `hook_plan_payload` no longer sees stale hard-mismatch state
- `P2:` stale `reviewed_at` packet fixtures force `repeat_ralph` again
- `P3:` `python3 experiments/run_ralph_smoke_evals.py` passes
- `Risk:` the smoke fix could hide a real stop-hook regression if the fixture reset is too broad
- `Rollback:` revert the fixture reseed and restore the prior case setup

### Plan Review
- `Refs:` `experiments/run_ralph_smoke_evals.py`, `bin/stop_hook.py`, `docs/specs/context-and-handoff-policy.md`
- `Scope:` smoke-eval fixture repair plus the missing ticket timestamp field needed by an existing review gate
- `Proof:` full smoke eval plus focused stop-hook unit suite
- `Guardrails:` preserve the current relevance-first gate semantics
- `Fixes:` keep the changes local to the failing smoke cases and the existing ticket loader contract

### Delegation
- `Need:` Not needed
- `Why:` single-file test harness repair
- `Artifact:` n/a

### Ask
- `Ready: yes`
- `Next:` implement the fixture reset and rerun verification

### Ticket Move
- `Now:` `status: building`, `phase: building`
- `On approval:` n/a
- `Follow-ups:` none expected
- `Blocked in building?:` no

## Acceptance Criteria
- [x] AC-1: `hook_plan_payload` is seeded with clean planning runtime state before it runs
- [x] AC-2: the smoke eval no longer fails from inherited hard-mismatch `last_user_turn` state
- [x] AC-3: stale review-packet timestamp fixtures force `repeat_ralph` again
- [x] AC-4: `python3 experiments/run_ralph_smoke_evals.py` passes

## Working Notes
- Direct manual replay showed that the planning payload no longer hard-mismatches under a clean planning `current-run.json`, but the current hook behavior advances the ticket into building rather than returning empty stdout.
- `review_packet_gate()` already expects ticket `updated_at`, but `load_ticket()` is not returning that field today.

## Implementation Notes
- Touched areas: smoke-eval fixture setup, ticket loader, focused stop-hook tests
- Reused patterns: existing `write_current_run_fixture(...)`
- Guardrails: do not change stop-hook semantics beyond restoring the missing `updated_at` field that an existing gate already depends on

## Evidence
- [x] Tests
- [x] Typecheck / syntax verification
- [x] Lint / diff hygiene
- [x] QA / manual verification

- Commands:
  - `python3 -m unittest discover -s bin -p 'test_*.py'`
  - `python3 -m py_compile bin/stop_hook.py bin/test_stop_hook.py experiments/run_ralph_smoke_evals.py`
  - `git diff --check`
  - `python3 experiments/run_ralph_smoke_evals.py`
- Manual verification:
  - directly replayed the planning payload under a clean planning `current-run.json` to confirm the original hard-mismatch failure was fixture leakage
  - confirmed the stale timestamp path only starts working once `load_ticket()` includes `updated_at`

## Review Packet
- `reviewed_at:` 2026-04-08 18:53 +0100
- `rubrics_used:` ["code-quality", "evidence-quality", "integration-readiness"]
- `overall_score:` 4.4
- `overall_threshold:` 4.0
- `overall_verdict:` pass
- `rerun_required:` false
- `evidence_quality:` pass
- `integration_readiness:` pass
- `traceability:` pass
- `freshness:` pass
- `hard_gate_failures:` []
- `blocking_findings:` []
- `next_action:` keep the smoke fixtures hermetic and preserve `updated_at` in normalized ticket objects whenever review-packet freshness depends on it

## Blockers
- none

## Handoff
- Current state: implemented and archived; the smoke eval now uses a clean planning fixture for `hook_plan_payload`, and stale timestamp gating works again
- Resume from: no follow-up expected unless another smoke case surfaces a separate fixture drift

## Writeback
- Update this ticket as work progresses.
- If the ticket changes queue state, update `status` and `phase` in frontmatter. Do not move the file.
- When implementation and verification pass, move `phase` to `documenting`, write durable docs, then move the ticket into `tickets/archive/` or set `status: done` briefly if you intentionally keep a short-lived visible completion state first.
