---
skill: skill-maintenance
date: 2026-07-09
change_type: behavior
owner: skill-maintenance
status: pass
review_route: self_check
before_ref: skills/skill-maintenance/SKILL.md
after_ref: skills/skill-maintenance/SKILL.md; skills/skill-maintenance/references/upgrade-skill-from-sources.md
reasoning_basis: advise
proof_artifacts: []
eval_required: no
---

# Skill Audit

## Change

- Before: Skill Maintenance could harden or refine skills from local lessons and
  audits, while Skill Creator had a book-to-skill branch for new or updated
  skills.
- After: Skill Maintenance has an `upgrade_skill_from_sources` mode that
  composes source research, book-to-skill extraction, best-of-worlds synthesis,
  owner-local skill edits, audit, validation, and review.
- Why: Existing skills can be structurally valid but strategically generic; the
  operator wanted a repeatable lane for upgrading them from current articles
  and book/framework sources.
- Tradeoff accepted: Added one method reference instead of creating a new
  top-level `skill-upgrader` skill before the workflow has repeated usage.

## Proof Artifacts

- Validator: pending `python3 skills/skill-maintenance/scripts/check_skills.py --write`.
- Eval required: no new eval; this is a maintenance workflow branch.
- Evidence gaps: pilot runs should create target-skill audit receipts and may
  justify a future eval if the route needs behavior proof.
