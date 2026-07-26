---
title: "Lean Goal evaluation loop migration"
status: complete
owner: goal-advisor
created_at: 2026-07-27
updated_at: 2026-07-27
kind: skill-audit
---

# Lean Goal Evaluation Loop Migration

## Behavior Delta

Before, the generic Goal program moved directly from a bounded action to
progress writeback. Budgets also exposed a subagent-count dimension, ML
Autoresearch was absent from the allowed mode list, and optimization progress
duplicated selection and receipt detail on every turn.

After, every Goal uses:

```text
choose -> act -> evaluate -> record observation/evidence/learning -> next action
```

The ticket or active skill owns evaluator meaning. `program.md` binds it into
continuation. Optimization roadmaps remain in `program.md`; `progress.md`
stores compact observations and links to detailed immutable receipts. ML
experiment expectations remain preregistered in those receipts so surprising
results can be investigated before promotion or rejection.

## Evidence

- Baseline:
  `.farplane/evals/runs/20260726-203305-goal-loop-lean-baseline/summary.json`
  (`1/3` pass; Goal Advisor missed required packet detail and Self Improve
  omitted required writeback fields).
- Candidate receipts:
  - `.farplane/evals/runs/20260726-203631-goal-loop-lean-candidate/summary.json`
    preserved the ML Autoresearch TAS-A pass and exposed missing Goal Advisor
    and Self Improve output contracts.
  - `.farplane/evals/runs/20260726-204116-goal-loop-lean-final/summary.json`
    promoted Self Improve to TAS-A after budget, eligibility, and concrete
    writeback hardening.
  - `.farplane/evals/runs/20260726-204258-goal-loop-lean-goal-final/summary.json`
    promoted Goal Advisor to TAS-A after enforcing the literal `Files:`
    manifest and named drift reviewer.
- Deterministic checks: skill-system validation, eval-query lint, JSON parsing,
  documentation references/parity, and diff whitespace validation.
- Scope: generic Goal templates, Goal Advisor, Self Improve, ML Autoresearch,
  focused eval expectations, and the owning framework explanation.

## Structure Review

- Kept first-load behavior: mode selection, evaluation, surprise handling,
  budget, continuation, and writeback rules.
- Kept conditional detail in program presets and prompt templates.
- Deleted duplication: mandatory rejected-alternative and full-receipt progress
  fields; subagent count as an execution-budget dimension.
- Added no new runtime, state owner, or public command.
