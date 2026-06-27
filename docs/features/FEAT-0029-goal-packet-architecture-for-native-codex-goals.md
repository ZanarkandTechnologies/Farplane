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

Goal Packet architecture for native Codex goals exists to wrap native Codex Goal mode
with visible ticket, program, and progress state. It belongs to [Horizon
Loop](../systems/horizon-loop.md) and keeps `FEAT-0029` as a stable capability handle
because the behavior has an owner, proof path, and maintenance boundary.

```text
goal_packet(ticket, program, progress) -> native_goal_prompt + resume_contract
```

## At A Glance

- Feature ID: `FEAT-0029`
- System: [Horizon Loop](../systems/horizon-loop.md)
- Status: `implemented`
- Category: `planning`
- Primary user: operator and long-running coding agent
- Job: wrap native Codex Goal mode with visible ticket, program, and progress state.

## Problem

Native Goal mode can keep working across continuations, but Farplane still needs
filesystem truth for scope, proof, blockers, and handoff.

Goal Packets solve that by making the native goal prompt a compiled instruction, not the
durable source of truth.

## What It Does

- Attaches a material goal to a ticket.
- Uses `ticket.md` as the task contract, `program.md` as loop configuration, and `progress.md` as append-only turn log.
- Compiles a native Goal prompt from those files.
- Keeps proof obligations in the ticket and artifacts rather than in hidden goal memory.
- Lets agents resume or review a goal by reading the packet files.

## User Stories

- As an operator, I can start a long task without losing control of proof and scope.
- As a resumed agent, I can recover the goal state from files.
- As a reviewer, I can compare progress against the ticket and program.

## Operating Contract

Goal mode is the continuation engine; the Goal Packet is the visible Farplane state
around it.

- Every material Goal attaches to an active ticket or creates one.
- `program.md` holds loop settings and continuation guidance.
- `progress.md` records append-only turn updates.
- The native Goal prompt is regenerated from packet state when needed.
- Completion still requires ticket proof gates and review when required.

## Surfaces

Owner surfaces:

- `docs/features/FEAT-0029-goal-packet-architecture-for-native-codex-goals.md`
- `skills/goal-advisor`
- `skills/horizon-advisor`
- `farplane/goals.md`
- `tickets/templates/goal-loop/program.md`
- `tickets/templates/goal-loop/progress.md`
- `agents/goal-drift-reviewer.toml`
- `docs/features/README.md`
- `README.md`

Source context:

- `https://developers.openai.com/cookbook/examples/codex/using_goals_in_codex`
- `docs/features/FEAT-0029-goal-packet-architecture-for-native-codex-goals.md`

External context:

- `https://developers.openai.com/codex/use-cases/follow-goals`

Evidence:

- `docs/HISTORY.md`
- `tickets/TASK-0193/ticket.md`

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
- Maintenance owner: Horizon Loop.

## Limits And Non-Goals

- This feature does not make Goal mode the source of truth.
- This feature does not bypass tickets for material work.
- This feature does not hide blockers or proof in the continuation prompt.
- Known limit: Contract, template, skill, and agent prompt surfaces only. Native Codex Goal mode owns leaf continuation; parent project-goals orchestration is heartbeat/manual-resume state selection. Farplane does not ship a hidden loop runtime, scheduler, automatic Goal manager, or Notion sync. End-to-end live project-goals heartbeat still needs a post-contract pilot.
- Delete or merge this feature only when its current truth has moved into a clearer owner and all active refs are removed.

## Metrics

- `goal_packet_reconstructability`
- `drift_review_alignment_pass`
- `project_goals_parent_leaf_boundary_pass`

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
