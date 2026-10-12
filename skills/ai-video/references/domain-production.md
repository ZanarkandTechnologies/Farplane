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
| Still images, posters, portraits, storyboard panels, cutouts, image upscale | [ai-image](../../ai-image/SKILL.md) |
| Model-native video, image-to-video, avatar/lipsync, video edit, upscale, voice, music, SFX | [ai-video](../SKILL.md) |
| Composition, overlays, captions, charts, deterministic timing, final render | HyperFrames (`/hyperframes`) |
| Script, scenes, shot list, asset inventory | [storyboard](../../storyboard/SKILL.md) |
| Website, landing page, or campaign asset set | [web-surface integration](web-surface-integration.md) |

## Shared Rules

- Copied upstream references are read-only usage docs. Do not run `npx skills add ...` commands from Related Skills sections unless the user explicitly asks.
- Paid model calls go through treg by default ([providers](providers.md)): `catalog_search`, then `catalog_get` for parameters and price, then `call`. Quote the price first and stay inside the operator's weekly cap.
- For the inference.sh fallback, load [reference-overrides.md](reference-overrides.md) before copying upstream examples, then verify live app availability with `belt app get <app>`. Treat `belt app run` as external compute/spend.
- Save project assets, prompts/scripts, input JSON, result JSON, final media, and notes inside the workspace.
- For long-running or batched jobs, use [long-running-jobs.md](long-running-jobs.md): job IDs, `jobs.md`, and adaptive polling.
- If the asset is used in a frontend, verify loading, fallback/poster behavior, responsive crop, autoplay/loop/muted policy, reduced-motion behavior, and visual quality through the frontend QA path.

## Output Bundle

Use an existing project asset directory when one is already established. Otherwise create a small bundle:

```text
.farplane/ai-video/<date>-<slug>/
  script-or-brief.md
  prompt.md
  input.json
  result.json
  final-media.ext
  notes.md
  jobs.md
```

Only include `jobs.md` for async or batched runs.
