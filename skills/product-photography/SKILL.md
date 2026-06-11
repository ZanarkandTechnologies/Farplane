---
name: product-photography
version: 1.0.0
description: "Turn product-image needs into packshots, lifestyle photos, detail shots, marketplace assets, cutouts, mockups, or product-page visuals."
tier: 3
group: content-image
source: local
methods:
  - product-photography:hero
  - product-photography:packshot
  - product-photography:lifestyle
  - product-photography:detail
  - product-photography:marketplace
  - product-photography:cutout-upscale
allowed-tools: Read, Grep, Glob, Bash
---

# Product Photography

<!-- BEGIN FARPLANE_IMPORTANT_CHECKLIST -->
## Todo List

# Product Photography Todos

Use this checklist whenever `product-photography` is active.

- [ ] Read [model](./references/model.md) and build the shot matrix: product
  facts, channel, shot job, aspect ratio, background, source asset,
  generation/postprocess route, output, and proof.
- [ ] Select one primary method: `product-photography:hero`,
  `product-photography:packshot`, `product-photography:lifestyle`,
  `product-photography:detail`, `product-photography:marketplace`, or
  `product-photography:cutout-upscale`. Add supporting methods only when the
  shot set genuinely spans jobs.
- [ ] Use [method-selection-smoke](./references/method-selection-smoke.md) when
  method routing is unclear or when changing the skill.
- [ ] Use [research:competitor](../research/SKILL.md#researchcompetitor) or
  [research:parity](../research/SKILL.md#researchparity) when product
  examples, marketplace specs, source assets, current model behavior, or
  commerce norms should guide the brief.
- [ ] Use the native planning phase when shot set, background/style, realism
  tradeoff, model family, output route, or marketplace scope needs a real
  decision.
- [ ] Load the shared [image/social production workflow](../image-generation/references/domain-production.md).
- [ ] Load upstream product or AI product photography references only when
  shot conventions, marketplace constraints, or model patterns matter.
- [ ] Use `imagegen` for normal Codex-native bitmap generation or editing.
- [ ] Use [image-generation](../image-generation/SKILL.md) for named
  inference.sh image models, background removal, upscaling, CLI repeatability,
  or structured result bundles.
- [ ] Route product-page or frontend integration through
  [frontend-craft](../frontend-craft/SKILL.md).
- [ ] Save source assets, prompts, inputs, result JSON, final images, and notes
  inside the workspace when external generation is involved.
- [ ] Confirm external compute, spend, uploads, or API usage is explicitly
  acceptable before running model or `belt` jobs.
- [ ] Do not publish, upload, or change store listings unless the user
  explicitly asks for that action.
- [ ] Follow the native execution phase proof and writeback loop before
  claiming commercial, marketplace, or product-clarity quality.
<!-- END FARPLANE_IMPORTANT_CHECKLIST -->

Domain entrypoint for product-photo planning and generated commercial imagery.

Compact model:

```text
ProductPhotography := ProductFacts + Channel + ShotMatrix + MethodSet + AssetRoute + ProofPlan

Shot := Job + Channel + AspectRatio + Background + SourceAsset + GenerationRoute + Output + QA

MethodSelection(shot, methods, constraints) :=
  candidates = filter(methods, shot, constraints)
  chosen = advise(top3(candidates))
```

Use `references/model.md` for the shot matrix, method selection, execution
packet, and proof rules.

## Steps

1. Load the shared [image/social production workflow](../image-generation/references/domain-production.md).
2. Load [upstream product photography](references/upstream-product-photography.md) for shot types, e-commerce requirements, angles, backgrounds, and marketplace constraints.
3. Load [upstream AI product photography](references/upstream-ai-product-photography.md) for model examples, commercial styles, and generation workflows.
4. Decide the shot set before generation: hero, packshot, lifestyle, scale, detail, in-use, variation, cutout, or upscale.
5. Use `imagegen` for normal bitmap generation/editing, or `image-generation` when the user needs inference.sh models, background removal, upscaling, CLI repeatability, or named model control.

Use the shared production workflow for prompt/input/result bundles, async batches, frontend/product-page QA, and upstream-reference safety.

## Method Notes

- `product-photography:hero` for product-page, campaign, or ad hero images.
- `product-photography:packshot` for clean catalog, SKU, white/background, or
  product-only images.
- `product-photography:lifestyle` for contextual, in-use, aspirational, or
  environment shots.
- `product-photography:detail` for close-up, feature, texture, scale, or
  comparison shots.
- `product-photography:marketplace` for Amazon, Shopify, or marketplace listing
  sets and channel-specific proof.
- `product-photography:cutout-upscale` for background removal, isolation,
  transparent cutouts, cleanup, and upscaling.

## Reference Map

- `references/model.md` - shot matrix, method selection, execution packet, and
  proof rules.
- `references/method-selection-smoke.md` - smoke cases for method routing.
