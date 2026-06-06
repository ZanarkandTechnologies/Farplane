# Skill Graph

Generated visual inspection surface for Farplane skills.

## Files

- `skill-graph.json`: generated graph data from `docs/skills/registry.jsonl`
- `skill-graph.js`: generated local-file wrapper for the same graph data
- `skill-docs.json`: generated `SKILL.md` frontmatter and body Markdown
- `skill-docs.js`: generated local-file wrapper for the same skill docs
- `index.html`: static graph viewer

## Regenerate

```bash
python3 skills/skill-maintenance/scripts/generate_skill_graph.py
```

## Open

Open `index.html` directly, or serve the repo root with a local static server
and visit `/skills/skill-maintenance/graph/`.

The graph treats `skill_links` as solid Markdown-reference edges and
`common_chains.after` as dashed chain edges. Nodes are color-coded by tier and
marked when the skill is upstream-owned external source. Clicking a node opens
the skill detail panel with parsed frontmatter, raw YAML frontmatter, rendered
`SKILL.md` Markdown, and outgoing links.
