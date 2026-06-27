---
title: Skill tier leverage classes
status: implemented
owner: feature-registry
created_at: 2026-06-26
updated_at: 2026-06-26
tags:
  - farplane
  - feature
  - sys-0006
refs:
  - templates/global/AGENTS.md
  - docs/skills/system.md
  - skills/plan
  - skills/reference-grounding
  - skills/prototyping
  - skills/research
  - skills/review
  - docs/review/rubrics
  - docs/skills/README.md
  - bin/validators/sync_skill_registry.py
  - bin/validators/check_skill_todo_tiers.py
  - bin/validators/check_tier0_phase_protocol.py
feature_id: FEAT-0022
system_id: SYS-0006
category: skills
public: true
surfaces:
  - templates/global/AGENTS.md
  - docs/skills/system.md
  - skills/plan
  - skills/reference-grounding
  - skills/prototyping
  - skills/research
  - skills/review
  - docs/review/rubrics
  - docs/skills/README.md
  - bin/validators/sync_skill_registry.py
  - bin/validators/check_skill_todo_tiers.py
  - bin/validators/check_tier0_phase_protocol.py
source_refs:
  - "docs/MEMORY.md#MEM-0098"
  - docs/features/README.md
external_refs: []
evidence_refs:
  - docs/HISTORY.md
known_limits: Depends on skill maintainers keeping Markdown links accurate; numeric tiers describe compound upgrade priority while first-load todo links enforce loading boundaries; Tier 0 is a universal phase protocol rather than a skill tier, plan is a planning prompt-template rather than the phase itself, execute remains a deprecated compatibility wrapper, and concrete coding skills such as spec-to-ticket, impl-plan, goal-advisor, and close-ticket must not be treated as universal generic workflows.
metrics: []
last_verified: 2026-06-23
---
# Skill tier leverage classes

Skill tier leverage classes is a first-class Farplane feature in [Skill System](../systems/skill-system.md). It survives as a `FEAT-*` handle because it has owner surfaces, evidence, limits, and a maintenance path.

```text
feature(FEAT-0022, repo_state?) -> behavior + evidence + maintenance_signal
```

## System

- System: [Skill System](../systems/skill-system.md)
- Feature ID: `FEAT-0022`
- Status: `implemented`
- Category: `skills`

## Owned Behavior

This feature owns the behavior implemented, specified, or enforced by its owner surfaces. Keep the details in those surfaces; keep this page focused on the stable feature contract and registry metadata.

## Owner Surfaces

- `templates/global/AGENTS.md`
- `docs/skills/system.md`
- `skills/plan`
- `skills/reference-grounding`
- `skills/prototyping`
- `skills/research`
- `skills/review`
- `docs/review/rubrics`
- `docs/skills/README.md`
- `bin/validators/sync_skill_registry.py`
- `bin/validators/check_skill_todo_tiers.py`
- `bin/validators/check_tier0_phase_protocol.py`

## Source Context

- `docs/MEMORY.md#MEM-0098`
- `docs/features/README.md`

## Evidence

- `docs/HISTORY.md`

## Known Limits

Depends on skill maintainers keeping Markdown links accurate; numeric tiers describe compound upgrade priority while first-load todo links enforce loading boundaries; Tier 0 is a universal phase protocol rather than a skill tier, plan is a planning prompt-template rather than the phase itself, execute remains a deprecated compatibility wrapper, and concrete coding skills such as spec-to-ticket, impl-plan, goal-advisor, and close-ticket must not be treated as universal generic workflows.

## Metrics

- no dedicated metric yet

## Maintenance

Update this feature doc before regenerating `docs/features/registry.jsonl`. If the feature stops deserving its own doc, delete this file and remove all active template, source, ticket, and system refs to `FEAT-0022`.
