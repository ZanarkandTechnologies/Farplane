---
title: "Source And Sidecar Systems"
status: active
owner: farplane-framework
created_at: 2026-06-26
updated_at: 2026-06-26
tags:
  - farplane
  - systems
  - source-and-sidecar-systems
refs:
  - docs/sources/registry.jsonl
  - skills/harness-scout/SKILL.md
  - skills/feed-scout/SKILL.md
  - docs/specs/inspiration-vault.md
system_record_json: |
  {
    "id": "SYS-0008",
    "name": "Source And Sidecar Systems",
    "status": "implemented",
    "summary": "The external-source, inspiration, video-to-skill, and sidecar-product surfaces that let Farplane adapt useful patterns without making them live dependencies.",
    "owner_spec": "docs/systems/source-sidecar-systems.md",
    "primary_feature_ref": "FEAT-0011",
    "feature_refs": [
      "FEAT-0011",
      "FEAT-0025"
    ],
    "refs": [
      "docs/sources/registry.jsonl",
      "skills/harness-scout/SKILL.md",
      "skills/feed-scout/SKILL.md",
      "docs/specs/inspiration-vault.md"
    ],
    "last_verified": "2026-06-26"
  }
---

# Source And Sidecar Systems

The external-source, inspiration, video-to-skill, and sidecar-product surfaces that let Farplane adapt useful patterns without making them live dependencies.

## Role

Source and Sidecar Systems ingest outside evidence and adjacent product ideas without making external sources or sidecars live dependencies.

## What Belongs Here

Source registry, harness scouting, video-to-skill reconstruction, and sidecar/draft product grounding surfaces.

## What Belongs Elsewhere

Accepted core behavior moves to the owning system; raw research and bulky media stay in experiments or ticket artifacts.

## Feature Docs

- [FEAT-0011 Harness scout source ingestion](../features/FEAT-0011-harness-scout-source-ingestion.md)
- [FEAT-0025 Video-to-skill source reconstruction](../features/FEAT-0025-video-to-skill-source-reconstruction.md)

## Maintenance

This system page owns only the system-level contract. Feature registry rows are authored as feature pages in `docs/features/` and generated into `docs/features/registry.jsonl`.
