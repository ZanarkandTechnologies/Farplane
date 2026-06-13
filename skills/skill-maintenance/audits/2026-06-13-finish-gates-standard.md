---
skill: skill-maintenance
date: 2026-06-13
change_type: behavior
owner: skill-maintenance
status: pass
review_route: advise
before_ref: docs/skills/best-practices.md
after_ref: docs/skills/best-practices.md
reasoning_basis: first_principles
proof_artifacts:
  - docs/skills/best-practices.md
  - docs/skills/system.md
  - docs/skills/README.md
  - skills/skill-creator/references/SKILL_TEMPLATE.md
  - skills/skill-maintenance/SKILL.md
eval_required: no
---

# Skill Audit

## Change

- Before: The shared skill standard treated final `review` as the default
  completion shape, even when a skill needed QA, eval, validator, demo, human
  feedback, or a domain checklist.
- After: The shared standard uses `finish_gate` as the general concept and
  routes to review, QA, eval, validator, checklist, demo, human feedback, or
  self-check based on the claim.
- Why: Some skills need operated proof or domain QA rather than judgment review.
  Long QA and quality checklists should be loaded at the finish stage, not
  placed directly into first-load todos.
- Tradeoff accepted: The standard adds one new concept, but it removes the
  misleading habit of calling every proof step a review.

## First-Principles Reasoning

- Objective: Make skill completion gates match the evidence needed by each
  output type.
- Placement logic: `docs/skills/best-practices.md` owns authoring standards;
  `skills/skill-creator/references/SKILL_TEMPLATE.md` seeds new skills;
  `skills/skill-maintenance/SKILL.md` owns rollout language.
- Expected behavior delta: New and updated skills name a specific finish gate
  and move long QA or quality checklists into `references/*-checklist.md` when
  those checks are only needed after an artifact exists.
- Proof needed: Registry sync, doc-reference validation, and targeted grep for
  stale `review gates` wording.

## Binary Rubric

| Check | Verdict | Evidence |
| --- | --- | --- |
| `first_load_sufficiency` | pass | Template now asks for a named finish gate. |
| `reference_load_precision` | pass | Standard says long QA/checklists belong in references when only needed at finish. |
| `missing_context_rate` | pass | Finish gate routing table covers review, QA, eval, validators, doc quality, demo, feedback, and self-check. |
| `noisy_context_rate` | pass | Standard discourages long QA checklists in `## Todo List` unless needed before execution. |
| `duplicated_instruction_count` | pass | Shared finish-gate standard replaces repeated local review-only language. |
| `prompt_size_tokens` | unknown | No token measurement run. |
| `task_success_rate` | unknown | No behavioral eval run. |
| `review_tas_rate` | unknown | No reviewer receipt. |
| `maintenance_locality` | pass | Changed shared standard, template, selection guide, and maintenance skill only. |
| `composition_clarity` | pass | Finish gates compose with review, QA, eval, validators, and skill-local checklists. |

## Proof Artifacts

- Skill-local evals, when needed: not required for this standards wording pass.
- Structure evals, when needed: standard skill maintenance check.
- Reviewer receipt: not used; this is an operator-directed local standard update.
- Validator: `python3 skills/skill-maintenance/scripts/check_skills.py --write`.
- Eval required: no, unless future agents keep treating review as the only
  finish gate.
- Evidence gaps: no broad migration of existing skills to add QA checklists.

## Before Behavior

- Skill standards biased authors toward final review even for user-visible or
  operated workflows.

## After Behavior

- Skill standards ask authors to choose the correct finish gate and keep long
  finish-stage checklists in lazy-loaded references.

## Followups

- On contact, add `references/*-qa-checklist.md` to frontend, media, content,
  and agent-testing skills that need operated proof.
