---
kind: feed-scout
ref: reports/feed-scout/<timestamp>
project: <project>
created_at: <timestamp>
review_window: <start>..<end>
status: draft
ui_summary: "<one concise source-change summary under 100 words>"
source_gaps: []
candidate_handoff:
  candidates: []
  recovery_tickets_created: []
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

## Dedupe, Source Redundancy, And Extraction

| Item | Canonical key | Exact duplicate / source-family relation | Distinct channel signal | Extraction path | Result |
| --- | --- | --- | --- | --- | --- |

## Instruction-Driven Proposals

| Source | Effective instruction ref | Proposal type | Candidate | Existing ledger/config match | Review route |
| --- | --- | --- | --- | --- | --- |

## Ticket Candidates

| Candidate | Source evidence | Executable scope | Reward / proof / stop | Authority | Verdict / reason |
| --- | --- | --- | --- | --- | --- |

Verdicts: `planner_candidate`, `duplicate`, `insufficient_signal`,
`scope_missing`, `proof_missing`, `authority_missing`, `report_only`.

## Planner Candidate Handoff

| Candidate | Area / KPI | Expected reward | Source refs | Verdict |
| --- | --- | --- | --- | --- |

- `report_written_before_handoff:` yes | no
- `recovery_ticket_limit:`
- `recovery_tickets_created:`
- `exploration_or_experiment_tickets_created:` 0
- `notion_tasks_created:` 0
- `execution_started:` no

## Source Gaps And Blockers

| Gap | Effect | Safe fallback |
| --- | --- | --- |
