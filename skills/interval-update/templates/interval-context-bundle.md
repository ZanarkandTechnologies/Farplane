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

| Work item / report | State | Observation | Sanitized evidence ref |
| --- | --- | --- | --- |

Provider: `<filesystem_tickets|notion|source_gap>`. Binding:
`farplane/bindings.yaml#integrations.kanban` or `legacy_default`. Never include
resolved private provider IDs, URLs, tokens, or raw payloads.

## Completed Provider Reports

| Provider | Report ref | Freshness | Useful signal / source gap |
| --- | --- | --- | --- |

## Active Work-Item Dedupe Set

| Sanitized work-item ref | Problem / scope | State |
| --- | --- | --- |

## Source Gaps

| Missing source | Effect | Safe fallback |
| --- | --- | --- |
