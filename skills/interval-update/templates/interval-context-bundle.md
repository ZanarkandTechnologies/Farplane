---
kind: interval-context
ref: reports/interval/<interval_id>/context/<timestamp>
project: <project>
automation_id: <automation_id>
interval_id: <daily|weekly>
status: draft
created_at: <timestamp>
review_window: <start>..<end>
ui_summary: "<one concise BAU evidence-bundle summary under 100 words>"
---

# BAU Interval Evidence Bundle

Use this optional sidecar only when a large Weekly window needs bounded source
pointers outside the report. The report remains the durable decision surface.

## Prior Finalized Evidence

| Ref | Kind | Window | Problem / signal | Status |
| --- | --- | --- | --- | --- |

## Same-Run Discoveries

| Ref | Problem / signal | Why ledger-only this run |
| --- | --- | --- |

## Work Outcomes

| Ticket / report | State | Observation | Evidence |
| --- | --- | --- | --- |

## Completed Provider Reports

| Provider | Report ref | Freshness | Useful signal / source gap |
| --- | --- | --- | --- |

## Active Ticket Dedupe Set

| Ticket | Problem / scope | State |
| --- | --- | --- |

## Source Gaps

| Missing source | Effect | Safe fallback |
| --- | --- | --- |
