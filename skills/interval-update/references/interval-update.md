---
title: "Interval Update Workflow"
status: active
owner: interval-update
kind: reference
---

# Interval Update Workflow

`interval_update` is the generic Farplane report-then-plan primitive. Use it
when one explicit Codex automation needs to review a configured bounded window,
check drift against configured context, write a report, plan the next bounded
window, and give guidance to Pulse, Goal Advisor, or ticket creation.

```text
interval_update(project_root, interval_id, review_window, planning_window,
                context_refs?, report_workflows?, planning_policy?,
                write_policy?)
  -> context_bundle
   + source_gaps
   + interval_report
   + workflow_findings
   + drift_findings
   + next_window_plan
   + downstream_guidance
   + ticket_deltas
   + proposed_goals_delta?
   + applied_goals_delta?
   + approval_required_goals_delta?
   + goal_advisor_handoffs?
```

## Default Context Refs

The skill resolves these for every Farplane project unless `context_refs`
adds or replaces a source:

```text
default_context_refs(project_root, interval_id) = {
  harness_ref: project_root/farplane/harness.md,
  products_ref: project_root/farplane/products.md,
  local_product_skill_refs: project_root/.agents/skills/**/SKILL.md,
  goals_ref: project_root/farplane/goals.yaml,
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

## Configurable Context Refs

Callers use `context_refs` to wire interval-to-interval dependencies. This is
where one interval can say "read the latest report from another interval" or
"read another interval's reports inside this review window." The skill only
knows how to resolve the selectors.

```text
context_refs = {
  extra_refs?: [ref],
  parent_context_refs?: [ref],
  workflow_refs?: {
    telemetry_refs?: [ref],
    feedback_refs?: [ref],
    opportunity_refs?: [ref],
    metric_refs?: [ref],
    status_refs?: [ref]
  },
  interval_output_refs?: [
    {
      interval_id: string,
      selector: latest | inside_review_window | explicit_paths,
      as: string,
      required?: bool
    }
  ],
  replace_refs?: { <default_ref_name>: ref | [ref] }
}
```

Rules:

- `extra_refs` and `parent_context_refs` are additive.
- `workflow_refs` binds source refs to optional report workflows. Use it when
  telemetry, feedback, opportunity, metric, or status sources should feed a
  specific workflow.
- `interval_output_refs.selector = latest` selects the newest dated report under
  `.farplane/reports/interval/<interval_id>/`.
- `interval_output_refs.selector = inside_review_window` selects dated reports
  from that interval whose timestamps fall inside `review_window`.
- `interval_output_refs.selector = explicit_paths` reads only supplied paths.
- Missing optional refs become source gaps. Missing required refs block durable
  goals or ticket mutation but still allow a report.
- Use `replace_refs` only when a project has a non-standard source of truth.

## Optional Report Workflows

Report workflows are generic functions over a context bundle and timeframe. The
caller enables them with booleans or lightweight modes.

```text
report_workflows = {
  plan_progress?: bool | "light",
  codex_attention_drift?: bool | "light",
  ticket_board_drift?: bool | "light",
  feedback_obligations?: bool | "when_sources_exist",
  opportunity_signals?: bool | "when_sources_exist",
  goal_drift?: bool | "light",
  metric_snapshot?: bool | "when_sources_exist",
  compounding_leverage_review?: bool | "light",
  skill_hardening?: bool | "when_sources_exist",
  skill_refinement?: bool | "when_sources_exist",
  docs_consolidation?: bool | "when_sources_exist",
  priority_planning?: bool | "light"
}
```

Missing workflow flags mean do not run that workflow. `SKILL.md` owns the
workflow reference index. Load only the workflow ref files for enabled flags;
those files own detailed todos, inline-vs-subagent routing, evidence rules, and
merge shape.

## Workflow

1. Bind `interval_id`, `review_window`, `planning_window`, and configured
   context refs.
2. Read default refs plus configured refs; label missing or stale sources.
3. Resolve cross-interval refs from `interval_output_refs`.
4. Normalize evidence into
   [interval-context-bundle.md](../templates/interval-context-bundle.md).
5. Reflect on the past window by running only enabled reflection workflows
   against the context bundle, `review_window`, and `planning_window`, loading
   only the workflow reference files named in `SKILL.md`.
6. Close or update rewards. For enabled self-update workflows, close due reward
   signals from prior interval reports before selecting new bets.
7. Score leverage and reward signals. Treat scores as planning aids with cited
   evidence, not objective telemetry.
8. Read product work lanes, local product skill refs, and static allocation
   guardrails when priority planning or ticket refill is enabled.
9. For enabled `skill_hardening`, route repeated lessons, troubles,
   ticket-progress findings, and proof failures to
   `skill-maintenance(mode: harden_skill)`.
10. For enabled `skill_refinement`, route accumulated older evals, gotchas,
   usage results, and compaction risks to
   `skill-maintenance(mode: refine_skill)`.
11. For enabled `docs_consolidation`, route whole-project context refresh to
   `update-memory` and substantive durable doc cleanup to `doc-advisor`.
12. Review the past window against the static harness charter, goals, and
    configured parent contexts.
13. Refresh metric readings when skills, CLIs, ticket searches, manual notes, or
    local ledgers are available: read goal-axis SMART goals from
    `farplane/goals.yaml` for KPI selection and interpretation, then use each
    KPI's `farplane/bindings.yaml` metric recipe `refresh` prompt to choose the
    work. Write one compact daily metrics file under
    `.farplane/metrics/daily/<date>.json`, then run
    `farplane project snapshot`. Do not parse ops memory as a deterministic
    database.
14. Review budget and runway for active projects. Use `farplane/harness.md`
    allocation guardrails, `farplane/ops-memory.md` contribution modes, ticket
    `Reward` blocks, metric snapshots, interval reports, source gaps, and
    operator feedback. Assign each active project a decision:
    `continue`, `narrow`, `pause`, `instrument`, `stop`, or
    `escalate_to_revenue`. Do not create a second ticket budget field.
15. Run final next-window planning. `priority_planning` should consume the
    reflection findings, reward closure, leverage decisions, product lanes, and
    guardrails; it should verify that each selected priority moves a named goal,
    bottleneck, or reward signal.
16. Write [interval-report.md](../templates/interval-report.md) before any
    goals mutation. Fill `ui_summary` in YAML frontmatter with one concise
    under-100-word string so UI consumers can render report cards without
    scraping prose.
17. Classify every goals delta as `auto_apply`, `approval_required`, or
    `rejected_source_gap`.
18. Convert executable changes into ticket deltas or Goal Advisor handoffs,
    including local product skill refs when they own the workflow.
19. Return downstream guidance so Pulse gets the next constraints.

## Goals Delta Promotion

The skill may update `farplane/goals.yaml` only after the interval report
contains a `Goals Delta` block with evidence and a promotion decision.

```text
apply_goals_delta(proposed_goals_delta, policy)
  -> goals.yaml patch | approval_required | rejected_source_gap
```

Promotion decisions:

- `auto_apply`: source refs, current-signal notes, stale labels, or minor
  milestone wording backed by clear evidence.
- `approval_required`: north star, KPI, strategy axis, project priority, hold,
  stop condition, quarterly goal, yearly goal, or durable milestone changes.
- `rejected_source_gap`: insufficient evidence; create an instrumentation,
  access, feedback, or research ticket instead.

Metric reading guidance:

```text
daily_metric_file := {
  date,
  metrics: {
    [metric_id]: {
      value: number | null,
      status: available | source_gap | blocked,
      payload?: object
    }
  }
}
```

Each metric value is the point reading for that date. The compiler derives
daily difference from consecutive readings, cumulative totals for
`kind: daily_count` metrics, and best-daily values. Content IDs, ticket IDs,
post IDs, API responses, and confidence notes belong under freeform `payload`,
not in KPI names. Ticket-derived KPI counts should be collected during this
daily refresh by counting tickets whose `Reward.kpi_rewards[].kpi_id` matches
the KPI, then storing the resulting count like any other metric value.

Reusable interval-owned helper signatures:

```text
$interval-update.count_ticket_kpi_rewards(ticket_dir, date, kpi_key)
  -> { value, status, payload? }

$interval-update.calculate_autonomy_time_ratio(runtime_dir, date)
  -> { value, status, payload? }

$interval-update.calculate_ticket_intervention_metrics(ticket_dir, runtime_dir, date)
  -> {
       auto_completion_rate: MetricReading,
       intervention_free_ticket_count: MetricReading,
       ticket_intervention_turn_count: MetricReading
     }

$interval-update.select_content_metric_targets(content_ledger, platform, kpi_key, date, window_days?)
  -> {
       status,
       external_ids,
       items,
       payload: { since_date, until_date, fetch_command, gaps }
     }
```

The concrete CLI owner is
`skills/interval-update/scripts/metric_refresh.py`. Refresh prompts may cite the
helper signature instead of restating the counting algorithm.

For owned-content distribution KPIs, first call
`select_content_metric_targets` to select posted ledger rows in the lookback
window. Then call the returned platform fetch command through `$x-account` or
`$instagram-account`, read the produced compact metrics, and store the selected
KPI's aggregate value plus per-post `payload.items` in the daily metric file.

Runway review guidance:

```text
runway_decision := {
  active_project,
  contribution_mode,
  expected_reward,
  observed_evidence,
  rough_spend_or_attention,
  decision: continue | narrow | pause | instrument | stop | escalate_to_revenue,
  next_constraint
}
```

The decision is a planning constraint, not a spend authorization. Publishing,
customer contact, paid external services, deploys, destructive cleanup, and
product-boundary changes still need explicit authorization unless granted by a
ticket or policy.

Quarterly, yearly, and other intervals greater than one week should normally
be represented as explicit interval automations only when they produce useful
decisions often enough to deserve their own thread and cadence. Otherwise, the
weekly interval can create a ticket or Goal Advisor handoff for the longer
horizon review.

## Workflow Rules

- Every enabled workflow output must cite context-bundle evidence or raw source
  pointers. Reject generic strategy prose.
- Analysis subagents are read-only. They must not mutate tickets, goals,
  external tools, or automation state.
- Leverage signals should come from existing reports, tickets, skills,
  registries, lessons, troubles, feedback, metrics, or explicitly supplied
  external source refs. Do not create a separate leverage backlog by default.
- Static charter changes belong to `farplane/harness.md` and require explicit
  human approval. Intervals may propose charter deltas in the dated report but
  must not apply them silently.
- The dated interval report is the state store for self-update decisions:
  reward closure, selected bets, rejected/deferred/expired candidates, advisor
  routes, and next reward signals.
- UI cards parse only the report frontmatter `ui_summary` string for compact
  card copy. Keep it under 100 words for every daily or weekly interval report.
  Use existing frontmatter fields and the report file path for title, date,
  type, and deep-link behavior.
- Skill hardening is not a separate compatibility automation. Weekly Interval
  routes learning sources to `skill-maintenance(mode: harden_skill)` and records
  processed or deferred learning in the dated report.
- Skill refinement is a separate optional workflow from hardening. Use it only
  after immediate guardrails exist, so compaction does not delay fresh
  prevention work.
- Docs consolidation is a separate optional workflow from memory refresh.
  Intervals should produce handoffs or compact deltas first, then let
  `update-memory` or `doc-advisor` own the actual doc edits when warranted.
- Urgent leverage escalation is allowed only for high-confidence evidence with
  a source ref, explicit loss term, review-by date, and next owner route.
