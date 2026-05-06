---
name: video-ad-specs
version: 1.0.0
description: Plan platform-specific video ads and paid social creative for TikTok, Instagram Reels/Stories, YouTube, Facebook, LinkedIn, Shorts, bumper ads, pre-roll, and mobile ad formats. Covers dimensions, duration, safe zones, hooks, captions, AIDA, and creative QA. Routes production through `video-generation`, stills through `imagegen` or `image-generation`, and web/campaign integration through `frontend-craft`.
allowed-tools: Read, Grep, Glob, Bash
---

# Video Ad Specs

Domain entrypoint for platform-specific video ad planning and creative production.

## Steps

1. Load the shared [domain video production workflow](../video-generation/references/domain-production.md).
2. Load the [upstream video ad guide](references/upstream.md) for platform specs, aspect ratios, safe zones, duration limits, hooks, captions, and ad frameworks.
3. Load [video ad prompting](references/prompting.md) when writing platform-specific hooks, visual scenes, UGC prompts, caption-safe shots, or CTA prompts.
4. Pick the platform and final deliverables before generating assets.

Use the shared production workflow for image/video/Remotion/frontend routing, saved artifacts, async jobs, and upstream-reference safety.
