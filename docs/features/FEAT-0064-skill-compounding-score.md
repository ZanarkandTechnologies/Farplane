---
title: "Skill compounding score"
status: implemented
owner: feature-registry
created_at: 2026-06-26
updated_at: 2026-06-26
tags:
  - farplane
  - feature
  - sys-0006
refs:
  - docs/specs/skill-compounding-score.md
  - docs/skills/system.md
  - skills/taste-loop
  - farplane/automations.md
  - docs/skills/registry.jsonl
  - docs/farplane-framework/lifecycle.md
  - farplane/products.md
  - skills/skill-maintenance/graph/README.md
  - skills/taste-loop/SKILL.md
  - skills/taste-loop/templates/heartbeat-prompt.md
  - skills/taste-loop/eval_task.json
feature_record_json: |
  {
    "id": "FEAT-0064",
    "name": "Skill compounding score",
    "status": "implemented",
    "system_id": "SYS-0006",
    "category": "skills",
    "public": true,
    "surfaces": [
      "docs/specs/skill-compounding-score.md",
      "docs/skills/system.md",
      "skills/taste-loop",
      "farplane/automations.md",
      "docs/skills/registry.jsonl"
    ],
    "source_refs": [
      "docs/farplane-framework/lifecycle.md",
      "docs/skills/system.md",
      "farplane/products.md",
      "skills/skill-maintenance/graph/README.md"
    ],
    "external_refs": [],
    "evidence_refs": [
      "skills/taste-loop/SKILL.md",
      "skills/taste-loop/templates/heartbeat-prompt.md",
      "skills/taste-loop/eval_task.json"
    ],
    "known_limits": "Official ranking contract only; the current implementation is prompt-consumed by Taste Loop and generated graph data. No standalone scorer, UI renderer, hidden scheduler, or automatic skill mutation is shipped.",
    "metrics": [
      "skill_compounding_score_traceability_pass",
      "taste_loop_score_breakdown_pass",
      "skill_registry_validation_pass"
    ],
    "last_verified": "2026-06-26"
  }
---

# Skill compounding score

Skill compounding score is a first-class Farplane feature in [Skill System](../systems/skill-system.md). It survives as a `FEAT-*` handle because it has owner surfaces, evidence, limits, and a maintenance path.

```text
feature(FEAT-0064, repo_state?) -> behavior + evidence + maintenance_signal
```

## System

- System: [Skill System](../systems/skill-system.md)
- Feature ID: `FEAT-0064`
- Status: `implemented`
- Category: `skills`

## Owned Behavior

This feature owns the behavior implemented, specified, or enforced by its owner surfaces. Keep the details in those surfaces; keep this page focused on the stable feature contract and registry metadata.

## Owner Surfaces

- `docs/specs/skill-compounding-score.md`
- `docs/skills/system.md`
- `skills/taste-loop`
- `farplane/automations.md`
- `docs/skills/registry.jsonl`

## Source Context

- `docs/farplane-framework/lifecycle.md`
- `docs/skills/system.md`
- `farplane/products.md`
- `skills/skill-maintenance/graph/README.md`

## Evidence

- `skills/taste-loop/SKILL.md`
- `skills/taste-loop/templates/heartbeat-prompt.md`
- `skills/taste-loop/eval_task.json`

## Known Limits

Official ranking contract only; the current implementation is prompt-consumed by Taste Loop and generated graph data. No standalone scorer, UI renderer, hidden scheduler, or automatic skill mutation is shipped.

## Metrics

- `skill_compounding_score_traceability_pass`
- `taste_loop_score_breakdown_pass`
- `skill_registry_validation_pass`

## Maintenance

Update this feature doc before regenerating `docs/features/registry.jsonl`. If the feature stops deserving its own doc, delete this file and remove all active template, source, ticket, and system refs to `FEAT-0064`.
