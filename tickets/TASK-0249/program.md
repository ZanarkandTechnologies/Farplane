---
kind: goal-program
ticket_id: TASK-0249
status: complete
created_at: 2026-06-30T05:22:00Z
template_id: goal-loop-program
template_version: "0.1.1"
feature_refs:
  - FEAT-0029
---

# TASK-0249 Goal Program

## Goal Mode

- `mode:` active_goal
- `trigger:` native_goal
- `files:`
  - `tickets/TASK-0249/ticket.md`
  - `tickets/TASK-0249/program.md`
  - `tickets/TASK-0249/progress.md`
  - `tickets/TASK-0248/artifacts/kpi-snapshot-decision.md`
  - `tickets/TASK-0248/artifacts/metric-source-card.md`
  - `farplane/goals.md`
  - `farplane/bindings.md`
  - `bin/farplane.py`
  - `bin/core/farplane_metrics.py`
  - `bin/tests/test_farplane_metrics.py`
- `compiled_from_ticket_updated_at:` 2026-06-30T05:22:00Z
- `generated_prompt:` inline in progress entry
- `approval:` approved by operator request to run
- `budget:` local-only implementation; no external APIs, no deploy, no spend
- `time_window:` current Codex turn

## Metric Provider

- `provider:` mechanical
- `feedback_preset:` none
- `signal:` generated `.farplane/metrics/ui/latest.json`, focused tests, and ticket metadata validation
- `direction:` pass/fail
- `minimum:` command and tests pass without fake unavailable values

## Proof Policy

- `proof_weight:` tests
- `derived_from:` ticket.md QA Strategy
- `delegated_lanes:` none
- `drift_check_owner:` inline
- `final_evidence:` command outputs and `.farplane/metrics/ui/latest.json`
- `final_checkpoint:` update ticket/progress with proof links before completion
- `self_certification:` allowed for focused mechanical checks only

## Drift Policy

- `drift_check:` inline
- `checkpoints:` before implementation, before completion
- `block_on_drift:` yes

## Stop Conditions

- `complete_when:` tracked KPI config exists, generator writes latest UI JSON, tests pass, and progress records evidence
- `blocked_when:` local files are insufficient to derive a truthful first snapshot or tests reveal incorrect chart semantics
- `pause_when:` external social credentials or manual metrics are required for real X/Instagram values
- `escalate_when:` goals or product boundary changes exceed the approved point/daily snapshot design
