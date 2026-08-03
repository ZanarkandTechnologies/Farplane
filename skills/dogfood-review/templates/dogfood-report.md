---
kind: dogfood-review
ref: reports/dogfood-review/<timestamp>
project: <project>
created_at: <timestamp>
review_window: <start>..<end>
portfolio_cutoff: <timestamp>
previous_report_ref: <path or null>
status: draft
ui_summary: "<one concise summary>"
planner_context_ref: reports/dogfood-review/<timestamp>
source_gaps: []
no_action_receipt: "no planning, materialization, execution, dispatch, check-in, Reward decision, promotion, rollback, or skill mutation"
---

# Weekly Self-Improvement Portfolio Checkpoint

## Summary

- `portfolio_result:`
- `most_material_learning:`
- `cutoff_and_cursor:`
- `next_planner_context:`

## Reconstruction Receipt

| Query (`limit: all`) | Exhausted | Cutoff | Exact-area matches | Still-live earlier | Ambiguous/source gaps | Evidence |
| --- | --- | ---: | ---: | --- | --- |

## Complete Outcome Ledger

| Ticket | Surface | State | Ultimate KPI / contribution | Expected | Actual | Decision/check-in | Evidence |
| --- | --- | --- | --- | --- | --- | --- | --- |

Allowed state: `pending`, `monitoring`, `due_checkin_pending`, `iterating`,
`accepted`, `killed`, `source_gap`. Missing/immature outcomes remain pending.

## Live Portfolio And Conflicts

| Ticket | Surface | State | Next wake | Conflict set | Evidence minimum |
| --- | --- | --- | --- | --- | --- |

## Forecast Calibration

| Ticket | Mode/cohort | Frozen forecast | Mature actual | Error/coverage | Attribution limit |
| --- | --- | --- | --- | --- | --- |

## Portfolio-Selection Lessons

| Pattern ID | Scope | Finding | Source ticket/Reward/evidence | Status | Target-memory ref |
| --- | --- | --- | --- | --- | --- |

## Opportunity Signals

| Signal | Surface | Evidence | Expected business link | Dedupe/conflict | Verdict |
| --- | --- | --- | --- | --- | --- |

Verdicts: `qualified`, `deprioritized`, `duplicate`, `conflict`, `source_gap`,
`not_ticketable`. These are planner context, not executable skill calls.

## Feature, Skill, And Harness Findings

| Surface | Current evidence | Failure/opportunity | Proof gap | Source refs |
| --- | --- | --- | --- | --- |

## Planner Context Handoff

- `planner_context_ref:` this report
- `planning_scope:` normal global Plan Next Wave
- `skill_calls_created_by_dogfood:` 0
- `tickets_materialized_by_dogfood:` 0
- `wave_size:` derived later from current execution/review/conflict/delayed capacity

## Source Gaps

| Gap | Effect | Safe decision |
| --- | --- | --- |

## Receipts

- `history_query_limit:` all | invalid_numeric_limit
- `history_receipt_exhausted:` yes | no
- `all_live_earlier_packets_read:` yes | no
- `ambiguous_area_kept_as_source_gap:` yes | no
- `previous_report_used_as_cursor_only:` yes | no | not_available
- `ticket_truth_preserved:` yes | no
- `external_outcome_attribution_only:` yes | no
- `planner_skill_calls_created:` 0
- `tickets_materialized:` 0
- `execution_or_dispatch:` no
- `checkin_or_reward_decision:` no
- `skill_or_policy_mutation:` no
