---
title: "Daily Interval Workflow"
status: active
owner: interval-update
created_at: 2026-06-23
updated_at: 2026-06-24
---

# Daily Interval Workflow

```text
daily_interval_update(
  review_window = last_24h,
  planning_window = next_24h,
  context_refs = {
    parent_plan_ref: latest weekly interval report,
    ticket_refs: tickets/,
    pulse_report_refs: .farplane/reports/pulse/,
    worker_thread_refs: spawned worker thread rows or PM thread index
  }
) -> daily_interval_report + next_24h_plan + pulse_guidance
```

Run `interval-update`. Review the last 24 hours of
Pulse decisions, worker outcomes, ticket changes, blockers, failed attempts,
and notable file changes. Compare that work against the latest weekly interval
plan when available.

Plan only the next 24 hours. The output should help the operator scan the day
and help Pulse choose bounded actions until the next daily interval run.

Do not run broad strategy replanning unless a weekly interval job is also due
or a real plan trigger is hit. Do not execute leaf tickets from this workflow.
