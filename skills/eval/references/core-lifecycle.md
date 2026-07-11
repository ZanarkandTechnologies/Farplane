---
title: Core Lifecycle Eval Matrix
owner: eval
status: active
updated_at: 2026-07-11
---

# Core Lifecycle Eval Matrix

This is the canonical bounded set used when Farplane claims core lifecycle eval
coverage. Each owner must keep at least one happy-path case, one authority or
ownership-boundary case, and one highest-risk failure case. A valid JSON file
and lint pass prove fixture readiness; run artifacts are required before
claiming behavior success.

| Lifecycle stage | Skill owners |
| --- | --- |
| Bootstrap and strategy | `init-advisor`, `harness-creator`, `horizon-advisor` |
| Execution compilation and recurring work | `goal-advisor`, `automation-advisor`, `pulse-update` |
| Work supply and interval learning | `ticket-opportunity-generator`, `interval-update`, `feed-scout` |
| Self-improvement | `dogfood-review`, `self-improve` |
| Review and completion | `worker-artifact-review-request`, `impl-plan`, `qa`, `review`, `close-ticket` |

```text
core_lifecycle_eval_readiness(skill_set)
  -> every_skill_has(eval_task.json)
   + every_skill_has(happy_path, authority_boundary, highest_risk_failure)
   + query_lint_passes

core_lifecycle_behavior_proof(skill_set)
  -> readiness
   + representative_eval_run_artifacts
   + reviewed_results
```
