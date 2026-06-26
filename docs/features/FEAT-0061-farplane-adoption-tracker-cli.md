---
title: "Farplane adoption tracker CLI"
status: implemented
owner: feature-registry
created_at: 2026-06-26
updated_at: 2026-06-26
tags:
  - farplane
  - feature
  - sys-0009
refs:
  - bin/farplane.py#adoption scan
  - bin/core/farplane_adoption.py
  - bin/tests/test_farplane_adoption.py
  - docs/features/registry.jsonl
  - experiments/decisions/2026-06-24-project-harness-rollout-feature/decision.md
  - tickets/TASK-0216/ticket.md
feature_record_json: |
  {
    "id": "FEAT-0061",
    "name": "Farplane adoption tracker CLI",
    "status": "implemented",
    "system_id": "SYS-0009",
    "category": "proof",
    "public": true,
    "surfaces": [
      "bin/farplane.py#adoption scan",
      "bin/core/farplane_adoption.py",
      "bin/tests/test_farplane_adoption.py",
      "docs/features/registry.jsonl"
    ],
    "source_refs": [
      "experiments/decisions/2026-06-24-project-harness-rollout-feature/decision.md",
      "tickets/TASK-0216/ticket.md"
    ],
    "external_refs": [],
    "evidence_refs": [
      "bin/tests/test_farplane_adoption.py"
    ],
    "known_limits": "Local CLI resolver only. It reads explicit project roots, roots files, or known ~/.farplane state files; it does not crawl the whole computer, mutate project manifests, or render Office UI directly.",
    "metrics": [
      "farplane_adoption_scan_pass",
      "feature_adoption_drift_count"
    ],
    "last_verified": "2026-06-24"
  }
---

# Farplane adoption tracker CLI

Farplane adoption tracker CLI is a first-class Farplane feature in [Maintenance And Release OS](../systems/maintenance-release-os.md). It survives as a `FEAT-*` handle because it has owner surfaces, evidence, limits, and a maintenance path.

```text
feature(FEAT-0061, repo_state?) -> behavior + evidence + maintenance_signal
```

## System

- System: [Maintenance And Release OS](../systems/maintenance-release-os.md)
- Feature ID: `FEAT-0061`
- Status: `implemented`
- Category: `proof`

## Owned Behavior

This feature owns the behavior implemented, specified, or enforced by its owner surfaces. Keep the details in those surfaces; keep this page focused on the stable feature contract and registry metadata.

## Owner Surfaces

- `bin/farplane.py#adoption scan`
- `bin/core/farplane_adoption.py`
- `bin/tests/test_farplane_adoption.py`
- `docs/features/registry.jsonl`

## Source Context

- `experiments/decisions/2026-06-24-project-harness-rollout-feature/decision.md`
- `tickets/TASK-0216/ticket.md`

## Evidence

- `bin/tests/test_farplane_adoption.py`

## Known Limits

Local CLI resolver only. It reads explicit project roots, roots files, or known ~/.farplane state files; it does not crawl the whole computer, mutate project manifests, or render Office UI directly.

## Metrics

- `farplane_adoption_scan_pass`
- `feature_adoption_drift_count`

## Maintenance

Update this feature doc before regenerating `docs/features/registry.jsonl`. If the feature stops deserving its own doc, delete this file and remove all active template, source, ticket, and system refs to `FEAT-0061`.
