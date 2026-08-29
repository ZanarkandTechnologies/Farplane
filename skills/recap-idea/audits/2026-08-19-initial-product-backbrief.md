---
skill: recap-idea
date: 2026-08-19
change_type: behavior
owner: skill-maintenance
status: pass
review_route: reviewer
before_ref: none
after_ref: working-tree
reasoning_basis: advise
proof_artifacts:
  - tickets/TASK-0438/artifacts/eval-proof.md
eval_required: yes
---

# Initial Product Backbrief Skill Audit

## Change

- Before: no reusable workflow tested shared product understanding after an
  extended discussion.
- After: `recap-idea` returns a proposed operated story, ASCII system
  map, boundaries, assumptions, conflicts, and alignment questions.
- Why: the Content Intelligence discussion showed that playback exposed
  semantic mistakes that ordinary summaries and plans had preserved.
- Tradeoff accepted: add one Tier 2 public skill rather than duplicate the
  checkpoint across planning skills.

## First-Principles Reasoning

- Objective: expose product-model disagreement before durable commitment.
- Placement logic: a skill is the smallest just-in-time reusable owner;
  `recap-task` remains operational recovery and `deep-interview` remains
  question-led intent clarification.
- Expected behavior delta: product discussions gain an explicit human-confirmed
  semantic checkpoint.
- Proof needed: distinct positive, conflict, composition, and negative-routing
  eval cases plus independent structure and readiness review.

## Binary Rubric

| Check | Verdict | Evidence |
| --- | --- | --- |
| `first_load_sufficiency` | pass | 4/4 native skill evals pass |
| `reference_load_precision` | pass | Reviewer TAS-A |
| `missing_context_rate` | pass | Conflict and source-boundary cases pass |
| `noisy_context_rate` | pass | Reviewer TAS-A |
| `duplicated_instruction_count` | pass | Reviewer TAS-A |
| `prompt_size_tokens` | pass | `SKILL.md` is 116 physical lines |
| `task_success_rate` | pass | Full rerun is 4/4 TAS-A |
| `review_tas_rate` | pass | Independent reviewer TAS-A |
| `maintenance_locality` | pass | Reviewer confirmed one skill owner |
| `composition_clarity` | pass | Recap composition and non-trigger controls pass |

## Proof Artifacts

- Skill-local evals: `skills/recap-idea/evals/evals.json`
- Structure evals: deterministic skill-maintenance checks
- Reviewer receipt: `tickets/TASK-0438/artifacts/reviewer.md` — TAS-A
- Validator: `check_skills.py --write` and query-spoiler check pass
- Eval required: yes
- Evidence gaps: baseline tied one composition case; operator confirmation
  remains the intentional runtime finish gate

## Before Behavior

- Agents could summarize discussions or recap task state without reconstructing
  the intended product as an operated, correctable model.

## After Behavior

- Operators can request one proposed shared model and correct it before the
  conversation becomes a PRD, ticket, or implementation plan.

## Followups

- None. Revisit Tier 1 promotion only after multiple Tier 2 callers prove the
  move as a base dependency.
