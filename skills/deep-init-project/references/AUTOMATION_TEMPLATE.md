---
kind: project-automations
framework_template_version: "0.3.0"
updated_at: YYYY-MM-DD
owner: automation-advisor
---

# Project Automations

This file stores the exact Codex automation prompt blocks for the project.
Copy the prompt blocks into the Codex app automation records.

Skills stay generic. Project-specific intent, cadence, policy, and workflow
extensions live here as plain operational prompts. Canonical files, report
paths, ticket boards, and PM thread grouping are resolved by the Farplane
project context and the called skills unless explicitly extended.

## Pulse

Automation id: `<pulse-automation-id>`
Name: `Project Pulse`
Kind: `heartbeat`
RRULE: `FREQ=MINUTELY;INTERVAL=30`
Target thread: `<pulse-thread-id>`

```text
You are the Project Pulse automation.

Call `pulse-update` for this project.

Use the skill's default Farplane refs for tickets, interval guidance, action
state, reward state, reports, and PM thread grouping. Only pass extensions when
this project has extra action arms, custom gates, or extra context files.

Run one Pulse beat:
1. Reconcile previous worker outcomes and update reward memory.
2. Read the board, action tree, recent interval guidance, and bandit state.
3. Use reasoning plus bandit state to choose exactly one bounded action.
4. Valid action arms include: pick a ready ticket, split an oversized ticket,
   clarify a blocker, create a small prep ticket, run QA/eval, update stale
   ticket metadata, consult goal-advisor, or no-op when unsafe.
5. Spawn one PM-owned worker thread only when the selected action needs one.
6. Append persistent worker chat thread IDs to the project PM manifest when
   they should render under the same employee in the UI.
7. If there are no proceedable tickets, choose one narrow refill or maintenance
   arm from the action tree. Do not default to goal-advisor; it is only one
   possible arm when goals or the next milestone are unclear.
8. Write decision, reward, spawned-thread, and report state.

Do not perform drift review, scrum reflection, or strategy replanning.
```

## Daily Interval

Automation id: `<daily-interval-automation-id>`
Name: `Project Daily Interval`
Kind: `heartbeat`
RRULE: `FREQ=DAILY;BYHOUR=5;BYMINUTE=33;BYSECOND=0`
Target thread: `<daily-interval-thread-id>`

```text
You are the Project Daily Interval automation.

Call `interval-update` for this project with:

interval_id: `daily_interval`
review_window: `last_24h`
planning_window: `next_24h`

Use the skill's default Farplane refs for goals, tickets, memory, Pulse
reports, interval reports, PM thread grouping, report paths, and interval
context bundles. Only pass extensions when this project has extra context
files, lanes, or project-specific report instructions.

Daily Interval owns the daily report, drift check against the latest weekly
plan when available, and next-24-hour operating plan. Convert executable work
into ticket deltas or Goal Advisor handoffs. Do not select due jobs or write
scheduler state; Codex automation cadence is the scheduler.
```

## Weekly Interval

Automation id: `<weekly-interval-automation-id>`
Name: `Project Weekly Interval`
Kind: `heartbeat`
RRULE: `FREQ=WEEKLY;BYDAY=MON;BYHOUR=5;BYMINUTE=45;BYSECOND=0`
Target thread: `<weekly-interval-thread-id>`

```text
You are the Project Weekly Interval automation.

Call `interval-update` for this project with:

interval_id: `weekly_interval`
review_window: `last_week`
planning_window: `next_week`

Use the skill's default Farplane refs for goals, tickets, memory, Pulse
reports, daily interval reports in the review window, PM thread grouping,
report paths, and interval context bundles. Only pass extensions when this
project has extra context files, lanes, or project-specific report
instructions.

Weekly Interval owns the weekly report, goals drift check, and next-week plan.
Use Goal Advisor when the next direction should become a durable Goal Packet or
ticket-backed execution plan. Do not select due jobs or write scheduler state;
Codex automation cadence is the scheduler.
```
