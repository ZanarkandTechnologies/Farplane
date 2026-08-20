---
kind: interval-knowledge-receipt
ref: reports/interval/<interval_id>/<timestamp>-knowledge
project: <project>
automation_id: <automation_id>
interval_id: <daily|weekly>
status: final
created_at: <timestamp>
review_window: <start>..<end>
report_ref: <matching-finalized-interval-report>
source_gaps: []
---

# <Daily|Weekly> Knowledge Receipt

## Summary

- `candidate_upserts:`
- `promoted:`
- `no_op:`
- `staged_or_blocked:`
- `changed_owners:`
- `validation_result:` pass | partial | blocked

## Delta Results

| Stable source locator | Evidence refs | Type | Route / destination | Patch digest | Disposition | Result | Changed paths | Validation / blocker |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |

On Daily, `Disposition` is `pending` and `Result` is `candidate_upsert` or
`no_op`; canonical promotions must be zero. On Weekly, `Disposition` is
`promoted`, `duplicate`, `monitor`, `dismissed`, `source_gap`, or `blocked`, and
`Result` records the observed owner write or no-op. A repeated fingerprint with
no draft or destination change is `no_op`.

## Weekly Consolidation

Weekly only. Record the working draft and Daily receipts reviewed, every
candidate disposition, repeated deltas merged, canonical owner/index checks,
the finalized report, and the next draft opened.

## Receipts

- `report_finalized_before_knowledge_mutation:` yes | no
- `daily_canonical_promotions:` 0 | not_daily
- `weekly_candidate_dispositions_complete:` yes | not_weekly
- `weekly_draft_finalized:` yes | not_weekly
- `next_week_draft_opened:` yes | not_weekly
- `raw_transcript_content_persisted:` no
- `unsupported_claims_applied:` 0
- `direct_generated_index_or_projection_edits:` 0
- `skill_route_validation:` pass | no_change | blocked | not_applicable
- `docs_route_validation:` pass | no_change | blocked | not_applicable
- `wiki_route_validation:` pass | no_change | blocked | not_applicable
- `external_side_effects:` none
- `ticket_goal_pulse_worker_execution:` none
