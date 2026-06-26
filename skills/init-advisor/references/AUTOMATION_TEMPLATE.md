---
kind: project-automations
framework_template_version: "0.4.0"
updated_at: YYYY-MM-DD
owner: automation-advisor
---

# Project Automations

This file stores the exact Codex automation prompt blocks for the project.
Prompts configure cadence, project root, thread IDs, and project-specific
extensions only. Reusable loop behavior lives in `pulse-update` and
`interval-update`.

## Pulse

| Field | Value |
| --- | --- |
| Automation id | `<pulse-automation-id>` |
| Name | `Project Pulse` |
| Kind | `heartbeat` |
| RRULE | `FREQ=MINUTELY;INTERVAL=30` |
| Target thread | `<pulse-thread-id>` |

```text
Run one Project Pulse beat.

Call:
- `pulse_update(project_root="<project-root>")`

Project extensions: none.

Project gates:
- no push, deploy, publish, spend, account changes, or destructive cleanup.
- no drift review, scrum reflection, or strategy replanning.

Final output:
- execution mode
- reward updates
- child thread IDs or planning request
- report/state paths
- evidence that will decide the next reward update
```

## Daily Interval

| Field | Value |
| --- | --- |
| Automation id | `<daily-interval-automation-id>` |
| Name | `Project Daily Interval` |
| Kind | `cron` |
| RRULE | `FREQ=DAILY;BYHOUR=5;BYMINUTE=33;BYSECOND=0` |
| Workspace | `<project-root>` |

```text
Run the Project Daily Interval.

Call:
- `interval_update(project_root="<project-root>", interval_id="daily_interval", review_window="last_24h", planning_window="next_24h", timezone="<timezone>")`

Project context:
- read the latest `weekly_interval` report when it exists.

Project workflows:
- `plan_progress`: light.
- `goal_drift`: light.
- `ticket_board_drift`: light.

Project gates:
- report before mutation.
- source gaps instead of guessed refs.
- no scheduler state writes.
- no push, deploy, publish, spend, external mutation, commit, unbounded worker
  spawning, or destructive cleanup.

Final output:
- dated report path
- next-24-hour plan
- Pulse guidance
- proposed ticket deltas or Goal Advisor handoffs
- approval-required goals delta, if any
```

## Weekly Interval

| Field | Value |
| --- | --- |
| Automation id | `<weekly-interval-automation-id>` |
| Name | `Project Weekly Interval` |
| Kind | `cron` |
| RRULE | `FREQ=WEEKLY;BYDAY=MON;BYHOUR=5;BYMINUTE=45;BYSECOND=0` |
| Workspace | `<project-root>` |

```text
Run the Project Weekly Interval.

Call:
- `interval_update(project_root="<project-root>", interval_id="weekly_interval", review_window="last_week", planning_window="next_week", timezone="<timezone>")`

Project context:
- read all `daily_interval` reports inside `last_week`.

Project workflows:
- `plan_progress`: true.
- `codex_attention_drift`: true.
- `ticket_board_drift`: true.
- `feedback_obligations`: when sources exist.
- `opportunity_signals`: when sources exist.
- `goal_drift`: true.
- `metric_snapshot`: when sources exist.
- `compounding_leverage_review`: true.
- `skill_hardening`: true.
- `skill_refinement`: when sources exist.
- `docs_consolidation`: when sources exist.
- `priority_planning`: true.

Project gates:
- report before mutation.
- approval required for static charter, north-star, KPI, strategy-axis,
  quarterly/yearly, durable milestone, and hold changes.
- urgent leverage escalation requires high confidence, explicit loss term,
  evidence refs, review-by date, and owner route.
- source gaps instead of guessed refs.
- no scheduler state writes.
- no push, deploy, publish, spend, external mutation, commit, unbounded worker
  spawning, or destructive cleanup.

Final output:
- dated report path
- next-week plan
- lane distribution and ticket budget
- Pulse guidance
- proposed ticket deltas or Goal Advisor handoffs
- approval-required goals delta, if any
- leverage decisions and reward closure
```
