---
title: "Self-Improvement And Learning"
status: active
owner: farplane-framework
created_at: 2026-06-26
updated_at: 2026-06-26
tags:
  - farplane
  - systems
  - self-improvement-learning
refs:
  - docs/specs/self-improvement-contracts.md
  - docs/LESSONS.md
  - docs/TROUBLES.md
  - skills/metric-advisor/SKILL.md
system_record_json: |
  {
    "id": "SYS-0007",
    "name": "Self-Improvement And Learning",
    "status": "implemented",
    "summary": "The learning loop that observes behavior gaps, captures hardcases, chooses metrics, routes correction, and turns repeated failures into skills, evals, or docs.",
    "owner_spec": "docs/systems/self-improvement-learning.md",
    "primary_feature_ref": "FEAT-0039",
    "feature_refs": [
      "FEAT-0039",
      "FEAT-0005",
      "FEAT-0006",
      "FEAT-0012",
      "FEAT-0013",
      "FEAT-0026",
      "FEAT-0040",
      "FEAT-0063"
    ],
    "refs": [
      "docs/specs/self-improvement-contracts.md",
      "docs/LESSONS.md",
      "docs/TROUBLES.md",
      "skills/metric-advisor/SKILL.md"
    ],
    "last_verified": "2026-06-26"
  }
capability_records_json: |
  [
    {
      "id": "FEAT-0039",
      "name": "Behavior correction, hardcase metadata, and narrow eval capture",
      "status": "implemented",
      "category": "improvement-loop",
      "surfaces": [
        "skills/gap-analysis",
        "skills/harness-advisor",
        "skills/metric-advisor",
        "skills/optimize-harness",
        "skills/eval",
        "docs/LESSONS.md",
        "experiments/hardcases",
        "docs/specs/self-improvement-contracts.md"
      ],
      "source_refs": [
        "docs/HISTORY.md",
        "docs/features/registry.jsonl#FEAT-0006",
        "docs/features/registry.jsonl#FEAT-0031",
        "docs/features/registry.jsonl#FEAT-0063",
        "docs/specs/self-improvement-contracts.md"
      ],
      "external_refs": [],
      "evidence_refs": [
        "skills/gap-analysis/SKILL.md",
        "skills/harness-advisor/SKILL.md",
        "skills/metric-advisor/SKILL.md",
        "skills/optimize-harness/SKILL.md",
        "skills/eval/SKILL.md",
        "docs/specs/self-improvement-contracts.md",
        "experiments/hardcases/20260607-1917-repent-eval-capture/case.md",
        "tickets/TASK-0228/ticket.md",
        "docs/HISTORY.md"
      ],
      "known_limits": "Correction is skill-and-artifact driven. Hardcase is eval metadata and legacy standalone hardcase artifacts should become runnable eval rows when the expected behavior is testable. Metric selection routes through metric-advisor before self-improve. The loop does not train models, sell data, inspect full Codex histories without a seed anchor, or auto-apply broad harness migrations without proof.",
      "metrics": [
        "gap_packet_quality_pass",
        "harness_placement_quality_pass",
        "metric_card_traceability_pass",
        "hardcase_eval_metadata_pass",
        "narrow_regression_eval_pass"
      ],
      "last_verified": "2026-06-26",
      "capability_role": "primary",
      "public": true
    },
    {
      "id": "FEAT-0005",
      "name": "Metric-driven autoresearch sessions",
      "status": "retired",
      "category": "improvement-loop",
      "surfaces": [],
      "source_refs": [
        "tickets/TASK-0228/ticket.md",
        "docs/HISTORY.md"
      ],
      "external_refs": [],
      "evidence_refs": [
        "tickets/TASK-0228/ticket.md",
        "docs/HISTORY.md"
      ],
      "known_limits": "Retired on 2026-06-26. The old autoresearch-plan and autoresearch-exec skill packages were removed from active routing; use metric-advisor, Goal/eval, and self-improve surfaces instead.",
      "metrics": [],
      "last_verified": "2026-06-26",
      "capability_role": "retired",
      "public": false
    },
    {
      "id": "FEAT-0006",
      "name": "Skill self-improvement with binary evals",
      "status": "implemented",
      "category": "improvement-loop",
      "surfaces": [
        "skills/self-improve",
        "skills/metric-advisor",
        "skills/eval",
        "skills/goal-advisor"
      ],
      "source_refs": [
        "skills/self-improve",
        "skills/metric-advisor",
        "docs/specs/self-improvement-contracts.md",
        "tickets/TASK-0228/ticket.md",
        "docs/HISTORY.md"
      ],
      "external_refs": [],
      "evidence_refs": [
        "skills/self-improve/SKILL.md",
        "skills/metric-advisor/SKILL.md",
        "tickets/TASK-0228/ticket.md",
        "docs/HISTORY.md"
      ],
      "known_limits": "Durable skill memory is only for reusable evals and lessons; scratch runs stay in experiments, and metric choice belongs to metric-advisor before Goal/eval/self-improve routes.",
      "metrics": [
        "skill_eval_pass_rate"
      ],
      "last_verified": "2026-06-26",
      "capability_role": "subcapability",
      "public": false
    },
    {
      "id": "FEAT-0012",
      "name": "Gated skill opportunity applier",
      "status": "implemented",
      "category": "improvement-loop",
      "surfaces": [
        "bin/user_turn.py",
        "bin/capture_user_turn.py",
        "bin/stop_hook.py",
        "bin/self_improve_hook_probe.py",
        "agents/skill-opportunity-applier.toml",
        "docs/specs/invocation-and-adapters.md"
      ],
      "source_refs": [
        "experiments/harness-scout/runs/2026-05-04-self-evolving-agents/compact-analysis.md"
      ],
      "external_refs": [
        "https://www.youtube.com/watch?v=2zhchG0r6iI"
      ],
      "evidence_refs": [
        "bin/tests/test_runtime_state.py",
        "bin/tests/test_stop_hook.py"
      ],
      "known_limits": "Hook sidecar defaults to dry-run probes for local verification; live Notion task creation still depends on Codex CLI tool availability and Notion access. Benchmark-driven rollback and automatic quality comparison remain follow-up work.",
      "metrics": [
        "skill_apply_success_rate",
        "skill_regression_rate",
        "duplicate_skill_change_rate"
      ],
      "last_verified": "2026-05-23",
      "capability_role": "subcapability",
      "public": false
    },
    {
      "id": "FEAT-0013",
      "name": "Hook-based error learning reminder comparison",
      "status": "proposed",
      "category": "memory",
      "surfaces": [],
      "source_refs": [
        "experiments/harness-scout/runs/2026-05-04-self-evolving-agents/compact-analysis.md"
      ],
      "external_refs": [
        "https://www.youtube.com/watch?v=2zhchG0r6iI"
      ],
      "evidence_refs": [
        "experiments/harness-scout/runs/2026-05-04-self-evolving-agents/handoff.md"
      ],
      "known_limits": "Benchmark-only until useful captures beat false reminders and context noise on representative fixtures.",
      "metrics": [
        "useful_learning_capture_rate",
        "false_reminder_rate",
        "context_cost"
      ],
      "last_verified": "2026-05-04",
      "capability_role": "subcapability",
      "public": false
    },
    {
      "id": "FEAT-0026",
      "name": "Case-based memory context graph",
      "status": "designed",
      "category": "memory",
      "surfaces": [
        "docs/fundamentals/harness-algebra.md",
        "docs/MEMORY.md",
        "docs/HISTORY.md",
        "docs/TROUBLES.md",
        "docs/LESSONS.md",
        "docs/features/registry.jsonl",
        "docs/sources/registry.jsonl"
      ],
      "source_refs": [
        "docs/fundamentals/harness-algebra.md"
      ],
      "external_refs": [],
      "evidence_refs": [
        "docs/HISTORY.md"
      ],
      "known_limits": "Seed design is now folded into the harness algebra case-memory model; no extractor, generated case graph, query helper, or review integration exists yet.",
      "metrics": [
        "case_retrieval_precision",
        "policy_consistency_catch_rate",
        "duplicate_feature_prevention_rate"
      ],
      "last_verified": "2026-06-11",
      "capability_role": "subcapability",
      "public": false
    },
    {
      "id": "FEAT-0040",
      "name": "Meta-harness automation map",
      "status": "implemented",
      "category": "improvement-loop",
      "surfaces": [
        "docs/specs/harness-techniques.md",
        "docs/specs/self-improvement-contracts.md",
        "docs/features/registry.jsonl",
        "docs/skills/registry.jsonl",
        "docs/skills/system.md",
        "skills/skill-maintenance",
        "bin/validators/sync_skill_registry.py",
        "docs/skills/templates/SKILL_TEMPLATE.md"
      ],
      "source_refs": [
        "docs/specs/harness-techniques.md",
        "docs/MEMORY.md#MEM-0132"
      ],
      "external_refs": [],
      "evidence_refs": [
        "bin/validators/test_sync_skill_registry.py",
        "docs/HISTORY.md"
      ],
      "known_limits": "Documentation, registry routing, and validated `feature_refs` metadata only; broad skill feature adoption remains manual/on-contact, and Farplane does not run hidden skill-health daemons or background schedulers.",
      "metrics": [
        "skill_feature_ref_validation_pass"
      ],
      "last_verified": "2026-06-11",
      "capability_role": "implementation_detail",
      "public": false
    },
    {
      "id": "FEAT-0063",
      "name": "Metric advisor cards",
      "status": "implemented",
      "category": "skills",
      "surfaces": [
        "skills/metric-advisor",
        "docs/skills/README.md",
        "docs/specs/self-improvement-contracts.md",
        "docs/specs/review-gates.md"
      ],
      "source_refs": [
        "tickets/TASK-0228/ticket.md",
        "skills/best-of-worlds/references/metric-discovery.md",
        "docs/specs/self-improvement-contracts.md"
      ],
      "external_refs": [],
      "evidence_refs": [
        "skills/metric-advisor/SKILL.md",
        "skills/metric-advisor/eval_task.json",
        "tickets/TASK-0228/ticket.md"
      ],
      "known_limits": "Advisory metric-card contract only; callers still own execution, proof, review, and writeback. It must preserve qualitative `none mechanical` cases instead of forcing fake scores.",
      "metrics": [
        "metric_card_traceability_pass",
        "skill_eval_query_lint_pass"
      ],
      "last_verified": "2026-06-26",
      "capability_role": "subcapability",
      "public": false
    }
  ]
---

# Self-Improvement And Learning

The learning loop that observes behavior gaps, captures hardcases, chooses metrics, routes correction, and turns repeated failures into skills, evals, or docs.

## Role

This system spec is the authored source for one public Farplane system and its internal capability handles. The generated registries expose the same data as `docs/systems/registry.jsonl` and `docs/features/registry.jsonl`.

## Public Capability

- `FEAT-0039` - Behavior correction, hardcase metadata, and narrow eval capture

## Capability Handles

- `FEAT-0039` `primary` - Behavior correction, hardcase metadata, and narrow eval capture
- `FEAT-0005` `retired` - Metric-driven autoresearch sessions
- `FEAT-0006` `subcapability` - Skill self-improvement with binary evals
- `FEAT-0012` `subcapability` - Gated skill opportunity applier
- `FEAT-0013` `subcapability` - Hook-based error learning reminder comparison
- `FEAT-0026` `subcapability` - Case-based memory context graph
- `FEAT-0040` `implementation_detail` - Meta-harness automation map
- `FEAT-0063` `subcapability` - Metric advisor cards

## Maintenance Notes

- Edit the `system_record_json` and `capability_records_json` blocks in this file, then run `python3 docs/features/validate_features.py --write`.
- Keep public docs focused on the system and primary capability; use subcapability rows for compatibility, dedupe, rollout, and evidence tracking.
