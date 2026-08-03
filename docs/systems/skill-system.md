---
title: "Skill System"
status: active
owner: farplane-framework
created_at: 2026-06-26
updated_at: 2026-08-03
tags:
  - farplane
  - systems
  - skill-system
refs:
  - docs/skills/README.md
  - docs/skills/advisors.md
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
      "FEAT-0057",
      "FEAT-0062",
      "FEAT-0064"
    ],
    "refs": [
      "docs/skills/README.md",
      "docs/skills/advisors.md",
      "docs/skills/system.md",
      "docs/skills/templates/SKILL_TEMPLATE.md",
      "skills/skill-maintenance/SKILL.md"
    ],
    "last_verified": "2026-08-03"
  }
---
# Skill System

The reusable expertise layer: skill tiers, packaging, templates, evals, QA checklists,
registry intelligence, and maintenance constraints. This page is the product-layer owner
for that subsystem: it explains what belongs here, which feature specs make up the
stack, and where adjacent responsibilities should move.

```text
skill_system(change, repo_state?) -> owned_feature_set + boundary_decision + maintenance_signal
```

## At A Glance

- System ID: `SYS-0006`
- Status: `implemented`
- Primary feature: `FEAT-0022`
- Owner spec: `docs/systems/skill-system.md`
- Feature count: `5`

## Role

Skill System owns reusable expertise: skill packages, tiering, templates, local evals,
QA checklists, registry intelligence, and maintenance constraints. It lets Farplane add
capability without bloating the agent kernel.

The [Advisor System Index](../skills/advisors.md) is the human discovery view
for the cross-cutting advisor family inside this system. It does not create a
second registry or a separate formal subsystem: advisor package metadata stays
canonical in each skill and in the generated skill registry.

## Feature Docs

- [FEAT-0022 Skill tier leverage classes](../features/FEAT-0022-skill-tier-leverage-classes.md)
- [FEAT-0030 On-demand skill plugin packaging](../features/FEAT-0030-on-demand-skill-plugin-packaging.md)
- [FEAT-0057 Skill-local QA checklist artifacts](../features/FEAT-0057-skill-local-qa-checklist-artifacts.md)
- [FEAT-0062 Capped skill surface budget](../features/FEAT-0062-capped-skill-surface-budget.md)
- [FEAT-0064 Skill signals](../features/FEAT-0064-skill-signals.md)

## What Belongs Here

Skill authoring, tier/leverage classification, plugin packaging, QA checklists,
capped skill-surface budgets, skill signals, and skill registry maintenance.

## What Belongs Elsewhere

Always-loaded behavior belongs in Agent Kernel; task execution belongs in Work Loop;
domain-specific product workflows may live in Domain Skill Families.

## Operating Contract

- Skills are callable mini harnesses with clear inputs, outputs, and proof expectations.
- Detailed workflows stay skill-local where possible.
- Skill metadata, todo links, evals, and QA checklists remain validator-friendly.
- Installed copies are not the source of truth for repo-owned skills.
- Feature-level behavior belongs in `docs/features/FEAT-*.md`; this page owns the system boundary and feature grouping.
- Registry data is generated from system and feature docs, not edited by hand.
- When a capability no longer deserves a feature page, fold its current truth into the best owner and remove active refs.

## System Flow

```mermaid
flowchart LR
  classDef keep fill:#f3f4f6,stroke:#6b7280,color:#111827
  classDef changed fill:#fef3c7,stroke:#b45309,color:#111827
  classDef added fill:#dcfce7,stroke:#15803d,color:#111827
  classDef retired fill:#fee2e2,stroke:#b91c1c,color:#7f1d1d,stroke-dasharray: 5 3

  skill["skills/*/SKILL.md<br/>frontmatter + Todo List"]:::keep
  templates["skill templates<br/>qa_checklist + eval_task"]:::keep
  system["SYS-0006 Skill System<br/>tiers, packaging, budgets"]:::changed
  maintenance["skill-maintenance<br/>registry + graph checks"]:::changed
  registry["docs/skills/registry.jsonl<br/>template intelligence"]:::added
  features["FEAT-0022 / 0030 / 0057 / 0062 / 0064"]:::keep

  skill --> system
  templates --> system
  features --> system
  system --> maintenance --> registry
```

The Skill System owns reusable workflow packaging, tier semantics, QA sidecars, budgets, and generated skill intelligence.

## Surfaces

- `docs/skills/README.md`
- `docs/skills/advisors.md`
- `docs/skills/system.md`
- `docs/skills/templates/SKILL_TEMPLATE.md`
- `skills/skill-maintenance/SKILL.md`

## Proof And Maintenance

- Registry proof: `python3 docs/features/validate_features.py`.
- Link proof: `python3 bin/validators/check_doc_refs.py`.
- Update this system page when product-layer boundaries or feature membership changes.
- Update feature pages when capability behavior changes.
- Regenerate registries and commit generated outputs with the source docs.

## Change History

- 2026-08-03: Added the grouped Advisor System index as a human discovery
  surface backed by the generated skill registry.
- 2026-06-28: Added capped skill surface budget as a Skill System feature.
- 2026-06-27: Migrated into the reader-first system-spec shape.
- 2026-07-07: Moved skill-local eval task feature ownership into consolidated
  Farplane evals under Proof And Review.
