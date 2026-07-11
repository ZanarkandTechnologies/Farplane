---
kind: feed-scout
ref: reports/feed-scout/<timestamp>
project: <project>
created_at: <timestamp>
review_window: <start>..<end>
status: draft
ui_summary: "<one concise source-change summary under 100 words>"
source_gaps: []
ticket_projection:
  limit: <n>
  created: []
  no_execution_receipt: "no Goal, Pulse, worker, implementation, publication, or outreach invoked"
---

# Feed Scout Report

## Summary

- `sources_checked:`
- `new_or_changed_items:`
- `strongest_signal:`
- `operator_attention:`

## Source Items

| Key | Source / date basis | Today-specific delta | Evidence | Signal | Route |
| --- | --- | --- | --- | --- | --- |

## Dedupe And Extraction

| Item | Canonical key | Prior occurrence / active ticket | Extraction path | Result |
| --- | --- | --- | --- | --- |

## Ticket Candidates

| Candidate | Source evidence | Executable scope | Reward / proof / stop | Authority | Verdict / reason |
| --- | --- | --- | --- | --- | --- |

Verdicts: `create_after_report`, `duplicate`, `insufficient_signal`,
`scope_missing`, `proof_missing`, `authority_missing`, `report_only`.

## Ticket Projection Receipt

| Ticket | Candidate | Admission | Source refs | Result |
| --- | --- | --- | --- | --- |

- `report_written_before_projection:` yes | no
- `ticket_limit:`
- `tickets_created:`
- `execution_started:` no

## Source Gaps And Blockers

| Gap | Effect | Safe fallback |
| --- | --- | --- |
