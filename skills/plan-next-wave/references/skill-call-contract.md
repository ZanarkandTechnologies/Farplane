---
title: Plan Next Wave skill-call contract
status: active
owner: plan-next-wave
updated_at: 2026-07-17
---

# Skill-call contract

```yaml
call_id:
title:
skill_ref:
area_id: # optional passive ICP/metric context
arguments: {} # exactly the selected skill's required_arguments
admission: # required only when planner_contract.admission_contract exists
  workstream_key:
  decision: admit
  open_lifecycle_refs: [] # exact current refs; count must remain below configured capacity
  release_condition:
  reason:
expected_artifact:
current_alternative:
why_now:
evidence_refs: []
objective_contribution:
  ultimate_kpi_id: revenue_usd | evidence_distribution_reach | active_subscriptions
  contribution_type: outcome | enabler | guard
  kpi_or_guard_id:
  causal_mechanism:
  expected_change:
  forecast_basis:
    kind: measured_baseline | cited_comparable | configured_threshold | source_gap
    ref:
    source_gap:
  metric_provider:
  signal_horizon:
  check_in_at:
lifecycle:
  status: todo
  depends_on: []
  human_gate: none | [tag, reason]
  due_at: timezone-bearing ISO-8601 timestamp # optional; omit when evidence supplies none
proof:
  success:
  falsifier:
dedupe:
  compared_against: []
  decision: novel | materially_distinct
ranking:
  reason:
  confidence: low | medium | high
  time_to_signal:
  cost:
  risk:
  human_load:
  interference:
```

The skill owns the workflow. `arguments` binds its public inputs; it never
contains workflow steps, copied todos, phases, or a nested ticket spec.

For an admission-controlled skill, the planner must inspect the current
workstream before proposing the call. `hold`, `preempt_request`, and `reject`
belong in `rejections`; only an `admit` receipt whose exact current open refs
remain below `max_open_lifecycles` may appear in `proposed_skill_calls`.
