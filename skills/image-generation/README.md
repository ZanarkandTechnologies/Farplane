# Image Generation

Category-level inference.sh skill for generating, editing, upscaling, and processing project-bound image assets.

## Purpose

Keep one active image-generation skill with the upstream umbrella model map in `SKILL.md` and provider-specific detail in references. Use built-in `imagegen` for normal Codex-native bitmap generation/editing.

## Entry Point

- `SKILL.md`: trigger rules, best-current defaults, model map, routing, spend gates, output contract, and frontend handoff.
- `todos.md`: ordered routing checklist for choosing the right reference.
- `references/tools/`: upstream inference.sh image tool `SKILL.md` files copied as reference material.

Use `SKILL.md` for broad model choice. Use `todos.md` to select the relevant branch:

- `references/tools/infsh-cli.md`: `belt` CLI usage.
- `references/tools/*.md`: provider/app instructions.

## Minimal Example

```bash
belt app get openai/gpt-image-2
belt app sample openai/gpt-image-2 --save output/image-generation/demo/input.json
```

Then edit `input.json`, run with `belt app run ... --save result.json` only when external compute/spend is acceptable, and copy the final image into the project asset path.

## How To Test

```bash
python3 skills/skill-creator/scripts/quick_validate.py skills/image-generation
belt --help
belt app list --category image
```
