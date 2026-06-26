---
title: "Proof And Review"
status: active
owner: farplane-framework
created_at: 2026-06-26
updated_at: 2026-06-26
tags:
  - farplane
  - systems
  - proof-review
refs:
  - docs/specs/review-gates.md
  - skills/qa/SKILL.md
  - skills/review/SKILL.md
  - docs/review/rubrics
system_record_json: |
  {
    "id": "SYS-0005",
    "name": "Proof And Review",
    "status": "implemented",
    "summary": "The QA, review, completion, and adversarial testing surfaces that keep Farplane work evidence-backed instead of self-certified.",
    "owner_spec": "docs/systems/proof-review.md",
    "primary_feature_ref": "FEAT-0008",
    "feature_refs": [
      "FEAT-0008",
      "FEAT-0010",
      "FEAT-0031",
      "FEAT-0034",
      "FEAT-0043"
    ],
    "refs": [
      "docs/specs/review-gates.md",
      "skills/qa/SKILL.md",
      "skills/review/SKILL.md",
      "docs/review/rubrics"
    ],
    "last_verified": "2026-06-26"
  }
capability_records_json: |
  [
    {
      "id": "FEAT-0008",
      "name": "Artifact-first QA and completion proof",
      "status": "implemented",
      "category": "proof",
      "surfaces": [
        "tickets/README.md",
        "tickets/templates/ticket.md",
        "skills/qa",
        "skills/review",
        "docs/specs/review-gates.md"
      ],
      "source_refs": [
        "docs/MEMORY.md#MEM-0048",
        "docs/MEMORY.md#MEM-0064",
        "docs/MEMORY.md#MEM-0148"
      ],
      "external_refs": [],
      "evidence_refs": [
        "docs/HISTORY.md"
      ],
      "known_limits": "Depends on compact `Done / Proof` obligations plus linked artifacts, progress logs, and reviewer gates, not ticket-body proof theater.",
      "metrics": [],
      "last_verified": "2026-06-12",
      "capability_role": "primary",
      "public": true
    },
    {
      "id": "FEAT-0010",
      "name": "Stop-hook continuation and completion judgment",
      "status": "implemented",
      "category": "proof",
      "surfaces": [
        "hooks.json",
        "bin/stop_hook.py",
        "agents/completion-reviewer.toml",
        "docs/specs/review-gates.md"
      ],
      "source_refs": [
        "docs/MEMORY.md#MEM-0064",
        "docs/specs/harness-techniques.md"
      ],
      "external_refs": [],
      "evidence_refs": [
        "bin/tests/test_stop_hook.py",
        "docs/HISTORY.md"
      ],
      "known_limits": "Completion authority depends on visible review receipts and active ticket-backed impl loops.",
      "metrics": [],
      "last_verified": "2026-05-04",
      "capability_role": "subcapability",
      "public": false
    },
    {
      "id": "FEAT-0031",
      "name": "Agent behavior test workflow",
      "status": "implemented",
      "category": "proof",
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
      "last_verified": "2026-05-25",
      "capability_role": "subcapability",
      "public": false
    },
    {
      "id": "FEAT-0034",
      "name": "Adversarial agent QA test skill",
      "status": "implemented",
      "category": "proof",
      "surfaces": [
        "skills/agent-qa-test",
        "docs/skills/registry.jsonl"
      ],
      "source_refs": [
        "docs/fundamentals/harness-engineering-doctrine.md",
        "docs/features/registry.jsonl#FEAT-0031"
      ],
      "external_refs": [],
      "evidence_refs": [
        "skills/agent-qa-test/SKILL.md",
        "docs/HISTORY.md"
      ],
      "known_limits": "Skill and prompt-template surface only; actual native subagent execution still depends on the invoking agent and available runtime tools.",
      "metrics": [
        "agent_qa_test_skill_validation_pass"
      ],
      "last_verified": "2026-05-26",
      "capability_role": "subcapability",
      "public": false
    },
    {
      "id": "FEAT-0043",
      "name": "Project-level system prompt eval suite",
      "status": "implemented",
      "category": "proof",
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
      "last_verified": "2026-06-07",
      "capability_role": "subcapability",
      "public": false
    }
  ]
---

# Proof And Review

The QA, review, completion, and adversarial testing surfaces that keep Farplane work evidence-backed instead of self-certified.

## Role

This system spec is the authored source for one public Farplane system and its internal capability handles. The generated registries expose the same data as `docs/systems/registry.jsonl` and `docs/features/registry.jsonl`.

## Public Capability

- `FEAT-0008` - Artifact-first QA and completion proof

## Capability Handles

- `FEAT-0008` `primary` - Artifact-first QA and completion proof
- `FEAT-0010` `subcapability` - Stop-hook continuation and completion judgment
- `FEAT-0031` `subcapability` - Agent behavior test workflow
- `FEAT-0034` `subcapability` - Adversarial agent QA test skill
- `FEAT-0043` `subcapability` - Project-level system prompt eval suite

## Maintenance Notes

- Edit the `system_record_json` and `capability_records_json` blocks in this file, then run `python3 docs/features/validate_features.py --write`.
- Keep public docs focused on the system and primary capability; use subcapability rows for compatibility, dedupe, rollout, and evidence tracking.
