---
kind: goal-program
ticket_id: TASK-XXXX
status: draft
created_at: 2026-06-12
template_id: goal-loop-program
template_version: "0.1.7"
feature_refs:
  - FEAT-0029
  - FEAT-0032
---

# TASK-XXXX Goal Program

## Goal Mode

- `mode:` `active_goal` | `heartbeat` | `rollout` | `skill_improvement` |
  `ml_autoresearch` | `feedback_loop` | `batch_goal`
- `trigger:` `native_goal` | `scheduled_heartbeat` |
  `human_feedback_received` | `manual_resume`
- `files:` inline list of ticket/program/progress/spec/board/artifact files the
  generated Goal prompt must name under `Files:` and read before execution;
  experiment-backed packets also list their `hypothesis-tree.json`
- `compiled_from_ticket_updated_at:` timestamp copied from `ticket.md`
  frontmatter when this packet was generated
- `generated_prompt:` path to the native `/goal` prompt artifact, inline prompt
  location, or `none` only for explicit direct execution without native Goal
- `approval:` `pending` | `approved` | `revise` | `blocked`
- `budget:` time/token/model/compute/review/QA/feedback/spend limits,
  or `none`
- `time_window:` uninterrupted native Goal window, heartbeat cadence, or `none`
- `portfolio_boundary:` optional; use only when a longer planning graph is
  needed beyond the listed files

## Execution Contract

- `program_role:` executable loop policy for the Goal Packet, not a second
  ticket and not transcript memory
- `ticket_role:` source of truth for scope, acceptance, proof, blockers, and
  current next action
- `progress_role:` append-only observed state, evidence pointers, drift notes,
  blockers, and next actions
- `hypothesis_tree_role:` when Experiment Backbone is enabled, the sole current
  research-state owner; `program.md` must not duplicate nodes and `progress.md`
  must not become a competing frontier
- `prompt_contract:` the generated native `/goal` prompt must list this file
  under `Files:`, instruct the executor to read it before execution, and obey
  it for trigger mode, budget, metric or feedback provider, proof route, drift
  policy, after-turn routine, heartbeat or batch rules, and stop conditions
- `conflict_policy:` ticket scope and QA Strategy win over this program; if the
  ticket changed after `compiled_from_ticket_updated_at`, regenerate this
  program and the native `/goal` prompt before execution

## Metric Provider

- `provider:` `mechanical` | `review` | `agent_qa` | `human_feedback` |
  `market` | `hybrid`
- `feedback_preset:` `optimize-with-human` | `none`
- `signal:` command, eval, review verdict, feedback file, market result, or
  artifact-presence check
- `direction:` `higher` | `lower` | `pass/fail` | `accept/revise` | `none`
- `minimum:` pass threshold, TAS gate, human decision, or `none`

## Experiment Backbone

- `mode:` `disabled` | `enabled`
- `source_stage:` before the first mutation, bind the evaluator and baseline,
  then use local failures, supplied material, configured Feed Scout signals,
  linked papers/repos, or bounded direct research to extract applicable
  techniques, mechanisms, variables, and source references; stop on sufficient
  coverage rather than source count
- `hypothesis_tree:` `tickets/TASK-XXXX/hypothesis-tree.json` when enabled
- `tree_contract:` top-level source synthesis plus nodes keyed by stable ID;
  each node contains only `parent`, `family` (`intervention` or `diagnostic`),
  `hypothesis`, `mechanism`, `expected_observation`, `falsifier`,
  `expected_reward`, `reward_basis`, `source_refs`, `status`, `result`,
  `insight`, and `evidence_refs`; status is `pending`, `running`, `supported`,
  `falsified`, `inconclusive`, or `pruned`
- `derived_state:` derive children, depth, and pending leaves from `parent` and
  `status`; do not persist a second frontier, rank score, or Markdown projection
- `selector:` `leverage-advisor` performs one evidence-backed ordinal
  compounding comparison over eligible pending leaves; no pairwise tournament
  or tree-local scorer
- `selection_inputs:` objective, current bottleneck, tree, progress learnings,
  experiment receipts, constraints, guards, prerequisites, and remaining budget
- `search_budget:` bind beam/breadth, diagnostic-child, repair/rerun, mutable
  surface, compute, spend, and stopping limits inside this packet
- `diagnostic_rule:` create bounded diagnostic children only for surprising,
  invalid, prerequisite-uncertain, or causally ambiguous evidence; expected
  negative evidence can close a branch directly
- `writeback:` after evaluation, update the selected node and any new children
  in `hypothesis-tree.json`, then append the same selection rationale, evidence,
  learning, disposition, mutation, and next action chronologically to
  `progress.md`
- `concurrency:` parallelize source synthesis or experiments only when mutation
  surfaces and attribution are independent; one writer reconciles the tree

## Proof Policy

- `proof_weight:` `smoke` | `tests` | `qa` | `visual_qa` | `agent_qa` |
  `review` | `demo`
- `derived_from:` `ticket.md QA Strategy`; ticket proof policy wins on conflict
- `delegated_lanes:` `none` or list of `qa-tester`, `visual-qa`,
  `agent-qa-test`, `reviewer`, `demo`
- `drift_check_owner:` `inline` | `reviewer` | `goal-drift-reviewer` |
  `qa-tester`
- `design_baseline:` `tickets/TASK-XXXX/design.md` or `none`
- `final_evidence:` command output, report link, review receipt, screenshot
  Markdown image link, demo artifact, or blocker report
- `final_checkpoint:` before `stop_complete`, run or request QA evidence review
  and completion review when required by this proof policy, and satisfy
  `Docs Strategy` validation; write links back to `ticket.md`, `progress.md`,
  and `artifacts/`, then run `farplane ticket close TASK-XXXX`
- `self_certification:` allowed only for tiny mechanical checks; prohibited for
  QA, visual QA, adversarial QA, review, demo, or completion claims

## Feedback Policy

- `human_feedback:` `none` | `optional` | `required`
- `review_question:`
- `feedback_file:` `tickets/TASK-XXXX/artifacts/feedback/feedback.json`
- `notification:` `telegram` | `local_path` | `none`

## After Each Turn

1. Read every file listed in `files`, including each relevant `progress.md`
   tail and the current `hypothesis-tree.json` when enabled.
2. Choose the next action from the largest unresolved acceptance, evidence, or
   blocker gap. Experiment-backed modes use Leverage Advisor to select an
   eligible pending tree leaf from current evidence; they do not replay a fixed
   order.
3. Execute one bounded step.
4. Evaluate the result with the declared Metric Provider, ticket proof
   contract, or active skill evaluator.
5. If a result materially misses a declared expectation, is implausibly
   strong, or appears invalid, check evaluator and evidence integrity before
   trusting it. Allow bounded in-budget repairs or reruns only while a concrete
   integrity concern remains; repeated valid contradictory evidence must update
   the next action.
6. For experiment-backed modes, update the canonical tree first. Then append a
   compact observation, evidence link, learning, decision, tree mutation, and
   `next_action` to every `progress.md` whose ticket state changed.
7. Run or request drift check when required by `Drift Policy`; delegate the
   check when proof policy forbids self-certification.
8. Continue, stop complete, stop blocked, or wait for heartbeat/feedback.

## After Completion

- `on_goal_window_complete:` append completion progress to changed files, run
  proof/review; for a material implementation Goal, after QA passes run the
  `demo` skill to produce its narrated lead-engineer recap MP4; then run or
  request final QA evidence review and completion review when required by
  `Proof Policy`, satisfy `Docs Strategy` validation, surface final evidence
  required by `Proof Policy`, and close the ticket before `stop_complete`.
  Heartbeats, feedback checks, planning-only Goals, and direct non-Goal work do
  not inherit this demo step
- `on_milestone_complete:` run parent heartbeat or replan routine before
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
- `heartbeat_action:` start_goal | resume_goal | request_feedback | replan |
  blocked | no_op
- `selected_file_policy:` output/resume one time/budget-bounded Goal prompt
  with an inline `Files:` list

## Check-In Program

- `mode:` `not_applicable` | `delayed_reward`
- `inputs:` for `delayed_reward`, name the original `ticket.md`, this
  `program.md`, `progress.md`, matured Reward IDs supplied by Work
  Pulse, the current timestamp, and the exact evidence sources or artifacts
  needed to score them
- `procedure:` for `delayed_reward`, write an ordered, experiment-specific
  procedure that reads this program first, validates the supplied Reward IDs,
  collects the named evidence, compares actuals with the baseline and expected
  result, accounts for declared guards or confounders, evaluates only the matured
  rows, and chooses one declared decision
- `writeback:` define the exact `actual_result`, `decision`, `evaluated_at`,
  `evaluation_key`, `supersedes_evaluation_key`, and `evidence_refs` writeback
  for matured Reward rows plus the append-only `progress.md` observation and
  decision entry
- `decisions:` define experiment-specific `accept_when`, `kill_when`, and
  `monitor_when`; define how `monitor` schedules the next check-in on the same
  row. A materially changed hypothesis becomes a new experiment ticket rather
  than an `iterate` decision hidden in the old outcome.
- `idempotency:` preserve future and already-complete Reward rows; on retry,
  treat the same `evaluation_key` as a no-op. A correction requires a new key,
  `supersedes_evaluation_key`, new named evidence, and an explicit progress note.
- `source_gap:` when required evidence is missing, stale, or below the Metric
  Provider minimum, record the gap, choose `monitor` unless this program
  explicitly defines another safe outcome, and set the next check-in condition

For immediate feedback or tickets without delayed Reward rows, keep only
`mode: not_applicable` plus a short reason. Do not fill the delayed inputs,
procedure, writeback, decisions, idempotency, or source-gap fields.

## Batch / Board Policy

- `target_set:` none or list/path/query
- `board_source:` none or ticket index/board path
- `proceedable_filter:` status=todo, unclaimed, dependencies satisfied, and
  required tools available; a human gate limits only its named final action
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
