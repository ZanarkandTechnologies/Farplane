---
title: "Feature Catalog Compatibility"
status: active
owner: doc-governance
created_at: 2026-06-26
updated_at: 2026-06-26
tags:
  - farplane
  - features
  - systems
  - generated-registry-source
refs:
  - docs/systems/README.md
  - docs/systems/registry.jsonl
  - docs/features/README.md
  - docs/features/registry.jsonl
  - docs/features/validate_features.py
---

# Feature Catalog Compatibility

Farplane no longer keeps a hand-authored feature catalog in this spec. The
authored source of truth is now split by owner:

- [`docs/systems/`](../systems/README.md) for public product modules.
- [`docs/features/`](../features/README.md) for first-class `FEAT-*` feature
  docs.

```text
docs/systems/*.md
  -> docs/systems/registry.jsonl

feature pages in docs/features/
  -> docs/features/registry.jsonl
  -> docs/features/registry.md
```

Use this file as a compatibility pointer when older docs, tickets, templates, or
research notes mention `docs/specs/feature-catalog.md`.

## Current Contract

- Public product modules are `SYS-*` records authored in
  `docs/systems/*.md` front matter.
- Stable feature handles are `FEAT-*` records authored as feature pages in
  `docs/features/`.
- Every surviving `FEAT-*` handle belongs to exactly one system through
  `system_id` and the owning system's `feature_refs`.
- If a capability does not deserve its own feature page, delete the handle and
  remove active references to it.
- `docs/systems/registry.jsonl` is generated public system inventory.
- `docs/features/registry.jsonl` is generated feature inventory for templates,
  tickets, sources, validators, and adoption checks.
- New durable capabilities should start from `docs/features/TEMPLATE.md`. If no
  existing system owns the feature, update the system stack before creating the
  `FEAT-*` handle.

## Update Flow

1. Edit the owning file under `docs/systems/` or `docs/features/`.
2. Run:

   ```bash
   python3 docs/features/validate_features.py --write
   python3 docs/features/validate_features.py
   ```

3. Update template, source, docs, or ticket refs only when their referenced
   capability or system changed.

Do not add `feature_records_json` here. Do not hand-edit generated JSONL.
