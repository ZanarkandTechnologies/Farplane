---
skill: leverage-advisor
date: 2026-07-22
change_type: behavior
owner: skill-maintenance
status: pass
review_route: reviewer
before_ref: skills/leverage-advisor/SKILL.md@pre-TASK-0401
after_ref: skills/leverage-advisor/SKILL.md@TASK-0401
reasoning_basis: deliberative_advice
proof_artifacts:
  - .farplane/evals/runs/20260721-193158-task-0401-replanning
eval_required: yes
---

# Evidence-Updated Leverage Selection

## Change

- Before: ranked leverage plays from a capability and recommended one proof.
- After: also consumes a lever catalog, roadmap progress, and remaining budget;
  returns a contingent next wave and explicit replan conditions.
- Why: repeated improvement loops need one decision owner that compounds
  observed learning instead of advancing a fixed experiment list.
- Tradeoff accepted: selection language remains similar to Plan Next Wave until
  real stable duplication proves a smaller primitive is warranted.

## First-Principles Reasoning

- Objective: choose the highest-value next move from current evidence.
- Placement logic: extend the existing Tier-2 decision owner; do not add a new
  planner, registry, runner, or state surface.
- Expected behavior delta: rank bottleneck fit, information gain, downstream
  unlocks, proof speed, cost, risk, and interference after every result.
- Proof needed: reject fixed ladders, surface missing-catalog gaps, and preserve
  campaign-ticket ownership.

## Binary Rubric

| Check | Verdict | Evidence |
| --- | --- | --- |
| `first_load_sufficiency` | pass | Signature and main checklist bind catalog, progress, budget, selection, and replan outputs. |
| `reference_load_precision` | pass | Research routes are conditional on an evidence-thin frontier. |
| `missing_context_rate` | pass | Eval selects from explicit progress observations without inventing facts. |
| `noisy_context_rate` | pass | No global catalog or new state schema was added. |
| `duplicated_instruction_count` | pass | Domain loops call the advisor instead of copying its scoring workflow. |
| `prompt_size_tokens` | pass | One existing skill grew; no always-loaded prompt changed. |
| `task_success_rate` | pass | Focused Leverage Advisor eval passed. |
| `review_tas_rate` | pass | TASK-0401 final review returned TAS-A. |
| `maintenance_locality` | pass | Behavior, QA, and evals remain skill-local. |
| `composition_clarity` | pass | Advisor chooses; callers execute; ticket artifacts own state. |

## Proof Artifacts

- Skill-local evals: focused Leverage Advisor pass in the listed Eval run.
- Structure evals: `quick_validate.py`, `check_skills.py --write`.
- Reviewer receipt: `tickets/TASK-0401/artifacts/review/final-review.md`.
- Validator: eval query lint and ticket metadata checks pass.
- Eval required: yes.
- Evidence gaps: none for the shipped harness contract; live campaign efficacy remains a pilot question.

## Before Behavior

- The advisor stopped at one ranked recommendation and first proof.

## After Behavior

- The advisor recomputes the next wave from roadmap, progress evidence, and
  remaining budget, with source-gap and stop/replan branches.

## Followups

- Extract a smaller primitive only after another Tier-2 caller demonstrates
  stable semantic duplication.
