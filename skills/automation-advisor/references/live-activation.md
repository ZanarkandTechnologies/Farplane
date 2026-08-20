---
title: Codex Automation Live Activation
status: active
owner: automation-advisor
kind: reference
---

# Codex Automation Live Activation

Load this only when the operator explicitly asks to activate or update live
Codex automations.

```text
activate_farplane_automations(project_root, desired_records,
                              pulse_thread_id?, persistent_thread_policy?)
  -> automation_ids + pulse_thread_id? + optional_pm_json_delta
```

1. Inspect existing Codex automations and update records matching project and
   automation identity rather than creating duplicates.
2. Update `farplane/automations.toml` first with the exact desired prompt,
   target, cadence, and status.
3. Reuse the existing Project Pulse thread for the one heartbeat. Target Feed
   Scout, Daily/Weekly Interval, Dogfood, and maintenance cron jobs at the
   project workspace by default.
4. Copy each desired prompt exactly into the matching Codex automation.
5. Only for an explicit persistent-thread exception, record the visible thread
   ID in `farplane/pm.json`; never store automation runtime IDs there.
6. Do not activate when goals are placeholders or the request is planning only.
   If app automation tools are unavailable, return `needs_automation_setup`.

Never create an extra scheduler thread, automation JSON manifest, cadence env
vars, or thread rows merely to make cron jobs look persistent.
