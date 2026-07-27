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
content_impl_plan(idea, brand_kit?, tasty_pack?, content_kind?, video_method?, icp?, platform?, proof?, production_policy?, artifact_owner?)
  -> content_ticket + creative_hypothesis + leverage_map
   + low_fi_visual_storyboard + scene_asset_manifest
   + advisor_action_list + production_program | blocked_report

state:
  reads(user brief, optional approved Brand Kit snapshot, optional complete
        Tasty Pack captures, proof/examples/swipes, active ticket?,
        qa_checklist.md)
  writes(content implementation ticket or ticket-scoped artifact when durable
        execution is requested)

gates:
  idea_bound; icp_contract_resolved; audience_and_promise_named;
  causal_story_and_viewer_turns_named; asset_evidence_decisions_complete;
  asset_discovery_receipts_complete; no_custom_svg_animation_assets;
  scene_asset_bundles_complete; genuine_asset_files_accepted;
  persona_review_passed; creative_direction_composed;
  brand_policy_preserved_when_supplied;
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
  final_visuals_before_timing_master; creative_lock_skipped;
  generic_icp; wallpaper_assets; metaphor_as_proof; persona_self_approval;
  missing_scene_asset_triad; renamed_box_as_asset;
  chart_as_complete_scene; creative_lock_from_planned_paths;
  remotion_before_asset_discovery; custom_svg_animation_asset;
  jsx_or_programmatic_drawing_as_asset_substitute
```

## Production Contract

After binding the brief, load
[production contract](references/production-contract.md) before compiling the
ticket. It owns visual-direction composition, Resource Bank readiness,
`creative_lock`, deliberate scene-packet approval, and the full ticket template.
For narrative, persuasive, editorial, documentary, explainer, or launch work,
also load [storytelling, asset evidence, and persona review](references/storytelling-asset-persona.md).
It owns the resolved ICP, causal/viewer-state beat contract, evidence-ranked
asset decisions, thumbnail/animatic passes, and blocking persona-review receipt.
For every visual production scene, also load
[scene asset bundles](references/scene-asset-bundles.md). It owns the mandatory
background/main-topic/foreground manifest, genuine-asset rule, readiness
states, and representative layered-frame gate.

## Phase Boundary

Plan inline by default. Use the child skills only when their output is needed
for the ticket to be executable. Use `review` before execution when the plan
will guide a public campaign, paid spend, high-visibility proof, or close
reference recreation. Use `qa` when a produced artifact needs formal proof.

## Repair and fast-track responses

Do not answer a repair or “go straight to Remotion” request with policy prose or
a schema alone.

- When a selected child handoff omitted its golden example or golden recipe,
  reopen the authoritative Brand Kit/Tasty element record and emit a visibly
  repopulated `ElementRealizationPacket` containing actual provenance,
  description, `whyItWorks`, resolved `goldenExample`, resolved `goldenRecipe`,
  planned use, and acceptance check. If the authoritative record truly lacks a
  value, show the populated fields that are available, mark the exact missing
  field `blocked_unresolved`, and stop before the child route.
- When one chart/image/PNG plus narration is supplied, classify the supplied
  file as `main_topic_asset`, then emit concrete `shared_background_packet` and
  `foreground_packet` objects with exact owner, source query or generation
  prompt, rights note, output path, and acceptance check. A complete trio of
  packets is `asset_packet_ready`; it is not `creative_lock_passed` until the
  outputs and assembled frame are accepted.

## Mandatory production-plan emissions

Do not leave these as future instructions. Emit the applicable records in the
plan itself, even when values remain honestly blocked:

```text
SceneDirection {
  causal_beats[]                 # measured clause, one state change, handoff
  scene_concepts[beat_id][3]     # literal, causal physical, context/scale
  concept_selection[]            # specificity, clarity, neighbor novelty, feasibility
  timed_animatic_receipt
  scene_asset_manifest[]         # background + topic + foreground
  asset_family_ledger[]          # identity, denominator, similarity calibration
  foreground_geometry_receipts[]
  newsprint_treatment_receipts[]
  persona_content_review
  independent_story_review
}
```

- `causal_beats`: derive ranges from measured narration. Target 4-5 seconds,
  document 3.5-6 second exceptions, name 2-3 meaningful reveals and the causal
  handoff to the next beat, and route failed timing or silent comprehension to
  storyboard/timing-master revision before asset lock.
- `scene_concepts`: emit three records per beat before search. Mechanically
  validate count/type in the plan verifier; route material distinctness and
  selection quality to storyboard or independent review.
- `concept_selection`: cite narration specificity, causal clarity,
  neighboring-scene novelty, and production feasibility. Only after selection
  emit main-topic, foreground, composition, reveal, and search/generation
  packets tied to that concept.
- `asset_family_ledger`: define production-scene denominator excluding
  title-only holds; treat derivatives as one family; require zero adjacent main
  and foreground overlap; report >=80% main and >=85% foreground uniqueness;
  calibrate perceptual similarity with one known-reuse pair and one
  known-distinct pair.
- `intentional_motif`: when used, name causal function, appearances, state and
  role transformation, plus two other varying dimensions per appearance.
  Shared background is excluded; brand consistency cannot excuse unrelated
  repeated topics or foregrounds.
- `foreground_geometry_receipts`: deterministic validation records rendered
  nontransparent pixels, visible bbox, edge contact, occlusion, tight alpha,
  and the calibrated lower 20-45% or equivalent edge-spanning mass. Independent
  frame review judges narration-specific semantic relevance. Tiny visible
  objects, mostly empty PNGs, and one-pixel borders fail.
- `newsprint_treatment_receipts`: asset/image ownership records prepared
  grayscale/contrast, subject-mask halftone scale, alpha, and accent.
  Remotion ownership records deterministic final compositing. Independent style
  review inspects final-resolution subject and background crops. Creative lock
  remains blocked until all three receipts pass.
- `independent_story_review`: compare viable boards pairwise; cite every scene
  on specificity, causal clarity, hierarchy/depth, neighbor novelty, silent
  comprehension, and evidence integrity; provisionally select the strongest
  board and repair its weak scenes. The plan author cannot self-approve, and
  hard blockers never average away.

<!-- BEGIN FARPLANE_IMPORTANT_CHECKLIST -->
## Todo List

- [ ] 1. Bind the implementation brief.
  - [ ] Resolve idea, content kind, video method, optional approved Brand Kit,
    optional Tasty Pack/reference material, ICP, viewer
    promise, proof, platform, target artifact, production policy, CTA, deadline, and
    artifact owner.
  - [ ] Read `qa_checklist.md` as preflight guardrails.
  - [ ] Resolve the ICP into role/job, context, starting belief, friction,
    knowledge, emotional stake, objection, must-believe-after, and desired
    action. Mark only low-risk inferences as assumptions; do not invent
    demographic personas.
- [ ] 2. Compile the story, asset evidence, and audience gate.
  - [ ] For narrative or persuasive work, load
    `references/storytelling-asset-persona.md`.
  - [ ] For a voice-led documentary or editorial reel built from layered
    stills and overlays, load
    `../remotion/references/documentary-reel.md` and bind its measured-voice,
    scene-layer, frame-event, prepared-overlay, audio-spine, deterministic
    treatment, and proof obligations into the owner action list.
  - [ ] Write one point of view plus stakes, select an honest causal backbone,
    and give every beat a viewer question, state before/after, causal link,
    evidence/explanation/soul function, narration, and visual direction.
  - [ ] Before asset search, create three materially different
    `SceneConcept` records per beat: literal evidence, causal physical
    mechanism, and context/scale. Concepts must differ in the relationship
    represented, not only crop, color, style, or query. Select one with a
    concise reason and record why the other two lost.
  - [ ] Measure the narration and target one causal state change per 4-5 second
    scene; 3.5-6 seconds is the calibrated exception band. Name two or three
    meaningful reveals that introduce, transform, connect, remove, or
    recontextualize a story-bearing element. A transition, text flicker, or
    arbitrary timestamp split is not a reveal.
  - [ ] Give every selected asset one job, evidence level, material identity,
    motion purpose, provenance, rights status, and acceptance check. Reject or
    quarantine wallpaper; metaphor and decoration cannot prove facts.
  - [ ] Load `references/scene-asset-bundles.md` and emit one manifest row per
    production scene. Every row must resolve a reused or justified shared
    background, a dominant main-topic asset, and a separate foreground
    depth/attention asset, each with a source or generation packet, owner,
    rights note, expected output, accepted-file field, and acceptance check.
  - [ ] Assign `asset_family_id` to every main-topic and foreground asset.
    Renames, recolors, flips, crops, and small rotations remain one family.
    Excluding the shared background and a declared transformed story motif,
    adjacent main-topic and foreground family overlap must be zero. Use
    provisional production-wide bands of >=80% unique main families and >=85%
    unique foreground families.
  - [ ] Apply the genuine-asset rule. CSS rectangles, cards, panels, labels,
    chart containers, generic document mocks, generic silhouettes, and
    unmaterialized filenames do not count as gathered layers. A chart is a
    main-topic asset and still needs background and foreground assets.
  - [ ] Enforce discovery before generation. Route every missing visual layer
    through `asset-advisor` for a visible candidate-search receipt covering
    local/source media, Resource Bank or supplied references, and suitable
    web/stock/library sources. The receipt must preserve queries, candidate
    links or asset IDs, rights/licensing notes, fit decisions, and the selected
    file or `searched_no_fit`. Do not route generation merely because drawing a
    substitute would be faster.
  - [ ] Distinguish planning from approved execution. A planning artifact may
    carry unresolved discovery rows and remain below `creative_lock`; once the
    operator approves execution, activate `asset-advisor` in the same work loop
    and require actual searched candidates before visual production. A future
    “search later” action is not an executed Asset Advisor handoff.
  - [ ] Ban custom-created SVG animation assets throughout this production
    path. Do not author new scene illustrations, characters, props,
    backgrounds, textures, diagrams, or asset stand-ins as SVG, JSX drawing
    primitives, or programmatic vector art. Existing user-supplied,
    brand-owned, licensed, or discovered SVG files may be accepted as static
    source media and transformed in Remotion. After a documented
    `searched_no_fit`, route new still or moving imagery to the appropriate
    image/video owner as raster or video media, not a custom SVG animation.
  - [ ] Record every row as exactly `storyboard_draft_ready`,
    `asset_packet_ready`, or `creative_lock_passed`. Use the lowest row state as
    production state. Do not route Remotion until accepted files exist for all
    three layers and an assembled representative frame passes the no-card-grid
    check.
  - [ ] Before `creative_lock`, require final-resolution receipts for foreground
    visible-pixel geometry and newsprint treatment. Geometry uses rendered
    nontransparent pixels, tight alpha bounds, edge contact, and occlusion—not
    transparent canvas dimensions. The clean editorial treatment uses a quiet
    background crop plus subject-mask crop proving controlled halftone,
    grayscale/contrast, crisp alpha, and restrained registration; global grime
    never substitutes for subject treatment.
  - [ ] Create three cheap thumbnail alternatives for the opening, main
    mechanism, and payoff; select timing master, run a timed animatic, and
    record silent/mute tests before style/asset lock.
  - [ ] Derive two to four decision-relevant persona lenses from the ICP and
    require an independent `PersonaContentReview` before creative lock:
    primary lens >=4/5 in comprehension, relevance, trust, and action clarity;
    required secondary lenses >=3/5; no evidence blocker may be averaged away.
    Pair the persona result with scene-cited judgments for specificity, causal
    clarity, hierarchy/depth, neighbor novelty, silent comprehension, and
    evidence integrity. Deterministic timing, reveal, family, and geometry
    receipts cannot self-certify story quality; compare viable boards
    pairwise, and keep blockers unaverageable.
  - [ ] Compile useful provisional plan sections before blocking on genuinely
    missing production evidence. Do not replace a possible leverage map,
    realization packet, or storyboard draft with a generic request for context.
- [ ] 3. Compose Brand Kit identity with optional Tasty Pack inspiration.
  - [ ] Treat the Brand Kit as approved identity and policy/prompt truth and
    the Tasty Pack as optional ad-hoc inspiration. Brand Kit policy wins every
    conflict; explicitly choose, augment, reject, or block each conflicting
    Tasty element instead of silently blending it.
  - [ ] Do not accept or resolve `style_profile` as a third reusable creative
    source in this skill. Direct callers may still use standalone
    `video-production` profile behavior outside this composition path.
  - [ ] Route video method selection through `video-production`, passing the
    compiled creative direction rather than asking it to merge a profile.
  - [ ] When a Tasty Pack is supplied, identify the storyboard opening beat,
    timeline beats, story pattern, editing rhythm, format affordances, creative
    elements, and why the reference likely works; classify the reference type,
    reject nearby story engines, and separate reusable structure from rights or
    brand policy.
  - [ ] Emit labeled `Reference type`, `Rejected nearby formats`, `Narrative
    spine`, and `Viewer question -> answer` fields; do not leave these implied
    inside scene prose.
  - [ ] Build one `element_leverage_map` from complete Brand Kit and Tasty Pack
    elements to planned beats, assets, advisor actions, audio cues, motion
    cues, storyboard copy moves, editing/subtitle moves, or production rules.
    Map pinned Tasty elements first and
    explain every selected, rejected, conflicting, or unused element. If
    `meta.warnings` says an operator note exists but no element was pinned from
    it, state the gap before treating the pack as production guidance.
  - [ ] When a Tasty Pack is supplied, emit a visible pinned-first decision
    table with one row for every capture element and columns for `pinned`,
    `chosen | augmented | rejected | conflicting | unused`, rationale, planned
    use or nonuse reason, owner/output, and acceptance. A general statement
    that pinned items were considered does not satisfy the map.
  - [ ] Enforce `is_element(value) = independently selectable &&
    independently conditionable from an example && owned by a recognizable
    production step`; accept only `format`, `storyboard`, `visual`,
    `character`, `audio`, and `editing` as CreativeElement kinds. Fold hook
    into storyboard opening beat, semantic copy into storyboard, subtitle
    rendering/timing into editing, and constraints into production policy or
    Brand Kit prompt text.
  - [ ] If named reference elements exist but their capture payload is missing,
    map those named elements provisionally at element level and block only the
    unresolved evidence/rights fields; do not replace the map with generic
    category placeholders.
  - [ ] When a Tasty Pack is supplied, classify `reference_readiness` as
    `media_ready`, `regen_ready`, `semantic_only`, or `blocked`; do not route to
    Remotion as production until pinned visual/audio/editing elements have
    accepted media files. For visual scene assets, `regen_ready` follows
    `references/production-contract.md`: it requires Asset Advisor discovery
    evidence and permits only the named raster/video generation owner; a
    regeneration packet never unlocks Remotion by itself.
  - [ ] Emit a creative hypothesis explaining why the idea, approved Brand Kit
    identity, and selected Tasty mechanics should work together and what would
    falsify that hypothesis.
- [ ] 4. Produce the low-fidelity approval packet.
  - [ ] Before final generation, emit the creative hypothesis, conflict/reject
    decisions, exact element leverage map, low-fidelity demo, and visual
    storyboard with image paths and notes tied to element IDs.
  - [ ] Treat text-only panels and intended image paths as draft-only. Provider
    spend waits for the operator's visual-storyboard approval.
- [ ] 5. Create the content ticket shape.
  - [ ] Use `Summary`, `Scope`, `Delta`, `Program`, `Map`, `Done / Proof`,
    `State`, `Links`, and `Notes`.
  - [ ] Make the before/after explicit: idea plus reference to executable
    production program.
- [ ] 6. Route child planning work with element realization packets.
  - [ ] For every selected element routed to a child, include element ID,
    provenance, kind, `description`, `whyItWorks`, resolved
    `goldenExample { assetId, description? }`, `goldenRecipe`, planned use, and
    acceptance check. Block generation handoffs that omit the recipe or
    example; do not route title/description-only packets.
  - [ ] For repair requests, repopulate the actual packet from the
    authoritative element record in the response. Do not emit only the packet
    type, a list of required fields, or a future retrieval instruction.
  - [ ] Route narrative, script, beats, and scene map to `storyboard`. For
    deliberate breaks, require one clean/annotated grid packet per 4-5 second
    model-native clip and load
    `video-production/references/scene-grid-production.md`.
  - [ ] Materialize each review packet through the child image/storyboard route
    as actual clean-grid and annotated-grid image files, then verify file
    existence and dimensions. Inline panels, intended paths, or a list saying
    grids will be needed are `storyboard_draft_ready`, not human-review-ready.
  - [ ] Route asset inventory, candidate discovery, rights/fit decisions, and
    recreation decisions to `asset-advisor`; require its discovery receipt
    before any image/video generation handoff or Remotion production route.
  - [ ] Route persistent presenter/character needs to `avatar-advisor`.
  - [ ] Route voice, music, SFX, Foley, SoundButtonsWorld candidate discovery,
    provider packets/execution, receipts, and mix notes to `audio-advisor`.
  - [ ] For every interesting/common SFX idea, put up to three candidate item
    links—or `searched_no_fit`—in the final plan as
    `awaiting_operator_download_and_approval`; never download them.
  - [ ] Route still or model-native generation details to `ai-image-advisor`
    and `ai-video-advisor` only when generation inputs are needed.
- [ ] 7. Compile the timing-master advisor action list.
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
- [ ] 8. End with production proof.
  - [ ] Run `creative_lock` and stop with a blocked report when narrative,
    ICP/story turns, asset evidence decisions, persona review, timing-master
    media/cues, element realization receipts,
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
- Do not let “original,” “rights-safe,” “deterministic,” or “local-only” become
  permission to skip asset discovery and draw the content as custom SVG/JSX.
  Those constraints change source selection; they do not remove the
  `asset-advisor` search gate.

## Reference Map

- `references/production-contract.md` - load after brief binding and before
  ticket compilation for Resource Bank readiness, creative lock detail, scene
  approval, and the full ticket template.
- `references/storytelling-asset-persona.md` - load for narrative/persuasive
  work; owns ICP resolution, causal beats, asset evidence, story passes, and
  persona review.
- `references/scene-asset-bundles.md` - load for every visual production scene;
  owns concrete background/main-topic/foreground bundles, readiness states,
  and the representative frame gate.
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
- `../remotion/references/documentary-reel.md` - load for a voice-led
  documentary/editorial reel using layered stills, prepared overlays, shared
  treatment, and frame-addressed motion.
