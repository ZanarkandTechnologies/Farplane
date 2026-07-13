---
ticket_id: TASK-0356
artifact_type: qa-eval-summary
status: pass
created_at: 2026-07-14T04:15:00+08:00
---

# QA Skill Eval Summary

## Result

All five representative QA behaviors reached TAS-A in one fixture-backed run.
Every generated receipt also passed the skill-local schema, `QA_RESULT`, and
existing-artifact validator.

| Case | Final TAS | Evidence |
| --- | --- | --- |
| complete CLI proof | A | `20260713-203845-task-0356-qa-final-reviewed` |
| UI proof missing image | A | `20260713-203845-task-0356-qa-final-reviewed` |
| claim/evidence mismatch | A | `20260713-203845-task-0356-qa-final-reviewed` |
| unavailable external source | A | `20260713-203845-task-0356-qa-final-reviewed` |
| runtime, writeback, and learning | A | `20260713-203845-task-0356-qa-final-reviewed` |

Generated summaries:

- `.farplane/evals/runs/20260713-203845-task-0356-qa-final-reviewed/summary.json`

The final run reached `pass_rate: 1.0` with five A verdicts. A second mechanical
gate then parsed each answer's canonical JSON block, ran
`validate_qa_result.py`, required `QA_RESULT` to point at `result.json`, and
confirmed every evidence and judgment path named by the receipt exists.
It also requires the `QA_RESULT` verdict to match the JSON receipt verdict.

## Findings Repaired During the Eval Loop

1. The initially invoked installed runner was stale and expected retired
   `skills/*/eval_task.json` files. The ticket now uses the repo-owned runner:
   `skills/eval/scripts/run_evals.py`.
2. Early fixture prompts demanded concrete artifact paths without supplying
   them. The fixtures now provide explicit clean-room ticket, runtime, and
   evidence paths so the skill is never rewarded for invention.
3. The validator originally required image `best_evidence` even for a UI run
   blocked because no screenshot existed. It now requires concrete best
   evidence for passes while allowing `null` on an honest non-pass with an
   explicit blocker.
4. Source-gap behavior now preserves deterministic local checks without
   substituting them for unavailable external proof.
5. Candidate shortcuts remain `ticket_only` before capture and become
   `cookbook_update` with a concrete cookbook ref only after verification.
6. Current-schema fixture tickets and evidence now live under
   `skills/qa/evals/fixtures/`; eval prompts read those files rather than
   narrating phantom proof.
7. Passing proof policies containing `visual-qa`, `agent-qa-test`, or
   `reviewer` now require a matching judgment receipt path.
8. The reusable-learning case is phrased as a natural operator problem; its
   prompt no longer supplies the routing, learning transition, receipt fields,
   or conditional writeback answer.

## Residual Risk

These cases prove the Farplane QA contract and agent behavior at the harness
level. They do not replace browser QA for a downstream application ticket.
