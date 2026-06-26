---
title: "Project-level system prompt eval suite"
status: implemented
owner: feature-registry
created_at: 2026-06-26
updated_at: 2026-06-26
tags:
  - farplane
  - feature
  - sys-0005
refs:
  - skills/eval/examples/farplane-global-harness/tasks.json
  - skills/eval
  - templates/global/AGENTS.md
  - skills/eval/references/eval-best-practices.md
  - docs/HISTORY.md
  - skills/eval/tests/test_run_evals.py
feature_record_json: |
  {
    "id": "FEAT-0043",
    "name": "Project-level system prompt eval suite",
    "status": "implemented",
    "system_id": "SYS-0005",
    "category": "proof",
    "public": true,
    "surfaces": [
      "skills/eval/examples/farplane-global-harness/tasks.json",
      "skills/eval",
      "templates/global/AGENTS.md"
    ],
    "source_refs": [
      "skills/eval/references/eval-best-practices.md",
      "docs/HISTORY.md"
    ],
    "external_refs": [],
    "evidence_refs": [
      "skills/eval/examples/farplane-global-harness/tasks.json",
      "skills/eval/tests/test_run_evals.py",
      "docs/HISTORY.md"
    ],
    "known_limits": "The current runner judges final answers and task artifacts, not full hidden reasoning or complete live tool-event traces. Behavior claims that need child-agent command logs should use agent-behavior-test or agent-qa-test.",
    "metrics": [
      "system_prompt_eval_pass_rate"
    ],
    "last_verified": "2026-06-07"
  }
---

# Project-level system prompt eval suite

Project-level system prompt eval suite is a first-class Farplane feature in [Proof And Review](../systems/proof-review.md). It survives as a `FEAT-*` handle because it has owner surfaces, evidence, limits, and a maintenance path.

```text
feature(FEAT-0043, repo_state?) -> behavior + evidence + maintenance_signal
```

## System

- System: [Proof And Review](../systems/proof-review.md)
- Feature ID: `FEAT-0043`
- Status: `implemented`
- Category: `proof`

## Owned Behavior

This feature owns the behavior implemented, specified, or enforced by its owner surfaces. Keep the details in those surfaces; keep this page focused on the stable feature contract and registry metadata.

## Owner Surfaces

- `skills/eval/examples/farplane-global-harness/tasks.json`
- `skills/eval`
- `templates/global/AGENTS.md`

## Source Context

- `skills/eval/references/eval-best-practices.md`
- `docs/HISTORY.md`

## Evidence

- `skills/eval/examples/farplane-global-harness/tasks.json`
- `skills/eval/tests/test_run_evals.py`
- `docs/HISTORY.md`

## Known Limits

The current runner judges final answers and task artifacts, not full hidden reasoning or complete live tool-event traces. Behavior claims that need child-agent command logs should use agent-behavior-test or agent-qa-test.

## Metrics

- `system_prompt_eval_pass_rate`

## Maintenance

Update this feature doc before regenerating `docs/features/registry.jsonl`. If the feature stops deserving its own doc, delete this file and remove all active template, source, ticket, and system refs to `FEAT-0043`.
