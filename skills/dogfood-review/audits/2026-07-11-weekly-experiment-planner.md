---
skill: dogfood-review
date: 2026-07-11
change_type: behavior
owner: skill-maintenance
status: pass
review_route: reviewer
before_ref: skills/dogfood-review/SKILL.md@216-lines
after_ref: skills/dogfood-review/SKILL.md@171-lines
reasoning_basis: first_principles
proof_artifacts:
  - skills/dogfood-review/eval_task.json
  - skills/dogfood-review/qa_checklist.md
eval_required: yes
---

# Skill Audit

## Change

- Before: Dogfood bulk-reviewed registry-tracked features and emitted one
  generic improvement ticket or candidate for Interval.
- After: Dogfood owns weekly self-improvement review, inspects experiment Goal
  Packets first, writes a report, and may create one immediate/delayed
  experiment Goal Packet without executing it.
- Why: experiment portfolio judgment and next-experiment selection need one
  bounded owner separate from Pulse execution.
- Tradeoff accepted: packets default to review-required unless explicit local
  automation authority grants Pulse admission.

## Binary Rubric

| Check | Verdict | Evidence |
| --- | --- | --- |
| `first_load_sufficiency` | pass | Portfolio review, ranking, packet, and stop boundaries are first-load. |
| `reference_load_precision` | pass | Registry and downstream skill refs have conditions. |
| `missing_context_rate` | pass | Reward/program/progress/proof inputs and source gaps are explicit. |
| `noisy_context_rate` | pass | First-load shrank from 216 to 171 lines. |
| `duplicated_instruction_count` | pass | Generic improvement-ticket and interval-summary paths were removed. |
| `prompt_size_tokens` | pass | 171-line first-load surface. |
| `task_success_rate` | unknown | Requires representative packet-generation QA. |
| `review_tas_rate` | unknown | Parent ticket reviewer pending. |
| `maintenance_locality` | pass | Report and experiment selection live in one package. |
| `composition_clarity` | pass | Inputs, feedback classes, packet files, and non-execution handoff are explicit. |

## Proof Artifacts

- Skill-local evals: existing-experiment-first, delayed packet, and immediate
  packet cases.
- Validator: JSON and skill-system checks.
- Evidence gaps: composed Goal Packet fixture inspection remains parent QA.

## Followups

- Automation write policy must choose review-required versus Pulse-ready
  admission explicitly.
