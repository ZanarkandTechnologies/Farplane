---
kind: skill-audit
skill: harness-creator
status: complete
created_at: 2026-06-15
---

# Feedback Loop And Scrum Standard

## Decision

`harness-creator` now treats project operation as a Scrum-like loop with two
default automations:

- `ticket_update`: frequent leaf execution that advances one proceedable ticket
  or requests PM strategy help when blocked.
- `weekly_pm_update`: strategy/backlog refresh that may call `update_strategy`,
  `update_memory`, `harden_skill`, and `refine_skill` as subroutines.

Feedback loops are now required at init time. Missing feedback is represented
as a concrete skill capability plus a precise ticket, not as a generic
"create feedback loop" task.

## Rationale

The harness should not refine from vibes. Every project needs at least one
honest signal source before optimization starts. When the signal source does
not exist, the program should name the missing feedback skill first, then
ticket the access, export, connector, setup, or operator-label step that would
make the skill usable.

## Example

```harness-program
skill instagram_attention_graph {
  status: needs_access
  requires: [instagram_insights_export]
  use: "read attention graph, retention, replay, save, share, and comment signals"
}

ticket instagram_insights_export {
  type: unblock
  human_step: "Connect read-only metrics access or provide a CSV export"
  enables: [instagram_attention_graph]
  fallback: human_feedback("operator ranks recent posts manually")
}
```
