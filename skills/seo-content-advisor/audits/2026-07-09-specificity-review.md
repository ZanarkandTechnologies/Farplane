---
skill: seo-content-advisor
date: 2026-07-09
change_type: qa_checklist_design
owner: skill-maintenance
status: pass
review_route: self_check
before_ref: skills/seo-content-advisor/SKILL.md; skills/seo-content-advisor/qa_checklist.md
after_ref: skills/seo-content-advisor/qa_checklist.md
reasoning_basis: first_principles
proof_artifacts: []
eval_required: no
---

# Skill Audit

## Change

- Before: SEO Content Advisor had people-first SEO checks, but its QA did not
  explicitly fail generic article-writing behavior.
- After: QA now requires intent angle, reader promise, original proof asset,
  freshness risk, do-not-claim boundary, and section jobs.
- Why: SEO content advice should produce a reader-specific, evidence-backed
  article strategy rather than a generic outline with keywords.
- Tradeoff accepted: Checklist wording was tightened without changing the main
  workflow.

## Proof Artifacts

- Validator: pending `python3 skills/skill-maintenance/scripts/check_skills.py --write`.
- Eval required: no new eval; existing eval covers people-first article brief behavior.
- Evidence gaps: no behavior run executed in this pass.
