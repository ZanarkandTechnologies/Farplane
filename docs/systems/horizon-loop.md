---
title: "Horizon Loop"
status: active
owner: farplane-framework
created_at: 2026-06-26
updated_at: 2026-07-12
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
    "summary": "The project control loop with one Work Pulse heartbeat and bounded scheduled report/candidate sources for BAU, scouting, and self-improvement.",
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
    "last_verified": "2026-07-12"
  }
---
# Horizon Loop

The project control loop that coordinates Goal Packets, one Work Pulse
heartbeat, and bounded scheduled report/candidate sources without becoming a hidden
daemon.

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
Pulse, scheduled BAU reports, backoff, PR watching, and the shared candidate
handoff from Feed Scout, Dogfood, Interval, and operator sources.

## Feature Docs

- [FEAT-0029 Retired Goal Packet architecture](../features/FEAT-0029-goal-packet-architecture-for-native-codex-goals.md)
- [FEAT-0032 Goal Advisor execution loop](../features/FEAT-0032-goal-advisor-execution-compilation.md)
- [FEAT-0065 Pulse and interval automation](../features/FEAT-0065-pulse-and-interval-automation.md)
- [FEAT-0066 Product-scoped Pulse loops](../features/FEAT-0066-product-scoped-pulse-loops.md)
- [FEAT-0067 Daily interval review reports](../features/FEAT-0067-daily-interval-review-reports.md)
- [FEAT-0071 Project Work Pulse](../features/FEAT-0071-project-work-pulse.md)

## What Belongs Here

Goal-backed continuation, Pulse admission/dispatch/check-ins, BAU interval
reports, horizon recalibration, adaptive waits, and visible automation cadence.

## What Belongs Elsewhere

Single-ticket execution belongs in Work Loop; external source discovery belongs
in Source And Sidecar Systems; experiment selection belongs in Self-Improvement
And Learning; proof standards belong in Proof And Review.

## Operating Contract

- Recurring loops must have visible prompts, reports, tickets, or automations as state owners.
- Automations may no-op when no safe valuable action exists.
- Exactly one base project automation is a heartbeat: Work Pulse. Other
  recurring jobs are bounded cron/manual automations.
- Scheduled sources write reports and bounded candidates, and may admit direct
  recovery tickets for evidenced existing failures with known fixes and no
  experiment debt. The adaptive Work Pulse planner globally ranks proactive
  opportunities, uncertain fixes, and experiments.
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

  goals["program / goals / tickets"]:::keep
  automations["automations<br/>farplane/automations.toml"]:::keep
  advisor["FEAT-0032<br/>goal-advisor"]:::changed
  pulse["FEAT-0071<br/>project Work Pulse"]:::added
  interval["FEAT-0067<br/>Daily / Weekly BAU reports"]:::changed
  sources["Feed Scout + Dogfood + Interval + operator<br/>reports + candidates"]:::keep
  old["FEAT-0065<br/>retired umbrella automation"]:::retired
  productPulse["FEAT-0066<br/>retired product-scoped Pulse"]:::retired
  planner["adaptive project planner<br/>global rank + admission"]:::added
  outputs["tickets + reports<br/>bounded next work"]:::added

  goals --> advisor --> outputs
  automations --> pulse --> outputs
  automations --> interval --> outputs
  sources --> planner --> outputs --> pulse
  old -. "superseded_by" .-> pulse
  old -. "superseded_by" .-> interval
  productPulse -. "superseded_by" .-> pulse
```

The Horizon Loop coordinates one execution heartbeat and several report-backed
candidate sources without giving each source its own admission policy or executor.

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
