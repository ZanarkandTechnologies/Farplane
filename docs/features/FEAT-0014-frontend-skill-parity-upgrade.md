---
title: Frontend skill parity upgrade
status: implemented
owner: feature-registry
created_at: 2026-06-26
updated_at: 2026-06-26
tags:
  - farplane
  - feature
  - sys-0010
refs:
  - skills/frontend-craft
  - skills/frontend-design
  - skills/visual-design
  - skills/delegate-frontend
  - skills/visual-qa
  - skills/landing-page
  - experiments/harness-scout/runs/2026-05-09-frontend-skill-parity
  - "docs/MEMORY.md#MEM-0085"
  - experiments/harness-scout/runs/2026-05-09-frontend-skill-parity/implementation.md
  - experiments/harness-scout/runs/2026-05-09-frontend-skill-parity/post-implementation-review.md
  - docs/HISTORY.md
feature_id: FEAT-0014
system_id: SYS-0010
category: frontend-skills
public: true
surfaces:
  - skills/frontend-craft
  - skills/frontend-design
  - skills/visual-design
  - skills/delegate-frontend
  - skills/visual-qa
  - skills/landing-page
source_refs:
  - experiments/harness-scout/runs/2026-05-09-frontend-skill-parity
  - "docs/MEMORY.md#MEM-0085"
external_refs:
  - https://github.com/nextlevelbuilder/ui-ux-pro-max-skill/tree/main/.claude/skills
  - https://github.com/Leonxlnx/taste-skill/blob/main/skills/taste-skill/SKILL.md
  - https://ui.shadcn.com/docs/mcp
  - https://ui.shadcn.com/docs/cli
  - https://ui.shadcn.com/docs/components-json
  - https://ui.shadcn.com/r/registries.json
evidence_refs:
  - experiments/harness-scout/runs/2026-05-09-frontend-skill-parity/implementation.md
  - experiments/harness-scout/runs/2026-05-09-frontend-skill-parity/post-implementation-review.md
  - docs/HISTORY.md
known_limits: Docs/skill-contract upgrade only; no automated eval suite or searchable frontend rule corpus yet.
metrics:
  - frontend_skill_prebuild_completeness_rate
  - generic_ui_regression_rate
last_verified: 2026-05-11
---
# Frontend skill parity upgrade

Frontend skill parity upgrade is a first-class Farplane feature in [Domain Skill Families](../systems/domain-skill-families.md). It survives as a `FEAT-*` handle because it has owner surfaces, evidence, limits, and a maintenance path.

```text
feature(FEAT-0014, repo_state?) -> behavior + evidence + maintenance_signal
```

## System

- System: [Domain Skill Families](../systems/domain-skill-families.md)
- Feature ID: `FEAT-0014`
- Status: `implemented`
- Category: `frontend-skills`

## Owned Behavior

This feature owns the behavior implemented, specified, or enforced by its owner surfaces. Keep the details in those surfaces; keep this page focused on the stable feature contract and registry metadata.

## Owner Surfaces

- `skills/frontend-craft`
- `skills/frontend-design`
- `skills/visual-design`
- `skills/delegate-frontend`
- `skills/visual-qa`
- `skills/landing-page`

## Source Context

- `experiments/harness-scout/runs/2026-05-09-frontend-skill-parity`
- `docs/MEMORY.md#MEM-0085`

## Evidence

- `experiments/harness-scout/runs/2026-05-09-frontend-skill-parity/implementation.md`
- `experiments/harness-scout/runs/2026-05-09-frontend-skill-parity/post-implementation-review.md`
- `docs/HISTORY.md`

## Known Limits

Docs/skill-contract upgrade only; no automated eval suite or searchable frontend rule corpus yet.

## Metrics

- `frontend_skill_prebuild_completeness_rate`
- `generic_ui_regression_rate`

## Maintenance

Update this feature doc before regenerating `docs/features/registry.jsonl`. If the feature stops deserving its own doc, delete this file and remove all active template, source, ticket, and system refs to `FEAT-0014`.
