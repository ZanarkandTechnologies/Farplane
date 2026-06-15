---
title: Template Registry
status: active
owner: Farplane
updated_at: 2026-06-16
---

# Template Registry

`docs/templates/registry.jsonl` tracks the highest-impact prompt-shaped
templates whose structure can materially change harness behavior.

## Current Scope

The registry is deliberately focused on five surfaces:

- `templates/global/AGENTS.md`
- `skills/skill-creator/references/SKILL_TEMPLATE.md`
- `tickets/templates/ticket.md`
- `tickets/templates/goal-loop/program.md`
- `skills/harness-creator/templates/project-harness.md`

Each tracked template declares:

- `template_id`
- `template_version`
- `feature_refs`

`path` is added by the generator so the UI and validators can resolve the
template row back to source.

## Commands

```bash
python3 bin/validators/sync_template_registry.py --write
python3 bin/validators/sync_template_registry.py --check
python3 bin/validators/check_template_version_metadata.py --all
```

## Boundary

This is not broad document versioning yet. Scaffold templates, UI app starter
files, and low-impact helper templates stay out until they have a clear
consumer or optimization loop. Document versioning can use a separate registry
once its owner and UI are known.
