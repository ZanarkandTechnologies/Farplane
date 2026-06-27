---
title: "Pulse Codex Automation Template"
status: active
owner: automation-advisor
created_at: 2026-06-23
updated_at: 2026-06-27
template_version: "0.5.0"
---

# Pulse Codex Automation Template

Use these marker-delimited blocks for the project's Pulse automation in
`farplane/automations.md`. The TOML block is Codex automation metadata; the
prompt block carries the skill call and skill params copied into the live Codex
automation.

````markdown
<!-- farplane:automation-config id="<automation-id>" format="toml" -->
```toml
id = "<automation-id>"
name = "<human name>"
kind = "heartbeat"
status = "active"
target_thread_id = "<thread-id>"

[schedule]
type = "interval"
interval_minutes = 30
```
<!-- /farplane:automation-config -->

<!-- farplane:automation-prompt id="<automation-id>" -->
```text
Use $pulse-update.

Run one bounded Farplane Pulse beat for the project. Reconcile recent outcomes,
select at most the configured ready work, and write the normal Pulse report or
blocker through the skill contract.

Params:
project_root = "<project-root>"

Config source:
farplane/automations.md automation-config id="<automation-id>"
```
<!-- /farplane:automation-prompt -->
````
