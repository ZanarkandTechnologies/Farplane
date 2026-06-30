---
kind: project-ops-memory
status: active
project: Farplane
created_at: 2026-06-30
updated_at: 2026-06-30
owner: interval-update
source_of_truth:
  - farplane/harness.md
  - farplane/goals.md
  - farplane/products.md
  - docs/farplane-framework/pulse-and-interval-loop.md
---

# Farplane Ops Memory

This file is Farplane's active operating memory: the compact, mutable place for
what the autonomous team is trying to accomplish now. Stable strategy stays in
`farplane/goals.md`, product lanes stay in `farplane/products.md`, executable
work stays in `tickets/`, and dated receipts stay under `.farplane/reports/`.

## Current Focus

Make Pulse and Interval act like an autonomous team that works from an explicit
frontier instead of planning one-ticket crumbs or defaulting to low-value
maintenance.

## Active Projects

### Pulse / Interval Autonomy

- `lane:` productization
- `goal_axes:` project_control, quality_and_proof, validated_self_improvement
- `done_signal:`
  - Pulse can name the active focus and next frontier before creating tickets.
  - Daily and Weekly can refresh the active focus without rewriting goals or
    products.
  - Maintenance stays parked unless it unblocks the active frontier.
- `critical_path:`
  1. Add this ops-memory surface.
  2. Teach Pulse to read and cite the active frontier before next-wave tickets.
  3. Teach Interval to refresh focus, active projects, constraints, and parking
     lot entries.
  4. Run one manual Pulse beat and judge whether it avoids one-ticket crumbs.
- `next_frontier:`
  - Implement `TASK-0251`.
  - After implementation, run a manual Pulse beat and record whether the report
    cites ops-memory.

### Evidence-To-Content Loop

- `lane:` experiments, ablations, trust_distribution
- `goal_axes:` distribution_from_evidence, validated_self_improvement
- `done_signal:`
  - one accepted ablation or experiment proof
  - one findings report
  - one paper-style diagram or content-ready visual plan
  - one technical X/Instagram content draft
  - one KPI or feedback capture note
- `critical_path:`
  1. Select the strongest implemented harness claim to test.
  2. Define baseline, variant, and proof route.
  3. Run or simulate the smallest honest experiment.
  4. Write findings.
  5. Convert findings into technical content.
  6. Capture feedback or metric source gaps.
- `next_frontier:`
  - Wait until the ops-memory/Pulse frontier is in place, then let Pulse create
    the first evidence-to-content tickets from this path.

## Next Frontier

- `primary:` finish `TASK-0251` and prove Pulse/Interval can discover
  ops-memory.
- `secondary:` turn the evidence-to-content loop into the next active ticket
  wave after Pulse cites this memory.

## Constraints

- Caps and cadence live in `.farplane/automation/heartbeat-policy.json`, not in
  this file.
- Do not mutate `farplane/goals.md`, `farplane/products.md`, publishing,
  accounts, spend, deploys, or customer contact from ops-memory alone.
- Do not create a roadmap registry, project schema, database, UI, hidden
  scheduler, or ticket-drainer from this file.
- Use this file to choose the active frontier; use tickets to execute work.

## Parking Lot

- `TASK-0246` Kenji Review metadata cleanup if it continues to confuse Pulse.
- Strict YAML frontmatter validation for ticket metadata.
- `autonomy_profile` / `review_mode` metadata idea; not needed for the current
  MVP.
- Dirty-surface closeout work that does not unblock the current frontier.

## Recent Decisions

- Use `farplane/ops-memory.md`, not `farplane/ops.md`, to make the memory split
  explicit.
- Keep roadmaps and projects as flexible Markdown sections inside ops-memory,
  not as new artifact families.
- Plan from the active frontier, execute up to policy cap, and record receipts.

## Pulse Notes

- When creating next-wave tickets, cite the active project and frontier step
  that justified the ticket.
- If this file is stale, missing, or contradicted by the latest Daily/Weekly
  strategy, record that in the Pulse report instead of guessing.
- If maintenance is selected, name the active frontier it unblocks.
