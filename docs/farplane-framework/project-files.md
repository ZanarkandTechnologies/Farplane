---
title: Project Files
status: active
owner: harness
created_at: 2026-06-15
updated_at: 2026-07-11
framework_template_version: "0.3.0"
source_of_truth:
  - docs/farplane-framework/README.md
  - farplane/manifest.json
  - farplane/harness.md
  - farplane/goals.yaml
  - farplane/metrics.yaml
  - farplane/automations.toml
  - docs/farplane-framework/reporting.md
  - farplane/bindings.yaml
  - farplane/hooks.json
  - .agents/skills/README.md
  - farplane/pm.json
  - .gitignore
---

# Project Files

Farplane separates tracked project policy from ignored runtime state:

```text
farplane/       tracked project framework config
.agents/skills/ tracked project-local capability skills
.farplane/      ignored reports, observations, generated views, eval runs, and logs
docs/           durable human-readable system memory
tickets/        executable work, Goal Packets, progress, QA, and review evidence
skills/         reusable cross-project workflows
```

## Minimality Rule

Project files are declarative state. They may contain identity, value
direction, goals, thresholds, constraints, refs, provider coordinates, and
human-approved boundaries.

They must not contain orchestration algorithms, worker pools, ordered artifact
procedures, check-in implementations, review procedures, or repeated agent
instructions. Put those in skills, small hooks/validators, or the owning ticket
`program.md`, where behavior can be tested and resumed.

## Tracked Framework Config

```text
farplane/
  README.md
  manifest.json
  harness.md
  goals.yaml
  metrics.yaml
  automations.toml
  bindings.yaml
  hooks.json
  pm.json

.agents/
  skills/
    README.md
    <capability>/SKILL.md?
```

### `farplane/manifest.json`

Versioned project spec and compact UI identity. It names standard tracked and
ignored paths and carries `project.name`, `project.description`, and
`project.archetype`. It is not a strategy document or workflow catalog.

### `farplane/harness.md`

Static human charter: mission, thesis, operating principles, non-tradeoffs,
durable leverage commitments, allocation guardrails, agent authority, change
rule, and stable capability references.

This is the owner for the human idea the system must preserve. Agents may
propose changes with evidence, but material charter changes require explicit
human approval. Capability references identify important recurring workflows;
the referenced skills own their procedures.

Use YAML front matter plus Markdown sections. Do not add a custom harness DSL,
live backlog, worker allocation table, or changing goal state here.

### `farplane/goals.yaml`

Project-level value direction and strategy: north star, value function, goal
axes, SMART goals, stable KPI IDs, current bets, current milestone, and holds.
Goals do not need execution-lane foreign keys. Capability skills consume goals
as inputs but do not own parallel goal trees.

```yaml
goals:
  improve_harness:
    name: Improve autonomous usefulness
    smart_goals:
      - id: accepted_improvement_rate
        target: Ship and verify two meaningful improvements this month.
        kpis:
          - id: accepted_harness_improvements
            target: 2
            direction: above
        interpretation: Count only ticket-backed improvements with proof.
```

`horizon-advisor` owns material long-horizon deltas. Ticket planners read this
file when ranking work; they do not rewrite it merely because the board is
empty.

### `farplane/automations.toml`

Human-reviewable desired state for Codex automations. It contains exactly one
Work Pulse heartbeat plus separate cron/manual jobs such as Feed Scout,
Daily/Weekly BAU, Dogfood self-improvement, and low-frequency maintenance.

Each record owns its schedule, workspace, status, and exact project-specific
prompt. Generic workflow behavior remains in the called skill. Scheduled
sources may write reports and their bounded ticket class; they do not execute
the tickets they create.

### `farplane/metrics.yaml`

Canonical metric semantics: stable ID, label, description, unit, kind, display
behavior, and pinned state. Goal KPI refs must resolve to this catalog; target
and direction remain goal-specific in `goals.yaml`.

Metric observations remain generated runtime evidence under `.farplane/`; this
tracked file defines what the observations mean, not their current values.

### `farplane/bindings.yaml`

Non-secret connector and provider coordinates: safe IDs, URLs, labels,
aliases, source configuration, dashboard refs, and metric-provider refresh
instructions. Secrets are runtime inputs supplied by environment or private
local config, never tracked here. Metric meaning belongs in `metrics.yaml`;
this file explains how a provider can obtain or refresh a reading.

### `farplane/hooks.json`

Declarative hook configuration. Hook algorithms belong in installed runtime
shims, skills, scripts, or validators. Hooks observe and gate; they do not own
continuation or ticket planning.

### `.agents/skills/`

Project-local capability workflows. Use this when an important recurring
artifact or operation is specific to one company/project and no reusable root
skill already owns it:

```text
.agents/skills/<capability>/SKILL.md
```

Reference these skills from `harness.md`, tickets, or automation prompts as
needed. Promote one into root `skills/` only after repeated cross-project proof.
Do not create a local skill merely to preserve a retired category or planning
controller.

### `farplane/pm.json`

Optional UI grouping glue for chat and automation thread IDs. It does not own
runtime automation IDs, worker state, or strategy.

## Tickets Own Work And Evidence

```text
tickets/TASK-XXXX/
  ticket.md
  program.md?
  progress.md?
  artifacts/
    qa/
    review/
```

The ticket is the executable contract and compact task memory. `program.md`
owns Goal/check-in loop instructions; `progress.md` is append-only execution
history; `artifacts/` owns implementation, QA, review, and supporting evidence.
Do not store QA or review receipts in a detached project-level evidence folder.

Active project tickets are normally ignored local work state while ticket
templates and board docs remain tracked, subject to the repository's explicit
policy.

## Ignored Runtime State

`.farplane/` contains generated or local state, never a competing strategy
owner:

```text
.farplane/
  reports/
  metrics/
  project/ui/
  automation/
  state/
  evals/runs/
  logs/
```

Reports are dated context for readers and planners. Metric observations are
raw/normalized readings. UI snapshots and registries are generated projections
over canonical files and runtime evidence. If a projection is stale, rebuild
it from its owners rather than hand-editing it.

## Runtime Secrets

Farplane Core resolves secret/runtime values through the process environment
and private local configuration. Use `farplane doctor` for readiness without
printing secret values. Tracked project files contain only non-secret refs and
labels.

## Initialization Contract

`init-advisor` creates or preserves the minimal tracked config, ignored runtime
folders, ticket/QA surfaces, and optional project-local skill home. In `full`
mode, `harness-creator` grounds the charter, goals, required capabilities,
feedback loops, missing-system tickets, and current milestone.

A clean project is not considered ready merely because files exist. Readiness
requires:

- a grounded charter and authority boundary;
- a usable project goal contract;
- metric IDs in goals resolve to `farplane/metrics.yaml`;
- an owned capability route for required recurring outputs, or a refinement
  ticket;
- an executable board and proof surface;
- one Work Pulse heartbeat when live automation is requested;
- explicit source gaps for unavailable metrics, access, or integrations.

## Migration Rule

When removing an obsolete project file, migrate every active reader and
validator first, prove the project can initialize and operate without it, then
delete the source. Do not retain aliases, fallback parsers, empty directories,
or generated compatibility indexes unless a public contract explicitly
requires them.
