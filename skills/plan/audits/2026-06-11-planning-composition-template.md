---
skill: plan
date: 2026-06-11
change_type: structure
owner: skill-maintenance
status: pass
review_route: self_check
before_ref: skills/plan/SKILL.md@bd880ba
after_ref: skills/plan/SKILL.md
reasoning_basis: first_principles
proof_artifacts:
  - python3 skills/skill-maintenance/scripts/check_skills.py --write
  - python3 bin/validators/check_tier0_phase_protocol.py
eval_required: no
---

# Skill Audit

## Change

- Before: `plan` was described as a deprecated compatibility wrapper for the
  native Tier 0 planning phase.
- After: `plan` is a Tier 2 planning prompt-template function for grounding
  budgets, skill-todo composition, strategy choices, review loops, proof
  targets, and handoff.
- Why: Tier 0 owns the universal planning phase, but a reusable planning skill
  is still useful when the next phase needs a better task-specific todo list or
  workflow composition.
- Tradeoff accepted: Keep `plan` callable without making it a mandatory
  dependency for every skill invocation; expose review loops as a budget knob
  rather than a default extra phase.

## First-Principles Reasoning

- Objective: reduce wasted search and unclear workflow composition before
  expensive research, implementation, or review phases.
- Placement logic: `plan` belongs as Tier 2 because many Tier 3 workflows can
  benefit from the same planning prompt-template, while Tier 0 remains the
  always-present phase protocol.
- Expected behavior delta: agents invoke `plan` when planning itself needs
  budgeted grounding, skill-todo composition, review-loop control, or
  proof-bearing handoff; they do not invoke it just because a task has a
  planning phase.
- Proof needed: skill registry remains valid, todo tier checks pass, and the
  Tier 0 guard still prevents `plan`/`execute` from becoming routine todo
  dependencies.

## Binary Rubric

| Check | Verdict | Evidence |
| --- | --- | --- |
| `first_load_sufficiency` | pass | `SKILL.md` includes context, signature, budget types, phase contract, executable todo list, modes, output, and guardrails. |
| `reference_load_precision` | pass | No extra references are required for first-load behavior. |
| `missing_context_rate` | pass | Todo step 1 binds task, phase, active skills, constraints, and budget. |
| `noisy_context_rate` | pass | The skill keeps conceptual detail compact and mode-driven. |
| `duplicated_instruction_count` | pass | Shared skill-system rules stay in docs; `plan` only owns planning-template behavior. |
| `prompt_size_tokens` | pass | Single-file first-load contract is longer than the old wrapper but still focused. |
| `task_success_rate` | unknown | No runnable eval exists yet for planning quality. |
| `review_tas_rate` | unknown | No reviewer receipt was requested for this draft. |
| `maintenance_locality` | pass | Changes are local to `plan` plus canonical docs and generated registry surfaces. |
| `composition_clarity` | pass | Signature and modes explicitly distinguish direct binding, composition, advice, research, prototype, review plans, and bounded review loops. |

## Proof Artifacts

- Skill-local evals, when needed: not added in this pass.
- Structure evals, when needed: covered by skill maintenance validators.
- Reviewer receipt: not requested; self-check used for this draft.
- Validator: `python3 skills/skill-maintenance/scripts/check_skills.py --write`.
- Eval required: no.
- Evidence gaps: future plan-quality evals could test whether `plan` composes
  multiple skill todo lists without bloating the output.

## Before Behavior

- `$plan` mostly acted as a legacy wrapper over native planning behavior.
- It preserved useful planning output headings but did not clearly model
  budgets, skill-todo composition, or subagent/council escalation as parameters.

## After Behavior

- `$plan` is a callable planning function:
  `plan(task, context?, active_skills?, phase?, budget?) -> plan_packet + composed_todos + proof_target + handoff`.
- It makes grounding/search/compute/time/review budget explicit, including
  `ReviewBudget.depth`, loop count, stop condition, and rubric.
- It treats subagents as a budgeted parameter instead of a default behavior.

## Followups

- Add a small `skills/plan/eval_task.json` once plan-quality eval criteria are
  stable enough to judge composition behavior.
