---
skill: lead-scout
date: 2026-07-09
change_type: behavior
owner: skill-maintenance
status: pass
review_route: self_check
before_ref: skills/lead-scout/SKILL.md; skills/lead-scout/qa_checklist.md; skills/lead-scout/eval_task.json
after_ref: skills/lead-scout/SKILL.md; skills/lead-scout/qa_checklist.md; skills/lead-scout/eval_task.json
reasoning_basis: source_synthesis
proof_artifacts:
  - skills/skill-maintenance/audits/2026-07-09-marketing-skills-source-upgrade-pilot.md
eval_required: no
---

# Skill Audit

## Change

- Before: Lead Scout ranked candidates by fit, evidence, and safety, but did
  not force a timely prospecting hypothesis.
- After: Lead Scout now requires `why them`, `why now`, `why this source`, and
  `why this outreach channel`, and rejects broad persona matches without a
  trigger.
- Why: Prospecting sources converged on qualified prospects, buyer persona,
  engagement channel, and prioritization as the core difference between a lead
  list and an outreach-worthy candidate packet.
- Tradeoff accepted: Added one first-load hypothesis gate and folded QA/eval
  wording into existing capped surfaces.
