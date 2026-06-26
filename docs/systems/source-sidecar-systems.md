---
title: "Source And Sidecar Systems"
status: active
owner: farplane-framework
created_at: 2026-06-26
updated_at: 2026-06-26
tags:
  - farplane
  - systems
  - source-sidecar-systems
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
      "FEAT-0025",
      "FEAT-0035",
      "FEAT-0056"
    ],
    "refs": [
      "docs/sources/registry.jsonl",
      "skills/harness-scout/SKILL.md",
      "skills/feed-scout/SKILL.md",
      "docs/specs/inspiration-vault.md"
    ],
    "last_verified": "2026-06-26"
  }
capability_records_json: |
  [
    {
      "id": "FEAT-0011",
      "name": "Harness scout source ingestion",
      "status": "implemented",
      "category": "source-ingestion",
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
      "last_verified": "2026-05-04",
      "capability_role": "primary",
      "public": true
    },
    {
      "id": "FEAT-0025",
      "name": "Video-to-skill source reconstruction",
      "status": "implemented",
      "category": "source-ingestion",
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
      "last_verified": "2026-05-21",
      "capability_role": "subcapability",
      "public": false
    },
    {
      "id": "FEAT-0035",
      "name": "Entity-linked harness resource tracking",
      "status": "partial",
      "category": "source-ingestion",
      "surfaces": [
        "skills/feed-scout/references/data-model.md",
        "skills/feed-scout/templates/codex-automation-prompt.md"
      ],
      "source_refs": [
        "SRC-0011",
        "SRC-0012",
        "docs/HISTORY.md"
      ],
      "external_refs": [
        "https://github.com/openclaw/agent-skills",
        "https://x.com/steipete"
      ],
      "evidence_refs": [
        "skills/feed-scout/references/data-model.md",
        "skills/feed-scout/templates/codex-automation-prompt.md",
        "docs/HISTORY.md"
      ],
      "known_limits": "Model and seed config only; no dedicated validator script, GitHub polling helper, X API/Apify boundary, or content ledger integration is shipped yet.",
      "metrics": [],
      "last_verified": "2026-05-27",
      "capability_role": "subcapability",
      "public": false
    },
    {
      "id": "FEAT-0056",
      "name": "Inspiration vault grounding surface",
      "status": "proposed",
      "category": "source-ingestion",
      "surfaces": [
        "skills/ingest-content",
        "docs/specs/inspiration-vault.md"
      ],
      "source_refs": [
        "docs/specs/inspiration-vault.md",
        "skills/ingest-content/SKILL.md"
      ],
      "external_refs": [],
      "evidence_refs": [
        "skills/ingest-content/audits/2026-06-12-create-ingest-content.md"
      ],
      "known_limits": "Proposed feature and skill contract only; Farplane UI browsing/graph/recall, retrieval ranking, and autonomous content metric loops are not implemented yet.",
      "metrics": [
        "inspiration_capture_verification_pass",
        "inspiration_retrieval_relevance"
      ],
      "last_verified": "2026-06-12",
      "capability_role": "subcapability",
      "public": false
    }
  ]
---

# Source And Sidecar Systems

The external-source, inspiration, video-to-skill, and sidecar-product surfaces that let Farplane adapt useful patterns without making them live dependencies.

## Role

This system spec is the authored source for one public Farplane system and its internal capability handles. The generated registries expose the same data as `docs/systems/registry.jsonl` and `docs/features/registry.jsonl`.

## Public Capability

- `FEAT-0011` - Harness scout source ingestion

## Capability Handles

- `FEAT-0011` `primary` - Harness scout source ingestion
- `FEAT-0025` `subcapability` - Video-to-skill source reconstruction
- `FEAT-0035` `subcapability` - Entity-linked harness resource tracking
- `FEAT-0056` `subcapability` - Inspiration vault grounding surface

## Maintenance Notes

- Edit the `system_record_json` and `capability_records_json` blocks in this file, then run `python3 docs/features/validate_features.py --write`.
- Keep public docs focused on the system and primary capability; use subcapability rows for compatibility, dedupe, rollout, and evidence tracking.
