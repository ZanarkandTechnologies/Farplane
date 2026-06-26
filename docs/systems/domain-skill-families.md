---
title: "Domain Skill Families"
status: active
owner: farplane-framework
created_at: 2026-06-26
updated_at: 2026-06-26
tags:
  - farplane
  - systems
  - domain-skill-families
refs:
  - skills/frontend-craft/SKILL.md
  - skills/frontend-design/SKILL.md
  - skills/visual-design/SKILL.md
  - skills/delegate-frontend/SKILL.md
system_record_json: |
  {
    "id": "SYS-0010",
    "name": "Domain Skill Families",
    "status": "implemented",
    "summary": "The specialized skill families for frontend, media, content, and future vertical workflows that build on the core Work Loop and Skill System.",
    "owner_spec": "docs/systems/domain-skill-families.md",
    "primary_feature_ref": "FEAT-0014",
    "feature_refs": [
      "FEAT-0014"
    ],
    "refs": [
      "skills/frontend-craft/SKILL.md",
      "skills/frontend-design/SKILL.md",
      "skills/visual-design/SKILL.md",
      "skills/delegate-frontend/SKILL.md"
    ],
    "last_verified": "2026-06-26"
  }
capability_records_json: |
  [
    {
      "id": "FEAT-0014",
      "name": "Frontend skill parity upgrade",
      "status": "implemented",
      "category": "frontend-skills",
      "surfaces": [
        "skills/frontend-craft",
        "skills/frontend-design",
        "skills/visual-design",
        "skills/delegate-frontend",
        "skills/visual-qa",
        "skills/landing-page"
      ],
      "source_refs": [
        "experiments/harness-scout/runs/2026-05-09-frontend-skill-parity",
        "docs/MEMORY.md#MEM-0085"
      ],
      "external_refs": [
        "https://github.com/nextlevelbuilder/ui-ux-pro-max-skill/tree/main/.claude/skills",
        "https://github.com/Leonxlnx/taste-skill/blob/main/skills/taste-skill/SKILL.md",
        "https://ui.shadcn.com/docs/mcp",
        "https://ui.shadcn.com/docs/cli",
        "https://ui.shadcn.com/docs/components-json",
        "https://ui.shadcn.com/r/registries.json"
      ],
      "evidence_refs": [
        "experiments/harness-scout/runs/2026-05-09-frontend-skill-parity/implementation.md",
        "experiments/harness-scout/runs/2026-05-09-frontend-skill-parity/post-implementation-review.md",
        "docs/HISTORY.md"
      ],
      "known_limits": "Docs/skill-contract upgrade only; no automated eval suite or searchable frontend rule corpus yet.",
      "metrics": [
        "frontend_skill_prebuild_completeness_rate",
        "generic_ui_regression_rate"
      ],
      "last_verified": "2026-05-11",
      "capability_role": "primary",
      "public": true
    }
  ]
---

# Domain Skill Families

The specialized skill families for frontend, media, content, and future vertical workflows that build on the core Work Loop and Skill System.

## Role

This system spec is the authored source for one public Farplane system and its internal capability handles. The generated registries expose the same data as `docs/systems/registry.jsonl` and `docs/features/registry.jsonl`.

## Public Capability

- `FEAT-0014` - Frontend skill parity upgrade

## Capability Handles

- `FEAT-0014` `primary` - Frontend skill parity upgrade

## Maintenance Notes

- Edit the `system_record_json` and `capability_records_json` blocks in this file, then run `python3 docs/features/validate_features.py --write`.
- Keep public docs focused on the system and primary capability; use subcapability rows for compatibility, dedupe, rollout, and evidence tracking.
