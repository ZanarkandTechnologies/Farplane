---
title: On-demand skill plugin packaging
status: implemented
owner: feature-registry
created_at: 2026-06-26
updated_at: 2026-06-27
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

On-demand skill plugin packaging exists to package reusable Farplane skills and plugin
surfaces only when they have a real consumer and validation path. It belongs to [Skill
System](../systems/skill-system.md) and keeps `FEAT-0030` as a stable capability handle
because the behavior has an owner, proof path, and maintenance boundary.

```text
package_skill(skill_dir, audience) -> plugin_artifact + install_contract + validation_signal
```

## At A Glance

- Feature ID: `FEAT-0030`
- System: [Skill System](../systems/skill-system.md)
- Status: `implemented`
- Category: `skills`
- Primary user: skill author and plugin maintainer
- Job: package reusable Farplane skills and plugin surfaces only when they have a real consumer and validation path.

## Problem

Farplane skills can outgrow local-only use, but packaging everything too early creates
stale plugin shells and version noise.

This feature defines when a skill deserves on-demand packaging and what proof is
required before it becomes installable.

## What It Does

- Identifies skills or plugin surfaces that should be distributed beyond the repo.
- Keeps local skill docs, templates, scripts, and QA checklists as the source package.
- Creates plugin metadata and install paths only for skills with clear consumer value.
- Runs validation before treating a package as shipped.
- Keeps retired or local-only workflows out of public plugin ceremony.

## User Stories

- As a skill author, I know when to keep a workflow local and when to package it.
- As an installer, I can trust packaged skills include metadata and validation.
- As a maintainer, I can avoid packaging every experiment as a product.

## Operating Contract

Packaging follows proven reuse, not speculative distribution.

- A package has a source skill directory, consumer, metadata, install path, and validation check.
- The repo-owned skill remains the source of truth until an explicit release process says otherwise.
- Plugin metadata references stable skill behavior rather than duplicating full instructions.
- Package changes are validated with the owning skill and registry checks.

## Surfaces

Owner surfaces:

- `skills/skill-maintenance/scripts/sync_skill_plugins.py`
- `skills/skill-maintenance/scripts/install_selected_skills.py`
- `install.sh`
- `README.md`

Source context:

- `skills/skill-maintenance/scripts/sync_skill_plugins.py`
- `skills/skill-maintenance/scripts/install_selected_skills.py`
- `install.sh`
- `docs/HISTORY.md`

External context:

- `https://developers.openai.com/codex/plugins`
- `https://developers.openai.com/codex/plugins/build`

Evidence:

- `skills/skill-maintenance/scripts/test_install_selected_skills.py`
- `skills/skill-maintenance/scripts/test_sync_skill_plugins.py`
- `docs/HISTORY.md`

## Proof And Quality

Required checks:

- `python3 docs/features/validate_features.py`
- `python3 bin/validators/check_doc_refs.py`

Acceptance signals:

- The feature remains listed under exactly one owning system.
- The owner surfaces still exist and agree with this contract.
- Evidence refs support the current status.

## Rollout And Maintenance

- Update this feature page first when the capability contract changes.
- Then update owner surfaces and regenerate feature/system registries when metadata changes.
- Preserve the feature ID while active templates, skills, tickets, or docs still reference it.
- Maintenance owner: Skill System.

## Limits And Non-Goals

- This feature does not publish every local skill.
- This feature does not let installed copies become the source of truth.
- This feature does not replace skill-maintenance.
- Known limit: Generated plugin packages are no longer tracked in source. Farplane keeps `skills/*` as the source of truth; skill-maintenance owns the implementation, and install.sh now calls the owner script directly. Official self-serve public Plugin Directory publishing, icons, screenshots, apps, MCP servers, and hooks are not included yet.
- Delete or merge this feature only when its current truth has moved into a clearer owner and all active refs are removed.

## Metrics

- `selected_skill_installer_tests_pass`
- `skill_plugin_generation_pass`

## Alternatives Considered

- Keep this only as a registry row.
  Decision: reject.
  Reason: Farplane features must be readable specs, not opaque metadata entries.
- Fold this entirely into the owning system page.
  Decision: defer.
  Reason: keep the `FEAT-*` page while templates, skills, tickets, or proof surfaces need a stable capability handle.

## Change History

- 2026-06-26: Feature spec created.
- 2026-06-27: Migrated into the reader-first feature-spec shape.
