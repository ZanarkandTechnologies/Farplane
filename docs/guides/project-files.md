---
title: Project Files
status: active
owner: harness
created_at: 2026-06-15
updated_at: 2026-10-15
framework_template_version: "0.4.0"
source_of_truth:
  - docs/guides/README.md
  - farplane/manifest.json
  - farplane/harness.yaml
  - farplane/metrics.yaml
  - farplane/automations/
  - docs/guides/reporting.md
  - docs/guides/wiki-and-entities.md
  - farplane/bindings.yaml
  - .agents/skills/README.md
  - farplane/pm.json
  - farplane/capability-profiles.yaml
  - .gitignore
---

# Project Files

Farplane separates tracked project policy from ignored runtime state:

```text
farplane/       tracked project framework config
.agents/skills/ tracked project-local capability skills
.farplane/      ignored reports, observations, generated views, eval runs, and logs
docs/           durable human-readable system memory
tickets/        issue templates and the frozen legacy archive (work lives in GitHub Issues)
skills/         reusable cross-project workflows
```

## Minimality Rule

Project files are declarative: identity, value direction, selected metrics,
thresholds, constraints, refs, provider coordinates, and approved boundaries.

They never contain orchestration algorithms, worker pools, ordered procedures,
check-in implementations, review procedures, or repeated agent instructions.
Put those in skills, small hooks/validators, or the owning issue's
`## Goal program`, where behavior can be tested and resumed.

## Tracked Framework Config

```text
farplane/
  README.md
  manifest.json
  harness.yaml
  metrics.yaml
  automations/
  bindings.yaml
  pm.json
  capability-profiles.yaml

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

Typed human charter: identity with stable problems, planning areas with canonical per-area ICPs, feature meaning,
operating principles, non-tradeoffs, durable leverage commitments, allocation
guardrails, authority, stable capability references, selected metric refs, and
planner skill allowlists.

This is the owner for the human idea the system must preserve. Agents may
propose changes with evidence, but protected charter changes require explicit
operator approval. Areas group metric and history context for one adaptive
planner; they do not own planners, workers, quotas, controllers, budgets,
progress, or strategy. Capability references identify workflows; the
referenced skills own their procedures.

Mutable strategy does not live in `harness.yaml`. Project-level dated goals and
product-bet portfolios are retired active surfaces. Stable intent constrains
review and refill through problems, areas, authority, selected metrics, and
configured skills; chosen interventions live on tickets with priority,
optional `due_at`, dependencies, proof, Reward, and Goal Packets when needed.

Each area is passive planning context, never a planner, quota, budget, or
strategy:

```text
harness.areas.<area_id> =
  description + icp + skill_refs + metric_refs
```

`icp` names the people served by the area, their relevant jobs and pains, and
the evidence bar that would change their belief or workflow. This is canonical
human meaning. Feed Scout may render it into Scout Brief and add observed
current context, but external evidence cannot silently rewrite it.

`planning.skill_refs` is the allowlist of skills a planner may call. Each skill's
`planner_contract` owns its required arguments, while its skill body owns the
workflow. A planner may use areas to ground audience and metrics but may not derive
new work types from area prose.

Use typed YAML. Do not add a custom harness DSL, live backlog, worker
allocation table, mutable goal status, product-bet portfolio, project strategy
ledger, or product controller state here.

### `farplane/automations/`

Committed desired state for the project's scheduled jobs: one `*.md` file per
live routine, tagged with the `runtime` (`claude` or `codex`) and `runtime_task`
that run it, so a job runs on one side only. Steps a job calls live in
`farplane/automations/steps/` and are never scheduled on their own. A project
with no jobs has an empty or absent folder; automation-advisor adds jobs from its
templates. Generated run data stays in ignored `.farplane/`.

YAML front matter owns identity, schedule, workspace, and status. The Markdown
body is the exact project-specific prompt. Generic workflow behavior remains in the called skill. Scheduled
sources are cron records that write reports and bounded candidate context;
they never create or execute work. Work enters as a GitHub issue in the
project's own repository and runs through `goal-advisor` (native Goal), or
directly when small.

### `.farplane/feed-scout/scout-brief.md`

One ignored, update-in-place Markdown Scout Brief synthesis of canonical ICP profiles,
current trends, notable things, and source gaps. It is a cheap retrieval surface
for Feed Scout and ticket-owned artifact work—not a
snapshot archive, monthly trend ledger, planner, or source of authority.

### `farplane/metrics.yaml`

This file owns metric meaning and acquisition. Reusable `refreshers` group one
prompt or owner-skill call that can provide several metrics; flat metric
definitions select that group with `refresh_ref`. A metric may instead carry
one inline `refresh`, but never both. The Morning chain's
[Metrics Refresh](../../farplane/automations/steps/metrics-refresh.md) step
(`farplane metrics refresh`) resolves stale selected metrics into unique
groups, runs each group once, and stores separate flat observations.

A metric needs two things: its id (the name; `label` defaults to it) and how to
read it (`refresh` or `refresh_ref`). Everything else has a default, filled by
`with_metric_defaults` in `bin/core/farplane_metric_schema.py` wherever the file
is read: `type: stock`, `unit: count`, `direction: maximize`, `max_age_days: 7`,
and `display` from the type (a flow charts as daily bars plus the running total,
a stock as a line). Write a field only when the default is wrong for that
metric. Flow means additive activity; stock means a point-in-time balance.
`harness.yaml` selects active objectives/guards and owns objective
priority. Unselected non-guard metrics are tracked observations, not ordinary
planner context.

`type: markdown` is the deliberately narrow exception for one current,
qualitative claim: its dated observation value is one non-empty Markdown
paragraph. It has no unit, direction, target, guard, display, comparison,
series, or cumulative projection. Core selects the latest valid paragraph as
of the requested window end; it neither sums nor invents a trend. A same-day
repeat with identical text dedupes, while conflicting text or malformed/missing
refresh output becomes a dated source gap and leaves the last valid paragraph
intact. A project may declare at most one `leverage: edge` Markdown metric; it
is `pinned: true` but stays unselected so Daily can refresh it without making it
a planner objective. Numeric `leverage: distribution` only labels existing
flow/stock evidence for the read-only global Leverage projection. Account
collectors attach `distribution_account: {platform, account_id, label}` to their
ignored dated observation payload; Core carries that observed identity to the
raw distribution card. The global projection groups only by `platform` plus
`account_id`, never by a metric name, display label, or project. Account IDs do
not belong in tracked `metrics.yaml` or the browser response; missing identity
is an explicit evidence gap until a collector refresh supplies it.

Dated facts remain canonical runtime evidence. The snapshot or UI caller
supplies an inclusive calendar window and timezone. Core then derives
the current-window value, the preceding equal-window absolute and percentage
delta, a direction-normalized improving/flat/worsening trend, and a cumulative
total for flows only. Flows sum within windows; stocks use the latest known
reading at each window boundary and never accumulate. Do not store formula,
cadence, comparison, aggregation, cumulative, or window configuration here,
and do not author duplicate growth, timeframe, or cumulative metrics.
`metrics.yaml` has no formula language and never defines one metric from
others; a refresher may record a derived business fact (for example `profit`)
as its own observed metric.

Metric observations remain generated runtime evidence under `.farplane/`; this
tracked file defines what the observations mean, not their current values.

For Leverage, the project snapshot compiler materializes the explicit
Distribution and Edge cards in `.farplane/project/ui/latest.json`. That is a
read-only handoff to the bunker (Farplane-UI-v2); company Capital remains Finance-owned state,
outside the project metric store.

### `farplane/bindings.yaml`

Non-secret connector and provider coordinates: safe IDs, URLs, labels,
aliases, source configuration, and dashboard refs. Secrets are runtime inputs supplied by environment or private
local config, never tracked here. Metric meaning and refresh prompts belong in
`metrics.yaml`; bindings contain only non-secret project/provider coordinates,
which refresh prompts may resolve when calling their owner tools.

`integrations.kanban.provider` selects the work-evidence provider for generic
reporting workflows. `github_issues` reads the repository named in
`integrations.github.repo`; Farplane's own bindings use it with
`filesystem_ticket_policy: exclude`. `filesystem_tickets` uses safe
project-relative ticket directories and survives only for legacy projects.
`notion` uses a named private-handle alias and the existing private-context plus
`ntn` boundary; the binding never stores the resolved database ID, URL, or
credential. `filesystem_ticket_policy: exclude` is a hard no-fallback gate:
provider access failures become source gaps rather than permission to inspect
`tickets/**`.

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
runtime automation IDs, worker state, or strategy; each automation record names
its own `runtime` and `runtime_task`.

### `farplane/capability-profiles.yaml`

Optional restriction-only policy for the one visual Project PM. A missing
binding means full access; it never means a default persona or a second
persistent worker. Each selected profile has an explicit `allow.skill_ids` and
`allow.mcp_server_ids` list. Farplane's own checkout has no project file;
the `farplane capability-profiles` commands are due for a re-audit now that
the archived Farplane UI server no longer calls them ([CLI](cli.md#known-gaps)). Project profiles may extend a `global:<id>` from
`~/.farplane/capability-profiles.yaml`; their effective access is the
intersection, so a local profile cannot widen a global restriction.

Core validates the portable schema and resolves global/project inheritance.
The selected runtime adapter checks allowed IDs against its live inventory;
Codex compiles the result into a fresh `thread/start.config` and records one
immutable launch receipt at
`.farplane/capability-profiles/sessions/`. `pm.json` remains thread grouping
only. Use `farplane capability-profiles read|write|snapshot` rather than
hand-editing generated thread configuration.

## Tickets Own Work And Evidence

```text
GitHub issue <n> in the project's own repository
  body: ticket sections
  body: ## Goal program?
  body: ## Current Goal state?
  Goal turn comments?
  proof comment
  linked artifacts (repository files or attachments)
```

The issue body is the executable contract and compact task memory. `## Goal
program` owns Goal/check-in loop instructions; `## Current Goal state` holds the
latest checkpoint; Goal turn comments are append-only execution history; linked
repository files or attachments own implementation, QA, review, and supporting
evidence. Do not store QA or review receipts in a detached project-level
evidence folder.

Issue templates and the issue workflow (`tickets/README.md`) remain tracked
under `tickets/`, beside the frozen legacy archive.

## Ignored Runtime State

`.farplane/` contains generated or local state, never a competing strategy
owner:

```text
.farplane/
  views.yaml
  entities/
  wiki/
  reports/
  metrics/
  project/ui/
  automation/
  events/
  mine/
  state/
  evals/runs/
  logs/
  capability-profiles/sessions/
```

Hooks write their runtime state here too: `state/message-windows/` (user
turn), `events/`, `logs/`, and `evals/runs/`. Global hook receipts live under
`~/.farplane/state/` (`hook-delivery/`, `stop-gate/decisions.jsonl`,
`skill-invocations/`); see [Hooks And Runtime](hooks-and-runtime.md).

Flat `.farplane/entities/<id>.md` files are canonical local Wiki articles;
`.farplane/views.yaml` is canonical local named membership over those IDs;
their adjacent `index.json`, `graph.json`, and `crm.json` files are generated
views. `.farplane/wiki/wiki.sqlite` is the generated page cache, FTS5 search
index, and originating-page claim store. See [Wiki And Entities](wiki-and-entities.md). Reports are dated context for readers and planners.
Metric observations are raw/normalized readings. UI snapshots and registries
are generated projections over canonical files and runtime evidence. If a
projection is stale, run `farplane wiki rebuild` from its owners rather than
hand-editing it.

Thread notes are not project files. A project's notes live in
`~/.farplane/memory/projects/<project>/`, inside the one local-only memory git
repo, so no pushable checkout ever holds them. See
[Thread notes](wiki-and-entities.md#thread-notes).

The ignored `.farplane/` boundary normally owns generated/runtime state, with
two explicit authored local exceptions: entity Markdown and `views.yaml`.
These remain local because they may contain personal research
and relationship organization. Shared connector/source coordinates still belong in tracked
`farplane/bindings.yaml`; do not introduce a generic `.farplane/config.yaml`.

## Runtime Secrets

Farplane Core resolves secret/runtime values through the process environment
and private local configuration. Use `farplane doctor` for readiness without
printing secret values. Tracked project files contain only non-secret refs and
labels.

## Initialization Contract

`setup-advisor` creates or preserves the minimal tracked config, ignored runtime
folders, issue templates, and optional project-local skill home; its
[critical path](../../skills/setup-advisor/references/critical-path.md) owns
the bootstrap order. In `full`
mode, `setup-advisor` grounds the typed charter, planning areas/instructions,
required capabilities, feedback loops, missing-system tickets, and selected
metric objectives.

A clean project is not considered ready merely because files exist. Readiness
requires:

- a grounded charter and authority boundary;
- at least one honest selected objective in `farplane/harness.yaml`;
- selected objective and guard IDs resolve to metric definitions and bindings;
- an owned capability route for required recurring outputs, or a refinement
  ticket;
- GitHub Issues (or the configured `integrations.kanban` provider) as the work
  and proof surface;
- cron records only when live automation is requested (no execution
  heartbeat; work enters through GitHub Issues and `goal-advisor`);
- explicit source gaps for unavailable metrics, access, or integrations.

## Migration Rule

When removing an obsolete project file, migrate every active reader and
validator first, prove the project can initialize and operate without it, then
delete the source. Do not retain aliases, fallback parsers, empty directories,
or generated compatibility indexes unless a public contract explicitly
requires them.
