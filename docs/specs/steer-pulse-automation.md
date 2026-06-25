---
title: "Pulse and Interval Automation"
status: active
owner: farplane-framework
created_at: 2026-06-23
updated_at: 2026-06-25
tags:
  - farplane
  - automations
  - pulse
  - intervals
refs:
  - farplane/automations.md
  - skills/pulse-update/SKILL.md
  - skills/interval-update/SKILL.md
  - skills/automation-advisor/SKILL.md
---

# Pulse and Interval Automation

Farplane projects run autonomously through explicit Codex automations:

```text
pulse_update(project_root, extensions?, pulse_policy?)
  -> ready ticket execution + planning request? + decision state

interval_update(project_root, interval_id, review_window, planning_window,
                context_refs?, report_workflows?, planning_policy?,
                write_policy?, now?)
  -> dated interval report + next-window plan + Pulse guidance
```

The default project set is Pulse, Daily Interval, and Weekly Interval. Codex
automation cadence is the scheduler. Farplane does not add a hidden scheduler,
daemon, compiler, or Steer thread between `farplane/automations.md` and the
Codex app automation records.

## Principle

Use the smallest explicit loop that preserves useful context isolation:

- Pulse is the fast executor loop. It reconciles outcomes, admits ready
  tickets, executes parallelizable work up to policy cap, writes planning
  requests when no executable work exists, and records the decision.
- Daily Interval reviews the last 24 hours, writes a dated report, reads the
  latest weekly interval output through configured context refs, and plans the
  next 24 hours.
- Weekly Interval reviews the last week, writes a dated report, reads daily
  interval outputs inside the review window through configured context refs,
  checks drift against goals, scores leverage opportunities when enabled, and
  plans the next week.
- Files are the shared memory. Loops should not depend on shared transcript
  context.
- Longer horizons become explicit interval automations only after repeated
  weekly reports prove they produce useful decisions often enough to deserve
  their own cadence and thread.

## Adoption Thresholds

Use no automation when a project is still a one-off setup, exploratory note, or
human-driven spike with no recurring action expectation.

Use Pulse when the project has proceedable tickets, open loops, or outcome
ledgers that benefit from frequent execution. Pulse is appropriate when a
30-minute to few-hour cadence can produce value without replanning the whole
project. If the board is empty or stale, Pulse writes a planning request; Daily
or Weekly Interval owns creating, splitting, or reprioritizing work.

Use interval automations when the project needs reports, drift checks, or
bounded replanning. Daily and weekly are the default because they create a
human-readable daily digest and a weekly strategy reset without forcing every
interval through another scheduler.

Use all three when the project should run autonomously: Weekly Interval updates
direction, Daily Interval keeps the immediate plan current, and Pulse turns
current direction into bounded action.

## Activation Critical Path

Project bootstrap and live automation activation are separate phases.

```text
init_advisor(...)
  -> files + automations.md + pm_manifest

automation_advisor(activate=true, project_ref)
  -> pulse_thread + codex_automations + pm_json_thread_group_delta
```

Critical path:

1. Scaffold the project files with `init-advisor`.
2. Create or verify `farplane/automations.md` with the exact Pulse, Daily
   Interval, and Weekly Interval prompts to copy into Codex automations.
3. Create or verify `farplane/pm.json` as UI grouping glue with
   `threads.chats` and `threads.automations`.
4. Use `horizon-advisor` to shape `farplane/goals.md` when project goals are
   missing, placeholder, or stale.
5. Use `goal-advisor` to compile the first executable frontier into a
   ticket-backed Goal Packet when the goals are actionable.
6. Use `automation-advisor` to prepare the live Codex automation prompts.
7. When the operator requests live automation activation, create or reuse the
   dedicated `Project Pulse` thread.
8. Attach the Pulse heartbeat automation to the Pulse thread at the fast idle
   cadence.
9. Create or update standalone Codex cron automations for Daily Interval and
   Weekly Interval at their configured cadences.
10. Append PM-visible thread IDs and automation IDs to `farplane/pm.json` only
    when they should render under the persistent PM employee.
11. When Pulse creates persistent PM-owned ticket or worker chat threads,
    append those thread IDs to `farplane/pm.json` `threads.chats`.

When the Codex app automation tools are unavailable, write the prompt templates
and report `needs_automation_setup` instead of pretending activation happened.

Activation is idempotent: inspect existing project automation threads and
automations first, update matches, and create only missing pieces. The
canonical UI grouping writeback is `farplane/pm.json`; automation runtime IDs
belong in the Codex app automation store, not in `pm.json`.

## Risk Guards

- `duplicate_loops:` do not create duplicate automations for the same loop and
  cadence unless a separate ticket explicitly changes the project standard.
- `placeholder_goals:` do not activate autonomous loops when `farplane/goals.md`
  is still placeholder, stale, or not grounded in the operator's intent; report
  `needs_goal_intake`.
- `tool_unavailable:` if Codex thread or automation tools are unavailable,
  produce prompts and report `needs_automation_setup`.
- `thread_confusion:` each context-isolated recurring loop gets a dedicated
  named thread when thread-attached heartbeats are used.
- `state_confusion:` PM-visible thread grouping lives in `farplane/pm.json`;
  automation cadence/runtime IDs live in the Codex app automation store; Pulse
  decision/reward state lives under `.farplane/automation/`; interval outputs
  live under `.farplane/reports/interval/`.
- `pm_worker_threads:` when Pulse creates persistent ticket or worker chat
  threads that should belong to the project PM employee, append the IDs to
  `farplane/pm.json` `threads.chats`.

## Pulse Execution State

Pulse is an admission and execution loop. Planner-level reward learning may
later use ticket outcomes to adjust work-lane distribution, but Pulse itself
does not own strategy arms or product-lane exploration.

Ignored runtime state:

```text
.farplane/automation/decisions.jsonl
  -> each Pulse execution mode, admitted or excluded tickets, reason, and expected reward

.farplane/automation/rewards.jsonl
  -> reconciled reward observations from worker outcomes

.farplane/automation/action-outcomes.jsonl
  -> normalized outcomes for ticket, QA, planning, or metadata actions

.farplane/automation/spawned-threads.jsonl
  -> child thread IDs, context refs, expected proof, and reward horizon
```

Default execution modes:

- `execute_ready_tickets`
- `repair_ticket_admission_state`
- `request_planning`
- `no_op_blocked`

## Interval Reports

Reports are dated records, not mutable `latest.md` files:

```text
.farplane/reports/pulse/<YYYY-MM-DDTHHMMSSZ>.md
.farplane/reports/interval/<interval_id>/<YYYY-MM-DDTHHMMSSZ>.md
```

Consumers find the newest interval report by timestamp sorting or by explicit
links written in later reports. No tracked config file exists solely to store
`last_report`.

Project-configured intervals:

```text
daily_interval:
  review_window: last_24h
  planning_window: next_24h
  Reads:
    - default interval refs
    - farplane/products.md work lanes
    - latest weekly_interval report as parent_weekly_plan

weekly_interval:
  review_window: last_week
  planning_window: next_week
  Reads:
    - default interval refs
    - farplane/products.md work lanes
    - farplane/goals.md
    - daily_interval reports inside last_week as daily_reports
  Runs:
    - plan_progress
    - codex_attention_drift
    - ticket_board_drift
    - goal_drift
    - compounding_leverage_review
    - learning_backpropagation
    - priority_planning
```

## Goals Delta And Self-Update

Weekly Interval may propose goals deltas, but it must report before mutation.
It classifies each delta:

- `auto_apply`: minor evidence-backed source/current-signal/stale-label updates
  when policy allows.
- `approval_required`: north-star, KPI, strategy-axis, priority, hold,
  quarterly/yearly, stop-condition, or durable milestone changes.
- `rejected_source_gap`: insufficient evidence; create a source, research,
  feedback, metric, or ticket proposal instead.

Approval path:

```text
weekly_interval_report
  -> goals_delta_candidates
  -> operator accepts or asks horizon-advisor to apply material strategy delta
  -> farplane/goals.md update
  -> goal-advisor compiles selected executable bets
  -> Pulse executes ready tickets
  -> reports/rewards feed the next interval
```

When `compounding_leverage_review` is enabled, Weekly Interval also scores
Farplane improvement levers and chooses 1-3 next-window bets. `leverage-advisor`
scores value; `harness-advisor` chooses the owner surface; `goal-advisor`
compiles selected execution; Pulse executes ready tickets after planners create
them.

Use the advisor matrix instead of inventing hidden orchestration:

| Question | Owner |
| --- | --- |
| Should goals, KPI tree, value function, or frontier change? | `horizon-advisor` |
| Which existing capability compounds fastest? | `leverage-advisor` |
| Where should the change live? | `harness-advisor` |
| What proof surface should judge the claim? | `proof-advisor` |
| Is this a new reusable skill? | `skill-creator` |
| Does an existing skill need backpropagation? | `skill-maintenance` |
| Does the coding bet need a plan/proof contract? | `impl-plan` |
| Is selected execution ready to run? | `goal-advisor` |
| Is the full harness behavior gap the task? | `optimize-harness` |

Before selecting new leverage bets, Weekly Interval closes reward signals from
prior selected bets in the dated report:

```text
previous_weekly_interval_report
  -> selected leverage bets + reward signals
  -> current weekly reward closure
  -> accept | continue | kill | resize | source_gap
  -> next selected bets
```

Leverage signals are evidence extracted from existing artifacts: reports,
tickets, skill or feature registry changes, evals, troubles, lessons, feedback,
metrics, opportunity refs, or supplied external source refs. Do not create a
separate leverage backlog by default; write selected/rejected/deferred/expired
decisions into the dated interval report.

Weekly scores are reasoning aids, not blind telemetry. The report may summarize
signals such as accepted output, accepted agent-hours, intervention minutes,
false-completion incidents, context-isolation failures, source gaps,
proof-closure rate, and skill-backpropagation events, but the final choice must
cite the evidence and explain why the selected bets reduce a named loss term.

An urgent signal may bypass weekly selection only when it is high-confidence,
source-backed, names an explicit loss term, includes a review-by date, and has
a clear owner route. Urgent escalation may create a report, ticket, Goal
Advisor handoff, or approval request; it must not mutate strategy directly.

## Migration Rule

The old daily, weekly, rhythm, heartbeat, ticket-drainer, and Steer scheduler
packages are retired as active surfaces. Their useful practices live in
`pulse-update`, `interval-update`, and project automation prompts.

The active model is:

- `pulse-update` owns the fast executor loop, ready-ticket admission,
  child-thread handoffs, reward state, planning requests, and outcome
  reconciliation.
- `interval-update` owns report-before-plan interval review, drift checks,
  work-lane distribution, goals-delta promotion, next-window plans, Pulse
  guidance, and Goal Advisor handoffs.
- `automation-advisor` owns prompt authoring and live Codex automation setup.

Do not recreate legacy cadence skills, a separate ticket-drainer automation, or
a Steer scheduler/orchestrator unless a future ticket proves explicit Codex
automations cannot hold the work.
