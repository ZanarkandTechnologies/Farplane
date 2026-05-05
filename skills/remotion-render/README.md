# Remotion Render

Skill for rendering React/Remotion TSX components to video through inference.sh `belt` when available.

## Purpose

Keep deterministic code-to-video rendering separate from model-native video generation.

## Entry Point

- `SKILL.md`: trigger rules, capability/spend gates, render workflow, and output contract.
- `references/remotion-render.md`: upstream inference.sh Remotion `SKILL.md` copied as reference material.

Use this when the user wants code-driven motion graphics, data-driven video, animated UI sequences, or React animation exported as MP4. Use `video-generation` for model-native text/image/reference video.

## Minimal Example

```bash
belt app get infsh/remotion-render
belt app sample infsh/remotion-render --save output/remotion-render/demo/input.json
```

Then add TSX code and render with `belt app run infsh/remotion-render --input output/remotion-render/demo/input.json --save output/remotion-render/demo/result.json` when external compute/spend is acceptable.

## How To Test

```bash
python3 skills/skill-creator/scripts/quick_validate.py skills/remotion-render
belt app get infsh/remotion-render
```
