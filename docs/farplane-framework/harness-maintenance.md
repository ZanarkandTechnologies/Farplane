---
title: "Harness Maintenance Features"
status: active
owner: farplane-framework
created_at: 2026-06-24
updated_at: 2026-06-24
framework_template_version: "0.2.0"
tags:
  - farplane
  - maintenance
  - registry
  - graph
  - rollout
refs:
  - docs/farplane-framework/graph-contract.md
  - docs/farplane-framework/lifecycle.md
  - docs/systems/README.md
  - docs/systems/registry.jsonl
  - docs/features/registry.jsonl
  - docs/templates/registry.jsonl
  - docs/skills/README.md
  - docs/templates/README.md
  - skills/skill-maintenance/graph/README.md
  - bin/README.md
---

# Harness Maintenance Features

Farplane now has a small maintenance OS for keeping the harness visible,
auditable, and UI-renderable.

```text
harness_maintenance(repo_root, project_roots?)
  -> inventories
   + rollout_reports
   + graph_projections
   + validators
   + CLI/UI payloads
```

The important distinction: source metadata, generated registries, rollout,
graph, and CLI are separate layers. System docs own authored `SYS-*` metadata.
Feature docs own authored `FEAT-*` metadata. Generated registries expose
queryable inventory. Rollout reports compare consumers against current
templates or manifests. Graphs show relationships. CLI commands expose stable
JSON payloads for humans and Farplane UI.

## Shared Services Boundary

Overlapping surfaces must share service logic instead of reimplementing the
same interpretation in each generator, CLI command, or UI route.

| Shared Service | Owned Logic | Consumers |
| --- | --- | --- |
| `bin/validators/template_usage.py` | Parse and validate `template_uses`, including the canonical consumer declaration shape. | Template registry checks, skill registry sync, template intelligence, project adoption CLI. |
| `bin/validators/sync_skill_registry.py` | Convert `skills/*/SKILL.md` frontmatter, todo links, and Markdown links into `docs/skills/registry.jsonl`. | Skill graph, skill template rollout, skill OS checks, skill rollout CLI. |
| `skills/skill-maintenance/scripts/generate_template_intelligence.py` | Compute skill template rollout and high-impact template rollout. | `skill-template-intelligence.json`, graph viewer, `farplane skills rollout scan`. |
| `skills/skill-maintenance/scripts/graph_ir.py` | Shared graph node/edge/bundle structs, JSON/JS writers, comparison, and endpoint validation. | Skill graph, harness reference graph, lifecycle graph. |
| `skills/skill-maintenance/scripts/graph_projection_config.py` | Named graph projection profiles and output targets. | Graph dispatcher, compatibility graph wrappers, Farplane UI graph routes. |
| `skills/skill-maintenance/scripts/graph_projection.py` | Generic graph filtering, projection writing, and stale-output checks. | Projection dispatcher and graph tests. |
| `bin/core/farplane_adoption.py` | Project manifest adoption and feature/template drift resolution. | `farplane adoption scan`, Farplane UI project rollout views. |
| `bin/core/farplane_skill_rollout.py` | Read-only UI-facing normalization over generated skill/template rollout intelligence. | `farplane skills rollout scan`, Farplane UI skill rollout views. |
| `bin/core/farplane_harness_health.py` | Compile transparent skill, rollout, latest-eval health, and actionable priority-skill/source-gap readings from generated artifacts and local eval runs. | `farplane harness health compile`, local planners, Farplane UI health views. |
| `bin/core/farplane_primitive_metrics.py` | Deterministic primitive reducers over tickets, project bindings, local Codex stores, and ignored Farplane runtime state. | `farplane metrics primitives`, interval-update, project snapshot compiler, Farplane UI metric tabs. |
| `bin/core/farplane_project_snapshot.py` | Read-only project/company projection joining canonical files, primitive readings, Feed Scout artifacts, and source gaps. | `farplane project snapshot`, Farplane UI Overview/Goals/Products/Distribution/News tabs, interval context. |

Rule of thumb:

```text
UI route or CLI projection
  -> read shared payload or generated artifact
  -> normalize for display
  -> never recompute registry, rollout, or graph semantics from scratch
```

## Quick Map

| Feature | Source Of Truth | Generated / Output Surface | Main Commands | Purpose |
| --- | --- | --- | --- | --- |
| System metadata | `docs/systems/*.md` `system_record_json` | Authored `SYS-*` records grouped by public product module | `python3 docs/features/validate_features.py --write` | Track the small system stack humans should reason about. |
| Feature metadata | feature pages in `docs/features/` `feature_record_json` | Authored first-class `FEAT-*` feature docs linked from one owning system | `python3 docs/features/validate_features.py --write` | Keep only docs-worthy feature handles with their own surfaces, evidence, limits, and metrics. |
| System registry | `docs/systems/registry.jsonl` | Generated system rows grouped by ID, primary feature, refs, and limits | `python3 docs/features/validate_features.py` | Queryable public system inventory consumed by docs and future UI. |
| Feature registry | `docs/features/registry.jsonl` | Generated feature rows grouped by ID, system, status, category, surfaces, refs, evidence, and limits | `python3 docs/features/validate_features.py` | Queryable feature output consumed by adoption, templates, sources, and docs. |
| Template registry | `docs/templates/registry.jsonl` | `path`-resolved template rows and template rollout rows | `python3 bin/validators/sync_template_registry.py --write` | Track high-impact templates, versions, feature refs, and consumer scopes. |
| Project manifest adoption | `farplane/manifest.json` in each project plus the Farplane standard manifest | `farplane adoption scan --json` | `python3 bin/farplane.py adoption scan --project-root . --json` | Show project spec/template drift, local skill presence, and explicit or implied feature adoption. |
| Primitive metrics | tickets, `farplane/bindings.yaml`, local Codex stores, `.farplane/mine/runs/**/input.json` | `.farplane/metrics/daily/YYYY-MM-DD.json`, `.farplane/metrics/observations/**` | `python3 bin/farplane.py metrics primitives --project-root . --date YYYY-MM-DD --json` | Produce Core-owned readings for ticket/KPI/product counts, KPI-attributed ticket ratio, Codex thread usage, burn source gaps, and ticket/thread association backfill. |
| Metric refresh plan | `farplane/metrics.yaml` refreshers plus current observations | agent-owned refresh groups and flat observations | `python3 skills/interval-update/scripts/metric_refresh.py refresh-plan --metrics-file farplane/metrics.yaml --date YYYY-MM-DD --metric-id <id>` | Deduplicate prompt/provider acquisition by refresher ID; the Daily Interval agent executes prompts, while Core remains deterministic. |
| Project snapshot | canonical project files plus primitive metric outputs | `.farplane/project/ui/latest.json` | `python3 bin/farplane.py project snapshot --project-root . --json` | Give Farplane UI and intervals one read-only project/company payload without making the snapshot a source of truth. |
| Skill registry | `skills/*/SKILL.md` front matter, direct todo lists, and Markdown links | `docs/skills/registry.jsonl` | `python3 bin/validators/sync_skill_registry.py --write` | Inventory skills without hand-maintaining a second registry. |
| Skill template rollout | `docs/skills/registry.jsonl` plus `docs/skills/templates/SKILL_TEMPLATE.md` metadata | `skills/skill-maintenance/graph/skill-template-intelligence.json` fields `rollout` and `rollout_summary` | `python3 skills/skill-maintenance/scripts/generate_template_intelligence.py` | Show which skills are current, stale, missing, or external for the current skill template. |
| Template rollout | `docs/templates/registry.jsonl` plus consumer `template_uses` fields | `skill-template-intelligence.json` fields `template_rollout` and `template_rollout_summary` | `python3 skills/skill-maintenance/scripts/generate_template_intelligence.py` | Show high-impact template adoption across skills and projects. |
| Skill rollout CLI | Skill registry plus template intelligence artifact | `farplane skills rollout scan --json` | `python3 bin/farplane.py skills rollout scan --json` | Stable UI-facing payload for skill/template rollout without reading graph internals directly. |
| Harness health projection | Skill graph/docs, skill rollout intelligence, registry, and local eval runs | `.farplane/state/harness-health.json` and `.farplane/metrics/observations/harness_health/YYYY-MM-DD.json` | `python3 bin/farplane.py harness health compile --project-root . --date YYYY-MM-DD` | Give planners and UI one versioned local bundle plus actionable priority-skill and source-integrity readings without promoting weighted health scores into objectives. |
| Skill graph | `docs/skills/registry.jsonl` plus `.farplane/events/*.jsonl` skill telemetry | `skills/skill-maintenance/graph/skill-graph.json` and `skill-docs.json` | `python3 skills/skill-maintenance/scripts/generate_skill_graph.py` | Visualize skill nodes, skill docs, observed skill heat, Markdown links, todo-chain edges, and Tier 3 chain edges. |
| Harness reference graph | Repo Markdown links and literal local paths | `skills/skill-maintenance/graph/harness-graph.json` and doc audit report | `python3 skills/skill-maintenance/scripts/generate_harness_graph.py` | Audit local references, backlink cleanup, unresolved docs paths, and navigation sprawl. |
| Lifecycle graph | Skill signatures, hooks, curated framework files, automations, reports, tickets, and runtime surfaces | `skills/skill-maintenance/graph/farplane-lifecycle-graph.json` | `python3 skills/skill-maintenance/scripts/generate_farplane_lifecycle_graph.py` | Provide semantic framework maps and finite-state projections for UI and agent context. |
| Graph projection dispatcher | Shared GraphIR and projection profiles | selected generated graph JSON/JS | `python3 skills/skill-maintenance/scripts/generate_graph_projection.py --projection <name>` | Route graph generation through one shared model with named projections. |
| Eval system | `skills/*/evals/evals.json`, eval templates, and eval examples | local eval runs and eval reports | `python3 skills/eval/scripts/run_evals.py` | Test skills, prompts, and harness behavior with repeatable tasks and judges. |
| Doc tracker | active docs, registries, local links, and canonical entrypoints | doc-ref validation and generated doc audit report | `python3 bin/validators/check_doc_refs.py` | Keep local references, canonical doc links, and registry refs from rotting. |
| Skill OS checks | skill frontmatter, todo list contracts, capability fixtures, plugin sync, installed-skill import | validators, generated registries, install previews, plugin packages | `python3 skills/skill-maintenance/scripts/check_skills.py --write` | Maintain skill structure, first-load todo tiers, metadata, plugins, and installed-copy hygiene. |

## Rollout Layers

Farplane currently has three rollout/adoption layers.

### Template Rollout

```text
template_rollout(template_registry, consumers.template_uses)
  -> current | stale | missing per consumer/template pair
```

Template rollout answers: "For each tracked high-impact template, which
consumers use the current version, a stale version, or no version?"

Tracked templates live in `docs/templates/registry.jsonl`. Consumers declare
adoption through `template_uses`, for example:

```yaml
template_uses:
  skill-template: "0.3.2"
  skill-eval-task: "0.1.0"
```

JSON consumers use the same shape:

```json
{
  "template_uses": {
    "farplane-framework": "1.3.0"
  }
}
```

The generated report lives in
`skills/skill-maintenance/graph/skill-template-intelligence.json` as
`template_rollout_summary` and `template_rollout`.

### Skill Template Rollout

```text
skill_template_rollout(skill_registry, current_skill_template_version)
  -> current | stale | missing | external per skill
```

Skill template rollout answers: "Which skills have been structurally onboarded
to the current skill template?"

This uses the generated skill registry plus the current skill-template version.
The result also lives in `skill-template-intelligence.json` as
`rollout_summary` and `rollout`.

The new Core CLI projection exposes this through:

```bash
python3 bin/farplane.py skills rollout scan --json
python3 bin/farplane.py skills rollout scan
```

The CLI is read-only. It does not regenerate graph files, change skill
frontmatter, or update templates.

### Project Adoption / Feature Rollout

```text
project_adoption(project_manifest, standard_manifest, generated_feature_registry, template_registry)
  -> project drift + explicit/implied feature adoption
```

Project adoption answers: "Which local Farplane projects are aligned with the
current framework manifest, templates, and feature refs?"

Each project declares its framework state in `farplane/manifest.json`.
The Core CLI reads explicit project roots, a roots file, or known
`~/.farplane` state files:

```bash
python3 bin/farplane.py adoption scan --project-root . --json
python3 bin/farplane.py adoption scan --roots-file ~/.farplane/state/projects.json --json
```

This layer can report:

- manifest presence,
- project spec-version drift,
- tracked template version drift,
- explicit `feature_pins`,
- implied feature adoption from template feature refs,
- local skill presence under project `.agents/skills/`.

It does not crawl the whole computer or mutate project manifests.

## Graph Layers

The graph system has one shared GraphIR toolkit and several named projections.
The graph artifacts are generated inspection and UI surfaces, not runtime state.

```text
build_graph_projection(repo_root, projection_profile)
  -> nodes[] + edges[] + optional finite_state_projections
```

Current projection profiles:

- `skill-registry`: skill registry graph and rendered skill docs.
- `harness-reference`: repo-wide local-reference graph and doc audit report.
- `farplane-framework-core`: manifest-backed Framework Core projection for
  Harness OS Map. Sources come from `farplane/manifest.json`
  `farplane_graph.framework_core.include`; source docs, workflow nodes, direct
  framework file/spec refs, directly mentioned skills, ordered workflow skill
  edges, and curated lifecycle routes are retained. Repo-wide connector
  expansion is intentionally excluded from this operator map.
- `farplane-lifecycle-core`: compact lifecycle graph for UI and agent context.
- `farplane-lifecycle-full`: audit lifecycle graph with optional detail nodes.

The lifecycle graph is not a child of the skill graph. It is a sibling
projection because it needs non-skill surfaces: hooks, automations, reports,
ticket files, runtime state, curated framework edges, and finite-state
projections.

Use the dispatcher when you want the shared projection path:

```bash
python3 skills/skill-maintenance/scripts/generate_graph_projection.py --list
python3 skills/skill-maintenance/scripts/generate_graph_projection.py --projection skill-registry
python3 skills/skill-maintenance/scripts/generate_graph_projection.py --projection harness-reference
python3 skills/skill-maintenance/scripts/generate_graph_projection.py --projection farplane-framework-core
python3 skills/skill-maintenance/scripts/generate_graph_projection.py --projection farplane-lifecycle-core
python3 skills/skill-maintenance/scripts/generate_graph_projection.py --projection farplane-lifecycle-full
```

Use compatibility commands when working on one graph family:

```bash
python3 skills/skill-maintenance/scripts/generate_skill_graph.py
python3 skills/skill-maintenance/scripts/generate_harness_graph.py
python3 skills/skill-maintenance/scripts/generate_farplane_lifecycle_graph.py
```

## Maintenance Command Set

Use these commands as the practical harness-maintenance dashboard until the UI
absorbs more of them.

```bash
# Project and framework adoption
python3 bin/farplane.py adoption scan --project-root . --json

# Skill/template rollout for UI
python3 bin/farplane.py skills rollout scan --json

# Filesystem-backed skill, rollout, and eval health for planners and UI
python3 bin/farplane.py harness health compile --project-root .

# Skill registry and skill contract upkeep
python3 skills/skill-maintenance/scripts/check_skills.py --write
python3 bin/validators/sync_skill_registry.py --check
python3 bin/validators/check_skill_todo_tiers.py
python3 bin/validators/check_skill_capabilities.py validate

# Template registry and template metadata upkeep
python3 bin/validators/sync_template_registry.py --check
python3 bin/validators/check_template_version_metadata.py --all

# Graphs
python3 skills/skill-maintenance/scripts/generate_graph_projection.py --projection skill-registry
python3 skills/skill-maintenance/scripts/generate_graph_projection.py --projection harness-reference
python3 skills/skill-maintenance/scripts/generate_graph_projection.py --projection farplane-framework-core
python3 skills/skill-maintenance/scripts/generate_graph_projection.py --projection farplane-lifecycle-core

# Docs and references
python3 bin/validators/check_doc_refs.py
python3 bin/validators/check_doc_parity.py

# Tickets and task memory
python3 tickets/scripts/check_ticket_metadata.py
```

## Ownership Rules

- Registries are source-of-truth inventories.
- Generated graph files are projections.
- CLI scan commands are stable read-only payloads for humans and UI.
- Skills own workflow semantics, proof expectations, and skill-local surfaces.
- `skill-maintenance` owns generated skill inventory, graph generation, template
  intelligence, and skill-system upkeep.
- Farplane UI owns rendering, navigation, shared state, and product-grade views.
- Project `farplane/manifest.json` owns project adoption state.
- `.farplane/` owns live generated state and reports, not reusable standards.

Do not turn rollout reports into a second source of truth. If a rollout row is
wrong, fix the declaring surface: template registry, skill frontmatter,
consumer `template_uses`, project manifest, or generated registry.

## Mental Model

```text
source declarations
  -> registries
  -> rollout reports
  -> graph projections
  -> CLI/UI payloads
```

Examples:

- Skill frontmatter changes `docs/skills/registry.jsonl`.
- System or feature metadata changes `docs/systems/registry.jsonl` and
  `docs/features/registry.jsonl` through
  `docs/features/validate_features.py --write`.
- Template metadata changes `docs/templates/registry.jsonl`.
- `template_uses` changes template rollout.
- `skill_template_version` changes skill template rollout.
- `farplane/manifest.json` changes project adoption.
- Markdown links and skill signatures change graph projections.
- CLI commands expose stable slices of those generated surfaces.

The maintenance OS works when each layer stays honest about its job.
