---
kind: dogfood-review
project: <project>
created_at: <timestamp>
review_window: <start>..<end>
status: draft
ui_summary: "<one concise CEO-readable summary under 100 words>"
policy_ref: farplane/harness.md#Feature-Policy
tracked_refs:
  - <FEAT-#### or SYS-####>
experimental_refs:
  - <FEAT-####>
decisions:
  <FEAT-#### or SYS-####>: continue | adjust | cap | pause | rollback | graduate | split_feature | merge | source_gap
source_gaps: []
---

# Dogfood Review Report

## Summary

- `decision:`
- `policy_basis:`
- `why_now:`
- `accepted_tradeoff:`

## Tracked Items

| Ref | Experimental | Track prompt / review question | Decision | Evidence | Source gaps |
| --- | --- | --- | --- | --- | --- |

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

## Interval Summary

Use this section as the snippet that Daily or Weekly Interval can copy or link.

- `report_path:`
- `top_decisions:`
- `pulse_guidance:`
- `source_gaps:`
