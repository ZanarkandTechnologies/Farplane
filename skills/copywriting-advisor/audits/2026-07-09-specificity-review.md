---
skill: copywriting-advisor
date: 2026-07-09
change_type: qa_checklist_design
owner: skill-maintenance
status: pass
review_route: self_check
before_ref: skills/copywriting-advisor/SKILL.md; skills/copywriting-advisor/qa_checklist.md
after_ref: skills/copywriting-advisor/qa_checklist.md
reasoning_basis: first_principles
proof_artifacts: []
eval_required: no
---

# Skill Audit

## Change

- Before: Copywriting Advisor already had source mining and story-spine
  strategy, but its QA did not explicitly fail generic writing-skill behavior.
- After: QA now requires awareness stage, objection, message angle, proof
  strategy, swipe move, and concrete before/after situation.
- Why: Copywriting quality depends on distinctive strategy, not just polished
  prose.
- Tradeoff accepted: Checklist wording was tightened without changing the main
  workflow.

## Proof Artifacts

- Validator: pending `python3 skills/skill-maintenance/scripts/check_skills.py --write`.
- Eval required: no new eval; existing eval covers source-backed compact page copy.
- Evidence gaps: no behavior run executed in this pass.
