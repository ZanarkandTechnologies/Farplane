---
title: Eval Skill Batch 01 Feedback Request
owner: skills/eval
status: waiting-for-feedback
run: 1
updated: 2026-06-11
---

# Eval Skill Batch 01 Feedback Request

Please review the first eval-for-eval seed batch.

## Artifacts

- Program memory:
  `skills/eval/self-improve/program.md`
- Candidate eval tasks:
  `skills/eval/eval_task.json`
- Internal review:
  `skills/eval/audits/2026-06-11-eval-for-eval-batch-01.md`
- Smoke proof:
  `.farplane/evals/runs/20260611-052148-eval-skill-smoke/summary.json`

## Review Question

Should this four-task batch become the seed pattern for how we write evals for
the `eval` skill, or should batch 01 be smaller/different before we continue?

Please judge:

- Are the queries realistic enough?
- Are the reference points visible enough to grade?
- Is the batch too broad for the first eval-for-eval pass?
- Should the skill-structure placement case stay in `skills/eval/eval_task.json`
  or move later to a cross-skill suite?

## Feedback Shape

```json
{
  "run": 1,
  "verdict": "accept | revise | reject",
  "feedback": "What feels good or wrong about the eval-writing pattern.",
  "next_instruction": "The next change to make before rollout."
}
```
