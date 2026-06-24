---
title: "Pulse and Interval Automation"
status: active
owner: farplane-framework
created_at: 2026-06-23
updated_at: 2026-06-24
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
  -> one bounded action + decision state

interval_update(project_root, interval_id, review_window, planning_window, extensions?, now?)
  -> dated interval report + next-window plan + Pulse guidance
```

The default project set is Pulse, Daily Interval, and Weekly Interval. Codex
automation cadence is the scheduler. Farplane does not add a hidden scheduler,
daemon, compiler, or Steer thread between `farplane/automations.md` and the
Codex app automation records.

## Principle

Use the smallest explicit loop that preserves useful context isolation:

- Pulse is the fast actor/idle loop. It reconciles outcomes, uses reasoning
  plus bandit state to select one board/action-tree move, spawns a bounded
  worker when useful, and records the decision.
- Daily Interval reviews the last 24 hours, writes a dated report, compares
  against the latest weekly plan when available, and plans the next 24 hours.
- Weekly Interval reviews the last week, writes a dated report, checks drift
  against `farplane/goals.md`, and plans the next week.
- Files are the shared memory. Loops should not depend on shared transcript
  context.
- Longer horizons become explicit interval automations only after repeated
  weekly reports prove they produce useful decisions often enough to deserve
  their own cadence and thread.

## Adoption Thresholds

Use no automation when a project is still a one-off setup, exploratory note, or
human-driven spike with no recurring action expectation.

Use Pulse when the project has proceedable tickets, open loops, or outcome
ledgers that benefit from frequent small decisions. Pulse is appropriate when a
30-minute to few-hour cadence can produce value without replanning the whole
project. If the board is empty, Pulse chooses one narrow action-tree arm;
`consult_goal_advisor` is one option, not the default.

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
deep_init_project(...)
  -> files + automations.md + pm_manifest

automation_advisor(activate=true, project_ref)
  -> loop_threads + codex_automations + pm_json_thread_group_delta
```

Critical path:

1. Scaffold the project files with `deep-init-project`.
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
   dedicated project threads named by `farplane/automations.md`, commonly:
   - `Project Pulse`
   - `Project Daily Interval`
   - `Project Weekly Interval`
8. Attach each Codex automation to the matching thread at the named cadence.
9. Append visible loop thread IDs to `farplane/pm.json` so the UI renders them
   under the persistent PM employee.
10. When Pulse creates persistent PM-owned ticket or worker chat threads,
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

## Pulse Action State

Pulse combines reasoning with a weak memory prior. The bandit state is useful
because it remembers which action arms have recently paid off, but it is not a
replacement for judgment.

Ignored runtime state:

```text
.farplane/automation/bandit-state.json
  -> action arm scores, counts, uncertainty, and last update

.farplane/automation/decisions.jsonl
  -> each Pulse decision, selected arm, reason, and expected reward

.farplane/automation/rewards.jsonl
  -> reconciled reward observations from worker outcomes

.farplane/automation/action-outcomes.jsonl
  -> normalized outcomes for ticket, QA, planning, or metadata actions

.farplane/automation/spawned-threads.jsonl
  -> child thread IDs, context refs, expected proof, and reward horizon
```

Default action arms:

- `pick_ready_ticket`
- `split_oversized_ticket`
- `clarify_blocker`
- `create_prep_ticket`
- `run_qa_or_eval`
- `refresh_ticket_metadata`
- `consult_goal_advisor`
- `no_op_unsafe`

## Interval Reports

Reports are dated records, not mutable `latest.md` files:

```text
.farplane/reports/pulse/<YYYY-MM-DDTHHMMSSZ>.md
.farplane/reports/interval/<interval_id>/<YYYY-MM-DDTHHMMSSZ>.md
```

Consumers find the newest interval report by timestamp sorting or by explicit
links written in later reports. No tracked config file exists solely to store
`last_report`.

Default intervals:

```text
daily_interval:
  review_window: last_24h
  planning_window: next_24h
  parent_context: latest weekly_interval report when present

weekly_interval:
  review_window: last_week
  planning_window: next_week
  parent_context: farplane/goals.md + daily_interval reports in review_window
```

## Migration Rule

The old daily, weekly, rhythm, heartbeat, ticket-drainer, and Steer scheduler
packages are retired as active surfaces. Their useful practices live in
`pulse-update`, `interval-update`, and project automation prompts.

The active model is:

- `pulse-update` owns the fast idle loop, ticket selection, child-thread
  handoffs, bandit/reward state, and outcome reconciliation.
- `interval-update` owns report-before-plan interval review, drift checks,
  goals-delta promotion, next-window plans, Pulse guidance, and Goal Advisor
  handoffs.
- `automation-advisor` owns prompt authoring and live Codex automation setup.

Do not recreate legacy cadence skills, a separate ticket-drainer automation, or
a Steer scheduler/orchestrator unless a future ticket proves explicit Codex
automations cannot hold the work.
