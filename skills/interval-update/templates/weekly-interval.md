---
title: "Weekly Interval Workflow"
status: active
owner: interval-update
created_at: 2026-06-23
updated_at: 2026-06-24
---

# Weekly Interval Workflow

```text
weekly_interval_update(
  review_window = last_week,
  planning_window = next_week,
  context_refs = {
    goals_ref: farplane/goals.md,
    daily_report_refs: .farplane/reports/interval/daily_interval/<review-window>*.md,
    ticket_refs: tickets/,
    memory_refs: [docs/MEMORY.md, docs/LESSONS.md, docs/TROUBLES.md],
    pulse_report_refs: .farplane/reports/pulse/
  }
) -> weekly_interval_report + drift_check + next_week_plan + goals_delta? + pulse_guidance
```

Run `interval-update`. Review the week through daily interval reports, ticket
movement, Pulse outcomes, worker outcomes, memory, lessons, and troubles.
Check drift against `farplane/goals.md`.

Plan only the next week. Route executable changes into tickets or Goal Advisor
handoffs. Use Goal Advisor when the next direction should become a durable Goal
Packet or ticket-backed execution plan.

Approval is required for north-star, KPI, strategy-axis, project-priority,
hold, quarterly, yearly, or durable milestone changes. Low-risk evidence and
current-signal updates may be proposed as auto-apply only when the report
contains clear supporting evidence.
