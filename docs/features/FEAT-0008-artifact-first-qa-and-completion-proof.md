---
title: "Artifact-first QA and completion proof"
status: implemented
owner: feature-registry
created_at: 2026-06-26
updated_at: 2026-06-26
tags:
  - farplane
  - feature
  - sys-0005
refs:
  - tickets/README.md
  - tickets/templates/ticket.md
  - skills/qa
  - skills/review
  - docs/specs/review-gates.md
  - docs/MEMORY.md#MEM-0048
  - docs/MEMORY.md#MEM-0064
  - docs/MEMORY.md#MEM-0148
  - docs/HISTORY.md
feature_record_json: |
  {
    "id": "FEAT-0008",
    "name": "Artifact-first QA and completion proof",
    "status": "implemented",
    "system_id": "SYS-0005",
    "category": "proof",
    "public": true,
    "surfaces": [
      "tickets/README.md",
      "tickets/templates/ticket.md",
      "skills/qa",
      "skills/review",
      "docs/specs/review-gates.md"
    ],
    "source_refs": [
      "docs/MEMORY.md#MEM-0048",
      "docs/MEMORY.md#MEM-0064",
      "docs/MEMORY.md#MEM-0148"
    ],
    "external_refs": [],
    "evidence_refs": [
      "docs/HISTORY.md"
    ],
    "known_limits": "Depends on compact `Done / Proof` obligations plus linked artifacts, progress logs, and reviewer gates, not ticket-body proof theater.",
    "metrics": [],
    "last_verified": "2026-06-12"
  }
---

# Artifact-first QA and completion proof

Artifact-first QA and completion proof is a first-class Farplane feature in [Proof And Review](../systems/proof-review.md). It survives as a `FEAT-*` handle because it has owner surfaces, evidence, limits, and a maintenance path.

```text
feature(FEAT-0008, repo_state?) -> behavior + evidence + maintenance_signal
```

## System

- System: [Proof And Review](../systems/proof-review.md)
- Feature ID: `FEAT-0008`
- Status: `implemented`
- Category: `proof`

## Owned Behavior

This feature owns the behavior implemented, specified, or enforced by its owner surfaces. Keep the details in those surfaces; keep this page focused on the stable feature contract and registry metadata.

## Owner Surfaces

- `tickets/README.md`
- `tickets/templates/ticket.md`
- `skills/qa`
- `skills/review`
- `docs/specs/review-gates.md`

## Source Context

- `docs/MEMORY.md#MEM-0048`
- `docs/MEMORY.md#MEM-0064`
- `docs/MEMORY.md#MEM-0148`

## Evidence

- `docs/HISTORY.md`

## Known Limits

Depends on compact `Done / Proof` obligations plus linked artifacts, progress logs, and reviewer gates, not ticket-body proof theater.

## Metrics

- no dedicated metric yet

## Maintenance

Update this feature doc before regenerating `docs/features/registry.jsonl`. If the feature stops deserving its own doc, delete this file and remove all active template, source, ticket, and system refs to `FEAT-0008`.
