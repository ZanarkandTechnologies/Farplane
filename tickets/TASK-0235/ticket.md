---
template_id: ticket-template
template_version: "0.1.1"
feature_refs:
  - FEAT-0060
ticket_id: TASK-0235
title: Make feature registry source-of-truth feature docs
phase: complete
status: done
owner: codex
claimed_by:
priority: high
depends_on:
  - TASK-0231
blocked_by: []
ready: false
approval_required: false
requires_qa: true
requires_demo: false
created_at: 2026-06-26T15:42:57+08:00
updated_at: 2026-06-26T21:34:03+08:00
next_action: complete; commit the strict feature-doc registry cleanup
last_verification: all Done / Proof commands passed; stale deleted FEAT search returned no active refs
---

# TASK-0235: Make Feature Registry Source-Of-Truth Feature Docs

## Summary

Replace the weak "systems own many tiny feature rows" model with a stricter
feature-doc model. Systems explain Farplane's public product layers. A `FEAT-*`
survives only when it has its own feature page in `docs/features/` with
frontmatter, `feature_record_json`, owner surfaces, evidence, limits, and
maintenance rules.

## Scope

- In:
  - Keep `docs/systems/*.md` as the public system layer.
  - Move first-class feature records into feature pages in `docs/features/`.
  - Generate `docs/features/registry.jsonl`, `docs/features/registry.md`,
    `docs/systems/registry.jsonl`, and `docs/systems/registry.md`.
  - Collapse the old 64-row feature registry down to the 21 feature IDs that
    earn their own feature docs.
  - Remove active template, source, and docs references to deleted feature IDs.
  - Make `docs/features/TEMPLATE.md` the feature-authoring template.
  - Rewrite docs, scout, skill, and governance guidance around the new source
    of truth.
  - Delete tracked generated template snapshot archives and move future
    snapshots to ignored `tmp/`.
- Out:
  - No generic entity-consolidation engine.
  - No metrics registry implementation.
  - No hidden scheduler, daemon, or UI route.
  - No retention of non-doc-worthy `FEAT-*` handles as aliases.

## Delta

- `Before:` `FEAT-*` rows could survive as internal compatibility handles
  under system docs, which made implementation details look like product
  features.
- `After:` `FEAT-*` means "docs-worthy first-class feature." If it lacks a
  feature page, it gets deleted and active references are removed.
- `Example:` `FEAT-0064 Skill signals` survives as
  `docs/features/FEAT-0064-skill-signals.md`; Inspiration Vault is
  removed from feature metadata and remains only a proposed spec until it earns
  a real feature doc.

## Program

```text
strict_feature_docs(repo)
  -> surviving_feature_docs
   + generated_system_registry
   + generated_feature_registry
   + stale_ref_cleanup
   + validation_evidence

program:
  inventory(old_feature_rows, system_specs, template_refs, source_refs)
    -> survivor_set + deleted_ids

  author_feature_docs(survivor_set)
    -> feature pages in docs/features/
    -> docs/features/TEMPLATE.md

  simplify_system_docs()
    -> system_record_json only
    -> feature_refs pointing at surviving feature docs

  rewrite_docs_contract()
    -> feature README/AGENTS
    -> system README
    -> docs governance and lifecycle
    -> source/scout/skill guidance

  purge_stale_refs(deleted_ids)
    -> templates, source refs, specs, tickets, generated docs

  verify()
    -> feature/system generator pass
    -> source/template/doc/skill/ticket validators
    -> py_compile
```

## Map

- `Touch:`
  - feature pages in `docs/features/`
  - `docs/features/TEMPLATE.md`
  - `docs/features/README.md`
  - `docs/features/AGENTS.md`
  - `docs/features/validate_features.py`
  - `docs/features/registry.jsonl`
  - `docs/features/registry.md`
  - `docs/systems/*.md`
  - `docs/systems/README.md`
  - `docs/systems/registry.jsonl`
  - `docs/systems/registry.md`
  - `docs/specs/feature-catalog.md`
  - `docs/specs/doc-governance.md`
  - `docs/specs/filesystem-lifecycle.md`
  - `docs/specs/harness-techniques.md`
  - `docs/specs/inspiration-vault.md`
  - `docs/sources/registry.jsonl`
  - `docs/templates/registry.jsonl`
  - `skills/*` docs that mention system/feature metadata
  - high-impact templates with `feature_refs`
- `Delete:`
  - `skills/skill-maintenance/templates/archive/*`
- `Inspect:`
  - template and source validators
  - stale FEAT reference search
  - generated registry diffs

## Done / Proof

- [x] `python3 docs/features/validate_features.py --write`
- [x] `python3 docs/features/validate_features.py`
- [x] `python3 docs/sources/validate_sources.py`
- [x] `python3 bin/validators/sync_template_registry.py --write`
- [x] `python3 bin/validators/sync_template_registry.py`
- [x] `python3 bin/validators/check_doc_refs.py`
- [x] `python3 bin/validators/check_doc_parity.py`
- [x] `python3 bin/validators/check_harness_invariants.py`
- [x] `python3 skills/skill-maintenance/scripts/check_skills.py --write`
- [x] `python3 skills/skill-maintenance/scripts/check_skills.py`
- [x] `python3 tickets/scripts/check_ticket_metadata.py`
- [x] `python3 -m py_compile docs/features/validate_features.py skills/skill-maintenance/scripts/generate_template_intelligence.py`

## State

- `2026-06-26T15:42:57+08:00:` Ticket drafted around feature hierarchy.
- `2026-06-26T17:05:00+08:00:` First migration pass shipped the weaker
  system-owned capability-row model.
- `2026-06-26T21:28:00+08:00:` Operator rejected compatibility handles for
  non-doc-worthy features. Ticket reopened for strict feature-doc source of
  truth and deletion of dead feature rows.
- `2026-06-26T21:34:03+08:00:` Strict feature-doc source of truth implemented,
  registries regenerated, tracked template snapshot archive deleted, and proof
  checks passed.

## Links

- `docs/systems/README.md`
- `docs/features/README.md`
- `docs/features/TEMPLATE.md`
- `docs/specs/feature-catalog.md`
- `docs/specs/doc-governance.md`
