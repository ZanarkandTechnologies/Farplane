---
title: "Goal Drift Workflow"
status: active
owner: interval-update
kind: workflow-reference
template_uses:
  skill-template: "0.3.2"
---

# Goal Drift Workflow

## Context

Use this workflow when an interval update needs to check whether review-window
work still ladders to configured goals and parent contexts. This workflow
reports drift and proposes goals-delta candidates. It does not edit
`farplane/goals.yaml`.

Material north-star, KPI, strategy-axis, project priority, quarterly/yearly, or
durable milestone changes are approval-required unless the caller supplies an
explicit goals-delta policy.

## Workflow Signature

```text
goal_drift(context_bundle, review_window, planning_window,
           harness_ref, goals_ref, parent_context_refs?, metric_refs?,
           status_refs?)
  -> verdict + goal_findings + unmapped_work + goals_delta_candidates
     + source_gaps

state: reads(context_bundle, harness_ref, goals_ref, parent_context_refs?,
             metric_refs?, status_refs?);
       writes(parent_interval_update_report_section)
gates: goals_ref_checked; parent_context_checked_or_gap;
       evidence_cited; goals_delta_proposed_not_applied
fails: changing goals during analysis; treating maintenance as drift by
       default; approving strategy changes without explicit policy
```

## Source Contract

Default sources:

- `harness_ref`: default `farplane/harness.md` for the static human thesis,
  non-tradeoffs, and agent authority.
- `goals_ref`: default `farplane/goals.yaml`.
- `parent_context_refs`: configured parent plans, strategy docs, or goals.
- interval outputs, tickets, Pulse reports, worker outcomes, and memory docs
  from the context bundle.

Optional sources:

- `context_refs.workflow_refs.status_refs`: project status or planning system
  refs.
- `context_refs.workflow_refs.metric_refs`: KPI/feedback proof.

Do not load project-specific planning systems unless configured.

## Phase Boundary

Enabled `goal_drift` runs as a read-only subagent lane by default. The parent
interval agent may handle only mechanical source binding inline; the lane reads
the context bundle, consumes summary context first, opens raw evidence pointers
only for cited proof or source gaps, and returns goals-delta candidates for the
parent report. The lane never edits `farplane/goals.yaml`.

## Todo List

- [ ] 1. Bind inputs.
  - [ ] Resolve `goals_ref`.
  - [ ] Resolve `harness_ref` and treat missing static charter context as a
        source gap.
  - [ ] Resolve parent context refs and mark missing parents as source gaps.
- [ ] 2. Map work to goals.
  - [ ] Read review-window tickets, reports, Pulse outcomes, and worker
        outcomes.
  - [ ] Map each evidence cluster to goals, strategy axes, parent plans, or
        `unmapped_work`, while checking the static charter boundary.
- [ ] 3. Classify drift.
  - [ ] Label each goal as `aligned`, `drifting`, `blocked`, or `source_gap`.
  - [ ] Label unmapped work as `necessary_unplanned_work`,
        `strategic_discovery`, `maintenance`, or `avoidable_drift`.
- [ ] 4. Propose goals deltas.
  - [ ] Cite evidence for each candidate.
  - [ ] Mark material strategy changes as approval-required.
  - [ ] Mark static charter changes as approval-required harness deltas, not
        goals deltas.
  - [ ] Do not edit goals.
- [ ] 5. Return planning implication.
  - [ ] Name what the next plan should protect, correct, or stop doing.

## Templates

Read-only subagent handoff:

```text
Read <context_bundle>. Run goal_drift for <review_window> and
<planning_window>. Return verdict, goal_findings, unmapped_work,
goals_delta_candidates, and source_gaps. Do not edit goals.
```

## Gotchas

- Necessary maintenance can support goals even when it does not look like
  feature progress.
- Goals can be stale; propose a delta instead of silently planning around a
  broken goal.
- Metrics strengthen drift findings only when source windows and goal targets
  match.

## Reference Map

- Parent interval update loads this file only when
  `report_workflows.goal_drift` is enabled.

## Output

```text
verdict: aligned | drifting | blocked | source_gap
goal_findings:
  - goal:
    status:
    evidence:
unmapped_work:
  - item:
    label:
    evidence:
goals_delta_candidates:
  - delta:
    decision: auto_apply | approval_required | rejected_source_gap
    evidence:
source_gaps:
```
