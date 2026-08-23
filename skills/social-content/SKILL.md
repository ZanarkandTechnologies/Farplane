---
name: social-content
version: 1.0.0
description: "Turn social campaign goals into carousels, LinkedIn posts, calendars, hooks, captions, thumbnails, or cross-platform content plans."
tier: 3
group: marketing
source: local
template_uses:
  skill-template: "0.3.6"
  skill-qa-checklist: "0.1.0"
  skill-eval-task: "0.2.0"
methods:
  - id: social-content:cross-platform
    class: artifact
    output: cross-platform-content-bundle
  - id: social-content:carousel
    class: artifact
    output: social-carousel-draft
  - id: social-content:linkedin
    class: artifact
    output: linkedin-post-draft
allowed-tools: Read, Grep, Glob, Bash
eval: evals/evals.json
qa_checklist: qa_checklist.md
---

# Social Content

## Context

Use this skill for social content planning, copy, and asset handoff across
platforms. It owns cross-platform, carousel, and LinkedIn draft decisions, not
publishing.

Route a standalone X post, thread, quote-post, or reply chain to
[x-thread](../x-thread/SKILL.md). That artifact needs a reviewable tweet
sequence rather than a generic social-content method.

## Skill Signature

```text
social_content(brief, platform_set?, artifact_format?, stage?, constraints?)
  -> content_plan | social_draft_bundle | blocked_report

state:
  reads(references/model.md, qa_checklist.md, method reference when needed,
        user swipe/reference/examples when supplied)
  writes(workspace draft artifacts when generation or external work is involved)

gates:
  artifact_matrix_bound
  method_selected
  platform_constraints_checked
  concrete_structure_before_review
  publish_boundary_explicit
  external_spend_or_posting_approved

routes:
  content-impl-plan | storyboard | asset-advisor | imagegen |
  ai-image-advisor | ai-video-advisor | remotion | impl-plan |
  research | review

fails:
  vague_premise_as_thread_plan
  local_or_private_context_missing_from_review_prompt
  publish_or_schedule_without_explicit_user_request
  external_generation_without_spend_or_upload_approval
```

## Phase Boundary

Perform planning and drafting inline. When the platform, format, hook, asset
route, CTA, or campaign direction is a real choice, compare the viable options
and recommend one. Use `research`
or current web grounding when examples, platform rules, peer patterns, or
campaign expectations materially affect the output.

<!-- BEGIN FARPLANE_IMPORTANT_CHECKLIST -->
## Todo List

- [ ] 1. Bind the artifact.
  - [ ] Read [model](./references/model.md) and build the artifact matrix:
  platform, format, message job, copy payload, asset carrier, publish boundary,
  and proof.
  - [ ] Read `qa_checklist.md` as preflight guardrails.
- [ ] 2. Select one primary method:
  `social-content:cross-platform`, `social-content:carousel`, or
  `social-content:linkedin`. Add supporting methods only when the artifact
  genuinely spans formats; route X-native copy to [x-thread](../x-thread/SKILL.md).
  - [ ] Use [method-selection-smoke](./references/method-selection-smoke.md) when
  method routing is unclear or when changing the skill.
- [ ] 3. Ground the format when needed.
  - [ ] Use current web grounding, `research:competitor`, or `research:parity`
  when examples, platform specs, peer posts, swipe patterns, or campaign
  expectations should guide scope.
  - [ ] Load upstream method references only when their platform constraints,
  examples, or format rules matter.
- [ ] 4. Draft the concrete structure.
  - [ ] Draft copy, hooks, CTAs, slide sequence, prompts, or asset plans before
  generation or rendering.
  - [ ] For quality-sensitive creative work, load
  [examples](references/examples.md) or a user-provided swipe/reference before
  finalizing the first variant.
- [ ] 5. Route production work.
  - [ ] Route idea plus Tasty Pack/reference video production planning through
  [content-impl-plan](../content-impl-plan/SKILL.md).
  - [ ] Route script, beats, and scene maps through
  [storyboard](../storyboard/SKILL.md); route asset decomposition through
  [asset-advisor](../asset-advisor/SKILL.md).
  - [ ] Route still visuals through `imagegen` or
  [ai-image-advisor](../ai-image-advisor/SKILL.md); route video through
  [ai-video-advisor](../ai-video-advisor/SKILL.md) or
  [remotion](../remotion/SKILL.md); route precise HTML assets
  or campaign pages through [impl-plan](../impl-plan/SKILL.md).
  - [ ] Save drafts, outlines, slide copy, prompts, inputs, result JSON,
  generated files, final asset paths, and notes inside the workspace when
  external generation is involved.
  - [ ] Confirm external compute, spend, uploads, or API usage is explicitly
  acceptable before running model or `belt` jobs.
- [ ] 6. Finish with proof and boundary checks.
  - [ ] Do not publish, post, reply, comment, DM, schedule, or cross-post unless
  the user explicitly asks for that action.
  - [ ] Apply `qa_checklist.md` again before claiming artifact quality or
  sending a review request.
  - [ ] Follow the native execution phase proof and writeback loop before
  claiming platform fit, campaign readiness, professional voice, slide
  hierarchy, thread quality, or final quality.
<!-- END FARPLANE_IMPORTANT_CHECKLIST -->

## Templates

Compact model:

```text
SocialContent := Brief + PlatformSet + ArtifactMatrix + MethodSet + AssetPlan + ProofPlan

Artifact := Platform + Format + Audience + MessageJob + CopyPayload + AssetCarrier + PublishBoundary + QA

MethodSelection(artifact, methods, constraints) :=
  candidates = filter(methods, artifact, constraints)
  chosen = compare_and_recommend(top3(candidates))
```

Use `references/model.md` for the artifact matrix and execution packet rules.

Use method addresses to choose the smallest relevant workflow:

- `social-content:cross-platform` for TikTok, Instagram, YouTube Shorts,
  Twitter/X, content calendars, UGC concepts, thumbnails, captions, hashtags,
  or multi-platform campaign bundles.
- `social-content:carousel` for Instagram, LinkedIn, Twitter/X, or Facebook
  carousel posts and multi-slide social assets.
- `social-content:linkedin` for LinkedIn posts, professional content,
  thought-leadership, B2B/founder content, hiring posts, comments, and
  LinkedIn carousel planning.

## Gotchas

- Do not claim a platform recommendation came from current norms unless the
  run loaded a current source, peer examples, or supplied swipe.
- Do not publish, schedule, comment, reply, DM, or cross-post without explicit
  user permission.
- Do not hide artifact context in desktop-only paths when asking for mobile or
  Telegram feedback; include the reviewable excerpt inline.

## Reference Map

- `qa_checklist.md` - read at skill start and finish for social artifact QA.
- `references/model.md` - artifact matrix, method selection, execution packet,
  and proof rules.
- `references/examples.md` - load for quality-sensitive voice, taste,
  explanation, or visual structure.
- `references/method-selection-smoke.md` - load when method routing is unclear
  or when changing the skill.
- `references/upstream-social.md` - load for multi-platform campaign,
  caption, hashtag, or calendar constraints.
- `references/upstream-carousel.md` - load for carousel format, slide count,
  visual sequence, or platform carousel constraints.
- `references/upstream-linkedin.md` - load for LinkedIn-native professional,
  founder, B2B, hiring, or thought-leadership copy.

## Output

- `content_plan`: bound artifact matrix, selected method, platform
  constraints, asset route, publish boundary, and proof plan.
- `social_draft_bundle`: copy, slide sequence, captions, prompts, or
  saved artifact paths as appropriate.
- `blocked_report`: missing context, missing approval for external side
  effects, or proof that cannot run.
