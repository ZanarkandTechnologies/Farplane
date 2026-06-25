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
instructions live here as plain operational prompts. Canonical files, report
paths, ticket boards, and PM thread grouping are resolved by the Farplane
project context and the called skills unless the prompt explicitly says to read
or write something else.

## Pulse

Automation id: `<pulse-automation-id>`
Name: `Project Pulse`
Kind: `heartbeat`
RRULE: `FREQ=MINUTELY;INTERVAL=30`
Target thread: `<pulse-thread-id>`

```text
You are the Project Pulse automation.

Call `pulse-update` for this project.

Use the skill's default Farplane refs for the static harness charter, tickets,
interval guidance, project products, action state, reward state, reports, and
PM thread grouping. Only pass extensions when this project has extra action
arms, custom gates, or extra context files.

Run one Pulse beat:
1. Reconcile previous worker outcomes and update reward memory.
2. Read the board, static harness charter, project products, action tree,
   recent interval guidance, and bandit state.
3. Use reasoning plus bandit state to choose exactly one bounded action.
4. Valid action arms include: pick a ready ticket, split an oversized ticket,
   clarify a blocker, create a small prep ticket, run QA/eval, update stale
   ticket metadata, consult goal-advisor, or no-op when unsafe.
5. Spawn one PM-owned worker thread only when the selected action needs one.
6. Append persistent worker chat thread IDs to the project PM manifest when
   they should render under the same employee in the UI.
7. If there are no proceedable tickets, choose one narrow product-shaped refill
   or maintenance arm from the action tree. Use `farplane/harness.md` to
   preserve the static human thesis and `farplane/products.md` to shape product
   refill tickets; chores stay in the default maintenance/proof arms. Do not
   default to goal-advisor; it is only one possible arm when goals or the next
   milestone are unclear.
8. Write decision, reward, spawned-thread, and report state.

Do not perform drift review, scrum reflection, or strategy replanning.
```

## Daily Interval

Automation id: `<daily-interval-automation-id>`
Name: `Project Daily Interval`
Kind: `cron`
RRULE: `FREQ=DAILY;BYHOUR=5;BYMINUTE=33;BYSECOND=0`
Execution environment: `local`
Workspace: `<project-root>`

```text
You are the Project Daily Interval automation.

Call:
- `interval_update(project_root="<project-root>", interval_id="daily_interval", review_window="last_24h", planning_window="next_24h", timezone="<timezone>")`

Reads:
- Default Farplane refs for the static harness charter, goals, tickets, memory,
  Pulse reports, interval reports, PM thread grouping, report paths, and
  interval context bundles.
- `farplane/goals.md` as the parent goal context.
- The latest `weekly_interval` report when one exists; use it as
  `parent_weekly_plan` and mark a source gap when it does not exist yet.

Writes:
- A dated daily interval report.
- The next-24-hour operating plan.
- Pulse guidance, proposed ticket deltas, Goal Advisor handoffs, and any
  approval-required goals delta.

Runs:
- `plan_progress`: light.
- `goal_drift`: light.
- `ticket_board_drift`: light.

Gates:
- Report before mutation.
- Source gaps instead of guessed refs.
- No scheduler state writes.

Only add more Reads/Writes lines or workflow instructions when this project has
extra context files, workflows, or project-specific report requirements.

Daily Interval owns the daily report, configured drift checks against goals and
the latest weekly interval report when available, and next-24-hour operating
plan. Convert executable work into ticket deltas or Goal Advisor handoffs. Do
not select due jobs or write scheduler state; Codex automation cadence is the
scheduler.
```

## Weekly Interval

Automation id: `<weekly-interval-automation-id>`
Name: `Project Weekly Interval`
Kind: `cron`
RRULE: `FREQ=WEEKLY;BYDAY=MON;BYHOUR=5;BYMINUTE=45;BYSECOND=0`
Execution environment: `local`
Workspace: `<project-root>`

```text
You are the Project Weekly Interval automation.

Call:
- `interval_update(project_root="<project-root>", interval_id="weekly_interval", review_window="last_week", planning_window="next_week", timezone="<timezone>")`

Reads:
- Default Farplane refs for the static harness charter, goals, tickets, memory,
  Pulse reports, interval reports, PM thread grouping, report paths, and
  interval context bundles.
- `farplane/goals.md` as the parent goal context.
- All `daily_interval` reports inside `last_week`; use them as
  `daily_reports` and mark a source gap when none exist yet.

Writes:
- A dated weekly interval report.
- The next-week plan.
- Pulse guidance, proposed ticket deltas, Goal Advisor handoffs, and any
  approval-required goals delta.
- Leverage decisions in the weekly interval report: selected, rejected,
  deferred, expired, or escalated candidates.
- Reward closure in the weekly interval report for previously selected
  leverage bets whose reward signal is due.

Runs:
- `plan_progress`: true.
- `codex_attention_drift`: true.
- `ticket_board_drift`: true.
- `feedback_obligations`: when sources exist.
- `opportunity_signals`: when sources exist.
- `goal_drift`: true.
- `metric_snapshot`: when sources exist.
- `compounding_leverage_review`: true.
- `priority_planning`: true.

Gates:
- Report before mutation.
- Approval required for static charter, north-star, KPI, strategy-axis,
  quarterly/yearly, durable milestone, and hold changes.
- Urgent leverage escalation requires high confidence, explicit loss term,
  evidence refs, review-by date, and owner route.
- Source gaps instead of guessed refs.
- No scheduler state writes.

Only add more Reads/Writes lines or workflow instructions when this project has
extra context files, workflows, or project-specific report requirements.

Weekly Interval owns the weekly report, configured report workflows, goals
drift check, and next-week plan. Use Goal Advisor when the next direction
should become a durable Goal Packet or ticket-backed execution plan. Do not
select due jobs or write scheduler state; Codex automation cadence is the
scheduler. When enabled report workflows have large context, `interval-update`
may run read-only subagent analysis lanes before merging findings into the
interval report.
When `compounding_leverage_review` is enabled, close due reward signals before
selecting the next 1-3 leverage bets.
```
