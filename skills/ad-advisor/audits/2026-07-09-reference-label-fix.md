---
skill: ad-advisor
date: 2026-07-09
change_type: maintenance
owner: skill-maintenance
status: pass
review_route: self_check
before_ref: skills/ad-advisor/SKILL.md
after_ref: skills/ad-advisor/SKILL.md
reasoning_basis: operator_correction
proof_artifacts: []
eval_required: no
---

# Skill Audit

## Change

- Before: Reference Map labels used path-like labels such as
  `../social-content/SKILL.md`, which rendered ambiguously as `SKILL.md` in
  some views and looked like self-links.
- After: Reference Map labels name the target skills directly.
- Why: A Reference Map should make routing legible at a glance.
- Tradeoff accepted: Applied the same label style to the related new marketing
  skills and added checklist guardrails so future reviews catch it.
