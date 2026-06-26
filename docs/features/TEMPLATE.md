---
title: "Feature Name"
status: draft
owner: feature-registry
created_at: YYYY-MM-DD
updated_at: YYYY-MM-DD
tags:
  - farplane
  - feature
refs: []
feature_record_json: |
  {
    "id": "FEAT-####",
    "name": "Feature Name",
    "status": "designed",
    "system_id": "SYS-####",
    "category": "category",
    "public": true,
    "surfaces": [],
    "source_refs": [],
    "external_refs": [],
    "evidence_refs": [],
    "known_limits": "What this feature deliberately does not claim yet.",
    "metrics": [],
    "last_verified": "YYYY-MM-DD"
  }
---

# Feature Name

This feature is a first-class Farplane capability. Keep it only if it deserves its own behavior contract, proof path, and maintenance owner.

```text
feature(FEAT-####, repo_state?) -> behavior + evidence + maintenance_signal
```

## System

- System: [System Name](../systems/README.md)
- Feature ID: `FEAT-####`
- Status: `designed`
- Category: `category`

## What It Does

State the behavior this feature owns in concrete terms.

## Owner Surfaces

- `path/to/owner`

## Evidence

- `path/to/proof`

## Metrics

- `metric_name` when a real metric exists

## Maintenance

If this no longer deserves its own file, delete this doc and remove the feature from templates, sources, and generated registry output.
