---
name: explainer-video-guide
version: 1.0.0
description: Plan and produce explainer videos, how-it-works videos, product demos, onboarding videos, tutorial videos, walkthroughs, scripts, scenes, narration, and multi-step video production pipelines. Routes model-native generation through `video-generation`, still assets through `imagegen` or `image-generation`, and deterministic assembly through `remotion` or `remotion-render`.
tier: 3
group: content-video
source: local
allowed-tools: Read, Grep, Glob, Bash
---

# Explainer Video Guide

Domain entrypoint for explainer, tutorial, onboarding, and product-demo videos.

## Steps

1. Load the shared [domain video production workflow](../video-generation/references/domain-production.md).
2. Load the [upstream explainer guide](references/upstream.md) for script formulas, pacing rules, scene planning, voiceover, and production sequence guidance.
3. Load [explainer video prompting](references/prompting.md) when writing or improving prompts for problem scenes, feature demos, motion graphics, UI walkthroughs, or CTA shots.
4. Load [general video prompting](../video-generation/references/prompting/video-prompting-guide.md) when shot, camera, lighting, temporal motion, or model-specific phrasing matters.
5. Decide the explainer structure: PAS, BAB, feature spotlight, onboarding, tutorial, or product demo.

Use the shared production workflow for image/video/Remotion/frontend routing, saved artifacts, async jobs, and upstream-reference safety.
