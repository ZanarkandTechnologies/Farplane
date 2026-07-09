---
skill: copywriting-advisor
date: 2026-07-09
change_type: behavior
owner: skill-maintenance
status: pass
review_route: self_check
before_ref: skills/copywriting-advisor/SKILL.md; skills/copywriting-advisor/qa_checklist.md
after_ref: skills/copywriting-advisor/SKILL.md; skills/copywriting-advisor/qa_checklist.md; skills/copywriting-advisor/eval_task.json
reasoning_basis: first_principles
proof_artifacts: []
eval_required: no
---

# Skill Audit

## Change

- Before: Copywriting Advisor had source mining and story-shape selection, but
  did not explicitly choose a reusable persuasion formula for the reader stage.
- After: The skill now selects a persuasion path: AIDA, PAS, 4Cs, FAB, ACC, or
  SLAP, records formula fit in the copy packet, and checks it in QA/eval.
- Why: The operator supplied a Chase Dimond copywriting-formula chart and asked
  to extract skills from it. The durable behavior is formula selection, not
  copying the example ads.
- Tradeoff accepted: Kept the formula map first-load because it is short and
  normally useful; did not add a larger reference file yet.

## Proof Artifacts

- Validator: pending `python3 skills/skill-maintenance/scripts/check_skills.py --write`.
- Eval required: no new eval case; existing copywriting eval now includes
  formula-path selection.
- Evidence gaps: no behavior run executed in this pass.
