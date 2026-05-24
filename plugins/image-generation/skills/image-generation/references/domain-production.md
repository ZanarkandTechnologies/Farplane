# Image And Social Production

Shared workflow for image artifact domain skills such as product photography
and `social-content` methods.

## Load Order

1. Read the active artifact skill first.
2. Load that skill's `references/upstream*.md` files for domain structure and examples.
3. Use this shared workflow for routing, asset saving, async jobs, publishing guards, and upstream-reference safety.

## Route By Need

| Need | Route |
| --- | --- |
| Normal still image generation or editing | [imagegen](/Users/kenjipcx/.codex/skills/.system/imagegen/SKILL.md) first |
| Named inference.sh image model, CLI batch, cutout, upscale | [image-generation](../SKILL.md) |
| Product hero shot, packshot, e-commerce image, lifestyle product photo | [product-photography](../../product-photography/SKILL.md) |
| General cross-platform social campaign asset | [social-content:cross-platform](../../social-content/SKILL.md) |
| LinkedIn post, professional social writing, B2B thought leadership | [social-content:linkedin](../../social-content/SKILL.md) |
| Instagram/LinkedIn/X carousel or multi-slide post | [social-content:carousel](../../social-content/SKILL.md) |
| Twitter/X thread or post writing | [social-content:twitter-thread](../../social-content/SKILL.md) |
| Model-native video, image-to-video, avatar/lipsync, video edit | [video-generation](../../video-generation/SKILL.md) |
| Website, landing page, product page, or campaign asset set | [frontend-craft media pipelines](../../frontend-craft/references/media-pipelines.md) |

## Shared Rules

- Copied upstream references are read-only usage docs. Do not run `npx skills add ...` commands from Related Skills sections unless the user explicitly asks.
- Treat `belt app run` as external compute/spend. Confirm it is appropriate before running.
- Never publish to X, LinkedIn, TikTok, Instagram, YouTube, or other social platforms unless the user explicitly asks to publish.
- Save project assets, drafts, prompts/scripts, input JSON, result JSON, final media, and notes inside the workspace.
- For long-running or batched jobs, use [long-running-jobs.md](long-running-jobs.md): `--no-wait`, task IDs, `jobs.md`, and `belt task get <task-id>`.
- If the asset is used in a frontend, verify path loading, dimensions, alt text, responsive crop, fallback behavior, and visual quality through the frontend QA path.

## Output Bundle

Use an existing project asset directory when one is already established. Otherwise create a small bundle:

```text
output/<artifact-skill>/<slug>/
  brief-or-draft.md
  prompt.md
  input.json
  result.json
  final-media.ext
  notes.md
  jobs.md
```

Only include `jobs.md` for async or batched runs.
