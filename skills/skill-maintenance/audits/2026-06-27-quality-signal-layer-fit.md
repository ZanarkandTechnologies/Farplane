---
skill: skill-maintenance
date: 2026-06-27
change_type: maintenance
owner: skill-maintenance
status: pass
review_route: self_check
before_ref: skills/skill-maintenance/SKILL.md
after_ref: skills/skill-maintenance/SKILL.md
reasoning_basis: deliberative_advice
proof_artifacts:
  - docs/review/rubrics/architecture.md
eval_required: no
---

# Skill Maintenance Quality Signal Layer Fit

## Change

- Before: skill maintenance had no explicit guardrail against promoting
  checklist items into metrics or scalar scoring functions.
- After: `SKILL.md` and `qa_checklist.md` require layer-fit checks for QA,
  metrics, rubrics, and reward signals.
- Why: skill-level learning should preserve failed checks, reasons, evidence,
  and repair hints; goal/project metrics belong with `metric-advisor`.
- Tradeoff accepted: skill maintenance will resist convenient numeric summaries
  unless a caller supplies a real measurement objective.

## Binary Rubric

| Check | Verdict | Evidence |
| --- | --- | --- |
| `first_load_sufficiency` | pass | The new routing rule is in the main todo list and gotchas. |
| `maintenance_locality` | pass | Skill-maintenance owns the prevention guardrail. |
| `composition_clarity` | pass | The rule names `metric-advisor`, review rubrics, and skill QA. |
| `quality_signal_layer_fit` | pass | New checklist item catches future drift. |

## Proof Artifacts

- Validator: pending `check_skills.py --write`
- Eval required: no
- Evidence gaps: independent reviewer not required for this scoped guardrail.
