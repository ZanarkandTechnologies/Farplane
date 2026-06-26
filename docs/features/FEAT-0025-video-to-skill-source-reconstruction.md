---
title: "Video-to-skill source reconstruction"
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
  - skills/media-ingest
  - skills/video-understanding
  - SRC-0008
  - tickets/archive/TASK-0158/ticket.md
  - experiments/harness-scout/runs/2026-05-20-instagram-claude-portal-video/media-ingest-bundle.md
  - experiments/harness-scout/runs/2026-05-20-instagram-claude-portal-video/video-reconstruction-brief.md
  - experiments/harness-scout/runs/2026-05-20-instagram-claude-portal-video/video-understanding-smoke-log.md
  - docs/HISTORY.md
feature_record_json: |
  {
    "id": "FEAT-0025",
    "name": "Video-to-skill source reconstruction",
    "status": "implemented",
    "system_id": "SYS-0008",
    "category": "source-ingestion",
    "public": true,
    "surfaces": [
      "skills/harness-scout",
      "skills/media-ingest",
      "skills/video-understanding"
    ],
    "source_refs": [
      "SRC-0008",
      "tickets/archive/TASK-0158/ticket.md"
    ],
    "external_refs": [
      "https://www.instagram.com/p/DYijhcetmBP/"
    ],
    "evidence_refs": [
      "experiments/harness-scout/runs/2026-05-20-instagram-claude-portal-video/media-ingest-bundle.md",
      "experiments/harness-scout/runs/2026-05-20-instagram-claude-portal-video/video-reconstruction-brief.md",
      "experiments/harness-scout/runs/2026-05-20-instagram-claude-portal-video/video-understanding-smoke-log.md",
      "docs/HISTORY.md"
    ],
    "known_limits": "Support-skill and artifact contract only; platform fetching still depends on available local tools, public access, or user-provided exports, and transcript gaps must be recorded rather than hidden.",
    "metrics": [
      "video_to_skill_pipeline_validation_passed"
    ],
    "last_verified": "2026-05-21"
  }
---

# Video-to-skill source reconstruction

Video-to-skill source reconstruction is a first-class Farplane feature in [Source And Sidecar Systems](../systems/source-sidecar-systems.md). It survives as a `FEAT-*` handle because it has owner surfaces, evidence, limits, and a maintenance path.

```text
feature(FEAT-0025, repo_state?) -> behavior + evidence + maintenance_signal
```

## System

- System: [Source And Sidecar Systems](../systems/source-sidecar-systems.md)
- Feature ID: `FEAT-0025`
- Status: `implemented`
- Category: `source-ingestion`

## Owned Behavior

This feature owns the behavior implemented, specified, or enforced by its owner surfaces. Keep the details in those surfaces; keep this page focused on the stable feature contract and registry metadata.

## Owner Surfaces

- `skills/harness-scout`
- `skills/media-ingest`
- `skills/video-understanding`

## Source Context

- `SRC-0008`
- `tickets/archive/TASK-0158/ticket.md`

## Evidence

- `experiments/harness-scout/runs/2026-05-20-instagram-claude-portal-video/media-ingest-bundle.md`
- `experiments/harness-scout/runs/2026-05-20-instagram-claude-portal-video/video-reconstruction-brief.md`
- `experiments/harness-scout/runs/2026-05-20-instagram-claude-portal-video/video-understanding-smoke-log.md`
- `docs/HISTORY.md`

## Known Limits

Support-skill and artifact contract only; platform fetching still depends on available local tools, public access, or user-provided exports, and transcript gaps must be recorded rather than hidden.

## Metrics

- `video_to_skill_pipeline_validation_passed`

## Maintenance

Update this feature doc before regenerating `docs/features/registry.jsonl`. If the feature stops deserving its own doc, delete this file and remove all active template, source, ticket, and system refs to `FEAT-0025`.
