---
skill: ad-advisor
date: 2026-07-09
change_type: behavior
owner: skill-maintenance
status: pass
review_route: self_check
before_ref: skills/ad-advisor/SKILL.md; skills/ad-advisor/qa_checklist.md; skills/ad-advisor/eval_task.json
after_ref: skills/ad-advisor/SKILL.md; skills/ad-advisor/qa_checklist.md; skills/ad-advisor/eval_task.json
reasoning_basis: source_synthesis
proof_artifacts:
  - skills/skill-maintenance/audits/2026-07-09-marketing-skills-source-upgrade-pilot.md
eval_required: no
---

# Skill Audit

## Change

- Before: Ad Advisor required a campaign thesis, test matrix, spend gates, and
  policy risk labels.
- After: Ad Advisor also requires interpretable tests and labels platform
  learning or stability risk before iteration.
- Why: Current paid-social and digital-ad strategy sources converge on clean
  testing, diverse creative, platform signal quality, and avoiding noisy
  changes that make results impossible to interpret.
- Tradeoff accepted: Kept the delta inside the existing test-matrix gate rather
  than adding a long paid-media reference.
