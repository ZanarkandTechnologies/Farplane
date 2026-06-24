# Skill Graph

Generated visual inspection surface for Farplane skills and harness docs.

## Files

- `skill-graph.json`: generated graph data from `docs/skills/registry.jsonl`
- `skill-graph.js`: generated local-file wrapper for the same graph data
- `skill-docs.json`: generated `SKILL.md` frontmatter and body Markdown
- `skill-docs.js`: generated local-file wrapper for the same skill docs
- `harness-graph.json`: generated repo-wide local-reference graph for docs,
  skills, templates, agents, scripts, and root docs
- `harness-graph.js`: generated local-file wrapper for the same harness graph
- `farplane-lifecycle-graph.json`: generated semantic Farplane lifecycle graph
  with skill reads/writes/routes, framework files, hooks, and FSA projections
- `farplane-lifecycle-graph.js`: generated local-file wrapper for the same
  lifecycle graph
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

The graph treats `skill_links` as solid Markdown-reference edges and
`common_chains.after` as dashed chain edges. Nodes are color-coded by tier and
marked when the skill is upstream-owned external source. Clicking a node opens
the skill detail panel with parsed frontmatter, raw YAML frontmatter, rendered
`SKILL.md` Markdown, and outgoing links.

The harness graph is currently a data/report surface rather than a rendered UI
view. It detects local Markdown links and literal repo paths, resolves them to
repo files when possible, and keeps unresolved local-looking references visible
for cleanup.

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
