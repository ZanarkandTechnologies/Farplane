---
title: "Horizon Loop"
status: active
owner: farplane-framework
created_at: 2026-06-26
updated_at: 2026-07-25
tags:
  - farplane
  - systems
  - horizon-loop
refs:
  - docs/features/FEAT-0029-goal-packet-architecture-for-native-codex-goals.md
  - docs/features/FEAT-0065-pulse-and-interval-automation.md
  - docs/features/FEAT-0066-product-scoped-pulse-loops.md
  - docs/features/FEAT-0071-project-work-pulse.md
  - docs/features/FEAT-0067-daily-interval-review-reports.md
system_record_json: |
  {
    "id": "SYS-0003",
    "name": "Horizon Loop",
    "status": "implemented",
    "summary": "The project control loop where metric movement flows through report-first Interval review into the ticket board, with Work Pulse dispatch and Plan Next Wave as low-supply refill.",
    "owner_spec": "docs/systems/horizon-loop.md",
    "primary_feature_ref": "FEAT-0032",
    "feature_refs": [
      "FEAT-0029",
      "FEAT-0032",
      "FEAT-0065",
      "FEAT-0066",
      "FEAT-0067",
      "FEAT-0071"
    ],
    "refs": [
      "docs/features/FEAT-0029-goal-packet-architecture-for-native-codex-goals.md",
      "docs/features/FEAT-0065-pulse-and-interval-automation.md",
      "docs/features/FEAT-0066-product-scoped-pulse-loops.md",
      "docs/features/FEAT-0067-daily-interval-review-reports.md",
      "docs/features/FEAT-0071-project-work-pulse.md"
    ],
    "last_verified": "2026-07-25"
  }
---
# Horizon Loop

The project control loop where metric movement and evidence flow through
report-first Interval review into the ticket board, then Work Pulse dispatches
or checks in work. Plan Next Wave remains the side-effect-free low-supply
refill path. Native Goal Packets remain the continuation mechanism for
material ticket execution.

```text
horizon_loop(change, repo_state?) -> owned_feature_set + boundary_decision + maintenance_signal
```

## At A Glance

- System ID: `SYS-0003`
- Status: `implemented`
- Primary feature: `FEAT-0032`
- Owner spec: `docs/systems/horizon-loop.md`
- Feature count: `6`

## Role

Horizon Loop owns recurring and longer-running autonomy: Goal Packets, one Work
Pulse, Daily/Weekly Interval reports, low-supply refill, backoff, PR watching,
and the bounded handoff from Feed Scout, Dogfood, Interval, and operator
sources.

## Feature Docs

- [FEAT-0029 Retired Goal Packet architecture](../features/FEAT-0029-goal-packet-architecture-for-native-codex-goals.md)
- [FEAT-0032 Goal Advisor execution loop](../features/FEAT-0032-goal-advisor-execution-compilation.md)
- [FEAT-0065 Pulse and interval automation](../features/FEAT-0065-pulse-and-interval-automation.md)
- [FEAT-0066 Product-scoped Pulse loops](../features/FEAT-0066-product-scoped-pulse-loops.md)
- [FEAT-0067 Daily interval review reports](../features/FEAT-0067-daily-interval-review-reports.md)
- [FEAT-0071 Project Work Pulse](../features/FEAT-0071-project-work-pulse.md)

## What Belongs Here

Goal-backed continuation, Pulse dispatch/check-ins, report-first Interval
review/admission, low-supply refill, adaptive waits, and visible automation
cadence.

## What Belongs Elsewhere

Single-ticket execution belongs in Work Loop; external source discovery belongs
in Source And Sidecar Systems; experiment selection belongs in Self-Improvement
And Learning; proof standards belong in Proof And Review.

## Operating Contract

- Recurring loops must have visible prompts, reports, tickets, or automations as state owners.
- Automations may no-op when no safe valuable action exists.
- Exactly one base project automation is a heartbeat: Work Pulse. Other
  recurring jobs are bounded cron/manual automations.
- Daily and Weekly Interval write reports before ticket deltas, may admit
  grounded interventions or decision-changing investigations, and otherwise
  leave findings as source gaps or refill context.
- Work Pulse dispatches executable tickets and calls Plan Next Wave only when
  ready supply is low. Plan Next Wave ranks configured skill calls from stable
  problems, areas, metric movement, source-backed context, and ticket history.
- Backoff and polling stay tracked and bounded.
- Human authority remains required for ambiguous or high-risk direction.
- Feature-level behavior belongs in `docs/features/FEAT-*.md`; this page owns the system boundary and feature grouping.
- Registry data is generated from system and feature docs, not edited by hand.
- When a capability no longer deserves a feature page, fold its current truth into the best owner and remove active refs.

## System Flow

```mermaid
flowchart LR
  classDef keep fill:#f3f4f6,stroke:#6b7280,color:#111827
  classDef changed fill:#fef3c7,stroke:#b45309,color:#111827
  classDef added fill:#dcfce7,stroke:#15803d,color:#111827
  classDef retired fill:#fee2e2,stroke:#b91c1c,color:#7f1d1d,stroke-dasharray: 5 3

  metrics["metric observations<br/>raw + movement"]:::keep
  intent["stable intent<br/>problems + areas + metrics"]:::keep
  automations["automations<br/>farplane/automations.toml"]:::keep
  advisor["FEAT-0032<br/>goal-advisor"]:::changed
  pulse["FEAT-0071<br/>project Work Pulse"]:::added
  interval["FEAT-0067<br/>Daily / Weekly review"]:::changed
  sources["Feed Scout + Dogfood + operator<br/>reports + context"]:::keep
  old["FEAT-0065<br/>retired umbrella automation"]:::retired
  productPulse["FEAT-0066<br/>retired product-scoped Pulse"]:::retired
  planner["Plan Next Wave<br/>low-supply refill"]:::added
  board["ticket board<br/>priority + due_at + proof"]:::added
  outputs["reports + tickets<br/>bounded next work"]:::added

  metrics --> interval --> outputs --> board
  intent --> interval
  intent --> planner
  automations --> pulse --> board
  automations --> interval
  sources --> planner --> board --> pulse
  board --> advisor --> outputs
  old -. "superseded_by" .-> pulse
  old -. "superseded_by" .-> interval
  productPulse -. "superseded_by" .-> pulse
```

The Horizon Loop coordinates one execution heartbeat, one report-first
Interval review path, and one low-supply refill planner without giving every
source its own strategy ledger or executor.

## Surfaces

- `docs/features/FEAT-0029-goal-packet-architecture-for-native-codex-goals.md`
- `docs/features/FEAT-0065-pulse-and-interval-automation.md`
- `docs/features/FEAT-0066-product-scoped-pulse-loops.md`
- `docs/features/FEAT-0067-daily-interval-review-reports.md`
- `docs/features/FEAT-0071-project-work-pulse.md`

## Proof And Maintenance

- Registry proof: `python3 docs/features/validate_features.py`.
- Link proof: `python3 bin/validators/check_doc_refs.py`.
- Update this system page when product-layer boundaries or feature membership changes.
- Update feature pages when capability behavior changes.
- Regenerate registries and commit generated outputs with the source docs.

## Change History

- 2026-06-27: Migrated into the reader-first system-spec shape.
- 2026-07-07: Made Goal Advisor the primary Horizon feature and added
  experimental product-scoped Pulse plus daily interval report handles.
- 2026-07-10: Retired product-scoped Pulse and added one project Work Pulse.
- 2026-07-11: Limited heartbeat ownership to Work Pulse and added bounded
  scheduled BAU/source/experiment ticket sources.
- 2026-07-12: Centralized exploratory ticket admission in the adaptive Work
  Pulse planner while preserving bounded evidence-backed recovery admission in
  scheduled jobs.
- 2026-07-25: Consolidated the metric-to-ticket loop: Interval owns
  report-first evidence admission, Work Pulse owns dispatch and due_at
  ordering, and Plan Next Wave owns only low-supply refill.
