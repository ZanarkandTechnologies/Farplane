---
kind: interval-report
project: <project>
automation_id: <automation_id>
report_profile: <daily_interval | weekly_interval | custom>
status: draft
created_at: <timestamp>
review_window: <start>..<end>
planning_window: <start>..<end>
context_bundle: <path>
---

# Interval Update Report

## Summary

- `decision:`
- `why_now:`
- `accepted_tradeoff:`

## Evidence Reviewed

| Source | Status | Key signal | Evidence |
| --- | --- | --- | --- |

## Drift Check

- `drift_against:` parent plan, original goals, mission, current milestone
- `verdict:` aligned | drifting | blocked | source_gap
- `evidence:`
- `correction:`

## KPI / Feedback Status

| Axis / KPI / feedback surface | State | Trend | Confidence | Gap |
| --- | --- | --- | --- | --- |

## Strategy Decisions

| Decision | Kind | Evidence | Consequence | Owner / next surface |
| --- | --- | --- | --- | --- |

Kinds: `keep`, `change`, `pause`, `kill`, `test`.

## Next Window Plan

| Priority | Why now | Expected output | Proof or reward signal | Owner / next surface |
| --- | --- | --- | --- | --- |

## Goals Delta

Use this block as the only bridge from interval evidence into `farplane/goals.md`.
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

## Downstream Guidance

- `top_lanes:`
- `constraints:`
- `blocked_or_human_gated:`
- `allowed_pulse_actions:`
- `do_not_do:`

## Scheduled Actions

| Action | Due? | Result | Evidence | Next due |
| --- | --- | --- | --- | --- |
| quarterly_plan |  |  |  |  |
| annual_review |  |  |  |  |

Default: keep quarterly/yearly and other intervals greater than one week as
scheduled actions inside the weekly interval until repeated evidence shows a
separate persistent lane adds value.

## Source Gaps And Blockers

-

## Outputs

- `context_bundle:`
- `interval_report:`
- `goals_delta_applied:`
- `goals_delta_requires_approval:`
- `ticket_deltas:`
- `ledger_update:`
