---
title: "Documentation Skill Governance Refresh"
status: active
owner: documentation
created_at: 2026-06-23
updated_at: 2026-06-23
tags:
  - documentation
  - skill-maintenance
  - docs-governance
refs:
  - skills/documentation/SKILL.md
  - skills/documentation/qa_checklist.md
  - docs/features/FEAT-0060-registry-backed-documentation-os.md
  - docs/features/FEAT-0060-registry-backed-documentation-os.md
---

# Documentation Skill Governance Refresh

## Scope

Refresh `documentation` from a broad doc-writing helper into a docs-as-code
workflow that checks reader contract, placement, split/merge decisions, density
policy, source of truth, front matter, versioning metadata, grounding, and
review routing.

## Local Grounding

- `docs/features/FEAT-0060-registry-backed-documentation-os.md` defines the default durable Markdown
  front matter schema and says surface-specific schemas may add fields such as
  `template_version`, `feature_refs`, `source_refs`, `supersedes`, and
  `last_verified`.
- `docs/features/FEAT-0060-registry-backed-documentation-os.md` defines canonical doc surfaces, document
  architecture, structural checks, narrative audits, and the gardening loop.
- Existing docs use mixed schemas. The skill should preserve local schemas
  instead of inventing one universal version field.

## External Grounding

- Diataxis: classify docs by user need: tutorial, how-to, reference, or
  explanation.
- Google Developer Documentation Style Guide: make docs clear, consistent,
  accessible, descriptive, and concise.
- Microsoft Writing Style Guide: prefer warm, crisp, clear, concise, consistent
  technical prose.
- GitHub Docs, Hugo, and Quarto use YAML front matter for page metadata,
  versioning/routing, and content management.

## Change

- Added current skill front matter with `skill_template_version: "0.3.0"` and a
  root `qa_checklist.md`.
- Added a skill signature and bounded routing to `reference-grounding`,
  `advise`, `review`, and `close-ticket`.
- Promoted checklist work into a root checklist with metadata/versioning,
  placement, split/merge, density, grounding, and local validator gates.
- Added a documentation architecture policy to `docs/features/FEAT-0060-registry-backed-documentation-os.md`
  for new-file decisions, merge decisions, split triggers, density by surface,
  and task-evidence cleanup.
- Removed the old reference checklist path so `qa_checklist.md` is the single
  active checklist surface.

## Proof

- Run `python3 skills/skill-maintenance/scripts/check_skills.py --write`.
- Reinstall the live `documentation` skill after validation.
