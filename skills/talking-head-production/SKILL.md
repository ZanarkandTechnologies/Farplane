---
name: talking-head-production
version: 1.0.0
description: Produce talking-head, avatar, lipsync, AI spokesperson, presenter, course, demo, and social video workflows. Covers portrait requirements, voiceover, scripts, avatar model selection, P-Video-Avatar, OmniHuman, Fabric, PixVerse, and lipsync production. Routes generation through `video-generation` and still portraits through `imagegen` or `image-generation`.
tier: 3
group: content-video
source: local
allowed-tools: Read, Grep, Glob, Bash
---

# Talking Head Production

Domain entrypoint for avatar, lipsync, presenter, and spokesperson videos.

## Steps

1. Load the shared [domain video production workflow](../video-generation/references/domain-production.md).
2. Load the [upstream talking-head guide](references/upstream.md) for portrait requirements, script guidance, model comparisons, and production workflows.
3. Load [talking-head prompting](references/prompting.md) when writing avatar behavior prompts, voice prompts, portrait prompts, camera/background instructions, or lipsync scripts.
4. Load [general video prompting](../video-generation/references/prompting/video-prompting-guide.md) when shot, camera, lighting, temporal motion, or model-specific phrasing matters.
5. Decide the talking-head type: avatar presenter, lipsync, AI spokesperson, course segment, product demo, or social presenter clip.

Use the shared production workflow for image/video/Remotion/frontend routing, saved artifacts, async jobs, and upstream-reference safety.
