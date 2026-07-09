---
title: "Interval Ticket Reward Contract"
status: active
owner: interval-update
kind: reference
---

# Interval Ticket Reward Contract

Load this reference before creating ticket deltas from interval planning.

Every interval-planned ticket must carry expected reward at planning time.
Ticket deltas emitted by any interval report are part of the planning
algorithm, so they must include:

- frontmatter `rewards.kpi`
- a parseable `## Reward` fenced YAML block
- `kpi_rewards[]`
- `expected_reward`
- `check_in_at`
- `guard`

At least one `kpi_id` must come from
`farplane/products/<product>/product.md` KPI refs and resolve to
`farplane/bindings.yaml#metrics`. The KPI ID must match between frontmatter and
body.

If the interval cannot name the expected reward, emit downstream guidance or a
planning blocker instead of creating a ticket.
