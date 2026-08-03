---
name: qa
description: "Turn one selected ticket into proof artifacts, reconciled Done and QA Strategy obligations, and a structured QA result for Goal/ticket completion."
tier: 3
group: coding
source: local
template_uses:
  skill-template: "0.3.8"
  skill-surface-budget: "0.1.0"
  skill-eval-task: "0.2.0"
eval: evals/evals.json
qa_checklist: qa_checklist.md
common_chains:
  after: ["demo", "close-ticket"]
---

# QA

## Context

Use `qa` when an implementation-ready ticket needs ticket-scoped proof before
completion or when the operator needs to rerun proof without redoing the build.
It reconciles the selected ticket's `Done`, `QA Strategy`, optional `Agent
Contract`, and explicit proof-policy override against concrete artifacts.

Do not use it for unfinished planning; use `impl-plan` or `goal-advisor` at
that earlier boundary. Browser operation belongs to `qa-tester`, visual
judgment to `visual-qa`, adversarial agent proof to `agent-qa-test`, and final
sufficiency judgment to `reviewer`.

## Skill Signature

```text
qa(ticket, runtime_target?, proof_policy_override?)
  -> qa_artifacts + result_json + best_evidence + learning_decision
state:
  reads(ticket.md, optional design.md, runtime handoff, linked specs/docs,
        cookbook entry?, captured artifacts)
  writes(tickets/TASK-XXXX/artifacts/qa/<run>/{report.md,result.json},
         ticket Links, optional progress.md entry)
gates:
  ticket_selected; effective_proof_policy_read; runtime_bound_or_not_needed;
  artifacts_captured; result_validated; weak_proof_blocks;
  ui_work_has_screenshots_or_blocker; required_judgments_linked;
  learning_classified
routes: qa-tester | visual-qa | agent-qa-test | reviewer
fails:
  guesses runtime target; reads retired ticket sections; drives browser from
  coordinator when qa-tester is available; passes without concrete artifacts;
  self-certifies visual or adversarial proof; writes an invalid receipt
```

## Phase Contract

```text
qa_phase(ticket, bound_inputs, current_state)
  -> effective_proof_policy + captured_evidence
   + required_judgment_receipts + validated_result_json
   + ticket_writeback + learning_decision
```

Follow Tier 0 phases inline: ground the claim, choose the cheapest faithful
proof path, capture and reconcile evidence, apply guardrails, obtain required
independent judgment, then write back the validated receipt.

## Phase Boundary

This skill owns evidence collection, reconciliation, receipt validation, and
ticket writeback. Delegate operated browser capture to `qa-tester`; use
`visual-qa`, `agent-qa-test`, or `reviewer` only when the proof policy requires
their distinct judgment. Keep one primary journey owner from setup through
state change, failure check, result, and receipt; do not create one lane per
checklist item.

<!-- BEGIN FARPLANE_IMPORTANT_CHECKLIST -->
## Todo List

- [ ] 1. Bind the ticket and proof policy.
  - [ ] Read [qa_checklist.md](qa_checklist.md) before material QA as preflight
    guardrails; apply it again before completion.
  - [ ] Read the selected ticket's `Done`, `QA Strategy`, linked specs/docs,
    runtime handoff, and optional `Agent Contract`.
  - [ ] Build the effective policy from those sources plus an explicit caller
    override. An override may tighten or specialize proof, not erase ticket
    obligations.
  - [ ] If the ticket or policy is missing, return a non-pass result instead of
    judging loose logs.
- [ ] 2. Choose the proof branch and bind testability.
  - [ ] For browser, UI, or API proof, bind the runtime from the ticket,
    explicit caller handoff, or a verified cookbook entry; never guess a port,
    URL, process, account, fixture, or stale session.
  - [ ] When a matching `qa/cookbook/*.md` entry exists, use its verified fast
    entry, setup, reset, and verification path before manual exploration. The
    cookbook accelerates capture; it does not prove the current run passed.
  - [ ] CLI/artifact proof may use logs or generated files. Browser/UI proof
    requires a bound runtime and screenshot/image evidence.
- [ ] 3. Create the run and capture claim-matched evidence.
  - [ ] Create `tickets/TASK-XXXX/artifacts/qa/<timestamp>-<slug>/`.
  - [ ] Capture the relevant commands, exit status, responses, generated files,
    screenshots, snapshots, console logs, page errors, traces, or API evidence.
  - [ ] For material browser work, delegate operation and capture to
    `qa-tester`, which uses the Codex in-app Browser; the coordinating lane
    must not self-certify operated proof.
  - [ ] If an external source is unavailable, still record independent
    deterministic local checks, preserve the source gap, and never substitute
    an invented observation.
- [ ] 4. Reconcile the critical path and failure risk.
  - [ ] Map every `Done` and `QA Strategy` obligation to `PASS`, `FAIL`, or
    `not_provable` plus a concrete artifact.
  - [ ] Confirm the claimed workflow/lifecycle is named, ordered sanity checks
    ran where feasible, and every unrun full-path step is residual risk or a
    blocker.
  - [ ] Exercise the most relevant failure, constraint, stale-state, or
    regression risk. Stop with a non-pass verdict when current hooks cannot
    faithfully observe the claim.
- [ ] 5. Obtain distinct judgments when required.
  - [ ] For UI/visual claims, hand screenshots and context to
    [Visual QA](../visual-qa/SKILL.md); browser capture is not visual approval.
  - [ ] When the policy requires `agent-qa-test`, run or hand off adversarial
    agent proof instead of treating normal QA as that judgment.
  - [ ] When the policy requires `reviewer`, link its independent receipt; do
    not make the implementer self-approve material completion.
- [ ] 6. Write and validate the receipt.
  - [ ] Write `report.md` with the tested path, obligation-to-evidence map,
    verdict rationale, blockers, residual risk, and learning outcome.
  - [ ] Write the complete canonical `result.json` from `## Templates`, then
    run `python3 skills/qa/scripts/validate_qa_result.py <result.json>`.
  - [ ] For an explicitly read-only pre-capture preview, emit the same complete
    schema inline, list only existing context/source artifacts, use a non-pass
    verdict with `best_evidence: null` when required evidence is absent, and
    finish with `evidence=inline-result.json` without claiming a file was
    written.
- [ ] 7. Write back and classify learning.
  - [ ] Executed runs always update ticket `Links` with report, receipt,
    verdict, and strongest evidence. Append `progress.md` only when it already
    exists, the run is Goal-backed, or blocker/review state needs an append-only
    entry. A read-only preview describes but does not claim this writeback.
  - [ ] Classify learning as `ticket_only`, `cookbook_update`, or
    `instrumentation_ticket`. Candidate shortcuts stay `ticket_only` before
    capture; after verified reuse, use `cookbook_update` with the concrete
    cookbook ref. Create an instrumentation follow-up only for real missing
    implementation.
- [ ] 8. Apply the finish gate.
  - [ ] Reapply [qa_checklist.md](qa_checklist.md) and confirm the runtime,
    evidence branch, five gates, judgment receipts, writeback, and learning
    outcome agree across `report.md` and `result.json`.
  - [ ] Return `revise`, `fail`, `blocked`, or `not_provable` when proof is
    weak, confusing, incomplete, invalid, or missing required image/judgment
    evidence.
<!-- END FARPLANE_IMPORTANT_CHECKLIST -->

## Templates

Every report starts with:

```text
Ticket / Proof Policy: <ticket path or missing> / <proof policy or missing>
Verdict: pass | revise | fail | blocked | not_provable
```

Canonical `result.json`:

```json
{
  "schema_version": "1",
  "ticket_id": "TASK-0000",
  "phase": "qa",
  "proof_type": "ui",
  "runtime_target": "http://127.0.0.1:3000",
  "proof_policy": "Done + QA Strategy + Agent Contract",
  "verdict": "pass",
  "summary": "qa proved the required behavior",
  "gate_results": {
    "contract": "pass",
    "mechanism": "pass",
    "journey": "pass",
    "adversarial": "pass",
    "receipt": "pass"
  },
  "best_evidence": "tickets/TASK-0000/artifacts/qa/run/screens/final.png",
  "artifacts": [
    "tickets/TASK-0000/artifacts/qa/run/report.md",
    "tickets/TASK-0000/artifacts/qa/run/screens/final.png"
  ],
  "blockers": [],
  "residual_risk": [],
  "judgment_receipts": [],
  "learning": {
    "outcome": "ticket_only",
    "ref": null
  }
}
```

## Gotchas

- Do not read retired ticket `Plan`, `Acceptance Criteria`, `Verification`,
  `Evidence`, `Blockers`, or `State` sections as current QA truth.
- Do not fabricate completed commands, interactions, artifacts, judgments,
  screenshots, zero values, or future paths to satisfy the receipt schema.
- Do not point `QA_RESULT.evidence` at `best_evidence`; it names the validated
  `result.json` receipt. Browser capture, visual judgment, adversarial proof,
  and completion review remain distinct ownership surfaces.

## Reference Map

- [QA checklist](qa_checklist.md) — read before material execution and apply
  again at the finish gate.
- Codex in-app Browser — use through `qa-tester` when browser operation is
  required.
- [Visual QA](../visual-qa/SKILL.md) — load after UI capture when visual
  judgment is required.
- `qa/cookbook/*.md` — read the matching project runbook before manual
  exploration; update it only after a reusable path is verified.

## Output

Executed QA writes `report.md`, canonical `result.json`, and the supporting
artifacts required by the selected proof type under the ticket QA run folder.
It finishes with:

```text
QA_RESULT: verdict=<pass|revise|fail|blocked|not_provable> evidence=<result.json path> reason=<short reason>
```

Receipt invariants:

- `proof_type` is `cli | api | browser | ui | artifact | agent`; all five gate
  keys exist with `pass | fail | blocked`.
- `artifacts` is non-empty. A concrete `best_evidence` also appears there.
- A pass has all gates passing, concrete best evidence, and no blockers. A
  non-pass has at least one blocker and may use `best_evidence: null` when the
  required artifact does not exist.
- Browser/UI passes require a bound runtime and image best evidence; API proof
  requires a bound runtime. CLI/artifact proof may use logs or files.
- `ticket_only` uses `learning.ref: null`; `cookbook_update` and
  `instrumentation_ticket` require a non-empty ref.
- Passing policies containing `visual-qa`, `agent-qa-test`, or `reviewer`
  require a matching judgment receipt path.

Final ticket or Goal review may still reject completion when a structurally
valid QA pass is too weak, confusing, or incomplete for material readiness.
