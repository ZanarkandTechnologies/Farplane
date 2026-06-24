---
kind: goal-program
ticket_id: TASK-0218
status: active
created_at: 2026-06-24
template_id: goal-loop-program
template_version: "0.1.1"
feature_refs:
  - FEAT-0029
  - FEAT-0032
  - FEAT-0046
---

# TASK-0218 Goal Program

## Goal Mode

- `mode:` `active_goal`
- `trigger:` `native_goal`
- `files:`
  - `tickets/TASK-0218/ticket.md`
  - `tickets/TASK-0218/program.md`
  - `tickets/TASK-0218/progress.md`
  - `bin/README.md`
  - `bin/AGENTS.md`
  - `PROJECT_RULES.md`
  - `AGENTS.md`
  - `install.sh`
- `budget:` time not specified; token/model/compute none; subagent none by
  default; review none mechanical; QA none; feedback none; spend none
- `time_window:` current native Goal window until safe reductions are exhausted
  or a blocking compatibility constraint appears
- `portfolio_boundary:` none

## Metric Provider

- `provider:` `mechanical`
- `feedback_preset:` `none`
- `signal:` top-level bin file count, irreducible-bin report, reference scans,
  wrapper smoke checks, unit tests, validators, install shell syntax, and
  py_compile
- `direction:` `lower` for top-level bin file count; `pass/fail` for checks
- `minimum:` all remaining top-level bin files justified; all required checks
  pass; no generated bin caches remain

## Proof Policy

- `proof_weight:` `tests`
- `delegated_lanes:` `none`
- `drift_check_owner:` `inline`
- `design_baseline:` `none`
- `final_evidence:` before/after top-level bin file count, irreducible-bin
  report path, required check summary, and commit hash if committed
- `self_certification:` allowed for mechanical checks only

## Feedback Policy

- `human_feedback:` `none`
- `review_question:` none
- `feedback_file:` none
- `notification:` none

## After Each Turn

1. Read the ticket, program, progress tail, and current `bin/` inventory.
2. Choose the highest-confidence remaining reduction cluster.
3. Move/delete/consolidate only files whose references, install ownership, and
   wrapper semantics are understood.
4. Update docs, install paths, tests, validators, wrappers, and imports in the
   same cluster.
5. Append a compact progress entry before ending the turn.
6. Continue while safe reductions remain; otherwise run proof and write the
   irreducible-bin report.

## After Completion

- `on_goal_window_complete:` append completion entry, update ticket state,
  write `tickets/TASK-0218/artifacts/proof/irreducible-bin.md`, run proof
  checks, stage/commit only this ticket's cleanup if requested or if the
  working tree cleanup is complete enough for a coherent commit
- `on_milestone_complete:` none
- `manual_replan_allowed:` yes
- `automatic_replan:` none

## Drift Policy

- `drift_check:` `inline`
- `checkpoints:` turn start, before moving a public command, before deleting a
  file, before completion
- `drift_reviewer:` none
- `block_on_drift:` yes

## Heartbeat Policy

- `cadence:` none
- `heartbeat_prompt:` none
- `no_op_policy:` log no-op only if no safe reduction exists
- `wake_condition:` manual resume
- `heartbeat_action:` no_op
- `selected_file_policy:` none

## Batch / Board Policy

- `target_set:` top-level `bin/*` files
- `board_source:` none
- `proceedable_filter:` active local references understood, no human gate, no
  live install/hook compatibility break without wrapper
- `proof_rows:` one decision row per remaining top-level bin file in
  `artifacts/proof/irreducible-bin.md`
- `split_when:` removing a file requires changing public architecture,
  migration policy, external install behavior, or unrelated dirty work
- `no_op_policy:` log no-op when no safe reduction exists

## Stop Conditions

- `complete_when:` top-level `bin/` has been minimized as far as safe
  compatibility allows, every remaining file is justified, required checks pass,
  and generated caches are removed
- `blocked_when:` the next reduction requires breaking an installed/public
  command path, changing architecture beyond this ticket, or resolving
  unrelated dirty workspace changes
- `pause_when:` not applicable
- `escalate_when:` a candidate removal is valuable but needs operator approval
  because it would intentionally drop compatibility

## Rollout Policy

- `target_set:` none
- `sample_proof:` none
- `batch_size:` none
- `promotion_rule:` none
- `rollback_or_hold_rule:` restore wrapper/import path and rerun proof checks
