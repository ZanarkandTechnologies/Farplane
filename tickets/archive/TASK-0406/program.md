---
kind: goal-program
ticket_id: TASK-0406
status: active
created_at: 2026-07-25
template_id: goal-loop-program
template_version: "0.1.4"
feature_refs:
  - FEAT-0029
  - FEAT-0032
---

# TASK-0406 Goal Program

## Goal Mode

- `mode:` active_goal
- `trigger:` native_goal
- `files:`
  - `tickets/TASK-0406/ticket.md`
  - `tickets/TASK-0406/program.md`
  - `tickets/TASK-0406/progress.md`
  - `tickets/TASK-0406/diagrams.md`
  - `tickets/archive/TASK-0405/ticket.md`
  - `tickets/archive/TASK-0405/progress.md`
  - `farplane/harness.yaml`
  - `farplane/metrics.yaml`
  - `docs/features/FEAT-0007-ticket-as-durable-task-memory.md`
  - `docs/features/FEAT-0063-metric-advisor-cards.md`
  - `docs/features/FEAT-0067-daily-interval-review-reports.md`
  - `docs/features/FEAT-0071-project-work-pulse.md`
  - `docs/systems/horizon-loop.md`
- `compiled_from_ticket_updated_at:` 2026-07-25T23:04:13+08:00
- `generated_prompt:` `tickets/TASK-0406/artifacts/native-goal-prompt.md`
- `approval:` approved
- `budget:` time not specified; tokens not specified; local compute allowed;
  delegated QA, agent QA, drift, and review required; external spend none;
  deploy none
- `time_window:` uninterrupted until the ticket is complete or genuinely blocked
- `portfolio_boundary:` TASK-0406 only

## Execution Contract

- `program_role:` executable loop policy for this Goal Packet
- `ticket_role:` source of truth for scope, acceptance, proof, and blockers
- `progress_role:` append-only observations, evidence, drift, blockers, and next actions
- `prompt_contract:` read this program first and obey its budget, proof, drift,
  logging, and stop policies
- `conflict_policy:` ticket scope and QA Strategy win; regenerate this packet
  if the ticket changes materially

## Metric Provider

- `provider:` hybrid
- `feedback_preset:` none
- `signal:` ordered mechanical checks plus delegated QA, adversarial agent QA,
  evidence review, and completion review
- `direction:` pass/fail
- `minimum:` all ticket Done conditions and TAS-A evidence/completion reviews

## Proof Policy

- `proof_weight:` agent_qa
- `derived_from:` `ticket.md` QA Strategy
- `delegated_lanes:` qa-tester, agent-qa-test, reviewer, goal-drift-reviewer
- `drift_check_owner:` goal-drift-reviewer
- `design_baseline:` `tickets/TASK-0406/diagrams.md`
- `final_evidence:` ticket Done checklist, ordered test receipt, both integrated
  control-loop fixtures, TASK-0405 regression receipt, agent-QA report,
  evidence review, and completion review
- `final_checkpoint:` validate the active ticket with the explicit changed-path
  boundary; require QA evidence and completion reviews at TAS-A; update ticket,
  progress, and artifact links; run `farplane ticket close TASK-0406`
- `self_certification:` prohibited for QA, agent QA, evidence review, and completion

## Feedback Policy

- `human_feedback:` none
- `review_question:` Is the full approved TASK-0406 migration implemented,
  integrated, documented, and supported by the required proof?
- `feedback_file:` none
- `notification:` none

## After Each Turn

1. Re-read the ticket, program, and latest progress entry.
2. Compare current work with the six ticket changes and ordered sanity checks.
3. Execute the largest coherent unresolved slice without overwriting unrelated
   dirty-worktree changes.
4. Append a compact progress entry with changed files, checks, drift, blocker,
   and next action.
5. Request drift or proof review at the ticket checkpoints.
6. Continue until complete or genuinely blocked.

## After Completion

- `on_goal_window_complete:` complete all proof and review gates, close the
  ticket mechanically, and report artifacts plus residual risk
- `on_milestone_complete:` run focused tests before expanding to the next change
- `manual_replan_allowed:` only for a real blocker or ticket contradiction
- `automatic_replan:` none

## Drift Policy

- `drift_check:` subagent_required
- `checkpoints:` packet start, after core schema/control-loop implementation,
  before docs regeneration, before completion
- `drift_reviewer:` goal-drift-reviewer
- `block_on_drift:` yes

## Heartbeat Policy

- `cadence:` none
- `heartbeat_prompt:` none
- `no_op_policy:` not applicable
- `wake_condition:` manual resume only if genuinely blocked
- `heartbeat_action:` blocked
- `selected_file_policy:` this active Goal owns the approved ticket

## Check-In Program

- `mode:` not_applicable
- `reason:` the implementation proof is immediate; the ticket Reward remains a
  later outcome measurement owned by its existing Reward contract

## Batch / Board Policy

- `target_set:` TASK-0406
- `board_source:` `tickets/TASK-0406/ticket.md`
- `proceedable_filter:` approved active ticket owned by this session
- `proof_rows:` one implementation row plus integrated, QA, agent-QA, evidence,
  docs, and completion-review receipts
- `split_when:` a genuine authority, safety, or conflicting-write blocker appears
- `no_op_policy:` not applicable

## Stop Conditions

- `complete_when:` every Done condition passes, required artifacts exist,
  evidence and completion reviews reach TAS-A, and ticket close succeeds
- `blocked_when:` required authority is missing, dirty overlapping work cannot
  be reconciled safely, or a ticket contract contradiction prevents execution
- `pause_when:` external input is strictly required
- `escalate_when:` only after safe local alternatives and scoped checks are exhausted

## Rollout Policy

- `target_set:` none
- `sample_proof:` none
- `batch_size:` none
- `promotion_rule:` none
- `rollback_or_hold_rule:` keep the ticket open and do not restore dual strategy paths
