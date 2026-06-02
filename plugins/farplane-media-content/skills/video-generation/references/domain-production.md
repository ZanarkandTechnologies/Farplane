# Domain Video Production

Shared workflow for video artifact domain skills such as marketing videos, explainers, storyboards, talking heads, and video ads.

## Load Order

1. Read the active artifact skill first.
2. Load that skill's `references/upstream.md` for domain structure and examples.
3. Load that skill's `references/prompting.md` when writing or improving prompts.
4. Load [video-prompting-guide.md](prompting/video-prompting-guide.md) when general shot, camera, lighting, temporal motion, or model-specific video prompt guidance is needed.
5. Use this shared workflow for routing, asset saving, async jobs, and upstream-reference safety.

## Route By Need

| Need | Route |
| --- | --- |
| Normal still images, posters, portraits, storyboard panels | [imagegen](/Users/kenjipcx/.codex/skills/.system/imagegen/SKILL.md) first |
| Named inference.sh image model, CLI image batch, cutout, upscale | [image-generation](../../image-generation/SKILL.md) |
| Model-native video, image-to-video, avatar/lipsync, video edit, upscale | [video-generation](../SKILL.md) |
| Remotion code authoring, overlays, captions, charts, deterministic timing | [remotion](../../remotion/SKILL.md) |
| Render Remotion TSX/code through inference.sh | [remotion-render](../../remotion-render/SKILL.md) |
| Website, landing page, or campaign asset set | [frontend-craft media pipelines](../../frontend-craft/references/media-pipelines.md) |

## Shared Rules

- Copied upstream references are read-only usage docs. Do not run `npx skills add ...` commands from Related Skills sections unless the user explicitly asks.
- For inference.sh commands, load [reference-overrides.md](reference-overrides.md) before copying upstream examples, then verify live app availability with `belt app get <app>`.
- Treat `belt app run` as external compute/spend. Confirm it is appropriate before running.
- Save project assets, prompts/scripts, input JSON, result JSON, final media, and notes inside the workspace.
- For long-running or batched jobs, use [long-running-jobs.md](long-running-jobs.md): `--no-wait`, task IDs, `jobs.md`, and `belt task get <task-id>`.
- If the asset is used in a frontend, verify loading, fallback/poster behavior, responsive crop, autoplay/loop/muted policy, reduced-motion behavior, and visual quality through the frontend QA path.

## Output Bundle

Use an existing project asset directory when one is already established. Otherwise create a small bundle:

```text
output/<artifact-skill>/<slug>/
  script-or-brief.md
  prompt.md
  input.json
  result.json
  final-media.ext
  notes.md
  jobs.md
```

Only include `jobs.md` for async or batched runs.
