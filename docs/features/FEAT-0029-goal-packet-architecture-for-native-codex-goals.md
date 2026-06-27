---
title: Goal Packet architecture for native Codex goals
status: implemented
owner: feature-registry
created_at: 2026-06-26
updated_at: 2026-06-27
tags:
  - farplane
  - feature
  - sys-0003
refs:
  - docs/features/FEAT-0029-goal-packet-architecture-for-native-codex-goals.md
  - skills/goal-advisor
  - skills/horizon-advisor
  - farplane/goals.md
  - tickets/templates/goal-loop/program.md
  - tickets/templates/goal-loop/progress.md
  - agents/goal-drift-reviewer.toml
  - docs/features/README.md
  - README.md
  - https://developers.openai.com/cookbook/examples/codex/using_goals_in_codex
  - docs/HISTORY.md
  - tickets/TASK-0193/ticket.md
feature_id: FEAT-0029
system_id: SYS-0003
category: planning
public: true
surfaces:
  - docs/features/FEAT-0029-goal-packet-architecture-for-native-codex-goals.md
  - skills/goal-advisor
  - skills/horizon-advisor
  - farplane/goals.md
  - tickets/templates/goal-loop/program.md
  - tickets/templates/goal-loop/progress.md
  - agents/goal-drift-reviewer.toml
  - docs/features/README.md
  - README.md
source_refs:
  - https://developers.openai.com/cookbook/examples/codex/using_goals_in_codex
  - docs/features/FEAT-0029-goal-packet-architecture-for-native-codex-goals.md
external_refs:
  - https://developers.openai.com/codex/use-cases/follow-goals
evidence_refs:
  - docs/HISTORY.md
  - tickets/TASK-0193/ticket.md
known_limits: Contract, template, skill, and agent prompt surfaces only. Native Codex Goal mode owns leaf continuation; parent project-goals orchestration is heartbeat/manual-resume state selection. Farplane does not ship a hidden loop runtime, scheduler, automatic Goal manager, or Notion sync. End-to-end live project-goals heartbeat still needs a post-contract pilot.
metrics:
  - goal_packet_reconstructability
  - drift_review_alignment_pass
  - project_goals_parent_leaf_boundary_pass
last_verified: 2026-06-12
---
# Goal Packet architecture for native Codex goals

Goal Packet architecture for native Codex goals is a first-class Farplane feature in [Horizon Loop](../systems/horizon-loop.md). It survives as a `FEAT-*` handle because it has owner surfaces, evidence, limits, and a maintenance path.

```text
feature(FEAT-0029, repo_state?) -> behavior + evidence + maintenance_signal
```

## System

- System: [Horizon Loop](../systems/horizon-loop.md)
- Feature ID: `FEAT-0029`
- Status: `implemented`
- Category: `planning`

## Feature Spec

This feature owns long-horizon Goal Packets: the visible state around native Codex Goals, parent project goals, program notation, nested PM projects, and continuation policy.

```text
goal_packet(ticket, program, progress, horizon_state?) -> native_goal_prompt + drift_review_surface
```

The folded contract combines the former goal-loop, program-notation, and nested-PM specs:

- `ticket.md` remains the task contract and proof scoreboard.
- `program.md` stores loop configuration: trigger mode, skills, gates, budget, evidence, metrics, and handoff rules.
- `progress.md` is append-only turn memory for resumability and drift checks.
- `farplane/goals.md` or a project-level horizon file stores parent goals and ticket supply signals.
- Native Codex Goal mode owns leaf continuation; Farplane owns visible state, packet compilation, and proof routing around it.
- Parent/child PM projects only exist when a child loop has its own artifact stream, proof gates, and promotion rule.
- Program notation is a compact projection format, not a second runtime.

Non-goals:

- No hidden Goal manager.
- No automatic Notion sync.
- No one-PM-per-skill sprawl before a child project earns its own state and proof surface.

Proof gates:

- A Goal can resume from packet files without transcript context.
- Drift review can compare current work to the ticket/program/progress contract.
- Parent horizon updates create ticket supply or calibration changes, not vague strategy prose.

## Owner Surfaces

- `docs/features/FEAT-0029-goal-packet-architecture-for-native-codex-goals.md`
- `skills/goal-advisor`
- `skills/horizon-advisor`
- `farplane/goals.md`
- `tickets/templates/goal-loop/program.md`
- `tickets/templates/goal-loop/progress.md`
- `agents/goal-drift-reviewer.toml`
- `docs/features/README.md`
- `README.md`

## Source Context

- `https://developers.openai.com/cookbook/examples/codex/using_goals_in_codex`
- `docs/features/FEAT-0029-goal-packet-architecture-for-native-codex-goals.md`

## Evidence

- `docs/HISTORY.md`
- `tickets/TASK-0193/ticket.md`

## Known Limits

Contract, template, skill, and agent prompt surfaces only. Native Codex Goal mode owns leaf continuation; parent project-goals orchestration is heartbeat/manual-resume state selection. Farplane does not ship a hidden loop runtime, scheduler, automatic Goal manager, or Notion sync. End-to-end live project-goals heartbeat still needs a post-contract pilot.

## Metrics

- `goal_packet_reconstructability`
- `drift_review_alignment_pass`
- `project_goals_parent_leaf_boundary_pass`

## Maintenance

Update this feature doc before regenerating `docs/features/registry.jsonl`. If the feature stops deserving its own doc, delete this file and remove all active template, source, ticket, and system refs to `FEAT-0029`.
