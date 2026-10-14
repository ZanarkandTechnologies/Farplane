---
title: "Horizon Loop"
status: active
owner: farplane-framework
created_at: 2026-06-26
updated_at: 2026-10-14
tags:
  - farplane
  - systems
  - horizon-loop
refs:
  - docs/features/FEAT-0032-goal-advisor-execution-compilation.md
  - docs/features/FEAT-0067-daily-interval-review-reports.md
  - docs/farplane-framework/pulse-and-interval-loop.md
system_record_json: |
  {
    "id": "SYS-0003",
    "name": "Horizon Loop",
    "status": "implemented",
    "summary": "The project control loop where Company OS Daily and Weekly maintain money-linked project memory over work state held in GitHub Issues.",
    "owner_spec": "docs/systems/horizon-loop.md",
    "primary_feature_ref": "FEAT-0032",
    "feature_refs": [
      "FEAT-0032",
      "FEAT-0067"
    ],
    "refs": [
      "docs/features/FEAT-0032-goal-advisor-execution-compilation.md",
      "docs/features/FEAT-0067-daily-interval-review-reports.md",
      "docs/farplane-framework/pulse-and-interval-loop.md"
    ],
    "last_verified": "2026-10-12"
  }
---
# Horizon Loop

The project control loop where Company OS Daily and Weekly maintain
source-grounded project memory around money movement, constraints, decisions,
and next commitments. Work state lives in GitHub Issues; Work Pulse and its
low-supply refill planner were retired in #41 when `pulse-update` and
`plan-next-wave` were deleted. The former Interval weekly-draft and broad
promotion route is legacy reference only.

```text
horizon_loop(change, repo_state?) -> owned_feature_set + boundary_decision + maintenance_signal
```

## At A Glance

- System ID: `SYS-0003`
- Status: `implemented`
- Primary feature: `FEAT-0032`
- Owner spec: `docs/systems/horizon-loop.md`
- Feature count: `2`

## Role

Horizon Loop owns recurring and longer-running autonomy: Goal Packets, Company
OS Daily/Weekly project memory and reports, backoff, PR watching, and bounded
handoffs from Feed Scout and the operator.

## Feature Docs

- [FEAT-0032 Goal Advisor execution loop](../features/FEAT-0032-goal-advisor-execution-compilation.md)
- [FEAT-0067 Daily interval review reports](../features/FEAT-0067-daily-interval-review-reports.md)

## What Belongs Here

Goal-backed continuation, Company OS review and project memory, adaptive
waits, and visible automation cadence.

## What Belongs Elsewhere

Single-ticket execution belongs in Work Loop; external source discovery belongs
in Source And Sidecar Systems; experiment selection belongs in Self-Improvement
And Learning; proof standards belong in Proof And Review.

## Operating Contract

- Recurring loops must have visible prompts, reports, tickets, or automations as state owners.
- Automations may no-op when no safe valuable action exists.
- No project heartbeat runs; recurring jobs are bounded cron/manual
  automations, and GitHub Issues hold work state.
- Daily maintains one source-grounded memory result per eligible Project.
  Weekly reviews the complete frozen Project set and carries forward supported
  commitments. Both may update only authorized existing issues and neither
  admits work, invents strategy, promotes broad knowledge, or executes work.
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
  automations["automation config<br/>root + project-local"]:::keep
  advisor["FEAT-0032<br/>goal-advisor"]:::changed
  pulse["Work Pulse<br/>retired 2026-10-12, #41"]:::retired
  companyos["FEAT-0067<br/>Company OS Daily + Weekly"]:::changed
  memory["project memory + reports<br/>money movement + commitments"]:::added
  sources["Feed Scout + operator<br/>reports + context"]:::keep
  board["GitHub Issues<br/>priority + proof"]:::added
  outputs["reports + tickets<br/>bounded next work"]:::added

  metrics --> companyos --> memory --> outputs
  intent --> companyos
  automations --> companyos
  sources --> board
  board --> advisor --> outputs
  pulse -. "retired #41" .-> board
```

The Horizon Loop coordinates one Company OS memory and review path over
GitHub Issues without giving every source its own strategy ledger or executor.

## Surfaces

- `docs/features/FEAT-0032-goal-advisor-execution-compilation.md`
- `docs/features/FEAT-0067-daily-interval-review-reports.md`
- `docs/farplane-framework/pulse-and-interval-loop.md`

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
- 2026-08-20: Made Interval the parent reporting-and-knowledge workflow with
  Daily incremental owner updates and Weekly receipt consolidation/showcase.
- 2026-08-20: Replaced eager Daily owner updates with a weekly working draft
  and Weekly selective promotion.
- 2026-10-12: Retired Work Pulse (FEAT-0071) and its refill planner in #41
  when `pulse-update` and `plan-next-wave` were deleted; GitHub Issues hold
  work state.
- 2026-10-14: Deleted the retired Goal Packet architecture, Pulse umbrella,
  product-scoped Pulse and Work Pulse feature pages; Goal Advisor and Company
  OS Daily/Weekly are the remaining features.
