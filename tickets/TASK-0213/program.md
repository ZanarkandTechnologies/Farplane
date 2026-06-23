---
kind: goal-program
ticket_id: TASK-0213
status: active
created_at: 2026-06-23T23:22:07+0800
template_id: goal-loop-program
template_version: "0.1.1"
feature_refs:
  - FEAT-0029
  - FEAT-0032
  - FEAT-0046
---

# TASK-0213 Goal Program

## Goal Mode

- `mode:` active_goal
- `trigger:` native_goal
- `files:`
  - `tickets/TASK-0213/ticket.md`
  - `tickets/TASK-0213/program.md`
  - `tickets/TASK-0213/progress.md`
  - `docs/farplane-framework/README.md`
  - `docs/farplane-framework/deep-init-critical-path.md`
  - `docs/farplane-framework/project-files.md`
  - `docs/specs/filesystem-lifecycle.md`
  - `docs/specs/doc-governance.md`
  - `docs/specs/steer-pulse-automation.md`
  - `docs/specs/goal-loop-contract.md`
  - `docs/MEMORY.md`
  - `docs/TROUBLES.md`
  - `docs/LESSONS.md`
  - `hooks.json`
  - `skills/skill-maintenance/scripts/generate_harness_graph.py`
  - `skills/skill-maintenance/scripts/generate_skill_graph.py`
  - `skills/skill-maintenance/graph/README.md`
- `budget:` local shared checkout, one sustained implementation window, no deploy, no push, no spend, reviewer if available
- `time_window:` current native Goal until complete or blocked
- `portfolio_boundary:` none

## Metric Provider

- `provider:` hybrid
- `feedback_preset:` none
- `signal:` mechanical command pass plus documentation/schema review judgment
- `direction:` pass/fail
- `minimum:` all required checks pass; material review TAS-A or explicit reviewer-unavailable note with residual risk

## Proof Policy

- `proof_weight:` tests + review
- `delegated_lanes:` reviewer if available
- `drift_check_owner:` inline during execution; reviewer before final completion if available
- `design_baseline:` none
- `final_evidence:` links to lifecycle docs, graph contract, generated graph JSON, test results, and review/blocker note
- `self_certification:` allowed for mechanical test execution only; forbidden for final documentation/schema sufficiency when reviewer lane is available

## Feedback Policy

- `human_feedback:` none
- `review_question:` Does TASK-0213 provide a friendly, accurate lifecycle documentation surface and a conservative, useful semantic graph/FSA extraction path without overclaiming parser certainty or changing runtime semantics?
- `feedback_file:` none
- `notification:` none

## After Each Turn

1. Read every file listed in `files`, including this `progress.md` tail.
2. Choose the next action from the largest unresolved acceptance, evidence, or blocker gap.
3. Execute one bounded step.
4. Append a structured entry to `tickets/TASK-0213/progress.md`.
5. Run inline drift check against `ticket.md` and this program.
6. Continue, stop complete, or stop blocked with evidence.

## After Completion

- `on_goal_window_complete:` append completion progress, run proof/review, surface final evidence, and leave ticket ready for closeout/archive.
- `on_milestone_complete:` none
- `manual_replan_allowed:` yes
- `automatic_replan:` none

## Drift Policy

- `drift_check:` inline plus reviewer when available before final completion
- `checkpoints:` turn start, after docs draft, after generator/tests, before completion
- `drift_reviewer:` reviewer
- `block_on_drift:` yes

## Heartbeat Policy

- `cadence:` none
- `heartbeat_prompt:` none
- `no_op_policy:` not applicable
- `wake_condition:` none
- `heartbeat_action:` none
- `selected_file_policy:` none

## Batch / Board Policy

- `target_set:` none
- `board_source:` none
- `proceedable_filter:` none
- `proof_rows:` one proof row for TASK-0213 plus command/review evidence
- `split_when:` UI rendering becomes in scope, parser requires broad schema migration, or proof cannot be attributed to one ticket
- `no_op_policy:` not applicable

## Stop Conditions

- `complete_when:`
  - lifecycle docs and graph contract are written and linked
  - lifecycle graph generator and tests are implemented
  - generated graph artifacts exist
  - required checks pass or blockers are explicit
  - progress log records final evidence
- `blocked_when:`
  - local files needed for grounding are unavailable
  - parser ambiguity cannot be represented with confidence levels or curated overrides
  - tests fail after attempted repair
  - reviewer lane is required but unavailable and the risk is too high to self-report
- `pause_when:` user asks to change scope, UI rendering becomes necessary, or external service/deploy/push is requested
- `escalate_when:` docs conflict with memory decisions, graph schema implies runtime behavior, or hooks would mutate durable memory automatically

## Rollout Policy

- `target_set:` none
- `sample_proof:` none
- `batch_size:` none
- `promotion_rule:` none
- `rollback_or_hold_rule:` hold Farplane UI integration until graph artifact is stable
