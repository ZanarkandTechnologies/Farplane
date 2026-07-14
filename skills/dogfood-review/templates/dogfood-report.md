---
kind: dogfood-review
ref: reports/dogfood-review/<timestamp>
project: <project>
created_at: <timestamp>
review_window: <start>..<end>
portfolio_cutoff: <timestamp>
previous_report_ref: <path or null>
status: draft
ui_summary: "<one concise self-improvement summary under 100 words>"
context_ref: <path or null>
active_experiment_refs: []
recent_archived_experiment_refs: []
tracked_refs: []
source_gaps: []
experiment_goal_packets: []
no_execution_receipt: "Pulse materialization only; no implementation, Goal execution, worker dispatch, check-in, promotion, rollback, or external action invoked"
---

# Weekly Self-Improvement Portfolio Report

## Summary

- `portfolio_result:`
- `most_material_learning:`
- `portfolio_cutoff:`
- `prior_report_cursor:`
- `next_wave:`

The cutoff is a snapshot boundary, not an experiment deadline. State recorded
after the cutoff belongs to the next report.

## Experiment Outcome Ledger

| Experiment | Surface | Feedback | State at cutoff | Expected reward | Actual / score | Attribution | Decision | Evidence |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |

Allowed state: `pending`, `monitoring`, `due_checkin_pending`, `inconclusive`,
`accepted`, `killed`, `iterating`, `source_gap`. Decisions are observations of
canonical ticket state; this report never performs the check-in.

## Active And Pending Portfolio

| Experiment | Surface | State | Next check-in / wake | Evidence minimum | Conflict set | Blocks new supply? |
| --- | --- | --- | --- | --- | --- | --- |

Every nonterminal row counts toward total WIP. Monitoring or due-check-in-pending
work blocks only dependent or conflicting supply, subject to the per-surface
and delayed-live caps.

## Due Check-In Pending Gaps

| Experiment / Reward row | Due at | Missing score/evidence | Effect | Safe action |
| --- | --- | --- | --- | --- |

## Transfer Candidates

| Source experiment | Proven pattern | Target surface | Attribution / guards | Required bounded proof | Verdict |
| --- | --- | --- | --- | --- | --- |

An accepted toy/eval is normally evidence for a bounded transfer or live pilot,
not permission for automatic global rollout.

## Rejected Patterns

| Pattern | Source experiment / report | Rejection evidence | Reconsider only if |
| --- | --- | --- | --- |

## Reward, Proof, And Feature Review

| Ticket / tracked ref | Expected | Actual | Proof quality | Regression / review | Finding or gap |
| --- | --- | --- | --- | --- | --- |

Tracked feature/system decisions may be `continue`, `adjust`, `cap`, `pause`,
`rollback`, `graduate`, `split_feature`, `merge`, or `source_gap`.

## History Query Receipts

| Query | Input | Matched | Returned | Area derivation gaps | Use |
| --- | ---: | ---: | ---: | --- | --- |
| global latest 20 | | | | | dedupe, attention, recent Reward context |
| self_improvement history | | | | | accepted/killed/pending patterns and active conflicts |

## Harness Health Findings

| Surface / signal | Current evidence | Importance / heat | Failure or opportunity | Candidate effect |
| --- | --- | --- | --- | --- |

## Weekly Allocation Receipt

- `planning_scope:` `reserved_area:self_improvement`
- `area_record_ref:` `harness.areas.self_improvement`
- `area_instruction_ref:` `harness.areas.self_improvement.planner_instruction`
- `area_instruction_applied:`
- `weekly_ticket_target:` 5
- `max_concurrent_live_delayed:` 5
- `one_active_per_attributable_surface:` true
- `active_nonterminal_wip:`
- `active_live_delayed_wip:`
- `new_weekly_slots:` 5
- `available_delayed_slots:` `max(0, max_concurrent_live_delayed - active_live_delayed_wip)`
- `occupied_surfaces:`
- `review_or_operator_capacity_constraint:`
- `allocation_verdict:` target_five | shortfall
- `shortfall_reasons:` []

Active WIP constrains conflicts, delayed load, dedupe, and review burden; it
does not subtract from unrelated weekly slots. The delayed-live cap limits new
delayed pilots only. Immediate experiments may fill independent slots.

## Ranked Improvement Candidates

| Rank | Candidate | Surface | Feedback / proof route | Objective impact | Compounding value | Cost / risk / review load | Interference / dedupe | Verdict |
| ---: | --- | --- | --- | --- | --- | --- | --- | --- |

Verdicts: `selected`, `rejected`, `deferred`, `duplicate`, `interferes`,
`source_gap`.

## Reserved Self-Improvement Wave

| Candidate | Feedback | Surface | Expected Reward | Goal / check-in shape | Output artifact | Verdict / ticket path |
| --- | --- | --- | --- | --- | --- | --- |

- `candidates_compared:`
- `area_instruction_receipt:` `{area_id: self_improvement, instruction_ref: harness.areas.self_improvement.planner_instruction, instruction_applied: <summary>, candidate_or_no_candidate: <result>}`
- `specs_admitted:` 0..5
- `tickets_materialized_by_pulse:` 0..5
- `ticket_paths:` []
- `known_fix_recoveries_within_wave:` 0..1
- `no_op_reason:` none | <reason>

### Candidate Requirements

Each admitted candidate is a complete `plan-next-wave` executable experiment
spec. Pulse, not Dogfood, materializes its ticket path.

- Every candidate declares an area, attributable surface, hypothesis, baseline, Reward
  expectation/guard, metric provider, proof route, budget, stop conditions, and
  promotion/rollback policy.
- Immediate candidates use an immediately available signal and have no future
  `check_in_at`, event wake, or delayed Check-In Program debt.
- Delayed candidates name the future signal, provider, and check-in procedure
  outline needed if the adaptive planner admits and materializes the experiment.
- Human-feedback candidates route through `optimize-with-human` and name their
  feedback artifact plus later decision procedure.
- Dogfood calls the one adaptive planner in
  `reserved_area:self_improvement` scope with target wave size five, then sends
  accepted specs to Pulse's bounded materialization route.
- Completion-learning tickets already exist and are deduped once. A known-fix
  recovery may occupy one of five slots but never becomes an extra sixth ticket.

## Source Gaps

| Gap | Effect | Safe decision |
| --- | --- | --- |

## Receipts

- `active_and_recent_archive_reviewed_before_candidates:` yes | no
- `previous_report_used_as_cursor_only:` yes | no | not_available
- `report_written_before_selection:` yes | no
- `cutoff_applied_without_forcing_terminal_decisions:` yes | no
- `weekly_target_or_shortfall_proved:` yes | no
- `delayed_live_cap_respected:` yes | no
- `one_active_per_surface_respected:` yes | no
- `non_interfering_immediate_capacity_preserved:` yes | no | not_applicable
- `planner_specs_admitted:` 0..5
- `pulse_ticket_paths_created:` 0..5
- `all_delayed_packets_have_executable_checkin_program:` yes | no | not_applicable
- `all_human_feedback_packets_route_optimize_with_human:` yes | no | not_applicable
- `experiment_executed_or_checked_in:` no
