---
name: video-production
version: 1.0.0
description: "Plan and produce video workflows through method-addressed routes: video-production:marketing, video-production:explainer, video-production:storyboard, video-production:talking-head, and video-production:ad-spec. Use for marketing videos, promo clips, launch videos, explainer videos, product demos, storyboards, shot lists, talking-head/avatar/lipsync videos, and platform-specific video ad specs. Routes model-native generation through `video-generation`, still assets through `imagegen` or `image-generation`, deterministic assembly through `remotion` or `remotion-render`, and campaign/web integration through `frontend-craft`."
tier: 3
group: content-video
source: local
common_chains:
  after: ["video-generation", "remotion"]
methods:
  - video-production:marketing
  - video-production:explainer
  - video-production:storyboard
  - video-production:talking-head
  - video-production:ad-spec
allowed-tools: Read, Grep, Glob, Bash
---

# Video Production

Domain entrypoint for video planning, scripting, prompting, storyboard, ad-spec,
and production workflows.

Use method addresses to choose the smallest relevant workflow:

- `video-production:marketing` for marketing videos, promo clips, launch
  videos, product videos, brand videos, testimonials, UGC ads, and campaign
  creative.
- `video-production:explainer` for explainer videos, how-it-works videos,
  product demos, onboarding, tutorials, walkthroughs, narration, and feature
  spotlight sequences.
- `video-production:storyboard` for storyboards, shot lists, visual scripts,
  panel boards, continuity plans, animatic plans, and image-to-video motion
  tests.
- `video-production:talking-head` for avatar presenter, lipsync, AI
  spokesperson, portrait animation, course, demo, testimonial, and social
  presenter clips.
- `video-production:ad-spec` for TikTok, Instagram, YouTube, Facebook,
  LinkedIn, Shorts, bumper, pre-roll, mobile paid social, UGC ads, safe zones,
  captions, hooks, and platform deliverables.

## Steps

1. Load the shared [domain video production workflow](../video-generation/references/domain-production.md).
2. Select exactly one primary method from the requested artifact and add
   supporting methods only when the deliverable genuinely spans formats.
3. Load the matching upstream and prompting references only when platform specs,
   production norms, examples, prompt quality, or format constraints matter:
   - [marketing upstream](references/upstream-marketing.md) and
     [marketing prompting](references/prompting-marketing.md)
   - [explainer upstream](references/upstream-explainer.md) and
     [explainer prompting](references/prompting-explainer.md)
   - [storyboard upstream](references/upstream-storyboard.md) and
     [storyboard prompting](references/prompting-storyboard.md)
   - [talking-head upstream](references/upstream-talking-head.md) and
     [talking-head prompting](references/prompting-talking-head.md)
   - [ad-spec upstream](references/upstream-ad-spec.md) and
     [ad-spec prompting](references/prompting-ad-spec.md)
4. Decide audience, channel, structure, duration, aspect ratio, CTA, asset
   needs, source-asset/likeness constraints, output format, and handoff path
   before drafting or generating.
5. Draft scripts, shot lists, storyboard panels, ad specs, prompts, or asset
   plans before final generation or rendering.
6. Route model-native clips through `video-generation`.
7. Route still assets, posters, product frames, portraits, or references
   through `imagegen` or `image-generation`.
8. Route deterministic motion graphics, captions, overlays, or code-rendered
   assembly through `remotion` and `remotion-render`.
9. Route website, landing-page, campaign-bundle, or frontend integration through
   `frontend-craft`.
10. Save drafts, scripts, ad specs, prompts, inputs, result JSON, generated
    files, source-asset notes, review notes, and final asset paths inside the
    workspace when external generation is involved.
11. Do not publish, post, upload, buy media, spend media budget, or represent
    identity/likeness assets as approved unless the user explicitly asks for
    that action.

Use the shared production workflow for image/video/Remotion/frontend routing,
saved artifacts, async jobs, upstream-reference safety, spend gates, and proof.

## Method Notes

### `video-production:marketing`

Use for launch, feature highlight, testimonial, before/after, brand story, UGC
ad, product demo, paid creative, promo, commercial, or campaign video work.

### `video-production:explainer`

Use for how-it-works, onboarding, tutorial, product demo, walkthrough, feature
spotlight, problem/solution, narration, or CTA sequences.

### `video-production:storyboard`

Use for shot lists, visual scripts, panel boards, animatic plans, ad
storyboards, product storyboards, continuity checks, and image-to-video motion
tests.

### `video-production:talking-head`

Use for avatar presenters, lipsync, AI spokespersons, course segments, product
demos, testimonials, portrait animation, or social presenter clips. Keep
consent, likeness, brand, and source-asset boundaries explicit for real people
or customer assets.

### `video-production:ad-spec`

Use for platform-specific paid social and video ads. Define placement,
dimensions, duration, safe zones, captions, hook, CTA, deliverables, and proof
before producing creative. Use `video-production:marketing` as a supporting
method only when broader campaign story and creative concepting are needed.
