---
name: ai-image
description: "Use for \"make an image\", \"edit this image\", \"product shot\" or \"make an infographic\": routed, quoted, inspected image assets; owns every image create or edit, even through imagegen or treg."
source: local
department: marketing
template_uses:
  skill-template: "0.6.5"
  skill-eval-task: "0.2.0"
allowed-tools: Read, Glob, Grep, Bash
---

# AI Image

## Context

Use this for any still image handed outside the unit: a new image, an edit of
an existing image, an upscale or cutout, a product shot, an infographic, or a
9:16 reel collage. One pass returns one finished, inspected asset (or a small
set) saved with its prompt and route receipt.

It does not make video clips, voice, music, or avatars
([ai-video](../ai-video/SKILL.md)), 3D models
([meshy-3d-generation](../meshy-3d-generation/SKILL.md)), shot lists or asset
plans ([storyboard](../storyboard/SKILL.md)), post copy
([social-content](../social-content/SKILL.md)), or ad strategy ([ads](../ads/SKILL.md)
supplies the creative brief). Nothing is published or uploaded here.

## Skill Signature

```text
ai_image(request, mode?, source_image?, references?, brief?, output_dir?)
  -> image asset + receipt { route, provider, prompt, price, call id, inspection verdict }
reads: the request, source images, rights-safe references, an upstream brief (storyboard, ads, landing-page)
does: picks the mode and route, writes the prompt, quotes spend, runs, saves, inspects
writes: the project's asset dir, else .farplane/ai-image/<date>-<slug>/ (prompt.md, input.json, result.json, final.*, notes.md)
returns: final asset path(s), the receipt, the spend line for the operator's log, and any next owner
```

## Modes

| Mode | Use for | Reference |
| --- | --- | --- |
| `create` | A new image with no source image | [providers](references/providers.md) |
| `edit` | Every change to an existing image: one change, background swap, restyle, text fix, mask, character consistency | [providers](references/providers.md) |
| `upscale` / `cutout` | Higher resolution, restoration, transparent PNG | [providers](references/providers.md) |
| `product` | Hero, packshot, lifestyle, detail, marketplace set | [product-photography](references/product-photography.md) |
| `infographic` | Visual explanation, annotated dashboard, process map, data story | [infographic](references/infographic.md) |
| `collage` | 9:16 reel background from 1-4 images | [collage](references/collage.md) |

<!-- BEGIN FARPLANE_IMPORTANT_CHECKLIST -->
## Todo List

- [ ] **N1 — Pick the mode and bind the inputs.**
  `request -> mode + source/reference paths + brief | one narrow question`

  Rule: Choose one mode from the table. Any request that changes an existing
  image is `edit`, whatever tool or model the operator names. Bind the source
  image, rights-safe references, aspect ratio, channel, and where the asset
  will be used. When a storyboard or ads brief supplies references,
  transferable traits, or must-not-copy constraints, carry them into the
  model input itself, not into generic style prose. Load the mode reference
  for `product`, `infographic`, or `collage`.

  Assert:
  - The mode is named before any prompt is written.
  - Private or NDA images are used only when the operator confirms they may be.
- [ ] **N2 — Choose the route and get a price quote.**
  `mode -> route + exact price | blocked-credential branch`

  Rule: `edit` goes through Ideogram 4.5 Precise Edit (direct API via
  `farplane run --`), even when the request arrived through `treg` or
  `imagegen`; get the free quote with `?dry_run=true` first. If the Ideogram
  key is missing, fall back to Seedream 4.5 and say plainly that it re-dresses
  the whole set and is not a precise edit. `create`, `product` and the
  generated parts of `infographic` go through `treg` (default route: GPT
  Image 2 / 2.5, Gemini Image); read `catalog_get` for the price and pick the
  provider. `upscale` / `cutout` and named inference.sh apps use `belt`.
  `collage` runs locally at no cost. Load [providers](references/providers.md)
  when the model is not obvious.

  Example: `"swap the background on hero.png to a beach" -> edit -> Ideogram
  4.5 dry_run quote $0.06 -> paid call`

  Assert:
  - No paid call runs before its price is named.
  - Spend stays inside the operator's weekly cap.
- [ ] **N3 — Write the prompt with text and framing kept out of the model.**
  `inputs + route -> prompt.md + input.json`

  Rule: Never rely on an image model to render exact UI, product, label, or
  data text. Composite the real screen, packshot, or label, or render the text
  deterministically (HTML/SVG) over a generated base. Assets meant for an
  overlay or video edit carry no baked-in text. For a keyed talking head or
  speaker layout, keep faces out of the centre frame. For edits, say in the
  prompt what must stay unchanged. Save `prompt.md` and `input.json` before
  the call.

  Example: `dashboard explainer -> generated hand-drawn texture + real labels
  rendered in SVG, not "a dashboard that says Revenue $42k"`

  Assert:
  - Exact text in the final asset comes from a real screen or a deterministic layer.
  - Edit prompts list the elements that must not change.
- [ ] **N4 — Run, save, and log the spend.**
  `prompt + route -> local file + result.json + spend line`

  Rule: Run the call, copy the output into the workspace (project asset dir,
  else `.farplane/ai-image/<date>-<slug>/`), and save `result.json` with the
  provider call or job id. For batches or slow jobs use
  [long-running-jobs](references/long-running-jobs.md). Add a spend line to
  the operator profile's spend log: date, USD, what, ticket or project.

  Assert:
  - A remote URL or provider job id alone is not a saved asset.
  - Every paid call has a matching spend-log line.
- [ ] **N5 — Inspect the saved file before calling it accepted.**
  `local file -> inspection verdict | rerun with a named fix`

  Rule: Open the saved file and check dimensions, crop, the brief, the
  unchanged regions of an edit, text against the copy inventory, faces and
  safe zones, and artifacts (hands, logos, warped edges). Accept, or rerun
  once with the named defect fixed; a second failure goes back to the
  operator with both files. Web-bound assets hand the receipt to
  [impl-plan](../impl-plan/SKILL.md) for path, alt text, and responsive-crop QA.

  Assert:
  - "Accepted" names the inspected local path, not a job id.
  - Rejected outputs stay in the bundle with the reason in `notes.md`.
<!-- END FARPLANE_IMPORTANT_CHECKLIST -->

## Gotchas

- Every edit of an existing image is Ideogram 4.5 Precise Edit, even when the
  operator asked for `treg`, `imagegen`, GPT Image, or Seedream by name; quote
  it free with `dry_run`. Seedream is a fallback that re-dresses the set, and
  the operator is told when it was used.
- Image models cannot be trusted with exact UI, product, or label text; a
  generated "screenshot" or packshot label is never shipped as real.
- No baked-in text in backgrounds, collages, or plates meant for overlay;
  captions belong in the video edit (the external `hyperframes` skill).
- No faces centre-frame where a speaker will be keyed over the middle.
- `treg` is the default paid route; Ideogram is called directly because it is
  not on `treg` or `belt` (checked 2026-10-12).
- Upstream tool references are read-only; never run their `npx skills add` lines.
- Nothing is published, uploaded to a store, or posted; posting is `zernio`'s job.

## Reference Map

- [providers](references/providers.md) - N2: route order, Ideogram edit call
  and fallback, generation defaults, `belt` model map, tool reference index.
- [domain-production](references/domain-production.md) - routing table for
  callers, provider rules, output bundle layout.
- [long-running-jobs](references/long-running-jobs.md) - N4: async runs,
  `jobs.md`, polling.
- [product-photography](references/product-photography.md) - `product` mode:
  shot matrix, shot kinds, execution packet, routing smoke cases, upstream guides.
- [infographic](references/infographic.md) - `infographic` mode: packet,
  copy inventory, layout spec, production routes;
  [handdrawn-saas-wireframe](references/handdrawn-saas-wireframe.md) and its
  [example](examples/handdrawn-saas-wireframe/example.md) for the hand-drawn style.
- [collage](references/collage.md) - `collage` mode: `scripts/make_collage.py`
  usage, layouts, fit options.

## Output

```yaml
mode: create | edit | upscale | cutout | product | infographic | collage
asset: <inspected local path(s)>
route: treg <endpoint> | ideogram precise-edit | seedream fallback | belt <app> | local script
prompt: <path to prompt.md>
price_usd: <quoted / charged>
call_id: <provider call or job id>
inspection: accepted | rejected (<defect>)
spend_log: <line added, or "none: local">
next_owner: impl-plan | social-content | storyboard | ai-video | none
```
