---
title: "Plan Progress Workflow"
status: active
owner: interval-update
kind: workflow-reference
template_uses:
  skill-template: "0.3.2"
---

# Plan Progress Workflow

## Context

Use this workflow when an interval update needs to know whether the configured
plan actually moved during the review window. This is a read-only reporting
workflow. It produces findings that the parent interval update can use for the
next plan, ticket deltas, or Goal Advisor handoffs.

Do not query private planning systems by convention. Use the context bundle and
only the optional refs supplied by the calling automation.

## Workflow Signature

```text
plan_progress(context_bundle, review_window, planning_window,
              parent_context_refs?, status_refs?, metric_refs?)
  -> goal_movement + task_drag + plan_realism + priority_delta + source_gaps

state: reads(context_bundle, parent_context_refs?, status_refs?, metric_refs?);
       writes(parent_interval_update_report_section)
gates: review_window_bound; sources_cited; no_external_fetch_without_ref;
       no_ticket_or_goal_mutation
fails: treating stale plans as current; inventing Notion/CRM access;
       collapsing blocked work into failure; planning before reporting evidence
```

## Source Contract

Default sources from the context bundle:

- `parent_context_refs`: configured parent plans, goals, or strategy docs.
- `ticket_refs`: local Farplane tickets and ticket metadata.
- `interval_output_refs`: reports from other intervals, when configured.
- `pulse_report_refs`: Pulse decisions and spawned-work signals.
- worker/thread refs from `farplane/pm.json`, spawned-thread ledgers, and
  report links.

Optional source refs:

- `context_refs.workflow_refs.status_refs`: Notion task/project/status views,
  CRM/status exports, PM dashboards, or private project status docs.
- `context_refs.workflow_refs.metric_refs`: metrics that prove movement.

## Phase Boundary

Run inline for small boards. Use a read-only subagent only when there are many
tickets, reports, or status rows and the parent interval update would otherwise
lose the evidence trail.

## Todo List

- [ ] 1. Bind inputs.
  - [ ] Confirm `review_window` and `planning_window`.
  - [ ] Identify parent context refs, prior interval outputs, ticket refs,
        Pulse reports, and worker outcome refs.
- [ ] 2. Read planned work.
  - [ ] Extract planned priorities from parent context refs and prior interval
        reports.
  - [ ] Mark any missing or stale parent plan as a source gap.
- [ ] 3. Read actual work.
  - [ ] Collect review-window tickets, Pulse decisions, worker outcomes,
        blockers, and relevant status refs.
  - [ ] Split work into done, not done, blocked, and newly discovered.
- [ ] 4. Map evidence to plan.
  - [ ] Map each cluster to goals, parent plan items, tickets, or `source_gap`.
  - [ ] Label clusters as `needle_mover`, `maintenance`, `exploration`,
        `noise`, `blocked`, `stale`, `carry`, `delegate`, or `kill`.
- [ ] 5. Explain plan realism.
  - [ ] Identify bad estimates, weak priorities, dependencies, new evidence,
        justified plan changes, and source gaps.
  - [ ] Return carry/delegate/kill/new-priority recommendations sized to
        `planning_window`.

## Templates

Read-only subagent handoff:

```text
Read <context_bundle>. Run plan_progress for <review_window> with
<planning_window>. Use only configured refs. Return goal_movement, task_drag,
plan_realism, priority_delta, and source_gaps. Do not mutate files or external
systems. Cite evidence paths/rows.
```

## Gotchas

- A plan item with no visible progress may be correctly blocked, not bad work.
- Newly discovered work should be judged against goals before being called
  drift.
- Status refs can explain reality, but they do not replace project-local
  tickets unless the caller explicitly configured them as source of truth.

## Reference Map

- Parent interval update loads this file only when
  `report_workflows.plan_progress` is enabled.

## Output

```text
goal_movement:
  - goal_or_plan_item:
    movement: meaningful | partial | none | source_gap
    evidence:
task_drag:
  - item:
    label: blocked | stale | carry | delegate | kill
    evidence:
plan_realism:
  - issue:
    cause:
    calibration:
priority_delta:
  - next_priority:
    reason:
    proof_check:
source_gaps:
```
