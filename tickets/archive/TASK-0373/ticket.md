---
ticket_id: TASK-0373
title: Make ticket-thread associations the Pulse worker index
status: done
priority: high
created_at: 2026-07-15T05:12:18+08:00
updated_at: 2026-07-15T05:19:00+08:00
---

# TASK-0373: Make ticket-thread associations the Pulse worker index

## Summary

Remove active dependence on Pulse's split spawned/outcome runtime ledgers.
Tickets, progress files, and artifacts remain the task truth; the canonical
worker-thread lookup is `.farplane/state/ticket-thread-associations.jsonl`.

## Scope

- In:
  - Update Work Pulse board classification so worker capacity reads
    `.farplane/state/ticket-thread-associations.jsonl`.
  - Keep Reward/check-in projection in `list_pulse_board.py` unchanged.
  - Update interval autonomy-time metrics to derive autonomous worker runtime
    from ticket-thread associations.
  - Remove the temporary primitive-metric backfill from
    `.farplane/automation/spawned-threads.jsonl` and
    `.farplane/automation/action-outcomes.jsonl`.
  - Update focused tests and local docs/skill references that named those
    ledgers as active inputs.
- Out:
  - No deletion of ignored historical `.farplane/automation/*.jsonl` files.
  - No Reward/check-in mutation.
  - No worker launch, Pulse run, provider action, deploy, spend, commit, or
    push.
  - No broad graph regeneration unless a validator requires it.

## Delta

```text
before:
  Pulse board capacity used .farplane/automation/spawned-threads.jsonl, while
  primitive metrics had a temporary backfill from spawned/outcome ledgers.
after:
  Pulse board capacity, interval autonomy-time metrics, and primitive metrics
  use ticket-thread associations as the canonical worker index. Outcome facts
  belong in ticket/progress state and Pulse reports.
```

## Program

1. Replace board worker-index reads with ticket-thread associations.
2. Replace interval autonomy runtime reads with ticket-thread associations.
3. Remove primitive-metric Pulse spawned/outcome backfill code and tests.
4. Update docs/skill/catalog references away from the retired ledgers.
5. Run focused tests, py_compile, reference search, board smoke, and reviewer
   completion review.

## Map

- Board classifier: `skills/pulse-update/scripts/list_pulse_board.py`
- Board tests: `skills/pulse-update/scripts/test_list_pulse_board.py`
- Interval metrics: `skills/interval-update/scripts/metric_refresh.py`
- Interval tests: `bin/tests/test_interval_metric_refresh.py`
- Primitive metrics: `bin/core/farplane_primitive_metrics.py`
- Primitive tests: `bin/tests/test_farplane_primitive_metrics.py`
- Metric source card: `bin/core/farplane_project_snapshot.py`
- Pulse contract: `skills/pulse-update/SKILL.md`
- Runtime docs: `docs/farplane-framework/hooks-and-runtime.md`
- Lifecycle catalog: `skills/skill-maintenance/scripts/farplane_lifecycle_catalog.py`

## Done / Proof

- [x] Active code no longer reads `.farplane/automation/spawned-threads.jsonl`
      or `.farplane/automation/action-outcomes.jsonl`.
- [x] `list_pulse_board.py` reports
      `worker_index: .farplane/state/ticket-thread-associations.jsonl`.
- [x] Reward/check-in board classification still passes focused tests.
- [x] Interval autonomy-time metrics still pass focused tests using association
      rows.
- [x] Primitive metrics keep mine-input backfill behavior and no longer read
      Pulse spawned/outcome ledgers.
- [x] Docs/skill/catalog references no longer present those ledgers as active
      state.
- [x] Independent reviewer returns TAS-A or precise blocker.

Proof:

- Implementation evidence:
  `tickets/TASK-0373/artifacts/implementation-evidence.md`
- Independent review:
  `tickets/TASK-0373/artifacts/review/reviewer-verdict.md` returned TAS-A with
  no blocking findings.
- Focused tests:
  `python3 -m unittest skills.pulse-update.scripts.test_list_pulse_board bin.tests.test_interval_metric_refresh bin.tests.test_farplane_primitive_metrics`
  passed `43` tests.
- Static checks:
  `py_compile` and `git diff --check` passed for changed implementation files.
- Hard-gate search:
  `rg -n "spawned-threads|action-outcomes" bin skills docs farplane -g '!skills/skill-maintenance/graph/**' -g '!docs/skills/registry.jsonl'`
  returned no active matches.

## Review

rubric_families:

- code-quality
- integration-readiness
- evidence-quality

required_tas: TAS-A

hard_gates:

- no active source reference to `spawned-threads` or `action-outcomes` outside
  ignored generated graph/registry artifacts.
- focused tests pass.
- no external side effects, provider calls, deploy, spend, commit, or push.

## State

- `area:` framework_delivery
- `kpi:` ticket_intervention_turn_count
- `authority:` local reducer, board classifier, interval metrics, tests, and
  docs only
- `stop_condition:` stop after focused verification and independent review.

## Links

- Implementation evidence: `tickets/TASK-0373/artifacts/implementation-evidence.md`
