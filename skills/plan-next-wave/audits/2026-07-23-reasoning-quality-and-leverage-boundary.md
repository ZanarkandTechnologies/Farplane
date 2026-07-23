---
title: Plan Next Wave reasoning quality and leverage boundary
owner: plan-next-wave
status: complete
kind: skill-audit
created_at: 2026-07-23
---

# Plan Next Wave Reasoning Quality And Leverage Boundary

## Behavior Delta

Before, Plan Next Wave required grounded evidence, an objective contribution,
and a falsifier but did not explicitly reject contradictions among those
fields. The review index also retained the obsolete
`ticket-opportunity-quality` family from the retired free-form ticket generator.

After, call admission requires one consistent premise across arguments,
evidence, why-now rationale, objective contribution, and falsifier. Plan Next
Wave explicitly owns only bounded refill ranking and does not call
`leverage-advisor`; the advisor remains the operator-facing owner for capability
roadmaps and contingent compounding campaigns. The obsolete rubric and its
index routes were removed.

## Ownership

- Runtime call consistency: `skills/plan-next-wave/SKILL.md` and
  `qa_checklist.md`.
- Variable behavior proof: `skills/plan-next-wave/evals/evals.json`.
- Stable planner/advisor boundary:
  `docs/features/FEAT-0071-project-work-pulse.md`.
- Review routing: general `skill-contract`, `evidence-quality`, and
  `integration-readiness` families.

## Proof

- Focused Plan Next Wave eval JSON validation and query-spoiler check.
- Live Codex + Codex-judge eval:
  `.farplane/evals/runs/20260723-145849-20260723-reasoning-quality`;
  `TAS-A`, 8/8 assertions, including contradiction rejection and same-premise
  falsifier alignment.
- Skill registry and link regeneration through `check_skills.py --write`.
- Core mining tests cover mechanically visible redundant and contradictory
  structured output.
- Independent reviewer rereview passed `TAS-A` for `skill-contract` and
  `integration-readiness` after stale generated graph references were removed.

Baseline comparison was skipped because the surrounding Plan Next Wave
migration already exists as an uncommitted worktree delta, so reconstructing a
clean pre-change baseline in this checkout would not be attributable. The
candidate behavior is supported by the focused live eval and deterministic
Core tests.
