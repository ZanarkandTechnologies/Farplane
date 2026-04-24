---
name: qa
description: Run the QA phase for one selected ticket by collecting proof artifacts, reconciling acceptance criteria, and producing a structured QA result artifact for Stop-hook gating.
---

# QA

`$qa` is the proof-gathering phase for a selected ticket.

Use it when:

- implementation is ready for proof
- a ticket in `status: building` needs evidence before completion
- `$impl` or the operator needs to rerun QA without redoing implementation

Do not use it when:

- the ticket still needs planning; use `impl-plan`
- the work is not yet implementation-ready; use `$impl`

## Contract

- Read the selected ticket plus linked docs/specs.
- Gather ticket-scoped proof under `tickets/artifacts/TASK-XXXX/qa/`.
- For UI or user-visible work, use `visual-qa` as a separate judgment pass.
- Update the ticket `Evidence` section with the strongest artifact links.
- Write `result.json` under the QA artifact root and finish with:
  - `IMPL_RESULT: status=qa_complete next=building reason=...`

## Required artifacts

- `report.md`
- `result.json`
- supporting screenshots/logs/snapshots as needed for the ticket

## `result.json` shape

```json
{
  "ticket_id": "TASK-0000",
  "phase": "qa",
  "verdict": "pass",
  "summary": "qa proved the required behavior",
  "artifacts": [
    "tickets/artifacts/TASK-0000/qa/2026-04-24T210000Z/report.md"
  ]
}
```

The final Stop-hook reviewer may still fail completion even when QA `verdict` is
`pass` if the proof is too weak, too confusing, or not yet strong enough for an
internal PM-quality review.
