---
title: "Agent Kernel"
status: active
owner: farplane-framework
created_at: 2026-06-26
updated_at: 2026-06-26
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

The installed agent context, templates, prompt rules, and response conventions that let a Codex enter Farplane with the right operating shape.

## Role

Agent Kernel is the always-loaded operating layer: global prompt shape, local project AGENTS routing, response conventions, and the rule that detailed behavior belongs in smaller owned surfaces.

## What Belongs Here

Global and project agent instructions, prompt-load boundaries, response contracts, and high-level routing defaults.

## What Belongs Elsewhere

Domain workflows, skill procedures, proof rubrics, runtime hooks, and ticket-local plans belong in their owning docs or skills.

## Feature Docs

- [FEAT-0042 Lean global agent operating kernel](../features/FEAT-0042-lean-global-agent-operating-kernel.md)

## Maintenance

This system page owns only the system-level contract. Feature registry rows are authored as feature pages in `docs/features/` and generated into `docs/features/registry.jsonl`.
