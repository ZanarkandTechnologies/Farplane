---
title: "Invocation Runtime"
status: active
owner: farplane-framework
created_at: 2026-06-26
updated_at: 2026-06-26
tags:
  - farplane
  - systems
  - invocation-runtime
refs:
  - docs/specs/invocation-and-adapters.md
  - skills/farplane-invocation/SKILL.md
  - bin/farplane_invocation.py
system_record_json: |
  {
    "id": "SYS-0004",
    "name": "Invocation Runtime",
    "status": "implemented",
    "summary": "The explicit invocation, board adapter, compute selector, and external-runner boundary that keep Farplane an invocation/proof layer rather than a hidden daemon.",
    "owner_spec": "docs/systems/invocation-runtime.md",
    "primary_feature_ref": "FEAT-0015",
    "feature_refs": [
      "FEAT-0015",
      "FEAT-0016",
      "FEAT-0018",
      "FEAT-0019",
      "FEAT-0020"
    ],
    "refs": [
      "docs/specs/invocation-and-adapters.md",
      "skills/farplane-invocation/SKILL.md",
      "bin/farplane_invocation.py"
    ],
    "last_verified": "2026-06-26"
  }
capability_records_json: |
  [
    {
      "id": "FEAT-0015",
      "name": "Symphony-compatible Farplane invocation contract",
      "status": "implemented",
      "category": "execution",
      "surfaces": [
        "WORKFLOW.md",
        "skills/farplane-invocation",
        "bin/farplane_invocation.py",
        "docs/specs/invocation-and-adapters.md"
      ],
      "source_refs": [
        "docs/specs/invocation-and-adapters.md",
        "docs/HISTORY.md"
      ],
      "external_refs": [
        "Symphony Service Specification draft v1"
      ],
      "evidence_refs": [
        "tickets/archive/TASK-0107/ticket.md",
        "tickets/archive/TASK-0107/artifacts/qa/prepare-planning.json",
        "tickets/archive/TASK-0107/artifacts/qa/sample-proof-packet.json"
      ],
      "known_limits": "Filesystem ticket adapter and local compute only; no daemon, polling, Linear/Notion adapter, cloud execution, or Codex-launching wrapper.",
      "metrics": [
        "runner_contract_conformance",
        "proof_packet_parse_rate"
      ],
      "last_verified": "2026-05-05",
      "capability_role": "primary",
      "public": true
    },
    {
      "id": "FEAT-0016",
      "name": "Board and compute orchestration doctrine",
      "status": "implemented",
      "category": "execution",
      "surfaces": [
        "docs/specs/invocation-and-adapters.md",
        "WORKFLOW.md",
        "skills/farplane-invocation"
      ],
      "source_refs": [
        "SRC-0001",
        "SRC-0006",
        "docs/specs/invocation-and-adapters.md"
      ],
      "external_refs": [
        "Symphony Service Specification draft v1"
      ],
      "evidence_refs": [
        "tickets/archive/TASK-0111/ticket.md"
      ],
      "known_limits": "Spec/governance layer only; BoardAdapter v1, compute selector v2, Symphony shim, and parallel board-drain heartbeat remain follow-up tickets.",
      "metrics": [
        "orchestration_contract_traceability",
        "future_adapter_conformance"
      ],
      "last_verified": "2026-06-13",
      "capability_role": "subcapability",
      "public": false
    },
    {
      "id": "FEAT-0018",
      "name": "Filesystem BoardAdapter v1",
      "status": "implemented",
      "category": "execution",
      "surfaces": [
        "bin/farplane_boards.py",
        "bin/farplane_invocation.py",
        "skills/farplane-invocation",
        "docs/specs/invocation-and-adapters.md"
      ],
      "source_refs": [
        "SRC-0001",
        "docs/specs/invocation-and-adapters.md"
      ],
      "external_refs": [
        "Symphony Service Specification draft v1"
      ],
      "evidence_refs": [
        "tickets/archive/TASK-0113/ticket.md",
        "bin/tests/test_farplane_boards.py"
      ],
      "known_limits": "Filesystem read/normalization only; evidence writeback is explicit manual result and external board adapters remain future work.",
      "metrics": [
        "work_item_normalization_pass_rate",
        "board_adapter_path_containment"
      ],
      "last_verified": "2026-05-05",
      "capability_role": "subcapability",
      "public": false
    },
    {
      "id": "FEAT-0019",
      "name": "Compute selector admission policy v2",
      "status": "implemented",
      "category": "execution",
      "surfaces": [
        "bin/farplane_compute.py",
        "bin/farplane_invocation.py",
        "skills/farplane-invocation",
        "docs/specs/invocation-and-adapters.md"
      ],
      "source_refs": [
        "SRC-0001",
        "docs/specs/invocation-and-adapters.md",
        "skills/pr-runtime"
      ],
      "external_refs": [
        "Symphony Service Specification draft v1"
      ],
      "evidence_refs": [
        "tickets/archive/TASK-0114/ticket.md",
        "bin/tests/test_farplane_compute.py",
        "tickets/archive/TASK-0114/artifacts/compute"
      ],
      "known_limits": "Admission only; it does not launch worktrees, Symphony, Codex cloud, retries, polling, or remote scheduler work.",
      "metrics": [
        "compute_blocker_precision",
        "unsupported_target_fallback_rate",
        "worktree_runtime_hint_coverage"
      ],
      "last_verified": "2026-05-05",
      "capability_role": "subcapability",
      "public": false
    },
    {
      "id": "FEAT-0020",
      "name": "Symphony integration shim template",
      "status": "implemented",
      "category": "execution",
      "surfaces": [
        "skills/farplane-invocation/templates/symphony-run-envelope.json",
        "skills/farplane-invocation/references/symphony.md",
        "docs/specs/invocation-and-adapters.md"
      ],
      "source_refs": [
        "SRC-0001",
        "docs/specs/invocation-and-adapters.md"
      ],
      "external_refs": [
        "Symphony Service Specification draft v1"
      ],
      "evidence_refs": [
        "tickets/archive/TASK-0112/ticket.md",
        "bin/tests/test_farplane_invocation.py",
        "tickets/archive/TASK-0112/artifacts/smoke"
      ],
      "known_limits": "Template and smoke only; no Elixir service, Linear API integration, Codex app-server client, scheduler, retry loop, or remote worker launch ships here.",
      "metrics": [
        "symphony_envelope_prepare_pass_rate",
        "responsibility_boundary_clarity"
      ],
      "last_verified": "2026-05-05",
      "capability_role": "implementation_detail",
      "public": false
    }
  ]
---

# Invocation Runtime

The explicit invocation, board adapter, compute selector, and external-runner boundary that keep Farplane an invocation/proof layer rather than a hidden daemon.

## Role

This system spec is the authored source for one public Farplane system and its internal capability handles. The generated registries expose the same data as `docs/systems/registry.jsonl` and `docs/features/registry.jsonl`.

## Public Capability

- `FEAT-0015` - Symphony-compatible Farplane invocation contract

## Capability Handles

- `FEAT-0015` `primary` - Symphony-compatible Farplane invocation contract
- `FEAT-0016` `subcapability` - Board and compute orchestration doctrine
- `FEAT-0018` `subcapability` - Filesystem BoardAdapter v1
- `FEAT-0019` `subcapability` - Compute selector admission policy v2
- `FEAT-0020` `implementation_detail` - Symphony integration shim template

## Maintenance Notes

- Edit the `system_record_json` and `capability_records_json` blocks in this file, then run `python3 docs/features/validate_features.py --write`.
- Keep public docs focused on the system and primary capability; use subcapability rows for compatibility, dedupe, rollout, and evidence tracking.
