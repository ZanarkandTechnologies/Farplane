---
skill: ml-autoresearch
date: 2026-07-22
change_type: structure
owner: skill-creator
status: pass
review_route: reviewer
before_ref: absent
after_ref: skills/ml-autoresearch/SKILL.md@TASK-0401
reasoning_basis: deliberative_advice
proof_artifacts:
  - .farplane/evals/runs/20260721-193158-task-0401-replanning
  - .farplane/evals/runs/20260721-193727-task-0401-composition-repair
  - .farplane/evals/runs/20260721-193950-task-0401-artifact-owner
eval_required: yes
---

# Initial ML Autoresearch Skill

## Change

- Before: no discoverable Farplane ML experiment-loop entrypoint.
- After: one Tier-3 campaign skill with a frozen evaluator, baseline, bounded
  mutable surface, experiment receipts, budget, Goal Packet, and evidence-
  updated Leverage Advisor selection.
- Why: Karpathy's minimal loop needs Farplane-native state, authority, and proof
  boundaries without becoming a second orchestration runtime.
- Tradeoff accepted: the skill is a harness contract, not an experiment runner
  or global technique database.

## First-Principles Reasoning

- Objective: maximize trustworthy metric improvement per bounded experiment.
- Placement logic: ML-specific execution belongs in Tier 3; generic selection
  stays in Leverage Advisor; Goal Advisor compiles the native Goal.
- Expected behavior delta: one campaign can learn from failed experiments and
  select the next highest-leverage move without multiplying tickets.
- Proof needed: freeze baseline/evaluator, replan from program plus progress,
  route catalog gaps, and keep attempts inside one campaign.

## Binary Rubric

| Check | Verdict | Evidence |
| --- | --- | --- |
| `first_load_sufficiency` | pass | Mandatory composition and campaign contract are explicit in `SKILL.md`. |
| `reference_load_precision` | pass | One program template owns detailed Goal-loop configuration. |
| `missing_context_rate` | pass | Missing catalogs produce a bounded source gap instead of invented rankings. |
| `noisy_context_rate` | pass | No global registry, daemon, runner, or attempt tickets were added. |
| `duplicated_instruction_count` | pass | Generic selection is delegated to Leverage Advisor. |
| `prompt_size_tokens` | pass | Domain contract is compact and references one preset. |
| `task_success_rate` | pass | Four focused behavior cases pass across the listed runs. |
| `review_tas_rate` | pass | TASK-0401 final review returned TAS-A. |
| `maintenance_locality` | pass | Skill, QA, evals, template, and audit are package-local. |
| `composition_clarity` | pass | Program owns roadmap/replan policy; progress owns observations; named advisors retain single responsibilities. |

## Proof Artifacts

- Skill-local evals: all four ML Autoresearch cases pass across the listed runs.
- Structure evals: `quick_validate.py`, `check_skills.py --write`.
- Reviewer receipt: `tickets/TASK-0401/artifacts/review/final-review.md`.
- Validator: eval query lint, JSON parsing, and ticket metadata pass.
- Eval required: yes.
- Evidence gaps: live campaign efficacy remains for the TASK-0055 pilot.

## Before Behavior

- ML campaigns had no stable, discoverable Farplane composition contract.

## After Behavior

- `program.md` owns the initial roadmap and replan policy; before each
  experiment Leverage Advisor consumes that roadmap plus `progress.md`
  learnings, current receipts, and remaining budget to select one move.

## Followups

- Pilot the contract on TASK-0055 outside this harness-shipping ticket.
