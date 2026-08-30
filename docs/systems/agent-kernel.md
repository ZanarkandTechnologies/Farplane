---
title: "Agent Kernel"
status: active
owner: farplane-framework
created_at: 2026-06-26
updated_at: 2026-08-29
tags:
  - farplane
  - systems
  - agent-kernel
refs:
  - AGENTS.md
  - templates/global/AGENTS.md
  - docs/fundamentals/harness-engineering-doctrine.md
  - bin/README.md
system_record_json: |
  {
    "id": "SYS-0001",
    "name": "Agent Kernel",
    "status": "implemented",
    "summary": "The installed agent context, templates, prompt rules, and response conventions that let a Codex enter Farplane with the right operating shape.",
    "owner_spec": "docs/systems/agent-kernel.md",
    "primary_feature_ref": "FEAT-0042",
    "feature_refs": [
      "FEAT-0042"
    ],
    "refs": [
      "AGENTS.md",
      "templates/global/AGENTS.md",
      "docs/fundamentals/harness-engineering-doctrine.md",
      "bin/README.md"
    ],
    "last_verified": "2026-08-29"
  }
---
# Agent Kernel

The installed agent context, templates, prompt rules, and response conventions that let
a Codex enter Farplane with the right operating shape. This page is the product-layer
owner for that subsystem: it explains what belongs here, which feature specs make up the
stack, and where adjacent responsibilities should move.

```text
agent_kernel(change, repo_state?) -> owned_feature_set + boundary_decision + maintenance_signal
```

## At A Glance

- System ID: `SYS-0001`
- Status: `implemented`
- Primary feature: `FEAT-0042`
- Owner spec: `docs/systems/agent-kernel.md`
- Feature count: `1`

## Role

Agent Kernel owns the always-loaded operating shape for Farplane agents: autonomy,
action/plan/answer mode, reading discipline, skill routing, proof expectations, and
concise communication. It keeps permanent context lean by pointing detailed procedure to
skills, specs, tickets, validators, and templates.

## Feature Docs

- [FEAT-0042 Lean global agent operating kernel](../features/FEAT-0042-lean-global-agent-operating-kernel.md)

## What Belongs Here

Global and project AGENTS policy, install templates, prompt-load boundaries, response
conventions, and routing rules that every Farplane coding agent must inherit.

## What Belongs Elsewhere

Detailed workflows belong in skills; product capability contracts belong in feature
specs; task-local state belongs in tickets; generated checks belong in validators.

## Static Contract Route

Farplane keeps static source contracts, generated projections, and lifecycle
proof on separate routes:

- `farplane lint` selects read-only repository contracts from the typed
  `bin/core/lint/` registry. `lint all --changed` is also the Git-gate route,
  so feature, project, skill, eval, and ticket edits select their semantic
  static checks from one source of truth.
- Sync and generator commands are the only routes that update registries,
  graphs, or other projections. A lint command must never write them.
- `farplane ticket check --phase planning|complete` remains lifecycle proof: it
  selects phase-dependent evidence and may write a ticket-local
  receipt.
- A validator that checks one skill's generated packet or integration payload
  remains owned by that skill rather than becoming a repository-wide lint rule.

The command reference and maintenance examples live in
[`bin/README.md`](../../bin/README.md).

## Operating Contract

- Keep always-loaded policy lean and navigational.
- Require plain, concrete human-to-human writing in the global communication
  default. Keep artifact-specific examples and finish checks with their
  templates and review owners.
- Require independent evaluation before agreement; responses lead with the
  conclusion or evidence rather than stock praise or reflexive validation.
- Route detailed procedures to the smallest durable owner.
- Preserve feedback-first planning for materially branching design choices.
- Require local context and proof before implementation completion claims.
- Feature-level behavior belongs in `docs/features/FEAT-*.md`; this page owns the system boundary and feature grouping.
- Registry data is generated from system and feature docs, not edited by hand.
- When a capability no longer deserves a feature page, fold its current truth into the best owner and remove active refs.

## AGENTS Feature Inventory

This is the canonical index of behavior groups implemented by the two AGENTS
surfaces. The inventory is intentionally section-sized: individual rules stay
in their owning section, while high-risk behaviors also receive validator or
eval coverage. Every listed section must exist, and every level-two section in
either AGENTS file must be listed here.

<!-- BEGIN AGENT_KERNEL_FEATURE_INVENTORY -->
| ID | Surface | Required section | Behavior group |
| --- | --- | --- | --- |
| `AK-G01` | `templates/global/AGENTS.md` | `## Autonomy And Authority` | Authority, action mode, steering, and reversible autonomy |
| `AK-G02` | `templates/global/AGENTS.md` | `## Decision And Grounding` | Independent reasoning, alternatives, tradeoffs, evidence, and non-sycophantic stance |
| `AK-G03` | `templates/global/AGENTS.md` | `## Correction, Work, And Proof` | Correction handling, execution discipline, verification, and review |
| `AK-G04` | `templates/global/AGENTS.md` | `## Response Contract` | Response ledger, concise communication, visuals, and completion handoff |
| `AK-G05` | `templates/global/AGENTS.md` | `## Context Routing` | Nearest-owner context loading and durable guidance placement |
| `AK-G06` | `templates/global/AGENTS.md` | `## Task State And Artifacts` | Ticket, Goal Packet, and workflow artifact ownership |
| `AK-G07` | `templates/global/AGENTS.md` | `## Skills And Delegation` | Skill loading, phase ownership, and bounded delegation |
| `AK-G08` | `templates/global/AGENTS.md` | `## Local Workbench And Safety` | Checkout discipline, safe editing, polling, credentials, and install boundaries |
| `AK-P01` | `AGENTS.md` | `## Operating model` | Farplane's visible ticket, skill, Goal Packet, and proof model |
| `AK-P02` | `AGENTS.md` | `## Context budget` | Project-local context budget and owner routing |
| `AK-P03` | `AGENTS.md` | `## Local boundaries` | Farplane placement, browser proof, checkout, credential, and runtime boundaries |
| `AK-P04` | `AGENTS.md` | `## Durable truth` | Canonical state and documentation ownership |
| `AK-P05` | `AGENTS.md` | `## Map` | Repository navigation map |
| `AK-P06` | `AGENTS.md` | `## Stop and surface a decision` | Architectural conflict and rollback decision gates |
<!-- END AGENT_KERNEL_FEATURE_INVENTORY -->

Feature reconciliation is bidirectional:

1. Inventory to AGENTS: every listed section remains implemented.
2. AGENTS to inventory: every level-two AGENTS section remains documented.
3. High-risk behavior: validators and representative evals prove semantics that
   a section-presence check cannot prove, including independent reasoning before
   agreement.

## System Flow

```mermaid
flowchart LR
  classDef keep fill:#f3f4f6,stroke:#6b7280,color:#111827
  classDef changed fill:#fef3c7,stroke:#b45309,color:#111827
  classDef added fill:#dcfce7,stroke:#15803d,color:#111827
  classDef retired fill:#fee2e2,stroke:#b91c1c,color:#7f1d1d,stroke-dasharray: 5 3

  repo["repo-local policy<br/>AGENTS.md"]:::keep
  global["install template<br/>templates/global/AGENTS.md"]:::keep
  doctrine["harness doctrine<br/>docs/fundamentals/*"]:::keep
  kernel["SYS-0001 Agent Kernel<br/>entry rules and response shape"]:::changed
  retired["FEAT-0042<br/>retired kernel lean-down feature"]:::retired
  session["Codex session behavior<br/>autonomy, review, artifact-first state"]:::added

  repo --> kernel
  global --> kernel
  doctrine --> kernel
  retired -. "preserved as history" .-> kernel
  kernel --> session
```

The Agent Kernel turns local and install-time policy into the operating shape every Farplane Codex starts from.

## Surfaces

- `AGENTS.md`
- `templates/global/AGENTS.md`
- `docs/fundamentals/harness-engineering-doctrine.md`

## Proof And Maintenance

- Registry proof: `python3 docs/features/validate_features.py`.
- Link proof: `python3 bin/validators/check_doc_refs.py`.
- Static-contract proof: `python3 bin/farplane.py lint all`.
- Feature-fidelity proof: `python3 bin/validators/check_harness_invariants.py`.
- Behavior proof: the `global_independent_reasoning_before_agreement_01` and
  `global_warranted_agreement_after_reasoning_01` prompt evals.
- Update this system page when product-layer boundaries or feature membership changes.
- Update feature pages when capability behavior changes.
- Regenerate registries and commit generated outputs with the source docs.

## Change History

- 2026-08-29: Added the bidirectional AGENTS feature inventory and restored
  explicit independent-reasoning/non-sycophancy preservation proof.

- 2026-08-23: Established the pure static-lint registry and the explicit
  lint/sync/lifecycle routing boundary.

- 2026-07-19: Added the cross-project independent-reasoning and
  non-sycophantic response-opening contract.
- 2026-06-27: Migrated into the reader-first system-spec shape.
