---
kind: interval-weekly-working-draft
ref: reports/interval/weekly/<YYYY-Www>/draft
project: <project>
week: <YYYY-Www>
status: open
created_at: <timestamp>
updated_at: <timestamp>
previous_report_ref: <prior-finalized-weekly-report-or-none>
daily_receipt_refs: []
final_report_ref: null
---

# <Project> — Week <YYYY-Www>

This ignored runtime artifact is the compact current operating view. Upsert
Daily findings by `(stable source locator, intended owner, content digest)`.
Weekly sets every candidate's disposition, snapshots this draft into the
immutable report, marks it finalized, and opens the next draft.

## Current Context

Maximum five bullets covering current phase, material constraints,
dependencies, assumptions, and operator attention.

- <current context>

## Plan Versus Actual

| Planned result | Actual/progress | Evidence | Variance and implication |
| --- | --- | --- | --- |

## Problems

| Fingerprint | Problem | Evidence / recurrence | Impact | Proposed owner | Disposition |
| --- | --- | --- | --- | --- | --- |

## Promotion Candidates

| Fingerprint | Type | Candidate | Evidence | Value gate / missing fact | Route and destination | Disposition |
| --- | --- | --- | --- | --- | --- | --- |

`Type` is `decision`, `sop`, `resource`, or `entity`. `Disposition` remains
`pending` during Daily runs; Weekly replaces it with `promoted`, `duplicate`,
`monitor`, `dismissed`, `source_gap`, or `blocked`.

- A decision promotes only when it establishes a durable project-level
  precedent or updates an existing domain owner with supported rationale.
- An SOP promotes only with repeatability evidence and authority to change the
  owning skill.
- A resource promotes only when it has future reuse value outside its source
  task or thread.
- An entity fact promotes only with sourced identity and relationship evidence.

## Documentation Quality

| Fingerprint | Changed/high-risk doc | Quality gap | Evidence | Proposed patch or question | Disposition |
| --- | --- | --- | --- | --- | --- |

## Completeness And Follow-Ups

| Fingerprint | Source/owner | Missing fact or stale commitment | Decision unlocked | Proposed question/chase | Status |
| --- | --- | --- | --- | --- | --- |

Source-local comments and outgoing chases remain proposals unless separately
authorized. Never repeat an unresolved request.

## Next Week

| Commitment or carried problem | Owner | Evidence of priority | Approval status |
| --- | --- | --- | --- |

## Draft Receipt

- `daily_receipts_applied:`
- `candidate_upserts:`
- `duplicate_appends:` 0
- `canonical_promotions_during_daily:` 0
- `weekly_dispositions_complete:` no
- `draft_status:` open
