---
title: "Interval Update Workflow"
status: active
owner: interval-update
kind: reference
---

# Interval Update Workflow

`interval_update` is the generic Farplane report-then-plan primitive. Use it
when one explicit Codex automation needs to review a bounded window, check
drift, write a report, plan the next bounded window, and give guidance to
Pulse, Goal Advisor, or ticket creation.

```text
interval_update(project_root, interval_id, review_window, planning_window, extensions?)
  -> context_bundle
   + source_gaps
   + interval_report
   + drift_check
   + next_window_plan
   + downstream_guidance
   + ticket_deltas
   + proposed_goals_delta?
   + applied_goals_delta?
   + approval_required_goals_delta?
   + goal_advisor_handoffs?
```

## Default Context Refs

The skill resolves these for every Farplane project unless an extension adds or
replaces a source:

```text
default_context_refs(project_root, interval_id) = {
  goals_ref: project_root/farplane/goals.md,
  ticket_refs: project_root/tickets/,
  memory_refs: [
    project_root/docs/MEMORY.md,
    project_root/docs/HISTORY.md,
    project_root/docs/LESSONS.md,
    project_root/docs/TROUBLES.md
  ],
  pulse_report_refs: project_root/.farplane/reports/pulse/**,
  interval_report_refs: project_root/.farplane/reports/interval/**,
  report_root: project_root/.farplane/reports/interval/<interval_id>,
  context_bundle_root: project_root/.farplane/reports/interval/<interval_id>/context,
  pm_manifest_ref: project_root/farplane/pm.json
}
```

For `daily_interval`, add:

```text
review_window: last_24h
planning_window: next_24h
parent_plan_ref: latest weekly_interval report from .farplane/reports/interval/weekly_interval/
daily_report_refs: none
```

For `weekly_interval`, add:

```text
review_window: last_week
planning_window: next_week
daily_report_refs: daily_interval reports inside review_window
parent_plan_ref: goals_ref
```

## Extensions

Use `extensions`, not overrides. Extensions add to the default Farplane shape;
they do not make every project restate common paths.

```text
IntervalExtensions = {
  timezone?: string,
  context_extensions?: {
    extra_refs?: [ref],
    replace_refs?: { <default_ref_name>: ref | [ref] }
  },
  phase_extensions?: {
    before_context_load_append?,
    context_collection_append?,
    after_context_bundle_append?,
    analysis_lanes_append?,
    synthesis_append?,
    report_format_append?,
    writeback_candidates_append?
  },
  policy_extensions?: {
    goals_delta_policy?,
    side_effect_gates?,
    report_shape?
  }
}
```

Rules:

- Missing extensions mean use the default Farplane behavior.
- `extra_refs` are additive. Use `replace_refs` only when a project truly has a
  non-standard source of truth.
- Phase extensions append project-specific instructions to the default
  interval behavior. They cannot skip source-gap labels,
  report-before-goals-mutation, goals-delta promotion, side-effect gates, or
  leaf-execution avoidance.
- Project/person/customer/private paths belong in the project automation file,
  project docs, or bindings passed through extensions; never in generic skill
  first-load refs.

## Workflow

1. Bind `interval_id`, `review_window`, `planning_window`, report profile, and
   merged context refs.
2. Run `before_context_load_append` only to refine source plans and gates.
3. Read default refs plus extension refs; label missing or stale sources.
4. Normalize evidence into
   [interval-context-bundle.md](../templates/interval-context-bundle.md).
5. Run any lane or analysis extensions against the context bundle path.
6. Review the past window:
   - daily: compare actual work against the latest weekly interval plan when
     present.
   - weekly: compare daily reports and outcomes against goals.
7. Write [interval-report.md](../templates/interval-report.md) before any
   goals mutation.
8. Plan the next window, sized to `planning_window`.
9. Classify every goals delta as `auto_apply`, `approval_required`, or
   `rejected_source_gap`.
10. Convert executable changes into ticket deltas or Goal Advisor handoffs.
11. Return downstream guidance so Pulse gets the next constraints.

## Goals Delta Promotion

The skill may update `farplane/goals.md` only after the interval report
contains a `Goals Delta` block with evidence and a promotion decision.

```text
apply_goals_delta(proposed_goals_delta, policy)
  -> goals.md patch | approval_required | rejected_source_gap
```

Promotion decisions:

- `auto_apply`: source refs, current-signal notes, stale labels, or minor
  milestone wording backed by clear evidence.
- `approval_required`: north star, KPI, strategy axis, project priority, hold,
  stop condition, quarterly goal, yearly goal, or durable milestone changes.
- `rejected_source_gap`: insufficient evidence; create an instrumentation,
  access, feedback, or research ticket instead.

Quarterly, yearly, and other intervals greater than one week should normally
be represented as explicit interval automations only when they produce useful
decisions often enough to deserve their own thread and cadence. Otherwise, the
weekly interval can create a ticket or Goal Advisor handoff for the longer
horizon review.
