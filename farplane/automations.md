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
- Pulse is a persistent heartbeat thread because it owns fast PM/worker
  continuity. Daily and Weekly Interval are standalone Codex automations; each
  run writes dated reports, and file reports are the shared memory.

## Pulse

Automation id: `farplane-ticket-update`
Name: `Farplane Pulse`
Kind: `heartbeat`
RRULE: `FREQ=MINUTELY;INTERVAL=30`
Target thread: `019ed47a-3182-73f3-879f-a53797759b2a`

```text
You are the Farplane Pulse automation for this project.

Call `pulse-update` with project_root
`/Users/kenjipcx/Zanarkand Technologies/projects/Farplane` and no
project-specific extensions.

Use the skill's default Farplane refs for the static harness charter, tickets,
interval guidance, reports, project products, reward state, bandit state,
spawned-thread ledgers, action arms, and `farplane/pm.json`.

Run one Pulse beat only. Reconcile previous worker outcomes, use reasoning plus
the bandit policy to choose exactly one bounded action, and spawn or record the
result according to the `pulse-update` skill. If no proceedable tickets exist,
choose one narrow product-shaped refill or maintenance arm from the action tree.
Use `farplane/harness.md` to preserve the static human thesis and
`farplane/products.md` to shape product refill tickets; chores stay in the
default maintenance/proof arms. `consult goal-advisor` is one possible arm, not
the default.

Hard no-op gate: zero ready tickets means only `pick_ready_ticket` is blocked.
Before selecting `no_op_unsafe` or rewarding a no-op as positive, write an
`Action Arm Verdicts` section that evaluates `split_oversized_ticket`,
`clarify_blocker`, `create_prep_ticket`, `run_qa_or_eval`,
`refresh_ticket_metadata`, and `consult_goal_advisor` with concrete evidence.

Do not perform drift review, scrum reflection, or strategy replanning. Do not
push, deploy, publish, spend, mutate external systems, commit, or perform
destructive cleanup.

Final output: reward updates, selected action or no-op reason, child thread ID
or handoff blocker, report/state paths, and what evidence will decide the
reward next time.
```

## Daily Interval

Automation id: `farplane-daily-interval`
Name: `Farplane Daily Interval`
Kind: `cron`
RRULE: `FREQ=DAILY;BYHOUR=5;BYMINUTE=33;BYSECOND=0`
Execution environment: `local`
Workspace: `/Users/kenjipcx/Zanarkand Technologies/projects/Farplane`

```text
Run the Farplane Daily Interval automation for this project.

Call:
- `interval_update(project_root="/Users/kenjipcx/Zanarkand Technologies/projects/Farplane", interval_id="daily_interval", review_window="last_24h", planning_window="next_24h", timezone="Asia/Kuala_Lumpur")`

Reads:
- The skill's default Farplane refs for the static harness charter, goals,
  tickets, memory, lessons, troubles, history, Pulse reports, interval reports,
  PM thread grouping, report paths, and interval context bundles.
- `farplane/goals.md` as the parent goal context.
- The latest `weekly_interval` report when one exists; use it as
  `parent_weekly_plan` and mark a source gap when it does not exist yet.

Writes:
- A dated daily interval report under the default daily interval report path.
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

Daily Interval owns daily reporting, configured drift checks against goals and
the latest weekly interval report when available, and the next 24-hour
operating plan. The workflow must write the daily interval report first, then
produce the next-24h plan, Pulse guidance, Goal Advisor handoffs, and any
approval-required goals delta.

Pulse owns fast board action selection. Do not push, deploy, publish, spend,
mutate external systems, commit, spawn unbounded worker threads, perform
destructive cleanup, select due jobs, or write scheduler state.
```

## Weekly Interval

Automation id: `farplane-weekly-interval`
Name: `Farplane Weekly Interval`
Kind: `cron`
RRULE: `FREQ=WEEKLY;BYDAY=MON;BYHOUR=5;BYMINUTE=45;BYSECOND=0`
Execution environment: `local`
Workspace: `/Users/kenjipcx/Zanarkand Technologies/projects/Farplane`

```text
Run the Farplane Weekly Interval automation for this project.

Call:
- `interval_update(project_root="/Users/kenjipcx/Zanarkand Technologies/projects/Farplane", interval_id="weekly_interval", review_window="last_week", planning_window="next_week", timezone="Asia/Kuala_Lumpur")`

Reads:
- The skill's default Farplane refs for the static harness charter, goals,
  tickets, memory, lessons, troubles, history, Pulse reports, interval reports,
  PM thread grouping, report paths, and interval context bundles.
- `farplane/goals.md` as the parent goal context.
- All `daily_interval` reports inside `last_week`; use them as
  `daily_reports` and mark a source gap when none exist yet.

Writes:
- A dated weekly interval report under the default weekly interval report path.
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

Before final synthesis, run only the configured report workflows above. Keep
every workflow evidence-backed: cite tickets, daily reports, Pulse reports,
worker/thread refs, telemetry, feedback refs, feature/skill changes, external
source refs, prior leverage reward signals, or source gaps. Do not import
project-specific private Kenji workflow assumptions unless this automation later
supplies them as explicit context refs or workflows. When the context is large,
`interval-update` may run configured workflows as read-only subagent analysis
lanes before merging findings into the report.

Weekly Interval owns weekly reporting, drift checks against
`farplane/goals.md`, and next-week replanning. Use Goal Advisor when the next
direction should become a durable Goal Packet or ticket-backed execution plan.
When `compounding_leverage_review` is enabled, close due reward signals before
selecting the next 1-3 leverage bets.
Do not push, deploy, publish, spend, mutate external systems, commit, spawn
unbounded worker threads, perform destructive cleanup, select due jobs, or
write scheduler state.
```
