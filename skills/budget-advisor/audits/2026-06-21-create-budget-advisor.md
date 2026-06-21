---
title: "Create Budget Advisor Skill Audit"
status: draft
owner: skill-creator
created_at: 2026-06-21
updated_at: 2026-06-21
tags:
  - skills
  - budget-advisor
  - audit
refs:
  - skills/budget-advisor/SKILL.md
  - docs/skills/system.md
  - docs/skills/best-practices.md
  - docs/fundamentals/harness-engineering-doctrine.md
---

# Create Budget Advisor Skill Audit

## Change

Created `skills/budget-advisor` as a Tier 2 workflow interface that resolves a
budget-aware skill call into concrete execution template refs, parameters, and
guardrails.

## Placement

- Primary owner: `skills/budget-advisor`
- Secondary sync points: budget-aware caller skills such as `advise`, `plan`,
  `review`, `agent-qa-test`, and `deliberative-advice`
- Rejected as primary owner:
  - root/global prompt: too broad before the workflow proves value
  - `advise`: too narrow; budget routing should apply to multiple skills
  - `goal-advisor`: owns continuation loops, not per-skill budget templates
  - `review`: owns judgment over artifacts, not budget routing

## Review Notes

- First-load contract includes signature, budget request shape, todo workflow,
  core rules, reference map, and output shape.
- Branch-specific procedures live in references:
  - budget modes and time mapping
  - review depth
  - ensemble lanes and persona prompts
  - tournament / hierarchical aggregation
  - `advise` toy example
- The skill returns a program for the caller to execute. It does not spawn
  subagents or own hidden orchestration.

## Proof Plan

- Run `python3 skills/skill-maintenance/scripts/check_skills.py --write`.
- Run relevant registry/tier validation surfaced by the skill-maintenance
  script.
- Manually inspect that reference links resolve and the main skill is not too
  thin.

## Early Behavior Probe

- `agent-behavior-test` artifact:
  `experiments/agent-behavior-test/budget-advisor-2026-06-21/run/score.json`
- Scenario: fresh agent resolves an `advise` call with three complete persona
  prompts, `ensemble.count: 3`, `perspective_mode: different`, and
  `review_depth: 1`.
- Result: pass. The child loaded `SKILL.md`, `ensemble-lanes.md`,
  `review-depth.md`, and `advise-example.md`; preserved the full persona
  prompts; returned a concrete Budget Program; and did not spawn lanes or answer
  the advice decision itself.
- Remaining risk: this proves the happy path only. The skill-local eval file now
  includes missing-persona, large-ensemble, and time/mode mapping cases to catch
  subtler confusion before broader rollout.

## Eval Smoke

- Added `skills/budget-advisor/eval_task.json` with four cases:
  persona-lane happy path, missing personas, large ensemble aggregation, and
  budget mode/time mapping.
- First smoke:
  `.farplane/evals/runs/20260621-085423-budget-advisor-smoke/summary.json`
  returned `B`. The agent routed correctly but omitted `SKILL.md` from refs and
  compressed persona prompts.
- Tightening applied: `SKILL.md` and `ensemble-lanes.md` now require
  `source_refs` and complete `PersonaPrompt` objects in `resolved_params`.
- Second smoke:
  `.farplane/evals/runs/20260621-085621-budget-advisor-smoke-after-tighten/summary.json`
  returned `D` because the eval task did not explicitly point at the newly
  created source skill; the child agent drifted into `advise` /
  `deliberative-advice`.
- Final smoke:
  `.farplane/evals/runs/20260621-085814-budget-advisor-smoke-explicit-path/summary.json`
  returned `A` after the eval query explicitly started from
  `skills/budget-advisor/SKILL.md`.

## Design Tradeoffs Found

- First-load `SKILL.md` should stay short, but the output contract must be
  strict enough to prevent lossy persona compression.
- Reference files are the right place for template mechanics, but eval prompts
  for newly-created skills should name the source path until the skill is
  installed and discoverable in child Codex sessions.
- The behavior probe and eval smoke test different things: the probe verifies a
  tightly instructed child can follow the skill; the eval checks whether a more
  natural budget-advisor request routes correctly.
