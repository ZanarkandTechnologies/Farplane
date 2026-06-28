---
skill: doc-advisor
date: 2026-06-27
change_type: maintenance
owner: skill-maintenance
status: pass
review_route: self_check
before_ref: skills/doc-advisor/qa_checklist.md
after_ref: skills/doc-advisor/qa_checklist.md
reasoning_basis: deliberative_advice
proof_artifacts:
  - docs/review/rubrics/documentation-quality.md
eval_required: no
---

# Documentation Quality Layer Boundary

## Change

- Before: `qa_checklist.md` embedded a numeric documentation quality score and
  guard/anti-metric language.
- After: the checklist owns inspection checks, while
  `docs/review/rubrics/documentation-quality.md` owns readiness judgment.
- Why: skill-level documentation feedback is more useful as failed checks,
  reasons, evidence, and repair hints than as a scalar score.
- Tradeoff accepted: no simple 0-12 summary; review artifacts must carry the
  relevant failed checks and next action instead.

## Binary Rubric

| Check | Verdict | Evidence |
| --- | --- | --- |
| `maintenance_locality` | pass | Checklist and rubric now have distinct jobs. |
| `composition_clarity` | pass | `doc-advisor` routes material readiness to the review rubric. |
| `proof_surface_fit` | pass | Review verdicts, not metrics, classify documentation readiness. |
| `quality_signal_layer_fit` | pass | Metrics language was removed from the skill-local checklist. |

## Proof Artifacts

- Validator: pending `check_skills.py --write`
- Eval required: no
- Evidence gaps: independent reviewer not required for this small boundary edit.
