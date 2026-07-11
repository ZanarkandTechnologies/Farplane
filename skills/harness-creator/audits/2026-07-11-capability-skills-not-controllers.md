---
skill: harness-creator
date: 2026-07-11
change_type: behavior
owner: skill-maintenance
status: pass
review_route: reviewer
before_ref: skills/harness-creator/SKILL.md@pre-TASK-0321
after_ref: skills/harness-creator/SKILL.md
reasoning_basis: first_principles
proof_artifacts:
  - tickets/TASK-0321/ticket.md
eval_required: no
---

# Harness Creator Capability-Skill Audit

## Change

- Before: harness creation emitted product strategy files, a generated index,
  and product-skill plans.
- After: it emits charter/goals deltas plus reusable or project-local
  capability-skill reuse, stubs, and refinement tickets.
- Why: an artifact category should not become an orchestration boundary.
- Tradeoff accepted: capability inventories remain refs/maps rather than a new
  mandatory catalog schema.

## First-Principles Reasoning

- Objective: build the smallest evidence-producing project operating model.
- Placement logic: harness and goals own policy; skills own workflow; tickets
  own work and proof.
- Expected behavior delta: no product-controller artifacts are proposed.
- Proof needed: skill/template/reference sweep and parent reviewer.

## Binary Rubric

| Check | Verdict | Evidence |
| --- | --- | --- |
| `first_load_sufficiency` | pass | Normal operating-model workflow remains in the todo. |
| `reference_load_precision` | pass | Worksheet and legacy notation have explicit load conditions. |
| `missing_context_rate` | pass | Charter, goals, capability reuse, feedback, gates, and milestone remain. |
| `noisy_context_rate` | pass | Product catalog/index mechanics removed. |
| `duplicated_instruction_count` | pass | Worksheet mirrors owners without becoming canonical. |
| `prompt_size_tokens` | unknown | No token benchmark run; line count fell from 401 to 397. |
| `task_success_rate` | unknown | No fresh harness run in this seam. |
| `review_tas_rate` | unknown | Parent reviewer pending. |
| `maintenance_locality` | pass | Skill-owned first-load, worksheet, and legacy projection changed. |
| `composition_clarity` | pass | Init, Horizon, Goal, and capability-skill boundaries are explicit. |

## Proof Artifacts

- Skill-local evals, when needed: no existing harness eval changed
- Structure evals, when needed: scoped old-reference sweep
- Reviewer receipt: pending TASK-0321 reviewer
- Validator: `check_skills.py`
- Eval required: no
- Evidence gaps: real full-mode harness creation run

## Before Behavior

- Proposed product-local strategy/work-lane files and generated product index.

## After Behavior

- Maps recurring outputs directly to reusable or project-local capability
  skills under one project goal contract.

## Followups

- Parent integration QA should confirm no replacement catalog schema appeared.
