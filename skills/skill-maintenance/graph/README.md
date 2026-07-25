# Skill Graph

Tracked static viewer for Farplane skills and harness docs. Generated data is
written under `.farplane/generated/graphs/` so routine refreshes do not create
repository diffs.

## Files

- `.farplane/generated/graphs/skill-graph.json`: generated graph data from
  `docs/skills/registry.jsonl`
- `.farplane/generated/graphs/skill-graph.js`: generated local-file wrapper
  for the same graph data
- `.farplane/generated/graphs/skill-docs.json`: generated `SKILL.md`
  frontmatter and body Markdown
- `.farplane/generated/graphs/skill-docs.js`: generated local-file wrapper for
  the same skill docs
- `.farplane/generated/graphs/harness-graph.json`: generated repo-wide
  local-reference graph for docs,
  skills, templates, agents, scripts, and root docs
- `.farplane/generated/graphs/harness-graph.js`: generated local-file wrapper
  for the same harness graph
- `.farplane/generated/graphs/farplane-framework-core-graph.json`: generated
  manifest-backed Framework Core graph for Harness OS Map
- `.farplane/generated/graphs/farplane-framework-core-graph.js`: generated
  local-file wrapper for the same Framework Core graph
- `.farplane/generated/graphs/farplane-lifecycle-graph.json`: generated
  semantic Farplane lifecycle graph with skill reads/writes/routes, framework
  files, hooks, and FSA projections
- `.farplane/generated/graphs/farplane-lifecycle-graph.js`: generated
  local-file wrapper for the same lifecycle graph
- `index.html`: static graph viewer
- `docs/doc-audit/generated/doc-reference-report.md`: generated Markdown audit
  report for docs cleanup, global-docs bundling, and archive candidates

## Projection Model

All graph generators now route through a shared GraphIR and named projection
profiles under `skills/skill-maintenance/scripts/`:

- `graph_ir.py`: shared node, edge, timestamp, JSON/JS, comparison, and
  validation helpers
- `graph_projection_config.py`: named projection profiles and output defaults
- `graph_projection.py`: generic projection filtering and check helpers
- `generate_graph_projection.py`: profile-based dispatcher

The three generated graph families are sibling projections of one normalized
model, not parent/child views. In particular, the lifecycle graph is not a
projection of the skill graph because it needs hooks, automations, reports,
ticket files, finite-state projections, and curated framework edges that the
skill registry graph does not own.

Current projection profiles:

- `skill-registry`: skill registry graph and rendered skill docs
- `harness-reference`: repo-wide local-reference graph and docs audit report
- `farplane-framework-core`: manifest-backed Framework Core graph. It reads
  `farplane/manifest.json` `farplane_graph.framework_core`, matches source
  docs with include/exclude patterns, adds a curated workflow spine, keeps
  direct framework file/spec refs, and connects ordered workflow skills.
- `farplane-lifecycle-core`: compact lifecycle graph for UI and agent context
- `farplane-lifecycle-full`: audit lifecycle graph with optional detail nodes

## Regenerate

```bash
python3 skills/skill-maintenance/scripts/generate_skill_graph.py
python3 skills/skill-maintenance/scripts/generate_harness_graph.py
python3 skills/skill-maintenance/scripts/generate_farplane_lifecycle_graph.py
```

Or use the profile dispatcher:

```bash
python3 skills/skill-maintenance/scripts/generate_graph_projection.py --list
python3 skills/skill-maintenance/scripts/generate_graph_projection.py --projection skill-registry
python3 skills/skill-maintenance/scripts/generate_graph_projection.py --projection harness-reference
python3 skills/skill-maintenance/scripts/generate_graph_projection.py --projection farplane-framework-core
python3 skills/skill-maintenance/scripts/generate_graph_projection.py --projection farplane-lifecycle-core
python3 skills/skill-maintenance/scripts/generate_graph_projection.py --projection farplane-lifecycle-full
```

Each compatibility wrapper also accepts `--projection` for its graph family.
For example:

```bash
python3 skills/skill-maintenance/scripts/generate_farplane_lifecycle_graph.py --projection farplane-lifecycle-full --out /tmp/lifecycle-full.json --js-out /tmp/lifecycle-full.js
```

## Open

Open `index.html` directly, or serve the repo root with a local static server
and visit `/skills/skill-maintenance/graph/`.

Run the generators first after a fresh clone. The tracked viewer loads its
ignored runtime data from `.farplane/generated/graphs/`.

The graph treats `skill_links` as solid Markdown-reference edges,
`todo_skill_refs` as ordered todo-chain edges, and `common_chains.after` as
dashed chain edges. Nodes are color-coded by tier, sized by observed skill heat
when telemetry exists, and marked when the skill is upstream-owned external
source. Clicking a node opens the skill detail panel with parsed frontmatter,
raw YAML frontmatter, rendered `SKILL.md` Markdown, heat counters, and outgoing
links.

Skill heat defaults are configured at generation time through environment
variables, usually from `config.toml.example`:

- `FARPLANE_SKILL_HEAT_WINDOW_DAYS`: main ranking window, default `30`.
- `FARPLANE_SKILL_HEAT_RECENT_DAYS`: secondary recent counter, default `7`.
- `FARPLANE_SKILL_HEAT_TOP_N`: default hot-skills filter, default `25`.
- `FARPLANE_SKILL_HEAT_EVENT_TYPES`: comma-separated telemetry event types to
  count as skill heat.

The harness graph is currently a data/report surface rather than a rendered UI
view. It detects local Markdown links and literal repo paths, resolves them to
repo files when possible, and keeps unresolved local-looking references visible
for cleanup.

The Framework Core graph is the Harness OS Map surface. It starts from
manifest-owned framework doc include/exclude patterns, preserves those docs as
source nodes, adds workflow nodes for the main lifecycle lanes, keeps direct
refs to framework files/specs, adds mentioned skills from the source docs, and
uses curated lifecycle workflow edges to show skill order. It intentionally
avoids repo-wide connector expansion so the UI can explain the lifecycle and
core workflows instead of rendering every reachable maintenance file.

The lifecycle graph is a semantic framework surface. It combines conservative
`SKILL.md` signature parsing, `hooks.json` commands, curated framework-critical
edges, and finite state projections described in
`docs/farplane-framework/graph-contract.md`.

The default output is the compact core graph for UI and agent context use. Run
with `--full` when reviewing parser internals such as gates, FSA state nodes,
and abstract prose-derived state.

Use `--check` on the dispatcher or lifecycle wrapper when a workflow needs a
stale-output guard. The check ignores `generated_at` but compares the rest of
the generated JSON/JS payload exactly.
