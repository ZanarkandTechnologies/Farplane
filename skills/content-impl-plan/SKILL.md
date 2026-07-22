---
name: content-impl-plan
description: "Compose a content idea with an optional Brand Kit and Tasty Pack into a reviewable, timing-aware production plan with advisor handoffs and proof."
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
  after: ["video-production", "storyboard", "asset-advisor", "avatar-advisor", "audio-advisor", "ai-image-advisor", "ai-video-advisor", "remotion", "review"]
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
content_impl_plan(idea, brand_kit?, tasty_pack?, content_kind?, video_method?, icp?, platform?, proof?, constraints?, artifact_owner?)
  -> content_ticket + creative_hypothesis + leverage_map + low_fi_visual_storyboard + advisor_action_list + production_program | blocked_report

state:
  reads(user brief, optional approved Brand Kit snapshot, optional complete
        Tasty Pack captures, proof/examples/swipes, active ticket?,
        qa_checklist.md)
  writes(content implementation ticket or ticket-scoped artifact when durable
        execution is requested)

gates:
  idea_bound; audience_and_promise_named; creative_direction_composed;
  brand_constraints_preserved_when_supplied;
  complete_elements_mapped_when_supplied; storyboard_route_selected;
  low_fi_review_packet_observable; timing_master_selected;
  scene_grid_reviewable_when_deliberate_breaks; asset_graph_planned;
  advisor_actions_ordered; creative_lock_passed;
  remotion_terminal_path_named; review_and_qa_contract_observable

routes:
  video-production | storyboard | asset-advisor | avatar-advisor |
  audio-advisor | ai-image-advisor | ai-video-advisor |
  remotion | social-content | review | qa

fails:
  storyboard_as_parent_plan; format_sprawl; vibes_only_action_list;
  advisor_actions_without_owner; remotion_without_assets; qa_afterthought;
  tasty_pack_as_moodboard; style_profile_as_third_composition_source;
  brand_conflict_silently_blended; title_only_element_handoff;
  final_visuals_before_timing_master; creative_lock_skipped
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
  - [ ] Resolve idea, content kind, video method, optional approved Brand Kit,
    optional Tasty Pack/reference material, ICP, viewer
    promise, proof, platform, target artifact, constraints, CTA, deadline, and
    artifact owner.
  - [ ] Read `qa_checklist.md` as preflight guardrails.
- [ ] 2. Compose Brand Kit identity with optional Tasty Pack inspiration.
  - [ ] Treat the Brand Kit as approved identity/constraint truth and the
    Tasty Pack as optional ad-hoc inspiration. Brand Kit constraints win every
    conflict; explicitly choose, augment, reject, or block each conflicting
    Tasty element instead of silently blending it.
  - [ ] Do not accept or resolve `style_profile` as a third reusable creative
    source in this skill. Direct callers may still use standalone
    `video-production` profile behavior outside this composition path.
  - [ ] Route video method selection through `video-production`, passing the
    compiled creative direction rather than asking it to merge a profile.
  - [ ] When a Tasty Pack is supplied, identify hook stack, timeline beats,
    story pattern, pacing, format affordances, creative elements, and why the
    reference likely works; classify the reference type, reject nearby story
    engines, and separate reusable structure from rights/brand constraints.
  - [ ] Emit labeled `Reference type`, `Rejected nearby formats`, `Narrative
    spine`, and `Viewer question -> answer` fields; do not leave these implied
    inside scene prose.
  - [ ] Build one `element_leverage_map` from complete Brand Kit and Tasty Pack
    elements to planned beats, assets, advisor actions, audio cues, motion
    cues, copy moves, or production rules. Map pinned Tasty elements first and
    explain every selected, rejected, conflicting, or unused element. If
    `meta.warnings` says an operator note exists but no element was pinned from
    it, state the gap before treating the pack as production guidance.
  - [ ] If named reference elements exist but their capture payload is missing,
    map those named elements provisionally at element level and block only the
    unresolved evidence/rights fields; do not replace the map with generic
    category placeholders.
  - [ ] When a Tasty Pack is supplied, classify `reference_readiness` as
    `media_ready`, `regen_ready`, `semantic_only`, or `blocked`; do not route to
    Remotion as production until pinned visual/audio/editing elements have
    resolved media refs or concrete regeneration packets.
  - [ ] Emit a creative hypothesis explaining why the idea, approved Brand Kit
    identity, and selected Tasty mechanics should work together and what would
    falsify that hypothesis.
- [ ] 3. Produce the low-fidelity approval packet.
  - [ ] Before final generation, emit the creative hypothesis, conflict/reject
    decisions, exact element leverage map, low-fidelity demo, and visual
    storyboard with image paths and notes tied to element IDs.
  - [ ] Treat text-only panels and intended image paths as draft-only. Provider
    spend waits for the operator's visual-storyboard approval.
- [ ] 4. Create the content ticket shape.
  - [ ] Use `Summary`, `Scope`, `Delta`, `Program`, `Map`, `Done / Proof`,
    `State`, `Links`, and `Notes`.
  - [ ] Make the before/after explicit: idea plus reference to executable
    production program.
- [ ] 5. Route child planning work with element realization packets.
  - [ ] For every selected element routed to a child, include element ID,
    provenance, kind, `description`, `whyItWorks`, resolved
    `goldenExample { assetId, description? }`, `goldenRecipe`, planned use, and
    acceptance check. Block generation handoffs that omit the recipe or
    example; do not route title/description-only packets.
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
  - [ ] Route voice, music, SFX, Foley, SoundButtonsWorld candidate discovery,
    provider packets/execution, receipts, and mix notes to `audio-advisor`.
  - [ ] For every interesting/common SFX idea, put up to three candidate item
    links—or `searched_no_fit`—in the final plan as
    `awaiting_operator_download_and_approval`; never download them.
  - [ ] Route still or model-native generation details to `ai-image-advisor`
    and `ai-video-advisor` only when generation inputs are needed.
- [ ] 6. Compile the timing-master advisor action list.
  - [ ] Select `voiceover`, `music`, `source_video`, or `none` as timing master
    before final visual generation.
  - [ ] For voice-led explainer/avatar/lipsync work, lock script, generate and
    measure voice/timestamps, revise cue sheet/storyboard, then generate visual
    clips with safe surplus before Remotion. For music-led work, select or
    generate approved music first. For source-video-led work, inspect and
    measure source media first. Use storyboard/assets first only when timing
    master is `none` or as low-fi approval work.
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
- [ ] 7. End with production proof.
  - [ ] Run `creative_lock` and stop with a blocked report when narrative,
    assets, timing-master media/cues, element realization receipts,
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
- Do not reintroduce `style_profile` through aliases, fallback parsing, or
  `video-production` calls in this composition path. Standalone
  `video-production` remains the owner of direct profile use.
- Do not let a child consume only an element title or description. Selected
  work is conditioned on its resolved golden example and golden recipe, with a
  receipt mapping the realized output back to the element ID.

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
- `../audio-advisor/SKILL.md` - audio direction, SoundButtonsWorld candidate
  links for operator approval, provider execution, receipts, and mix.
- `../video-production/SKILL.md` - method selection and direct standalone style
  profiles; this skill passes compiled Brand Kit + Tasty Pack direction without
  adding a profile composition lane.
- `../video-production/references/scene-grid-production.md` - load for
  deliberate-scene-break model-native video; owns per-scene grids, approval,
  reuse locking, and Remotion assembly handoff.
- `../ai-image-advisor/SKILL.md` - still generation, edits, upscales, and
  cutouts.
- `../ai-video-advisor/SKILL.md` - model-native clip, avatar execution, video
  edit, or upscale provider route.
- `../remotion/SKILL.md` - React composition, stitching, captions, audio
  placement, and local render proof.
