---
skill: self-improve
date: 2026-07-22
change_type: behavior
owner: skill-maintenance
status: pass
review_route: reviewer
before_ref: skills/self-improve/SKILL.md@pre-TASK-0401
after_ref: skills/self-improve/SKILL.md@TASK-0401
reasoning_basis: deliberative_advice
proof_artifacts:
  - .farplane/evals/runs/20260721-193727-task-0401-composition-repair
eval_required: yes
---

# Leverage-Replanned Self Improvement

## Change

- Before: harden and refine used fixed phase policy after baseline.
- After: Leverage Advisor chooses every bounded experiment from the
  `program.md` roadmap, `progress.md` learnings, current Eval evidence, and
  remaining phase budget.
- Why: failed or guard-breaking candidates must change the next move.
- Tradeoff accepted: one extra named decision checkpoint per round in exchange
  for replayable, evidence-sensitive selection.

## First-Principles Reasoning

- Objective: reach the behavior floor, then minimize instruction length without
  wasting rounds on invalid or low-leverage moves.
- Placement logic: Self Improve executes skill experiments; Leverage Advisor
  selects; Goal Advisor compiles continuation; Eval measures.
- Expected behavior delta: prerequisites, rejected alternatives, and learned
  constraints affect every next harden/refine experiment.
- Proof needed: an eval must defer an invalid candidate, choose one attributable
  edit, and append the full selection/evidence decision to progress.

## Binary Rubric

| Check | Verdict | Evidence |
| --- | --- | --- |
| `first_load_sufficiency` | pass | Mandatory composition and active-turn report expose every owner and input. |
| `reference_load_precision` | pass | Detailed phase mechanics stay in existing references. |
| `missing_context_rate` | pass | The repaired eval explicitly refuses to invent missing evidence. |
| `noisy_context_rate` | pass | No runner, registry, or target-local state was added. |
| `duplicated_instruction_count` | pass | Selection mechanics remain owned by Leverage Advisor. |
| `prompt_size_tokens` | pass | Change is skill-local and compact. |
| `task_success_rate` | pass | Self Improve replanning eval returned A. |
| `review_tas_rate` | pass | TASK-0401 final review returned TAS-A. |
| `maintenance_locality` | pass | Changes stay in the skill, references, and eval. |
| `composition_clarity` | pass | Selector, compiler, evaluator, executor, and state owners are explicit. |

## Proof Artifacts

- Skill-local evals: Self Improve replanning A in the listed Eval run.
- Structure evals: `quick_validate.py`, `check_skills.py --write`.
- Reviewer receipt: `tickets/TASK-0401/artifacts/review/final-review.md`.
- Validator: eval query lint and JSON parsing pass.
- Eval required: yes.
- Evidence gaps: none for the composition change.

## Before Behavior

- Candidate order could remain effectively fixed inside a phase.

## After Behavior

- Every phase round is reselected from the roadmap plus accumulated evidence;
  rejected alternatives and learned constraints are written back.

## Followups

- None unless real campaign evidence exposes a missing selector input.
