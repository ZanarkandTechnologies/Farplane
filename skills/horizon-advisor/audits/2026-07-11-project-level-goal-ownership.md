---
skill: horizon-advisor
date: 2026-07-11
change_type: behavior
owner: skill-maintenance
status: pass
review_route: reviewer
before_ref: skills/horizon-advisor/SKILL.md@pre-TASK-0321
after_ref: skills/horizon-advisor/SKILL.md
reasoning_basis: first_principles
proof_artifacts:
  - tickets/TASK-0321/ticket.md
eval_required: no
---

# Horizon Advisor Goal-Ownership Audit

## Change

- Before: Horizon split goal/KPI ownership between `goals.yaml` and product
  files.
- After: `goals.yaml` is the project strategy owner; capability skills consume
  goals without owning parallel trees.
- Why: one project planner needs one value-direction contract.
- Tradeoff accepted: no per-category KPI membership view.

## First-Principles Reasoning

- Objective: make long-horizon planning coherent and inspectable.
- Placement logic: Horizon owns strategy; capability skills own workflows.
- Expected behavior delta: Horizon reads and writes no product-controller file.
- Proof needed: prompt/reference sweep and parent integration review.

## Binary Rubric

| Check | Verdict | Evidence |
| --- | --- | --- |
| `first_load_sufficiency` | pass | Signature, todo, and handoff remain complete. |
| `reference_load_precision` | pass | Project-goals reference is still branch-loaded. |
| `missing_context_rate` | pass | Goals, harness, tickets, metrics, and memory remain explicit inputs. |
| `noisy_context_rate` | pass | Duplicate category strategy inputs removed. |
| `duplicated_instruction_count` | pass | One strategy owner is named. |
| `prompt_size_tokens` | unknown | No token benchmark run; line count fell from 216 to 213. |
| `task_success_rate` | unknown | No live strategy run in this seam. |
| `review_tas_rate` | unknown | Parent reviewer pending. |
| `maintenance_locality` | pass | Only Horizon-owned skill/reference changed. |
| `composition_clarity` | pass | Goal Advisor remains the execution compiler. |

## Proof Artifacts

- Skill-local evals, when needed: not required; behavior is contract placement
- Structure evals, when needed: scoped old-reference sweep
- Reviewer receipt: pending TASK-0321 reviewer
- Validator: `check_skills.py`
- Eval required: no
- Evidence gaps: independent integration review

## Before Behavior

- Patched product files for KPI membership and regenerated their index.

## After Behavior

- Writes project strategy to `goals.yaml` and hands execution to Goal Advisor.

## Followups

- Bind the final metric owner after TASK-0322 lands `metrics.yaml`.
