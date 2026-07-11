---
skill: self-improve
date: 2026-07-11
change_type: behavior
owner: skill-maintenance
status: pass
review_route: reviewer
before_ref: skills/self-improve/SKILL.md; skills/self-improve/references/workflows.md; skills/self-improve/eval_task.json
after_ref: skills/self-improve/SKILL.md; skills/self-improve/references/workflows.md; skills/self-improve/eval_task.json
reasoning_basis: first_principles
proof_artifacts: []
eval_required: yes
---

# Self Improve Executable Delayed Check-In Audit

## Change

- Before: delayed experiments named generic Goal sections but did not require
  a single executable check-in instruction.
- After: delayed work routes through Goal Advisor to fill `Check-In Program`;
  immediate work explicitly avoids those fields.
- Why: experiment setup must leave enough policy for a later worker without
  burdening immediate eval loops.
- Tradeoff accepted: delayed setup is stricter before entering
  `waiting_signal`.

## First-Principles Reasoning

- Objective: make both feedback classes minimal and executable.
- Placement logic: Self Improve classifies and supplies experiment context;
  Goal Advisor compiles; Pulse dispatches.
- Expected behavior delta: delayed packets cannot wait with implicit policy,
  while immediate packets do not manufacture future machinery.
- Proof needed: immediate/delayed eval reference points and skill validation.

## Binary Rubric

| Check | Verdict | Evidence |
| --- | --- | --- |
| `first_load_sufficiency` | pass | Classification gate names executable delayed program and immediate not-applicable route. |
| `reference_load_precision` | pass | Exact packet fields remain in the delayed workflow reference. |
| `missing_context_rate` | pass | First load routes to Goal Advisor before waiting. |
| `noisy_context_rate` | pass | Field-level procedure stays conditional in the workflow reference. |
| `duplicated_instruction_count` | pass | Self Improve supplies context but does not own due-row dispatch. |
| `prompt_size_tokens` | pass | First load grew from 169 to 174 lines and remains below the review threshold. |
| `task_success_rate` | unknown | Requires a real delayed experiment. |
| `review_tas_rate` | unknown | Pending TASK-0320 reviewer. |
| `maintenance_locality` | pass | Timing classification remains in Self Improve. |
| `composition_clarity` | pass | Immediate and delayed routes name distinct owners and outputs. |

## Proof Artifacts

- Skill-local evals: updated immediate and delayed feedback cases
- Structure evals: skill validator
- Reviewer receipt: pending TASK-0320 completion review
- Validator: pending focused validation
- Eval required: yes
- Evidence gaps: no live delayed experiment run yet

## Before Behavior

- Delayed setup could reach `waiting_signal` without one runnable scorer.

## After Behavior

- Delayed setup requires an executable program; immediate setup carries only a
  compact not-applicable reason.

## Followups

- Verify the first real experiment's `monitor` path schedules its next row
  without modifying completed history.
