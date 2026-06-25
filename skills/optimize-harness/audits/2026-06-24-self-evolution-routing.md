---
skill: optimize-harness
date: 2026-06-24
change_type: behavior
owner: skill-maintenance
status: pass
review_route: self_check
before_ref: skills/optimize-harness/SKILL.md
after_ref: skills/optimize-harness/SKILL.md
reasoning_basis: first_principles
proof_artifacts:
  - skills/optimize-harness/SKILL.md
  - docs/farplane-framework/lifecycle.md
  - skills/interval-update/references/workflows/compounding-leverage-review.md
eval_required: no
---

# Self-Evolution Routing Audit

## Change

- Before: `optimize-harness` routed basic gap, placement, eval, self-improve,
  skill-maintenance, Goal Advisor, and review steps, but did not know the full
  self-evolving advisor matrix.
- After: `optimize-harness` explicitly binds loss terms and reward signals,
  reads Farplane goals/harness algebra for material self-evolution, routes
  strategy, leverage, proof, skill creation, skill maintenance, coding plans,
  Goal compilation, measured search, and review.
- Why: Weekly Interval can select bets where the harness behavior itself needs
  improvement. Those bets need one umbrella skill that diagnoses, places,
  proves, changes, and reviews without becoming a hidden loop.
- Tradeoff accepted: first-load grew, but remained under the rough 250-line
  budget because routing decisions are needed before execution.

## First-Principles Reasoning

- Objective: make self-evolution bets route through the right advisor or owner
  surface with explicit proof.
- Placement logic: `optimize-harness` owns whole behavior-gap optimization;
  individual advisors still own strategy, leverage scoring, proof, skill
  packaging, skill hardening, planning, execution compilation, and review.
- Expected behavior delta: agents should stop treating all harness improvement
  as either skill maintenance or generic strategy, and instead route through
  the smallest owner that reduces the named loss term.
- Proof needed: structure validation and doc-link checks are enough for this
  routing-doc update; no behavior eval was created because no executable
  behavior runner changed.

## Binary Rubric

| Check | Verdict | Evidence |
| --- | --- | --- |
| `first_load_sufficiency` | pass | `SKILL.md` includes loss term, metric/reward, routing, proof, accept/hold/rollback. |
| `reference_load_precision` | pass | References are direct skill/docs links with clear jobs. |
| `missing_context_rate` | pass | Farplane goals and harness algebra are named when material self-evolution is in scope. |
| `noisy_context_rate` | pass | Added text is routing-critical; no long examples or rare recipes added. |
| `duplicated_instruction_count` | pass | Lifecycle docs own the broad matrix; skill owns invocation routing. |
| `prompt_size_tokens` | pass | `SKILL.md` is 223 lines after the edit. |
| `task_success_rate` | unknown | No behavior eval run for this routing-only change. |
| `review_tas_rate` | unknown | No reviewer lane used for this self-contained routing update. |
| `maintenance_locality` | pass | `optimize-harness` owns umbrella behavior-gap routing; referenced skills own their domains. |
| `composition_clarity` | pass | Signature and todo list name reads, writes, gates, routes, and output. |

## Proof Artifacts

- Skill-local evals, when needed: not needed for routing-only documentation.
- Structure evals, when needed: `check_skills.py --write`.
- Reviewer receipt: not requested; self-check used.
- Validator: skill system checks and targeted tests.
- Eval required: no.
- Evidence gaps: future e2e eval should cover one Weekly Interval ->
  optimize-harness -> advisor route -> reward closure chain.

## Before Behavior

- Harness improvement requests could be routed through `optimize-harness`, but
  the skill under-described Horizon, Leverage, Proof Advisor, Skill Creator,
  Impl Plan, and Goal Advisor handoffs.

## After Behavior

- `optimize-harness` can act as the full self-evolution umbrella while
  preserving each advisor's owner boundary.

## Followups

- Add a focused e2e workflow eval once the first real weekly self-evolution
  route produces an artifact worth preserving.
