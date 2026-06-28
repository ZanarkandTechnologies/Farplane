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
owns cadence by running explicit automations. This skill owns the shared
report-then-plan workflow for one configured window. The caller supplies the
timeframe, cross-interval context refs, and optional report workflows.

Do not wrap this skill in a hidden scheduler thread. If a project needs another
cadence, create another explicit automation that calls this skill with a named
interval, review window, planning window, context refs, and workflow flags.

## Skill Signature

```text
interval_update(project_root, interval_id, review_window, planning_window,
                context_refs?, report_workflows?, planning_policy?,
                write_policy?, now?)
  -> context_bundle
   + source_gaps
   + interval_report
   + workflow_findings
   + drift_findings
   + next_window_plan
   + pulse_guidance
   + ticket_deltas
   + goals_delta?
   + goal_advisor_handoffs?

state:
  reads(farplane/harness.md?,
        farplane/products.md?,
        .agents/skills/**/SKILL.md?,
        farplane/goals.md?,
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
  default_refs_resolved; configured_refs_merged; review_window_bound;
  cross_interval_refs_resolved_or_gap_labeled;
  context_bundle_written_or_summarized; report_written_before_plan_or_goals_mutation;
  configured_report_workflows_run; drift_checked; next_window_plan_written; side_effect_gates_respected;
  date_stamped_report_used

routes:
  pulse-update | goal-advisor | feed-scout | update-memory |
  update-strategy | skill-maintenance | metric-advisor | review

fails:
  selecting due jobs; writing scheduler state; mutating tracked cadence config;
  making automations restate default Farplane paths; using latest.md as
  canonical report; spawning broad leaf work; changing goals without
  report-first goals-delta evidence
```

## Default Resolution

Resolve this standard context for every Farplane project, then merge
caller-supplied `context_refs`.

```text
default_context_refs(project_root, interval_id) = {
  harness_ref: farplane/harness.md,
  products_ref: farplane/products.md,
  goals_ref: farplane/goals.md,
  ticket_refs: tickets/,
  memory_refs: [docs/MEMORY.md, docs/HISTORY.md, docs/LESSONS.md, docs/TROUBLES.md],
  pulse_report_refs: .farplane/reports/pulse/**,
  interval_report_refs: .farplane/reports/interval/**,
  report_root: .farplane/reports/interval/<interval_id>,
  context_bundle_root: .farplane/reports/interval/<interval_id>/context
}
```

Configurable inputs:

```text
context_refs:
  extra_refs?: [ref]
  parent_context_refs?: [ref]
  workflow_refs?: {
    telemetry_refs?: [ref]
    feedback_refs?: [ref]
    opportunity_refs?: [ref]
    metric_refs?: [ref]
    status_refs?: [ref]
  }
  interval_output_refs?: [
    {
      interval_id: string,
      selector: latest | inside_review_window | explicit_paths,
      as: string
    }
  ]
  replace_refs?: { <default_ref_name>: ref | [ref] }

report_workflows:
  plan_progress?: bool | "light"
  codex_attention_drift?: bool | "light"
  ticket_board_drift?: bool | "light"
  feedback_obligations?: bool | "when_sources_exist"
  opportunity_signals?: bool | "when_sources_exist"
  goal_drift?: bool | "light"
  metric_snapshot?: bool | "when_sources_exist"
  compounding_leverage_review?: bool | "light"
  skill_hardening?: bool | "when_sources_exist"
  skill_refinement?: bool | "when_sources_exist"
  docs_consolidation?: bool | "when_sources_exist"
  priority_planning?: bool | "light"
```

`planning_policy` and `write_policy` may add phase instructions, side-effect
gates, goals-delta policy, or report shape. Missing optional configs mean use
the generic report-then-plan path only.
Use [references/interval-update.md](references/interval-update.md) for the
configuration contract, optional workflow definitions, and goals-delta policy.

Workflow reference index:

```text
plan_progress(review_window)
  -> goal_movement + task_drag + plan_realism
  ref: references/workflows/plan-progress.md

codex_attention_drift(review_window)
  -> attention_map + drift_causes
  ref: references/workflows/codex-attention-drift.md

ticket_board_drift(review_window)
  -> stale_work + board_hygiene_deltas
  ref: references/workflows/ticket-board-drift.md

feedback_obligations(review_window, planning_window)
  -> commitments + followups
  ref: references/workflows/feedback-obligations.md

opportunity_signals(review_window, planning_window)
  -> candidates + defer_or_displace_decisions
  ref: references/workflows/opportunity-signals.md

goal_drift(review_window)
  -> goal_findings + goals_delta_candidates
  ref: references/workflows/goal-drift.md

metric_snapshot(review_window)
  -> metric_status + gaps
  ref: references/workflows/metric-snapshot.md

compounding_leverage_review(review_window, planning_window)
  -> lever_inventory + top_experiment_candidates + reward_signals
  ref: references/workflows/compounding-leverage-review.md

skill_hardening(review_window, planning_window)
  -> harden_skill_handoffs + eval_candidates + processed_state_delta
  ref: references/workflows/skill-hardening.md

skill_refinement(review_window, planning_window)
  -> consolidate_skill_handoffs + compaction_candidates + coverage_risks
  ref: references/workflows/skill-refinement.md

docs_consolidation(review_window, planning_window)
  -> consolidate_docs_handoffs + stale_doc_candidates + source_gaps
  ref: references/workflows/docs-consolidation.md

priority_planning(review_window, planning_window)
  -> priorities + depriorities + proof_checks
  ref: references/workflows/priority-planning.md
```

<!-- BEGIN FARPLANE_IMPORTANT_CHECKLIST -->
## Todo List

- [ ] 1. Bind the interval invocation.
  - [ ] Resolve `project_root`.
  - [ ] Bind `interval_id`, `review_window`, and `planning_window`.
  - [ ] Load `context_refs`, `report_workflows`, `planning_policy`, and
        `write_policy` only when the automation supplies them.
- [ ] 2. Resolve default context.
  - [ ] Build default refs for the static harness charter, goals, tickets,
        memory, Pulse reports, interval reports, PM thread grouping, and worker
        outcome refs.
  - [ ] Merge configured refs without making the caller restate default
        Farplane paths.
  - [ ] Resolve configured cross-interval refs, such as latest output from one
        interval or reports from another interval inside `review_window`.
  - [ ] Bind workflow-specific source refs from `context_refs.workflow_refs`
        before running source-dependent report workflows.
  - [ ] Label missing or stale sources as source gaps.
- [ ] 3. Review the past window.
  - [ ] Summarize tickets, Pulse decisions, worker outcomes, blockers,
        failures, file/doc changes, and human feedback inside `review_window`.
  - [ ] Check drift against the static harness charter, configured parent
        context refs, and goals.
  - [ ] Run only the report workflows enabled by `report_workflows`, passing
        the context bundle, `review_window`, and `planning_window` to each
        workflow.
  - [ ] Load only the workflow ref files named in the workflow reference index
        for enabled workflows, then run inline or read-only subagent analysis
        lanes as those refs direct.
  - [ ] When `compounding_leverage_review` is enabled, close due reward
        signals from prior interval reports before selecting new leverage bets.
  - [ ] When metric snapshots or reward signals are ambiguous, use a metric
        card before allowing them to drive planning.
  - [ ] When `skill_hardening` is enabled, route repeated troubles, lessons,
        progress-log findings, and proof failures to
        `skill-maintenance(mode: harden_skill)`.
  - [ ] When `skill_refinement` is enabled, route accumulated older evals,
        gotchas, and usage results to `consolidate(..., structure = skill)`,
        then to `skill-maintenance(mode: refine_skill)` for accepted edits.
  - [ ] When `docs_consolidation` is enabled, route broad project context
        keep/merge/move/delete decisions through `consolidate(..., structure =
        docs_tree | memory)`, broad context refresh through `update-memory`,
        and substantive doc-quality rewrites through `doc-advisor`.
- [ ] 4. Write the report before durable mutations.
  - [ ] Write a date-stamped interval report.
  - [ ] Include source gaps, drift findings, evidence, and the proposed next
        plan before mutating goals or tickets.
  - [ ] Use goals-delta promotion before changing `farplane/goals.md`.
- [ ] 5. Emit next-window guidance.
  - [ ] Produce a plan sized to `planning_window`.
  - [ ] Convert executable work into ticket deltas or Goal Advisor handoffs,
        including `.agents/skills/<product-skill>/SKILL.md` refs when a
        local product skill owns the workflow.
  - [ ] Return Pulse guidance as constraints for the fast executor loop.
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

- [references/interval-update.md](references/interval-update.md) - interval
  planning, context refs, optional report workflows, and goals-delta promotion.
- [templates/interval-context-bundle.md](templates/interval-context-bundle.md)
  - default interval context bundle.
- [templates/interval-report.md](templates/interval-report.md) - default
  interval report.
- [../metric-advisor/SKILL.md](../metric-advisor/SKILL.md) - honest metric
  cards for interval snapshots and compounding reward signals.
- [../../docs/features/FEAT-0065-pulse-and-interval-automation.md](../../docs/features/FEAT-0065-pulse-and-interval-automation.md)
