---
title: Modular skill-local eval tasks
status: implemented
owner: feature-registry
created_at: 2026-06-26
updated_at: 2026-06-26
tags:
  - farplane
  - feature
  - sys-0006
refs:
  - skills/eval/scripts/run_evals.py
  - skills/eval/SKILL.md
  - skills/eval/eval_task.json
  - docs/skills/templates/SKILL_TEMPLATE.md
  - docs/skills/system.md
  - docs/skills/best-practices.md
  - "docs/MEMORY.md#MEM-0145"
  - docs/HISTORY.md
  - skills/eval/tests/test_run_evals.py
feature_id: FEAT-0054
system_id: SYS-0006
category: skills
public: true
surfaces:
  - skills/eval/scripts/run_evals.py
  - skills/eval/SKILL.md
  - skills/eval/eval_task.json
  - docs/skills/templates/SKILL_TEMPLATE.md
  - docs/skills/system.md
  - docs/skills/best-practices.md
source_refs:
  - "docs/MEMORY.md#MEM-0145"
  - docs/HISTORY.md
external_refs: []
evidence_refs:
  - skills/eval/eval_task.json
  - skills/eval/tests/test_run_evals.py
  - docs/HISTORY.md
known_limits: The runner discovers `skills/*/eval_task.json` as a modular suite, but it does not yet enforce every skill having one or validate skill-local eval coverage quality beyond the existing task JSON schema and judge prompts.
metrics:
  - skill_local_eval_discovery_pass
last_verified: 2026-06-11
---
# Modular skill-local eval tasks

Modular skill-local eval tasks is a first-class Farplane feature in [Skill System](../systems/skill-system.md). It survives as a `FEAT-*` handle because it has owner surfaces, evidence, limits, and a maintenance path.

```text
feature(FEAT-0054, repo_state?) -> behavior + evidence + maintenance_signal
```

## System

- System: [Skill System](../systems/skill-system.md)
- Feature ID: `FEAT-0054`
- Status: `implemented`
- Category: `skills`

## Owned Behavior

This feature owns the behavior implemented, specified, or enforced by its owner surfaces. Keep the details in those surfaces; keep this page focused on the stable feature contract and registry metadata.

## Owner Surfaces

- `skills/eval/scripts/run_evals.py`
- `skills/eval/SKILL.md`
- `skills/eval/eval_task.json`
- `docs/skills/templates/SKILL_TEMPLATE.md`
- `docs/skills/system.md`
- `docs/skills/best-practices.md`

## Source Context

- `docs/MEMORY.md#MEM-0145`
- `docs/HISTORY.md`

## Evidence

- `skills/eval/eval_task.json`
- `skills/eval/tests/test_run_evals.py`
- `docs/HISTORY.md`

## Known Limits

The runner discovers `skills/*/eval_task.json` as a modular suite, but it does not yet enforce every skill having one or validate skill-local eval coverage quality beyond the existing task JSON schema and judge prompts.

## Metrics

- `skill_local_eval_discovery_pass`

## Maintenance

Update this feature doc before regenerating `docs/features/registry.jsonl`. If the feature stops deserving its own doc, delete this file and remove all active template, source, ticket, and system refs to `FEAT-0054`.
