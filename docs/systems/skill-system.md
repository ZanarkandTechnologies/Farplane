---
title: "Skill System"
status: active
owner: farplane-framework
created_at: 2026-06-26
updated_at: 2026-06-26
tags:
  - farplane
  - systems
  - skill-system
refs:
  - docs/skills/README.md
  - docs/skills/system.md
  - docs/skills/templates/SKILL_TEMPLATE.md
  - skills/skill-maintenance/SKILL.md
system_record_json: |
  {
    "id": "SYS-0006",
    "name": "Skill System",
    "status": "implemented",
    "summary": "The reusable expertise layer: skill tiers, packaging, templates, evals, QA checklists, registry intelligence, and maintenance constraints.",
    "owner_spec": "docs/systems/skill-system.md",
    "primary_feature_ref": "FEAT-0022",
    "feature_refs": [
      "FEAT-0022",
      "FEAT-0030",
      "FEAT-0054",
      "FEAT-0057",
      "FEAT-0064"
    ],
    "refs": [
      "docs/skills/README.md",
      "docs/skills/system.md",
      "docs/skills/templates/SKILL_TEMPLATE.md",
      "skills/skill-maintenance/SKILL.md"
    ],
    "last_verified": "2026-06-26"
  }
---

# Skill System

The reusable expertise layer: skill tiers, packaging, templates, evals, QA checklists, registry intelligence, and maintenance constraints.

## Role

Skill System is the reusable expertise layer: skill packaging, templates, eval/checklist surfaces, plugin distribution, and improvement prioritization.

## What Belongs Here

Skill frontmatter, skill templates, skill-local eval and QA docs, plugin packaging, template intelligence, and skill improvement signals.

## What Belongs Elsewhere

Project runtime hooks belong to Invocation Runtime; broad system proof belongs to Proof and Review; domain-specific skill behavior belongs to Domain Skill Families.

## Feature Docs

- [FEAT-0022 Skill tier leverage classes](../features/FEAT-0022-skill-tier-leverage-classes.md)
- [FEAT-0030 On-demand skill plugin packaging](../features/FEAT-0030-on-demand-skill-plugin-packaging.md)
- [FEAT-0054 Modular skill-local eval tasks](../features/FEAT-0054-modular-skill-local-eval-tasks.md)
- [FEAT-0057 Skill-local QA checklist artifacts](../features/FEAT-0057-skill-local-qa-checklist-artifacts.md)
- [FEAT-0064 Skill compounding score](../features/FEAT-0064-skill-compounding-score.md)

## Maintenance

This system page owns only the system-level contract. Feature registry rows are authored as feature pages in `docs/features/` and generated into `docs/features/registry.jsonl`.
