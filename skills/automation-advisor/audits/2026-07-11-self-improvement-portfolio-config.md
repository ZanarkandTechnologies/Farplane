---
title: "Weekly Self-Improvement Portfolio Automation Audit"
owner: automation-advisor
status: pass_pending_live_sync
created_at: 2026-07-11
skill: automation-advisor
mode: config_update
ticket_ref: tickets/TASK-0320/ticket.md
---

# Weekly Self-Improvement Portfolio Automation Audit

## Behavior Delta

- Before: the weekly Dogfood prompt reviewed current experiments under a
  global WIP limit of one and could create at most one new packet.
- After: it reads active and recent archived Goal Packets plus the previous
  report, writes the portfolio report first, and may create a bounded,
  non-interfering next wave from available capacity.
- Work Pulse remains the only heartbeat, experiment executor, and check-in
  dispatcher. The prompt tells resumed check-ins to execute the original
  ticket's `program.md` rather than adding another scoring path.

## Operator Parameters

```text
experiment_wave_size = 2
experiment_wip_limit = 3
max_concurrent_live_delayed = 1
one_active_per_attributable_surface = true
```

These starting limits permit an unrelated immediate toy or eval while one
live delayed intervention monitors, without allowing overlapping experiments
on the same attributable surface.

## Proof

- Project and bootstrap TOML parse.
- Both weekly prompts carry the same portfolio inputs and four capacity
  parameters.
- The Monday 06:00 schedule and workspace target are unchanged.
- Desired topology remains one heartbeat plus six cron records.
- `python3 bin/validators/check_doc_refs.py`: pass.
- `python3 bin/validators/check_farplane_project_files.py`: pass.
- `python3 tickets/scripts/check_ticket_metadata.py tickets/TASK-0320/ticket.md`:
  pass.
- Live Codex automation sync is intentionally owned by the coordinating lane.
