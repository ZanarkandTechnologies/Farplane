---
skill: skill-creator
date: 2026-06-21
change_type: behavior
owner: skill-maintenance
status: pass
review_route: self_check
before_ref: skills/skill-creator/SKILL.md
after_ref: skills/skill-creator/SKILL.md
reasoning_basis: first_principles
proof_artifacts:
  - skills/skill-maintenance/qa_checklist.md
eval_required: no
---

# Skill Audit

## Change

- Before: `skill-creator` ran the structure checklist conditionally, and
  behavior proof was not an explicit finish gate for prompt-like skill changes.
- After: every skill create/update invocation must apply the structure
  checklist to changed surfaces, and behavior-sensitive skill work must run an
  eval, `agent-behavior-test`, or skill-local QA scenario before readiness.
- Why: structure validation alone can miss agent-comprehension failures, such
  as compressing required persona prompts or routing to the wrong skill.
- Tradeoff accepted: tiny mechanical skill edits now carry a compact checklist
  pass, but only behavior-sensitive work pays for stronger proof.

## First-Principles Reasoning

- Objective: make new and updated skills prove both structure and usable
  behavior before the creator declares them done.
- Placement logic: the rule belongs in `skill-creator` because it is the point
  where new skill packages and skill behavior changes are authored.
- Expected behavior delta: creators will always name checklist outcomes, and
  new prompt/program/router/budget skills will include or run behavioral proof.
- Proof needed: registry validation plus self-check against the structure
  checklist for the changed `skill-creator` contract.

## Binary Rubric

| Check | Verdict | Evidence |
| --- | --- | --- |
| `first_load_sufficiency` | pass | `SKILL.md` now says the checklist is required for every create/update invocation. |
| `reference_load_precision` | pass | The checklist link points directly to `../skill-maintenance/qa_checklist.md`. |
| `missing_context_rate` | pass | Behavior proof requirements are in the finish gate, not hidden in a reference. |
| `noisy_context_rate` | pass | The added rules are compact gates, not tutorial prose. |
| `duplicated_instruction_count` | pass | The structure checklist still owns detailed checks; `skill-creator` owns when to run them. |
| `prompt_size_tokens` | pass | `SKILL.md` is 253 lines after the edit, near the soft budget and still mostly gates/routing. |
| `task_success_rate` | unknown | Needs future behavior-test evidence across real skill-creator invocations. |
| `review_tas_rate` | unknown | No reviewer lane was run for this small policy tightening. |
| `maintenance_locality` | pass | Future authors update the creator gate in `SKILL.md` and checklist details in `qa_checklist.md`. |
| `composition_clarity` | pass | Finish gate names structure checklist, eval, behavior-test, and skill-local QA proof surfaces. |

## Proof Artifacts

- Skill-local evals, when needed: not required for this instruction-only creator
  tightening.
- Structure evals, when needed: self-check against
  `skills/skill-maintenance/qa_checklist.md`.
- Reviewer receipt: not run; change is scoped to explicit finish-gate wording.
- Validator: `python3 skills/skill-maintenance/scripts/check_skills.py --write`
  passed after the edit and refreshed generated registry/intelligence files.
- Eval required: no.
- Evidence gaps: future real invocations should show whether agents consistently
  record compact checklist verdicts instead of treating the line as decoration.

## Before Behavior

- A creator could treat the structure checklist as conditional and rely on
  `check_skills.py` even when the risk was behavioral comprehension.

## After Behavior

- A creator must run the structure checklist for changed skill surfaces, and a
  behavior-sensitive skill change must run or explicitly route behavior proof.

## Followups

- Promote recurring missed behavior-proof cases into a skill-local
  `qa_checklist.md` only after several examples show a stable reusable check.
