---
title: "Steer and Pulse Automation"
status: active
owner: farplane-framework
created_at: 2026-06-23
updated_at: 2026-06-23
tags:
  - farplane
  - automations
  - steer
  - pulse
refs:
  - farplane/steer.config.toml
  - skills/steer-update/SKILL.md
  - skills/pulse-update/SKILL.md
  - skills/automation-advisor/SKILL.md
---

# Steer and Pulse Automation

Farplane projects run autonomously through two framework loops:

```text
pulse_update(project, board_state, action_tree, reward_state)
  -> one bounded action + decision state

steer_update(project, report_interval, plan_interval, plan_triggers, scheduler_state)
  -> due reports/plans + date-stamped reports + scheduler state delta
```

Pulse and Steer are framework primitives, not project-specific inventions. A
project may start without enabling them, but once the goal is repeated
autonomous progress, these are the two default loops.

## Principle

Use the smallest loop that preserves useful context isolation:

- Pulse is the fast actor/idle loop. It reconciles outcomes, uses reasoning
  plus bandit state to select one board/action-tree move, spawns a bounded
  worker when useful, and records the decision.
- Steer is the PM/scrum loop. It writes daily report compression for the human,
  gathers recent ticket and report changes, performs drift checks against
  goals, reflects scrum-style on the last interval, and replans weekly or when
  a real trigger appears.
- Files are the shared memory. Pulse and Steer should not depend on shared
  transcript context.
- Codex automations are the runner. Farplane does not add a hidden scheduler,
  daemon, or compiler between the project files and Codex automations.

## Adoption Thresholds

Use no automation when a project is still a one-off setup, exploratory note, or
human-driven spike with no recurring action expectation.

Use Pulse when the project has proceedable tickets, open loops, or outcome
ledgers that benefit from frequent small decisions. Pulse is appropriate when a
30-minute to few-hour cadence can produce value without replanning the whole
project. If the board is empty, Pulse chooses one narrow action-tree arm; it
does not automatically call Goal Advisor.

Use Steer when the project has goals, strategy, recurring planning needs,
daily status reports, or checks that should not share Pulse's action context.
Steer is appropriate when the project needs a report interval, a plan interval,
and triggered replanning without separate persistent threads for each cadence.

Use both when the project should run autonomously: Steer updates direction and
drift; Pulse turns current direction into bounded action.

## Activation Critical Path

Project bootstrap and live automation activation are separate phases.

```text
deep_init_project(...)
  -> files + steer_config + scheduler_state + pm_manifest

automation_advisor(activate=true, project_ref)
  -> pulse_thread + steer_thread + pulse_automation + steer_automation + pm_json_thread_group_delta
```

Critical path:

1. Scaffold the project files with `deep-init-project`.
2. Create or verify `farplane/automations.md` with the exact Pulse and Steer
   prompts to copy into Codex automations.
3. Create or verify `.farplane/state/steer-scheduler.json`.
4. Create or verify `farplane/pm.json` as UI grouping glue with
   `threads.chats` and `threads.automations`.
5. Use `horizon-advisor` to shape `farplane/goals.md` when project goals are
   missing, placeholder, or stale.
6. Use `goal-advisor` to compile the first executable frontier into a
   ticket-backed Goal Packet when the goals are actionable.
7. Use `automation-advisor` to prepare the live Codex automation prompts.
8. When the operator requests live automation activation, create two dedicated
   project threads:
   - `Project Pulse`
   - `Project Steer`
9. Attach the Pulse automation to the Pulse thread at the fast idle cadence.
10. Attach the Steer automation to the Steer thread at the minimum planning
   cadence.
11. Append the visible Pulse/Steer thread IDs to `farplane/pm.json` so the UI
    renders them under the persistent PM employee.
12. When Pulse or Steer creates persistent PM-owned ticket or worker chat
    threads, append those thread IDs to `farplane/pm.json` `threads.chats`.

Do not create extra threads for daily, weekly, quarterly, yearly, ticket
draining, or strategy review jobs. Those are Steer jobs or Pulse actions.

When the Codex app automation tools are unavailable, write the prompt templates
and report `needs_automation_setup` instead of pretending activation happened.

Activation is idempotent: inspect existing project Pulse/Steer threads and
automations first, update matches, and create only missing pieces. The
canonical UI grouping writeback is `farplane/pm.json`; automation runtime IDs
belong in the Codex app automation store, not in `pm.json`.

## Risk Guards

- `duplicate_loops:` do not create more than one Pulse and one Steer loop per
  project unless a separate ticket explicitly changes the framework standard.
- `placeholder_goals:` do not activate autonomous loops when `farplane/goals.md`
  is still placeholder, stale, or not grounded in the operator's intent; report
  `needs_goal_intake`.
- `tool_unavailable:` if Codex thread or automation tools are unavailable,
  produce prompts and report `needs_automation_setup`.
- `thread_confusion:` Pulse and Steer get dedicated named threads when
  thread-attached heartbeats are used; daily/weekly/quarterly jobs do not get
  separate threads.
- `state_confusion:` tracked config stores job prompts and cadence only;
  PM-visible thread grouping lives in `farplane/pm.json`; automation runtime
  IDs live in the Codex app automation store; run timestamps live in
  `.farplane/state/steer-scheduler.json`.
- `pm_worker_threads:` when Pulse or Steer creates persistent ticket or worker
  chat threads that should belong to the project PM employee, append the IDs to
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

`consult_goal_advisor` is selected only when the empty board is caused by
unclear goals, an unclear milestone, or missing executable Goal Packets.

## Steer Schedule State

The preferred Steer model is one automation prompt with:

```text
report_interval = daily
plan_interval = weekly
plan_triggers = empty_board | repeated_failure | major_blocker |
                human_feedback | goal_drift
```

Tracked config, when present, is human-owned and intentionally small:

```text
farplane/steer.config.toml
  -> version, timezone, report_interval, plan_interval, plan_triggers,
     and any project-specific prompt overrides
```

Mutable scheduler state is ignored:

```text
.farplane/state/steer-scheduler.json
  -> config_version, last_report_run_at, next_report_due_at,
     last_plan_run_at, next_plan_due_at, last_report, last_plan_report,
     last_status
```

Keep the Steer config easy for a human to edit. A job is present only when it
should run. The job prompt may point at skills or workflow templates, but the
config should not duplicate their inputs, outputs, drift checks, reports, or
side-effect gates.

## Steer Due Check

```text
now = current_time()
load schedule from automation prompt or farplane/steer.config.toml
load .farplane/state/steer-scheduler.json

if state.config_version != config.version:
  initialize_or_migrate_state(config, state)

report_due = now >= state.next_report_due_at
plan_due = now >= state.next_plan_due_at or plan_trigger_hit

if report_due:
  write daily report
  update last_report_run_at, last_report, next_report_due_at

if plan_due:
  run weekly steering
  write steering report
  update last_plan_run_at, last_plan_report, next_plan_due_at

save scheduler state only
```

The hot path is timestamp comparison plus trigger detection. Recurrence
calculation happens only when a workflow runs or when state is initialized from
a new config version.

## Report Naming

Reports are dated records, not mutable `latest.md` files:

```text
.farplane/reports/steer/<job>/<YYYY-MM-DDTHHMMSSZ>.md
.farplane/reports/pulse/<YYYY-MM-DDTHHMMSSZ>.md
```

State files store `last_report` pointers when a loop needs the newest report.

## Migration Rule

The old daily, weekly, rhythm, horizon, heartbeat, and ticket-drainer packages
are migration sources until their useful practices have been moved into Steer
and Pulse. They should not remain the active framework model.

Do not delete a legacy planning skill only because the new loop exists. First
extract report-before-mutation, goals-delta promotion, ticket selection,
outcome reconciliation, and source-gap labeling practices into the new skills
or templates.
