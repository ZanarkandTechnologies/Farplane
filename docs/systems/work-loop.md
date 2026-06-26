---
title: "Work Loop"
status: active
owner: farplane-framework
created_at: 2026-06-26
updated_at: 2026-06-26
tags:
  - farplane
  - systems
  - work-loop
refs:
  - tickets/README.md
  - docs/specs/spec-first-execution-loop.md
  - docs/specs/spec-authoring-contract.md
  - docs/specs/first-principles-planning.md
system_record_json: |
  {
    "id": "SYS-0002",
    "name": "Work Loop",
    "status": "implemented",
    "summary": "The durable loop that turns intent into plans, tickets, skills, implementation, and reviewable proof for one bounded unit of work.",
    "owner_spec": "docs/systems/work-loop.md",
    "primary_feature_ref": "FEAT-0007",
    "feature_refs": [
      "FEAT-0007",
      "FEAT-0002",
      "FEAT-0003",
      "FEAT-0004",
      "FEAT-0017",
      "FEAT-0023",
      "FEAT-0027",
      "FEAT-0028",
      "FEAT-0037"
    ],
    "refs": [
      "tickets/README.md",
      "docs/specs/spec-first-execution-loop.md",
      "docs/specs/spec-authoring-contract.md",
      "docs/specs/first-principles-planning.md"
    ],
    "last_verified": "2026-06-26"
  }
capability_records_json: |
  [
    {
      "id": "FEAT-0007",
      "name": "Ticket as durable task memory",
      "status": "implemented",
      "category": "memory",
      "surfaces": [
        "tickets/README.md",
        "tickets/templates/ticket.md",
        "skills/impl-plan",
        "skills/spec-to-ticket",
        "docs/specs/context-and-handoff-policy.md"
      ],
      "source_refs": [
        "docs/specs/harness-techniques.md",
        "docs/MEMORY.md#MEM-0058",
        "docs/MEMORY.md#MEM-0148"
      ],
      "external_refs": [],
      "evidence_refs": [
        "docs/HISTORY.md"
      ],
      "known_limits": "Only works when agents keep the compact ticket-as-program body, ticket State/Links, progress logs, and artifact pointers current instead of hiding state in chat.",
      "metrics": [],
      "last_verified": "2026-06-12",
      "capability_role": "primary",
      "public": true
    },
    {
      "id": "FEAT-0002",
      "name": "Feature-gap research before implementation planning",
      "status": "implemented",
      "category": "planning",
      "surfaces": [
        "skills/research#research:gap",
        "skills/impl-plan",
        "tickets/templates/ticket.md"
      ],
      "source_refs": [
        "docs/MEMORY.md#MEM-0046",
        "docs/MEMORY.md#MEM-0097",
        "docs/specs/harness-techniques.md"
      ],
      "external_refs": [],
      "evidence_refs": [
        "docs/HISTORY.md"
      ],
      "known_limits": "Works only when agents ground gaps in real comparables rather than intuition.",
      "metrics": [],
      "last_verified": "2026-05-15",
      "capability_role": "subcapability",
      "public": false
    },
    {
      "id": "FEAT-0003",
      "name": "External parity research before local scoping",
      "status": "implemented",
      "category": "planning",
      "surfaces": [
        "skills/research#research:parity",
        "skills/research#research:gap",
        "skills/functional-ui"
      ],
      "source_refs": [
        "docs/MEMORY.md#MEM-0053",
        "docs/MEMORY.md#MEM-0097",
        "docs/specs/harness-techniques.md"
      ],
      "external_refs": [],
      "evidence_refs": [
        "docs/HISTORY.md"
      ],
      "known_limits": "Research method separation must stay intact so parity does not import every adjacent feature into local scope.",
      "metrics": [],
      "last_verified": "2026-05-15",
      "capability_role": "subcapability",
      "public": false
    },
    {
      "id": "FEAT-0004",
      "name": "Best-of-worlds synthesis",
      "status": "implemented",
      "category": "source-synthesis",
      "surfaces": [
        "skills/best-of-worlds",
        "skills/advise"
      ],
      "source_refs": [
        "docs/MEMORY.md#MEM-0073",
        "skills/best-of-worlds"
      ],
      "external_refs": [],
      "evidence_refs": [
        "docs/HISTORY.md"
      ],
      "known_limits": "External skills and repos are research inputs, not live dependencies or auto-synced behavior.",
      "metrics": [],
      "last_verified": "2026-05-04",
      "capability_role": "subcapability",
      "public": false
    },
    {
      "id": "FEAT-0017",
      "name": "Symphony-style spec authoring contract",
      "status": "implemented",
      "category": "planning",
      "surfaces": [
        "docs/specs/spec-authoring-contract.md",
        "skills/deep-system-design",
        "skills/spec-to-ticket",
        "skills/impl-plan"
      ],
      "source_refs": [
        "SRC-0001",
        "docs/specs/invocation-and-adapters.md"
      ],
      "external_refs": [
        "Symphony Service Specification draft v1"
      ],
      "evidence_refs": [
        "tickets/archive/TASK-0116/ticket.md"
      ],
      "known_limits": "Governance/template only; it should guide complex specs without forcing service-runtime ceremony into PRDs or small tickets.",
      "metrics": [
        "spec_contract_traceability",
        "conformance_matrix_coverage"
      ],
      "last_verified": "2026-05-05",
      "capability_role": "subcapability",
      "public": false
    },
    {
      "id": "FEAT-0023",
      "name": "Harness improvement placement advisor",
      "status": "implemented",
      "category": "planning",
      "surfaces": [
        "skills/harness-advisor",
        "skills/harness-advisor/references/placement-axes.md",
        "AGENTS.md",
        "ARCHITECTURE.md",
        "docs/skills/README.md",
        "docs/features/README.md"
      ],
      "source_refs": [
        "docs/fundamentals/harness-engineering-doctrine.md",
        "docs/fundamentals/harness-algebra.md",
        "ARCHITECTURE.md",
        "docs/MEMORY.md#MEM-0106"
      ],
      "external_refs": [],
      "evidence_refs": [
        "docs/HISTORY.md"
      ],
      "known_limits": "Advisory workflow only; it recommends the owning surface and validation path but does not mutate hooks, agents, skills, or registries by itself. Placement scoring is judgment-guided rather than mechanically enforced.",
      "metrics": [],
      "last_verified": "2026-06-10",
      "capability_role": "subcapability",
      "public": false
    },
    {
      "id": "FEAT-0027",
      "name": "Profile-driven project planning",
      "status": "implemented",
      "category": "planning",
      "surfaces": [
        "skills/init-advisor/references/project-profiles.md",
        "skills/init-advisor/references/project-lifecycle.md",
        "skills/init-advisor/references/AGENTS_TEMPLATE.md",
        "skills/init-advisor/references/PROJECT_RULES_TEMPLATE.md",
        "skills/init-advisor",
        "skills/deep-interview",
        "skills/prd",
        "skills/spec-to-ticket",
        "docs/skills/README.md"
      ],
      "source_refs": [
        "tickets/archive/TASK-0170/ticket.md",
        "tickets/archive/TASK-0165/ticket.md"
      ],
      "external_refs": [],
      "evidence_refs": [
        "docs/HISTORY.md",
        "tickets/archive/TASK-0170/artifacts/review/2026-05-22-profile-tier3-batch-review.md"
      ],
      "known_limits": "Planning-skill guidance and profile/lifecycle references only; no deterministic validator enforces profile quality, and prototype gates remain judgment-driven rather than automatic ticket generation.",
      "metrics": [
        "profile_driven_planning_validation_passed"
      ],
      "last_verified": "2026-05-22",
      "capability_role": "subcapability",
      "public": false
    },
    {
      "id": "FEAT-0028",
      "name": "First-principles planning contract",
      "status": "implemented",
      "category": "planning",
      "surfaces": [
        "docs/specs/first-principles-planning.md",
        "skills/init-advisor/references/AGENTS_TEMPLATE.md",
        "skills/prd",
        "skills/spec-to-ticket",
        "skills/impl-plan",
        "skills/advise",
        "tickets/templates/ticket.md",
        "ARCHITECTURE.md"
      ],
      "source_refs": [
        "docs/specs/first-principles-planning.md"
      ],
      "external_refs": [],
      "evidence_refs": [
        "docs/specs/first-principles-planning.md",
        "docs/HISTORY.md"
      ],
      "known_limits": "Planning/spec/advice contract only; it improves PRD, ticket, plan, and recommendation shape but does not mechanically prove that first-principles reasoning is correct.",
      "metrics": [
        "first_principles_planning_validation_passed"
      ],
      "last_verified": "2026-06-06",
      "capability_role": "subcapability",
      "public": false
    },
    {
      "id": "FEAT-0037",
      "name": "Sample-first prototyping primitive",
      "status": "implemented",
      "category": "planning",
      "surfaces": [
        "skills/prototyping",
        "skills/plan",
        "skills/execute",
        "skills/research",
        "skills/skill-maintenance",
        "skills/review",
        "docs/skills/README.md",
        "templates/global/AGENTS.md"
      ],
      "source_refs": [
        "docs/MEMORY.md#MEM-0125"
      ],
      "external_refs": [],
      "evidence_refs": [
        "docs/HISTORY.md",
        "docs/skills/registry.jsonl"
      ],
      "known_limits": "Judgment-driven skill primitive only; it records and requires representative Prototype Notes but does not automatically detect every over-scaled command or enforce sampling at shell runtime.",
      "metrics": [],
      "last_verified": "2026-06-13",
      "capability_role": "subcapability",
      "public": false
    }
  ]
---

# Work Loop

The durable loop that turns intent into plans, tickets, skills, implementation, and reviewable proof for one bounded unit of work.

## Role

This system spec is the authored source for one public Farplane system and its internal capability handles. The generated registries expose the same data as `docs/systems/registry.jsonl` and `docs/features/registry.jsonl`.

## Public Capability

- `FEAT-0007` - Ticket as durable task memory

## Capability Handles

- `FEAT-0007` `primary` - Ticket as durable task memory
- `FEAT-0002` `subcapability` - Feature-gap research before implementation planning
- `FEAT-0003` `subcapability` - External parity research before local scoping
- `FEAT-0004` `subcapability` - Best-of-worlds synthesis
- `FEAT-0017` `subcapability` - Symphony-style spec authoring contract
- `FEAT-0023` `subcapability` - Harness improvement placement advisor
- `FEAT-0027` `subcapability` - Profile-driven project planning
- `FEAT-0028` `subcapability` - First-principles planning contract
- `FEAT-0037` `subcapability` - Sample-first prototyping primitive

## Maintenance Notes

- Edit the `system_record_json` and `capability_records_json` blocks in this file, then run `python3 docs/features/validate_features.py --write`.
- Keep public docs focused on the system and primary capability; use subcapability rows for compatibility, dedupe, rollout, and evidence tracking.
