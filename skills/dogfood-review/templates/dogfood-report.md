---
kind: dogfood-review
project: <project>
created_at: <timestamp>
review_window: <start>..<end>
status: draft
ui_summary: "<one concise CEO-readable summary under 100 words>"
policy_ref: farplane/harness.md#Feature-Policy
method: inline_review | per_feature_reviewer_lanes | reviewer_unavailable
context_ref: <path or null>
tracked_refs:
  - <FEAT-#### or SYS-####>
experimental_refs:
  - <FEAT-####>
skipped_refs:
  <FEAT-#### or SYS-####>: retired | superseded | out_of_scope | explicit_filter
decisions:
  <FEAT-#### or SYS-####>: continue | adjust | cap | pause | rollback | graduate | split_feature | merge | source_gap
reviewer_tas:
  <FEAT-#### or SYS-####>: TAS-A | TAS-B | TAS-C | TAS-D | not_run
source_gaps: []
improvement_ticket:
  mode: created | candidate | not_applicable | blocked
  path: <tickets/TASK-XXXX/ticket.md or null>
  candidate_ref: <section heading or null>
  no_autostart_receipt: "no impl-plan, Goal, Pulse execution, automation sync, or worker spawn invoked"
---

# Dogfood Review Report

## Summary

- `decision:`
- `policy_basis:`
- `why_now:`
- `accepted_tradeoff:`

## Tracked Items

| Ref | Experimental | Method | Decision | TAS | Track checklist | Evidence | Source gaps |
| --- | --- | --- | --- | --- | --- | --- | --- |

## Skipped Items

| Ref | Reason | Evidence | Use as historical evidence for |
| --- | --- | --- | --- |

## Feature Policy Check

- `policy_ref:` `farplane/harness.md#Feature-Policy`
- `feature_relevance:` how the reviewed behavior helps maintain, evaluate,
  steer, prove, report on, or productize autonomous harness behavior
- `policy_source_gap:` none | gap

## Output Volume

| Ref | Produced in window | Useful | Duplicate / vague | Review burden | Notes |
| --- | --- | --- | --- | --- | --- |

## Ticket Batch Review

Group high-volume tickets by pattern. Do not create one long section per ticket
unless a specific ticket is the strongest evidence.

| Pattern | Tickets | Verdict | Evidence |
| --- | --- | --- | --- |

## Evidence Reviewed

| Source | Status | Key signal | Evidence |
| --- | --- | --- | --- |

## Decisions And Guidance

| Ref | Decision | Guidance | Owner | Follow-up |
| --- | --- | --- | --- | --- |

Allowed decisions: `continue`, `adjust`, `cap`, `pause`, `rollback`,
`graduate`, `split_feature`, `merge`, `source_gap`.

## Improvement Ticket

Use this section for material tracked-feature reviews. Produce exactly one
consolidated improvement ticket path or one complete candidate for the report;
do not create one ticket per feature.

- `mode:` created | candidate | not_applicable | blocked
- `ticket_path:` `tickets/TASK-XXXX/ticket.md` | null
- `candidate_ref:` section-local candidate below | null
- `no_autostart_receipt:` no `impl-plan`, Goal, Pulse execution, automation
  sync, or worker spawn was invoked by this report

### Candidate Or Created Ticket Summary

```text
title:
phase: planning
status: review
ready: false
approval_required: true
reward:
  kpi_rewards:
    - kpi_id:
      expected_reward:
  guard:
source_report:
context_ref:
skipped_refs:
findings_by_feature:
  - feature_ref:
    track_prompt_summary:
    reviewer_tas:
    issue:
    proposed_repair:
    evidence_refs:
cross_cutting_repairs:
done_proof:
links:
```

## Interval Summary

Use this section as the snippet that Daily or Weekly Interval can copy or link.

- `report_path:`
- `top_decisions:`
- `reviewer_tas:`
- `improvement_ticket:`
- `pulse_guidance:`
- `source_gaps:`
