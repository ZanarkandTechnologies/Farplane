---
skill: consolidate
date: 2026-06-27
change_type: behavior
owner: skill-creator
status: pass
review_route: deliberative_advice
before_ref: none
after_ref: skills/consolidate/SKILL.md
reasoning_basis: deliberative_advice
proof_artifacts:
  - skills/consolidate/eval_task.json
  - python3 skills/skill-maintenance/scripts/check_skills.py --write
  - .farplane/evals/runs/20260627-062615-consolidate-skill-final/summary.json
eval_required: yes
---

# Create Consolidate Skill Audit

## Change

- Before: Consolidation behavior was split across skill-maintenance,
  documentation, knowledge-tidier, update-memory, and ad hoc ticket plans.
- After: `consolidate` is a Tier 1 primitive for template-aware,
  value-preserving compression with explicit parameters, value functions, unit
  decisions, loss checks, and owner handoffs.
- Why: Multiple Tier 2 and Tier 3 workflows need the same base move: inventory
  units, identify the owning template, score value, rebuild minimally, and prove
  required value was not lost.
- Tradeoff accepted: The primitive is created before every downstream workflow
  has adopted it; the first-load contract stays narrow to avoid becoming a
  generic cleanup engine.

## First-Principles Reasoning

- Objective: preserve useful behavior and proof while reducing duplication,
  fluff, stale material, and wrong-owner sprawl.
- Placement logic: Tier 1 fits because documentation, skill-maintenance,
  update-memory, knowledge-tidier, interval-update, metric-advisor, and eval
  workflows can all depend on the same base consolidation move.
- Expected behavior delta: Agents should distinguish hard constraints from
  value judgment, rebuild into templates, and run loss checks instead of
  summarizing or deleting by word count.
- Proof needed: skill registry validation plus behavior eval cases for
  template preservation, constraint handling, and gotcha/checklist/eval routing.

## Binary Rubric

| Check | Verdict | Evidence |
| --- | --- | --- |
| `first_load_sufficiency` | pass | `SKILL.md` includes context, signature, todo path, gates, examples, gotchas, and output. |
| `reference_load_precision` | pass | No skill-local references added; first-load owns the default path. |
| `missing_context_rate` | pass | Parameters, constraints, value function, actions, and loss check are defined in first load. |
| `noisy_context_rate` | pass | No long external workflow prose or provider catalog included. |
| `duplicated_instruction_count` | pass | Related skill docs are referenced but not copied. |
| `prompt_size_tokens` | pass | First-load contract is compact for a Tier 1 primitive. |
| `task_success_rate` | pass | `consolidate-skill-final` ran 3 tasks with 3 A verdicts and pass rate 1.0. |
| `review_tas_rate` | pass | Final reviewer returned TAS-A for the `consolidate` scope with no blocking findings. |
| `maintenance_locality` | pass | Skill package owns primitive behavior; owner-specific edits remain with caller skills. |
| `composition_clarity` | pass | Signature names inputs, outputs, gates, routes, and failure modes. |

## Proof Artifacts

- Skill-local evals, when needed: `skills/consolidate/eval_task.json`
- Behavior eval:
  `.farplane/evals/runs/20260627-062615-consolidate-skill-final/summary.json`
  passed with 3/3 A verdicts.
- Structure evals, when needed:
  `python3 skills/skill-maintenance/scripts/check_skills.py --write` passed.
- Reviewer receipt: final reviewer returned TAS-A for the `consolidate` scope
  with no blocking findings; whole-worktree read-only registry checks remain
  conditional on unrelated untracked `skills/infographic/` cleanup.
- Validator: `check_skills.py --write` passed; registry sync, eval query
  lint, doc refs, skill capability fixtures, todo tier checks, and Tier 0
  phase protocol checks all passed.
- Eval required: yes.
- Evidence gaps: none for the `consolidate` skill scope. Whole-worktree shipped
  claim should wait for unrelated registry staleness caused by untracked
  `skills/infographic/`.

## Before Behavior

- Consolidation was implicit and easy to confuse with summarization,
  documentation cleanup, or skill refinement.

## After Behavior

- Consolidation has a primitive contract:
  `template + constraints + value_function -> minimal artifact + loss check`.

## Followups

- Adopt `consolidate` in `skill-maintenance`, `documentation`,
  `knowledge-tidier`, and `update-memory` on contact.
- Revisit whether TASK-0232 should reference `consolidate` directly after it is
  implemented.
