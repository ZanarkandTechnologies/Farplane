---
title: "Lean global agent operating kernel"
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
feature_record_json: |
  {
    "id": "FEAT-0042",
    "name": "Lean global agent operating kernel",
    "status": "implemented",
    "system_id": "SYS-0001",
    "category": "context-routing",
    "public": true,
    "surfaces": [
      "templates/global/AGENTS.md",
      "skills/init-advisor/references/AGENTS_TEMPLATE.md",
      "ARCHITECTURE.md"
    ],
    "source_refs": [
      "docs/fundamentals/harness-engineering-doctrine.md",
      "docs/HISTORY.md"
    ],
    "external_refs": [],
    "evidence_refs": [
      "templates/global/AGENTS.md",
      "skills/init-advisor/references/AGENTS_TEMPLATE.md",
      "docs/HISTORY.md"
    ],
    "known_limits": "The global template now owns only every-turn behavior; project-specific coding defaults and detailed workflows must keep living in project AGENTS files, skills, tickets, docs, validators, or subagent prompts.",
    "metrics": [],
    "last_verified": "2026-06-07"
  }
---

# Lean global agent operating kernel

Lean global agent operating kernel is a first-class Farplane feature in [Agent Kernel](../systems/agent-kernel.md). It survives as a `FEAT-*` handle because it has owner surfaces, evidence, limits, and a maintenance path.

```text
feature(FEAT-0042, repo_state?) -> behavior + evidence + maintenance_signal
```

## System

- System: [Agent Kernel](../systems/agent-kernel.md)
- Feature ID: `FEAT-0042`
- Status: `implemented`
- Category: `context-routing`

## Feature Spec

This feature owns the lean always-loaded operating kernel: how an agent decides, acts, communicates, and preserves durable state without bloating every prompt.

```text
agent_kernel(turn, repo_state, user_intent) -> act | plan | answer + durable_state_delta?
```

The first-principles planning contract folds into this feature:

- Start material decisions from objective, user/system need, root cause, constraints, assumptions, proof or falsification, tradeoffs, non-goals, and next action.
- Use three viable options when a real choice exists; recommend one and name the tradeoff.
- Treat low-confidence exploratory phrasing as a design signal unless an accepted ticket or explicit implementation request owns the scope.
- Promote only stable, reusable rules into always-loaded prompts. Move detailed procedures into skills, feature docs, tickets, validators, or owner surfaces.

Non-goal: the kernel is not the place for every workflow. It is the small decision loop that routes work to the right artifact.

Proof gates:

- The agent can explain why it acted, planned, or answered.
- Material choices name assumptions and proof needs.
- Durable policy is not duplicated into every surface.

## Owner Surfaces

- `templates/global/AGENTS.md`
- `skills/init-advisor/references/AGENTS_TEMPLATE.md`
- `ARCHITECTURE.md`

## Source Context

- `docs/fundamentals/harness-engineering-doctrine.md`
- `docs/HISTORY.md`

## Evidence

- `templates/global/AGENTS.md`
- `skills/init-advisor/references/AGENTS_TEMPLATE.md`
- `docs/HISTORY.md`

## Known Limits

The global template now owns only every-turn behavior; project-specific coding defaults and detailed workflows must keep living in project AGENTS files, skills, tickets, docs, validators, or subagent prompts.

## Metrics

- no dedicated metric yet

## Maintenance

Update this feature doc before regenerating `docs/features/registry.jsonl`. If the feature stops deserving its own doc, delete this file and remove all active template, source, ticket, and system refs to `FEAT-0042`.
