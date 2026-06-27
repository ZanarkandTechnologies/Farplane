---
kind: project-automations
framework_template_version: "0.5.0"
updated_at: 2026-06-27
owner: automation-advisor
source_of_truth:
  - skills/pulse-update/SKILL.md
  - skills/interval-update/SKILL.md
  - skills/taste-loop/SKILL.md
  - farplane/pm.json
---

# Farplane Automations

This file stores reviewable desired-state config and prompts for Codex
automation records. Each automation keeps:

- a marker-delimited TOML config block for Codex automation metadata only:
  kind, status, workspace/thread target, and schedule.
- a marker-delimited prompt block for the human-authored Codex instruction,
  including skill call, skill params, and skill-specific overrides.

The TOML block syncs to Codex automation settings. The prompt block is copied
to the Codex automation prompt. Reusable gates, report shapes, and workflow
behavior live in the called skill.

## Pulse

<!-- farplane:automation-config id="farplane-ticket-update" format="toml" -->
```toml
id = "farplane-ticket-update"
name = "Farplane Pulse"
kind = "heartbeat"
status = "active"
target_thread_id = "019ed47a-3182-73f3-879f-a53797759b2a"

[schedule]
type = "interval"
interval_minutes = 30

```
<!-- /farplane:automation-config -->

<!-- farplane:automation-prompt id="farplane-ticket-update" -->
```text
Use $pulse-update.

Run one bounded Farplane Pulse beat for the project. Reconcile recent outcomes,
select at most the configured ready work, and write the normal Pulse report or
blocker through the skill contract.

Params:
project_root = "/Users/kenjipcx/Zanarkand Technologies/projects/Farplane"

Config source:
farplane/automations.md automation-config id="farplane-ticket-update"
```
<!-- /farplane:automation-prompt -->

## Daily Interval

<!-- farplane:automation-config id="farplane-daily-interval" format="toml" -->
```toml
id = "farplane-daily-interval"
name = "Farplane Daily Interval"
kind = "cron"
status = "active"
workspace = "/Users/kenjipcx/Zanarkand Technologies/projects/Farplane"

[schedule]
type = "daily"
timezone = "Asia/Kuala_Lumpur"
time = "05:33"

```
<!-- /farplane:automation-config -->

<!-- farplane:automation-prompt id="farplane-daily-interval" -->
```text
Use $interval-update.

Run the daily Farplane interval. Review the last 24 hours, produce the
date-stamped interval report, and plan the next 24 hours without executing
ticket work directly.

Params:
project_root = "/Users/kenjipcx/Zanarkand Technologies/projects/Farplane"
interval_id = "daily_interval"
review_window = "last_24h"
planning_window = "next_24h"
timezone = "Asia/Kuala_Lumpur"

Config source:
farplane/automations.md automation-config id="farplane-daily-interval"

Overrides:
read_parent_interval = "latest weekly_interval report when present"
plan_progress = "light"
goal_drift = "light"
ticket_board_drift = "light"
```
<!-- /farplane:automation-prompt -->

## Weekly Interval

<!-- farplane:automation-config id="farplane-weekly-interval" format="toml" -->
```toml
id = "farplane-weekly-interval"
name = "Farplane Weekly Interval"
kind = "cron"
status = "active"
workspace = "/Users/kenjipcx/Zanarkand Technologies/projects/Farplane"

[schedule]
type = "weekly"
timezone = "Asia/Kuala_Lumpur"
days = ["Mon"]
time = "05:45"

```
<!-- /farplane:automation-config -->

<!-- farplane:automation-prompt id="farplane-weekly-interval" -->
```text
Use $interval-update.

Run the weekly Farplane interval. Review the last week, read child daily
intervals when present, update the week-scale plan, and emit Pulse or Goal
Advisor guidance rather than doing ticket implementation directly.

Params:
project_root = "/Users/kenjipcx/Zanarkand Technologies/projects/Farplane"
interval_id = "weekly_interval"
review_window = "last_week"
planning_window = "next_week"
timezone = "Asia/Kuala_Lumpur"

Config source:
farplane/automations.md automation-config id="farplane-weekly-interval"

Overrides:
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
<!-- /farplane:automation-prompt -->

## Active-Hours Taste Loop

<!-- farplane:automation-config id="farplane-active-hours-taste-loop" format="toml" -->
```toml
id = "farplane-active-hours-taste-loop"
name = "Farplane Active-Hours Taste Loop"
kind = "heartbeat"
status = "active"
target_thread_id = "019f0774-76d7-77d3-b7e5-0e9bb48e232f"

[schedule]
type = "active_hours_interval"
timezone = "Asia/Kuala_Lumpur"
days = ["Mon", "Tue", "Wed", "Thu", "Fri"]
start = "10:00"
end = "18:00"
interval_minutes = 60

```
<!-- /farplane:automation-config -->

<!-- farplane:automation-prompt id="farplane-active-hours-taste-loop" -->
```text
Use $taste-loop.

Run one scheduled active-hours Taste Loop beat for Farplane. Read the
UI-editable config from farplane/automations.md, use Codex automation memory as
the active worker ledger, and reuse or resume an active worker before creating
any new worker. Select product-lane artifact workflows, not broad skill
summaries. Create or hand off at most one reviewable artifact workflow, then
route human feedback through the worker thread and optimize-with-human.

Do not create repo/runtime artifacts, worker threads, feedback cards, or
Telegram messages for ordinary no-op beats.

Params:
project_root = "/Users/kenjipcx/Zanarkand Technologies/projects/Farplane"
top_n = 3
max_actions_per_beat = 1
max_open_feedback = 3
target_groups = ["content-social", "content-video", "frontend", "harness", "self-improvement"]
output_channels = ["local_report", "telegram_ready", "farplane_ui_ready"]
cooldown_hours = 24
convergence_window = 5
minimum_delta = "qualitative_threshold"
log_noop = false

Config source:
farplane/automations.md automation-config id="farplane-active-hours-taste-loop"

Overrides:
controller_memory = "Codex automation memory.md"
worker_state = "reuse active_worker before creating any new worker"
noop_policy = "no repo/runtime/thread/artifact/feedback/Telegram side effects unless diagnostic logging is enabled"
```
<!-- /farplane:automation-prompt -->
