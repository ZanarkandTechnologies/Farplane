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
- `index.html`: static graph viewer
- `docs/doc-audit/generated/doc-reference-report.md`: generated Markdown audit
  report for docs cleanup, global-docs bundling, and archive candidates

## Regenerate

```bash
python3 skills/skill-maintenance/scripts/generate_skill_graph.py
python3 skills/skill-maintenance/scripts/generate_harness_graph.py
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
