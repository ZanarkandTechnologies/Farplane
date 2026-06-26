---
title: "Agent Kernel"
status: active
owner: farplane-framework
created_at: 2026-06-26
updated_at: 2026-06-26
tags:
  - farplane
  - systems
  - agent-kernel
refs:
  - AGENTS.md
  - templates/global/AGENTS.md
  - docs/fundamentals/harness-engineering-doctrine.md
system_record_json: |
  {
    "id": "SYS-0001",
    "name": "Agent Kernel",
    "status": "implemented",
    "summary": "The installed agent context, templates, prompt rules, and response conventions that let a Codex enter Farplane with the right operating shape.",
    "owner_spec": "docs/systems/agent-kernel.md",
    "primary_feature_ref": "FEAT-0042",
    "feature_refs": [
      "FEAT-0042",
      "FEAT-0001",
      "FEAT-0045",
      "FEAT-0048",
      "FEAT-0050",
      "FEAT-0051",
      "FEAT-0052"
    ],
    "refs": [
      "AGENTS.md",
      "templates/global/AGENTS.md",
      "docs/fundamentals/harness-engineering-doctrine.md"
    ],
    "last_verified": "2026-06-26"
  }
capability_records_json: |
  [
    {
      "id": "FEAT-0042",
      "name": "Lean global agent operating kernel",
      "status": "implemented",
      "category": "context-routing",
      "surfaces": [
        "templates/global/AGENTS.md",
        "skills/init-advisor/references/AGENTS_TEMPLATE.md",
        "ARCHITECTURE.md"
      ],
      "source_refs": [
        "docs/fundamentals/harness-engineering-doctrine.md",
        "docs/HISTORY.md"
      ],
      "external_refs": [],
      "evidence_refs": [
        "templates/global/AGENTS.md",
        "skills/init-advisor/references/AGENTS_TEMPLATE.md",
        "docs/HISTORY.md"
      ],
      "known_limits": "The global template now owns only every-turn behavior; project-specific coding defaults and detailed workflows must keep living in project AGENTS files, skills, tickets, docs, validators, or subagent prompts.",
      "metrics": [],
      "last_verified": "2026-06-07",
      "capability_role": "primary",
      "public": true
    },
    {
      "id": "FEAT-0001",
      "name": "AGENTS.md as a map, not an encyclopedia",
      "status": "implemented",
      "category": "context-routing",
      "surfaces": [
        "AGENTS.md",
        "templates/global/AGENTS.md",
        "docs/fundamentals/harness-engineering-doctrine.md"
      ],
      "source_refs": [
        "docs/specs/harness-techniques.md",
        "docs/MEMORY.md#MEM-0033"
      ],
      "external_refs": [],
      "evidence_refs": [
        "docs/HISTORY.md"
      ],
      "known_limits": "Coverage depends on deeper docs and skills staying discoverable and current.",
      "metrics": [],
      "last_verified": "2026-05-04",
      "capability_role": "implementation_detail",
      "public": false
    },
    {
      "id": "FEAT-0045",
      "name": "Goal alignment header and split discipline",
      "status": "implemented",
      "category": "context-routing",
      "surfaces": [
        "templates/global/AGENTS.md",
        "skills/eval/examples/farplane-global-harness/tasks.json"
      ],
      "source_refs": [
        "docs/MEMORY.md#MEM-0141",
        "docs/HISTORY.md"
      ],
      "external_refs": [],
      "evidence_refs": [
        "templates/global/AGENTS.md",
        "skills/eval/examples/farplane-global-harness/tasks.json",
        "docs/HISTORY.md"
      ],
      "known_limits": "The behavior is prompt-and-eval enforced rather than mechanically checked in every chat response; it should trigger for long, multitopic, ambiguous, or substantial replies, not every tiny answer. `Goal:` is the default alignment header; `Topics:` remains available only when a true multi-topic ledger is needed for navigation. Independent or context-heavy tangents still need an explicit new-thread handoff rather than silently continuing in one overloaded chat.",
      "metrics": [
        "goal_alignment_eval_pass_rate"
      ],
      "last_verified": "2026-06-09",
      "capability_role": "subcapability",
      "public": false
    },
    {
      "id": "FEAT-0048",
      "name": "Harness algebra constrained optimization model",
      "status": "designed",
      "category": "context-routing",
      "surfaces": [
        "docs/fundamentals/harness-algebra.md",
        "README.md",
        "docs/specs/README.md",
        "docs/skills/best-practices.md",
        "docs/skills/templates/SKILL_TEMPLATE.md",
        "docs/skills/README.md"
      ],
      "source_refs": [
        "docs/fundamentals/harness-algebra.md"
      ],
      "external_refs": [],
      "evidence_refs": [
        "tickets/TASK-0188/ticket.md"
      ],
      "known_limits": "Canonical constrained-optimization model and skill-template guidance only; no broad skill migration, generated graph extraction from function contracts, semantic validator, or automatic optimization loop is shipped yet.",
      "metrics": [
        "harness_algebra_spec_validation_pass"
      ],
      "last_verified": "2026-06-10",
      "capability_role": "subcapability",
      "public": false
    },
    {
      "id": "FEAT-0050",
      "name": "Function-signature response notation",
      "status": "implemented",
      "category": "context-routing",
      "surfaces": [
        "templates/global/AGENTS.md",
        "docs/fundamentals/harness-algebra.md",
        "docs/MEMORY.md"
      ],
      "source_refs": [
        "docs/MEMORY.md#MEM-0139",
        "docs/fundamentals/harness-algebra.md"
      ],
      "external_refs": [],
      "evidence_refs": [
        "templates/global/AGENTS.md",
        "docs/fundamentals/harness-algebra.md",
        "docs/HISTORY.md"
      ],
      "known_limits": "Prompt-and-spec preference only; agents must still judge when signatures improve clarity rather than forcing pseudo-code into tiny or emotional replies.",
      "metrics": [],
      "last_verified": "2026-06-09",
      "capability_role": "implementation_detail",
      "public": false
    },
    {
      "id": "FEAT-0051",
      "name": "H3 headings with blockquoted delta format",
      "status": "implemented",
      "category": "context-routing",
      "surfaces": [
        "templates/global/AGENTS.md",
        "docs/MEMORY.md"
      ],
      "source_refs": [
        "docs/MEMORY.md#MEM-0140",
        "templates/global/AGENTS.md"
      ],
      "external_refs": [],
      "evidence_refs": [
        "templates/global/AGENTS.md",
        "docs/HISTORY.md"
      ],
      "known_limits": "Prompt-only response preference; agents still decide when a change is material enough for its own heading and should avoid heading or blockquote clutter for tiny one-line updates.",
      "metrics": [],
      "last_verified": "2026-06-09",
      "capability_role": "implementation_detail",
      "public": false
    },
    {
      "id": "FEAT-0052",
      "name": "Attention-protection pushback and escalation",
      "status": "implemented",
      "category": "context-routing",
      "surfaces": [
        "templates/global/AGENTS.md",
        "skills/eval/templates/config.json",
        "skills/eval/templates/contexts/agi-toy-shop.md",
        "skills/eval/examples/farplane-global-harness/tasks.json",
        "skills/eval/templates/agent.md",
        "skills/eval/scripts/run_evals.py",
        "skills/eval/references/eval-best-practices.md",
        "docs/MEMORY.md"
      ],
      "source_refs": [
        "docs/MEMORY.md#MEM-0142",
        "docs/MEMORY.md#MEM-0143",
        "experiments/best-of-worlds/global-agents-comparison/decision-matrix.md"
      ],
      "external_refs": [],
      "evidence_refs": [
        "templates/global/AGENTS.md",
        "skills/eval/templates/config.json",
        "skills/eval/templates/contexts/agi-toy-shop.md",
        "skills/eval/examples/farplane-global-harness/tasks.json",
        "skills/eval/templates/agent.md",
        "skills/eval/scripts/run_evals.py",
        "skills/eval/tests/test_run_evals.py",
        "skills/eval/references/eval-best-practices.md",
        "docs/HISTORY.md"
      ],
      "known_limits": "Prompt-and-eval behavior only; it relies on agent judgment to distinguish useful evidence-backed pushback from needless friction and to avoid over-formatting tiny operational replies. Generic task realism now uses AGI Toy Shop as a shared clean-room default context file, while task queries stay realistic user requests and task context is reserved for overrides or opt-out. Real repo prompts remain necessary when local files, validators, scripts, or installed skills are the behavior under test.",
      "metrics": [
        "attention_protection_eval_pass_rate"
      ],
      "last_verified": "2026-06-10",
      "capability_role": "subcapability",
      "public": false
    }
  ]
---

# Agent Kernel

The installed agent context, templates, prompt rules, and response conventions that let a Codex enter Farplane with the right operating shape.

## Role

This system spec is the authored source for one public Farplane system and its internal capability handles. The generated registries expose the same data as `docs/systems/registry.jsonl` and `docs/features/registry.jsonl`.

## Public Capability

- `FEAT-0042` - Lean global agent operating kernel

## Capability Handles

- `FEAT-0042` `primary` - Lean global agent operating kernel
- `FEAT-0001` `implementation_detail` - AGENTS.md as a map, not an encyclopedia
- `FEAT-0045` `subcapability` - Goal alignment header and split discipline
- `FEAT-0048` `subcapability` - Harness algebra constrained optimization model
- `FEAT-0050` `implementation_detail` - Function-signature response notation
- `FEAT-0051` `implementation_detail` - H3 headings with blockquoted delta format
- `FEAT-0052` `subcapability` - Attention-protection pushback and escalation

## Maintenance Notes

- Edit the `system_record_json` and `capability_records_json` blocks in this file, then run `python3 docs/features/validate_features.py --write`.
- Keep public docs focused on the system and primary capability; use subcapability rows for compatibility, dedupe, rollout, and evidence tracking.
