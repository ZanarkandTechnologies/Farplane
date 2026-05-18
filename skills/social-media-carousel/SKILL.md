---
name: social-media-carousel
version: 1.0.0
description: Plan and produce multi-slide carousel posts for Instagram, LinkedIn, Twitter/X, and Facebook. Covers carousel structure, hooks, slide hierarchy, platform dimensions, swipe psychology, educational carousels, and generated slide assets. Routes static slide assets through `imagegen` or `image-generation`, HTML-rendered slides through project code or inference.sh image tooling, and campaign bundles through `frontend-craft`.
tier: 3
group: content-social
source: local
allowed-tools: Read, Grep, Glob, Bash
---

# Social Media Carousel

Domain entrypoint for carousel posts and multi-slide social assets.

## Steps

1. Load the shared [image/social production workflow](../image-generation/references/domain-production.md).
2. Load the [upstream carousel guide](references/upstream.md) for platform specs, slide structure, layout rules, and examples.
3. Decide the platform, aspect ratio, slide count, and slide sequence before generating assets.
4. Route slide production through `imagegen`, `image-generation`, or code/HTML rendering based on whether the carousel needs generated imagery, precise typography, or repeatable templates.
5. Save every slide prompt/input/result and final image path; do not publish unless the user explicitly asks to publish.

Use the shared production workflow for artifact bundles, async image batches, frontend/campaign QA, and upstream-reference safety.
