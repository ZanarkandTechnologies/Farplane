---
template_id: ticket-template
template_version: "0.1.1"
feature_refs:
  - FEAT-0041
  - FEAT-0049
  - FEAT-0055
  - FEAT-0060
ticket_id: TASK-0235
title: Move feature registry to system-owned capability specs
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
updated_at: 2026-06-26T17:05:00+08:00
next_action: complete; scoped commit is the only remaining operator-visible follow-through
last_verification: all Done / Proof commands passed, including system/feature generation, template registry, doc refs/parity, harness invariants, skill maintenance checks, ticket metadata, and py_compile
---

# TASK-0235: Move Feature Registry To System-Owned Capability Specs

## Summary

Replace the flat hand-authored feature-catalog model with a small public system
stack. Authored metadata now lives in `docs/systems/*.md`; generated output
still preserves stable `FEAT-*` handles for templates, tickets, sources,
validators, and adoption checks.

## Scope

- In:
  - Add `docs/systems/` as the public system/spec layer.
  - Author one Markdown file per system with `system_record_json` plus
    `capability_records_json`.
  - Generate `docs/systems/registry.jsonl` and `docs/features/registry.jsonl`
    from system specs.
  - Collapse the old 64 capability rows under 10 system specs instead of
    presenting each row as a public feature.
  - Preserve existing `FEAT-*` IDs as compatibility handles.
  - Rewrite registry, docs-governance, framework, skill, source, and interval
    guidance so future edits go through `docs/systems/*.md`.
  - Keep `docs/specs/feature-catalog.md` only as a compatibility pointer.
  - Run docs, feature/system, template, ticket, and skill/doc validators.
- Out:
  - No deletion or reuse of existing `FEAT-*` IDs.
  - No hidden scheduler, daemon, UI route, or remote telemetry behavior.
  - No generic entity-consolidation engine.
  - No metrics registry implementation.
  - No broad archive deletion pass beyond replacing the stale feature catalog
    source.

## Delta

- `Before:` `docs/specs/feature-catalog.md` and scattered spec
  `feature_records_json` blocks acted as authored metadata sources. The
  generated registry made dozens of small internal handles look like equal
  public features.
- `After:` `docs/systems/*.md` is the authored source. `SYS-*` records are the
  public system/module view, while generated `FEAT-*` rows are internal
  capability handles with `system_id`, `system_name`, `capability_role`,
  `public`, and `owner_spec`.
- `Example:` `FEAT-0064 Skill compounding score` is owned by
  `docs/systems/skill-system.md`; `docs/specs/skill-compounding-score.md`
  remains the behavioral contract and points back through `feature_refs`.

## Program

```text
move_feature_registry_to_system_specs(repo)
  -> system_specs
   + generated_system_registry
   + generated_capability_registry
   + updated_docs_contract
   + validation_evidence

program:
  inventory(current_features, current_specs)
    -> capability_clusters

  create_system_specs(capability_clusters)
    -> docs/systems/*.md
    -> system_record_json + capability_records_json

  update_generator()
    -> validate system records
    -> validate capability records
    -> render docs/systems/registry.jsonl
    -> render docs/features/registry.jsonl

  rewrite_docs_contract()
    -> registry README and AGENTS files
    -> doc governance and filesystem lifecycle
    -> framework and skill guidance
    -> old feature catalog compatibility pointer

  verify()
    -> feature/system generator pass
    -> template registry pass
    -> doc refs/parity pass
    -> skill checks if skill docs changed
    -> ticket metadata pass
```

## Map

- `Touch:`
  - `docs/systems/*.md`
  - `docs/systems/README.md`
  - `docs/systems/registry.jsonl`
  - `docs/features/README.md`
  - `docs/features/AGENTS.md`
  - `docs/features/registry.jsonl`
  - `docs/features/validate_features.py`
  - `docs/specs/feature-catalog.md`
  - `docs/specs/skill-compounding-score.md`
  - `docs/specs/doc-governance.md`
  - `docs/specs/filesystem-lifecycle.md`
  - `docs/specs/harness-techniques.md`
  - `docs/specs/README.md`
  - docs and skill guidance that mentioned the old feature source
- `Inspect:`
  - `docs/templates/registry.jsonl`
  - `templates/global/AGENTS.md`
  - `docs/skills/templates/*`
  - `bin/validators/sync_template_registry.py`
  - `skills/harness-advisor/SKILL.md`
  - `skills/documentation/SKILL.md`
  - `skills/interval-update/references/workflows/docs-consolidation.md`

## Done / Proof

- [x] `python3 docs/features/validate_features.py --write`
- [x] `python3 docs/features/validate_features.py`
- [x] `python3 bin/validators/sync_template_registry.py --write`
- [x] `python3 bin/validators/sync_template_registry.py`
- [x] `python3 bin/validators/check_doc_refs.py`
- [x] `python3 bin/validators/check_doc_parity.py`
- [x] `python3 bin/validators/check_harness_invariants.py`
- [x] `python3 skills/skill-maintenance/scripts/check_skills.py --write`
- [x] `python3 skills/skill-maintenance/scripts/check_skills.py`
- [x] `python3 tickets/scripts/check_ticket_metadata.py`
- [x] `python3 -m py_compile docs/features/validate_features.py`

## State

- `2026-06-26T15:42:57+08:00:` Ticket drafted around feature hierarchy.
- `2026-06-26T16:40:00+08:00:` User approved stronger systems rewrite. Ticket
  moved to building; first generator write pass succeeded.
- `2026-06-26T17:05:00+08:00:` Migration implemented and proof checklist
  passed. Ready for scoped commit.

## Links

- `docs/systems/README.md`
- `docs/features/README.md`
- `docs/specs/feature-catalog.md`
- `docs/specs/doc-governance.md`
