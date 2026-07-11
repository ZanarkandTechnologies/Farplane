---
title: "Single Heartbeat Automation Topology Audit"
owner: automation-advisor
status: pass_with_external_sync
created_at: 2026-07-11
skill: automation-advisor
mode: structure_update
ticket_ref: tickets/archive/TASK-0319/ticket.md
---

# Single Heartbeat Automation Topology Audit

## Behavior Delta

- Before: Work Pulse and Taste Loop both used `kind = "heartbeat"`; Daily and
  Weekly Interval mixed provider intake, reward check-ins, self-improvement,
  and next-window planning.
- After: Work Pulse is the only heartbeat. Feed Scout, Daily BAU review,
  Weekly BAU review, Dogfood self-improvement, consolidation, and Taste Loop
  use separate cron records. Scheduled ticket sources stop after bounded ticket
  projection; Pulse owns execution and due experiment check-ins.

## First-Load Review

```text
line_count_before: 260
line_count_after: 269
kept_in_skill:
  - full desired-state TOML ownership
  - prompt minimality and live activation boundary
  - dedicated thread guidance
added:
  - one-heartbeat invariant
  - Feed Scout and Dogfood cron routes
moved_to_reference:
  - compact generic scheduled-record shape in templates/interval-automation.md
deleted_as_duplicate_or_rationale:
  - old Pulse/Daily/Weekly migration examples that restated skill workflows
extra_sections_kept_with_reason:
  - Live Activation Recipe remains the explicit app-side sync boundary
```

## Proof

- `farplane/automations.toml` parses and contains one heartbeat plus six cron
  records.
- `python3 bin/validators/check_farplane_project_files.py`: pass.
- `python3 bin/validators/run_git_gate.py --stage pre_commit --dry-run`: pass.
- Automation Advisor QA `single_heartbeat`, prompt size, skill boundary,
  runtime state, side-effect, and review-route checks: pass.
- Live automation/thread sync: pending because this implementation lane did
  not have app automation mutation tools.
