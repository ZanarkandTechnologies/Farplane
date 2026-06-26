---
kind: project-automations
framework_template_version: "0.4.1"
updated_at: 2026-06-26
owner: automation-advisor
source_of_truth:
  - skills/pulse-update/SKILL.md
  - skills/interval-update/SKILL.md
  - skills/taste-loop/SKILL.md
  - farplane/pm.json
---

# Farplane Automations

This file stores the exact prompt blocks copied into Codex automation records.
Prompts should configure cadence metadata, the target `$skill`, visible
`Params`, and intentional `Overrides` only. Reusable config contracts,
defaults, gates, report shapes, and workflow behavior live in the called skill.

## Pulse

| Field | Value |
| --- | --- |
| Automation id | `farplane-ticket-update` |
| Name | `Farplane Pulse` |
| Kind | `heartbeat` |
| RRULE | `FREQ=MINUTELY;INTERVAL=30` |
| Target thread | `019ed47a-3182-73f3-879f-a53797759b2a` |

Use `$pulse-update`.

Params:

```text
project_root = "/Users/kenjipcx/Zanarkand Technologies/projects/Farplane"
```

Overrides:

```text
none
```

## Daily Interval

| Field | Value |
| --- | --- |
| Automation id | `farplane-daily-interval` |
| Name | `Farplane Daily Interval` |
| Kind | `cron` |
| RRULE | `FREQ=DAILY;BYHOUR=5;BYMINUTE=33;BYSECOND=0` |
| Workspace | `/Users/kenjipcx/Zanarkand Technologies/projects/Farplane` |

Use `$interval-update`.

Params:

```text
project_root = "/Users/kenjipcx/Zanarkand Technologies/projects/Farplane"
interval_id = "daily_interval"
review_window = "last_24h"
planning_window = "next_24h"
timezone = "Asia/Kuala_Lumpur"
```

Overrides:

```text
read_parent_interval = "latest weekly_interval report when present"
plan_progress = "light"
goal_drift = "light"
ticket_board_drift = "light"
```
```

## Weekly Interval

| Field | Value |
| --- | --- |
| Automation id | `farplane-weekly-interval` |
| Name | `Farplane Weekly Interval` |
| Kind | `cron` |
| RRULE | `FREQ=WEEKLY;BYDAY=MO;BYHOUR=5;BYMINUTE=45;BYSECOND=0` |
| Workspace | `/Users/kenjipcx/Zanarkand Technologies/projects/Farplane` |

Use `$interval-update`.

Params:

```text
project_root = "/Users/kenjipcx/Zanarkand Technologies/projects/Farplane"
interval_id = "weekly_interval"
review_window = "last_week"
planning_window = "next_week"
timezone = "Asia/Kuala_Lumpur"
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

## Active-Hours Taste Loop

| Field | Value |
| --- | --- |
| Automation id | `farplane-active-hours-taste-loop` |
| Name | `Farplane Active-Hours Taste Loop` |
| Kind | `cron` |
| RRULE | `FREQ=HOURLY;INTERVAL=1` |
| Workspace | `/Users/kenjipcx/Zanarkand Technologies/projects/Farplane` |
| Status | `active in Codex app; gated by active-hours config` |

Use `$taste-loop`.

Params:

```text
project_root = "/Users/kenjipcx/Zanarkand Technologies/projects/Farplane"
```

Overrides:

```text
none
```
