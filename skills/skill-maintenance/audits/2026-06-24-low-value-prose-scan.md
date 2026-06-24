---
skill: skill-maintenance
date: 2026-06-24
change_type: structure
owner: skill-maintenance
status: pass
review_route: self_check
before_ref: skills/skill-maintenance/SKILL.md
after_ref: skills/skill-maintenance/SKILL.md
reasoning_basis: operator_feedback
proof_artifacts:
  - skills/skill-maintenance/references/low-value-prose-scan.md
  - skills/skill-maintenance/qa_checklist.md
eval_required: no
---

# Skill Audit

## Change

- Before: `skill-maintenance` had section-level bloat checks such as
  `noisy_context_rate`, `section_necessity`, and `workflow_duplication`, but no
  sentence-level candidate scan.
- After: `skill-maintenance` has `mode == low_value_prose_scan`, a reusable
  method reference, and a QA checklist item that asks whether each first-load
  sentence changes execution, routing, proof, safety, ownership, or maintenance
  decisions.
- Why: The operator asked for a concrete way to detect skill prose that does
  not provide value.
- Tradeoff accepted: This is a human/reviewer subworkflow, not a mechanical
  script. It returns candidate decisions, not automatic deletion verdicts.

## Proof Artifacts

- Method reference template: pass via `python3 skills/skill-maintenance/scripts/check_skills.py --write`.
- Validator: pass, `python3 skills/skill-maintenance/scripts/check_skills.py --write`.

## Followups

- Run the subworkflow during future `refine_skill` passes and record
  `keep | rewrite | move | delete` decisions in the skill audit.
