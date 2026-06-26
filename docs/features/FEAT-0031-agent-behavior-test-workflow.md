---
title: "Agent behavior test workflow"
status: implemented
owner: feature-registry
created_at: 2026-06-26
updated_at: 2026-06-26
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

## Owned Behavior

This feature owns the behavior implemented, specified, or enforced by its owner surfaces. Keep the details in those surfaces; keep this page focused on the stable feature contract and registry metadata.

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
