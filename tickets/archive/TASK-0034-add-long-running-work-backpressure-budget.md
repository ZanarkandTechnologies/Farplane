---
ticket_id: TASK-0034
title: add long-running work backpressure budget
phase: complete
status: done
owner: codex
priority: high
depends_on: []
blocked_by: []
ready: false
approval_required: false
created_at: 2026-04-08T03:20:00Z
updated_at: 2026-04-10T00:53:29Z
next_action: none; archived after stale-wait backpressure slice implementation and docs closeout
last_verification: `python3 -m py_compile bin/user_turn.py bin/stop_hook.py skills/impl/scripts/tmux_helper.py`; `python3 -m unittest bin/test_runtime_state.py`; `python3 -m unittest bin/test_stop_hook.py`; `python3 -m unittest bin/test_tmux_helper.py`; `python3 tickets/scripts/check_ticket_metadata.py`; `python3 bin/check_doc_parity.py`; `git diff --check`
linked_docs:
  - docs/prd.md
  - README.md
  - bin/AGENTS.md
  - skills/impl/AGENTS.md
  - skills/impl/README.md
  - docs/specs/harness-techniques.md
  - docs/specs/orchestrator-subagent-loop.md
  - docs/specs/context-and-handoff-policy.md
  - docs/specs/ralph-v2-direction.md
  - docs/specs/ralph-run-state.schema.json
  - docs/MEMORY.md
  - docs/HISTORY.md
  - docs/TROUBLES.md
  - tickets/TASK-0026-enforce-delegated-worker-contract.md
  - skills/impl/scripts/tmux_helper.py
  - bin/user_turn.py
  - bin/test_tmux_helper.py
  - bin/README.md
---

# TASK-0034: add long-running work backpressure budget

## Summary
Add a first live backpressure loop for long-running delegated work by surfacing stale waits in the existing runtime/status path and defining the required response when a worker has gone too long without a useful checkpoint.

## Scope
- In:
  - one initial soft threshold for "too long without a useful checkpoint"
  - additive runtime metadata for worker start/checkpoint timing
  - one operator-visible or orchestrator-visible status signal for over-budget waits
  - a documented required response: split work, add instrumentation, narrow scope, or continue with explicit justification
- Out:
  - hard-killing processes at a fixed timeout
  - background daemons or watchdog services
  - queue-wide scheduler redesign
  - optimizing arbitrary shell-command latency

## User Story
- `Actor:` orchestrator or operator running delegated builder/reviewer/QA/evidence-check work
- `Need:` know when a worker has been running too long without a meaningful checkpoint and what the next response should be
- `Outcome:` less dead waiting, faster replanning, and cleaner ticket-sized execution loops

## User Pain / JTBD
- `Current pain:` the harness can launch visible delegated lanes, but a long-running lane can still burn time silently because there is no explicit budget or stale-wait signal tied to the runtime contract
- `Why now:` TASK-0026 just made delegated lane identity and grounding explicit, so the next highest-leverage slice is to make stalled delegated work visible and actionable using the same runtime surface

## Non-Goals
- `Do not solve:` autonomous retry loops, process supervision, cloud dispatch, or a generalized job scheduler

## High-Fidelity Example
- `Example flow/artifact:` `$impl` launches a `builder` lane for `TASK-0034` at `12:00:00` and writes `worker_started_at` plus `last_checkpoint_at=12:00:00` with `checkpoint_summary="worker launched"`. At `12:01:20`, `tmux_helper status` reports `backpressure_state=over_budget`, `stale_for_secs=80`, and `recommended_action="split work or add instrumentation before waiting longer"` because no later checkpoint exists. The operator or orchestrator can then choose a visible next move instead of assuming the wait is fine.

## What Good Looks Like
- `Quality bar:` one status read makes it obvious that a delegated wait is stale, why it is stale, and what the allowed next responses are

## Proof Target
- `Reviewer-visible proof:` a dry-run or fixture shows a lane with stale checkpoint timing surfacing an over-budget backpressure state, and the docs describe the exact response contract without requiring the reader to infer policy from chat

## Plan

### Pitch
- `Req:` stop the harness from silently burning time on long-running delegated work when the right response is to replan instead of wait
- `Bet:` the smallest useful slice is a stale-wait signal in the existing runtime/status path, backed by additive checkpoint metadata and a clear response policy
- `Win:` we get real backpressure without adding hidden automation or a scheduler

### Recommendation
- `Best:` implement a soft stale-wait budget on the existing delegated-worker runtime contract: add `worker_started_at`, `last_checkpoint_at`, and `checkpoint_summary`, then teach `tmux_helper status` to emit `backpressure_state`, `stale_for_secs`, and a recommended response when the budget is exceeded
- `Why:` this reuses the surfaces that already exist after TASK-0026, gives immediate operator value, and keeps the first slice visible and advisory-first
- `Tradeoff accepted:` the first slice will not interrupt a worker automatically; it will surface and standardize the decision instead

### B -> A
- `Before:` the runtime contract knows who the delegated worker is and what artifact it owns, but it does not tell us whether the lane has been stale too long
- `After:` the same runtime/status surface can say not just who/what, but whether the wait is over budget and what to do next
- `Outcome:` delegated waiting becomes observable and policy-backed instead of subjective

### Delta
- `Touch:` `skills/impl/scripts/tmux_helper.py`, `bin/user_turn.py`, maybe `docs/specs/ralph-run-state.schema.json`, `bin/README.md`, and the canonical runtime policy docs
- `Keep:` session-first routing, lightweight runtime state, visible worker lanes, and human-visible follow-up decisions
- `Change:` add explicit wait/checkpoint metadata and a derived stale-wait signal
- `Delete/Avoid:` daemon watchdogs, invisible retries, or broad performance instrumentation

### Core Flow
```pseudo
launch delegated lane
persist worker_started_at, last_checkpoint_at, checkpoint_summary
status surface computes stale_for_secs from the latest checkpoint
if stale_for_secs > soft_budget_secs:
  emit backpressure_state=over_budget
  emit recommended_action from the allowed response set
operator or orchestrator chooses one visible next move:
  split work
  add instrumentation
  narrow scope
  continue with explicit justification
document the budget and response contract
```

### Proof
- `P1:` at least one operator-visible runtime surface reports an over-budget stale wait
- `P2:` the runtime contract includes checkpoint timing fields so the stale-wait judgment is inspectable
- `P3:` the docs define the allowed next responses explicitly instead of treating them as improvised judgment calls
- `Risk:` a single global threshold may be too blunt across planning, build, QA, and docs lanes
- `Rollback:` keep v1 to one default threshold plus advisory output; phase-specific budgets can stay a follow-up if needed

### Plan Review
- `Refs:` `docs/prd.md`, `docs/specs/orchestrator-subagent-loop.md`, `docs/specs/context-and-handoff-policy.md`, `docs/specs/ralph-v2-direction.md`, `docs/MEMORY.md`, `docs/TROUBLES.md`, `tickets/TASK-0034-add-long-running-work-backpressure-budget.md`, `tickets/TASK-0026-enforce-delegated-worker-contract.md`, `skills/impl/scripts/tmux_helper.py`, `bin/user_turn.py`, `bin/README.md`
- `Checks:` scope=pass; proof=pass; guardrails=pass; rollback=pass
- `Fixes:` narrowed the slice away from raw command latency, tied it to the new delegated-worker contract, and kept the first implementation to one visible stale-wait status path instead of hidden automation

### Options Appendix
- `Option 1:` docs-only policy with no runtime signal
- `Pros:` fastest to land; no code churn; zero risk of bad threshold math
- `Cons:` low user value; still leaves operators guessing whether a wait is stale; no leverage from the new delegated-worker fields
- `Why not chosen:` too weak for the actual failure mode
- `Option 2:` additive stale-wait signal in the existing runtime/status path
- `Pros:` strongest leverage per unit of code; reuses TASK-0026 fields; gives visible evidence without overbuilding; easy to extend later with real checkpoints
- `Cons:` first version is advisory, not autonomous; one default threshold may be coarse
- `Why not chosen:` recommended
- `Option 3:` autonomous watchdog or stop-hook-driven forced replanning
- `Pros:` strongest enforcement; could prevent very long stalls automatically
- `Cons:` higher risk; more hidden behavior; likely too much orchestration policy for one commit; harder to trust
- `Why not chosen:` premature for v1

### Delegation
- `Need:` Not needed
- `Why:` planning slice only
- `Artifact:` n/a

### Ask
- `Ready: yes`
- `Next:` approve the stale-wait status slice, then implement the additive checkpoint metadata plus over-budget status signal in one commit

### Ticket Move
- `Now:` `status: done`, `phase: complete`, ready for `tickets/archive/`
- `On approval:` already implemented
- `Follow-ups:` phase-specific budgets, explicit worker-emitted checkpoints, and automatic replan suggestions can stay follow-up work if the first slice proves useful
- `Blocked in building?:` no

## Acceptance Criteria
- [ ] AC-1: the runtime contract includes additive timing fields for delegated wait tracking, such as `worker_started_at`, `last_checkpoint_at`, and `checkpoint_summary`
- [ ] AC-2: `tmux_helper status` or the equivalent live status surface emits an explicit over-budget signal when a delegated wait exceeds the soft budget
- [ ] AC-3: the emitted status includes enough detail to act on: stale duration, current worker, current artifact, and recommended next action
- [ ] AC-4: the docs define the required response set for an over-budget wait: split work, add instrumentation, narrow scope, or continue with explicit justification
- [ ] AC-5: the first implementation proves the budget applies to delegated worker waits, not raw shell-command latency

## Working Notes
- User clarification on 2026-04-09: the important idea is not micro-benchmarking commands; it is treating overlong work loops as a sign that the work may need to be broken down differently.
- The first heuristic can start around one minute, but the real contract is "too long without a useful checkpoint", not "kill everything at exactly 60 seconds."
- Brainstorm result:
  - docs-only policy is too weak
  - status-surface backpressure is the best first bet
  - autonomous watchdog behavior is too risky for the first slice
- This fits the current harness pain better than pure command timing because the waste often shows up as waiting on subagents or long validation loops.

## Inspiration
- Source: Ryan Lopopolo, "Extreme Harness Engineering for the 1B token/day Dark Factory" on Latent Space. Video: https://www.youtube.com/watch?v=CeOXx-XTYek
- Transcript: https://www.latent.space/p/harness-eng
- Relevant takeaway: when a common loop stays slow or opaque for too long, that is itself a harness bug and should force a better execution shape instead of endless waiting.

## Implementation Notes
- Touched areas: `skills/impl/scripts/tmux_helper.py`, `bin/user_turn.py`, `bin/stop_hook.py`, `bin/test_tmux_helper.py`, `bin/test_runtime_state.py`, `docs/specs/ralph-run-state.schema.json`, `bin/README.md`, `docs/specs/context-and-handoff-policy.md`, `docs/HISTORY.md`, `docs/MEMORY.md`, `bin/AGENTS.md`, `skills/impl/AGENTS.md`, `skills/impl/README.md`
- Reused patterns: lightweight repo-local runtime surfaces, additive claim metadata, session-first routing, and canonical doc writeback
- Guardrails: keep the first slice narrow, visible, and advisory-first

## Evidence
- [x] Tests
- [x] Typecheck
- [ ] Lint
- [x] QA / manual verification

- `python3 -m py_compile bin/user_turn.py bin/stop_hook.py skills/impl/scripts/tmux_helper.py`
- `python3 -m unittest bin/test_runtime_state.py`
- `python3 -m unittest bin/test_stop_hook.py`
- `python3 -m unittest bin/test_tmux_helper.py`
- `python3 tickets/scripts/check_ticket_metadata.py`
- `python3 bin/check_doc_parity.py`
- `git diff --check`
- Manual verification: confirmed the implementation stays advisory-first, with stale-wait verdicts derived from explicit checkpoint timing instead of hidden watchdog behavior
- `Lint:` not run; this slice is Python/docs/runtime-config only and no additional lint target was needed for acceptance

## Review Packet
- `reviewed_at:` `2026-04-10 01:53 +0100`
- `rubrics_used:` `["code-quality","integration-readiness","evidence-quality"]`
- `overall_score:` `4.7`
- `overall_threshold:` `4.0`
- `overall_verdict:` `pass`
- `rerun_required:` `false`
- `evidence_quality:` `pass`
- `integration_readiness:` `pass`
- `traceability:` `pass`
- `freshness:` `pass`
- `hard_gate_failures:` `[]`
- `blocking_findings:` `[]`
- `next_action:` `archive the completed ticket`

## Blockers
- none

## Handoff
- Current state: implementation, tests, and docs writeback are complete. Runtime state now carries advisory stale-wait metadata via `worker_started_at`, `last_checkpoint_at`, and `checkpoint_summary`, and the tmux-helper status path derives `within_budget` / `over_budget` state plus recommended next action.
- Resume from: no resume required unless we open a follow-up for explicit worker-emitted checkpoints or phase-specific budgets.

## Writeback
- Update this ticket as work progresses.
- If the ticket changes queue state, update `status` and `phase` in frontmatter. Do not move the file.
- When implementation and verification pass, move `phase` to `documenting`, write durable docs, then move the ticket into `tickets/archive/` or set `status: done` briefly if you intentionally keep a short-lived visible completion state first.
