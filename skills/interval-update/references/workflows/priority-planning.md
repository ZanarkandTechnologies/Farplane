---
title: "Priority Planning Workflow"
status: active
owner: interval-update
kind: workflow-reference
template_uses:
  skill-template: "0.3.2"
---

# Priority Planning Workflow

## Context

Use this workflow when an interval update needs to turn review-window evidence
into a ranked plan for the configured planning window. This is the generic
version of the old weekly PM synthesis lane: it keeps the valuable parts of
priority review, deprioritization, proof checks, follow-up agenda, and Pulse
guidance without embedding one project’s context into the skill.

This workflow plans and routes. It does not execute leaf work.

## Workflow Signature

```text
priority_planning(context_bundle, review_window, planning_window,
                  workflow_findings?, parent_context_refs?, planning_policy?)
  -> priorities + depriorities + proof_checks + downstream_guidance
     + goals_delta_candidates + source_gaps

state: reads(context_bundle, workflow_findings?, parent_context_refs?,
             planning_policy?);
       writes(parent_interval_update_report_section)
gates: report_evidence_available; planning_window_sized; proof_checks_named;
       leaf_work_routed_not_executed; material_goal_deltas_approval_gated
fails: writing a vague plan; mixing reporting and execution; hiding
       depriorities; embedding project-specific priorities in the workflow
```

## Source Contract

Default sources:

- parent context refs and goals from the context bundle.
- enabled workflow findings such as plan progress, goal drift, ticket board
  drift, feedback obligations, opportunity signals, attention drift, and
  metric snapshots.
- tickets, Pulse reports, interval reports, worker outcomes, and memory docs.

Optional sources:

- `context_refs.workflow_refs.status_refs`: planning systems, Notion status
  views, project status docs, CRM/PM dashboards.
- `context_refs.workflow_refs.metric_refs`: KPI or feedback proof.
- `context_refs.workflow_refs.feedback_refs`: commitments and people-facing
  obligations.
- `context_refs.workflow_refs.opportunity_refs`: source-backed opportunities.

Do not fetch private planning systems by convention. They must be configured.

## Phase Boundary

Run inline for small intervals. Use a read-only subagent when multiple workflow
findings need independent synthesis or when the planning window is large enough
that a second read reduces self-confirmation.

## Todo List

- [ ] 1. Bind inputs.
  - [ ] Confirm `review_window`, `planning_window`, parent context refs, and
        enabled workflow findings.
  - [ ] Read planning policy for side-effect, goals-delta, or output-shape
        instructions.
- [ ] 2. Separate planning inputs.
  - [ ] Group inputs by goals, completed work, unfinished work, feedback,
        board hygiene, opportunity signals, metrics, and attention drift.
  - [ ] Convert changed insight into implication into action.
- [ ] 3. Rank priorities.
  - [ ] Pick the top priorities sized to `planning_window`.
  - [ ] For each priority, include why-now, owner or next surface, expected
        output, and proof check.
- [ ] 4. Name depriorities.
  - [ ] Identify drag, stale assumptions, weak fit, and opportunity cost.
  - [ ] Decide revisit, park, kill, or split.
- [ ] 5. Route downstream work.
  - [ ] Separate solo work, people-facing follow-ups, background-agent work,
        and approval-required decisions when the project has those lanes.
  - [ ] Convert executable work into proposed ticket deltas or Goal Advisor
        handoffs.
  - [ ] Return Pulse constraints for the fast action loop.
- [ ] 6. Gate strategy changes.
  - [ ] Mark material goals, KPI, strategy-axis, quarterly/yearly, or durable
        milestone changes as approval-required goals deltas.

## Templates

Read-only subagent handoff:

```text
Read <context_bundle> and enabled workflow findings. Run priority_planning for
<review_window> -> <planning_window>. Return ranked priorities, depriorities,
proof checks, downstream guidance, goals_delta_candidates, and source_gaps.
Do not mutate files, goals, tickets, or external systems.
```

Priority row:

```text
- priority:
  why_now:
  owner_or_next_surface:
  expected_output:
  proof_check:
  route: ticket_delta | goal_advisor_handoff | pulse_constraint | human_decision
```

## Gotchas

- A plan without depriorities is usually just a wish list.
- Larger planning windows need stronger proof checks, not more vague bullets.
- Goal Advisor is for durable goal/ticket architecture, not every tiny Pulse
  decision.

## Reference Map

- Parent interval update loads this file only when
  `report_workflows.priority_planning` is enabled.

## Output

```text
priorities:
  - priority:
    why_now:
    owner_or_next_surface:
    expected_output:
    proof_check:
depriorities:
  - item:
    reason:
    revisit_or_kill:
proof_checks:
  - item:
    check:
downstream_guidance:
  pulse_constraints:
  ticket_deltas:
  goal_advisor_handoffs:
goals_delta_candidates:
  - delta:
    decision: auto_apply | approval_required | rejected_source_gap
    evidence:
source_gaps:
```
