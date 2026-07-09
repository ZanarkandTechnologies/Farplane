---
skill: ad-advisor
date: 2026-07-09
change_type: qa_checklist_design
owner: skill-maintenance
status: pass
review_route: self_check
before_ref: skills/ad-advisor/SKILL.md
after_ref: skills/ad-advisor/SKILL.md; skills/ad-advisor/qa_checklist.md
reasoning_basis: first_principles
proof_artifacts: []
eval_required: no
---

# Skill Audit

## Change

- Before: Ad Advisor had spend and platform gates, but no skill-local QA and
  weak pressure to produce a campaign thesis or test plan.
- After: Ad Advisor now requires a campaign thesis, test matrix, spend/mutation
  gates, policy risk labels, and final QA.
- Why: Paid ads advice should produce a reviewable experiment, not only a list
  of campaign settings.
- Tradeoff accepted: Added one checklist file and small first-load gates rather
  than a broad paid-media handbook.

## Binary Rubric

| Check | Verdict | Evidence |
| --- | --- | --- |
| `first_load_sufficiency` | pass | `SKILL.md` now reads QA preflight and names campaign thesis/test matrix. |
| `reference_load_precision` | pass | QA checklist is linked in Reference Map. |
| `missing_context_rate` | pass | Spend, policy, measurement, and mutation gates remain in first load. |
| `noisy_context_rate` | pass | Review detail lives in `qa_checklist.md`. |
| `duplicated_instruction_count` | pass | First-load actions and checklist review have distinct jobs. |
| `maintenance_locality` | pass | Paid-campaign quality rules live in the ad-advisor package. |
| `composition_clarity` | pass | Checklist signature and pass/revise/blocked outputs are explicit. |

## Proof Artifacts

- Validator: pending `python3 skills/skill-maintenance/scripts/check_skills.py --write`.
- Eval required: no new eval; existing evals cover dry-run spend gate and sensitive targeting.
- Evidence gaps: no behavior run executed in this pass.
