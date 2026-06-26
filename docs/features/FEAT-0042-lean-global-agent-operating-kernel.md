---
title: "Lean global agent operating kernel"
status: implemented
owner: feature-registry
created_at: 2026-06-26
updated_at: 2026-06-26
tags:
  - farplane
  - feature
  - sys-0001
refs:
  - templates/global/AGENTS.md
  - skills/init-advisor/references/AGENTS_TEMPLATE.md
  - ARCHITECTURE.md
  - docs/fundamentals/harness-engineering-doctrine.md
  - docs/HISTORY.md
feature_record_json: |
  {
    "id": "FEAT-0042",
    "name": "Lean global agent operating kernel",
    "status": "implemented",
    "system_id": "SYS-0001",
    "category": "context-routing",
    "public": true,
    "surfaces": [
      "templates/global/AGENTS.md",
      "skills/init-advisor/references/AGENTS_TEMPLATE.md",
      "ARCHITECTURE.md"
    ],
    "source_refs": [
      "docs/fundamentals/harness-engineering-doctrine.md",
      "docs/HISTORY.md"
    ],
    "external_refs": [],
    "evidence_refs": [
      "templates/global/AGENTS.md",
      "skills/init-advisor/references/AGENTS_TEMPLATE.md",
      "docs/HISTORY.md"
    ],
    "known_limits": "The global template now owns only every-turn behavior; project-specific coding defaults and detailed workflows must keep living in project AGENTS files, skills, tickets, docs, validators, or subagent prompts.",
    "metrics": [],
    "last_verified": "2026-06-07"
  }
---

# Lean global agent operating kernel

Lean global agent operating kernel is a first-class Farplane feature in [Agent Kernel](../systems/agent-kernel.md). It survives as a `FEAT-*` handle because it has owner surfaces, evidence, limits, and a maintenance path.

```text
feature(FEAT-0042, repo_state?) -> behavior + evidence + maintenance_signal
```

## System

- System: [Agent Kernel](../systems/agent-kernel.md)
- Feature ID: `FEAT-0042`
- Status: `implemented`
- Category: `context-routing`

## Owned Behavior

This feature owns the behavior implemented, specified, or enforced by its owner surfaces. Keep the details in those surfaces; keep this page focused on the stable feature contract and registry metadata.

## Owner Surfaces

- `templates/global/AGENTS.md`
- `skills/init-advisor/references/AGENTS_TEMPLATE.md`
- `ARCHITECTURE.md`

## Source Context

- `docs/fundamentals/harness-engineering-doctrine.md`
- `docs/HISTORY.md`

## Evidence

- `templates/global/AGENTS.md`
- `skills/init-advisor/references/AGENTS_TEMPLATE.md`
- `docs/HISTORY.md`

## Known Limits

The global template now owns only every-turn behavior; project-specific coding defaults and detailed workflows must keep living in project AGENTS files, skills, tickets, docs, validators, or subagent prompts.

## Metrics

- no dedicated metric yet

## Maintenance

Update this feature doc before regenerating `docs/features/registry.jsonl`. If the feature stops deserving its own doc, delete this file and remove all active template, source, ticket, and system refs to `FEAT-0042`.
