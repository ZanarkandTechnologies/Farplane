---
name: qa
description: Run the QA phase for one selected ticket by collecting proof artifacts, reconciling acceptance criteria, and producing a structured QA result artifact for Stop-hook gating.
tier: 3
group: coding
source: local
common_chains:
  after: ["demo", "close-ticket"]
---

# QA

<!-- BEGIN CODEXTER_IMPORTANT_CHECKLIST -->
## Important Checklist

- [ ] Read the selected ticket, Proof Contract, acceptance criteria, linked
  specs/docs, and any runtime target handoff.
- [ ] Use the generic [execute](../execute/SKILL.md) proof/writeback shape, but
  keep `$qa` focused on ticket-scoped evidence collection.
- [ ] If browser evidence is needed, use [agent-browser](../agent-browser/SKILL.md)
  as the browser tool surface and keep Codexter-specific artifact rules here.
- [ ] If a live app/API target is ambiguous, require a runtime record from
  [pr-runtime](../pr-runtime/SKILL.md) or record the blocker instead of guessing
  ports from chat.
- [ ] Create a run folder under
  `tickets/TASK-XXXX/artifacts/qa/<timestamp>-<slug>/`.
- [ ] Capture the relevant evidence: command outputs, screenshots, snapshots,
  console logs, page errors, API responses, traces, or generated artifacts.
- [ ] For browser proof, prefer a snapshot before interaction, screenshots for
  important states, and console/page-error logs when the UI is user-visible.
- [ ] For UI or visual judgment, hand screenshots and context to
  [visual-qa](../visual-qa/SKILL.md) as a separate judgment pass.
- [ ] Write `report.md` with the tested path, evidence links, pass/fail
  rationale, and any gaps.
- [ ] Write `result.json` with ticket id, phase, verdict, summary, and artifact
  paths.
- [ ] Update the ticket Evidence section with the strongest QA artifacts.
- [ ] If the proof is weak, confusing, or incomplete, return a revise/blocker
  verdict instead of claiming QA passed.
<!-- END CODEXTER_IMPORTANT_CHECKLIST -->

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
- When `$qa` is entered from a live orchestration lane and delegation is available, keep the coordinating lane out of browser driving: spawn `qa-tester` to own browser/tool use, artifact capture, and ticket-scoped proof.
- Use [agent-browser](../agent-browser/SKILL.md) as the general browser tool
  surface when browser evidence is needed; Codexter-specific QA artifact
  policy lives in this skill, not in `agent-browser`.
- Gather ticket-scoped proof under `tickets/TASK-XXXX/artifacts/qa/`.
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
    "tickets/TASK-0000/artifacts/qa/2026-04-24T210000Z/report.md"
  ]
}
```

The final Stop-hook reviewer may still fail completion even when QA `verdict` is
`pass` if the proof is too weak, too confusing, or not yet strong enough for an
internal PM-quality review.
