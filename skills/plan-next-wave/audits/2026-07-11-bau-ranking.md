---
skill: plan-next-wave
date: 2026-07-11
change_type: behavior
owner: skill-maintenance
status: implemented
review_route: reviewer
reasoning_basis: TASK-0319
eval_required: yes
---

# BAU Ranking Audit

## Change

- Before: `plan_next_wave` preferred leverage but did not explicitly exclude
  harness self-improvement or expose its bottleneck/lever/ranking reasoning.
- After: the planner names the bottleneck, enumerates BAU levers, generates
  distinct moves, rejects self-improvement candidates, ranks by impact,
  bottleneck relief, urgency, proof speed, compounding reuse, cost/risk, and
  review load, and records depriorities.
- Boundary: user-facing product features, product documentation, reliability,
  and operational automations remain valid BAU when their primary outcome is
  project progress rather than improvement of Farplane's execution harness.

## Proof

- QA gates: `bau_boundary` and `leverage_and_ranking`
- Eval cases: `planner_rejects_harness_self_improvement`,
  `planner_preserves_bau_docs_automation_and_customer_features`, and
  `planner_ranks_compounding_bau_leverage`
- JSON parse: `jq empty skills/plan-next-wave/eval_task.json`
