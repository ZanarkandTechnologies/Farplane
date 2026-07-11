---
skill: feed-scout
date: 2026-07-11
change_type: behavior
owner: skill-maintenance
status: pass
review_route: reviewer
before_ref: skills/feed-scout/SKILL.md@190-lines
after_ref: skills/feed-scout/SKILL.md@226-lines
reasoning_basis: first_principles
proof_artifacts:
  - skills/feed-scout/eval_task.json
  - skills/feed-scout/qa_checklist.md
eval_required: yes
---

# Skill Audit

## Change

- Before: Feed Scout wrote feeds/reports and loosely routed proposals or tasks.
- After: Feed Scout writes the dated source report first, then may project a
  capped set of source-backed tickets through explicit quality/authority gates.
- Why: provider discovery should be independently scheduled and capable of
  creating actionable work without leaking execution into the provider run.
- Tradeoff accepted: first-load grew to make the post-report ticket gates and
  non-execution boundary impossible to miss; it remains below 250 lines.

## Binary Rubric

| Check | Verdict | Evidence |
| --- | --- | --- |
| `first_load_sufficiency` | pass | Report-first and ticket admission behavior is first-load. |
| `reference_load_precision` | pass | Data/workflow references retain explicit conditions. |
| `missing_context_rate` | pass | Cap, proof, authority, dedupe, and admission policy are named. |
| `noisy_context_rate` | pass | 226 lines; platform detail remains in the workflow reference. |
| `duplicated_instruction_count` | pass | Automation template specializes the scheduled caller. |
| `prompt_size_tokens` | pass | Under the 250-line review threshold. |
| `task_success_rate` | unknown | Requires report-only and report-plus-ticket fixture runs. |
| `review_tas_rate` | unknown | Parent ticket reviewer pending. |
| `maintenance_locality` | pass | Provider report/ticket projection stays owner-local. |
| `composition_clarity` | pass | Report precedes ticket paths in signature and workflow. |

## Proof Artifacts

- Skill-local evals: report-only, bounded ticket, and book-summary route cases.
- Validator: JSON, feed helper tests, and skill-system checks.
- Evidence gaps: composed source-backed ticket fixture remains parent QA.

## Followups

- The automation must supply an explicit ticket limit and write policy.
