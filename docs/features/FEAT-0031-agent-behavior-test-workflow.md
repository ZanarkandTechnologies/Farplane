---
title: "Agent behavior test workflow"
status: implemented
owner: feature-registry
created_at: 2026-06-26
updated_at: 2026-06-27
tags:
  - farplane
  - feature
  - sys-0005
refs:
  - skills/agent-behavior-test
  - skills/agent-behavior-test/scripts/run_codex_exec_behavior_test.py
  - docs/skills/registry.jsonl
  - docs/fundamentals/harness-engineering-doctrine.md
  - skills/harness-advisor/references/placement-axes.md
  - skills/agent-behavior-test/references/codex-exec-runner.md
  - docs/HISTORY.md
feature_record_json: |
  {
    "id": "FEAT-0031",
    "name": "Agent behavior test workflow",
    "status": "implemented",
    "system_id": "SYS-0005",
    "category": "proof",
    "public": true,
    "surfaces": [
      "skills/agent-behavior-test",
      "skills/agent-behavior-test/scripts/run_codex_exec_behavior_test.py",
      "docs/skills/registry.jsonl"
    ],
    "source_refs": [
      "docs/fundamentals/harness-engineering-doctrine.md",
      "skills/harness-advisor/references/placement-axes.md"
    ],
    "external_refs": [],
    "evidence_refs": [
      "skills/agent-behavior-test/references/codex-exec-runner.md",
      "skills/agent-behavior-test/scripts/run_codex_exec_behavior_test.py",
      "docs/HISTORY.md"
    ],
    "known_limits": "CLI JSONL runs capture visible messages, command events, final output, and usage, but not hidden chain-of-thought. Native subagent testing still depends on the subagent writing its own report artifact.",
    "metrics": [
      "agent_behavior_test_runner_smoke_pass"
    ],
    "last_verified": "2026-05-25"
  }
---

# Agent behavior test workflow

Agent behavior test workflow is a first-class Farplane feature in [Proof And Review](../systems/proof-review.md). It survives as a `FEAT-*` handle because it has owner surfaces, evidence, limits, and a maintenance path.

```text
feature(FEAT-0031, repo_state?) -> behavior + evidence + maintenance_signal
```

## System

- System: [Proof And Review](../systems/proof-review.md)
- Feature ID: `FEAT-0031`
- Status: `implemented`
- Category: `proof`

## Feature Spec

This feature owns isolated behavior probes for agents, prompts, skills, and workflow claims. It folds the agent-testability surface contract into the behavior-test workflow.

```text
behavior_test(claim, controls, state_probe, evidence_path) -> scored_run_report
```

A testable agent workflow should expose:

- control accelerators: fixtures, deterministic inputs, shortcuts, seeded state, or bounded prompts that make the behavior reachable;
- state probes: logs, artifacts, DOM snapshots, command outputs, ticket state, generated files, or structured reports;
- coordination views: visible ownership boundaries, handoff packets, and progress surfaces for multi-agent behavior.

Agent Testability Briefs should name the behavior claim, setup state, control move, observable state, failure mode, evidence path, and expected report shape.

Non-goal: this feature does not replace product QA. It captures one representative agent behavior with enough structure to learn from it.

Proof gates:

- The run can be inspected after the fact.
- The score is tied to evidence, not vibes.
- Any hardcase can be promoted to an eval, QA checklist, skill patch, or follow-up ticket.

## Owner Surfaces

- `skills/agent-behavior-test`
- `skills/agent-behavior-test/scripts/run_codex_exec_behavior_test.py`
- `docs/skills/registry.jsonl`

## Source Context

- `docs/fundamentals/harness-engineering-doctrine.md`
- `skills/harness-advisor/references/placement-axes.md`

## Evidence

- `skills/agent-behavior-test/references/codex-exec-runner.md`
- `skills/agent-behavior-test/scripts/run_codex_exec_behavior_test.py`
- `docs/HISTORY.md`

## Known Limits

CLI JSONL runs capture visible messages, command events, final output, and usage, but not hidden chain-of-thought. Native subagent testing still depends on the subagent writing its own report artifact.

## Metrics

- `agent_behavior_test_runner_smoke_pass`

## Maintenance

Update this feature doc before regenerating `docs/features/registry.jsonl`. If the feature stops deserving its own doc, delete this file and remove all active template, source, ticket, and system refs to `FEAT-0031`.
