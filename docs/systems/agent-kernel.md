---
title: "Agent Kernel"
status: active
owner: farplane-framework
created_at: 2026-06-26
updated_at: 2026-06-27
tags:
  - farplane
  - systems
  - agent-kernel
refs:
  - AGENTS.md
  - templates/global/AGENTS.md
  - docs/fundamentals/harness-engineering-doctrine.md
system_record_json: |
  {
    "id": "SYS-0001",
    "name": "Agent Kernel",
    "status": "implemented",
    "summary": "The installed agent context, templates, prompt rules, and response conventions that let a Codex enter Farplane with the right operating shape.",
    "owner_spec": "docs/systems/agent-kernel.md",
    "primary_feature_ref": "FEAT-0042",
    "feature_refs": [
      "FEAT-0042"
    ],
    "refs": [
      "AGENTS.md",
      "templates/global/AGENTS.md",
      "docs/fundamentals/harness-engineering-doctrine.md"
    ],
    "last_verified": "2026-06-26"
  }
---
# Agent Kernel

The installed agent context, templates, prompt rules, and response conventions that let
a Codex enter Farplane with the right operating shape. This page is the product-layer
owner for that subsystem: it explains what belongs here, which feature specs make up the
stack, and where adjacent responsibilities should move.

```text
agent_kernel(change, repo_state?) -> owned_feature_set + boundary_decision + maintenance_signal
```

## At A Glance

- System ID: `SYS-0001`
- Status: `implemented`
- Primary feature: `FEAT-0042`
- Owner spec: `docs/systems/agent-kernel.md`
- Feature count: `1`

## Role

Agent Kernel owns the always-loaded operating shape for Farplane agents: autonomy,
action/plan/answer mode, reading discipline, skill routing, proof expectations, and
concise communication. It keeps permanent context lean by pointing detailed procedure to
skills, specs, tickets, validators, and templates.

## Feature Docs

- [FEAT-0042 Lean global agent operating kernel](../features/FEAT-0042-lean-global-agent-operating-kernel.md)

## What Belongs Here

Global and project AGENTS policy, install templates, prompt-load boundaries, response
conventions, and routing rules that every Farplane coding agent must inherit.

## What Belongs Elsewhere

Detailed workflows belong in skills; product capability contracts belong in feature
specs; task-local state belongs in tickets; generated checks belong in validators.

## Operating Contract

- Keep always-loaded policy lean and navigational.
- Route detailed procedures to the smallest durable owner.
- Preserve feedback-first planning for materially branching design choices.
- Require local context and proof before implementation completion claims.
- Feature-level behavior belongs in `docs/features/FEAT-*.md`; this page owns the system boundary and feature grouping.
- Registry data is generated from system and feature docs, not edited by hand.
- When a capability no longer deserves a feature page, fold its current truth into the best owner and remove active refs.

## Surfaces

- `AGENTS.md`
- `templates/global/AGENTS.md`
- `docs/fundamentals/harness-engineering-doctrine.md`

## Proof And Maintenance

- Registry proof: `python3 docs/features/validate_features.py`.
- Link proof: `python3 bin/validators/check_doc_refs.py`.
- Update this system page when product-layer boundaries or feature membership changes.
- Update feature pages when capability behavior changes.
- Regenerate registries and commit generated outputs with the source docs.

## Change History

- 2026-06-27: Migrated into the reader-first system-spec shape.
