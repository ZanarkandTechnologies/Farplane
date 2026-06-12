# Farplane

![Farplane OS hero banner](./assets/farplane-hero.png)

Farplane is Farplane Core: the drift-resistant, evolve-first harness behind
Farplane OS.

Farplane OS gives Codex and adjacent agent runtimes a visible operating system:
structured skills, reviewable workflow artifacts, hooks, evals, benchmarks,
durable repo memory, operational dashboards, and optional immersive UI
surfaces. The ticket-first autonomous coding loop is one important feature, but
Farplane Core is broader than tickets: it is a way to keep an AI harness
learning without letting it silently sprawl, forget, or self-approve weak work.

## Product Shape

Farplane OS is the parent product family. This repo is Farplane Core: skills,
hooks, evals, review, memory, runtime state, and Done / Proof contracts. Farplane
Console is the practical dashboard for harness health and optimization.
Farplane UI keeps its current name as the optional immersive office/game
surface; Farplane Office is only an alias for that mode.

Current sibling shape:

| Surface | Path | Owns |
| --- | --- | --- |
| Farplane Core | `Farplane/` | Harness contracts, skills, hooks, evals, tickets, review, proof, and repo memory |
| Farplane Console | `Farplane-Console/` | Operational dashboard, activity telemetry, nudges, eval views, and Mighty Guard health workflows |
| Farplane UI | `Farplane-UI/` | Optional immersive office/game experience and skill-object interactions |
| Farplane Office | alias only | The office/game mode inside Farplane UI, not a repo rename |

Other app ideas are absorbed as Console modules, Core contracts, UI surfaces,
skill UIs, or archived experiments instead of staying as separate centers of
gravity.

```mermaid
flowchart LR
  classDef shell fill:#dbeafe,stroke:#2563eb,color:#111827
  classDef engine fill:#facc15,stroke:#854d0e,stroke-width:3px,color:#111827
  classDef module fill:#e5e7eb,stroke:#4b5563,color:#111827
  classDef adapter fill:#f5f3ff,stroke:#8b5cf6,color:#111827,stroke-dasharray:5 3

  os["Farplane OS<br/>product family"]:::shell --> engine["Farplane Core<br/>harness engine"]:::engine
  os --> console["Farplane Console<br/>dashboard + Mighty Guard"]:::module
  os --> ui["Farplane UI<br/>optional office/game mode"]:::module
  engine --> skills["skills + skill UI bindings"]:::module
  engine --> evals["evals + proof viewer"]:::module
  engine --> health["health / learning inbox<br/>Mighty Guard contracts"]:::module
  engine --> nudges["nudges / attention loops"]:::module
  engine --> map["harness map<br/>skills + docs + backlinks"]:::module
  engine --> state[".farplane/<br/>project runtime state"]:::module
  ui --> scene["office scene<br/>skill-object panels"]:::module
  console --> health
  console --> nudges
  engine -. runtime adapter .-> openclaw["OpenClaw"]:::adapter
```

The product rule is:

- **One product family:** Farplane OS owns the parent story while Core,
  Console, and UI keep clean surface boundaries.
- **Core owns proof:** Farplane Core owns harness semantics, skills, hooks,
  evals, tickets, review, memory, runtime state, and Done / Proof contracts.
- **Console owns operations:** Farplane Console owns the practical dashboard,
  activity telemetry, nudges, and Mighty Guard harness-health workflows.
- **UI stays optional:** Farplane UI owns the immersive office/game mode and
  skill-object interactions. Farplane Office is a mode alias, not a rename.
- **Skill-owned UI incubation:** a skill may ship a small viewer, panel, or URL
  binding before the workflow is productized.
- **Roll-up when proven:** useful skill UIs graduate into Console modules or
  Farplane UI surfaces while keeping a skill binding back to the owning
  workflow.
- **Adapters stay adapters:** OpenClaw, Telegram paths, external CLIs, and
  future runtimes connect to the engine without becoming the product core.
- **State is Farplane-native:** project-local product/runtime state lives under
  `.farplane/`; global product state can live under `~/.farplane/` when the
  multi-project shell needs it.

## Architecture

```mermaid
flowchart LR
  classDef core fill:#facc15,stroke:#854d0e,stroke-width:3px,color:#111827
  classDef surface fill:#e5e7eb,stroke:#4b5563,color:#111827
  classDef proof fill:#fee2e2,stroke:#b91c1c,color:#7f1d1d
  classDef future fill:#f5f3ff,stroke:#8b5cf6,color:#111827,stroke-dasharray:5 3

  ask[/operator ask/] --> map

  subgraph map["Visible Harness Memory"]
    agents[(AGENTS.md)]:::surface
    docs[(docs/*)]:::surface
    tickets[(tickets/*)]:::surface
    history[(HISTORY / MEMORY / TROUBLES / LESSONS)]:::surface
  end

  subgraph skills["Structured Skill Layer"]
    tier1["Tier 1 primitives"]:::core
    tier2["Tier 2 workflow interfaces"]:::core
    tier3["Tier 3 domain skills"]:::core
  end

  subgraph evolve["Evolve-First Layer"]
    skillEvals["skill evals"]:::proof
    workflowEvals["workflow evals"]:::proof
    promptEvals["system-prompt evals"]:::proof
    dislikedCases["saved disliked test cases"]:::proof
  end

  subgraph hooks["Opinionated Hooks"]
    stop["Stop / user-turn gates"]:::core
    realtime["real-time benchmarks<br/>coming soon"]:::future
    health["skill health monitoring<br/>coming soon"]:::future
  end

  subgraph work["Work Execution"]
    plan["plan / spec / ticket"]:::surface
    impl["build / QA / review"]:::surface
    close["docs / memory / closeout"]:::surface
  end

  map --> skills
  skills --> work
  work --> evolve
  evolve --> skills
  hooks --> work
  hooks --> evolve
  work --> history
```

## What Makes It Different

- **Drift-resistant by default.** Farplane keeps work grounded in visible docs,
  tickets, memories, validators, and review artifacts instead of transcript
  vibes.
- **Evolve-first.** Skills, workflows, and prompt behavior are meant to be
  benchmarked, revised, and re-tested as first-class harness surfaces.
- **Structured skills.** Skills are not loose prompt snippets; they have
  contracts, checklists, dependency shape, references, and on-demand plugin
  packaging when users want Codex plugin installs.
- **Function-defined harness.** Harness processes can be modeled as functions
  over inputs, visible artifacts, outputs, evidence, and state transitions, so
  skills, evals, hooks, memory drains, and tickets can compose without hidden
  variables.
- **Opinionated hooks.** Hooks track user intent, stop weak completion claims,
  route review, and will grow into real-time benchmark and skill-health
  monitoring.
- **Test-case memory.** The harness can preserve disliked outputs, misses, and
  benchmark cases so failures become reusable improvement pressure.
- **Human-marked hard cases.** Corrections and high-priority misses flow into
  local lessons, Notion improvement proposals, sanitized hardcase artifacts, or
  narrow regression eval rows through `gap-analysis`, `optimize-harness`, and
  `eval`.
- **Ticket-first autonomy as one mode.** Tickets remain the durable execution
  surface for coding work, but they are not the whole product.
- **Goal Packets make long loops visible.** Native Codex Goal mode owns
  continuation, while Farplane stores the transparent loop contract in
  `ticket.md`, `program.md`, and `progress.md` so drift, feedback, heartbeat,
  rollout, and completion decisions can be inspected.

## Gamechanging Workflows

- **Ask -> ground -> decide -> act.** Material work starts by checking local
  evidence, peer patterns, official/current docs when needed, and then uses
  advice-shaped decisions before execution.
- **Global prompt stays lean.** The installed AGENTS template carries only
  every-turn behavior; project coding defaults, skill procedures, review rules,
  and workflow detail live in owner files that can be tested and changed
  independently.
- **Skills render their own operating checklist.** Skill `SKILL.md` files own
  first-load todo lists, tiered dependency shape, references, and scripts so the
  agent can recursively compose workflows without stuffing the global prompt.
- **Failures become pressure, not vibes.** Operator corrections fix same-scope
  misses first, then capture a lesson, hardcase, or narrow regression eval when
  the miss is high-priority.
- **Validators can create hardcase seeds.** Deterministic skill-contract checks
  such as todo-tier violations can write deduplicated hardcases automatically,
  so obvious process failures become future eval/self-improvement material.
- **System-prompt behavior is evalable.** Repo-owned eval examples under
  `skills/eval/examples/` cover grounding, context gathering, advice routing,
  proactive action, holdback on risky work, skill todo rendering, correction
  capture, multitopic focus, and validator-triggered hardcase capture.
- **Long threads keep a whole-thread topic ledger.** In multitopic work,
  substantial replies name the root topic, tangents, and current focus, then
  split independently executable follow-ups into new-thread handoffs when the
  current chat is carrying too much.
- **Goal Advisor chooses loop shape.** Ambitious work should use
  `goal-advisor` to decide between active Goal, heartbeat, rollout, feedback
  loop, skill improvement, business loop, or direct work, then compile the
  selected Goal Packet into the native `/goal` prompt.

## Improvement Loop

```mermaid
flowchart LR
  classDef input fill:#dbeafe,stroke:#2563eb,color:#111827
  classDef surface fill:#e5e7eb,stroke:#4b5563,color:#111827
  classDef proof fill:#fee2e2,stroke:#b91c1c,color:#7f1d1d
  classDef learn fill:#ccfbf1,stroke:#0f766e,color:#111827

  ask[/operator ask or correction/]:::input --> ground["reference grounding<br/>local + world evidence"]:::surface
  ground --> decide["advise / placement<br/>choose owning surface"]:::surface
  decide --> change["skill, prompt, doc,<br/>validator, ticket, or agent"]:::surface
  change --> verify["tests, evals,<br/>QA, review"]:::proof
  verify --> capture["lessons, hardcases,<br/>feature registry"]:::learn
  capture --> evals["regression evals<br/>or behavior tests"]:::proof
  evals --> change
```

## Repo Index

| Path | Contains |
| --- | --- |
| `AGENTS.md` | Project-local operating contract for developing Farplane itself. |
| `ARCHITECTURE.md` | Deeper system map, ownership boundaries, and read order. |
| `agents/` | Bounded specialist role configs. |
| `assets/` | Repo-level media and generated assets. |
| `bin/` | Hooks, validators, runtime helpers, launchers, and sync scripts. |
| `docs/` | Specs, feature inventory, history, memory, troubles, lessons, and research. |
| `docs/features/` | Structured feature registry and feature metadata. |
| `docs/specs/` | Canonical behavior specs, meta-harness automation, and doc-gardening loop. |
| `experiments/` | Smoke runs, eval artifacts, prototypes, and temporary proof. |
| `.farplane/` | Ignored project-local runtime, generated, event, and product state. |
| `qa/` | QA cookbook, browser proof paths, and reusable test-entry guidance. |
| `rules/` | Shared policy fragments and prompt-engineering references. |
| `skills/` | Farplane skill packages, references, scripts, and templates. |
| `templates/` | Install-time global Codex templates and config scaffolding. |
| `tickets/` | Active task board, ticket template, artifacts, and archive. |

## Start Here

- Architecture map: [ARCHITECTURE.md](ARCHITECTURE.md)
- Specs index: [docs/specs/README.md](docs/specs/README.md)
- Harness algebra: [docs/specs/harness-algebra.md](docs/specs/harness-algebra.md)
- Self-growing harness map: [docs/specs/harness-techniques.md](docs/specs/harness-techniques.md#self-growing-harness-map)
- Feature inventory: [harness-techniques.md](docs/specs/harness-techniques.md)
- Structured feature registry: [docs/features/README.md](docs/features/README.md)
- Feature registry data: [docs/features/registry.jsonl](docs/features/registry.jsonl)
- Skill guide: [docs/skills/README.md](docs/skills/README.md)
- Ticket contract: [tickets/README.md](tickets/README.md)
- QA cookbook surface: [qa/README.md](qa/README.md)
- Review scoring: [skills/review/README.md](skills/review/README.md)
- Active queue: [tickets](tickets)

## Current Boundary

Farplane is installed into normal Codex and uses visible repo artifacts as the
control plane. It is not a hidden daemon, hosted scheduler, or parallel
multi-agent dispatcher today. Background hooks for live skill-health benchmarks
and saved disliked-case feedback loops are planned harness surfaces, not fully
shipped behavior yet.

Offline evals and human-marked failure capture are the shipped improvement
primitives today. Broader live skill-health benchmarks remain future work.
