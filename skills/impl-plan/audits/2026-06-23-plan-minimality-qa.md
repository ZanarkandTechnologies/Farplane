---
skill: impl-plan
date: 2026-06-23
change_type: behavior
owner: skill-maintenance
status: pass
review_route: self_check
before_ref: skills/impl-plan/SKILL.md@pre-plan-minimality-qa
after_ref: skills/impl-plan/SKILL.md
reasoning_basis: first_principles
proof_artifacts:
  - skills/impl-plan/qa_checklist.md
eval_required: no
---

# Skill Audit

## Change

- Before: `impl-plan` checked ticket-first planning, proof routes, maps, and
  review handoff, but did not explicitly challenge over-scoped plans.
- After: material plans must pass a minimality and reuse challenge covering
  smallest required version, existing seams, least parameters, necessary
  functions/files, real split boundaries, and concrete proof routes.
- Why: planning should push back before build when a ticket can be satisfied
  through reuse or a smaller owner-local edit.
- Tradeoff accepted: keep the detailed checklist in `qa_checklist.md` and only
  add first-load trigger/gate text to `SKILL.md`.

## First-Principles Reasoning

- Objective: make `impl-plan` reject bloated implementation plans before
  execution.
- Placement logic: `SKILL.md` owns the gate and invocation rule;
  `qa_checklist.md` owns the reusable runtime checks.
- Expected behavior delta: generated implementation plans now surface
  `revise` or `block` when they propose avoidable new parameters, functions,
  files, abstractions, splits, or proof gaps.
- Proof needed: source diff, checklist self-check, and skill-system validator.

## Binary Rubric

| Check | Verdict | Evidence |
| --- | --- | --- |
| `first_load_sufficiency` | pass | `SKILL.md` signature now includes `minimal_plan_challenge_passed`; Todo List links the checklist before accepting material plans. |
| `reference_load_precision` | pass | The Todo List and workflow say to load `qa_checklist.md` before accepting a material plan. |
| `missing_context_rate` | pass | Minimality, reuse, parameter, file, function, split, and proof-route gates remain visible in first load or the directly linked checklist. |
| `noisy_context_rate` | pass | Detailed QA tasks live in `qa_checklist.md`, not expanded inline in the Todo List. |
| `duplicated_instruction_count` | pass | `SKILL.md` names the gate; `qa_checklist.md` owns the checklist details. |
| `prompt_size_tokens` | unknown | `SKILL.md` was already 560 lines and is now 574 lines; this change does not resolve existing size debt. |
| `task_success_rate` | unknown | No live `impl-plan` run artifact yet. |
| `review_tas_rate` | unknown | No reviewer lane receipt requested for this small owner-local change. |
| `maintenance_locality` | pass | Future QA checklist changes have one owner: `skills/impl-plan/qa_checklist.md`. |
| `composition_clarity` | pass | Signature, gate, fails, Todo List, workflow, checklist function, threshold, checks, and finish gate are explicit. |

## Proof Artifacts

- Skill-local evals, when needed: not changed.
- Structure evals, when needed: not required; this was a targeted behavior
  checklist addition.
- Reviewer receipt: skipped; owner-local checklist hardening with self-check.
- Validator: `python3 scripts/check_skills.py --write` from
  `skills/skill-maintenance`.
- Eval required: no; the requested change is a runtime QA checklist guardrail,
  not a new runnable eval case.
- Evidence gaps: no live generated plan has been tested against the new
  checklist yet.

## Before Behavior

- A plan could pass while proposing extra files, functions, parameters, or
  internal decomposition as long as proof and map requirements were concrete.

## After Behavior

- A material plan must explicitly survive reuse and minimality review, or carry
  a `revise`/`block` result with the highest risk and fix/deferral.

## Followups

- Consider a future compaction pass for the 574-line `SKILL.md`; it predates
  this change and should be handled as separate `refine_skill` work.
