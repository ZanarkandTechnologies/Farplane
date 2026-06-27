---
title: Lean global agent operating kernel
status: implemented
owner: feature-registry
created_at: 2026-06-26
updated_at: 2026-06-27
tags:
  - farplane
  - feature
  - sys-0001
refs:
  - templates/global/AGENTS.md
  - skills/init-advisor/references/AGENTS_TEMPLATE.md
  - ARCHITECTURE.md
  - docs/fundamentals/harness-engineering-doctrine.md
  - docs/HISTORY.md
feature_id: FEAT-0042
system_id: SYS-0001
category: context-routing
public: true
surfaces:
  - templates/global/AGENTS.md
  - skills/init-advisor/references/AGENTS_TEMPLATE.md
  - ARCHITECTURE.md
source_refs:
  - docs/fundamentals/harness-engineering-doctrine.md
  - docs/HISTORY.md
external_refs: []
evidence_refs:
  - templates/global/AGENTS.md
  - skills/init-advisor/references/AGENTS_TEMPLATE.md
  - docs/HISTORY.md
known_limits: The global template now owns only every-turn behavior; project-specific coding defaults and detailed workflows must keep living in project AGENTS files, skills, tickets, docs, validators, or subagent prompts.
metrics: []
last_verified: 2026-06-07
---
# Lean global agent operating kernel

Lean global agent operating kernel exists to keep always-loaded agent policy small,
actionable, and routed to durable owner surfaces. It belongs to [Agent
Kernel](../systems/agent-kernel.md) and keeps `FEAT-0042` as a stable capability handle
because the behavior has an owner, proof path, and maintenance boundary.

```text
load_agent_context(repo, task) -> lean_kernel + routed_skill_context + proof_rules
```

## At A Glance

- Feature ID: `FEAT-0042`
- System: [Agent Kernel](../systems/agent-kernel.md)
- Status: `implemented`
- Category: `context-routing`
- Primary user: every Farplane coding agent
- Job: keep always-loaded agent policy small, actionable, and routed to durable owner surfaces.

## Problem

A powerful harness can collapse under its own prompt weight if every rule lives in
global context.

This feature keeps the global and project agent files as a lean operating kernel while
skills, specs, tickets, validators, and docs own the detailed procedures.

## What It Does

- Defines autonomy, action mode, reading, verification, and communication defaults.
- Routes detailed procedures into skills, tickets, specs, docs, hooks, or validators.
- Keeps Farplane-native identity in active repo-owned prompts and templates.
- Treats low-confidence design language as plan-first until a ticket or explicit implementation request exists.
- Requires local project context before edits and proof before completion claims.

## User Stories

- As an agent, I can enter Farplane with the right operating shape without loading every procedure.
- As a maintainer, I can move detailed rules into the right owner instead of bloating AGENTS.md.
- As an operator, I get momentum without silent architectural drift.

## Operating Contract

The agent kernel is a router and behavioral floor, not the full operating manual.

- Global and project AGENTS files stay navigational and policy-light.
- Detailed procedures live in skills, specs, tickets, docs, hooks, or validators.
- Material design choices remain feedback-first unless a ticket, spec, or explicit request owns the scope.
- Implementation work verifies before claiming completion.

## Surfaces

Owner surfaces:

- `templates/global/AGENTS.md`
- `skills/init-advisor/references/AGENTS_TEMPLATE.md`
- `ARCHITECTURE.md`

Source context:

- `docs/fundamentals/harness-engineering-doctrine.md`
- `docs/HISTORY.md`

Evidence:

- `templates/global/AGENTS.md`
- `skills/init-advisor/references/AGENTS_TEMPLATE.md`
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
- Maintenance owner: Agent Kernel.

## Limits And Non-Goals

- This feature does not paste every skill instruction into AGENTS.md.
- This feature does not override project-local ticket contracts.
- This feature does not replace skill loading.
- Known limit: The global template now owns only every-turn behavior; project-specific coding defaults and detailed workflows must keep living in project AGENTS files, skills, tickets, docs, validators, or subagent prompts.
- Delete or merge this feature only when its current truth has moved into a clearer owner and all active refs are removed.

## Metrics

- no dedicated metric yet

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
