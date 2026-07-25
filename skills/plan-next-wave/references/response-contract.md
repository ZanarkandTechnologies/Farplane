---
title: Plan Next Wave response contract
status: active
owner: plan-next-wave
updated_at: 2026-07-17
---

# Response contract

Return exactly one JSON object:

```yaml
global_query_receipt: {}
diagnosis:
  problem_context: []
  objective_movement: []
  wave_size: 1
  dogfood_role: current_context_only | not_supplied
  hard_guard: {}
skill_receipts: []
progressive_queries: []
proposed_skill_calls: []
rejections: []
decision:
  admitted_call_ids: []
  source_gaps: []
  human_request: null
  unused_capacity_reason: null
  validation_receipt: {}
  no_materialization_receipt:
    tickets_written: 0
    materialized: false
    executed: false
    owner: pulse-update
```

`proposed_skill_calls` is canonical. No other section repeats a full call.
`admitted_call_ids` contains only IDs from that list and at most `wave_size`
items. An empty wave names the exact guard, source, evidence, duplication,
authority, conflict, or leverage reason.
