---
name: interval-update
description: "Run one Farplane interval automation: review the past window, write a dated report, plan the next window, and emit Pulse or Goal Advisor guidance."
tier: 3
group: harness
source: local
template_uses:
  skill-template: "0.2.0"
  skill-eval-task: "0.1.0"
eval: eval_task.json
allowed-tools: Read, Glob, Grep, Bash

---

# Interval Update

## Context

Use this skill for one scheduled Farplane interval automation. The Codex app
owns cadence by running separate automations, such as Daily Interval and Weekly
Interval. This skill owns the shared report-then-plan workflow for a single
window.

Default presets:

- `daily_interval`: review the last 24 hours, plan the next 24 hours, and use
  the latest weekly interval report as parent context when present.
- `weekly_interval`: review the last week, plan the next week, and use goals
  plus daily reports from the review window as context.

Do not wrap this skill in a hidden scheduler thread. If a project needs another
cadence, create another explicit automation that calls this skill with a named
interval, review window, planning window, and small additive extensions.

## Skill Signature

```text
interval_update(project_root, interval_id, review_window, planning_window, extensions?, now?)
  -> context_bundle
   + source_gaps
   + interval_report
   + drift_findings
   + next_window_plan
   + pulse_guidance
   + ticket_deltas
   + goals_delta?
   + goal_advisor_handoffs?

state:
  reads(farplane/goals.md?,
        tickets/,
        docs/HISTORY.md?,
        docs/MEMORY.md?,
        docs/LESSONS.md?,
        docs/TROUBLES.md?,
        .farplane/reports/pulse/?,
        .farplane/reports/interval/?,
        farplane/pm.json?,
        worker thread refs when available)
  writes(.farplane/reports/interval/<interval_id>/<YYYY-MM-DDTHHMMSSZ>.md,
         optional .farplane/reports/interval/<interval_id>/context/<YYYY-MM-DDTHHMMSSZ>.md,
         farplane/goals.md only through explicit goals-delta policy)

gates:
  defaults_resolved; extensions_merged; review_window_bound;
  context_bundle_written_or_summarized; report_written_before_plan_or_goals_mutation;
  drift_checked; next_window_plan_written; side_effect_gates_respected;
  date_stamped_report_used

routes:
  pulse-update | goal-advisor | feed-scout | update-memory |
  update-strategy | skill-maintenance | review

fails:
  selecting due jobs; writing scheduler state; mutating tracked cadence config;
  making automations restate default Farplane paths; using latest.md as
  canonical report; spawning broad leaf work; changing goals without
  report-first goals-delta evidence
```

## Default Resolution

Resolve this standard context for every Farplane project:

```text
default_context_refs(project_root, interval_id) = {
  goals_ref: farplane/goals.md,
  ticket_refs: tickets/,
  memory_refs: [docs/MEMORY.md, docs/HISTORY.md, docs/LESSONS.md, docs/TROUBLES.md],
  pulse_report_refs: .farplane/reports/pulse/**,
  interval_report_refs: .farplane/reports/interval/**,
  report_root: .farplane/reports/interval/<interval_id>,
  context_bundle_root: .farplane/reports/interval/<interval_id>/context
}
```

Default presets:

```text
daily_interval:
  review_window: last_24h
  planning_window: next_24h
  parent_plan_ref: latest weekly_interval report when present

weekly_interval:
  review_window: last_week
  planning_window: next_week
  parent_plan_ref: farplane/goals.md
  daily_report_refs: daily_interval reports inside review_window
```

`extensions` may add context refs, phase instructions, analysis lanes, or
policy details. Missing extensions mean use the default Farplane behavior.
Use [references/interval-update.md](references/interval-update.md) for the
extension merge contract and goals-delta policy.

<!-- BEGIN FARPLANE_IMPORTANT_CHECKLIST -->
## Todo List

- [ ] 1. Bind the interval invocation.
  - [ ] Resolve `project_root`.
  - [ ] Bind `interval_id`, `review_window`, and `planning_window`.
  - [ ] Load additive `extensions` only when the automation supplies them.
- [ ] 2. Resolve default context.
  - [ ] Build default refs for goals, tickets, memory, Pulse reports, interval
        reports, PM thread grouping, and worker outcome refs.
  - [ ] Add daily parent weekly-plan context or weekly daily-report context
        from the preset.
  - [ ] Merge extension refs without making the caller restate default
        Farplane paths.
  - [ ] Label missing or stale sources as source gaps.
- [ ] 3. Review the past window.
  - [ ] Summarize tickets, Pulse decisions, worker outcomes, blockers,
        failures, file/doc changes, and human feedback inside `review_window`.
  - [ ] Check drift against the relevant parent context: latest weekly plan for
        daily intervals, goals and daily reports for weekly intervals.
- [ ] 4. Write the report before durable mutations.
  - [ ] Write a date-stamped interval report.
  - [ ] Include source gaps, drift findings, evidence, and the proposed next
        plan before mutating goals or tickets.
  - [ ] Use goals-delta promotion before changing `farplane/goals.md`.
- [ ] 5. Emit next-window guidance.
  - [ ] Produce a plan sized to `planning_window`.
  - [ ] Convert executable work into ticket deltas or Goal Advisor handoffs.
  - [ ] Return Pulse guidance as constraints for the fast action loop.
  - [ ] Summarize report paths, blockers, goals-delta decisions, and handoffs.
<!-- END FARPLANE_IMPORTANT_CHECKLIST -->

## Output

- interval id and windows.
- report paths.
- source gaps.
- drift findings.
- next-window plan.
- goals delta decisions or approval-required blockers.
- Pulse guidance.
- Goal Advisor handoffs or ticket deltas.

## Reference Map

- [templates/daily-interval.md](templates/daily-interval.md) - default daily
  interval preset.
- [templates/weekly-interval.md](templates/weekly-interval.md) - default weekly
  interval preset.
- [references/interval-update.md](references/interval-update.md) - interval
  planning, default context refs, extension merge rules, and goals-delta
  promotion.
- [templates/interval-context-bundle.md](templates/interval-context-bundle.md)
  - default interval context bundle.
- [templates/interval-report.md](templates/interval-report.md) - default
  interval report.
- [../../docs/specs/steer-pulse-automation.md](../../docs/specs/steer-pulse-automation.md)
