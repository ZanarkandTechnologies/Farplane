---
name: steer-update
description: "Run the Farplane planning loop: write interval reports, run weekly or triggered replanning, check drift, and give Pulse guidance."
tier: 3
group: harness
source: local
template_uses:
  skill-template: "0.2.0"
  skill-eval-task: "0.1.0"
eval: eval_task.json
allowed-tools: Read, Glob, Grep, Bash

---

# Steer Update

## Context

Use this skill for the Farplane Steer loop: report compression, drift checks,
scrum-style interval reflection, weekly planning, and long-horizon rollups.
Steer is the planning counterpart to `pulse-update`; it should not become a
fast action loop or hidden scheduler daemon.

The common project shape is one Steer automation with a daily report interval
and a weekly plan interval. Triggers such as an empty board, repeated failure,
major blocker, human feedback, or goal drift may pull the planning pass forward.
Steer can receive a schedule from the automation prompt or a helper config, but
the hot path should stay simple: compare `now` to the stored next report/plan
timestamps, run due work, then advance state.

## Skill Signature

```text
steer_update(project_root, report_interval, plan_interval, plan_triggers, scheduler_state, now)
  -> due_reports
   + due_plans
   + interval_reports
   + drift_findings
   + goals_delta?
   + pulse_guidance
   + scheduler_state_delta

state:
  reads(schedule params from caller or farplane/steer.config.json?,
        .farplane/state/steer-scheduler.json?,
        farplane/goals.md?,
        tickets/,
        docs/MEMORY.md?,
        docs/LESSONS.md?,
        docs/TROUBLES.md?,
        .farplane/reports/pulse/?)
  writes(.farplane/reports/steer/<job>/<YYYY-MM-DDTHHMMSSZ>.md,
         .farplane/state/steer-scheduler.json,
         farplane/goals.md only through explicit goals-delta policy)

gates:
  config_loaded; scheduler_state_loaded_or_initialized;
  config_version_reconciled; due_reports_selected_by_next_due_at;
  due_plans_selected_by_next_due_at_or_trigger; drift_checked; dated_reports_written;
  state_updated_without_config_mutation; side_effect_gates_respected

routes:
  pulse-update | goal-advisor | feed-scout | update-memory |
  update-strategy | skill-maintenance | review

fails:
  mutating tracked config during a normal run; recalculating all job schedules
  every beat; using latest.md as canonical report; spawning broad leaf work;
  changing goals without report-first goals-delta evidence
```

<!-- BEGIN FARPLANE_IMPORTANT_CHECKLIST -->
## Todo List

- [ ] 1. Load config and state.
  - [ ] Read the report interval, plan interval, plan triggers, and schedule
        passed by the caller, or `farplane/steer.config.json` only when the
        caller uses that helper file.
  - [ ] Read `.farplane/state/steer-scheduler.json` if present.
  - [ ] If state is missing or schedule version changed, initialize/migrate
        state from configured jobs without mutating the caller's config source.
- [ ] 2. Select due reports and plans.
  - [ ] Get the current date/time.
  - [ ] Select the report workflow when `now >= next_report_due_at`.
  - [ ] Select the plan workflow when `now >= next_plan_due_at` or a plan
        trigger is genuinely hit.
  - [ ] If nothing is due, write a compact no-due summary and avoid broad
        planning.
- [ ] 3. Run each due workflow.
  - [ ] For report due: summarize the last interval, blockers, repeated misses,
        stale context, missing evidence, and lightweight Pulse guidance.
  - [ ] For plan due or triggered: read recent reports and goals, reflect
        scrum-style, check drift, and use goal-advisor when direction should
        become executable tickets or a Goal Packet.
- [ ] 4. Write reports before durable mutations.
  - [ ] Write a date-stamped report for the job.
  - [ ] Use goals-delta promotion before mutating `farplane/goals.md`.
  - [ ] Convert executable work into tickets or Goal Advisor handoffs unless
        the job explicitly permits a bounded direct change.
- [ ] 5. Advance scheduler state.
  - [ ] Set `last_report_run_at`, `last_report`, `report_status`, and
        `next_report_due_at` when the report workflow runs.
  - [ ] Set `last_plan_run_at`, `last_plan_report`, `plan_status`, and
        `next_plan_due_at` when the planning workflow runs.
  - [ ] Save scheduler state only.
  - [ ] Summarize due reports, due plans, skipped work, blockers, and next due
        times.
<!-- END FARPLANE_IMPORTANT_CHECKLIST -->

## Output

- due reports/plans and skipped work.
- report paths.
- drift findings.
- goals delta decisions or approval-required blockers.
- Pulse guidance.
- scheduler state delta.

## Reference Map

- [templates/daily-plan.md](templates/daily-plan.md)
- [templates/daily-report.md](templates/daily-report.md)
- [templates/strategy-review.md](templates/strategy-review.md)
- [../../docs/specs/steer-pulse-automation.md](../../docs/specs/steer-pulse-automation.md)
