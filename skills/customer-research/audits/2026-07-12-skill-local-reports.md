---
skill: customer-research
date: 2026-07-12
change_type: behavior
owner: skill-maintenance
status: pass
review_route: reviewer
before_ref: skills/customer-research/SKILL.md
after_ref: skills/customer-research/SKILL.md
reasoning_basis: advise
proof_artifacts:
  - skills/customer-research/evals/evals.json
  - skills/customer-research/templates/report.md
eval_required: yes
---

# Skill Audit

## Change

- Before: customer research stored reports under CRM and rebuilt a CRM index.
- After: customer research owns its reports and links stable CRM entity IDs.
- Why: report memory belongs to its producing skill; CRM owns relationship state.
- Tradeoff accepted: entity backlinks require a report scan unless a derived
  cross-skill index is added later.

## First-Principles Reasoning

- Objective: separate durable entity state from dated research artifacts.
- Placement logic: report behavior stays in `customer-research`; entity shape
  stays in the CRM bootstrap template.
- Expected behavior delta: reports write to
  `.farplane/customer-research/reports/` with resolvable `entity_refs`.
- Proof needed: eval JSON, template/example consistency, skill validation, and
  independent review.

## Binary Rubric

| Check | Verdict | Evidence |
| --- | --- | --- |
| `first_load_sufficiency` | pass | Storage, linking, and write behavior are explicit in `SKILL.md`. |
| `reference_load_precision` | pass | The report template is loaded only when drafting. |
| `missing_context_rate` | unknown | No post-change invocation corpus exists yet. |
| `noisy_context_rate` | unknown | No post-change invocation corpus exists yet. |
| `duplicated_instruction_count` | pass | CRM indexing instructions and synchronizer were removed. |
| `prompt_size_tokens` | unknown | Token comparison is not required for this behavior migration. |
| `task_success_rate` | unknown | Runtime eval has not yet been sampled. |
| `review_tas_rate` | pass | Independent rerun returned TAS-A with no blockers. |
| `maintenance_locality` | pass | Skill reports and CRM entity state have distinct owners. |
| `composition_clarity` | pass | `lead-scout` hands entity IDs to `customer-research`. |

## Proof Artifacts

- Skill-local evals, when needed: updated entity-linking assertions.
- Structure evals, when needed: `check_skills.py --write`.
- Reviewer receipt: TAS-A; skill-contract and integration-readiness passed.
- Validator: JSON parse, bootstrap fixture, skill checker.
- Eval required: yes; static eval contract validation is required this turn.
- Evidence gaps: no live post-change customer-research invocation yet.

## Before Behavior

- Reports and their derived index lived under `.farplane/crm/`.

## After Behavior

- CRM owns `entities.json`; reports live under the producing skill and reference
  CRM IDs through `entity_refs`.

## Followups

- Add a generic derived report index only after report volume creates a real
  lookup problem.
