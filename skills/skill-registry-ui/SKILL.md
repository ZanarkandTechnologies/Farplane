---
name: skill-registry-ui
description: Open, refresh, and validate the Codexter skill registry graph UI, including clickable skill nodes, rendered SKILL.md Markdown, frontmatter details, tier colors, and common-chain edges.
tier: 3
group: skills
source: local
allowed-tools: Read, Bash
---

# Skill Registry UI

Use this when the operator asks to view, inspect, demo, or debug the local
Codexter skill graph UI.

## Workflow

1. Regenerate the registry and graph data:

```bash
python3 skills/skill-maintenance/scripts/check_skills.py --write
python3 skills/skill-maintenance/scripts/generate_skill_graph.py
```

2. Open the viewer:

```text
docs/skills/graph/index.html
```

The page can be opened directly through `file://` because the graph data and
skill Markdown are emitted as local JavaScript wrappers.

3. Click a node to inspect:

- registry metadata
- parsed frontmatter
- raw YAML frontmatter
- rendered `SKILL.md` body Markdown
- outgoing reference and common-chain edges

4. Use the controls to filter by tier, group, source ownership, Markdown
references, chain edges, and search text.

5. For proof, use browser inspection or screenshot capture to verify that:

- node count matches `docs/skills/registry.jsonl`
- chain edges are visible when enabled
- clicking a node renders frontmatter and Markdown
- console/page errors are absent

## Handoff

If the UI itself needs to change, route implementation through
`frontend-craft`. If the registry data or generated graph payload is stale or
wrong, route maintenance through `skill-maintenance`.
