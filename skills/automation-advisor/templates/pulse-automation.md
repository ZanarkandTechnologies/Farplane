---
title: "Pulse Codex Automation Template"
status: active
owner: automation-advisor
created_at: 2026-06-23
updated_at: 2026-07-10
template_version: "1.0.0"
---

# Pulse Codex Automation Template

Use this `[[automations]]` record in `farplane/automations.toml` for a
project's Pulse automation. The record is the full desired Codex automation
config: identity, schedule, target, status, and exact prompt text. It is the
project's only `kind = "heartbeat"` record; all other scheduled skills use
`kind = "cron"`.

```toml
[[automations]]
id = "<pulse-automation-id>"
name = "Project Pulse"
kind = "heartbeat"
status = "active"
prompt = '''
Use $pulse-update.

Run one bounded Work Pulse. Reconcile the board, make due ticket check-ins
eligible, dispatch executable tickets up to the worker limit, and refill an
empty BAU board through the next-wave planner. Pulse owns all ticket execution,
including experiment implementation and later reward check-ins.

Params:
project_root = "<project-root>"
wave_size = 3
worker_limit = 1
review_wip = 3

Final response:
- State the action taken or no-op reason.
- List tickets dispatched, chased, admitted, completed/reconciled, or blocked.
- Summarize refill outcome, worker/review limits, source gaps, and next owner.
- Link any report, ticket, worker, or receipt artifacts created by the beat.

Config source:
farplane/automations.toml automation id="<pulse-automation-id>"
'''

[automations.target]
thread_id = "<pulse-thread-id>"

[automations.schedule]
type = "interval"
interval_minutes = 30
```
