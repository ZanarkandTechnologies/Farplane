---
title: "Skill-local QA checklist artifacts"
status: implemented
owner: feature-registry
created_at: 2026-06-26
updated_at: 2026-06-26
tags:
  - farplane
  - feature
  - sys-0006
refs:
  - skills/skill-maintenance/qa_checklist.md
  - skills/skill-maintenance
  - skills/skill-creator
  - docs/skills/system.md
  - docs/skills/best-practices.md
  - docs/skills/README.md
  - docs/MEMORY.md#MEM-0150
  - docs/fundamentals/harness-algebra.md
  - skills/skill-maintenance/audits/2026-06-23-qa-checklist-preflight-review.md
feature_record_json: |
  {
    "id": "FEAT-0057",
    "name": "Skill-local QA checklist artifacts",
    "status": "implemented",
    "system_id": "SYS-0006",
    "category": "skills",
    "public": true,
    "surfaces": [
      "skills/skill-maintenance/qa_checklist.md",
      "skills/skill-maintenance",
      "skills/skill-creator",
      "docs/skills/system.md",
      "docs/skills/best-practices.md",
      "docs/skills/README.md"
    ],
    "source_refs": [
      "docs/MEMORY.md#MEM-0150",
      "docs/fundamentals/harness-algebra.md"
    ],
    "external_refs": [],
    "evidence_refs": [
      "skills/skill-maintenance/qa_checklist.md",
      "skills/skill-maintenance/audits/2026-06-23-qa-checklist-preflight-review.md"
    ],
    "known_limits": "Markdown artifact standard only; no dedicated qacheck runner, renderer, or subagent fanout script exists yet. Agents now read skill-local checklists as preflight guardrails, apply them again at finish, and route independent reviewer lanes for material checklist conformance through skill-maintenance, skill-creator, and recorded audit/proof notes.",
    "metrics": [
      "skill_qa_checklist_application_pass"
    ],
    "last_verified": "2026-06-23"
  }
---

# Skill-local QA checklist artifacts

Skill-local QA checklist artifacts is a first-class Farplane feature in [Skill System](../systems/skill-system.md). It survives as a `FEAT-*` handle because it has owner surfaces, evidence, limits, and a maintenance path.

```text
feature(FEAT-0057, repo_state?) -> behavior + evidence + maintenance_signal
```

## System

- System: [Skill System](../systems/skill-system.md)
- Feature ID: `FEAT-0057`
- Status: `implemented`
- Category: `skills`

## Owned Behavior

This feature owns the behavior implemented, specified, or enforced by its owner surfaces. Keep the details in those surfaces; keep this page focused on the stable feature contract and registry metadata.

## Owner Surfaces

- `skills/skill-maintenance/qa_checklist.md`
- `skills/skill-maintenance`
- `skills/skill-creator`
- `docs/skills/system.md`
- `docs/skills/best-practices.md`
- `docs/skills/README.md`

## Source Context

- `docs/MEMORY.md#MEM-0150`
- `docs/fundamentals/harness-algebra.md`

## Evidence

- `skills/skill-maintenance/qa_checklist.md`
- `skills/skill-maintenance/audits/2026-06-23-qa-checklist-preflight-review.md`

## Known Limits

Markdown artifact standard only; no dedicated qacheck runner, renderer, or subagent fanout script exists yet. Agents now read skill-local checklists as preflight guardrails, apply them again at finish, and route independent reviewer lanes for material checklist conformance through skill-maintenance, skill-creator, and recorded audit/proof notes.

## Metrics

- `skill_qa_checklist_application_pass`

## Maintenance

Update this feature doc before regenerating `docs/features/registry.jsonl`. If the feature stops deserving its own doc, delete this file and remove all active template, source, ticket, and system refs to `FEAT-0057`.
