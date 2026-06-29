---
kind: project-automations
framework_template_version: "0.5.0"
updated_at: 2026-06-27
owner: automation-advisor
source_of_truth:
  - skills/pulse-update/SKILL.md
  - skills/interval-update/SKILL.md
  - skills/consolidate/SKILL.md
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

Call:
Run the daily Farplane interval. Reflect on the last 24 hours, close or update
obvious reward signals, then plan the next 24 hours without executing ticket
work directly.

Reads:
- latest weekly_interval report when present as parent context

Runs:
- light reflection only: plan progress, goal drift, and ticket board drift

Gates:
- write a date-stamped interval report
- keep the next-window plan small and executable
- each selected priority must name the goal, bottleneck, or reward signal it
  moves
- emit Pulse constraints rather than doing ticket implementation

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

Call:
Run the weekly Farplane interval. Reflect on the last week, read child daily
intervals when present, close or update prior reward signals, then plan the
next week by working backwards from the goals and the bottlenecks that actually
move the needle.

Reads:
- all daily_interval reports inside last_week when present

Runs:
- reflection workflows for progress, attention, board state, feedback,
  opportunities, goal drift, and metrics when sources exist
- reward closure and compounding leverage review before final planning
- final priority planning only after reflection and reward/leverage synthesis

Gates:
- write a date-stamped interval report
- do not execute ticket implementation directly
- select only 1-3 leverage bets when compounding leverage review is enabled
- each selected lane or priority must name the goal, bottleneck, or reward
  signal it is expected to move
- emit Pulse constraints, ticket deltas, or Goal Advisor handoffs

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

## Monthly Registry Consolidation

<!-- farplane:automation-config id="farplane-monthly-registry-consolidation" format="toml" -->
```toml
id = "farplane-monthly-registry-consolidation"
name = "Farplane Monthly Registry Consolidation"
kind = "cron"
status = "active"
workspace = "/Users/kenjipcx/Zanarkand Technologies/projects/Farplane"

[schedule]
type = "monthly"
timezone = "Asia/Kuala_Lumpur"
day_of_month = 1
time = "06:15"

```
<!-- /farplane:automation-config -->

<!-- farplane:automation-prompt id="farplane-monthly-registry-consolidation" -->
```text
Use $consolidate.

Run the monthly Farplane registry consolidation review. This is a registry
truth and ownership compression pass, not the weekly self-learning loop and not
a direct skill/docs rewrite.

Scope:
target = [
  "docs/skills/registry.jsonl",
  "docs/features/registry.jsonl",
  "docs/systems/registry.jsonl",
  "docs/templates/registry.jsonl",
  "docs/sources/registry.jsonl"
]
structure = "registry"

Constraints:
preserve_ids = true
preserve_evidence = true
no_delete = true
owner_boundary = "registry rows only; route underlying artifact edits to their owning skill, doc, generator, or validator"

Output:
Write a dated report under:
.farplane/reports/consolidation/registry/<YYYY-MM-DDTHHMMSSZ>.md

The report should include:
- registry inventory and source freshness
- duplicate or overlapping row clusters
- stale, orphaned, generated-output-drift, or wrong-owner rows
- keep, merge, refactor, retire, or watch recommendations
- owner-specific handoffs for skill-maintenance, documentation, eval,
  generated registry validators, or tickets
- loss check showing IDs, evidence, generated outputs, and owner boundaries were preserved

Do not edit registries or underlying artifacts during this automation run.
Do not create a metrics registry. Metrics were intentionally removed from this
monthly workflow until repeated reports prove which measurements deserve a
separate owner.

Params:
project_root = "/Users/kenjipcx/Zanarkand Technologies/projects/Farplane"
review_window = "last_month"
planning_window = "next_month"
timezone = "Asia/Kuala_Lumpur"

Config source:
farplane/automations.md automation-config id="farplane-monthly-registry-consolidation"
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
days = ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"]
start = "10:00"
# Overnight window: active from 10:00 through 00:59; inactive 01:00-09:59.
end = "01:00"
interval_minutes = 60

```
<!-- /farplane:automation-config -->

<!-- farplane:automation-prompt id="farplane-active-hours-taste-loop" -->
```text
Use $taste-loop.

Run one Taste Loop beat for Farplane when invoked by the scheduled active-hours
automation or by explicit manual operator request. Read the UI-editable config
from farplane/automations.md, use Codex automation memory as the active worker
ledger, and reuse or resume an active worker before creating any new worker.
Select product-lane artifact workflows, not broad skill summaries. Run the
Goal-backed founder loop: reuse the active ticket for the same
`product_lane + workflow_id`, log a planning hypothesis cycle, create one to three
TasteProposal planning artifacts, route idea feedback through the worker
thread with optimize-with-human using `founder_lens=true`, then execute only
approved proposals and request execution feedback from that same worker thread.
TasteProposals must include customer/buyer, problem, wedge, offer/artifact,
distribution angle, validation question, next bet if approved, pivot trigger if
rejected, taste insight, artifact shape, core angle, execution beats, why it
could win, cringe risks, references or taste pack, feedback question, and next
step; hook-only cards are valid only when the artifact itself is just a hook.

Do not create repo/runtime artifacts, worker threads, feedback cards, or
Telegram messages for ordinary no-op beats.

If an active worker is waiting for feedback, verify the worker thread is visible
in the Codex app before trusting the ledger. If the worker id is missing or
unfindable, update the ticket/progress with a blocker instead of claiming the
thread is waiting. If the worker is visible and feedback is stale, send one
phone-viewable Telegram reminder from that worker thread: include the proposal
or artifact summary and one clear reply action in Telegram itself, prefer simple
Telegram Markdown for Taste Loop feedback/reminder bodies, then record
`last_reminder_at`, `reminder_count`, and send/fallback status.

When a ticket declares `progress_unit = hypothesis_cycle`, run
`python3 skills/taste-loop/scripts/check_progress_hypothesis_cycles.py
<program.md> <progress.md>` before recording a waiting or terminal state. If it
fails, update ticket/progress with a blocker instead of sending another
feedback request.

Params:
project_root = "/Users/kenjipcx/Zanarkand Technologies/projects/Farplane"
top_n = 3
max_actions_per_beat = 1
max_open_feedback = 3
impress_mode = true
founder_lens = true
max_planning_rollouts = 3
default_scenario = "tickets/TASK-0237/artifacts/agi-toy-shop-scenario.md"
target_groups = ["content-social", "content-video", "frontend", "harness", "self-improvement"]
output_channels = ["local_report", "telegram_ready", "farplane_ui_ready"]
cooldown_hours = 24
reminder_after_hours = 3
max_reminders_per_feedback = 2
convergence_window = 5
minimum_delta = "qualitative_threshold"
log_noop = false

Config source:
farplane/automations.md automation-config id="farplane-active-hours-taste-loop"

Overrides:
controller_memory = "Codex automation memory.md"
worker_state = "reuse active_worker before creating any new worker"
ticket_reuse = "reuse one active ticket/Goal Packet per product_lane + workflow_id until terminal completion, blocker, budget exhaustion, discard, closeout, or explicit operator request"
worker_visibility = "verify worker_thread_ref is app-visible before recording waiting_for_feedback; otherwise block"
reminder_policy = "for stale waiting feedback, send one phone-viewable Telegram Markdown reminder from the visible worker thread, then update progress and memory"
worker_goal_packet = "ticket.md + program.md + progress.md before worker action"
phase_policy = "TasteProposal planning artifacts before execution artifacts; use founder_lens=true; track idea_pass_rate and execution_pass_rate separately"
progress_log = "worker progress.md records planning/execution hypothesis cycles: current hypothesis, attempt, artifact refs, human question, feedback result, learning, and next hypothesis"
progress_validator = "run skills/taste-loop/scripts/check_progress_hypothesis_cycles.py before waiting or terminal state when progress_unit = hypothesis_cycle"
feedback_budget = "count valid product-workflow feedback only; report legacy broad-skill/router feedback as hygiene"
skill_promotion = "no target-skill hardening from one rejection; harden only repeated same-phase failure or reusable approved pattern"
noop_policy = "no repo/runtime/thread/artifact/feedback/Telegram side effects unless diagnostic logging is enabled"
```
<!-- /farplane:automation-prompt -->
