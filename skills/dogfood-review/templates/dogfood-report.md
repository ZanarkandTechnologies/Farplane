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
no_execution_receipt: "no implementation, Goal, Pulse, worker, check-in, promotion, rollback, or external action invoked"
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

## Capacity Receipt

- `experiment_wave_size:` 2
- `experiment_wip_limit:` 3
- `max_concurrent_live_delayed:` 1
- `one_active_per_attributable_surface:` true
- `active_nonterminal_wip:`
- `active_live_delayed_wip:`
- `raw_total_capacity:` `max(0, experiment_wip_limit - active_nonterminal_wip)`
- `available_packet_slots:` `min(experiment_wave_size, raw_total_capacity)`
- `available_delayed_slots:` `max(0, max_concurrent_live_delayed - active_live_delayed_wip)`
- `occupied_surfaces:`
- `review_or_operator_capacity_constraint:`
- `capacity_verdict:`

The delayed-live cap limits new delayed pilots only. An unrelated immediate toy,
replay, or eval may use remaining total capacity.

## Ranked Improvement Candidates

| Rank | Candidate | Surface | Feedback / proof route | Objective impact | Compounding value | Cost / risk / review load | Interference / dedupe | Verdict |
| ---: | --- | --- | --- | --- | --- | --- | --- | --- |

Verdicts: `selected`, `rejected`, `deferred`, `duplicate`, `interferes`,
`source_gap`.

## Experiment Candidate Wave

| Candidate | Area | Feedback | Surface | Expected Reward | Horizon / check-in shape | Cost / risk | Selection evidence |
| --- | --- | --- | --- | --- | --- | --- | --- |

- `candidates_proposed:` 0..<available_packet_slots>
- `recovery_ticket_limit:`
- `recovery_tickets_created_or_updated:`
- `experiment_tickets_created:` 0
- `no_op_reason:` none | <reason>

### Candidate Requirements

Each candidate is a report row, not a ticket or Goal Packet.

- Every candidate declares an area, attributable surface, hypothesis, baseline, Reward
  expectation/guard, metric provider, proof route, budget, stop conditions, and
  promotion/rollback policy.
- Immediate candidates use an immediately available signal and have no future
  `check_in_at`, event wake, or delayed Check-In Program debt.
- Delayed candidates name the future signal, provider, and check-in procedure
  outline needed if the adaptive planner admits and materializes the experiment.
- Work Pulse's adaptive planner globally ranks and admits ordinary experiment
  candidates. Completion-learning tickets already exist and are counted once
  from their report receipt; Dogfood must not recreate them. Dogfood may create
  only a bounded direct recovery ticket for other settled evidence and never
  creates an experiment ticket.

## Source Gaps

| Gap | Effect | Safe decision |
| --- | --- | --- |

## Receipts

- `active_and_recent_archive_reviewed_before_candidates:` yes | no
- `previous_report_used_as_cursor_only:` yes | no | not_available
- `report_written_before_selection:` yes | no
- `cutoff_applied_without_forcing_terminal_decisions:` yes | no
- `total_wip_cap_respected:` yes | no
- `delayed_live_cap_respected:` yes | no
- `one_active_per_surface_respected:` yes | no
- `non_interfering_immediate_capacity_preserved:` yes | no | not_applicable
- `goal_packets_created:` 0..<available_packet_slots>
- `all_delayed_packets_have_executable_checkin_program:` yes | no | not_applicable
- `experiment_executed_or_checked_in:` no
