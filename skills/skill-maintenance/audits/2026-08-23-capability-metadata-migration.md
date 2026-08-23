---
skill: skill-maintenance
date: 2026-08-23
change_type: metadata_update
status: passed
owner: skills/skill-maintenance
review_route: reviewer
---

# Capability Metadata Migration

## Decision

Retire `portfolio` and skill-local `profiles` from skill frontmatter. Keep
`group` for Tier 3 department ownership and `capability` for specialized
artifact, integration, and explicit-shortcut contracts. Runtime capability
profiles remain independent restriction policy.

## Changed Owners

- `bin/core/skill_contract.py`
- `bin/validators/sync_skill_registry.py`
- `bin/validators/check_skill_frontmatter.py`
- `skills/skill-maintenance/scripts/{generate_skill_graph.py,sync_skill_plugins.py}`
- `install.sh`, skill docs/template, tests, and generated registry

## Proof

- `python3 skills/skill-maintenance/scripts/check_skills.py --write`
  - 118 valid skills; capability coverage: 1 artifact, 18 integrations, 11
    shortcuts, 88 core-by-absence.
- Focused unit suite: 55 tests passed across schema, registry, graph, plugin,
  quick-validator, Git-gate, and installer surfaces.
- `bash -n install.sh`
- `python3 skills/skill-maintenance/scripts/sync_skill_plugins.py --check`
- `python3 bin/validators/check_skill_frontmatter.py --report`
- Independent reviewer follow-up: `TAS-A`, pass. The template uses only
  strict-valid capability fields, and both Git stages route capability-derived
  graph/plugin changes through the `skill_projection` test gate.

## Residual Decision

No artifact contracts were invented for the 88 skills without one. The next
artifact-map expansion must declare real durable input/output families, not
convert old portfolio labels mechanically.
