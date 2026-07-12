---
skill: init-advisor
date: 2026-07-12
change_type: template
owner: skill-maintenance
status: pass
review_route: reviewer
before_ref: skills/init-advisor/scripts/bootstrap.sh
after_ref: skills/init-advisor/scripts/bootstrap.sh
reasoning_basis: advise
proof_artifacts:
  - skills/init-advisor/references/CRM_README_TEMPLATE.md
eval_required: no
---

# Skill Audit

## Change

- Before: bootstrap created CRM reports and an empty CRM index.
- After: bootstrap creates `crm/entities.json` plus skill-local report folders.
- Why: initialized projects should demonstrate the same ownership boundary as
  the live skills.
- Tradeoff accepted: only known report-producing skills are pre-created; other
  skills create their own report directory when first used.

## First-Principles Reasoning

- Objective: make the new convention true in newly initialized projects.
- Placement logic: bootstrap owns filesystem creation; the CRM README owns the
  local data contract.
- Expected behavior delta: no new project starts with the retired CRM index.
- Proof needed: shell syntax, fixture bootstrap assertions, JSON parsing, and
  independent review.

## Binary Rubric

| Check | Verdict | Evidence |
| --- | --- | --- |
| `first_load_sufficiency` | pass | Init todo names CRM entity and skill-report state. |
| `reference_load_precision` | pass | CRM details remain in the copied README template. |
| `missing_context_rate` | unknown | No post-change init corpus exists yet. |
| `noisy_context_rate` | unknown | No post-change init corpus exists yet. |
| `duplicated_instruction_count` | pass | Bootstrap and README use one convention. |
| `prompt_size_tokens` | unknown | Token comparison is not required for this template change. |
| `task_success_rate` | unknown | Full init behavior was not externally sampled. |
| `review_tas_rate` | pass | Independent rerun returned TAS-A with no blockers. |
| `maintenance_locality` | pass | Filesystem and copied schema remain init-owned. |
| `composition_clarity` | pass | Bootstrapped paths match both caller skills. |

## Proof Artifacts

- Skill-local evals, when needed: not required for deterministic bootstrap.
- Structure evals, when needed: `check_skills.py --write`.
- Reviewer receipt: TAS-A; documentation and integration-readiness passed.
- Validator: bootstrap fixture, JSON parse, and shell syntax.
- Eval required: no.
- Evidence gaps: full project validator remains broader than this migration.

## Before Behavior

- `.farplane/crm/reports/` and `.farplane/crm/index.jsonl` were created.

## After Behavior

- `.farplane/crm/entities.json`, `.farplane/customer-research/reports/`, and
  `.farplane/lead-scout/reports/` are created.

## Followups

- None.
