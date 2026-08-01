---
skill: agency-opportunity-research
date: 2026-07-13
change_type: behavior
owner: skill-maintenance
status: passed
review_route: reviewer
before_ref: skills/agency-opportunity-research/SKILL.md
after_ref: skills/agency-opportunity-research/SKILL.md
reasoning_basis: first_principles
proof_artifacts:
  - skills/agency-opportunity-research/evals/evals.json
eval_required: yes
---

# Comparison table standard audit

## Change

- Before: accepted comparisons were required on the landing page but their
  visual structure was unspecified, allowing side-by-side cards.
- After: customer-facing competitive comparisons must use a semantic table;
  cards are an explicit regression failure.
- Why: buyers need to compare the same decision fields across options by row.
- Tradeoff accepted: narrow screens scroll horizontally instead of stacking
  cards and hiding cross-option alignment.

## First-Principles Reasoning

- Objective: make vendor differences faster to scan and harder to manipulate.
- Placement logic: the opportunity-research handoff owns the comparison shape;
  each consuming demo owns deterministic rendering assertions.
- Expected behavior delta: future demos emit tables, not card grids.
- Proof needed: skill checks, focused eval validation, installation, and review.

## Binary Rubric

| Check | Verdict | Evidence |
| --- | --- | --- |
| `first_load_sufficiency` | pass | The landing handoff rule is in todo 5. |
| `reference_load_precision` | pass | No reference routing changed. |
| `missing_context_rate` | pass | The normal path names the required semantic structure. |
| `noisy_context_rate` | pass | The delta adds one short operational clause. |
| `duplicated_instruction_count` | pass | Skill owns behavior; QA owns rejection; eval owns variable proof. |
| `prompt_size_tokens` | pass | Skill remains within the existing first-load envelope. |
| `task_success_rate` | pass | Representative Valefor consumers pass bounded table/no-card regressions and browser QA. |
| `review_tas_rate` | pass | Independent cross-project review returned TAS-A on 2026-07-13. |
| `maintenance_locality` | pass | Future behavior edits belong in todo 5. |
| `composition_clarity` | pass | Handoff output shape is explicit. |

## Proof Artifacts

- Skill-local evals: table/no-card assertion updated.
- Structure evals: skill-system validator passes.
- Reviewer receipt: Valefor `TASK-0034` table-correction review (TAS-A).
- Validator: eval JSON parses.
- Eval required: yes; reference point hardened in the existing industry case.
- Installed-copy check: table/no-card rule present after installation.
- Evidence gaps: none for the skill behavior change.

## Before Behavior

- Competitive choices could render as visually separate cards.

## After Behavior

- Competitive choices render in one semantic table with equal fields.

## Followups

- Closed after validator, installed-copy check, consumer regressions, responsive browser proof, and TAS-A review.
