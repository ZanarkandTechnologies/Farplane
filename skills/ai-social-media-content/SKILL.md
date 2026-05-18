---
name: ai-social-media-content
version: 1.0.0
description: Plan and produce AI-powered social media content across TikTok, Instagram, YouTube, Twitter/X, and campaign channels. Use for social media content, reels, shorts, UGC content, thumbnails, captions, hashtags, content calendars, social visuals, and multi-platform social asset workflows. Routes stills through `imagegen` or `image-generation`, video clips through `video-generation`, carousels through `social-media-carousel`, and frontend/campaign bundles through `frontend-craft`.
tier: 3
group: content-social
allowed-tools: Read, Grep, Glob, Bash
---

# AI Social Media Content

Domain entrypoint for social media content planning and asset production.

## Steps

1. Load the shared [image/social production workflow](../image-generation/references/domain-production.md).
2. Load the [upstream social content guide](references/upstream.md) for platform formats, workflows, and examples.
3. Decide the target platform and artifact: TikTok/Reels/Shorts video, feed image, carousel, thumbnail, caption set, hashtag set, UGC-style concept, or cross-platform campaign bundle.
4. Route execution through `imagegen`, `image-generation`, `video-generation`, `social-media-carousel`, or `frontend-craft` based on the artifact.
5. Draft copy and asset prompts first; do not publish to any social platform unless the user explicitly asks to publish.

Use the shared production workflow for model routing, saved artifacts, async jobs, upstream-reference safety, and frontend/campaign QA.
