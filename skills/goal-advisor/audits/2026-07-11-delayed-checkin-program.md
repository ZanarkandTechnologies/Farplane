---
skill: goal-advisor
date: 2026-07-11
change_type: behavior
owner: skill-maintenance
status: pass
review_route: reviewer
before_ref: skills/goal-advisor/SKILL.md; skills/goal-advisor/references/prompt-templates.md; tickets/templates/goal-loop/program.md
after_ref: skills/goal-advisor/SKILL.md; skills/goal-advisor/references/prompt-templates.md; skills/goal-advisor/qa_checklist.md; skills/goal-advisor/eval_task.json; tickets/templates/goal-loop/program.md
reasoning_basis: first_principles
proof_artifacts: []
eval_required: yes
---

# Goal Advisor Delayed Check-In Program Audit

## Change

- Before: delayed experiment policy could be reconstructed from Metric,
  Heartbeat, Stop, Rollout, and Pulse handoff prose.
- After: Goal Advisor compiles one executable `Check-In Program` into the
  original packet; immediate packets keep only `mode: not_applicable`.
- Why: a resumed worker needs one experiment-local instruction while Pulse
  remains only the due-row dispatcher.
- Tradeoff accepted: the Goal Program template gains one conditional section
  in exchange for eliminating duplicated runtime reasoning.

## First-Principles Reasoning

- Objective: make delayed scoring resumable, attributable, and idempotent.
- Placement logic: Goal Advisor already compiles `program.md`; it is the one
  owner that can bind experiment evidence and ticket policy before the wait.
- Expected behavior delta: a check-in worker executes the packet instead of
  inventing policy from scattered fields.
- Proof needed: JSON parse, template assertions, skill validator, and composed
  lifecycle QA.

## Binary Rubric

| Check | Verdict | Evidence |
| --- | --- | --- |
| `first_load_sufficiency` | pass | Signature, gates, and todo require compiling the delayed program. |
| `reference_load_precision` | pass | Resume prompt stays in the prompt reference loaded only for emission. |
| `missing_context_rate` | pass | Required inputs, procedure, writeback, decisions, idempotency, and source-gap behavior are named. |
| `noisy_context_rate` | pass | Immediate packets retain only a not-applicable reason. |
| `duplicated_instruction_count` | pass | Program owns policy; resume prompt only supplies runtime inputs. |
| `prompt_size_tokens` | unknown | First load grew from 447 to 460 lines; existing Goal Advisor breadth remains a future refinement candidate. |
| `task_success_rate` | unknown | Requires the first real delayed check-in run. |
| `review_tas_rate` | unknown | Pending TASK-0320 reviewer. |
| `maintenance_locality` | pass | Compiler behavior stays in Goal Advisor and the canonical Goal Program template. |
| `composition_clarity` | pass | Goal Advisor compiles; Pulse dispatches; worker executes. |

## Proof Artifacts

- Skill-local evals: `goal_advisor_delayed_checkin_program_01`
- Structure evals: skill validator and Goal Advisor QA checklist
- Reviewer receipt: pending TASK-0320 completion review
- Validator: pending focused validation
- Eval required: yes
- Evidence gaps: no live delayed check-in yet

## Before Behavior

- A worker could need Pulse prose or reconstruct decision rules from several
  generic Goal Program sections.

## After Behavior

- A delayed packet is incomplete until `Check-In Program` is executable; a
  resumed worker reads it first and immediate work carries no delayed workflow.

## Followups

- Use the first live delayed experiment to verify idempotent retry and
  below-minimum evidence behavior.
