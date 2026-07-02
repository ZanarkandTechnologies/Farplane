---
title: "Interval Codex Automation Template"
status: active
owner: automation-advisor
created_at: 2026-06-24
updated_at: 2026-07-02
template_version: "1.0.0"
---

# Interval Codex Automation Template

Use these `[[automations]]` records in `farplane/automations.toml` for scheduled
project interval automations. Each record is the full desired Codex automation
config: identity, schedule/RRULE-equivalent fields, workspace or thread target,
status, and exact prompt text.

## Canonical Shape

```toml
schema = "farplane_project_automations"
framework_template_version = "1.0.0"
updated_at = "YYYY-MM-DD"
owner = "automation-advisor"

[[automations]]
id = "<automation-id>"
name = "<human name>"
kind = "cron"
status = "active"
prompt = '''
Use $interval-update.

Run the configured Farplane interval. Review the bounded window, write the
date-stamped interval report, and emit Pulse or Goal Advisor guidance rather
than doing ticket implementation directly.

Params:
project_root = "<project-root>"
interval_id = "<interval_id>"
review_window = "<bounded review window>"
planning_window = "<bounded planning window>"
timezone = "<timezone or UTC>"

Config source:
farplane/automations.toml automation id="<automation-id>"
'''

[automations.target]
workspace = "<project-root>"

[automations.schedule]
type = "daily | weekly | monthly"
timezone = "<timezone>"
time = "05:33"
days = ["Mon"]
day_of_month = 1
rrule = "FREQ=DAILY;BYHOUR=5;BYMINUTE=33;BYSECOND=0"
```

Use either structured schedule fields or `rrule` when the target Codex
automation UI/API requires RRULE input. Do not include runtime run IDs,
last-run state, logs, or automation memory in tracked TOML.

## Migration Examples

Pulse:

```toml
[[automations]]
id = "project-pulse"
name = "Project Pulse"
kind = "heartbeat"
status = "active"
prompt = '''
Use $pulse-update.

Run one bounded Farplane Pulse beat for the project. Reconcile recent outcomes,
select at most the configured ready work, and write the normal Pulse report or
blocker through the skill contract.

Params:
project_root = "<project-root>"

Config source:
farplane/automations.toml automation id="project-pulse"
'''

[automations.target]
thread_id = "<pulse-thread-id>"

[automations.schedule]
type = "interval"
interval_minutes = 30
rrule = "FREQ=MINUTELY;INTERVAL=30"
```

Daily Interval:

```toml
[[automations]]
id = "project-daily-interval"
name = "Project Daily Interval"
kind = "cron"
status = "active"
prompt = '''
Use $interval-update.

Run the daily Farplane interval. Reflect on the last 24 hours, close or update
obvious reward signals, then plan the next 24 hours without executing ticket
work directly.

Params:
project_root = "<project-root>"
interval_id = "daily_interval"
review_window = "last_24h"
planning_window = "next_24h"
timezone = "<timezone>"

Config source:
farplane/automations.toml automation id="project-daily-interval"
'''

[automations.target]
workspace = "<project-root>"

[automations.schedule]
type = "daily"
timezone = "<timezone>"
time = "05:33"
rrule = "FREQ=DAILY;BYHOUR=5;BYMINUTE=33;BYSECOND=0"
```

Weekly Interval:

```toml
[[automations]]
id = "project-weekly-interval"
name = "Project Weekly Interval"
kind = "cron"
status = "active"
prompt = '''
Use $interval-update.

Run the weekly Farplane interval. Reflect on the last week, read child daily
intervals when present, close or update prior reward signals, then plan the
next week by working backwards from goals and bottlenecks.

Params:
project_root = "<project-root>"
interval_id = "weekly_interval"
review_window = "last_week"
planning_window = "next_week"
timezone = "<timezone>"

Config source:
farplane/automations.toml automation id="project-weekly-interval"
'''

[automations.target]
workspace = "<project-root>"

[automations.schedule]
type = "weekly"
timezone = "<timezone>"
days = ["Mon"]
time = "05:45"
rrule = "FREQ=WEEKLY;BYDAY=MO;BYHOUR=5;BYMINUTE=45;BYSECOND=0"
```
