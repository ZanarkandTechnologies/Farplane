---
skill: skill-maintenance
date: 2026-06-24
change_type: template
owner: skill-maintenance
status: pass
review_route: self_check
before_ref: skills/skill-creator/references/SKILL_TEMPLATE.md
after_ref: docs/skills/templates/SKILL_TEMPLATE.md
reasoning_basis: advise
proof_artifacts:
  - docs/skills/templates/SKILL_TEMPLATE.md
  - docs/skills/templates/QA_CHECKLIST_TEMPLATE.md
  - docs/skills/templates/METHOD_REFERENCE_TEMPLATE.md
  - skills/skill-creator/references/book-to-skill.md
  - skills/skill-maintenance/scripts/check_skills.py
eval_required: no
---

# Skill Audit

## Change

- Before: `skill-creator` physically owned `SKILL_TEMPLATE.md` and
  `QA_CHECKLIST_TEMPLATE.md`, while `skill-maintenance` and docs also treated
  them as shared standards.
- After: docs own canonical skill templates under `docs/skills/templates/`;
  `skill-creator` scaffolds from them, `skill-maintenance` validates them, and
  reusable method references can declare `skill-method-reference`.
- Why: Shared templates should have one neutral owner. Creation and maintenance
  are consumers with different jobs, not co-owners of the template source.
- Tradeoff accepted: The old creator-owned paths were removed instead of kept
  as compatibility pointers, so stale references fail fast.

## First-Principles Reasoning

- Objective: Make skill package templates, QA checklist templates, and subskill
  reference templates discoverable, enforceable, and owned by docs rather than
  by one caller skill.
- Placement logic: `docs/skills/templates/*` owns standards; `skill-creator`
  owns scaffolding and routing; `skill-maintenance` owns registry sync,
  validation, audits, and install checks.
- Expected behavior delta: New skill packages use docs-owned `SKILL_TEMPLATE`;
  reusable subskill/reference workflows use `METHOD_REFERENCE_TEMPLATE`; declared
  method references fail validation when required sections are missing.
- Proof needed: Focused template-registry/test checks plus full
  `check_skills.py --write`.

## Binary Rubric

| Check | Verdict | Evidence |
| --- | --- | --- |
| `first_load_sufficiency` | pass | `skill-creator` and `skill-maintenance` both link to docs-owned templates. |
| `reference_load_precision` | pass | `book-to-skill.md` declares `skill-method-reference` and follows the method sections. |
| `missing_context_rate` | pass | The standard check validates declared method references. |
| `noisy_context_rate` | pass | Method references are not forced into the full `SKILL.md` template. |
| `duplicated_instruction_count` | pass | Old creator-owned template files were moved, not duplicated. |
| `prompt_size_tokens` | pass | No broad first-load template body was copied into skills. |
| `task_success_rate` | unknown | No behavior eval was run; this is a structural/template migration. |
| `review_tas_rate` | unknown | Self-check only. |
| `maintenance_locality` | pass | Template source is docs; validation is skill-maintenance; scaffolding is skill-creator. |
| `composition_clarity` | pass | `docs/skills/system.md` defines the skill-template versus method-reference boundary. |

## Proof Artifacts

- Skill-local evals, when needed: not required
- Structure evals, when needed:
  - `python3 bin/validators/sync_template_registry.py --write && python3 bin/validators/sync_template_registry.py --check`
  - `python3 -m unittest bin.validators.test_check_template_version_metadata bin.validators.test_sync_template_registry`
  - `python3 scripts/check_skills.py --write` from `skills/skill-maintenance`
- Reviewer receipt: none
- Validator: passed on 2026-06-24
- Eval required: no
- Evidence gaps: reviewer lane not run for this same-turn operator-requested
  migration

## Before Behavior

- Shared skill templates appeared to have two owners: `skill-creator` by path
  and `skill-maintenance` by validation and rollout behavior.
- Subskill/reference workflows had no explicit template distinction from full
  callable skill packages.

## After Behavior

- Docs own shared template files.
- `skill-creator` and `skill-maintenance` consume those docs-owned templates.
- Reusable reference workflows can declare and validate
  `skill-method-reference: "0.1.0"`.

## Followups

- Consider adding more method-reference adopters only when a reference is
  genuinely reusable workflow logic, not ordinary background detail.
