---
title: "Goal Packet architecture for native Codex goals"
status: implemented
owner: feature-registry
created_at: 2026-06-26
updated_at: 2026-06-26
tags:
  - farplane
  - feature
  - sys-0003
refs:
  - docs/specs/goal-loop-contract.md
  - skills/goal-advisor
  - skills/horizon-advisor
  - farplane/goals.md
  - tickets/templates/goal-loop/program.md
  - tickets/templates/goal-loop/progress.md
  - agents/goal-drift-reviewer.toml
  - docs/specs/harness-techniques.md
  - README.md
  - https://developers.openai.com/cookbook/examples/codex/using_goals_in_codex
  - docs/HISTORY.md
  - tickets/TASK-0193/ticket.md
feature_record_json: |
  {
    "id": "FEAT-0029",
    "name": "Goal Packet architecture for native Codex goals",
    "status": "implemented",
    "system_id": "SYS-0003",
    "category": "planning",
    "public": true,
    "surfaces": [
      "docs/specs/goal-loop-contract.md",
      "skills/goal-advisor",
      "skills/horizon-advisor",
      "farplane/goals.md",
      "tickets/templates/goal-loop/program.md",
      "tickets/templates/goal-loop/progress.md",
      "agents/goal-drift-reviewer.toml",
      "docs/specs/harness-techniques.md",
      "README.md"
    ],
    "source_refs": [
      "https://developers.openai.com/cookbook/examples/codex/using_goals_in_codex",
      "docs/specs/goal-loop-contract.md"
    ],
    "external_refs": [
      "https://developers.openai.com/codex/use-cases/follow-goals"
    ],
    "evidence_refs": [
      "docs/HISTORY.md",
      "tickets/TASK-0193/ticket.md"
    ],
    "known_limits": "Contract, template, skill, and agent prompt surfaces only. Native Codex Goal mode owns leaf continuation; parent project-goals orchestration is heartbeat/manual-resume state selection. Farplane does not ship a hidden loop runtime, scheduler, automatic Goal manager, or Notion sync. End-to-end live project-goals heartbeat still needs a post-contract pilot.",
    "metrics": [
      "goal_packet_reconstructability",
      "drift_review_alignment_pass",
      "project_goals_parent_leaf_boundary_pass"
    ],
    "last_verified": "2026-06-12"
  }
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

## Owned Behavior

This feature owns the behavior implemented, specified, or enforced by its owner surfaces. Keep the details in those surfaces; keep this page focused on the stable feature contract and registry metadata.

## Owner Surfaces

- `docs/specs/goal-loop-contract.md`
- `skills/goal-advisor`
- `skills/horizon-advisor`
- `farplane/goals.md`
- `tickets/templates/goal-loop/program.md`
- `tickets/templates/goal-loop/progress.md`
- `agents/goal-drift-reviewer.toml`
- `docs/specs/harness-techniques.md`
- `README.md`

## Source Context

- `https://developers.openai.com/cookbook/examples/codex/using_goals_in_codex`
- `docs/specs/goal-loop-contract.md`

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
