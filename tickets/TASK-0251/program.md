---
kind: goal-program
ticket_id: TASK-0251
status: active
created_at: 2026-06-30T08:30:00Z
template_id: goal-loop-program
template_version: "0.1.1"
feature_refs:
  - FEAT-0029
  - FEAT-0065
---

# TASK-0251 Goal Program

## Goal Mode

- `mode:` `active_goal`
- `trigger:` `native_goal`
- `files:`
  - `tickets/TASK-0251/ticket.md`
  - `tickets/TASK-0251/program.md`
  - `tickets/TASK-0251/progress.md`
  - `tickets/TASK-0251/artifacts/review/impl-plan-review.md`
  - `farplane/goals.md`
  - `farplane/products.md`
  - `farplane/harness.md`
  - `docs/farplane-framework/pulse-and-interval-loop.md`
  - `skills/pulse-update/SKILL.md`
  - `skills/interval-update/SKILL.md`
  - `skills/interval-update/references/workflows/priority-planning.md`
  - `skills/interval-update/templates/interval-report.md`
  - `.farplane/automation/heartbeat-policy.json`
- `compiled_from_ticket_updated_at:` `2026-06-30T08:30:00Z`
- `generated_prompt:` `tickets/TASK-0251/artifacts/native-goal-prompt.md`
- `approval:` `approved`
- `budget:` `local-only docs/skill contract implementation; no spend, deploy, publish, external account mutation, automation cadence change, or cap change`
- `time_window:` `single native Goal execution window`

## Metric Provider

- `provider:` `hybrid`
- `feedback_preset:` `none`
- `signal:` required files changed, validators pass, focused grep/readback proves `ops-memory` is discoverable, and reviewer completion verdict is TAS-A or precise needs-revision
- `direction:` `pass/fail`
- `minimum:` all Done checks from `ticket.md` plus final completion review

## Proof Policy

- `proof_weight:` `tests`
- `derived_from:` `ticket.md QA Strategy`
- `delegated_lanes:` `reviewer` for final completion review
- `drift_check_owner:` `inline` during edits; `reviewer` before completion
- `design_baseline:` `none`
- `final_evidence:` `farplane/ops-memory.md`, updated skill/doc diffs, validator outputs, focused grep/readback, and final reviewer receipt under `tickets/TASK-0251/artifacts/review/`
- `final_checkpoint:` before `stop_complete`, run required validators, write progress/ticket links, request reviewer completion review, and block or revise unless the review is TAS-A/pass or gives a precise repair path
- `self_certification:` prohibited for final completion claim

## Feedback Policy

- `human_feedback:` `none`
- `review_question:` `Does TASK-0251 implement ops-memory without creating a roadmap/project registry, mutating caps, or weakening Pulse/Interval boundaries?`
- `feedback_file:` `none`
- `notification:` `none`

## After Each Turn

1. Read `ticket.md`, this `program.md`, and the `progress.md` tail.
2. Execute the largest unresolved Done/QA gap.
3. Append compact progress when files or proof state change.
4. Keep caps in `.farplane/automation/heartbeat-policy.json`; do not mutate cadence or live automation settings.
5. Run validators before completion and request reviewer completion review.

## After Completion

- `on_goal_window_complete:` append completion progress, update `ticket.md`
  state and links, run validators, record reviewer completion receipt, and
  report residual risk.
- `on_milestone_complete:` not applicable
- `manual_replan_allowed:` yes
- `automatic_replan:` none

## Drift Policy

- `drift_check:` `checkpoint_only`
- `checkpoints:` turn start, before completion
- `drift_reviewer:` `reviewer`
- `block_on_drift:` yes

## Heartbeat Policy

- `cadence:` none
- `heartbeat_prompt:` none
- `no_op_policy:` not applicable
- `wake_condition:` none
- `heartbeat_action:` none
- `selected_file_policy:` native Goal prompt lists the file set above

## Batch / Board Policy

- `target_set:` none
- `board_source:` none
- `proceedable_filter:` not applicable
- `proof_rows:` one row for `TASK-0251`
- `split_when:` not applicable
- `no_op_policy:` not applicable

## Stop Conditions

- `complete_when:`
  - `farplane/ops-memory.md` exists and stays compact
  - Pulse and Interval skill contracts read/maintain ops-memory
  - framework docs explain stable truth vs active memory vs tickets vs receipts
  - validators pass
  - reviewer completion review passes or records only nonblocking residual risk
- `blocked_when:`
  - the ops-memory owner boundary contradicts existing project docs
  - validators fail and cannot be repaired in scope
  - reviewer returns TAS-B/TAS-C without a small repair path
- `pause_when:` no pause expected
- `escalate_when:` any change would require live automation cadence/cap mutation, external side effects, or a broader project-management schema

## Rollout Policy

- `target_set:` none
- `sample_proof:` none
- `batch_size:` none
- `promotion_rule:` none
- `rollback_or_hold_rule:` remove ops-memory references and park `farplane/ops-memory.md` if the first live Pulse beat proves it increases confusion
