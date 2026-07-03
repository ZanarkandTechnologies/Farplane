---
kind: project-ops-memory
status: draft
project: TODO
created_at: TODO
updated_at: TODO
framework_template_version: "0.1.1"
owner: interval-update
source_of_truth:
  - farplane/harness.md
  - farplane/goals.yaml
  - farplane/products.md
  - docs/farplane-framework/pulse-and-interval-loop.md
---

# Project Ops Memory

This file is active operating memory: compact, mutable context for what the
autonomous team is doing now. Stable strategy stays in `farplane/goals.yaml`,
product lanes stay in `farplane/products.md`, executable work stays in
`tickets/`, and dated receipts stay under `.farplane/reports/`.

## Current Focus

TODO one paragraph or bullet naming the active frontier.

## Active Projects

### TODO Active Project

- `lane:` TODO product/work lane
- `goal_axes:` TODO goal_axis
- `contribution_mode:` TODO revenue | validated_learning | proof_quality | distribution | reusable_harness_capability | unblock_value
- `weekly_runway_decision:` continue | narrow | pause | instrument | stop | escalate_to_revenue
- `expected_reward:` TODO what evidence would justify more runway
- `done_signal:`
  - TODO observable finish or progress signal
- `critical_path:`
  1. TODO next ordered step
- `next_frontier:`
  - TODO ticket, proof, or setup step

## Tracked Feedback

- `content:` TODO content IDs, URLs, or review windows the agent should inspect
  when relevant; keep raw metrics in observation snapshots, not here.
- `customer_or_user_feedback:` TODO source refs or gaps
- `runtime_or_product_feedback:` TODO dashboards, logs, reports, or gaps
- `autonomy_time:` TODO local Codex/Farplane event ledgers, spawned-thread
  ledgers, or gaps for human attention vs autonomous worker time
- `repo_adoption:` TODO GitHub repo or package/download source refs when this
  project ships as open source or developer tooling
- `source_gaps:` TODO missing credentials, APIs, ledgers, or feedback mechanisms

## Next Frontier

- `primary:` TODO
- `secondary:` TODO

## Constraints

- Do not mutate `farplane/goals.yaml`, `farplane/products.md`, publishing,
  accounts, spend, deploys, customer contact, or product boundaries from
  ops-memory alone.
- Do not create a roadmap registry, project schema, database, UI, hidden
  scheduler, or ticket-drainer from this file.
- Use this file to choose the active frontier; use tickets to execute work.

## Parking Lot

- TODO items that are real but not worth active budget this week

## Recent Decisions

- TODO dated compact decision notes

## Pulse Notes

- When creating next-wave tickets, cite the active project and frontier step
  that justified the ticket.
- If this file is stale, missing, or contradicted by the latest Daily/Weekly
  strategy, record that in the Pulse report instead of guessing.
- If maintenance is selected, name the active frontier it unblocks.
