---
skill: deep-system-design
date: 2026-08-23
change_type: first-load-compaction
owner: skill-maintenance
status: reviewed
review_route: reviewer
reasoning_basis: line-cap failure plus first-load value review
eval_required: no
proof_artifacts:
  - python3 skills/skill-maintenance/scripts/check_skills.py --write
  - python3 bin/validators/check_skill_frontmatter.py
  - reviewer receipt in task transcript
---

# First-load compaction

**Before:** `SKILL.md` was 474 lines and mixed the invocation contract with
depth profiles, interview detail, scoring, artifact schema, and handoff prose.

**After:** the 79-line `SKILL.md` keeps trigger boundaries, signature, default
path, gates, output, and the precise workflow-reference route. The detailed
procedure lives in `references/workflow.md` under the same skill owner.

**Classification:** keep the first-load contract; move long scoring, challenge,
and brief-schema detail; delete no behavior.

**Loss check:** profiles, customer/data entry modes, one-question interviews,
recursive decomposition, readiness gates, pressure pass, visible writeback,
and downstream handoffs remain in the package reference.
