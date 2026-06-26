---
title: "Horizon Loop"
status: active
owner: farplane-framework
created_at: 2026-06-26
updated_at: 2026-06-26
tags:
  - farplane
  - systems
  - horizon-loop
refs:
  - docs/specs/goal-loop-contract.md
  - docs/specs/minimal-autonomy-loop.md
  - docs/specs/steer-pulse-automation.md
  - docs/specs/nested-pm-projects.md
system_record_json: |
  {
    "id": "SYS-0003",
    "name": "Horizon Loop",
    "status": "implemented",
    "summary": "The longer-running project loop that coordinates goals, Goal Packets, Pulse, Interval, backoff, PR watching, feedback, and horizon-level ticket supply.",
    "owner_spec": "docs/systems/horizon-loop.md",
    "primary_feature_ref": "FEAT-0029",
    "feature_refs": [
      "FEAT-0029",
      "FEAT-0009",
      "FEAT-0021",
      "FEAT-0032",
      "FEAT-0036",
      "FEAT-0038",
      "FEAT-0046"
    ],
    "refs": [
      "docs/specs/goal-loop-contract.md",
      "docs/specs/minimal-autonomy-loop.md",
      "docs/specs/steer-pulse-automation.md",
      "docs/specs/nested-pm-projects.md"
    ],
    "last_verified": "2026-06-26"
  }
capability_records_json: |
  [
    {
      "id": "FEAT-0029",
      "name": "Goal Packet architecture for native Codex goals",
      "status": "implemented",
      "category": "planning",
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
      "last_verified": "2026-06-12",
      "capability_role": "primary",
      "public": true
    },
    {
      "id": "FEAT-0009",
      "name": "Goal heartbeat board draining",
      "status": "implemented",
      "category": "execution",
      "surfaces": [
        "skills/goal-advisor",
        "docs/specs/goal-loop-contract.md",
        "docs/specs/spec-first-execution-loop.md"
      ],
      "source_refs": [
        "docs/MEMORY.md#MEM-0074",
        "docs/HISTORY.md",
        "tickets/archive/TASK-0196/ticket.md"
      ],
      "external_refs": [],
      "evidence_refs": [
        "docs/HISTORY.md",
        "tickets/archive/TASK-0196/ticket.md"
      ],
      "known_limits": "Board drain is now a Goal heartbeat pattern, not a public Ralph skill or hidden dispatcher. Parallel leases, worktrees, merge queue, stale-worker recovery, and batch QA remain future work.",
      "metrics": [],
      "last_verified": "2026-06-13",
      "capability_role": "subcapability",
      "public": false
    },
    {
      "id": "FEAT-0021",
      "name": "Parallel board-drain design contract",
      "status": "retired",
      "category": "execution",
      "surfaces": [
        "docs/specs/invocation-and-adapters.md",
        "docs/specs/goal-loop-contract.md"
      ],
      "source_refs": [
        "SRC-0001",
        "docs/MEMORY.md#MEM-0074",
        "docs/specs/invocation-and-adapters.md"
      ],
      "external_refs": [
        "Symphony Service Specification draft v1"
      ],
      "evidence_refs": [
        "tickets/archive/TASK-0115/ticket.md",
        "tickets/archive/TASK-0115/artifacts/review/2026-05-05-impl-review.json",
        "tickets/archive/TASK-0196/ticket.md"
      ],
      "known_limits": "Former parallel Ralph design was retired with the Ralph public skill. Future parallel board drain must be redesigned as a Goal heartbeat pattern with leases, worktrees, merge policy, stale-worker recovery, and batch QA before implementation.",
      "metrics": [
        "parallel_design_traceability",
        "hidden_parallel_runtime_count"
      ],
      "last_verified": "2026-06-13",
      "capability_role": "retired",
      "public": false
    },
    {
      "id": "FEAT-0032",
      "name": "Goal Advisor execution compilation",
      "status": "implemented",
      "category": "execution",
      "surfaces": [
        "skills/goal-advisor",
        "docs/specs/goal-loop-contract.md",
        "docs/specs/invocation-and-adapters.md",
        "docs/specs/spec-first-execution-loop.md",
        "tickets/templates/goal-loop/program.md"
      ],
      "source_refs": [
        "skills/goal-advisor",
        "docs/specs/goal-loop-contract.md",
        "docs/specs/invocation-and-adapters.md",
        "tickets/archive/TASK-0196/ticket.md"
      ],
      "external_refs": [
        "https://developers.openai.com/codex/use-cases/follow-goals"
      ],
      "evidence_refs": [
        "skills/goal-advisor/SKILL.md",
        "docs/HISTORY.md",
        "tickets/archive/TASK-0196/ticket.md"
      ],
      "known_limits": "Skill and docs contract only; it does not implement a daemon, hidden scheduler, Codex Cloud launcher, Symphony runner, or automatic Goal manager. Former work, Ralph, and batch-work public skill surfaces are retired into Goal standards.",
      "metrics": [],
      "last_verified": "2026-06-13",
      "capability_role": "subcapability",
      "public": false
    },
    {
      "id": "FEAT-0036",
      "name": "Explicit PR review watcher workflow",
      "status": "implemented",
      "category": "execution",
      "surfaces": [
        "skills/pr-review-watch",
        "skills/pr-review-watch/scripts/pr_review_watch.py",
        "docs/skills/registry.jsonl"
      ],
      "source_refs": [
        "tickets/archive/TASK-0187/ticket.md",
        "docs/fundamentals/harness-engineering-doctrine.md"
      ],
      "external_refs": [],
      "evidence_refs": [
        "skills/pr-review-watch/scripts/test_pr_review_watch.py",
        "tickets/archive/TASK-0187/ticket.md",
        "docs/HISTORY.md"
      ],
      "known_limits": "GitHub/gh-oriented first slice with fixture-first proof; no hidden daemon, cloud scheduler, automatic push/merge/deploy, or broad multi-provider live integration matrix. The owned implementation lives with the skill package; the old top-level bin wrapper was removed in TASK-0218.",
      "metrics": [
        "pr_review_watch_fixture_states_pass"
      ],
      "last_verified": "2026-06-24",
      "capability_role": "subcapability",
      "public": false
    },
    {
      "id": "FEAT-0038",
      "name": "Adaptive backoff operating policy",
      "status": "implemented",
      "category": "execution",
      "surfaces": [
        "templates/global/AGENTS.md",
        "docs/specs/adaptive-backoff.md",
        "skills/pr-review-watch",
        "skills/video-generation/references/long-running-jobs.md",
        "skills/remotion-render/AGENTS.md"
      ],
      "source_refs": [
        "docs/MEMORY.md#MEM-0130",
        "docs/specs/adaptive-backoff.md"
      ],
      "external_refs": [
        "https://datatracker.ietf.org/doc/rfc9110/"
      ],
      "evidence_refs": [
        "docs/HISTORY.md"
      ],
      "known_limits": "Policy and skill guidance only; deterministic script adoption remains per-caller and this feature must not become a hidden daemon, queue, scheduler, or automatic retry loop.",
      "metrics": [],
      "last_verified": "2026-06-02",
      "capability_role": "subcapability",
      "public": false
    },
    {
      "id": "FEAT-0046",
      "name": "Goal algebra with feedback and agent QA providers",
      "status": "implemented",
      "category": "planning",
      "surfaces": [
        "skills/goal-advisor",
        "skills/optimize-with-human",
        "skills/agent-qa-test",
        "skills/telegram-message",
        "docs/skills/registry.jsonl"
      ],
      "source_refs": [
        "skills/goal-advisor/SKILL.md",
        "skills/optimize-with-human/SKILL.md",
        "skills/agent-qa-test/SKILL.md",
        "skills/telegram-message/SKILL.md",
        "docs/features/registry.jsonl#FEAT-0029",
        "docs/features/registry.jsonl#FEAT-0034"
      ],
      "external_refs": [],
      "evidence_refs": [
        "docs/HISTORY.md"
      ],
      "known_limits": "Skill-contract composition only. Native Goal mode owns continuation; human feedback through optimize-with-human requires a human-authored feedback file or configured notification path, and agent QA execution depends on available subagent/runtime tools.",
      "metrics": [
        "goal_algebra_skill_validation_pass"
      ],
      "last_verified": "2026-06-12",
      "capability_role": "subcapability",
      "public": false
    }
  ]
---

# Horizon Loop

The longer-running project loop that coordinates goals, Goal Packets, Pulse, Interval, backoff, PR watching, feedback, and horizon-level ticket supply.

## Role

This system spec is the authored source for one public Farplane system and its internal capability handles. The generated registries expose the same data as `docs/systems/registry.jsonl` and `docs/features/registry.jsonl`.

## Public Capability

- `FEAT-0029` - Goal Packet architecture for native Codex goals

## Capability Handles

- `FEAT-0029` `primary` - Goal Packet architecture for native Codex goals
- `FEAT-0009` `subcapability` - Goal heartbeat board draining
- `FEAT-0021` `retired` - Parallel board-drain design contract
- `FEAT-0032` `subcapability` - Goal Advisor execution compilation
- `FEAT-0036` `subcapability` - Explicit PR review watcher workflow
- `FEAT-0038` `subcapability` - Adaptive backoff operating policy
- `FEAT-0046` `subcapability` - Goal algebra with feedback and agent QA providers

## Maintenance Notes

- Edit the `system_record_json` and `capability_records_json` blocks in this file, then run `python3 docs/features/validate_features.py --write`.
- Keep public docs focused on the system and primary capability; use subcapability rows for compatibility, dedupe, rollout, and evidence tracking.
