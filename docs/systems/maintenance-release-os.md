---
title: "Maintenance And Release OS"
status: active
owner: farplane-framework
created_at: 2026-06-26
updated_at: 2026-06-27
tags:
  - farplane
  - systems
  - maintenance-and-release-os
refs:
  - docs/features/FEAT-0060-registry-backed-documentation-os.md
  - docs/farplane-framework/harness-maintenance.md
  - docs/templates/registry.jsonl
system_record_json: |
  {
    "id": "SYS-0009",
    "name": "Maintenance And Release OS",
    "status": "implemented",
    "summary": "The registries, lifecycle rules, manifests, rollout checks, adoption scans, and docs validators that keep Farplane coherent as it evolves.",
    "owner_spec": "docs/systems/maintenance-release-os.md",
    "primary_feature_ref": "FEAT-0060",
    "feature_refs": [
      "FEAT-0060",
      "FEAT-0061"
    ],
    "refs": [
      "docs/features/FEAT-0060-registry-backed-documentation-os.md",
      "docs/farplane-framework/harness-maintenance.md",
      "docs/templates/registry.jsonl"
    ],
    "last_verified": "2026-06-27"
  }
---

# Maintenance And Release OS

The registries, lifecycle rules, manifests, rollout checks, adoption scans, and docs validators that keep Farplane coherent as it evolves.

## Role

Maintenance and Release OS keeps Farplane coherent as it changes: registries, templates, manifests, adoption checks, generated docs, and reference validation.

## What Belongs Here

Generated inventories, template rollout, project manifests, adoption scan, filesystem lifecycle, doc reference checks, and release hygiene.

## What Belongs Elsewhere

Feature behavior belongs to the feature doc; system narrative belongs to docs/systems; one-off proof stays with tickets.

## Feature Docs

- [FEAT-0060 Registry-backed documentation OS](../features/FEAT-0060-registry-backed-documentation-os.md)
- [FEAT-0061 Farplane adoption tracker CLI](../features/FEAT-0061-farplane-adoption-tracker-cli.md)

## Maintenance

This system page owns only the system-level contract. Feature registry rows are authored as feature pages in `docs/features/` and generated into `docs/features/registry.jsonl`.
