---
kind: goal-program
ticket_id: TASK-0253
status: active
created_at: 2026-07-01T00:00:00Z
template_id: goal-loop-program
template_version: "0.1.1"
feature_refs:
  - FEAT-0029
  - FEAT-0032
---

# TASK-0253 Goal Program

## Goal Mode

- `mode:` active_goal
- `trigger:` native_goal
- `files:`
  - `tickets/TASK-0253/ticket.md`
  - `tickets/TASK-0253/program.md`
  - `tickets/TASK-0253/progress.md`
  - `tickets/TASK-0253/artifacts/native-goal-prompt.md`
  - `farplane/goals.md`
  - `farplane/bindings.md`
  - `farplane/ops-memory.md`
  - `bin/core/farplane_metrics.py`
  - `bin/tests/test_farplane_metrics.py`
  - `docs/farplane-framework/project-files.md`
  - `docs/farplane-framework/pulse-and-interval-loop.md`
  - `skills/interval-update/references/interval-update.md`
  - `skills/x-account/references/metrics-snapshot.md`
  - `skills/instagram-account/references/metrics-snapshot.md`
- `compiled_from_ticket_updated_at:` 2026-07-01T00:00:00Z
- `generated_prompt:` tickets/TASK-0253/artifacts/native-goal-prompt.md
- `approval:` approved
- `budget:` one focused implementation window; local shared checkout; no spend;
  no deploy; no secret echo; use reviewer only if final data-contract proof is
  judgment-heavy or uncertain.
- `time_window:` current native Goal turn
- `portfolio_boundary:` TASK-0253 only

## Metric Provider

- `provider:` mechanical
- `feedback_preset:` none
- `signal:` focused unit tests, `farplane metrics snapshot`, skill/docs checks,
  and generated UI snapshot inspection
- `direction:` pass/fail
- `minimum:` all listed checks pass or ticket records blocker/residual risk

## Proof Policy

- `proof_weight:` tests
- `derived_from:` ticket.md QA Strategy
- `delegated_lanes:` reviewer when data-contract readability or completion
  claim needs independent judgment; otherwise none
- `drift_check_owner:` inline
- `design_baseline:` none
- `final_evidence:` command output summary, changed file list, generated
  `.farplane/metrics/ui/latest.json`, and any residual-risk note
- `final_checkpoint:` before completion, run focused tests/checks, update
  ticket/progress with evidence, and record residual risk
- `self_certification:` allowed for mechanical checks only

## Feedback Policy

- `human_feedback:` none
- `review_question:` Does the implementation preserve the lean data contract
  without reintroducing duplicate KPI registry bloat?
- `feedback_file:` none
- `notification:` none

## After Each Turn

1. Read ticket/program/progress and the current implementation files.
2. Execute the largest unresolved acceptance gap.
3. Append a compact progress entry before final response.
4. Run checks before claiming completion.
5. Stop complete only when the ticket Done and QA Strategy are satisfied; stop
   blocked if compatibility or parsing risk remains unresolved.

## Stop Conditions

- `complete_when:`
  - goals/bindings standards use the lean model or docs/templates clearly own
    the lean model.
  - metric generator accepts compact `metrics.<kpi>.value` snapshots and
    derives daily diffs while preserving current snapshot compatibility.
  - interval/update guidance points agents at goals + ops memory + provider
    skills without deterministic ops-memory parsing.
  - focused tests and snapshot smoke pass.
- `blocked_when:`
  - current data cannot be migrated without losing existing KPI history.
  - repo checks reveal broader template/registry consequences outside this
    ticket's scope.
- `pause_when:` none
- `escalate_when:` implementation would require a new project/distribution
  surface, secret handling change, deploy, or hidden scheduler.
