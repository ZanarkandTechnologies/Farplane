---
skill: skill-creator
date: 2026-07-09
change_type: qa_checklist_design
owner: skill-maintenance
status: pass
review_route: self_check
before_ref: skills/skill-creator/SKILL.md; skills/skill-creator/qa_checklist.md
after_ref: skills/skill-creator/SKILL.md; skills/skill-creator/qa_checklist.md
reasoning_basis: advise
proof_artifacts: []
eval_required: no
---

# Skill Audit

## Change

- Before: Skill Creator checked first-load structure and proof, but did not
  explicitly reject structurally valid todo lists that could be pasted into
  unrelated skills.
- After: Skill Creator now applies a domain-specificity check while drafting
  todo lists and carries a compact rubric in `qa_checklist.md`.
- Why: Recent marketing advisor skills showed that generic todo and QA wording
  can pass structural review while failing to encode niche workflow strategy.
- Tradeoff accepted: The rubric adds a little checklist surface, but stays
  under the skill-surface budget by folding proof and specificity together.

## Binary Rubric

| Check | Verdict | Evidence |
| --- | --- | --- |
| `first_load_sufficiency` | pass | First-load todo now tells authors to apply the domain-specificity check before finalizing todos. |
| `reference_load_precision` | pass | No new reference was added. |
| `missing_context_rate` | pass | Required guardrail lives in first load and QA checklist. |
| `noisy_context_rate` | pass | Detailed rubric is compact and checklist-local. |
| `duplicated_instruction_count` | pass | `SKILL.md` has the action; `qa_checklist.md` has the review rubric. |
| `prompt_size_tokens` | pass | Small addition only. |
| `maintenance_locality` | pass | Future edits belong to Skill Creator QA or best-practices if generalized. |
| `composition_clarity` | pass | Rubric names inputs and pass/weak/violation outputs. |

## Proof Artifacts

- Validator: pending `python3 skills/skill-maintenance/scripts/check_skills.py --write`.
- Eval required: no, this is a checklist/authoring guardrail.
- Evidence gaps: no independent reviewer lane used; change is small and local.
