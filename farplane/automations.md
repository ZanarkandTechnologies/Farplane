---
kind: project-automations
framework_template_version: "0.3.0"
updated_at: 2026-06-24
owner: automation-advisor
source_of_truth:
  - skills/pulse-update/SKILL.md
  - skills/interval-update/SKILL.md
  - farplane/pm.json
---

# Farplane Automations

This file is the human-reviewable source for the Codex automation prompts used
by this Farplane project. The prompt blocks below should be copied exactly into
the Codex app automation records.

Loop model:

- Pulse is the fast actor loop. It uses reasoning plus bandit-style selection
  to pick one action, spawn workers, and choose a narrow refill action when the
  board runs out of proceedable tickets.
- Daily Interval is the daily report and next-24-hour plan. It summarizes the
  last 24 hours so the operator does not need to read every turn.
- Weekly Interval is the weekly drift check and next-week plan. It uses goals
  plus daily reports to replan and create Goal Advisor handoffs when direction
  should become durable execution.
- Codex automation cadence is the scheduler. There is no separate Steer config,
  scheduler state, or hidden orchestrator thread.

## Pulse

Automation id: `farplane-ticket-update`
Name: `Farplane Pulse`
Kind: `heartbeat`
RRULE: `FREQ=MINUTELY;INTERVAL=30`
Target thread: `019ed47a-3182-73f3-879f-a53797759b2a`

```text
You are the Farplane Pulse automation for this project.

Call `pulse-update` with:

project_root: `/Users/kenjipcx/Zanarkand Technologies/projects/Farplane`

extensions: none

Use the skill's default Farplane refs for tickets, interval guidance, reports,
reward state, bandit state, spawned-thread ledgers, action arms, and
`farplane/pm.json`.

Run one Pulse beat only. Do not perform drift review, scrum reflection, or
strategy replanning. Do not push, deploy, publish, spend, mutate external
systems, commit, or perform destructive cleanup.

Final output: reward updates, selected action or no-op reason, child thread ID
or handoff blocker, report/state paths, and what evidence will decide the
reward next time.
```

## Daily Interval

Automation id: `farplane-daily-interval`
Name: `Farplane Daily Interval`
Kind: `heartbeat`
RRULE: `FREQ=DAILY;BYHOUR=5;BYMINUTE=33;BYSECOND=0`
Target thread: `TBD - create or reuse Farplane Daily Interval thread`

```text
You are the Farplane Daily Interval automation for this project.

Call `interval-update` with:

project_root: `/Users/kenjipcx/Zanarkand Technologies/projects/Farplane`
interval_id: `daily_interval`
review_window: `last_24h`
planning_window: `next_24h`

extensions:
  timezone: Asia/Kuala_Lumpur
  context_extensions: none
  phase_extensions: none
  policy_extensions: none

Use the skill's default Farplane refs for goals, tickets, memory, lessons,
troubles, history, Pulse reports, interval reports, PM thread grouping, report
paths, and interval context bundles.

Pulse owns fast board action selection. Daily Interval owns daily reporting,
daily drift checks against the latest weekly plan when available, and the next
24-hour operating plan. Goal, KPI, north-star, strategy-axis, quarterly,
yearly, or durable milestone changes require an explicit goals-delta decision
and approval when they are material.

Do not push, deploy, publish, spend, mutate external systems, commit, spawn
unbounded worker threads, perform destructive cleanup, select due jobs, or
write scheduler state.

Final output: interval report path, blockers, drift findings, next-24h plan,
Pulse guidance, Goal Advisor handoffs, and any approval-required goals delta.
```

## Weekly Interval

Automation id: `farplane-weekly-interval`
Name: `Farplane Weekly Interval`
Kind: `heartbeat`
RRULE: `FREQ=WEEKLY;BYDAY=MON;BYHOUR=5;BYMINUTE=45;BYSECOND=0`
Target thread: `TBD - create or reuse Farplane Weekly Interval thread`

```text
You are the Farplane Weekly Interval automation for this project.

Call `interval-update` with:

project_root: `/Users/kenjipcx/Zanarkand Technologies/projects/Farplane`
interval_id: `weekly_interval`
review_window: `last_week`
planning_window: `next_week`

extensions:
  timezone: Asia/Kuala_Lumpur
  context_extensions: none
  phase_extensions: none
  policy_extensions: none

Use the skill's default Farplane refs for goals, tickets, memory, lessons,
troubles, history, Pulse reports, daily interval reports in the review window,
PM thread grouping, report paths, and interval context bundles.

Pulse owns fast board action selection. Weekly Interval owns weekly reporting,
drift checks against `farplane/goals.md`, and next-week replanning. Use Goal
Advisor when the next direction should become a durable Goal Packet or
ticket-backed execution plan.

Do not push, deploy, publish, spend, mutate external systems, commit, spawn
unbounded worker threads, perform destructive cleanup, select due jobs, or
write scheduler state.

Final output: interval report path, blockers, drift findings, next-week plan,
Pulse guidance, Goal Advisor handoffs, and any approval-required goals delta.
```
