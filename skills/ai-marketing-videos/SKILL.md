---
name: ai-marketing-videos
version: 1.0.0
description: Plan and produce AI marketing videos, promo clips, launch videos, product demos, brand videos, testimonials, commercial scenes, and paid ad creative. Use for marketing video, ad video, promo video, commercial, brand video, product video, product launch video, Facebook/YouTube/Instagram/TikTok ad creative, and campaign video workflows. Routes model-native generation through `video-generation`, still assets through `imagegen` or `image-generation`, and frontend integration through `frontend-craft`.
tier: 3
group: content-video
source: local
allowed-tools: Read, Grep, Glob, Bash
---

# AI Marketing Videos

Domain entrypoint for marketing and campaign video production.

## Steps

1. Load the shared [domain video production workflow](../video-generation/references/domain-production.md).
2. Load the [upstream marketing guide](references/upstream.md) for frameworks, templates, shot types, and platform patterns.
3. Load [marketing video prompting](references/prompting.md) when writing or improving prompts for launch, product, testimonial, brand, or social promo clips.
4. Load [general video prompting](../video-generation/references/prompting/video-prompting-guide.md) when shot, camera, lighting, temporal motion, or model-specific phrasing matters.
5. Decide the campaign job: launch, feature highlight, testimonial, before/after, brand story, UGC ad, or product demo.

Use the shared production workflow for image/video/Remotion/frontend routing, saved artifacts, async jobs, and upstream-reference safety.
