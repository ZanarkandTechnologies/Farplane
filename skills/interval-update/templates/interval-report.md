---
kind: interval-report
ref: reports/interval/<interval_id>/<timestamp>
project: <project>
automation_id: <automation_id>
interval_id: <daily|weekly>
status: draft
created_at: <timestamp>
review_window: <start>..<end>
ui_summary: "<one concise BAU summary under 100 words>"
source_gaps: []
---

# <Daily|Weekly> BAU Report

## Summary

- `window_result:`
- `material_change:`
- `operator_attention:`

## Work Reviewed

| State | Tickets / reports | Evidence | Observation |
| --- | --- | --- | --- |

## Objective And Metric Signals

| Objective / metric | Direction | Evidence | Confidence / source gap |
| --- | --- | --- | --- |

## Problems

- [ ] <problem>. Evidence: `<prior or same-run ref>`. Ticket: none
- [x] <resolved or ticketed problem>. Evidence: `<ref>`. Ticket: `TASK-XXXX`

Use ordinary Markdown rows only. Label each open row in prose as either
`carried` from prior finalized evidence or `new` in this report. New rows are
left for the adaptive project planner to evaluate.

## Maintenance Candidates

| Problem | Prior finalized evidence | Dedupe evidence | Proof / stop condition | Area / KPI | Result |
| --- | --- | --- | --- | --- | --- |

Results: `planner_candidate`, `already_owned`, `ledger_only_new`,
`ineligible_direction`, `source_gap`.

## Source Gaps

| Missing or stale source | Effect on report | Safe fallback |
| --- | --- | --- |

## Receipts

- `report_finalized_before_candidate_handoff:` yes | no
- `recovery_ticket_limit:`
- `recovery_tickets_created_or_updated:`
- `experimental_or_new_direction_tickets_created:` 0
- `new_direction_planned:` no
- `provider_or_dogfood_run:` no
- `reward_or_checkin_mutated:` no
- `ticket_execution_started:` no
