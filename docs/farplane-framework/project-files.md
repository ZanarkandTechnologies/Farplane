---
title: Project Files
status: active
owner: harness
created_at: 2026-06-15
updated_at: 2026-07-14
framework_template_version: "0.3.0"
source_of_truth:
  - docs/farplane-framework/README.md
  - farplane/manifest.json
  - farplane/harness.yaml
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
direction, selected metrics, thresholds, constraints, refs, provider coordinates, and
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
  harness.yaml
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

### `farplane/harness.yaml`

Typed human charter: identity, planning areas with canonical per-area ICPs and
planner instructions, feature meaning, operating principles, non-tradeoffs, durable
leverage commitments, allocation guardrails, authority, stable capability
references, selected metric refs, and optional dated metric goals.

This is the owner for the human idea the system must preserve. Agents may
propose changes with evidence, but protected charter changes require explicit
human approval. Areas group metric and history context for one adaptive
planner; they do not own planners, workers, quotas, controllers, budgets,
progress, or strategy. Capability references identify workflows; the
referenced skills own their procedures.

`goals` is the only optional target layer. Each row binds a unique `goal_id` to
one selected objective `metric_id`, a numeric `target_value`, and an ISO
`target_date`. It does not copy metric direction or store mutable progress:

```text
goal_progress(goal, metric_definition, current_observation)
  -> active | completed | unknown

maximize: completed when current >= target_value
minimize: completed when current <= target_value
```

Plan Next Wave may use an active goal's target and date as urgency evidence.
Once current metric evidence satisfies the direction-derived comparison, the
goal is completed and stops adding urgency. Missing or stale evidence never
proves completion. Projects without a dated target use `goals: []` or omit the
field; no separate goals file or changing goal-status ledger is introduced.

Each area is a complete planning record:

```text
harness.areas.<area_id> =
  description + icp + planner_instruction + skill_refs + metric_refs
```

`icp` names the people served by the area, their relevant jobs and pains, and
the evidence bar that would change their belief or workflow. This is canonical
human meaning. Feed Scout may render it into persistent memory and add observed
current context, but external evidence cannot silently rewrite it.

`planner_instruction` is the canonical candidate-generation policy for that
area. Plan Next Wave reads every scope-relevant complete area record before
generating candidates. Pulse, Dogfood, reports, and automations pass or point
to this record; they do not maintain competing area-policy paraphrases.

Use typed YAML. Do not add a custom harness DSL, live backlog, worker
allocation table, mutable goal status, or product controller state here.

### `farplane/automations.toml`

Human-reviewable desired state for Codex automations. It contains exactly one
Work Pulse heartbeat plus separate cron/manual jobs such as Feed Scout,
Daily/Weekly BAU, Dogfood self-improvement, and low-frequency maintenance.

Each record owns its schedule, workspace, status, and exact project-specific
prompt. Generic workflow behavior remains in the called skill. Scheduled
sources write reports and bounded candidate context; Work Pulse owns normal
proactive ticket admission and execution.

### `.farplane/feed-scout/memory.md`

One ignored, update-in-place Markdown synthesis of canonical ICP profiles,
current trends, notable things, and source gaps. It is a cheap retrieval surface
for Feed Scout, Plan Next Wave, Pulse, and ticket-owned artifact work—not a
snapshot archive, monthly trend ledger, planner, or source of authority.

### `farplane/metrics.yaml`

This file owns metric meaning and acquisition. Reusable `refreshers` group one
prompt or owner-skill call that can provide several metrics; flat metric
definitions select that group with `refresh_ref`. A metric may instead carry
one inline `refresh`, but never both. The Daily Interval agent resolves stale
selected metrics into unique groups, executes each prompt once, and stores
separate flat observations.

Canonical reusable metric semantics. Each definition owns its stable ID,
label, description, unit, display behavior, direction, freshness, pinned state,
and optional hard-guard operator/threshold. `harness.yaml` selects active
objectives/guards and owns objective priority. Unselected non-guard metrics are
tracked observations, not ordinary planner context.

Metric observations remain generated runtime evidence under `.farplane/`; this
tracked file defines what the observations mean, not their current values.

### `farplane/bindings.yaml`

Non-secret connector and provider coordinates: safe IDs, URLs, labels,
aliases, source configuration, and dashboard refs. Secrets are runtime inputs supplied by environment or private
local config, never tracked here. Metric meaning and refresh prompts belong in
`metrics.yaml`; bindings contain only non-secret project/provider coordinates,
which refresh prompts may resolve when calling their owner tools.

`integrations.kanban` selects the work-evidence provider for generic reporting
workflows. `filesystem_tickets` uses safe project-relative ticket directories.
`notion` uses a named private-handle alias and the existing private-context plus
`ntn` boundary; the binding never stores the resolved database ID, URL, or
credential. `filesystem_ticket_policy: exclude` is a hard no-fallback gate:
provider access failures become source gaps rather than permission to inspect
`tickets/**`.

### `farplane/hooks.json`

Declarative typed file-event capture configuration. Core owns event identity,
durable outbox/snapshots, route validation, mining runs, and lean reports;
`bindings.yaml` maps local event names to immutable Core programs. Hooks observe
and route; they do not own continuation or ticket planning, and no daemon is
required.

### `.agents/skills/`

Project-local capability workflows. Use this when an important recurring
artifact or operation is specific to one company/project and no reusable root
skill already owns it:

```text
.agents/skills/<capability>/SKILL.md
```

Reference these skills from `harness.yaml`, tickets, or automation prompts as
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
  events/
  file-events/
  mine/
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
mode, `harness-creator` grounds the typed charter, planning areas/instructions,
required capabilities, feedback loops, missing-system tickets, and selected
metric objectives.

A clean project is not considered ready merely because files exist. Readiness
requires:

- a grounded charter and authority boundary;
- at least one honest selected objective in `farplane/harness.yaml`;
- selected objective and guard IDs resolve to metric definitions and bindings;
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
