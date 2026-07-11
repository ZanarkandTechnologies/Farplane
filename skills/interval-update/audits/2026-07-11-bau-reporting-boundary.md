---
skill: interval-update
date: 2026-07-11
change_type: behavior
owner: skill-maintenance
status: pass
review_route: reviewer
before_ref: skills/interval-update/SKILL.md@239-lines
after_ref: skills/interval-update/SKILL.md@141-lines
reasoning_basis: first_principles
proof_artifacts:
  - skills/interval-update/eval_task.json
  - skills/interval-update/qa_checklist.md
eval_required: yes
---

# Skill Audit

## Change

- Before: Interval mixed reporting, workflow fan-out, rewards, Dogfood,
  leverage, priority planning, goals, and ticket mutation.
- After: Interval writes a compact Daily/Weekly BAU report and may resurface
  only prior-evidenced, deduped, capped maintenance after the report.
- Why: one owner is needed for reporting, BAU direction, experiment review,
  and execution.
- Tradeoff accepted: Interval cannot act immediately on same-run discoveries;
  they stay visible in the report until prior evidence or operator action exists.

## Binary Rubric

| Check | Verdict | Evidence |
| --- | --- | --- |
| `first_load_sufficiency` | pass | Signature, gates, todo, templates, and ownership routes are first-load. |
| `reference_load_precision` | pass | Two active references have explicit load conditions. |
| `missing_context_rate` | pass | Prior-evidence and same-run distinctions are explicit. |
| `noisy_context_rate` | pass | First-load shrank from 239 to 141 lines. |
| `duplicated_instruction_count` | pass | Workflow matrix removed from the runtime contract. |
| `prompt_size_tokens` | pass | 141-line first-load surface. |
| `task_success_rate` | unknown | Requires an automation behavior run. |
| `review_tas_rate` | unknown | Parent ticket reviewer pending. |
| `maintenance_locality` | pass | Report/admission behavior is owner-local. |
| `composition_clarity` | pass | Report and maintenance outputs are explicit. |

## Proof Artifacts

- Skill-local evals: Daily report-only, same-run ledger-only, and prior-evidence
  resurfacing cases.
- Validator: JSON and skill-system checks.
- Evidence gaps: composed Daily/Weekly fixture run remains parent-ticket QA.

## Followups

- Move or retire the now-unreferenced legacy workflow catalog only after the
  Pulse lane has reused any due-reward helper it needs.
