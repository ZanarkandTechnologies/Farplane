---
skill: lead-scout
date: 2026-07-09
change_type: qa_checklist_design
owner: skill-maintenance
status: pass
review_route: self_check
before_ref: skills/lead-scout/SKILL.md
after_ref: skills/lead-scout/SKILL.md; skills/lead-scout/qa_checklist.md
reasoning_basis: first_principles
proof_artifacts: []
eval_required: no
---

# Skill Audit

## Change

- Before: Lead Scout had prospect discovery steps, but no skill-local QA and
  weak pressure against generic web-search-and-rank output.
- After: Lead Scout now requires a signal ladder, discovery lanes, ranked
  evidence, near-miss contrast, privacy limits, and final QA.
- Why: Lead scouting is only useful when it explains why a public signal makes
  a candidate worth researching next.
- Tradeoff accepted: Added a checklist file instead of expanding first-load
  prose with a long outreach rubric.

## Binary Rubric

| Check | Verdict | Evidence |
| --- | --- | --- |
| `first_load_sufficiency` | pass | `SKILL.md` reads QA preflight and names signal ladder/discovery lane work. |
| `reference_load_precision` | pass | QA checklist is referenced directly. |
| `missing_context_rate` | pass | Ranking, ethics, evidence, and next-owner gates are visible. |
| `noisy_context_rate` | pass | Detailed review checks are in `qa_checklist.md`. |
| `duplicated_instruction_count` | pass | `SKILL.md` owns actions; checklist owns pass/revise/block review. |
| `maintenance_locality` | pass | Lead-specific quality rules live in the lead-scout package. |
| `composition_clarity` | pass | Checklist signature and outputs are explicit. |

## Proof Artifacts

- Validator: pending `python3 skills/skill-maintenance/scripts/check_skills.py --write`.
- Eval required: no new eval; existing evals already cover routing, qualification, and safety.
- Evidence gaps: no behavior run executed in this pass.
