---
name: product-photography
version: 1.0.0
description: Plan and produce product photography, AI product photos, packshots, e-commerce images, Amazon listing images, Shopify product assets, commercial product hero shots, lifestyle product photos, detail shots, scale shots, mockups, and advertising photos. Routes normal still generation through `imagegen`, named inference.sh image models through `image-generation`, cutouts/upscales through image-generation tools, and frontend/product-page integration through `frontend-craft`.
allowed-tools: Read, Grep, Glob, Bash
---

# Product Photography

Domain entrypoint for product-photo planning and generated commercial imagery.

## Steps

1. Load the shared [image/social production workflow](../image-generation/references/domain-production.md).
2. Load [upstream product photography](references/upstream-product-photography.md) for shot types, e-commerce requirements, angles, backgrounds, and marketplace constraints.
3. Load [upstream AI product photography](references/upstream-ai-product-photography.md) for model examples, commercial styles, and generation workflows.
4. Decide the shot set before generation: hero, packshot, lifestyle, scale, detail, in-use, variation, cutout, or upscale.
5. Use `imagegen` for normal bitmap generation/editing, or `image-generation` when the user needs inference.sh models, background removal, upscaling, CLI repeatability, or named model control.

Use the shared production workflow for prompt/input/result bundles, async batches, frontend/product-page QA, and upstream-reference safety.
