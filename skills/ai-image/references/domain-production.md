# Image Production Routing

Shared routing, saving, async and publish rules for every `ai-image` mode and
for other skills that hand image work to it (social-content, landing-page,
storyboard, ads).

## Load Order

1. Read [ai-image](../SKILL.md) first; its nodes own the default path.
2. Load the mode reference only when the mode needs it:
   [product-photography](product-photography.md),
   [infographic](infographic.md), or [collage](collage.md).
3. Use this file for routing, asset saving, async jobs, publishing guards, and
   upstream-reference safety.

## Route By Need

| Need | Route |
| --- | --- |
| Editing an existing image (any change, mask, text fix, reference-guided) | [ai-image](../SKILL.md) `edit`: Ideogram 4.5 Precise Edit, quoted with `dry_run` first |
| New still image (no source image), paid model | [ai-image](../SKILL.md) `create` through `treg` (default route) |
| Quick Codex-native draft with no named model and no spend | built-in `imagegen` |
| Named inference.sh model, `belt` batch, cutout, upscale | [ai-image](../SKILL.md) `upscale` / `cutout`; `belt` details in [infsh-cli](tools/infsh-cli.md) |
| Product hero shot, packshot, e-commerce image, lifestyle product photo | [ai-image](../SKILL.md) `product` |
| Infographic, annotated dashboard, process map, data story image | [ai-image](../SKILL.md) `infographic` |
| 9:16 reel collage background from four images | [ai-image](../SKILL.md) `collage` |
| Social campaign asset, LinkedIn post, carousel, thread | [social-content](../../social-content/SKILL.md) |
| Model-native video, image-to-video, avatar/lipsync, voice, music | [ai-video](../../ai-video/SKILL.md) |
| 3D model, texture, rig | [meshy-3d-generation](../../meshy-3d-generation/SKILL.md) |
| Shot list, script, asset plan for a video | [storyboard](../../storyboard/SKILL.md) |
| Website, landing page, or product page integration | [impl-plan](../../impl-plan/SKILL.md) with QA |

## Provider Route

- `treg` is the default route for paid generation (GPT Image 2 / 2.5, Gemini
  Image, Seedream). Run `catalog_search` then `catalog_get` for the exact price
  and pick the provider; `call` only after the quote is named.
- Ideogram 4.5 Precise Edit is not on `treg` or `belt`; call its API directly
  through `farplane run --` with `IDEOGRAM_API_KEY` (Doppler
  `farplane/dev_personal`). Add `?dry_run=true` for a free exact quote.
- `belt` (inference.sh) is the route when the operator names an inference.sh
  app or a `belt`-only model (Topaz upscaler, BiRefNet cutout, FLUX LoRA).
  Check `belt app get <app>` and `belt app sample <app>` before trusting a
  schema.
- Spend stays inside the operator's weekly cap. Log every paid call in the
  operator profile's spend log with date, USD, what, and the ticket or project.

## Shared Rules

- Copied upstream references are read-only usage docs. Do not run `npx skills add ...` commands from Related Skills sections unless the user explicitly asks.
- Treat `belt app run`, `treg call` and Ideogram calls as external spend. Quote first.
- Never publish to X, LinkedIn, TikTok, Instagram, YouTube, or other social platforms unless the user explicitly asks to publish.
- Save project assets, prompts, input JSON, result JSON, final media, and notes inside the workspace.
- For long-running or batched jobs, use [long-running-jobs.md](long-running-jobs.md): `--no-wait`, task IDs, `jobs.md`, and `belt task get <task-id>`.
- If the asset is used in a frontend, verify path loading, dimensions, alt text, responsive crop, fallback behavior, and visual quality through the frontend QA path.

## Output Bundle

Use an existing project asset directory when one is already established.
Otherwise create a small bundle under `.farplane/ai-image/<date>-<slug>/`:

```text
.farplane/ai-image/<date>-<slug>/
  prompt.md
  input.json
  result.json
  source.png      (edits only)
  final.png
  notes.md        (route, provider, price, call id, inspection verdict)
  jobs.md         (async or batched runs only)
```
