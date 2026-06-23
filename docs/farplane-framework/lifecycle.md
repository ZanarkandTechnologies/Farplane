---
title: "Farplane Lifecycle"
status: active
owner: farplane-framework
created_at: 2026-06-23
updated_at: 2026-06-23
framework_template_version: "0.2.0"
tags:
  - farplane
  - lifecycle
  - automations
  - goals
  - graph
refs:
  - docs/farplane-framework/README.md
  - docs/farplane-framework/deep-init-critical-path.md
  - docs/farplane-framework/project-files.md
  - docs/farplane-framework/graph-contract.md
  - docs/farplane-framework/hooks-and-runtime.md
  - docs/specs/steer-pulse-automation.md
  - docs/specs/goal-loop-contract.md
  - docs/specs/filesystem-lifecycle.md
  - docs/MEMORY.md
---

# Farplane Lifecycle

Farplane is a file-backed operating system for agent-run projects. The shortest
mental model is:

```text
init_project(intent)
  -> visible project files
  -> goals and current frontier
  -> ticket-backed Goal Packets
  -> Pulse acts and Steer plans
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
resumed. It uses two automation loops because planning and acting have
different context needs: Steer compresses and replans, while Pulse chooses one
bounded move. It requires proof because autonomous progress is only useful when
the next human or agent can audit what changed. It uses drains because raw
reports, troubles, lessons, and eval results become noise unless they are
periodically routed to their owning docs, skills, tickets, or memory files.

## Quick Start

If you are setting up a project with Codex, start from a plain request:

```text
Use deep-init-project for this repo: <project intent>. Create the Farplane
project files, first ticket, QA/proof surfaces, and framework config. Stop for
secrets, spend, deploys, destructive actions, or unclear product decisions.
```

Then inspect the created files:

1. Open `farplane/README.md` for the project-local framework overview.
2. Open `farplane/harness.md` for mission, values, systems, and skill bindings.
3. Open `farplane/goals.md` for strategy, current milestone, KPIs, and holds.
4. Open `tickets/TASK-0001/ticket.md` for the first planning or discovery
   handoff.
5. Run or ask for `horizon-advisor` only when `farplane/goals.md` is missing,
   stale, or too broad.
6. Run or ask for `goal-advisor` only after the current milestone is concrete
   enough to become a ticket-backed Goal Packet.
7. Activate Pulse and Steer only after goals, reviewed automation prompts,
   visible work, and proof surfaces exist.

The deeper bootstrap path is [Deep Init Critical Path](deep-init-critical-path.md).
The file-by-file reference is [Project Files](project-files.md).

## Lifecycle Map

```mermaid
flowchart TD
  A["Operator intent"] --> B["deep-init-project"]
  B --> C["Farplane project files"]
  C --> D["horizon-advisor"]
  D --> E["farplane/goals.md"]
  E --> F["goal-advisor"]
  F --> G["Goal Packet: ticket.md + program.md + progress.md"]
  G --> H["Native Codex Goal"]
  H --> I["implementation, QA, demo, review evidence"]
  I --> J["ticket closeout and docs writeback"]
  E --> K["steer-update"]
  K --> L["dated Steer reports + Pulse guidance"]
  G --> M["pulse-update"]
  L --> M
  M --> N["one bounded action or worker handoff"]
  N --> O["Pulse reports and ledgers"]
  O --> K
  J --> P["update-memory / learning-drain / skill-maintenance"]
  P --> Q["compressed memory, lessons, skills, evals"]
  Q --> D
```

## Files First

Farplane divides project state by lifecycle:

```text
farplane/   tracked framework config and project strategy
.farplane/  ignored runtime reports, scheduler state, ledgers, logs, eval runs
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

`deep-init-project` turns an empty or existing repo into a Farplane-shaped
project. It creates or preserves local policy, project docs, ticket templates,
QA entrypoints, framework config, and ignored runtime folders.

The init step does not pretend that file creation is the same as project
understanding. When the project intent is not grounded, it reports
`needs_goal_intake` and routes to `horizon-advisor`.

`horizon-advisor` shapes `farplane/goals.md`. It names the north star, value
function, KPIs, anti-metrics, strategy axes, and current frontier. It expands
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
contract that future turns, reviewers, Pulse, Steer, and closeout can inspect.

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

## Steer And Pulse

Farplane autonomous operation uses two Codex automation loops:

```text
pulse_update(project, board_state, action_tree, reward_state)
  -> one bounded action + decision state

steer_update(project, jobs, plan_triggers, scheduler_state)
  -> due interval jobs + scheduler state delta + Pulse guidance
```

Pulse is the fast actor loop. It reads current goals, recent Steer guidance,
ticket state, action arms, rewards, and ledgers. It selects one bounded board
move, optionally spawns a worker, writes a dated Pulse report, and updates
decision/reward state.

Steer is the planning loop. It reads configured jobs, scheduler state, goals,
recent tickets, memory, lessons, troubles, and Pulse reports. It calls
`horizon-update` for due daily or weekly interval planning, writes dated Steer
reports, gives Pulse guidance, and updates `.farplane/state/steer-scheduler.json`.

The important design choice is that Pulse does not become long-horizon
strategy, and Steer does not become a fast action dispatcher. They share files,
not hidden transcript memory.

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
- `learning-drain` dedupes recent troubles and lessons, writes processed state,
  and routes durable skill hardening or eval follow-up.
- `skill-maintenance` turns behavior deltas and lesson hardening into owner
  skill edits, evals, registry sync, audit proof, and review.
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
