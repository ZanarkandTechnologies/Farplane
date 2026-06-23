---
kind: goal-program
ticket_id: TASK-0212
status: active
created_at: 2026-06-23T21:49:00+0800
template_id: goal-loop-program
template_version: "0.1.1"
feature_refs:
  - FEAT-0029
  - FEAT-0032
  - FEAT-0046
---

# TASK-0212 Goal Program

## Goal Mode

- `mode:` active_goal
- `trigger:` native_goal
- `files:`
  - `tickets/TASK-0212/ticket.md`
  - `tickets/TASK-0212/program.md`
  - `tickets/TASK-0212/progress.md`
  - `docs/templates/registry.jsonl`
  - `rules/template-registry.toml`
  - `skills/skill-creator/references/SKILL_TEMPLATE.md`
  - `skills/skill-maintenance/scripts/generate_template_intelligence.py`
  - `skills/skill-maintenance/scripts/check_skills.py`
  - `bin/validators/sync_template_registry.py`
  - `bin/validators/check_farplane_project_files.py`
  - `farplane/manifest.json`
  - `../Farplane-UI/farplane/manifest.json`
- `budget:` local implementation window; no deploy, spend, push, or account changes
- `time_window:` current uninterrupted native Goal window
- `portfolio_boundary:` none

## Metric Provider

- `provider:` mechanical
- `feedback_preset:` none
- `signal:` validators, unit tests, and generated rollout artifact inspection
- `direction:` pass/fail
- `minimum:` all required checks pass or unrelated pre-existing failures are isolated with evidence

## Proof Policy

- `proof_weight:` tests + review
- `delegated_lanes:` reviewer if available before final completion; otherwise record review gap
- `drift_check_owner:` inline
- `design_baseline:` none
- `final_evidence:` command summary plus generated rollout artifact counts
- `self_certification:` allowed for mechanical implementation checks; review gate required for final readiness when available

## Feedback Policy

- `human_feedback:` none
- `review_question:` Does the rollout tracker reuse existing template systems without adding unnecessary layers, and does it make template blast radius visible?
- `feedback_file:` none
- `notification:` none

## After Each Turn

1. Read the listed files and latest `progress.md` entry.
2. Choose the next unresolved gap from the ticket `Done / Proof`.
3. Execute one bounded implementation or verification step.
4. Append a compact entry to `progress.md`.
5. Drift-check against the ticket: one field, reusable existing systems, skills/projects scope.
6. Continue until checks pass or a conflict/blocker is concrete.

## After Completion

- `on_goal_window_complete:` update ticket state, append completion entry, and summarize rollout counts and checks.
- `on_milestone_complete:` complete this ticket or identify the specific follow-up ticket.
- `manual_replan_allowed:` yes
- `automatic_replan:` none

## Drift Policy

- `drift_check:` inline
- `checkpoints:` before broad metadata migration, before final validation, before completion
- `drift_reviewer:` none
- `block_on_drift:` yes

## Heartbeat Policy

- `cadence:` none
- `heartbeat_prompt:` none
- `no_op_policy:` none
- `wake_condition:` manual resume only
- `heartbeat_action:` none
- `selected_file_policy:` none

## Batch / Board Policy

- `target_set:` skills with existing template version metadata; Farplane and Farplane-UI project manifests
- `board_source:` none
- `proceedable_filter:` existing fields only; avoid unrelated archive/history churn
- `proof_rows:` one implementation proof summary plus generated rollout artifact
- `split_when:` sibling project edits conflict with user work or validators expose unrelated failures
- `no_op_policy:` none

## Stop Conditions

- `complete_when:` all done/proof bullets are satisfied and command evidence is logged.
- `blocked_when:` unrelated dirty worktree conflict prevents scoped edits or required validator cannot be made to distinguish related from unrelated failures.
- `pause_when:` none planned.
- `escalate_when:` project-level field semantics would require a new schema registry or broad all-doc metadata rollout.

## Rollout Policy

- `target_set:` skills/projects listed above
- `sample_proof:` generated template intelligence artifact
- `batch_size:` all current applicable consumers
- `promotion_rule:` current consumers declare `template_uses`; legacy aliases are read-only compatibility
- `rollback_or_hold_rule:` stop if generated counts become misleading or overwrite unrelated user edits
