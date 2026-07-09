---
kind: interval-context
ref: reports/interval/<interval_id>/context/<timestamp>
project: <project>
automation_id: <automation_id>
interval_id: <interval_id>
status: draft
created_at: <timestamp>
review_window: <start>..<end>
planning_window: <start>..<end>
ui_summary: "<one concise context-bundle summary under 100 words>"
---

# Interval Context Bundle

Generated: <timestamp>
Project: <project>
Review window: <start> to <end> <timezone>
Planning window: <start> to <end> <timezone>
Interval id: <interval_id>
Report workflows: <enabled workflow list>

## Context Contract

Workflow lanes read `summary_context` first. They open
`raw_evidence_pointers` only when a finding needs cited source proof,
source-gap classification, or an explicit workflow exception such as
`reward_checkins`.

```text
summary_context:
  purpose: bounded tables and planning signals sufficient for first-pass
    workflow analysis
raw_evidence_pointers:
  purpose: paths, selectors, report refs, ticket refs, metric refs, or artifact
    refs that lanes may inspect for cited proof
lane_policy:
  default: read_only_subagent
  parent_only: context resolution, final synthesis, report writing, allowed
    post-report mutations
  exception: reward_checkins may patch ticket Reward actuals and score fields
    under its workflow contract
```

## Summary Context

Use these sections as the default bounded input for workflow lanes. Keep rows
compact and cite evidence instead of copying raw reports or ticket bodies.

## Source Status

| Source | Status | Freshness | Notes |
| --- | --- | --- | --- |
| Static harness charter |  |  |  |
| Product work lanes |  |  |  |
| Goals portfolio |  |  |  |
| Run ledger |  |  |  |
| Parent plan / goals |  |  |  |
| Daily interval reports |  |  |  |
| Prior interval reports |  |  |  |
| Pulse outcomes |  |  |  |
| Worker threads |  |  |  |
| Ticket board |  |  |  |
| Memory docs |  |  |  |
| Metrics refs |  |  |  |
| Thread index |  |  |  |
| Meeting or feedback refs |  |  |  |
| Opportunity sources |  |  |  |

## Static Charter Snapshot

| Thesis / leverage commitment / non-tradeoff | Current signal | Evidence | Gap |
| --- | --- | --- | --- |

## Goals Snapshot

| Goal / axis / project | Current signal | Evidence | Gap |
| --- | --- | --- | --- |

## Product Work Lane Snapshot

| Lane | Default weight hint | Current signal | Evidence | Gap |
| --- | ---: | --- | --- | --- |

## KPI And Feedback Snapshot

| KPI / feedback surface | Current value or state | Trend | Evidence | Gap |
| --- | --- | --- | --- | --- |

## Report Inputs

| Report | Window | Useful signal | Stale or missing? | Evidence |
| --- | --- | --- | --- | --- |

## Ticket And Work Outcomes

| Ticket / work item | State | Impact | Carry / pause / kill / split | Evidence |
| --- | --- | --- | --- | --- |

## Planning Signals

| Signal | What happened | Planning implication | Evidence |
| --- | --- | --- | --- |

## Configured Report Workflow Inputs

| Workflow | Inputs present | Missing or stale sources | Notes |
| --- | --- | --- | --- |
| Plan progress |  |  |  |
| Codex attention drift |  |  |  |
| Ticket / board drift |  |  |  |
| Relationship / feedback obligations |  |  |  |
| Opportunity signals |  |  |  |
| Priority planning |  |  |  |

## External / Opportunity Signals

| Signal | Source | Fit to goals | Decision pressure | Evidence |
| --- | --- | --- | --- | --- |

## Proposed Goals Delta Candidates

| Candidate | Target | Evidence | Risk | Initial promotion decision |
| --- | --- | --- | --- | --- |

## Source Gaps

-

## Raw Evidence Pointers

Use this section for evidence that a workflow lane may open only when it needs
source-level proof, source-gap classification, or an explicit exception.

-
