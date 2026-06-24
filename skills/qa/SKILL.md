---
name: qa
description: "Turn one selected ticket into proof artifacts, reconciled Done / Proof obligations, and a structured QA result for Stop-hook gating."
tier: 3
group: coding
source: local
workflow: true
eval: eval_task.json
qa_checklist: qa_checklist.md
common_chains:
  after: ["demo", "close-ticket"]
---

# QA

## Context

`qa` is the ticket-scoped proof aggregator. It reconciles a selected ticket's
`Done / Proof` and proof policy against concrete artifacts. Browser operation
belongs to `qa-tester`; visual judgment belongs to `visual-qa`; adversarial
claim testing belongs to `agent-qa-test`; sufficiency review belongs to
`reviewer`.

## Skill Signature

```text
qa(ticket, runtime_target?, proof_policy?) -> qa_artifacts + result_json + best_evidence
state: reads(ticket.md, optional design.md, runtime handoff, linked specs/docs, captured artifacts); writes(tickets/TASK-XXXX/artifacts/qa/<run>/report.md, result.json, ticket State/Links)
gates: ticket_selected; proof_policy_read; artifacts_captured; weak_proof_blocks; ui_work_has_screenshots_or_blocker
routes: qa-tester | visual-qa | agent-qa-test | review
fails: guesses runtime target; drives browser from coordinator when qa-tester is available; passes without concrete artifacts; self-certifies visual or adversarial proof
```

## Phase Boundary

This skill owns evidence collection and reconciliation only. It delegates
browser-driving to `qa-tester`, visual judgment to `visual-qa`, adversarial
claim proof to `agent-qa-test`, and final sufficiency to `review`.

<!-- BEGIN FARPLANE_IMPORTANT_CHECKLIST -->
## Todo List

- [ ] Read the selected ticket, `Done / Proof` block, linked specs/docs, and
  any runtime target handoff.
- [ ] Start the QA result with a `Ticket / Proof Policy` line naming the
  selected ticket and proof policy that were read or checked. If either is
  missing, write `Ticket / Proof Policy: missing selected ticket or proof
  policy` and return `blocked`, `revise`, or `NOT PROVABLE` instead of judging
  from loose logs.
- [ ] Use the native execution phase proof/writeback shape, but
  keep `$qa` focused on ticket-scoped evidence collection.
- [ ] If browser evidence is needed, use [agent-browser](../agent-browser/SKILL.md)
  as the browser tool surface and keep Farplane-specific artifact rules here.
  - [ ] In live Goal-backed or material runs, delegate browser/tool driving to
    `qa-tester` when available; do not self-certify from the coordinator lane.
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
- [ ] For UI/user-visible proof, require at least one best screenshot/image
  evidence item or record a blocker/revise verdict explaining why it is absent.
- [ ] Write `report.md` with the tested path, evidence links, pass/fail
  rationale, and any gaps.
- [ ] Write `result.json` with ticket id, phase, verdict, summary, and artifact
  paths.
- [ ] Update the ticket `Links` or `State` section with the strongest QA
  artifacts.
- [ ] If the proof is weak, confusing, or incomplete, return a revise/blocker
  verdict instead of claiming QA passed.
<!-- END FARPLANE_IMPORTANT_CHECKLIST -->

`$qa` is the proof-gathering phase for a selected ticket.

Use it when:

- implementation is ready for proof
- a ticket in `status: building` needs evidence before completion
- `goal-advisor` or the operator needs to rerun QA without redoing implementation

Do not use it when:

- the ticket still needs planning; use `impl-plan`
- the work is not yet implementation-ready; use `goal-advisor`

## Contract

- Read the selected ticket plus linked docs/specs.
- When `$qa` is entered from a live orchestration lane and delegation is available, keep the coordinating lane out of browser driving: spawn `qa-tester` to own browser/tool use, artifact capture, and ticket-scoped proof.
- Use [agent-browser](../agent-browser/SKILL.md) as the general browser tool
  surface when browser evidence is needed; Farplane-specific QA artifact
  policy lives in this skill, not in `agent-browser`.
- Gather ticket-scoped proof under `tickets/TASK-XXXX/artifacts/qa/`.
- For UI or user-visible work, use `visual-qa` as a separate judgment pass.
- If the ticket proof policy includes `agent_qa`, run or hand off to
  `agent-qa-test`; do not treat normal QA as adversarial proof.
- Update the ticket `Links` or `State` section with the strongest artifact
  links.
- The final QA report must identify `best_evidence`, and for UI/user-visible
  proof that item should be a screenshot/image path suitable for the operator's
  final Markdown image link.
- If the only evidence is command logs for a UI/user-visible ticket, return
  `revise`, `fail`, `blocked`, or `NOT PROVABLE`; name the missing
  `best_evidence` image path as the blocker.
- Write `result.json` under the QA artifact root and finish with:
  - `EXECUTION_RESULT: status=qa_complete next=building reason=...`

## Required artifacts

- `report.md`
- `result.json`
- supporting screenshots/logs/snapshots as needed for the ticket
- `best_evidence` path or explicit missing-evidence blocker for
  UI/user-visible tickets

## Report Start

Every QA result starts with:

```text
Ticket / Proof Policy: <ticket path or missing> / <proof policy or missing>
Verdict: pass | revise | fail | blocked | NOT PROVABLE
```

If the ticket or proof policy is missing, do not pass. If a UI ticket has only
command logs, do not pass.

## `result.json` shape

```json
{
  "ticket_id": "TASK-0000",
  "phase": "qa",
  "verdict": "pass",
  "summary": "qa proved the required behavior",
  "best_evidence": "tickets/TASK-0000/artifacts/qa/2026-04-24T210000Z/screens/final.png",
  "artifacts": [
    "tickets/TASK-0000/artifacts/qa/2026-04-24T210000Z/report.md"
  ]
}
```

The final Stop-hook reviewer may still fail completion even when QA `verdict` is
`pass` if the proof is too weak, too confusing, or not yet strong enough for an
internal PM-quality review.
