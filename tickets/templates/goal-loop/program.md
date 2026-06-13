---
kind: goal-program
ticket_id: TASK-XXXX
status: draft
created_at: 2026-06-12
---

# TASK-XXXX Goal Program

## Goal Mode

- `mode:` `active_goal` | `heartbeat` | `rollout` | `skill_improvement` |
  `feedback_loop` | `batch_goal`
- `trigger:` `native_goal` | `scheduled_heartbeat` |
  `human_feedback_received` | `manual_resume`
- `files:` inline list of ticket/program/progress/spec/board/artifact files the
  generated Goal prompt must name under `Files:`
- `budget:` time/token/model/compute/subagent/review/QA/feedback/spend limits,
  or `none`
- `time_window:` uninterrupted native Goal window, heartbeat cadence, or `none`
- `portfolio_boundary:` optional; use only when a longer planning graph is
  needed beyond the listed files

## Metric Provider

- `provider:` `mechanical` | `review` | `agent_qa` | `human_feedback` |
  `market` | `hybrid`
- `feedback_preset:` `optimize-with-human` | `none`
- `signal:` command, eval, review verdict, feedback file, market result, or
  artifact-presence check
- `direction:` `higher` | `lower` | `pass/fail` | `accept/revise` | `none`
- `minimum:` pass threshold, TAS gate, human decision, or `none`

## Feedback Policy

- `human_feedback:` `none` | `optional` | `required`
- `review_question:`
- `feedback_file:` `tickets/TASK-XXXX/artifacts/feedback/feedback.json`
- `notification:` `telegram` | `local_path` | `none`

## After Each Turn

1. Read every file listed in `files`, including each relevant `progress.md`
   tail.
2. Choose the next action from the largest unresolved acceptance, evidence, or
   blocker gap.
3. Execute one bounded step.
4. Append a structured entry to every `progress.md` whose ticket state changed.
5. Run or request drift check when required by `Drift Policy`.
6. Continue, stop complete, stop blocked, or wait for heartbeat/feedback.

## After Completion

- `on_goal_window_complete:` append completion progress to changed files, run
  proof/review, then start/resume the next eligible file set or wait for
  heartbeat
- `on_frontier_complete:` run parent heartbeat or replan routine before
  expanding the next branch
- `manual_replan_allowed:` yes/no
- `automatic_replan:` none or cadence/checkpoint

## Drift Policy

- `drift_check:` `inline` | `subagent_required` | `checkpoint_only`
- `checkpoints:` turn start, turn end, before broad rollout, before completion
- `drift_reviewer:` `goal-drift-reviewer`
- `block_on_drift:` yes/no

## Heartbeat Policy

- `cadence:` none or interval
- `heartbeat_prompt:` path or inline summary
- `no_op_policy:` log no-op when no useful action exists
- `wake_condition:` time, feedback file, external event, or manual resume
- `heartbeat_action:` no_op | start_child_goal | resume_child_goal |
  request_feedback | replan
- `selected_file_policy:` output/resume one time/budget-bounded Goal prompt
  with an inline `Files:` list

## Batch / Board Policy

- `target_set:` none or list/path/query
- `board_source:` none or ticket index/board path
- `proceedable_filter:` ready, unblocked, unclaimed, dependencies satisfied,
  no human gate, required tools available
- `proof_rows:` one per ticket plus optional batch/integration row
- `split_when:` attribution unclear, conflicting write scope, separate human
  gate, unsupported compute, or missing tool
- `no_op_policy:` log no-op when no proceedable work exists

## Stop Conditions

- `complete_when:`
- `blocked_when:`
- `pause_when:`
- `escalate_when:`

## Rollout Policy

- `target_set:` none or list/path
- `sample_proof:` none or artifact
- `batch_size:`
- `promotion_rule:`
- `rollback_or_hold_rule:`
