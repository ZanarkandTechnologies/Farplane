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
authored source of truth is now the system stack under
[`docs/systems/`](../systems/README.md).

```text
docs/systems/*.md
  -> docs/systems/registry.jsonl
  -> docs/features/registry.jsonl
```

Use this file as a compatibility pointer when older docs, tickets, templates, or
research notes mention `docs/specs/feature-catalog.md`.

## Current Contract

- Public product modules are `SYS-*` records authored in
  `docs/systems/*.md` front matter.
- Stable compatibility handles remain `FEAT-*` records, but each one now
  belongs to exactly one system spec through `capability_records_json`.
- `docs/systems/registry.jsonl` is generated public system inventory.
- `docs/features/registry.jsonl` is generated internal capability inventory for
  templates, tickets, sources, validators, and adoption checks.
- New durable capabilities should be added to the owning system spec. If no
  existing system owns the capability, update the system stack before creating
  another `FEAT-*` handle.

## Update Flow

1. Edit the owning file under `docs/systems/`.
2. Run:

   ```bash
   python3 docs/features/validate_features.py --write
   python3 docs/features/validate_features.py
   ```

3. Update template, source, docs, or ticket refs only when their referenced
   capability or system changed.

Do not add `feature_records_json` here. Do not hand-edit generated JSONL.
