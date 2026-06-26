---
kind: goal-program
ticket_id: TASK-0231
status: draft
created_at: 2026-06-26T00:00:00+08:00
template_id: goal-loop-program
template_version: "0.1.1"
feature_refs:
  - FEAT-0029
  - FEAT-0032
  - FEAT-0046
---

# TASK-0231 Goal Program

## Goal Mode

- `mode:` active_goal
- `trigger:` native_goal after human approval
- `files:`
  - `tickets/TASK-0231/ticket.md`
  - `tickets/TASK-0231/program.md`
  - `tickets/TASK-0231/progress.md`
  - `docs/features/README.md`
  - `docs/features/registry.jsonl`
  - `docs/features/validate_features.py`
  - `docs/specs/doc-governance.md`
  - `docs/specs/filesystem-lifecycle.md`
  - `docs/farplane-framework/harness-maintenance.md`
  - `skills/documentation/SKILL.md`
  - `skills/interval-update/references/workflows/docs-consolidation.md`
  - `bin/core/farplane_adoption.py`
  - `bin/validators/sync_template_registry.py`
- `budget:` one strong local implementation window; reviewer lane required;
  no external spend, deploy, or customer contact
- `time_window:` uninterrupted native Goal window after approval
- `portfolio_boundary:` none

## Metric Provider

- `provider:` hybrid
- `feedback_preset:` none
- `signal:` mechanical validators/tests plus reviewer TAS verdict
- `direction:` pass/fail
- `minimum:` all Done / Proof commands pass and reviewer returns TAS-A or
  accepted revise items are resolved

## Proof Policy

- `proof_weight:` tests + review
- `delegated_lanes:` reviewer
- `drift_check_owner:` reviewer before completion
- `design_baseline:` none
- `final_evidence:` validator/test output summary, stale-ref search, deletion
  audit summary, generated registry summary, and reviewer receipt
- `self_certification:` prohibited for final completion claim

## Feedback Policy

- `human_feedback:` required only for approving this plan before execution
- `review_question:` Does the migration preserve stable feature refs, remove
  stale docs safely, and make specs the clear authored source of feature truth?
- `feedback_file:` none
- `notification:` none

## After Each Turn

1. Read `tickets/TASK-0231/ticket.md`, this program, and the tail of
   `tickets/TASK-0231/progress.md`.
2. Choose the next action from the largest unresolved source-of-truth,
   generator, consumer, deletion, validation, or review gap.
3. Execute one bounded implementation step.
4. Append a compact progress entry with files changed, evidence, drift verdict,
   next action, and blockers.
5. Before completion, request reviewer evidence or produce a review handoff
   artifact under `tickets/TASK-0231/artifacts/review/`.
6. Continue, stop complete, or stop blocked.

## After Completion

- `on_goal_window_complete:` append completion progress, run proof commands,
  attach reviewer receipt, and summarize final evidence.
- `on_milestone_complete:` none
- `manual_replan_allowed:` yes, only if feature metadata schema or deletion
  audit reveals a material fork.
- `automatic_replan:` none

## Drift Policy

- `drift_check:` subagent_required
- `checkpoints:` before deleting archive/futureideas; before completion
- `drift_reviewer:` reviewer
- `block_on_drift:` yes

## Heartbeat Policy

- `cadence:` none
- `heartbeat_prompt:` none
- `no_op_policy:` not applicable
- `wake_condition:` manual approval/resume
- `heartbeat_action:` no_op
- `selected_file_policy:` one approved Goal Packet

## Batch / Board Policy

- `target_set:` none
- `board_source:` none
- `proceedable_filter:` not applicable
- `proof_rows:` one proof bundle for TASK-0231
- `split_when:` split only if migration uncovers an unsupported runtime or
  public-consumer compatibility blocker
- `no_op_policy:` block with missing input

## Stop Conditions

- `complete_when:` Done / Proof passes, stale refs are cleared, archive/futureideas
  deletion audit is recorded, and reviewer accepts the migration.
- `blocked_when:` stable feature ID preservation conflicts with generated
  schema, archive deletion would remove still-current truth without an owner,
  or a consumer cannot be migrated safely inside this ticket.
- `pause_when:` human approval is needed for a plan/schema change beyond this
  ticket.
- `escalate_when:` deletion scope expands beyond `docs/archive/**` and
  `docs/futureideas/**`, or ticket archives/source registries/proof artifacts
  become implicated.

## Rollout Policy

- `target_set:` current active Farplane docs and registry consumers
- `sample_proof:` first generated registry output compared against old
  feature rows before deleting the hand-authored source assumption
- `batch_size:` all current feature rows in one migration
- `promotion_rule:` generated registry validates and consumer tests pass
- `rollback_or_hold_rule:` keep generated registry compatibility output and
  stop before deletion if current truth cannot be promoted safely
