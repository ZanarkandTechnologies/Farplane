---
title: "Invocation Runtime"
status: active
owner: farplane-framework
created_at: 2026-06-26
updated_at: 2026-06-26
tags:
  - farplane
  - systems
  - invocation-runtime
refs:
  - docs/specs/invocation-and-adapters.md
  - skills/farplane-invocation/SKILL.md
  - bin/farplane_invocation.py
system_record_json: |
  {
    "id": "SYS-0004",
    "name": "Invocation Runtime",
    "status": "implemented",
    "summary": "The explicit invocation, board adapter, compute selector, and external-runner boundary that keep Farplane an invocation/proof layer rather than a hidden daemon.",
    "owner_spec": "docs/systems/invocation-runtime.md",
    "primary_feature_ref": "FEAT-0015",
    "feature_refs": [
      "FEAT-0015"
    ],
    "refs": [
      "docs/specs/invocation-and-adapters.md",
      "skills/farplane-invocation/SKILL.md",
      "bin/farplane_invocation.py"
    ],
    "last_verified": "2026-06-26"
  }
---

# Invocation Runtime

The explicit invocation, board adapter, compute selector, and external-runner boundary that keep Farplane an invocation/proof layer rather than a hidden daemon.

## Role

Invocation Runtime defines how Farplane is called, what work item adapters produce, and where compute selection stops before becoming a hidden scheduler.

## What Belongs Here

Explicit invocation, board adapter shape, compute selector boundaries, and local/external runner contracts.

## What Belongs Elsewhere

Business cadence belongs to Horizon Loop; proof gates belong to Proof and Review; UI payload rendering belongs to Maintenance OS when generated.

## Feature Docs

- [FEAT-0015 Symphony-compatible Farplane invocation contract](../features/FEAT-0015-symphony-compatible-farplane-invocation-contract.md)

## Maintenance

This system page owns only the system-level contract. Feature registry rows are authored as feature pages in `docs/features/` and generated into `docs/features/registry.jsonl`.
