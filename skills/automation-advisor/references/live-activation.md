---
title: Automation Live Activation
status: active
owner: automation-advisor
kind: reference
---

# Automation Live Activation

Load this only when the operator explicitly asks to activate or update live
automations (Claude scheduled tasks or Codex automations).

```text
activate_farplane_automations(project_root, desired_records,
                              persistent_thread_policy?)
  -> automation_ids + optional_pm_json_delta
```

1. Inspect existing live tasks for the record's `runtime` and update records matching project and
   automation identity rather than creating duplicates.
2. Update the owning Markdown first with the exact desired prompt, target,
   cadence, and status in the owning workspace's `farplane/automations/`.
   Never activate a step from `steps/` or an unresolved placeholder.
3. Target Feed Scout, token burn, and maintenance cron jobs at the project
   workspace. Target the single Daily/Weekly pair at the AI Office workspace.
   Never create a heartbeat; Work Pulse was deleted.
4. Copy each desired prompt exactly into the matching live task (`runtime_task`).
5. Only for an explicit persistent-thread exception, record the visible thread
   ID in `farplane/pm.json`; never store automation runtime IDs there.
6. Do not activate when goals are placeholders or the request is planning only.
   If app automation tools are unavailable, return `needs_automation_setup`.
7. After activation, compare desired and live state: no execution heartbeat,
   only the expected cron jobs, the correct project target, and no duplicate
   executor for the same record.

Never create an extra scheduler thread, automation JSON manifest, cadence env
vars, or thread rows merely to make cron jobs look persistent.
