---
kind: dogfood-review
project: <project>
created_at: <timestamp>
review_window: <start>..<end>
status: draft
ui_summary: "<one concise CEO-readable summary under 100 words>"
tracked_refs:
  - <FEAT-#### or SYS-####>
decisions:
  <FEAT-#### or SYS-####>: continue | adjust | cap | pause | rollback | source_gap
source_gaps: []
---

# Dogfood Review Report

## Summary

- `decision:`
- `why_now:`
- `accepted_tradeoff:`

## Tracked Items

| Ref | Track prompt | Decision | Evidence | Source gaps |
| --- | --- | --- | --- | --- |

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
`source_gap`.

## Interval Summary

Use this section as the snippet that Daily or Weekly Interval can copy or link.

- `report_path:`
- `top_decisions:`
- `pulse_guidance:`
- `source_gaps:`
