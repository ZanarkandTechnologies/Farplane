---
title: "Horizon Loop"
status: active
owner: farplane-framework
created_at: 2026-06-26
updated_at: 2026-06-26
tags:
  - farplane
  - systems
  - horizon-loop
refs:
  - docs/specs/goal-loop-contract.md
  - docs/specs/minimal-autonomy-loop.md
  - docs/specs/steer-pulse-automation.md
  - docs/specs/nested-pm-projects.md
system_record_json: |
  {
    "id": "SYS-0003",
    "name": "Horizon Loop",
    "status": "implemented",
    "summary": "The longer-running project loop that coordinates goals, Goal Packets, Pulse, Interval, backoff, PR watching, feedback, and horizon-level ticket supply.",
    "owner_spec": "docs/systems/horizon-loop.md",
    "primary_feature_ref": "FEAT-0029",
    "feature_refs": [
      "FEAT-0029",
      "FEAT-0032"
    ],
    "refs": [
      "docs/specs/goal-loop-contract.md",
      "docs/specs/minimal-autonomy-loop.md",
      "docs/specs/steer-pulse-automation.md",
      "docs/specs/nested-pm-projects.md"
    ],
    "last_verified": "2026-06-26"
  }
---

# Horizon Loop

The longer-running project loop that coordinates goals, Goal Packets, Pulse, Interval, backoff, PR watching, feedback, and horizon-level ticket supply.

## Role

Horizon Loop is the long-running coordination layer: Goal Packets, pulse/interval cadence, feedback loops, and multi-window execution memory.

## What Belongs Here

Goal architecture, heartbeat execution, drift checks, backoff, PR watch loops, and longer-horizon planning.

## What Belongs Elsewhere

Single-ticket build contracts stay in Work Loop; validators and release registries stay in Maintenance OS.

## Feature Docs

- [FEAT-0029 Goal Packet architecture for native Codex goals](../features/FEAT-0029-goal-packet-architecture-for-native-codex-goals.md)
- [FEAT-0032 Goal Advisor execution compilation](../features/FEAT-0032-goal-advisor-execution-compilation.md)

## Maintenance

This system page owns only the system-level contract. Feature registry rows are authored as feature pages in `docs/features/` and generated into `docs/features/registry.jsonl`.
