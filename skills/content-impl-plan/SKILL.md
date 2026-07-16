---
name: content-impl-plan
description: "Turn a content idea, reusable style profile, and optional Inspiration Pack into a ticket-shaped production plan with advisor actions, QA, and production handoff."
tier: 3
group: content-production
source: local
template_uses:
  skill-template: "0.3.7"
  skill-qa-checklist: "0.1.1"
  skill-eval-task: "0.2.0"
  skill-surface-budget: "0.1.0"
eval: evals/evals.json
qa_checklist: qa_checklist.md
common_chains:
  after: ["video-production", "storyboard", "asset-advisor", "avatar-advisor", "audio-advisor", "audio-generation", "ai-image-advisor", "ai-video-advisor", "remotion", "review"]
allowed-tools: Read, Grep, Glob, Bash
---

# Content Impl Plan

## Context

Use this skill when an idea, proof point, offer, or Tasty Pack/reference needs
to become an executable content-production ticket. This is the content analogue
to the coding `impl-plan`: it compiles creative intent into a storyboard, asset
decomposition, advisor action list, production order, proof contract, and final
Remotion/review path.

This skill owns the parent plan and action list. For deliberate scene breaks,
the plan is not human-review-ready until child routes have materialized each
low-cost clean/annotated storyboard grid as an actual image file plus its notes
packet. Text panel descriptions are `storyboard_draft_ready` only. It
does not generate final provider clips, write Remotion code, render, publish,
or replace the advisor skills.

## Skill Signature

```text
content_impl_plan(idea, content_kind?, video_method?, style_profile?, inspiration_pack?, icp?, platform?, proof?, constraints?, artifact_owner?)
  -> content_ticket + advisor_action_list + production_program | blocked_report

state:
  reads(user brief, video-production style profile/config when selected,
        optional Inspiration Pack/Tasty Pack captures, proof/examples/swipes,
        active ticket?, qa_checklist.md)
  writes(content implementation ticket or ticket-scoped artifact when durable
        execution is requested)

gates:
  idea_bound; audience_and_promise_named; visual_direction_resolved;
  style_profile_resolved_when_supplied;
  inspiration_evidence_mapped_when_supplied; storyboard_route_selected;
  scene_grid_reviewable_when_deliberate_breaks; asset_graph_planned;
  advisor_actions_ordered; creative_lock_passed;
  remotion_terminal_path_named; review_and_qa_contract_observable

routes:
  video-production | storyboard | asset-advisor | avatar-advisor |
  audio-advisor | audio-generation | ai-image-advisor | ai-video-advisor |
  remotion | social-content | review | qa

fails:
  storyboard_as_parent_plan; format_sprawl; vibes_only_action_list;
  advisor_actions_without_owner; remotion_without_assets; qa_afterthought;
  inspiration_pack_as_moodboard; style_profile_as_creator_impersonation;
  unconditional_reference_gate; creative_lock_skipped
```

## Production Contract

After binding the brief, load
[production contract](references/production-contract.md) before compiling the
ticket. It owns visual-direction composition, Resource Bank readiness,
`creative_lock`, deliberate scene-packet approval, and the full ticket template.

## Phase Boundary

Plan inline by default. Use the child skills only when their output is needed
for the ticket to be executable. Use `review` before execution when the plan
will guide a public campaign, paid spend, high-visibility proof, or close
reference recreation. Use `qa` when a produced artifact needs formal proof.

<!-- BEGIN FARPLANE_IMPORTANT_CHECKLIST -->
## Todo List

- [ ] 1. Bind the implementation brief.
  - [ ] Resolve idea, content kind, video method, optional style profile,
    optional Inspiration Pack/Tasty Pack/reference material, ICP, viewer
    promise, proof, platform, target artifact, constraints, CTA, deadline, and
    artifact owner.
  - [ ] Read `qa_checklist.md` as preflight guardrails.
- [ ] 2. Resolve visual direction and conditional reference evidence.
  - [ ] Route video work through `video-production` and record method_default,
    profile_only, inspiration_only, composed_direction, or blocked_report.
  - [ ] When a style profile is supplied, load its profile, prompt, collocated
    example, compatibility, provenance, and QA assertions.
  - [ ] When Inspiration is supplied, identify hook stack, timeline beats,
    story pattern, pacing, format affordances, creative elements, and why the
    reference likely works; classify the reference type, reject nearby story
    engines, and separate reusable structure from rights/brand constraints.
  - [ ] Emit labeled `Reference type`, `Rejected nearby formats`, `Narrative
    spine`, and `Viewer question -> answer` fields; do not leave these implied
    inside scene prose.
  - [ ] When Inspiration is supplied, build a `reference_leverage_map` from
    `captures[].elements` to planned shots, assets, audio cues, motion cues, or narrative beats;
    map pinned elements first and explain any pinned element not reused. If
    `meta.warnings` says an operator note exists but no element was pinned from
    it, state the gap before treating the pack as production guidance.
  - [ ] If named reference elements exist but their capture payload is missing,
    map those named elements provisionally at element level and block only the
    unresolved evidence/rights fields; do not replace the map with generic
    category placeholders.
  - [ ] When Inspiration is supplied, classify `reference_readiness` as
    `media_ready`, `regen_ready`, `semantic_only`, or `blocked`; do not route to
    Remotion as production until pinned visual/audio/editing elements have
    resolved media refs or concrete regeneration packets.
- [ ] 3. Create the content ticket shape.
  - [ ] Use `Summary`, `Scope`, `Delta`, `Program`, `Map`, `Done / Proof`,
    `State`, `Links`, and `Notes`.
  - [ ] Make the before/after explicit: idea plus reference to executable
    production program.
- [ ] 4. Route child planning work.
  - [ ] Route narrative, script, beats, and scene map to `storyboard`. For
    deliberate breaks, require one clean/annotated grid packet per 4-5 second
    model-native clip and load
    `video-production/references/scene-grid-production.md`.
  - [ ] Materialize each review packet through the child image/storyboard route
    as actual clean-grid and annotated-grid image files, then verify file
    existence and dimensions. Inline panels, intended paths, or a list saying
    grids will be needed are `storyboard_draft_ready`, not human-review-ready.
  - [ ] Route asset inventory and recreation decisions to `asset-advisor`.
  - [ ] Route persistent presenter/character needs to `avatar-advisor`.
  - [ ] Route voice, music, SFX, Foley, and mix notes to `audio-advisor`.
  - [ ] Route approved provider-ready voice, music, or SFX packets to
    `audio-generation`; do not make `audio-advisor` execute providers.
  - [ ] Route still or model-native generation details to `ai-image-advisor`
    and `ai-video-advisor` only when generation inputs are needed.
- [ ] 5. Compile the advisor action list.
  - [ ] Order actions by dependency: storyboard, assets, generation/capture,
    audio, Remotion composition, render proof, review/QA.
  - [ ] For narrative video, declare generation topology before spend:
    `continuous_chain`, `deliberate_scene_breaks`, or `montage`; block isolated
    clip batches unless the chosen format is intentionally montage. For
    deliberate breaks, make the scene-grid packet the human approval surface
    before generation; approval locks unchanged assets for reuse.
  - [ ] State the unused topology obligations too: continuous chains require
    explicit start/end-frame handoffs; isolated narrative batches are blocked
    unless the selected format is montage.
  - [ ] Give every action an owner skill, input, output, acceptance check, and
    blocker condition.
- [ ] 6. End with production proof.
  - [ ] Run `creative_lock` and stop with a blocked report when narrative,
    assets, cue timing, Inspiration-use evidence when Inspiration was supplied,
    or other applicable QA gates are missing.
  - [ ] Route final stitching, captions, overlays, audio placement, and local
    render proof to `remotion` only after `creative_lock` passes.
  - [ ] Name review and QA checklist gates before claiming the plan ready.
  - [ ] Apply `qa_checklist.md` again before completion.
<!-- END FARPLANE_IMPORTANT_CHECKLIST -->

## Gotchas

- Do not make `storyboard` carry the whole implementation plan. Storyboard owns
  narrative and scene design; this skill owns the parent ticket and production
  action list.
- Do not create format-specific skills for every trend. Use Tasty Pack or
  reusable style profiles plus optional references, then route through stable
  primitives.
- Do not require an Inspiration Pack merely to use a named style profile or a
  method default. Do not treat a style profile as permission to impersonate a
  creator or copy protected examples.
- Do not let Remotion start before assets, cue timing, dimensions, and proof
  checks are named.
- Do not treat a Tasty Pack or Inspiration Pack as a vibe source. If the pack
  has no captures or no creative elements, block or request reingestion before
  production.
- Do not let a final video consume only the text of pinned elements when the
  user's expectation is Tasty Pack reuse. Resolve `assetId + anchor` into media
  refs or route regeneration first; otherwise label the output
  `semantic_storyboard_only`.

## Reference Map

- `references/production-contract.md` - load after brief binding and before
  ticket compilation for Resource Bank readiness, creative lock detail, scene
  approval, and the full ticket template.
- `qa_checklist.md` - read at start and finish for content implementation plan
  QA.
- `../storyboard/SKILL.md` - narrative, script, beat sheet, and scene map.
- `../asset-advisor/SKILL.md` - asset inventory, recreation plan, and owner
  routes.
- `../avatar-advisor/SKILL.md` - persistent avatar, presenter, or lipsync
  direction.
- `../audio-advisor/SKILL.md` - voice, music, SFX, Foley, cue sheet, and mix
  direction.
- `../audio-generation/SKILL.md` - provider-neutral generation packets for
  approved voice, music, and SFX execution.
- `../video-production/SKILL.md` - method selection, reusable style profiles,
  four-case visual-direction resolution, and style ingestion.
- `../video-production/references/scene-grid-production.md` - load for
  deliberate-scene-break model-native video; owns per-scene grids, approval,
  reuse locking, and Remotion assembly handoff.
- `../ai-image-advisor/SKILL.md` - still generation, edits, upscales, and
  cutouts.
- `../ai-video-advisor/SKILL.md` - model-native clip, avatar execution, video
  edit, or upscale provider route.
- `../remotion/SKILL.md` - React composition, stitching, captions, audio
  placement, and local render proof.

## Output

- `content_ticket`: executable content-production ticket or ticket-scoped plan
  artifact.
- `advisor_action_list`: ordered actions with owner, input, output, acceptance
  check, and blocker.
- `production_program`: resolved visual direction, conditional reference
  leverage map, reviewable scene-grid packets when required, asset, generation,
  audio, creative lock, Remotion, review, and QA route map. It labels reference
  type, rejected formats, narrative spine, viewer question/answer, selected
  topology, and continuous-chain/montage obligations even when not selected.
- `blocked_report`: missing idea, required reference evidence, proof, rights,
  production route, owner, or proof gate.
