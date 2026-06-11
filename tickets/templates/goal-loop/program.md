---
kind: goal-program
ticket_id: TASK-XXXX
status: draft
created_at: 2026-06-12
---

# TASK-XXXX Goal Program

## Goal Mode

- `mode:` `active_goal` | `heartbeat` | `rollout` | `skill_improvement` |
  `feedback_loop`
- `trigger:` `native_goal` | `scheduled_heartbeat` |
  `human_feedback_received` | `manual_resume`
- `budget:` turn/time/spend/compute limits, or `none`

## Metric Provider

- `provider:` `mechanical` | `review` | `agent_qa` | `with-human` |
  `market` | `hybrid`
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

1. Read `ticket.md`, this `program.md`, and the tail of `progress.md`.
2. Choose the next action from the largest unresolved acceptance, evidence, or
   blocker gap.
3. Execute one bounded step.
4. Append a structured entry to `progress.md`.
5. Run or request drift check when required by `Drift Policy`.
6. Continue, stop complete, stop blocked, or wait for heartbeat/feedback.

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
