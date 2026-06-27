---
skill: skill-maintenance
date: 2026-06-28
change_type: maintenance
owner: skill-maintenance
status: pass
review_route: self_check
before_ref: tickets/TASK-0221/ticket.md
after_ref: bin/validators/check_skill_surface_budget.py
reasoning_basis: first_principles
proof_artifacts:
  - bin/validators/test_check_skill_surface_budget.py
  - docs/features/FEAT-0062-capped-skill-surface-budget.md
  - tickets/TASK-0221/ticket.md
eval_required: no
---

# Capped Skill Surface Seed Rollout Audit

## Change

- Before: skill todos, QA checklists, and skill-local evals had no opt-in
  mechanical budget scanner.
- After: `FEAT-0062` defines capped skill surfaces, and
  `template_uses.skill-surface-budget: "0.1.0"` enrolls Seed A/B skills into
  the `10 / 5 / 5` budget scanner.
- Template release: `skill-template` moved from `0.3.6` to `0.3.7`, and
  `skill-qa-checklist` moved from `0.1.0` to `0.1.1` because both templates now
  carry FEAT-0062 guidance.
- Maintenance self-update: `skill-maintenance` now names capped-surface rollout,
  the minimizer helper, and the preserve-budget gate for enrolled skills.
- Why: high-leverage skills should focus agents on the most useful guardrails
  instead of accumulating long lists that are easy to skim.
- Tradeoff accepted: enforcement is opt-in, so legacy skills are skipped until
  maintainers intentionally refine and enroll them.

## First-Principles Reasoning

- Objective: preserve skill behavior while reducing repeated first-load and QA
  checklist bloat.
- Placement logic: deterministic counting belongs in `bin/validators`; value
  preservation belongs in `consolidate` via `skill-maintenance.refine_skill`.
- Expected behavior delta: subscribed skills fail when over `10 / 5 / 5` and
  receive an exact minimizer command; unsubscribed skills stay quiet.
- Proof needed: unit tests, budget scanner pass, feature registry validation,
  and full `check_skills.py --write`.

## Binary Rubric

| Check | Verdict | Evidence |
| --- | --- | --- |
| `first_load_sufficiency` | pass | Seed skills keep their main contracts in `SKILL.md`; only overlapping QA items were merged. |
| `reference_load_precision` | pass | No new references were added. |
| `missing_context_rate` | pass | Consolidated QA checklists preserve preflight/final-review guardrails. |
| `noisy_context_rate` | pass | Seed B QA checklists now fit 5-item budget. |
| `duplicated_instruction_count` | pass | Preflight/final-review duplicates were merged into single guardrails. |
| `prompt_size_tokens` | pass | `prototyping` top-level todos reduced from 11 to 10. |
| `task_success_rate` | unknown | No behavioral eval run was required for mechanical budget enforcement. |
| `review_tas_rate` | unknown | No reviewer lane was run in this pass. |
| `maintenance_locality` | pass | `FEAT-0062`, scanner, minimizer, and skill-maintenance docs name one owner path. |
| `composition_clarity` | pass | `refine_skill` calls `consolidate(..., structure = skill)` before Seed B enrollment. |
| `template_version_truthful` | pass | Edited skill templates were bumped and `check_template_version_metadata.py --all` passed. |

## Proof Artifacts

- Skill-local evals, when needed: not required.
- Structure evals, when needed: `python3 -m unittest bin/validators/test_check_skill_surface_budget.py`.
- Reviewer receipt: not run.
- Validator:
  - `python3 bin/validators/check_skill_surface_budget.py`
  - `python3 docs/features/validate_features.py`
  - `python3 bin/validators/check_template_version_metadata.py --all`
  - `python3 skills/skill-maintenance/scripts/check_skills.py --write`
- Eval required: no.
- Evidence gaps: final independent review is still available if this becomes a
  precedent-setting policy expansion.

## Before Behavior

- No subscribed-skill budget scanner existed.
- Seed B skills had QA checklist or top-level todo counts above the new budget.

## After Behavior

- Seed A and Seed B skills are enrolled through `skill-surface-budget`.
- Scanner reports `checked=8 skipped=90 failed=0`.
- `check_skills.py --write` includes the budget scanner and passes.

## Followups

- Use the same `refine_skill -> consolidate` path before enrolling Seed C.
- Consider lowering future caps only after Seed A/B run quietly for real work.
