---
title: Adversarial agent QA test skill
status: implemented
owner: feature-registry
created_at: 2026-06-26
updated_at: 2026-06-26
tags:
  - farplane
  - feature
  - sys-0005
refs:
  - skills/agent-qa-test
  - docs/skills/registry.jsonl
  - docs/fundamentals/harness-engineering-doctrine.md
  - "docs/features/registry.jsonl#FEAT-0031"
  - skills/agent-qa-test/SKILL.md
  - docs/HISTORY.md
feature_id: FEAT-0034
system_id: SYS-0005
category: proof
public: true
surfaces:
  - skills/agent-qa-test
  - docs/skills/registry.jsonl
source_refs:
  - docs/fundamentals/harness-engineering-doctrine.md
  - "docs/features/registry.jsonl#FEAT-0031"
external_refs: []
evidence_refs:
  - skills/agent-qa-test/SKILL.md
  - docs/HISTORY.md
known_limits: Skill and prompt-template surface only; actual native subagent execution still depends on the invoking agent and available runtime tools.
metrics:
  - agent_qa_test_skill_validation_pass
last_verified: 2026-05-26
---
# Adversarial agent QA test skill

Adversarial agent QA test skill is a first-class Farplane feature in [Proof And Review](../systems/proof-review.md). It survives as a `FEAT-*` handle because it has owner surfaces, evidence, limits, and a maintenance path.

```text
feature(FEAT-0034, repo_state?) -> behavior + evidence + maintenance_signal
```

## System

- System: [Proof And Review](../systems/proof-review.md)
- Feature ID: `FEAT-0034`
- Status: `implemented`
- Category: `proof`

## Owned Behavior

This feature owns the behavior implemented, specified, or enforced by its owner surfaces. Keep the details in those surfaces; keep this page focused on the stable feature contract and registry metadata.

## Owner Surfaces

- `skills/agent-qa-test`
- `docs/skills/registry.jsonl`

## Source Context

- `docs/fundamentals/harness-engineering-doctrine.md`
- `docs/features/registry.jsonl#FEAT-0031`

## Evidence

- `skills/agent-qa-test/SKILL.md`
- `docs/HISTORY.md`

## Known Limits

Skill and prompt-template surface only; actual native subagent execution still depends on the invoking agent and available runtime tools.

## Metrics

- `agent_qa_test_skill_validation_pass`

## Maintenance

Update this feature doc before regenerating `docs/features/registry.jsonl`. If the feature stops deserving its own doc, delete this file and remove all active template, source, ticket, and system refs to `FEAT-0034`.
