---
title: "Farplane Lifecycle"
status: active
owner: farplane-framework
created_at: 2026-06-23
updated_at: 2026-06-29
framework_template_version: "0.2.0"
tags:
  - farplane
  - lifecycle
  - automations
  - goals
  - graph
refs:
  - docs/farplane-framework/README.md
  - docs/farplane-framework/init-advisor-critical-path.md
  - docs/farplane-framework/project-files.md
  - docs/farplane-framework/ticket-execution-loop.md
  - docs/farplane-framework/pulse-and-interval-loop.md
  - docs/farplane-framework/graph-contract.md
  - docs/farplane-framework/hooks-and-runtime.md
  - docs/features/FEAT-0065-pulse-and-interval-automation.md
  - docs/features/FEAT-0029-goal-packet-architecture-for-native-codex-goals.md
  - docs/features/FEAT-0060-registry-backed-documentation-os.md
  - docs/MEMORY.md
---

# Farplane Lifecycle

Farplane is a file-backed operating system for agent-run projects. The shortest
mental model is:

```text
init_project(intent)
  -> visible project files
  -> static human charter, products, goals, and current milestone
  -> ticket-backed Goal Packets
  -> Pulse acts and intervals plan
  -> weekly reports propose goals deltas and leverage bets
  -> drains compress outcomes back into docs, memory, skills, and tickets
```

The framework is intentionally boring at the center. Files carry durable state,
skills carry reusable workflows, tickets carry work contracts, native Codex
Goals carry uninterrupted execution, and hooks stay small enough to observe or
gate without becoming another hidden brain.

## Why This Shape

Farplane uses visible files because agents need shared memory that survives
outside one chat transcript. It uses Goal Packets because material work needs a
small contract, loop configuration, and progress log that can be reviewed or
resumed. It uses explicit automation loops because planning and acting have
different context needs: interval automations compress and replan, while Pulse
chooses one bounded move. It requires proof because autonomous progress is only useful when
the next human or agent can audit what changed. It uses drains because raw
reports, troubles, lessons, and eval results become noise unless they are
periodically routed to their owning docs, skills, tickets, or memory files.

## Quick Start

If you are setting up a project with Codex, start from a plain request:

```text
Use init-advisor for this repo: <project intent>. Create the Farplane
project files, first ticket, QA/proof surfaces, and framework config. Stop for
secrets, spend, deploys, destructive actions, or unclear product decisions.
```

Then inspect the created files:

1. Open `farplane/README.md` for the project-local framework overview.
2. Open `farplane/harness.md` for the static human charter: mission, thesis,
   static leverage commitments, non-tradeoffs, agent authority, systems, and
   skill bindings.
3. Open `farplane/goals.md` for strategy, current milestone, KPIs, and holds.
4. Open `farplane/products.md` for the primary and supporting products this
   team creates.
5. Open `tickets/TASK-0001/ticket.md` for the first planning or discovery
   handoff.
6. Run or ask for `horizon-advisor` only when `farplane/goals.md` is missing,
   stale, or too broad.
7. Run or ask for `goal-advisor` only after the current milestone is concrete
   enough to become a ticket-backed Goal Packet.
8. Activate Pulse, Daily Interval, and Weekly Interval only after goals,
   products, reviewed automation prompts, visible work, and proof surfaces
   exist.

The deeper bootstrap path is [Init Advisor Critical Path](init-advisor-critical-path.md).
The file-by-file reference is [Project Files](project-files.md).

## Lifecycle Map

```mermaid
flowchart TD
  A["Operator intent"] --> B["init-advisor"]
  B --> C["Farplane project files"]
  C --> D["horizon-advisor"]
  D --> E["farplane/goals.md"]
  E --> F["goal-advisor"]
  F --> G["Goal Packet: ticket.md + program.md + progress.md"]
  G --> H["Native Codex Goal"]
  H --> I["implementation, QA, demo, review evidence"]
  I --> J["ticket closeout and docs writeback"]
  E --> K["interval-update"]
  K --> L["dated interval reports + Pulse guidance"]
  K --> R["goals delta proposals + leverage bets"]
  R --> S{"approval required?"}
  S -->|strategy/KPI/frontier change| D
  S -->|execution bet selected| F
  S -->|minor evidence-backed update| E
  G --> M["pulse-update"]
  L --> M
  M --> N["ready ticket execution or planning request"]
  N --> O["Pulse reports and ledgers"]
  O --> K
  J --> P["update-memory / skill-maintenance"]
  P --> Q["compressed memory, lessons, skills, evals"]
  Q --> D
```

## Files First

Farplane divides project state by lifecycle:

```text
farplane/   tracked framework config and project strategy
.farplane/  ignored runtime reports, automation ledgers, logs, eval runs
tickets/    work contracts, Goal Packets, progress, proof artifacts
docs/       durable memory, specs, lessons, troubles, and reader docs
skills/     reusable workflows with declared reads, writes, routes, and gates
hooks.json  small Codex hook entry points
```

This split comes from the memory rule that native Codex Goal mode is the only
formal semantic continuation loop. Farplane adds visible files around it:
`ticket.md` for the task contract, `program.md` for loop configuration, and
`progress.md` for append-only observed execution.

## Init To Goals

`init-advisor` turns an empty or existing repo into a Farplane-shaped
project. It creates or preserves local policy, project docs, ticket templates,
QA entrypoints, framework config, and ignored runtime folders.

The init step does not pretend that file creation is the same as project
understanding. When the human thesis, static leverage commitments, products, or
goals are not grounded, it reports the specific readiness gap before claiming
the project is initialized.

`horizon-advisor` shapes `farplane/goals.md`. It names the north star, value
function, KPIs, anti-metrics, strategy axes, and current milestone. It expands
only the first branch that can produce useful evidence now, then hands
executable work to `goal-advisor`.

## Goals To Native Codex Goal

`goal-advisor` is the execution compiler. For material work it creates or
attaches to a Goal Packet:

```text
ticket.md    task contract, scope, map, Done / Proof
program.md   loop config, metric, budgets, review/QA policy
progress.md  append-only execution log and drift evidence
```

The generated `/goal` prompt lists the packet files and current proof policy.
It is runtime input, not the source of truth. The files remain the durable
contract that future turns, reviewers, Pulse, interval automations, and closeout can inspect.

Within a coding Pulse or native Goal, the normal leaf workflow is:

```text
ticket implementation plan
  -> goal-advisor execution prompt
  -> native Codex Goal
  -> build
  -> QA
  -> demo when required
  -> documentation and memory writeback
```

`impl-plan` may be used before execution when the selected ticket needs a
focused implementation plan, test strategy, and proof contract. Once the Goal
Packet is approved, Goal execution should land the whole ticket unless a real
blocker or proof boundary makes narrower scope necessary.

## Ticket Execution Loop

Ticket execution is the work-completion loop. It starts when human-shaped
intent has become an accepted ticket or controlling spec, then moves through
`impl-plan`, reviewer plan review, `goal-advisor`, native Goal execution,
QA/proof, reviewer completion review, and closeout.

Use [Ticket Execution Loop](ticket-execution-loop.md) for the detailed field
contract, phase owners, autonomy boundary, skill cooperation model, and
hardening risks.

## Pulse And Interval Loop

Pulse and Interval are the orchestration loops. Pulse chooses or executes ready
tickets from current state. Daily Interval reviews the recent window and plans
the next one. Weekly Interval checks strategy drift, proposes goals deltas, and
routes leverage bets back to the right owner.

Use [Pulse And Interval Loop](pulse-and-interval-loop.md) for the detailed
automation signatures, self-update model, advisor routing matrix, reward
signals, and urgent escalation rule.

## Hooks And Runtime

Codex hooks are boundary tools, not orchestration engines. In this repo,
`UserPromptSubmit` captures current-turn user intent and sends a console
heartbeat. `Stop` runs mechanical completion checks and sends a stop heartbeat.

Hooks may detect, capture, gate, or route. They should not rewrite durable
memory, optimize documentation, or silently decide project strategy. When a
hook finds something judgment-heavy, it should hand off to a ticket, skill,
review, or drain workflow.

The hook contract is described in [Hooks and Runtime](hooks-and-runtime.md).

## Drains And Compression

Farplane keeps information useful by compressing it into the right owner:

- `update-memory` refreshes project context across README, docs, memory,
  history, lessons, troubles, tickets, and reports when an owning path and
  approval are explicit.
- `skill-maintenance` turns behavior deltas and lesson hardening into owner
  skill edits, evals, registry sync, audit proof, processed learning state, and
  review. Weekly Interval routes learning backpropagation here instead of using
  a separate drain wrapper.
- `knowledge-tidier` ranks bloated knowledge artifacts and routes keep, cut,
  archive, or owner-specific handoffs.
- `eval` converts agent, prompt, or skill behavior into repeatable tasks,
  judge results, run artifacts, and verdicts.

Compression is not deletion by default. The filesystem lifecycle rule is:
raw signal goes to raw ledgers, distilled rules go to durable ledgers or owner
skills, proof stays near the ticket or experiment, and stale material is
archived, marked superseded, or deleted only with an owner.

## Programmatic Lifecycle Graph

The lifecycle can also be generated as a graph. The graph combines:

- skill signatures such as `state: reads(...)`, `writes(...)`, `routes:`, and
  `gates:`
- framework file nodes from `farplane/`, `.farplane/`, `tickets/`, `docs/`,
  `skills/`, and `hooks.json`
- hook command nodes from Codex hook config
- curated lifecycle edges for the framework-critical path
- finite state projections for init, automation activation, ticket-to-Goal
  execution, and drain/update upkeep

The default artifact is intentionally flattened. Tickets are represented as
`tickets/TASK-*` file shapes rather than individual ticket IDs, and noisy
details such as gate nodes, FSA state nodes, and abstract prose-derived state
are omitted unless the generator is run in full/detail mode.

The graph contract lives in [Graph Contract](graph-contract.md). The generated
artifacts live at
`skills/skill-maintenance/graph/farplane-lifecycle-graph.json` and
`skills/skill-maintenance/graph/farplane-lifecycle-graph.js`.
