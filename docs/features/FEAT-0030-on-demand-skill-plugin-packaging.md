---
title: On-demand skill plugin packaging
status: implemented
owner: feature-registry
created_at: 2026-06-26
updated_at: 2026-06-26
tags:
  - farplane
  - feature
  - sys-0006
refs:
  - skills/skill-maintenance/scripts/sync_skill_plugins.py
  - skills/skill-maintenance/scripts/install_selected_skills.py
  - install.sh
  - README.md
  - docs/HISTORY.md
  - skills/skill-maintenance/scripts/test_install_selected_skills.py
  - skills/skill-maintenance/scripts/test_sync_skill_plugins.py
feature_id: FEAT-0030
system_id: SYS-0006
category: skills
public: true
surfaces:
  - skills/skill-maintenance/scripts/sync_skill_plugins.py
  - skills/skill-maintenance/scripts/install_selected_skills.py
  - install.sh
  - README.md
source_refs:
  - skills/skill-maintenance/scripts/sync_skill_plugins.py
  - skills/skill-maintenance/scripts/install_selected_skills.py
  - install.sh
  - docs/HISTORY.md
external_refs:
  - https://developers.openai.com/codex/plugins
  - https://developers.openai.com/codex/plugins/build
evidence_refs:
  - skills/skill-maintenance/scripts/test_install_selected_skills.py
  - skills/skill-maintenance/scripts/test_sync_skill_plugins.py
  - docs/HISTORY.md
known_limits: Generated plugin packages are no longer tracked in source. Farplane keeps `skills/*` as the source of truth; skill-maintenance owns the implementation, and install.sh now calls the owner script directly. Official self-serve public Plugin Directory publishing, icons, screenshots, apps, MCP servers, and hooks are not included yet.
metrics:
  - selected_skill_installer_tests_pass
  - skill_plugin_generation_pass
last_verified: 2026-06-24
---
# On-demand skill plugin packaging

On-demand skill plugin packaging is a first-class Farplane feature in [Skill System](../systems/skill-system.md). It survives as a `FEAT-*` handle because it has owner surfaces, evidence, limits, and a maintenance path.

```text
feature(FEAT-0030, repo_state?) -> behavior + evidence + maintenance_signal
```

## System

- System: [Skill System](../systems/skill-system.md)
- Feature ID: `FEAT-0030`
- Status: `implemented`
- Category: `skills`

## Owned Behavior

This feature owns the behavior implemented, specified, or enforced by its owner surfaces. Keep the details in those surfaces; keep this page focused on the stable feature contract and registry metadata.

## Owner Surfaces

- `skills/skill-maintenance/scripts/sync_skill_plugins.py`
- `skills/skill-maintenance/scripts/install_selected_skills.py`
- `install.sh`
- `README.md`

## Source Context

- `skills/skill-maintenance/scripts/sync_skill_plugins.py`
- `skills/skill-maintenance/scripts/install_selected_skills.py`
- `install.sh`
- `docs/HISTORY.md`

## Evidence

- `skills/skill-maintenance/scripts/test_install_selected_skills.py`
- `skills/skill-maintenance/scripts/test_sync_skill_plugins.py`
- `docs/HISTORY.md`

## Known Limits

Generated plugin packages are no longer tracked in source. Farplane keeps `skills/*` as the source of truth; skill-maintenance owns the implementation, and install.sh now calls the owner script directly. Official self-serve public Plugin Directory publishing, icons, screenshots, apps, MCP servers, and hooks are not included yet.

## Metrics

- `selected_skill_installer_tests_pass`
- `skill_plugin_generation_pass`

## Maintenance

Update this feature doc before regenerating `docs/features/registry.jsonl`. If the feature stops deserving its own doc, delete this file and remove all active template, source, ticket, and system refs to `FEAT-0030`.
