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
---

# Domain Skill Families

The specialized skill families for frontend, media, content, and future vertical workflows that build on the core Work Loop and Skill System.

## Role

Domain Skill Families are specialized workflow products that sit on top of the core loops, starting with frontend/media/content-style work.

## What Belongs Here

Vertical skill families, domain-specific orchestration, specialized QA, and future workflow products that reuse core Farplane loops.

## What Belongs Elsewhere

Shared skill mechanics belong to Skill System; generic execution and proof stay in Work Loop and Proof and Review.

## Feature Docs

- [FEAT-0014 Frontend skill parity upgrade](../features/FEAT-0014-frontend-skill-parity-upgrade.md)

## Maintenance

This system page owns only the system-level contract. Feature registry rows are authored as feature pages in `docs/features/` and generated into `docs/features/registry.jsonl`.
