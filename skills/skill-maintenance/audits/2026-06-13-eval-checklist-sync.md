---
skill: skill-maintenance
date: 2026-06-13
change_type: behavior
owner: skill-maintenance
status: pass
review_route: self_check
before_ref: skills/skill-maintenance/SKILL.md
after_ref: skills/skill-maintenance/SKILL.md
reasoning_basis: first_principles
proof_artifacts:
  - docs/fundamentals/harness-algebra.md
  - skills/eval/SKILL.md
  - skills/skill-maintenance/SKILL.md
eval_required: no
---

# Eval Checklist Sync Audit

## Change

- Before: `skill-maintenance` owned checklist and reference cleanup but did not
  explicitly absorb reusable eval reference points.
- After: `skill-maintenance` checks changed skill eval reference points and
  promotes reusable runtime guardrails into checklist references, final QA
  checks, validator candidates, or audit notes.
- Why: evals, todos, and QA checklists should converge around the same behavior
  contract without blindly copying every eval point into first-load context.
- Tradeoff accepted: sync remains judgment-based rather than fully automated.

## First-Principles Reasoning

- Objective: make eval-to-checklist convergence durable and owner-local.
- Placement logic: checklist files and skill-local references are maintained by
  `skill-maintenance`.
- Expected behavior delta: material eval updates trigger a checklist-sync
  review during skill maintenance.
- Proof needed: structure validation and line-count/context review.

## Binary Rubric

| Check | Verdict | Evidence |
| --- | --- | --- |
| `first_load_sufficiency` | pass | The sync rule appears in the first-load maintenance checklist. |
| `reference_load_precision` | pass | The full algebra stays in the fundamentals doc. |
| `missing_context_rate` | pass | The rule names target outputs instead of implying hidden automation. |
| `noisy_context_rate` | pass | The change is two compact bullets. |
| `duplicated_instruction_count` | pass | It complements the `eval` handoff without copying eval policy. |
| `prompt_size_tokens` | pass | No templates or examples were moved into first load. |
| `task_success_rate` | unknown | No behavioral eval run was required. |
| `review_tas_rate` | unknown | No reviewer lane was required for this narrow self-check. |
| `maintenance_locality` | pass | The durable writeback rule lives in the maintenance owner. |
| `composition_clarity` | pass | The owner chain is eval reference points to maintenance writeback. |

## Proof Artifacts

- Skill-local evals, when needed: not required.
- Structure evals, when needed: not required.
- Reviewer receipt: not required for this narrow rule.
- Validator: pending command result in final work summary.
- Eval required: no.
- Evidence gaps: no automated sync tool exists yet.

## Before Behavior

- A changed skill eval could remain only an eval, even when its reference points
  should also guard runtime execution.

## After Behavior

- Skill maintenance treats reusable eval reference points as candidates for
  checklist, QA, validator, or audit promotion.

## Followups

- If this pattern repeats often, add a deterministic helper that diffs
  `eval_task.json` reference points against skill-local checklist references.
