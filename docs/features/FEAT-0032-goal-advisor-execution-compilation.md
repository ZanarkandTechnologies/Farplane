---
title: Goal Advisor execution compilation
status: implemented
owner: feature-registry
created_at: 2026-06-26
updated_at: 2026-06-26
tags:
  - farplane
  - feature
  - sys-0003
refs:
  - skills/goal-advisor
  - docs/features/FEAT-0029-goal-packet-architecture-for-native-codex-goals.md
  - docs/features/FEAT-0015-symphony-compatible-farplane-invocation-contract.md
  - docs/features/FEAT-0007-ticket-as-durable-task-memory.md
  - tickets/templates/goal-loop/program.md
  - tickets/archive/TASK-0196/ticket.md
  - skills/goal-advisor/SKILL.md
  - docs/HISTORY.md
feature_id: FEAT-0032
system_id: SYS-0003
category: execution
public: true
surfaces:
  - skills/goal-advisor
  - docs/features/FEAT-0029-goal-packet-architecture-for-native-codex-goals.md
  - docs/features/FEAT-0015-symphony-compatible-farplane-invocation-contract.md
  - docs/features/FEAT-0007-ticket-as-durable-task-memory.md
  - tickets/templates/goal-loop/program.md
source_refs:
  - skills/goal-advisor
  - docs/features/FEAT-0029-goal-packet-architecture-for-native-codex-goals.md
  - docs/features/FEAT-0015-symphony-compatible-farplane-invocation-contract.md
  - tickets/archive/TASK-0196/ticket.md
external_refs:
  - https://developers.openai.com/codex/use-cases/follow-goals
evidence_refs:
  - skills/goal-advisor/SKILL.md
  - docs/HISTORY.md
  - tickets/archive/TASK-0196/ticket.md
known_limits: Skill and docs contract only; it does not implement a daemon, hidden scheduler, Codex Cloud launcher, Symphony runner, or automatic Goal manager. Former work, Ralph, and batch-work public skill surfaces are retired into Goal standards.
metrics: []
last_verified: 2026-06-13
---
# Goal Advisor execution compilation

Goal Advisor execution compilation is a first-class Farplane feature in [Horizon Loop](../systems/horizon-loop.md). It survives as a `FEAT-*` handle because it has owner surfaces, evidence, limits, and a maintenance path.

```text
feature(FEAT-0032, repo_state?) -> behavior + evidence + maintenance_signal
```

## System

- System: [Horizon Loop](../systems/horizon-loop.md)
- Feature ID: `FEAT-0032`
- Status: `implemented`
- Category: `execution`

## Owned Behavior

This feature owns the behavior implemented, specified, or enforced by its owner surfaces. Keep the details in those surfaces; keep this page focused on the stable feature contract and registry metadata.

## Owner Surfaces

- `skills/goal-advisor`
- `docs/features/FEAT-0029-goal-packet-architecture-for-native-codex-goals.md`
- `docs/features/FEAT-0015-symphony-compatible-farplane-invocation-contract.md`
- `docs/features/FEAT-0007-ticket-as-durable-task-memory.md`
- `tickets/templates/goal-loop/program.md`

## Source Context

- `skills/goal-advisor`
- `docs/features/FEAT-0029-goal-packet-architecture-for-native-codex-goals.md`
- `docs/features/FEAT-0015-symphony-compatible-farplane-invocation-contract.md`
- `tickets/archive/TASK-0196/ticket.md`

## Evidence

- `skills/goal-advisor/SKILL.md`
- `docs/HISTORY.md`
- `tickets/archive/TASK-0196/ticket.md`

## Known Limits

Skill and docs contract only; it does not implement a daemon, hidden scheduler, Codex Cloud launcher, Symphony runner, or automatic Goal manager. Former work, Ralph, and batch-work public skill surfaces are retired into Goal standards.

## Metrics

- no dedicated metric yet

## Maintenance

Update this feature doc before regenerating `docs/features/registry.jsonl`. If the feature stops deserving its own doc, delete this file and remove all active template, source, ticket, and system refs to `FEAT-0032`.
