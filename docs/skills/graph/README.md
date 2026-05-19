# Skill Graph

Generated visual inspection surface for Codexter skills.

## Files

- `skill-graph.json`: generated graph data from `docs/skills/registry.jsonl`
- `skill-graph.js`: generated local-file wrapper for the same graph data
- `index.html`: static graph viewer

## Regenerate

```bash
python3 skills/skill-maintenance/scripts/generate_skill_graph.py
```

## Open

Open `index.html` directly, or serve the repo root with a local static server
and visit `/docs/skills/graph/`.

The graph treats `skill_links` as solid Markdown-reference edges and
`common_chains.after` as dashed chain edges. Nodes are color-coded by tier and
marked when the skill is upstream-owned external source.
