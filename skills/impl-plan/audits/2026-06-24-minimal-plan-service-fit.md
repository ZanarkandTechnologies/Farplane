---
skill: impl-plan
date: 2026-06-24
change_type: behavior
owner: skill-maintenance
status: pass
review_route: self_check
before_ref: skills/impl-plan/qa_checklist.md@pre-minimal-plan-service-fit
after_ref: skills/impl-plan/qa_checklist.md
reasoning_basis: advise
proof_artifacts:
  - skills/impl-plan/qa_checklist.md
  - skills/impl-plan/prompts/plan.md
  - skills/impl-plan/references/template.md
eval_required: no
---

# Skill Audit

## Change

- Before: `impl-plan` checked minimal required version, reuse, least
  parameters, and function/file necessity, but did not require the generated
  plan to explicitly claim minimality or prove that new functions could not
  belong to an existing owner surface.
- After: material plan QA now includes `minimal-impl-plan-claim` and
  `existing-service-fit`, and the prompt/template expose the matching
  `plan_qa` fields.
- Why: plans should bias toward the smallest ticket-satisfying implementation
  and force each new function, helper, service, or module to earn its surface
  area before build.
- Tradeoff accepted: add two checklist checks plus small prompt/template
  mirrors instead of rewriting the broader minimality section.

## First-Principles Reasoning

- Objective: prevent `impl-plan` from approving broad new implementation
  surfaces when existing services, modules, helpers, or owner files can carry
  the change.
- Placement logic: `qa_checklist.md` owns repeatable runtime guardrails;
  `prompts/plan.md` reminds planners during drafting; `references/template.md`
  makes the readiness result visible without duplicating checklist prose.
- Expected behavior delta: material plans explicitly state they are the minimal
  implementation plan for the selected ticket, and any new service-shaped
  function must justify why it cannot live inside an existing owner surface.
- Proof needed: source diff, targeted grep, checklist self-check, and standard
  skill validator attempt.

## Binary Rubric

| Check | Verdict | Evidence |
| --- | --- | --- |
| `first_load_sufficiency` | pass | `SKILL.md` already routes material plan QA through `qa_checklist.md`; no new first-load behavior required. |
| `reference_load_precision` | pass | Existing Reference Map points to `qa_checklist.md`; changed template/prompt are already named references. |
| `missing_context_rate` | pass | The new guardrail lives in the owner checklist and is mirrored in the prompt/template finish surface. |
| `noisy_context_rate` | pass | Detailed checks stay out of `SKILL.md`; only checklist/prompt/template changed. |
| `duplicated_instruction_count` | pass | Checklist owns check detail; prompt/template carry only drafting and readiness cues. |
| `prompt_size_tokens` | pass | `SKILL.md` line count unchanged. |
| `task_success_rate` | unknown | No live generated ticket plan was run in this pass. |
| `review_tas_rate` | unknown | Reviewer lane not used; change is narrow and owner-local. |
| `maintenance_locality` | pass | Future edits belong in `skills/impl-plan/qa_checklist.md`. |
| `composition_clarity` | pass | Finish gate names the two new `plan_qa` fields. |

## Proof Artifacts

- Skill-local evals, when needed: not required; this is a runtime QA checklist
  guardrail, not a new variable behavior case.
- Structure evals, when needed: targeted self-check against
  `skills/skill-maintenance/qa_checklist.md`.
- Reviewer receipt: skipped; narrow owner-local checklist hardening.
- Validator: `python3 scripts/check_skills.py --write` from
  `skills/skill-maintenance` blocked on an unrelated pre-existing
  `skills/proof-advisor/SKILL.md` name/directory check.
- Eval required: no.
- Evidence gaps: no generated `impl-plan` ticket was run to demonstrate the new
  fields in a concrete ticket body.

## Before Behavior

- A material plan could pass broad minimality checks without explicitly saying
  "this is the minimal implementation plan" or proving that new functions did
  not belong to an existing service/module/helper.

## After Behavior

- A material plan must include `minimal_impl_plan_claim` and
  `existing_service_fit` in its compact `plan_qa` readiness note, or revise/block
  before handoff.

## Followups

- Run a live `impl-plan` example or eval later if repeated plans still create
  unnecessary new functions or services.
