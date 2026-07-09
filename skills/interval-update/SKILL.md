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

The parent interval run is:

```text
interval_parent_run(config, context_refs, workflow_flags)
  -> context_bundle(summary_context, raw_evidence_pointers)
   + workflow_findings
   + dated_interval_report
   + next_window_guidance
   + allowed_post_report_deltas
```

Callers own cadence, presets, and invocation profile. `interval-update` owns
one configured report-then-plan run. It must not select scheduler jobs, manage
heartbeat state, reconcile worker boards, or execute ticket work.

Parent responsibilities:
- Resolve defaults and configured refs.
- Build `summary_context` plus `raw_evidence_pointers`.
- Spawn one isolated read-only subagent lane for each enabled report workflow.
- Run deterministic helper scripts inline only for mechanical discovery.
- Collect workflow findings and run final synthesis.
- Write the dated report before any durable ticket, product, or goals mutation.
- Apply only explicitly allowed post-report deltas.

Workflow lanes consume `summary_context` first and open
`raw_evidence_pointers` only when they need cited source proof, source-gap
classification, or an explicit workflow exception. The default lane is
read-only: it must not edit tickets, goals, product files, automation state, or
external systems. `reward_checkins` is the gated exception: its helper may find
due ticket reward items, and the analyzer may propose ticket reward patches for
`Reward.kpi_rewards[].actual_result`, `reward_score`, and
`reward_score_reason`. The parent applies those patches only after the dated
report records them as allowed post-report deltas.
Detailed workflow catalogs, helper signatures, ticket reward contracts, and
caller preset boundaries live in references. Load only the refs required by the
enabled flags and branch conditions.

## Skill Signature

```text
interval_update(project_root, interval_id, review_window, planning_window,
                context_refs?, report_workflows?, planning_policy?,
                write_policy?, now?)
  -> context_bundle
   + summary_context
   + raw_evidence_pointers
   + source_gaps
   + interval_report
   + ui_summary
   + workflow_findings
   + drift_findings
   + next_window_plan
   + pulse_guidance
   + ticket_deltas
   + allowed_post_report_deltas
   + goals_delta?
   + goal_advisor_handoffs?

state:
  reads(default Farplane refs, configured context_refs, tickets/,
        product refs, goals, memory/history/lessons/troubles,
        Pulse/interval/dogfood reports, registries, PM/worker refs)
  writes(.farplane/reports/interval/<interval_id>/<YYYY-MM-DDTHHMMSSZ>.md,
         optional .farplane/reports/interval/<interval_id>/context/<YYYY-MM-DDTHHMMSSZ>.md,
         ticket Reward actual/score patches only as recorded post-report deltas,
         farplane/products/*/product.md only when write_policy allows,
         farplane/goals.yaml only through explicit goals-delta policy)

gates:
  default_refs_resolved; configured_refs_merged; review_window_bound;
  cross_interval_refs_resolved_or_gap_labeled;
  context_bundle_written_or_summarized; summary_context_built;
  raw_evidence_pointers_preserved; enabled_workflows_spawned_read_only;
  reward_checkins_exception_gated; report_written_before_plan_or_goals_mutation;
  configured_report_workflows_run; drift_checked; next_window_plan_written; side_effect_gates_respected;
  date_stamped_report_used; report_ref_frontmatter_written; ui_summary_frontmatter_written

routes:
  pulse-update | goal-advisor | feed-scout | dogfood-review | update-memory |
  update-strategy | skill-maintenance | metric-advisor | review

fails:
  selecting due jobs; writing scheduler state; mutating tracked cadence config;
  making automations restate default Farplane paths; using latest.md as
  canonical report; spawning broad leaf work; running enabled workflows inline
  as the default; letting workflow lanes mutate state; changing goals without
  report-first goals-delta evidence; treating Pulse as an interval workflow
```

Extended schema and branch detail live in references; the todo list owns when
to load them.

<!-- BEGIN FARPLANE_IMPORTANT_CHECKLIST -->
## Todo List

- [ ] 1. Bind the interval invocation.
  - [ ] Resolve `project_root`.
  - [ ] Bind `interval_id`, `review_window`, and `planning_window`.
  - [ ] Load `context_refs`, `report_workflows`, `planning_policy`, and
        `write_policy` only when the automation supplies them.
  - [ ] Load [references/interval-update.md](references/interval-update.md)
        when the run needs full context schema, default path details, metric
        lifecycle, goals-delta policy, or caller ownership boundaries.
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
- [ ] 3. Reflect on the past window.
  - [ ] Summarize tickets, Pulse decisions, worker outcomes, blockers,
        failures, file/doc changes, and human feedback inside `review_window`.
  - [ ] Check drift against the static harness charter, configured parent
        context refs, and goals.
  - [ ] Run only the enabled reflection workflows, passing the context bundle,
        `review_window`, and `planning_window` to each workflow lane.
  - [ ] Load [references/workflow-index.md](references/workflow-index.md) and
        only the workflow ref files for enabled workflows, then spawn read-only
        subagent analysis lanes by default.
  - [ ] Each workflow lane consumes `summary_context` first and opens
        `raw_evidence_pointers` only for cited proof, source gaps, or an
        explicit exception.
- [ ] 4. Close rewards and synthesize leverage.
  - [ ] For each enabled workflow in this phase, load its workflow ref and spawn
        a separate isolated lane; default lanes are read-only and return
        findings or handoffs to the parent.
  - [ ] When `reward_checkins` is enabled, run the due-check helper, then spawn
        one bounded analyzer lane to propose `ticket_reward_patches` for due
        item `actual_result`, `reward_score`, and `reward_score_reason`; route
        low scores or source gaps into the report, and apply patches only later
        as recorded post-report deltas.
  - [ ] When `compounding_leverage_review` is enabled, run its isolated lane
        before selecting new leverage moves.
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
  - [ ] When `tracked_feature_review` is enabled, call `dogfood-review` for
        active generated feature or system registry rows whose `track` value is
        a non-empty string and for active feature rows with `experimental:
        true`, excluding retired or superseded feature rows, then link or
        summarize the dogfood report in the interval report.
  - [ ] If dogfood-review returns an improvement ticket path or candidate,
        surface it in the interval report before final planning. Do not expand
        it into additional feature-by-feature tickets, and do not autostart
        `impl-plan`, Goal, Pulse execution, automation sync, or worker spawn.
- [ ] 5. Plan the next window.
  - [ ] Run `priority_planning` after reflection and reward/leverage synthesis
        when enabled; it must consume dogfood review findings when present and
        check that next-window priorities move a named goal, bottleneck, or
        leverage signal instead of merely filling time.
  - [ ] Produce a plan sized to `planning_window`.
  - [ ] Convert executable work into ticket deltas or Goal Advisor handoffs,
        including `.agents/skills/<product-skill>/SKILL.md` refs when a
        local product skill owns the workflow.
  - [ ] Before creating ticket deltas, load
        [references/ticket-reward-contract.md](references/ticket-reward-contract.md)
        and reject rewardless interval-planned tickets.
  - [ ] Return Pulse guidance as constraints for the fast executor loop.
- [ ] 6. Write the report before durable mutations.
  - [ ] Write a date-stamped interval report.
  - [ ] Include minimal Core report frontmatter: `ref:
        reports/interval/<interval_id>/<YYYY-MM-DDTHHMMSSZ>`, `kind:
        interval-report`, `created_at`, and `ui_summary`, preserving existing
        interval frontmatter such as `project`, `automation_id`,
        `interval_id`, `report_workflows`, `status`, `review_window`,
        `planning_window`, and `context_bundle`.
  - [ ] When writing an interval context bundle under `.farplane/reports/**`,
        include Core report frontmatter too: `ref:
        reports/interval/<interval_id>/context/<YYYY-MM-DDTHHMMSSZ>`, `kind:
        interval-context`, `created_at`, and `ui_summary`.
  - [ ] Include source gaps, drift findings, evidence, product strategy
        proposals, and the proposed next plan before mutating goals, product
        files, or tickets.
  - [ ] Apply only recorded `allowed_post_report_deltas`, including
        `ticket_reward_patches` for Reward actual/score fields.
  - [ ] Use goals-delta promotion before changing `farplane/goals.yaml`.
  - [ ] Run `farplane reports index --project-root <project_root>` after
        writing the report when the CLI is available.
- [ ] 7. Emit next-window guidance.
  - [ ] Summarize report paths, blockers, goals-delta decisions, and handoffs.
<!-- END FARPLANE_IMPORTANT_CHECKLIST -->

## Reference Map
- [references/interval-update.md](references/interval-update.md) - interval
  planning, context refs, caller ownership, metric lifecycle, and goals-delta
  promotion.
- [references/workflow-index.md](references/workflow-index.md) - load when
  `report_workflows` enables optional workflows; maps flags to workflow refs,
  helper scripts, and output shapes.
- [references/ticket-reward-contract.md](references/ticket-reward-contract.md)
  - load before creating ticket deltas from interval planning.
- [references/parent-run-contract.md](references/parent-run-contract.md) - load
  for audits or compaction only; `SKILL.md` is the runtime authority.
- [templates/interval-context-bundle.md](templates/interval-context-bundle.md)
  - default interval context bundle.
- [templates/interval-report.md](templates/interval-report.md) - default
  interval report.
- [references/workflows/reward-checkins.md](references/workflows/reward-checkins.md)
  - expected-vs-actual reward check-in workflow.
- [../metric-advisor/SKILL.md](../metric-advisor/SKILL.md) - honest metric
  cards for interval snapshots and compounding reward signals.
- [../../docs/features/FEAT-0065-pulse-and-interval-automation.md](../../docs/features/FEAT-0065-pulse-and-interval-automation.md)
