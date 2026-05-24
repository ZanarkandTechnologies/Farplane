---
name: product-photography
version: 1.0.0
description: Plan and produce product photography, AI product photos, packshots, e-commerce images, Amazon listing images, Shopify product assets, commercial product hero shots, lifestyle product photos, detail shots, scale shots, mockups, and advertising photos. Routes normal still generation through `imagegen`, named inference.sh image models through `image-generation`, cutouts/upscales through image-generation tools, and frontend/product-page integration through `frontend-craft`.
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
