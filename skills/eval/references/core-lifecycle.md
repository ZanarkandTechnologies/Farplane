---
title: Core Lifecycle Eval Matrix
owner: eval
status: active
updated_at: 2026-07-19
---

# Core Lifecycle Eval Matrix

This is the canonical bounded set used when Farplane claims core lifecycle eval
coverage. Each owner must keep at least one happy-path case, one authority or
ownership-boundary case, and one highest-risk failure case. A valid JSON file
and lint pass prove fixture readiness; run artifacts are required before
claiming behavior success.

| Lifecycle stage | Skill owners |
| --- | --- |
| Bootstrap and objectives | `setup-advisor`, `goal-advisor` (metric card) |
| Execution compilation and recurring work | `goal-advisor`, `automation-advisor` |
| Work supply and operating review | `pm`, `report-gen`, `feed-scout` |
| Skill self-improvement | `eval`, `self-improve` |
| Review and completion | `telegram-message`, `impl-plan`, `qa`, `review` |

```text
core_lifecycle_eval_readiness(skill_set)
  -> every_skill_has(evals/evals.json)
   + every_skill_has(happy_path, authority_boundary, highest_risk_failure)
   + query_lint_passes

core_lifecycle_behavior_proof(skill_set)
  -> readiness
   + representative_eval_run_artifacts
   + reviewed_results
```
