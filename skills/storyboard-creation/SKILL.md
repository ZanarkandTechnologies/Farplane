---
name: storyboard-creation
version: 1.0.0
description: Create film, animation, ad, product, and video storyboards with shot vocabulary, panel planning, camera angles, continuity, visual scripts, animatics, and storyboard image generation. Routes panels through `imagegen` or `image-generation`, clips through `video-generation`, and web/campaign asset planning through `frontend-craft`.
allowed-tools: Read, Grep, Glob, Bash
---

# Storyboard Creation

Domain entrypoint for storyboards, shot lists, visual scripts, and animatic planning.

## Steps

1. Load the shared [domain video production workflow](../video-generation/references/domain-production.md).
2. Load the [upstream storyboard guide](references/upstream.md) for shot types, camera angles, continuity rules, panel formats, and storyboard generation patterns.
3. Load [storyboard prompting](references/prompting.md) when writing panel prompts, shot lists, visual continuity prompts, or image-to-video motion prompts from panels.
4. Load [general video prompting](../video-generation/references/prompting/video-prompting-guide.md) when shot, camera, lighting, temporal motion, or model-specific phrasing matters.
5. Decide the board shape: shot list, visual script, panel board, animatic plan, or image-to-video motion test.

Use the shared production workflow for image/video/Remotion/frontend routing, saved artifacts, async jobs, and upstream-reference safety.
