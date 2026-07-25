---
title: "Farplane Lifecycle Graph Contract"
status: active
owner: farplane-framework
created_at: 2026-06-23
updated_at: 2026-06-24
framework_template_version: "0.2.0"
tags:
  - farplane
  - lifecycle
  - graph
  - ui
refs:
  - docs/farplane-framework/lifecycle.md
  - docs/farplane-framework/hooks-and-runtime.md
  - docs/features/FEAT-0065-pulse-and-interval-automation.md
  - docs/features/FEAT-0029-goal-packet-architecture-for-native-codex-goals.md
  - skills/skill-maintenance/scripts/farplane_lifecycle_graph.py
  - skills/skill-maintenance/scripts/generate_farplane_lifecycle_graph.py
  - .farplane/generated/graphs/farplane-lifecycle-graph.json
---

# Farplane Lifecycle Graph Contract

The Farplane lifecycle graph is a UI-consumable and agent-consumable projection
of how the framework moves information through skills, files, hooks,
automations, Goal Packets, reports, and drains.

It is not a new runtime. It is a harness map.

```text
build_graph_projection(repo_root, projection_profile)
  -> nodes[] + edges[] + fsa_projections? + extraction_report?
```

The generated graph surfaces are sibling projections over a shared GraphIR:

- `skill-registry`: skill registry nodes, Markdown references, common chains,
  workflow chains, and rendered skill docs.
- `harness-reference`: local file/doc references for cleanup and navigation.
- `farplane-lifecycle-core`: compact semantic lifecycle graph for UI and agent
  context.
- `farplane-lifecycle-full`: audit lifecycle graph with optional gate,
  abstract-state, and FSA-state nodes.

The lifecycle graph is not a child projection of the skill graph. It needs
non-skill entities such as hooks, automations, reports, ticket files, runtime
state, curated framework edges, and finite-state projections.

## Node Contract

```text
LifecycleNode = {
  id: string,
  kind: skill | file | state | hook | automation | report | ticket |
        doc | gate | fsa_state | runtime | command | route,
  label: string,
  path?: string,
  owner?: string,
  tags: string[],
  metadata?: object
}
```

Node IDs are stable strings. File-like IDs use repo-relative paths, such as
`file:farplane/metrics.yaml`. Skills use `skill:<name>`. FSA states use
`fsa:<projection-id>:<state-id>`.

## Edge Contract

```text
LifecycleEdge = {
  source: string,
  target: string,
  type: reads | writes | routes_to | triggers | guards | updates |
        documents | contains | transition | produces | consumes,
  label?: string,
  evidence_ref: string,
  confidence: explicit | parsed | curated
}
```

`confidence` tells readers and UI code how strongly to treat the edge:

- `explicit`: declared in a structured source, such as `hooks.json`.
- `parsed`: extracted from a skill signature or local file text.
- `curated`: added by the generator because a framework spec defines the
  critical path but no single structured line declares it.

No edge should claim `explicit` without a concrete source reference.

## Extraction Rules

The first generator version intentionally parses a small, stable surface:

- `SKILL.md` front matter for `name`, `description`, `tier`, `group`, and
  `source`.
- `SKILL.md` `## Todo List` sections for ordered todo-chain edges. The parser
  records first-seen explicit skill references in order: Markdown `SKILL.md`
  links, backticked `skill-name` refs, or `$skill-name` refs. It does not read
  plain prose or Reference Map prose as execution order.
- `.farplane/events/*.jsonl` skill telemetry for observed skill heat. Graph
  prominence is generated from behavior instead of a hand-maintained workflow
  marker.
- `## Skill Signature` blocks for `state: reads(...)`, `writes(...)`,
  `gates:`, and `routes:`.
- `hooks.json` for Codex hook events and command hook targets.
- a curated framework map for lifecycle-critical files and state nodes.

The parser should prefer omission over hallucination. Ambiguous state phrases
become `state:*` nodes with `parsed` confidence instead of fake file paths.
Routes that do not name an installed skill become `route:*` nodes rather than
fake `skills/<name>/SKILL.md` paths. Method addresses such as `research:gap`
route to the base skill when that skill exists.
Framework-critical edges that are true but not machine-declared use
`curated` confidence and cite the owning doc.

The default generated artifact is the `core` graph. It omits gate nodes, FSA
state nodes, and abstract prose-derived state nodes so the main UI can focus on
how concrete framework files are consumed. Use `--full`, `--include-gates`,
`--include-abstract-state`, or `--include-fsa-nodes` when auditing parser
detail.

Projection profiles live in
`skills/skill-maintenance/scripts/graph_projection_config.py`. Keep them as
small named Python configs until a non-Python consumer needs an external
JSON/YAML config file. This keeps profile behavior typed, testable, and close
to the generator code while the model is still settling.

## Finite State Projections

The graph includes finite state projections for views that are easier to render
as lifecycle tracks than as a dense network.

```text
FsaProjection = {
  id: string,
  label: string,
  start: string,
  terminal: string[],
  states: string[],
  transitions: LifecycleEdge[]
}
```

Required projections:

- `project_initialization`: operator intent to initialized Farplane substrate,
  goal intake, and first Goal Advisor handoff.
- `automation_activation`: reviewed automation prompts to Pulse and Interval
  thread/automation activation and PM UI grouping.
- `ticket_goal_execution`: selected ticket to implementation plan, Goal
  Packet, native Goal, QA/demo/review proof, and closeout.
- `memory_drain_upkeep`: reports/troubles/lessons to update-memory,
  skill-maintenance, evals, and compressed durable context.
- `self_update_loop`: Weekly Interval report to goals-delta decision,
  leverage/harness placement, Goal Advisor handoff, Pulse execution, reward
  signal, and next weekly review.

The FSA is a projection over the graph, not a claim that Farplane has one
central state machine. A project can be initialized while another ticket is in
Goal execution and a drain is also due.

## UI Use

The Farplane UI can start with three views:

- `critical_path`: a left-to-right lifecycle view for new users.
- `skill_io`: skill-to-file reads/writes, useful for model context and impact
  analysis.
- `fsa`: selectable finite state projections for init, automations, Goal
  execution, and upkeep.

Graph consumers should render unknown or abstract `state:*` nodes differently
from concrete file nodes. They should also expose edge confidence so humans can
decide whether a relationship came from code/config, a skill signature, or a
curated framework rule.
