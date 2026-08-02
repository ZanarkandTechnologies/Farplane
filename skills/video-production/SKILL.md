---
name: video-production
version: 1.0.0
description: "Turn video deliverable goals into marketing clips, explainers, storyboards, talking-head pieces, demos, or platform ad specs."
tier: 3
group: content-video
source: local
common_chains:
  after: ["ai-video-advisor", "remotion"]
template_uses:
  skill-method-reference: "0.1.0"
eval: evals/evals.json
qa_checklist: qa_checklist.md
methods:
  - video-production:marketing
  - video-production:explainer
  - video-production:storyboard
  - video-production:talking-head
  - video-production:ad-spec
  - video-production:ingest-style
allowed-tools: Read, Grep, Glob, Bash
---

# Video Production

<!-- BEGIN FARPLANE_IMPORTANT_CHECKLIST -->
## Todo List

# Video Production Todos

Use this checklist whenever `video-production` or one of its method addresses
is active.

- [ ] Bind invocation inputs before selecting a method, named style, or
  fallback. Invocation constraints override the explicit defaults in this
  skill.
- [ ] Read [model](./references/model.md) and build the scene/deliverable
  matrix: job, channel, duration, format, source assets, method, asset route,
  delivery specs, and proof.
- [ ] Select one primary method:
  `video-production:marketing`, `video-production:explainer`,
  `video-production:storyboard`, `video-production:talking-head`, or
  `video-production:ad-spec`. Add supporting methods only when the deliverable
  genuinely spans formats.
- [ ] Resolve visual direction with `resolve_visual_direction`: method default,
  named style profile, task-specific Inspiration Pack, or their explicit
  composition. Load a profile's `profile.md`, `prompts.md`, and collocated
  `example.md` together; do not claim a named profile when only method defaults
  were used.
- [ ] When called by `content-impl-plan`, consume its compiled Brand Kit +
  optional Tasty Pack creative direction and element realization packets. Do
  not add a style profile as a third composition source, and do not reinterpret
  selected elements from title/description alone; retain direct standalone
  profile ingestion and `resolve_visual_direction` behavior for other callers.
- [ ] For multi-scene model-native video using `deliberate_scene_breaks`, load
  [scene-grid production](./references/scene-grid-production.md). Make one
  normally 4-5 second clean/annotated grid packet map to one provider clip;
  require in-frame IDs on each moving subject and fixed landmark, motion arrows
  attached to the actual moving parts, mandatory endpoints, and provider-prompt
  clauses keyed to those IDs. Generic panel-to-panel arrows do not count;
  obtain storyboard, recurring-character card, and notes approval and lock
  unchanged assets before spend. Any provider fallback that changes a visible
  character or reference invalidates that approval and returns the changed
  character card plus affected clean/annotated grids to human review before
  another production call. Preserve the canonical character unchanged, create
  a versioned provider-safe sibling, and keep every unaffected approved scene
  locked. Bind `canonical_character_path`/`canonical_character_sha256` and the
  approved effective variant through the local generation-envelope preflight;
  the effective character must appear in the exact provider `reference_images`.
- [ ] For `video-production:ingest-style`, load
  [ingest-style](./references/ingest-style.md) and consume a saved
  `ingest-content` capture rather than duplicating source reading or storage.
- [ ] Use [method-selection-smoke](./references/method-selection-smoke.md) when
  method routing is unclear or when changing the skill.
- [ ] Use [research:competitor](../research/SKILL.md#researchcompetitor) or
  [research:parity](../research/SKILL.md#researchparity) when examples,
  platform specs, source assets, current model behavior, peer videos, or
  production standards should guide scope.
- [ ] Use the native planning phase when campaign angle, structure, visual
  carrier, model family, platform cut, production route, or scope boundary
  needs a real tradeoff decision.
- [ ] Load the shared [domain video production workflow](../ai-video-advisor/references/domain-production.md).
- [ ] Load upstream or prompting references only when their platform specs,
  production norms, examples, or prompt patterns matter.
- [ ] Draft scripts, shot lists, panel sequences, ad specs, caption/safe-zone
  notes, prompt sets, asset lists, and proof plans before generation or
  rendering.
- [ ] Route model-native clips through [ai-video-advisor](../ai-video-advisor/SKILL.md).
- [ ] Route still assets through `imagegen` or
  [ai-image-advisor](../ai-image-advisor/SKILL.md); route deterministic motion
  graphics or assembly through [remotion](../remotion/SKILL.md) and
  [remotion-render](../remotion-render/SKILL.md); route campaign/web
  integration through [frontend-craft](../frontend-craft/SKILL.md).
- [ ] Save briefs, scripts, storyboards, ad specs, prompts, inputs, result
  JSON, generated files, source-asset notes, and review notes inside the
  workspace when external generation is involved.
- [ ] Confirm external compute, spend, uploads, or API usage is explicitly
  acceptable before running model or `belt` jobs.
- [ ] Do not publish, post, upload, buy media, spend media budget, or represent
  generated identity assets as approved unless the user explicitly authorizes
  that use.
- [ ] Follow the native execution phase proof and writeback loop before
  claiming narrative quality, continuity, platform fit, likeness/voice quality,
  creative quality, render quality, or final production quality.
<!-- END FARPLANE_IMPORTANT_CHECKLIST -->

Domain entrypoint for video planning, scripting, prompting, storyboard, ad-spec,
and production workflows.

Compact model:

```text
VideoProduction := Brief + Audience + ChannelPlan + SceneMatrix + MethodSet + AssetPlan + DeliveryPlan + ProofPlan

Deliverable := Job + Channel + Duration + Format + SourceAssets + ScriptOrPanel + AssetRoutes + DeliverySpecs + QA

MethodSelection(deliverable, methods, constraints) :=
  candidates = filter(methods, deliverable, constraints)
  chosen = advise(top3(candidates))

resolve_visual_direction(method, style_profile?, inspiration_pack?) :=
  neither          -> method_default
  profile_only     -> profile_only
  inspiration_only -> inspiration_only (over method defaults)
  both             -> composed_direction
```

Invocation constraints always win. In a composed direction, the named profile
owns reusable aesthetic and motion grammar; the Inspiration Pack owns task
facts, approved source assets, and task-specific motifs. Return a
`blocked_report` when hard constraints conflict, the profile does not support
the selected method, or either source lacks enough evidence for its claimed
role. Do not silently blend incompatible directions.

Use `references/model.md` for scene/deliverable matrix, method selection, and
execution packet rules. Keep the `SKILL.md` Todo List short; upstream references stay
method-specific detail.

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
- `video-production:ingest-style` for compiling a reviewed, creator-neutral
  style profile from an existing `ingest-content` saved capture.

## Steps

1. Bind invocation overrides; otherwise default to `explainer`, method-default
   visual direction, and `16:9` delivery.
2. Load the shared [domain video production workflow](../ai-video-advisor/references/domain-production.md).
3. Select exactly one primary method from the requested artifact and add
   supporting methods only when the deliverable genuinely spans formats.
4. Resolve a named style through
   [explainer style index](references/explainer-styles/index.md) when supplied,
   then apply the four-case visual-direction table. For `ingest-style`, use its
   method reference and skip ordinary deliverable production.
5. Load the matching upstream and prompting references only when platform specs,
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
6. Decide audience, channel, structure, duration, aspect ratio, CTA, asset
   needs, source-asset/likeness constraints, output format, and handoff path
   before drafting or generating.
7. Draft scripts, shot lists, storyboard panels, ad specs, prompts, or asset
   plans before final generation or rendering. For deliberate model-native
   scene breaks, expose the actual scene grids and keyed notes for approval.
8. Route model-native clips through `ai-video-advisor`.
9. Route still assets, posters, product frames, portraits, or references
   through `imagegen` or `ai-image-advisor`.
10. Route deterministic motion graphics, captions, overlays, or code-rendered
   assembly through `remotion` and `remotion-render`.
11. Route website, landing-page, campaign-bundle, or frontend integration through
   `frontend-craft`.
12. Save drafts, scripts, ad specs, prompts, inputs, result JSON, generated
    files, source-asset notes, review notes, and final asset paths inside the
    workspace when external generation is involved.
13. Do not publish, post, upload, buy media, spend media budget, or represent
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

### `video-production:ingest-style`

Use when the operator wants a saved `ingest-content` capture promoted into a
reusable visual system. Compile a new directory under
`references/explainer-styles/<profile-id>/` containing `profile.md`,
`prompts.md`, and `example.md`. Preserve provenance and observed-versus-inferred
distinctions. Reject an existing profile ID unless explicit replace authority
is present. Copy only small, rights-safe text/example assets; otherwise retain
a source reference instead of copying media. Creator names may appear in
provenance, but the reusable style name and generation instructions must remain
creator-neutral and must not request impersonation.

## Reference Map

- `references/model.md` - scene/deliverable matrix, method selection,
  execution packet, and proof rules.
- `references/method-selection-smoke.md` - smoke cases for method routing.
- `references/explainer-styles/index.md` - available creator-neutral profiles,
  supported methods, and package contract.
- `references/ingest-style.md` - saved-capture-to-profile compilation method,
  collision, provenance, rights, and completeness gates.
- `references/scene-grid-production.md` - one-scene-grid-to-one-provider-clip
  contract, approval packet, locked asset reuse, character package placement,
  and Remotion assembly ownership.
