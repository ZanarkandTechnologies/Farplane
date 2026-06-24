---
title: "Codex Attention Drift Workflow"
status: active
owner: interval-update
kind: workflow-reference
template_uses:
  skill-template: "0.3.2"
---

# Codex Attention Drift Workflow

## Context

Use this workflow when an interval update needs to know where Codex attention
actually went and whether that matched the configured plan or goals. This is a
reporting workflow for agent attention, not a license to inspect unrelated
personal history.

Use configured telemetry refs first. Fall back to project-local Farplane
evidence. Raw Codex session inspection is last-resort and only allowed when the
automation policy permits it.

## Workflow Signature

```text
codex_attention_drift(context_bundle, review_window, planning_window,
                      telemetry_refs?)
  -> attention_map + alignment_buckets + drift_causes + calibration_note

state: reads(context_bundle, telemetry_refs?, pm_thread_grouping?,
             pulse_reports?, spawned_thread_ledgers?);
       writes(parent_interval_update_report_section)
gates: project_local_or_configured_refs_only; evidence_cited;
       no_private_history_inference; no_thread_mutation
fails: treating token volume as value; reading unrelated Codex history;
       blaming drift without classifying necessary unplanned work
```

## Source Contract

Preferred optional refs:

- `context_refs.workflow_refs.telemetry_refs`: Farplane UI telemetry exports,
  Codex app-server projections, thread usage summaries, model/cost/token
  aggregates, or session timelines.

Default fallback refs from the context bundle:

- `farplane/pm.json`: PM-visible thread grouping.
- `.farplane/reports/pulse/**`: selected actions and worker handoffs.
- `.farplane/automation/spawned-threads.jsonl`: child lineage when available.
- ticket links, report links, and worker outcome refs.

Last-resort refs:

- local Codex session indexes or raw rollout files only when clean telemetry is
  unavailable and the automation policy permits local raw inspection.

## Phase Boundary

Run inline for small pulse/report windows. Use a read-only subagent when
telemetry, thread rows, or Pulse reports are large enough that independent
clustering will improve the evidence trail.

## Todo List

- [ ] 1. Bind inputs.
  - [ ] Confirm `review_window` and available telemetry/project-local refs.
  - [ ] Mark unavailable telemetry as a source gap instead of guessing.
- [ ] 2. Build an attention map.
  - [ ] Collect thread, Pulse, ticket, worker, and telemetry evidence.
  - [ ] Group attention by project, goal, plan item, ticket, or unknown.
- [ ] 3. Classify alignment.
  - [ ] Label clusters as `planned_execution`, `necessary_unplanned_work`,
        `strategic_discovery`, `maintenance`, `avoidable_drift`, or `unclear`.
  - [ ] Cite the evidence for each bucket.
- [ ] 4. Explain drift causes.
  - [ ] Identify unrealistic plan, underspecified ticket, new evidence, tool
        failure, dependency, curiosity spiral, or genuine leverage.
- [ ] 5. Produce calibration.
  - [ ] Write one calibration note for the next planning window.
  - [ ] Name what Pulse or interval planning should do differently.

## Templates

Read-only subagent handoff:

```text
Read <context_bundle>. Run codex_attention_drift for <review_window>.
Use only configured telemetry/project-local refs. Return attention_map,
alignment_buckets, drift_causes, calibration_note, and source_gaps. Cite
evidence. Do not mutate files, threads, or automations.
```

## Gotchas

- High attention on unplanned work can be correct when it unblocks the plan.
- Thread grouping is UI glue; it is evidence of project association, not a full
  work ledger.
- Cost/token telemetry is a proxy for attention, not proof of impact.

## Reference Map

- Parent interval update loads this file only when
  `report_workflows.codex_attention_drift` is enabled.

## Output

```text
attention_map:
  - cluster:
    evidence_refs:
    attention_proxy:
    project_or_goal:
alignment_buckets:
  - bucket:
    items:
    evidence:
drift_causes:
  - cause:
    evidence:
calibration_note:
source_gaps:
```
