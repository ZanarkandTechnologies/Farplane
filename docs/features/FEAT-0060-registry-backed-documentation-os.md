---
title: Registry-backed documentation OS
status: implemented
owner: feature-registry
created_at: 2026-06-26
updated_at: 2026-06-27
tags:
  - farplane
  - feature
  - sys-0009
refs:
  - docs/features/README.md
  - docs/features/TEMPLATE.md
  - docs/features/validate_features.py
  - docs/features/registry.jsonl
  - docs/systems/README.md
  - docs/systems/registry.jsonl
  - docs/templates/registry.jsonl
  - docs/templates/README.md
  - rules/template-registry.toml
  - rules/template-version-watch.toml
  - bin/validators/sync_template_registry.py
  - templates/global/AGENTS.md
  - docs/skills/templates/SKILL_TEMPLATE.md
feature_id: FEAT-0060
system_id: SYS-0009
category: context-routing
public: true
surfaces:
  - docs/features/README.md
  - docs/features/TEMPLATE.md
  - docs/features/validate_features.py
  - docs/features/registry.jsonl
  - docs/systems/README.md
  - docs/systems/registry.jsonl
  - docs/templates/registry.jsonl
  - docs/templates/README.md
  - rules/template-registry.toml
  - rules/template-version-watch.toml
  - bin/validators/sync_template_registry.py
  - templates/global/AGENTS.md
  - docs/skills/templates/SKILL_TEMPLATE.md
source_refs:
  - docs/features/README.md
  - docs/systems/README.md
  - docs/templates/registry.jsonl
external_refs: []
evidence_refs:
  - docs/features/validate_features.py
  - bin/validators/test_check_doc_refs.py
  - bin/validators/test_doc_parity.py
  - bin/validators/test_sync_template_registry.py
known_limits: Owns documentation, system, feature, and template registry coherence. It does not preserve retired feature IDs or permanent tracked archive docs just to keep historical noise searchable.
metrics:
  - feature_registry_validation_pass
  - template_feature_registry_validation_pass
  - doc_reference_validation_pass
last_verified: 2026-06-27
---
# Registry-backed documentation OS

Registry-backed documentation OS is a first-class Farplane feature in [Maintenance And Release OS](../systems/maintenance-release-os.md). It survives as a `FEAT-*` handle because it owns the way public docs, systems, features, templates, and generated registries stay coherent.

```text
documentation_os(change, repo_state) -> owner_doc + generated_registry_delta + validation_result
```

## System

- System: [Maintenance And Release OS](../systems/maintenance-release-os.md)
- Feature ID: `FEAT-0060`
- Status: `implemented`
- Category: `context-routing`

## Feature Spec

This feature folds the former doc-governance, filesystem-lifecycle, feature-catalog, harness-technique inventory, and high-impact template registry specs into one owner.

Core rules:

- Feature docs are the spec files. A `FEAT-*` exists only when a concrete file such as `docs/features/FEAT-0060-registry-backed-documentation-os.md` owns the behavior contract, surfaces, evidence, limits, and registry metadata.
- System docs are public product-layer containers. They group feature specs; they do not preserve weak feature rows.
- Generated registries are outputs. Edit system and feature Markdown, then regenerate JSONL/Markdown registries.
- Durable Markdown uses compact YAML front matter for routing and machine-readable metadata; body prose owns the human contract.
- Artifact-first writing applies when a result will be reused, resumed, audited, or validated. Chat is fine for one-off answers.
- Raw signal stays in tickets, experiments, source records, or temporary artifacts until distilled into an owning feature, system, skill, lesson, or memory file.
- Stale specs, duplicate docs, retired feature aliases, permanent future-idea piles, and tracked archive docs are deleted after current truth is folded into an active owner.

Lifecycle owners:

- `docs/features/FEAT-NNNN-name.md`: feature specs and registry source.
- `docs/systems/*.md`: system stack and feature grouping.
- `docs/fundamentals/`: theory and reusable doctrine.
- `docs/skills/` and `skills/<name>/`: skill-system policy and executable workflows.
- `tickets/`: task-local plans, blockers, proof, and closeout evidence.
- `experiments/` and `tmp/`: bounded proof and scratch work that must not become canonical memory by accident.

Template registry contract:

- High-impact prompt-shaped templates keep stable metadata and feature refs.
- `bin/validators/sync_template_registry.py` owns generated template registry freshness.
- Low-impact scaffolds do not get registry ceremony until they have a real consumer.

Non-goals:

- No parallel spec-folder truth shelf.
- No permanent tracked archives by default.
- No compatibility feature rows for capabilities that do not earn their own feature spec.

Proof gates:

- `python3 docs/features/validate_features.py` passes.
- `python3 bin/validators/check_doc_parity.py` passes for canonical entrypoint coherence.
- `python3 bin/validators/check_doc_refs.py` passes for canonical docs.
- Feature docs, system docs, and template registries agree on surviving IDs.
- Deleted docs leave no active broken references in scanned canonical surfaces.

## Owner Surfaces

- `docs/features/README.md`
- `docs/features/TEMPLATE.md`
- `docs/features/validate_features.py`
- `docs/features/registry.jsonl`
- `docs/systems/README.md`
- `docs/systems/registry.jsonl`
- `docs/templates/registry.jsonl`
- `docs/templates/README.md`
- `rules/template-registry.toml`
- `rules/template-version-watch.toml`
- `bin/validators/sync_template_registry.py`
- `templates/global/AGENTS.md`
- `docs/skills/templates/SKILL_TEMPLATE.md`

## Source Context

- `docs/features/README.md`
- `docs/systems/README.md`
- `docs/templates/registry.jsonl`

## Evidence

- `docs/features/validate_features.py`
- `bin/validators/test_check_doc_refs.py`
- `bin/validators/test_doc_parity.py`
- `bin/validators/test_sync_template_registry.py`

## Known Limits

Owns documentation, system, feature, and template registry coherence. It does not preserve retired feature IDs or permanent tracked archive docs just to keep historical noise searchable.

## Metrics

- `feature_registry_validation_pass`
- `template_feature_registry_validation_pass`
- `doc_reference_validation_pass`

## Maintenance

Update this feature doc before regenerating `docs/features/registry.jsonl`. If the feature stops deserving its own doc, delete this file and remove all active template, source, ticket, and system refs to `FEAT-0060`.
