# Video Generation

Category-level skill for generating, editing, assembling, and QA-ing project-bound video assets.

## Purpose

Keep video generation as one first-load skill with the upstream umbrella model map in `SKILL.md` and provider-specific detail in references. This avoids copying inference.sh's endpoint-per-skill tree into active context.

## Entry Point

- `SKILL.md`: trigger rules, upstream umbrella model map, routing, spend gates, output contract, and frontend handoff.
- `todos.md`: ordered routing checklist for choosing the right reference.
- `references/tools/`: upstream inference.sh tool `SKILL.md` files copied as reference material.
- `references/guides/`: upstream inference.sh guide `SKILL.md` files copied as reference material.
- `references/frontend-asset-qa.md`: Codexter handoff rules for web use.

Use `SKILL.md` for routing. Use `todos.md` to select only the relevant branch:

- `references/tools/infsh-cli.md`: `belt` CLI usage.
- `references/tools/*.md`: provider/app instructions.
- `references/guides/*.md`: use-case instructions.

Remotion/code-rendered video lives in `skills/remotion-render/`.

## Minimal Example

```bash
belt app get pruna/p-video-avatar
belt app sample pruna/p-video-avatar --save output/video-generation/avatar/input.json
```

Then edit `input.json`, run with `belt app run ... --save result.json` only when external compute/spend is acceptable, and copy the final video into the project asset path.

## How To Test

```bash
python3 skills/skill-creator/scripts/quick_validate.py skills/video-generation
belt --help
belt app list --category video
```
