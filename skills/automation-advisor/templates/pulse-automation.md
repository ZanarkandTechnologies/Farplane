---
title: "Pulse Codex Automation Template"
status: active
owner: automation-advisor
created_at: 2026-06-23
updated_at: 2026-07-02
template_version: "1.0.0"
---

# Pulse Codex Automation Template

Use this `[[automations]]` record in `farplane/automations.toml` for a
project's Pulse automation. The record is the full desired Codex automation
config: identity, schedule, target, status, and exact prompt text.

```toml
[[automations]]
id = "<pulse-automation-id>"
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
farplane/automations.toml automation id="<pulse-automation-id>"
'''

[automations.target]
thread_id = "<pulse-thread-id>"

[automations.schedule]
type = "interval"
interval_minutes = 30
```
