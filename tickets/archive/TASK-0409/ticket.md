---
template_id: ticket-template
template_version: "0.2.3"
feature_refs:
  - FEAT-0007
  - FEAT-0070
ticket_id: TASK-0409
title: "Stop completion learning from inventing QA preflight gates"
status: done
priority: high
created_at: 2026-07-25T15:45:57.020968Z
updated_at: 2026-07-26T15:53:29.369479Z
---
# TASK-0409: Stop completion learning from inventing QA preflight gates

## Summary

TASK-0408's first QA pass correctly returned `revise` because its proof was
incomplete. Completion learning misclassified that successful QA correction
loop as a harness defect and proposed a new pre-QA evidence gate.

The fix belongs in completion learning, not QA. Mining must distinguish inputs
needed to make QA runnable from evidence QA owns collecting and external facts
that can only arrive later.

## Scope

- In:
  - classify missing proof as a testability prerequisite, QA-owned evidence, or
    delayed external signal
  - prevent QA-owned evidence and delayed signals from producing pre-QA gate
    findings
  - preserve legitimate findings when QA could not start because a runtime,
    fixture, credential, or other testability prerequisite was missing
- Out:
  - a new pre-QA validator
  - changes to QA's existing revise/pass/not-provable behavior
  - reopening TASK-0408

## Delta

```text
before:
  completed_after_qa_rerun:
    - miner sees evidence missing on the first QA pass
    - miner treats the rerun as avoidable work
    - miner proposes a pre-QA evidence validator
after:
  completed_after_qa_rerun:
    - miner classifies what was missing
    - QA-owned evidence is expected correction-loop work and produces no finding
    - delayed external facts become waiting signals, not QA prerequisites
    - only missing testability inputs may produce a readiness improvement
why_now:
  TASK-0409 is itself evidence that the completion learner produced a false positive
```

## Program

```yaml
mode: improve
owner_surface: completion_learning_program
confidence: high
instruction: "Correct the classifier that generated this ticket; do not add a QA gate."
```

## Done / Proof

- [x] The active completion-learning program explicitly distinguishes
      testability prerequisites, QA-owned evidence, and delayed external facts.
- [x] The program rejects pre-QA gate findings for evidence QA owns collecting.
- [x] The program routes delayed external facts to a waiting/check-in signal
      rather than QA preflight.
- [x] A focused regression check locks the classification contract.
- [x] Existing mining tests and route validation pass.

## Links

- `tickets/archive/TASK-0408/ticket.md`
- `.farplane/mine/runs/73bb407506948934fe0404db469c830e988d6b29a97b3cf56dab15c0aa0d3253/report.json`
- `tickets/TASK-0409/artifacts/validation/completion-learning-proof.json`
- `tickets/TASK-0409/artifacts/review/completion-receipt.json`
- `tickets/archive/TASK-0408/progress.md`
- `tickets/archive/TASK-0408/artifacts/qa/evidence-review.json`

## Notes

- `completion_learning_fingerprint: 79fdafb50bc084c15f77ccbe647ad010cc27bd9517d7c141ce1c4a2eaf84147f`
- `completion_learning_key: missing_evidence_preflight`
- `completion_learning_depth: 1`
- `source_event_id: cac0276fc6856066b5fce3119068c19bfc5f91692c3b2c6d027b942b447483b1`
- `generated_by: core:ticket-completion-learning`
