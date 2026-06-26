---
title: "Harness scout source ingestion"
status: implemented
owner: feature-registry
created_at: 2026-06-26
updated_at: 2026-06-26
tags:
  - farplane
  - feature
  - sys-0008
refs:
  - skills/harness-scout
  - docs/features/registry.jsonl
  - experiments/harness-scout
  - docs/HISTORY.md
  - experiments/harness-scout/runs/2026-05-04-self-evolving-agents
feature_record_json: |
  {
    "id": "FEAT-0011",
    "name": "Harness scout source ingestion",
    "status": "implemented",
    "system_id": "SYS-0008",
    "category": "source-ingestion",
    "public": true,
    "surfaces": [
      "skills/harness-scout",
      "docs/features/registry.jsonl",
      "experiments/harness-scout"
    ],
    "source_refs": [
      "docs/HISTORY.md"
    ],
    "external_refs": [
      "https://www.youtube.com/watch?v=2zhchG0r6iI"
    ],
    "evidence_refs": [
      "experiments/harness-scout/runs/2026-05-04-self-evolving-agents",
      "docs/HISTORY.md"
    ],
    "known_limits": "Manual scorecard and dedupe workflow only; no cron polling, OpenClaw integration, or async Codex benchmark runner.",
    "metrics": [
      "decision_matrix_quality",
      "manual_variant_score_1_to_10"
    ],
    "last_verified": "2026-05-04"
  }
---

# Harness scout source ingestion

Harness scout source ingestion is a first-class Farplane feature in [Source And Sidecar Systems](../systems/source-sidecar-systems.md). It survives as a `FEAT-*` handle because it has owner surfaces, evidence, limits, and a maintenance path.

```text
feature(FEAT-0011, repo_state?) -> behavior + evidence + maintenance_signal
```

## System

- System: [Source And Sidecar Systems](../systems/source-sidecar-systems.md)
- Feature ID: `FEAT-0011`
- Status: `implemented`
- Category: `source-ingestion`

## Owned Behavior

This feature owns the behavior implemented, specified, or enforced by its owner surfaces. Keep the details in those surfaces; keep this page focused on the stable feature contract and registry metadata.

## Owner Surfaces

- `skills/harness-scout`
- `docs/features/registry.jsonl`
- `experiments/harness-scout`

## Source Context

- `docs/HISTORY.md`

## Evidence

- `experiments/harness-scout/runs/2026-05-04-self-evolving-agents`
- `docs/HISTORY.md`

## Known Limits

Manual scorecard and dedupe workflow only; no cron polling, OpenClaw integration, or async Codex benchmark runner.

## Metrics

- `decision_matrix_quality`
- `manual_variant_score_1_to_10`

## Maintenance

Update this feature doc before regenerating `docs/features/registry.jsonl`. If the feature stops deserving its own doc, delete this file and remove all active template, source, ticket, and system refs to `FEAT-0011`.
