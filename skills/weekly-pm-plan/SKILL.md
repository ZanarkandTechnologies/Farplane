---
name: weekly-pm-plan
description: "Turn weekly reports, outcomes, external context, memory, and tickets into strategy, roadmap, and next-week operating priorities."
tier: 3
group: harness
source: local
skill_template_version: "0.2.0"
eval: eval_task.json
allowed-tools: Read, Glob, Grep, Bash
---

# Weekly PM Plan

## Context

Use this skill for weekly strategy. It sets direction for daily planning and the
short PM heartbeat. It may refresh memory, external context, skill upkeep, and
strategy reports, but it should not execute leaf tickets.

This skill is intentionally separate from `daily-pm-plan` and `pm-heartbeat` so
each cadence can be tested and customized by editing its own `SKILL.md`.

This is the generic project-PM shape behind specialized weekly strategy
wrappers. For example, [weekly-strategy-analysis](../weekly-strategy-analysis/SKILL.md)
pre-fills Kenji-specific Notion, meeting, Codex-thread, and opportunity-scan
refs. This skill should accept those surfaces as context params instead of
hard-coding personal paths or private tools.

## Automation Presets

`weekly-pm-plan.strategy @7d -> reports.weekly_pm`

The automation manifest supplies cadence, grouped jobs, freshness policy,
report handles, gates, and local overrides. This skill owns weekly synthesis,
strategic deltas, memory/strategy coordination, ticket shaping, and next-week
priority output.

## Skill Signature

```text
weekly_pm_plan(project_root, context_refs, reports?, policy?, window?)
  -> weekly_strategy
   + weekly_report
   + next_week_priorities
   + ticket_deltas
   + proposed_goals_delta
   + applied_goals_delta?
   + approval_required_goals_delta?
   + daily_plan_guidance
   + context_bundle

state:
  reads(context_refs.goals_ref, context_refs.automation_ref,
        context_refs.report_refs, context_refs.ledger_ref,
        context_refs.memory_refs, context_refs.ticket_refs,
        context_refs.thread_index_ref?, context_refs.metrics_refs?,
        context_refs.meeting_refs?, context_refs.opportunity_sources?,
        context_refs.private_context_refs?)
  writes(.farplane/reports/weekly-pm/latest.md,
         .farplane/reports/weekly-pm/runs/<timestamp>.md,
         context_refs.output_bundle_dir/<timestamp>-weekly-pm-context.md,
         farplane/goals.md only through the goals_delta promotion policy,
         strategy and ticket deltas when safe)

gates:
  reports_fresh_or_labeled; goals_read; memory_checked; tickets_checked;
  context_bundle_written; weekly_report_written_before_goals_mutation;
  goals_delta_promotion_decided; strategy_delta_evidence_tied;
  leaf_execution_avoided; daily_guidance_written

routes:
  feed-scout | update-memory | update-strategy | skill-maintenance |
  daily-pm-plan | goal-advisor | weekly-strategy-analysis | review

fails:
  executing leaf tickets; producing only a status digest; inventing metrics;
  letting daily noise dominate weekly direction; skipping memory or external
  context freshness labels; mutating goals.md before a weekly report exists;
  silently auto-applying north-star, KPI, strategy-axis, project-priority,
  hold, quarterly, or yearly goal changes
```

## Context Params

Callers supply file or tool-backed references; the generic skill does not
discover personal systems by convention.

```text
WeeklyPMContext = {
  project_root,
  review_window,
  goals_ref,
  automation_ref,
  ledger_ref,
  ticket_refs,
  memory_refs,
  report_refs,
  thread_index_ref?,
  metrics_refs?,
  meeting_refs?,
  opportunity_sources?,
  private_context_refs?,
  output_bundle_dir
}
```

Rules:

- Write a bounded context bundle before synthesis; lanes and child agents read
  the bundle instead of hidden chat state.
- Label missing refs as source gaps. Do not fabricate task, meeting, metric,
  thread, or opportunity evidence.
- Normalize source rows before strategy: keep status, dates, owner/context,
  impact, blockers, artifact pointers, and source links; avoid raw dumps.
- Specialized wrappers may prefill refs and add domain lanes. The reusable
  contract remains `weekly_pm_plan(project_root, context_refs, ...)`.

## Templates

Use [templates/context-bundle.md](templates/context-bundle.md) for the bounded
evidence bundle and [templates/report.md](templates/report.md) for the weekly
decision record. Specialized wrappers may add source-specific sections, but
they must preserve the generic `Goals Delta`, `Daily PM Guidance`, source-gap,
and output fields.

## Goals Delta Promotion

Weekly PM may update `farplane/goals.md` only after the weekly report contains
a `Goals Delta` block with evidence and a promotion decision.

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

Quarterly and yearly planning are rollup modes by default, not separate
scheduled threads. Add a quarterly/yearly cadence only after repeated weekly
reports show that the longer horizon produces decisions weekly context cannot
handle.

<!-- BEGIN FARPLANE_IMPORTANT_CHECKLIST -->
## Todo List

- [ ] 1. Load weekly evidence.
  - [ ] Bind `context_refs` including goals, automation policy, ledger, reports,
        memory docs, tickets, optional metrics, thread index, meetings,
        opportunity sources, and output bundle dir.
  - [ ] Read the supplied refs and recent daily/heartbeat outcomes.
  - [ ] Label missing or stale inputs explicitly.
- [ ] 2. Build the context bundle.
  - [ ] Normalize source rows into a bounded weekly context bundle before
        synthesis or lane delegation.
  - [ ] Include source/tool status, review window, evidence pointers, and
        source gaps.
- [ ] 3. Ensure required weekly inputs.
  - [ ] Reuse fresh external context, memory, skill hardening/refinement,
        registry drift, and strategy reports.
  - [ ] Run or request stale grouped jobs only within side-effect gates.
- [ ] 4. Synthesize strategy.
  - [ ] Identify kept, changed, paused, killed, or testable bets.
  - [ ] Write the weekly report from `templates/report.md` before mutating
        `farplane/goals.md`.
  - [ ] Fill `Goals Delta` with `auto_apply`, `approval_required`, or
        `rejected_source_gap` for each proposed portfolio change.
  - [ ] Auto-apply only low-risk evidence/current-signal updates; require
        approval for north-star, KPI, strategy-axis, project-priority, hold,
        quarterly, or yearly changes.
  - [ ] Convert actionable changes into ticket deltas or Goal Advisor
        handoffs, not hidden execution.
- [ ] 5. Write daily guidance.
  - [ ] Produce next-week priorities and constraints that `daily-pm-plan` can
        translate into daily lanes.
  - [ ] Name external context, memory, or feedback gaps that should influence
        the next daily plan.
- [ ] 6. Finish with report and ledger.
  - [ ] Write latest and timestamped weekly PM reports.
  - [ ] Update ledger freshness and blocked systems.
<!-- END FARPLANE_IMPORTANT_CHECKLIST -->

## Output

- context bundle path.
- weekly PM report path.
- weekly strategy delta.
- proposed goals delta with promotion decisions.
- next-week priorities and constraints.
- ticket deltas or Goal Advisor handoffs.
- daily planner guidance.
- source gaps.
- report and ledger paths.
