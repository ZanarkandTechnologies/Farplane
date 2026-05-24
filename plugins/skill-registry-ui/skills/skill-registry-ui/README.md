# Skill Registry UI

## Purpose

Open and validate the local Codexter skill graph viewer.

## Entrypoints

- `skills/skill-registry-ui/SKILL.md`
- `docs/skills/graph/index.html`
- `skills/skill-maintenance/scripts/generate_skill_graph.py`

## Example

```bash
python3 skills/skill-maintenance/scripts/check_skills.py --write
python3 skills/skill-maintenance/scripts/generate_skill_graph.py
open docs/skills/graph/index.html
```

## Test

Run the generator, open the viewer, click a skill node, and confirm the panel
shows frontmatter plus rendered Markdown.
