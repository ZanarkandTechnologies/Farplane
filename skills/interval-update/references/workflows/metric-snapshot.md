---
title: "Metric Snapshot Workflow"
status: active
owner: interval-update
kind: workflow-reference
template_uses:
  skill-template: "0.3.2"
---

# Metric Snapshot Workflow

## Context

Use this workflow when an interval update needs a compact status of KPI,
telemetry, QA/eval, business, or feedback metrics during the review window.
This is a measurement workflow, so source discipline matters more than prose.

Do not invent numeric trends. If sources are absent and the workflow mode is
`when_sources_exist`, return `not_applicable`.

## Workflow Signature

```text
metric_snapshot(context_bundle, review_window, planning_window,
                metric_refs?, telemetry_refs?, feedback_refs?)
  -> metric_status + implications + confidence + gaps

state: reads(context_bundle, metric_refs?, telemetry_refs?, feedback_refs?);
       writes(parent_interval_update_report_section)
gates: metric_sources_present_or_not_applicable; windows_compatible_or_gap;
       measured_vs_qualitative_separated; no_invented_trends
fails: comparing incompatible windows; treating anecdotes as metrics;
       fabricating KPI movement; omitting instrumentation gaps
```

## Source Contract

Preferred refs:

- `context_refs.workflow_refs.metric_refs`: KPI exports, analytics summaries,
  scorecards, QA/eval metrics, business metrics, or manually maintained metric
  docs.

Supporting refs:

- `context_refs.workflow_refs.telemetry_refs`: usage/cost/timing telemetry.
- `context_refs.workflow_refs.feedback_refs`: qualitative feedback that
  explains metric movement.

## Phase Boundary

Enabled `metric_snapshot` runs as a read-only subagent lane by default. The
parent interval agent may handle only mechanical source binding inline; the
lane reads the context bundle, consumes summary context first, opens raw
evidence pointers only for cited proof or source gaps, and returns metric
findings for the parent report.

## Todo List

- [ ] 1. Bind inputs.
  - [ ] If no metric refs exist and mode is `when_sources_exist`, return
        `not_applicable`.
  - [ ] Confirm source windows and freshness.
- [ ] 2. Normalize metrics.
  - [ ] Extract name, window, value/state, trend if supplied, confidence, and
        evidence.
  - [ ] Separate measured values from qualitative feedback.
- [ ] 3. Compare against goals.
  - [ ] Compare only when the goal defines the metric or target.
  - [ ] Mark missing instrumentation, stale sources, or incompatible windows as
        gaps.
- [ ] 4. Produce implications.
  - [ ] Explain what the metric changes mean for `planning_window`.
  - [ ] Avoid overfitting on weak or one-off signals.

## Templates

Read-only subagent handoff:

```text
Read <context_bundle>. Run metric_snapshot for <review_window> and
<planning_window>. Return metric_status, implications, confidence, and gaps.
Do not invent data or compare incompatible windows without flagging the gap.
```

## Gotchas

- A qualitative complaint can explain a metric, but it is not a metric.
- Missing instrumentation is a finding, not a reason to hallucinate trend.
- The review window may not match the metric source window; report that
  mismatch.

## Reference Map

- Parent interval update loads this file only when
  `report_workflows.metric_snapshot` is enabled.

## Output

```text
metric_status:
  - metric:
    state_or_value:
    trend:
    confidence:
    evidence:
implications:
  - implication:
    next_action:
confidence:
gaps:
```
