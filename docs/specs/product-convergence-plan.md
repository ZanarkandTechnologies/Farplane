---
title: "Farplane OS Product Convergence Plan"
status: draft
owner: product-architecture
created_at: 2026-06-12
updated_at: 2026-06-12
tags:
  - farplane-os
  - farplane-core
  - farplane-console
  - farplane-ui
  - product-convergence
refs:
  - README.md
  - docs/skills/README.md
  - tickets/TASK-0191/ticket.md
  - /Users/kenjipcx/Zanarkand Technologies/projects/Farplane-UI/README.md
  - /Users/kenjipcx/Zanarkand Technologies/projects/Farplane-Console/README.md
  - /Users/kenjipcx/Zanarkand Technologies/projects/Farplane-Console/docs/specs/mighty-guard.md
  - /Users/kenjipcx/Zanarkand Technologies/projects/Sigmax-Archive-2026-06-12/tokenmaxer/ARCHITECTURE.md
---

# Farplane OS Product Convergence Plan

## Decision

Farplane OS is the parent product system.

The current repos should converge into this product model:

| Current surface | Target name | Role |
| --- | --- | --- |
| `Farplane/` | Farplane Core | Harness, skills, tickets, hooks, evals, review gates, Done / Proof contracts, and lifecycle doctrine |
| `Farplane-Console/` | Farplane Console | Operational dashboard for harness health, evals, maintenance, usage telemetry, nudges, and self-improvement workflows |
| `Farplane-UI/` | Farplane UI | Optional immersive office/game UI for Codex, skill objects, world interactions, and spatial workflows. Farplane Office is an alias for this mode, not a rename target now. |
| archived health ideas | Mighty Guard | Farplane Console module for harness health, observability, evals, and maintenance |

This is a hard-shift migration. There are no public users yet, so previous
active product names should be removed rather than preserved as long-term
product baggage.

## First Principles

Objective:
Give the operator one coherent Farplane OS product family where harness health,
agent activity, skill quality, prompt usage, office/game workflows, and
self-improvement loops feel connected.

User need:
Some users want a practical dashboard, not a game. Some users want the office
because it makes Codex feel alive and spatial. Farplane OS should support both
without forcing the game UI to be the primary value proposition.

System need:
Keep Farplane Core as the file-backed harness source of truth. Put operational
dashboard product value in Farplane Console. Let Farplane UI render immersive
interactions and skill-object panels without owning all harness state. Farplane
Office can describe the office/game mode, but the app keeps the Farplane UI
name for now.

Business hypothesis:
The strongest paid value is likely harness-health and optimization: evals,
skill management, maintenance, safety, telemetry, nudges, and insight into how
the operator actually uses their prompts and agents. The office is delightful,
but it should be optional because it has performance cost and a narrower buyer
shape.

## Product Boundary

Use this ownership split:

| Surface | Owns | Does not own |
| --- | --- | --- |
| Farplane Core | Harness contracts, skills, eval semantics, hooks, tickets, memory, review gates, proof, local lifecycle doctrine | Primary product dashboard, game rendering, hosted telemetry product |
| Farplane Console | Health dashboards, eval views, skill maintenance UI, usage/activity insights, nudge controls, Mighty Guard workflows | Spatial office/game engine, canonical harness policy |
| Farplane UI | Codex-as-office experience, skill-object interactions, immersive UI, optional game surfaces. Farplane Office is a mode alias. | Default dashboard value, canonical health semantics |
| Mighty Guard | Console module for harness health, observability, evals, skill maintenance, safety, and optimization | Standalone app identity |

Signature:

```text
place_capability(capability, maturity, frequency, proof) -> core_contract | console_module | office_surface | skill_ui_incubation | archive
```

## Recommendation

Make Farplane Console the practical product surface first, with Mighty Guard as
its first serious module. Keep Farplane UI as the optional immersive shell.
Keep Farplane Core focused on harness contracts and proof.

Tradeoff accepted:
The old side-project identities disappear from active surfaces. That is worth
it because the product becomes easier to understand before anyone has adopted
the old names.

## Flattening Strategy

Target sibling shape:

```text
/Users/kenjipcx/Zanarkand Technologies/projects/
  Farplane/             # Farplane Core; path stays sealed
  Farplane-Console/     # flattened Console app
  Farplane-UI/          # current immersive UI app; Farplane Office may be used as a mode alias
```

Recommended path:

1. Hard rename the current Console app in place to Farplane Console.
2. Convert the old umbrella repo into the Console repo by moving app contents
   to the repo root with git-aware moves where possible.
3. Inventory non-Console projects and move or archive them deliberately instead
   of silently deleting them.
4. Rename the filesystem folder to `Farplane-Console`.
5. Update Farplane Core docs to describe the Farplane OS product family while keeping Farplane UI named as-is.

Why not a monorepo first:

- The current uncertainty is product ownership, not package management.
- A monorepo would make the move bigger before the boundaries are proved.
- Sibling repos keep Core, Console, and Farplane UI understandable while the product
  shape settles.

Monorepo trigger:

- shared contracts change in lockstep every week
- tests need cross-repo fixtures
- release work repeatedly requires synchronized Core/Console/Farplane UI changes
- duplicated event schemas become a real maintenance problem

## Capability Placement

| Capability | Destination | Rationale |
| --- | --- | --- |
| Evals dashboard | Farplane Console / Mighty Guard | Sellable harness-health value |
| Skill management and maintenance | Farplane Console / Mighty Guard | Operational workflow, frequent use, needs dashboard density |
| Skill health checks | Farplane Core semantics plus Console views | Core defines proof; Console renders and triages |
| Safety and drift checks | Farplane Core semantics plus Console views | Core owns policy; Console owns operator visibility |
| Harness optimization insights | Farplane Console | Practical dashboard value |
| Activity logging and agent-hours | Farplane Console, fed by Core hooks | Operational telemetry, not office-only |
| Prompt usage insights | Farplane Console | Useful even without game UI |
| Nudges and work reminders | Farplane Console first, Farplane UI optional | Needs controls and policy before spatial flavor |
| Skill-object panels | Farplane UI | Spatial object interaction is the office/game mode's unique value |
| Training/gym metaphors | Farplane UI surface backed by Core/Console data | Good for game UX, not the canonical data model |
| Tokenmaxer lifecycle tracking | Console adapter or archived input | Useful if it feeds utilization insights |
| Daily Laws | Archive or separate personal app | Not core harness optimization |
| archived mobile app | Defer | Mobile should wait until Console module boundaries settle |

## Promotion Ladder

Features start in the smallest surface that proves value.

```text
script/hook -> skill UI -> Console module -> Farplane UI surface when spatial value is real
```

Graduate a feature when:

- it answers a recurring operator question
- it has a clear source of truth
- it has stable events, queries, or files
- it has a proof path or regression check
- it improves harness operation rather than merely adding dashboard clutter

## Roadmap Handle

The active roadmap and Goal Packet for this convergence is:

- `tickets/TASK-0191/ticket.md`
- `tickets/TASK-0191/program.md`
- `tickets/TASK-0191/progress.md`

Use that ticket for chunked execution and operator checkpoints.

## Mighty Guard Implementation Slices

The Console-owned module contract lives at:

- `/Users/kenjipcx/Zanarkand Technologies/projects/Farplane-Console/docs/specs/mighty-guard.md`

First implementation tickets:

- `/Users/kenjipcx/Zanarkand Technologies/projects/Farplane-Console/tickets/TASK-0010/ticket.md`: read-only dashboard health summary from existing Console data.
- `/Users/kenjipcx/Zanarkand Technologies/projects/Farplane-Console/tickets/TASK-0011/ticket.md`: summary-safe Farplane Core health event ingestion.
- `/Users/kenjipcx/Zanarkand Technologies/projects/Farplane-Console/tickets/TASK-0012/ticket.md`: operator-approved maintenance queue for findings.

## Open Decisions

- Exact Farplane Console env prefix: `FARPLANE_CONSOLE_*` versus a shorter
  `FARPLANE_*` namespace.
- Whether Farplane Office becomes more than a mode alias later. For the current
  migration, Farplane UI stays named Farplane UI.
- Whether archived non-Console subprojects under `Sigmax-Archive-2026-06-12/`
  should later move to a permanent archive or separate repos.
- Whether Farplane Console eventually owns a hosted telemetry service, or stays
  local-first until the harness-health module proves demand.
