---
kind: weekly-pm-report
project: <project>
automation_id: <automation_id>
cadence: weekly_pm_plan
status: draft
created_at: <timestamp>
review_window: <start>..<end>
context_bundle: <path>
---

# Weekly PM Report

## Summary

- `decision:`
- `why_now:`
- `accepted_tradeoff:`

## Evidence Reviewed

| Source | Status | Key signal | Evidence |
| --- | --- | --- | --- |

## KPI / Feedback Status

| Axis / KPI / feedback surface | State | Trend | Confidence | Gap |
| --- | --- | --- | --- | --- |

## Strategy Decisions

| Decision | Kind | Evidence | Consequence | Owner / next surface |
| --- | --- | --- | --- | --- |

Kinds: `keep`, `change`, `pause`, `kill`, `test`.

## Goals Delta

Use this block as the only bridge from weekly evidence into `farplane/goals.md`.
Do not edit the goals portfolio before this block exists.

| Delta | Target | Decision | Evidence | Risk | Next action |
| --- | --- | --- | --- | --- | --- |

Decisions:

- `auto_apply`: source refs, current-signal notes, stale labels, or minor
  milestone wording backed by clear evidence.
- `approval_required`: north star, KPI, strategy axis, project priority, hold,
  stop condition, quarterly goal, yearly goal, or durable milestone changes.
- `rejected_source_gap`: insufficient evidence; create an instrumentation,
  access, feedback, or research ticket instead.

## Ticket Delta

| Ticket / candidate | Delta | Reason | Evidence |
| --- | --- | --- | --- |

## Daily PM Guidance

- `top_lanes:`
- `constraints:`
- `blocked_or_human_gated:`
- `allowed_heartbeat_actions:`
- `do_not_do:`

## Quarterly / Yearly Rollup

- `decision:` no_new_schedule | manual_rollup | propose_future_cadence
- `reason:`
- `evidence:`

Default: keep quarterly/yearly as manual or on-demand aggregation over weekly
reports until repeated weekly evidence shows a separate scheduled thread adds
value.

## Source Gaps And Blockers

-

## Outputs

- `context_bundle:`
- `weekly_report:`
- `goals_delta_applied:`
- `goals_delta_requires_approval:`
- `ticket_deltas:`
- `ledger_update:`
