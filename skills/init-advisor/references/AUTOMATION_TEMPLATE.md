---
kind: project-automations
framework_template_version: "0.4.1"
updated_at: YYYY-MM-DD
owner: automation-advisor
---

# Project Automations

This file stores the exact Codex automation prompt blocks for the project.
Prompts configure cadence metadata, the target `$skill`, visible `Params`, and
intentional `Overrides` only. Reusable config contracts, defaults, gates,
report shapes, and workflow behavior live in the called skill.

## Pulse

| Field | Value |
| --- | --- |
| Automation id | `<pulse-automation-id>` |
| Name | `Project Pulse` |
| Kind | `heartbeat` |
| RRULE | `FREQ=MINUTELY;INTERVAL=30` |
| Target thread | `<pulse-thread-id>` |

Use `$pulse-update`.

Params:

```text
project_root = "<project-root>"
```

Overrides:

```text
none
```

## Daily Interval

| Field | Value |
| --- | --- |
| Automation id | `<daily-interval-automation-id>` |
| Name | `Project Daily Interval` |
| Kind | `cron` |
| RRULE | `FREQ=DAILY;BYHOUR=5;BYMINUTE=33;BYSECOND=0` |
| Workspace | `<project-root>` |

Use `$interval-update`.

Params:

```text
project_root = "<project-root>"
interval_id = "daily_interval"
review_window = "last_24h"
planning_window = "next_24h"
timezone = "<timezone>"
```

Overrides:

```text
read_parent_interval = "latest weekly_interval report when present"
plan_progress = "light"
goal_drift = "light"
ticket_board_drift = "light"
```

## Weekly Interval

| Field | Value |
| --- | --- |
| Automation id | `<weekly-interval-automation-id>` |
| Name | `Project Weekly Interval` |
| Kind | `cron` |
| RRULE | `FREQ=WEEKLY;BYDAY=MON;BYHOUR=5;BYMINUTE=45;BYSECOND=0` |
| Workspace | `<project-root>` |

Use `$interval-update`.

Params:

```text
project_root = "<project-root>"
interval_id = "weekly_interval"
review_window = "last_week"
planning_window = "next_week"
timezone = "<timezone>"
```

Overrides:

```text
read_child_intervals = "all daily_interval reports inside last_week"
plan_progress = true
codex_attention_drift = true
ticket_board_drift = true
feedback_obligations = "when sources exist"
opportunity_signals = "when sources exist"
goal_drift = true
metric_snapshot = "when sources exist"
compounding_leverage_review = true
skill_hardening = true
skill_refinement = "when sources exist"
docs_consolidation = "when sources exist"
priority_planning = true
```
