---
name: social-content
version: 1.0.0
description: "Plan and produce social media content through method-addressed workflows: social-content:cross-platform, social-content:carousel, social-content:linkedin, and social-content:twitter-thread. Use for social posts, captions, hooks, content calendars, carousel plans, LinkedIn posts, Twitter/X threads, UGC concepts, thumbnails, and cross-platform campaign bundles. Routes still visuals through `imagegen` or `image-generation`, video clips through `video-generation`, deterministic video through `remotion` or `remotion-render`, and campaign or web bundles through `frontend-craft`."
tier: 3
group: content-social
source: local
methods:
  - social-content:cross-platform
  - social-content:carousel
  - social-content:linkedin
  - social-content:twitter-thread
allowed-tools: Read, Grep, Glob, Bash
---

# Social Content

<!-- BEGIN FARPLANE_IMPORTANT_CHECKLIST -->
## Important Checklist

# Social Content Todos

Use this checklist whenever `social-content` or one of its method addresses is
active.

- [ ] Read [model](./references/model.md) and build the artifact matrix:
  platform, format, message job, copy payload, asset carrier, publish boundary,
  and proof.
- [ ] Select one primary method:
  `social-content:cross-platform`, `social-content:carousel`,
  `social-content:linkedin`, or `social-content:twitter-thread`. Add
  supporting methods only when the artifact genuinely spans formats.
- [ ] Use [method-selection-smoke](./references/method-selection-smoke.md) when
  method routing is unclear or when changing the skill.
- [ ] Use [research:competitor](../research/SKILL.md#researchcompetitor) or
  [research:parity](../research/SKILL.md#researchparity) when examples,
  platform specs, peer posts, swipe patterns, or campaign expectations should
  guide scope.
- [ ] Use [plan](../plan/SKILL.md) when platform mix, format, hook, asset
  route, CTA, or scope boundary needs a real tradeoff decision.
- [ ] Load upstream method references only when their platform constraints,
  examples, or format rules matter.
- [ ] Draft copy, hooks, CTAs, thread outline, slide sequence, prompts, or
  asset plans before generation or rendering.
- [ ] Route still visuals through `imagegen` or
  [image-generation](../image-generation/SKILL.md); route video through
  [video-generation](../video-generation/SKILL.md), [remotion](../remotion/SKILL.md),
  or [remotion-render](../remotion-render/SKILL.md); route precise HTML assets
  or campaign pages through [frontend-craft](../frontend-craft/SKILL.md).
- [ ] Save drafts, outlines, slide copy, prompts, inputs, result JSON,
  generated files, final asset paths, and notes inside the workspace when
  external generation is involved.
- [ ] Confirm external compute, spend, uploads, or API usage is explicitly
  acceptable before running model or `belt` jobs.
- [ ] Do not publish, post, reply, comment, DM, schedule, or cross-post unless
  the user explicitly asks for that action.
- [ ] Follow the [execute](../execute/SKILL.md) proof and writeback loop before
  claiming platform fit, campaign readiness, professional voice, slide
  hierarchy, thread quality, or final quality.
<!-- END FARPLANE_IMPORTANT_CHECKLIST -->

Domain entrypoint for social media content planning and asset production.

Compact model:

```text
SocialContent := Brief + PlatformSet + ArtifactMatrix + MethodSet + AssetPlan + ProofPlan

Artifact := Platform + Format + Audience + MessageJob + CopyPayload + AssetCarrier + PublishBoundary + QA

MethodSelection(artifact, methods, constraints) :=
  candidates = filter(methods, artifact, constraints)
  chosen = advise(top3(candidates))
```

Use `references/model.md` for the artifact matrix and execution packet rules.
Keep the `SKILL.md` Important Checklist short; upstream references stay method-specific detail.

Use method addresses to choose the smallest relevant workflow:

- `social-content:cross-platform` for TikTok, Instagram, YouTube Shorts,
  Twitter/X, content calendars, UGC concepts, thumbnails, captions, hashtags,
  or multi-platform campaign bundles.
- `social-content:carousel` for Instagram, LinkedIn, Twitter/X, or Facebook
  carousel posts and multi-slide social assets.
- `social-content:linkedin` for LinkedIn posts, professional content,
  thought-leadership, B2B/founder content, hiring posts, comments, and
  LinkedIn carousel planning.
- `social-content:twitter-thread` for Twitter/X posts, threads, quote-post
  drafts, reply chains, hook tweets, and media-supported threads.

## Steps

1. Load the shared [image/social production workflow](../image-generation/references/domain-production.md).
2. Select exactly one primary method from the requested artifact and add
   supporting methods only when the artifact truly spans formats.
3. Load the matching upstream reference only when platform specs, content
   structure, examples, or format constraints matter:
   - [cross-platform social guide](references/upstream-social.md)
   - [carousel guide](references/upstream-carousel.md)
   - [LinkedIn guide](references/upstream-linkedin.md)
   - [Twitter/X guide](references/upstream-twitter.md)
4. Decide the platform, audience, artifact, format, output count, tone, asset
   route, and handoff path before drafting or generating.
5. Draft copy, slide sequence, prompts, or asset plans before final generation
   or rendering.
6. Route execution through `imagegen`, `image-generation`, `video-generation`,
   `remotion`, `remotion-render`, or `frontend-craft` based on the artifact.
7. Save drafts, prompts, inputs, result JSON, generated files, and notes inside
   the workspace when external generation is involved.
8. Do not publish, post, schedule, comment, DM, or cross-post unless the user
   explicitly asks for that action.

Use the shared production workflow for model routing, saved artifacts, async
jobs, upstream-reference safety, frontend/campaign QA, and publish boundaries.

## Method Notes

### `social-content:cross-platform`

Use for general social media content, multi-platform planning, captions,
hashtags, thumbnails, UGC concepts, content calendars, reels/shorts briefs, and
campaign bundles.

### `social-content:carousel`

Use for educational, product, announcement, thought-leadership, case-study,
infographic, campaign, or recap carousels. Decide the platform, aspect ratio,
slide count, hook, CTA, and slide sequence before producing final slides.

### `social-content:linkedin`

Use for professional voice, founder/B2B thought leadership, hiring posts,
comments, announcements, and LinkedIn-native carousel outlines. Preserve the
professional context, audience, point of view, and CTA before drafting.

### `social-content:twitter-thread`

Use for X/Twitter-native hook tweets, single posts, threads, quote-post drafts,
reply chains, and media-supported threads. Preserve standalone tweet logic,
thread progression, character limits, and CTA before drafting.

## Reference Map

- `references/model.md` - artifact matrix, method selection, execution packet,
  and proof rules.
- `references/method-selection-smoke.md` - smoke cases for method routing.
