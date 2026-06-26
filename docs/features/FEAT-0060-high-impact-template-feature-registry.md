---
title: "High-impact template feature registry"
status: implemented
owner: feature-registry
created_at: 2026-06-26
updated_at: 2026-06-26
tags:
  - farplane
  - feature
  - sys-0009
refs:
  - docs/templates/registry.jsonl
  - docs/templates/README.md
  - rules/template-registry.toml
  - rules/template-version-watch.toml
  - bin/validators/sync_template_registry.py
  - templates/global/AGENTS.md
  - docs/skills/templates/SKILL_TEMPLATE.md
  - docs/skills/templates/METHOD_REFERENCE_TEMPLATE.md
  - tickets/templates/ticket.md
  - tickets/templates/goal-loop/program.md
  - skills/harness-creator/templates/project-harness.md
  - docs/features/registry.jsonl
feature_record_json: |
  {
    "id": "FEAT-0060",
    "name": "High-impact template feature registry",
    "status": "implemented",
    "system_id": "SYS-0009",
    "category": "context-routing",
    "public": true,
    "surfaces": [
      "docs/templates/registry.jsonl",
      "docs/templates/README.md",
      "rules/template-registry.toml",
      "rules/template-version-watch.toml",
      "bin/validators/sync_template_registry.py",
      "templates/global/AGENTS.md",
      "docs/skills/templates/SKILL_TEMPLATE.md",
      "docs/skills/templates/METHOD_REFERENCE_TEMPLATE.md",
      "tickets/templates/ticket.md",
      "tickets/templates/goal-loop/program.md",
      "skills/harness-creator/templates/project-harness.md"
    ],
    "source_refs": [
      "docs/features/registry.jsonl",
      "rules/template-registry.toml"
    ],
    "external_refs": [],
    "evidence_refs": [
      "bin/validators/test_sync_template_registry.py"
    ],
    "known_limits": "Tracks high-impact prompt-shaped templates and the docs-owned skill/method template standards. Broader documentation versioning and low-impact scaffold templates are intentionally deferred until they have a clear consumer.",
    "metrics": [
      "template_feature_registry_validation_pass"
    ],
    "last_verified": "2026-06-24"
  }
---

# High-impact template feature registry

High-impact template feature registry is a first-class Farplane feature in [Maintenance And Release OS](../systems/maintenance-release-os.md). It survives as a `FEAT-*` handle because it has owner surfaces, evidence, limits, and a maintenance path.

```text
feature(FEAT-0060, repo_state?) -> behavior + evidence + maintenance_signal
```

## System

- System: [Maintenance And Release OS](../systems/maintenance-release-os.md)
- Feature ID: `FEAT-0060`
- Status: `implemented`
- Category: `context-routing`

## Owned Behavior

This feature owns the behavior implemented, specified, or enforced by its owner surfaces. Keep the details in those surfaces; keep this page focused on the stable feature contract and registry metadata.

## Owner Surfaces

- `docs/templates/registry.jsonl`
- `docs/templates/README.md`
- `rules/template-registry.toml`
- `rules/template-version-watch.toml`
- `bin/validators/sync_template_registry.py`
- `templates/global/AGENTS.md`
- `docs/skills/templates/SKILL_TEMPLATE.md`
- `docs/skills/templates/METHOD_REFERENCE_TEMPLATE.md`
- `tickets/templates/ticket.md`
- `tickets/templates/goal-loop/program.md`
- `skills/harness-creator/templates/project-harness.md`

## Source Context

- `docs/features/registry.jsonl`
- `rules/template-registry.toml`

## Evidence

- `bin/validators/test_sync_template_registry.py`

## Known Limits

Tracks high-impact prompt-shaped templates and the docs-owned skill/method template standards. Broader documentation versioning and low-impact scaffold templates are intentionally deferred until they have a clear consumer.

## Metrics

- `template_feature_registry_validation_pass`

## Maintenance

Update this feature doc before regenerating `docs/features/registry.jsonl`. If the feature stops deserving its own doc, delete this file and remove all active template, source, ticket, and system refs to `FEAT-0060`.
