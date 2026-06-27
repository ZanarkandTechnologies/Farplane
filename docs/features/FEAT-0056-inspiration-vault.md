---
title: "Inspiration Vault"
status: proposed
owner: feature-registry
created_at: 2026-06-27
updated_at: 2026-06-27
tags:
  - farplane
  - feature
  - sys-0008
refs:
  - docs/systems/source-sidecar-systems.md
  - skills/ingest-content/SKILL.md
  - skills/media-ingest/SKILL.md
  - skills/harness-scout/SKILL.md
feature_record_json: |
  {
    "id": "FEAT-0056",
    "name": "Inspiration Vault",
    "status": "proposed",
    "system_id": "SYS-0008",
    "category": "source-ingestion",
    "public": true,
    "surfaces": [
      "docs/systems/source-sidecar-systems.md",
      "skills/ingest-content/SKILL.md",
      "skills/media-ingest/SKILL.md",
      "skills/harness-scout/SKILL.md"
    ],
    "source_refs": [
      "docs/systems/source-sidecar-systems.md"
    ],
    "external_refs": [],
    "evidence_refs": [],
    "known_limits": "Proposed product surface. It needs a dedicated implementation ticket and proof path before it can be marked implemented.",
    "metrics": [
      "inspiration_recall_quality",
      "creative_grounding_reuse"
    ],
    "last_verified": "2026-06-27"
  }
---

# Inspiration Vault

Inspiration Vault is a proposed first-class Farplane feature in [Source And Sidecar Systems](../systems/source-sidecar-systems.md). It survived the purge because it already had enough product shape to deserve a feature spec rather than a stray idea file.

```text
inspiration_vault(source_item, project_context) -> searchable_inspiration + grounding_candidate
```

## System

- System: [Source And Sidecar Systems](../systems/source-sidecar-systems.md)
- Feature ID: `FEAT-0056`
- Status: `proposed`
- Category: `source-ingestion`

## Feature Spec

Intent: capture liked links, images, videos, UI examples, product patterns, and operator notes into a searchable inspiration bank that can later ground creative or product work.

Placement decision:

- Source ingestion belongs in the sidecar/source system until an item becomes accepted Farplane behavior.
- Raw inspiration is not a feature by itself. The feature is the reusable capture, retrieval, and grounding loop.
- Accepted insights can promote into source records, feature specs, skills, evals, or tickets.

Data contract:

- source URL or local file reference;
- media type and capture method;
- title, author/source, timestamps, and representative thumbnail/frame when available;
- extracted transcript, caption, or notes when available;
- tags, project relevance, and reusable pattern notes;
- privacy/sensitivity flag;
- promoted targets such as source registry row, ticket, skill, or feature spec.

UI requirements:

- browse by project, source type, tag, recency, and promoted status;
- search and recall examples for a given product or creative task;
- inspect representative media without opening raw private clutter;
- promote one item into a ticket, source record, skill note, or content artifact.

Grounding engine role:

- Use the vault to make creative/product claims concrete.
- Prefer representative examples over vague taste memory.
- Keep inspiration as evidence, not as automatic policy.

Non-goals:

- Not a generic bookmarking app.
- Not a replacement for source registry decisions.
- Not a place to store secrets, private transcripts, or unredacted user data.

Proof path:

- capture a small mixed-media sample;
- retrieve it for a later Farplane product/design/content task;
- show that the retrieved item changed or grounded the output;
- promote only durable conclusions to the owning source, feature, skill, or ticket surface.

## Owner Surfaces

- `docs/systems/source-sidecar-systems.md`
- `skills/ingest-content/SKILL.md`
- `skills/media-ingest/SKILL.md`
- `skills/harness-scout/SKILL.md`

## Source Context

- `docs/systems/source-sidecar-systems.md`

## Evidence

- no implementation evidence yet

## Known Limits

Proposed product surface. It needs a dedicated implementation ticket and proof path before it can be marked implemented.

## Metrics

- `inspiration_recall_quality`
- `creative_grounding_reuse`

## Maintenance

Update this feature doc before regenerating `docs/features/registry.jsonl`. If the feature stops deserving its own doc, delete this file and remove all active template, source, ticket, and system refs to `FEAT-0056`.
