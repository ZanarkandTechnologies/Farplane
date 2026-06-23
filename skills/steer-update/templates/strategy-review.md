---
title: "Steer Strategy Review Workflow"
status: active
owner: steer-update
created_at: 2026-06-23
updated_at: 2026-06-23
---

# Steer Strategy Review Workflow

```text
weekly_steer(goals, memory, lessons, troubles, tickets, interval_reports)
  -> weekly_scrum_reflection + drift_check + next_week_plan + goals_delta? + ticket_deltas + pulse_constraints
```

Use the migrated weekly PM practices as a scrum steering loop: gather tickets
created, started, completed, blocked, or spawned in the last interval; build
the report before mutating goals; label stale or missing evidence; check drift
against `farplane/goals.md`; separate kept/changed/paused bets; and plan the
next week. Route executable changes into tickets or Goal Advisor handoffs.

Approval is required for north-star, KPI, strategy-axis, project-priority,
hold, quarterly, yearly, or durable milestone changes. Low-risk evidence and
current-signal updates may be proposed as auto-apply only when the report
contains clear supporting evidence.
