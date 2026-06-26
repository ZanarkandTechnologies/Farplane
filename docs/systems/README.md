---
title: "Systems"
status: active
owner: doc-governance
created_at: 2026-06-26
updated_at: 2026-06-26
tags:
  - farplane
  - systems
  - features
refs:
  - docs/features/README.md
  - docs/features/registry.jsonl
  - docs/systems/registry.jsonl
---

# Systems

Farplane systems are the public, maintainable product modules. Each Markdown file in this directory owns one system record plus the capability handles that belong to it.

```text
system spec markdown
  -> docs/systems/registry.jsonl       # public system inventory
  -> docs/features/registry.jsonl      # internal capability inventory
```

Use this directory when deciding what Farplane is made of. Use `docs/features/registry.jsonl` when a template, ticket, source run, or validator needs a stable `FEAT-*` compatibility handle.

## Current Systems

| System | Primary capability | Owner file |
| --- | --- | --- |
| Agent Kernel | `FEAT-0042` | `agent-kernel.md` |
| Work Loop | `FEAT-0007` | `work-loop.md` |
| Horizon Loop | `FEAT-0029` | `horizon-loop.md` |
| Invocation Runtime | `FEAT-0015` | `invocation-runtime.md` |
| Proof And Review | `FEAT-0008` | `proof-review.md` |
| Skill System | `FEAT-0022` | `skill-system.md` |
| Self-Improvement And Learning | `FEAT-0039` | `self-improvement-learning.md` |
| Source And Sidecar Systems | `FEAT-0011` | `source-sidecar-systems.md` |
| Maintenance And Release OS | `FEAT-0060` | `maintenance-release-os.md` |
| Domain Skill Families | `FEAT-0014` | `domain-skill-families.md` |

## Update Flow

1. Update the owning system Markdown file.
2. Run `python3 docs/features/validate_features.py --write`.
3. Run `python3 docs/features/validate_features.py`.
4. Run template/adoption/doc validators when a referenced capability or owner path changes.

Do not hand-edit generated JSONL registries.
