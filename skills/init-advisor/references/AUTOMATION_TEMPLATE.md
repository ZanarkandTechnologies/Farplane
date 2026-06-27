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

## Monthly Registry Consolidation

| Field | Value |
| --- | --- |
| Automation id | `<monthly-registry-consolidation-automation-id>` |
| Name | `Project Monthly Registry Consolidation` |
| Kind | `cron` |
| RRULE | `FREQ=MONTHLY;BYMONTHDAY=1;BYHOUR=6;BYMINUTE=15;BYSECOND=0` |
| Workspace | `<project-root>` |

Use `$consolidate`.

Run the monthly registry consolidation review. This is a report-only registry
truth and ownership compression pass, not a weekly self-learning loop and not
a direct artifact rewrite.

Scope:

```text
target = [
  "docs/skills/registry.jsonl",
  "docs/features/registry.jsonl",
  "docs/systems/registry.jsonl",
  "docs/templates/registry.jsonl",
  "docs/sources/registry.jsonl"
]
structure = "registry"
```

Constraints:

```text
preserve_ids = true
preserve_evidence = true
no_delete = true
owner_boundary = "registry rows only; route underlying artifact edits to owners"
```

Output:

```text
.farplane/reports/consolidation/registry/<YYYY-MM-DDTHHMMSSZ>.md
```

Params:

```text
project_root = "<project-root>"
review_window = "last_month"
planning_window = "next_month"
timezone = "<timezone>"
```
