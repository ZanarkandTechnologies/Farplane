---
name: storyboard
description: "Turn a content implementation plan, idea, ICP, proof, or offer into script, beats, and storyboard scenes for production handoff."
tier: 3
group: marketing
source: local
template_uses:
  skill-template: "0.3.7"
  skill-qa-checklist: "0.1.1"
  skill-eval-task: "0.2.0"
  skill-surface-budget: "0.1.0"
eval: evals/evals.json
qa_checklist: qa_checklist.md
common_chains:
  after: ["asset-advisor", "audio-advisor", "avatar-advisor", "remotion", "social-content"]
allowed-tools: Read, Grep, Glob, Bash
---

# Storyboard

## Context

Use this skill when a content implementation plan, creative idea, proof point,
offer, or campaign goal needs script, beats, and storyboard scenes before
production. It is a child primitive of `content-impl-plan`: it turns the chosen
idea and reference pattern into narrative signatures, beat structure, scene
requirements, and production-facing shot notes.

This skill owns narrative and scene design. It does not own the parent content
implementation ticket, asset decomposition, media generation, Remotion code,
publishing, or final creative QA. Route parent planning to `content-impl-plan`
and production-specific work to the relevant advisor or Remotion skill.

## Skill Signature

```text
storyboard(idea_or_brief, icp?, proof?, platform?, duration?, style?, cta?, reference_pattern?, source_title?, element_realization_packets?, generation_topology?, artifact_owner?)
  -> script_storyboard + hook_decision? + scene_handoff + scene_grid_packets? | blocked_report

state:
  reads(user brief, supplied proof/examples/swipes, active ticket?,
        qa_checklist.md, examples/remotion-proof-video/example.md when useful)
  writes(storyboard artifact or content-ticket section when durable output is requested)

gates:
  viewer_promise_bound; proof_or_reason_to_believe_named;
  narrative_signatures_present; short_form_hook_compared_when_applicable;
  beat_sheet_and_script_aligned;
  storyboard_executable; selected_elements_mapped_to_beats_and_panels;
  low_fi_visual_storyboard_observable; asset_needs_named; scene_handoff_observable;
  asset_discovery_handoff_named; no_custom_svg_animation_assets;
  scene_grid_packets_reviewable_when_deliberate_breaks

routes:
  content-impl-plan | asset-advisor | audio-advisor | avatar-advisor |
  remotion | ai-video-advisor | social-content | review

fails:
  vague_video_idea_as_plan; script_without_shots; shots_without_viewer_promise;
  generic_brand_filler; parent_action_list_hidden_in_storyboard;
  production_handoff_without_assets_or_proof;
  short_form_hook_lab_incomplete; source_title_not_compared;
  hook_requires_jargon_decoding;
  custom_svg_animation_asset; missing_asset_discovery_route;
  publishing_or_rendering_as_default
```

## Phase Boundary

Plan inline by default. Use `content-impl-plan` when the user needs the parent
ticket, advisor action list, and execution order. Use `research` only when current platform norms, peer
examples, official specs, or source material materially affect the script. Use
`review` when a material creative plan needs independent judgment before
production. Hand off to production skills only after this skill has named the
scene handoff, asset needs, proof, and blocker conditions.

<!-- BEGIN FARPLANE_IMPORTANT_CHECKLIST -->
## Todo List

- [ ] 1. Bind the creative ticket inputs.
  - [ ] Resolve or state assumptions for ICP, viewer promise, core idea, proof
    or reason to believe, platform, duration, style, CTA, constraints, and
    artifact owner.
  - [ ] Read `qa_checklist.md` as preflight guardrails.
- [ ] 2. Choose the artifact home.
  - [ ] Use `tickets/TASK-XXXX/artifacts/storyboard.md` when an active
    ticket owns the work.
  - [ ] Use `.farplane/content/<date>-<slug>/storyboard.md` for a fast
    proof run without an owning ticket.
  - [ ] Keep chat-only output only for tiny sketches where no production or
    review handoff is expected.
- [ ] 3. Draft the narrative spine.
  - [ ] Include `Narrative Signatures`: hook, tension, turn, proof moment,
    payoff, and final action.
  - [ ] For short-form, latest-news, title-led, or retention-sensitive work,
    load the [plain-language hook lab](references/plain-language-hook-lab.md)
    and complete it before drafting the script:
    `hook_lab(idea, proof, audience, source_title?) -> candidates[10+] +
    finalists[3+] + winner + first_3_seconds + rejected_reasons`.
    Generate materially different promises and causal framings, not minor
    synonym swaps. Tag candidates across at least six lenses—actor causes
    consequence, actor stops/reverses consequence, contradiction, before/after,
    unexpected buyer/payer/helper, threat/deadline, familiar comparison, or
    simple paradox—and use no more than two candidates from one lens. Output
    all ten or more candidates and the full finalist comparison; do not
    silently collapse the lab to a few preferred lines.
    Compare finalists with the source title when one exists.
  - [ ] Make the winning hook child-simple without becoming childish: an
    unfamiliar general viewer should understand it immediately, normally as
    one recognizable actor, one concrete action, and one understandable
    consequence. For a short-form display hook, target at most eight words;
    let the following voiceover carry necessary detail. Prefer one-breath
    phrasing and words a viewer can visualize.
    Reject unexplained legal, financial, technical, or infrastructure jargon;
    reject abstract bridge phrases such as `get the money`, `get backing`,
    `help fund`, or `secure financing` when the evidence supports an ordinary
    visible action such as `help buy`, `help pay`, `build`, `stop`, or `save`.
    If the hook needs a definition before it becomes interesting, rewrite it.
    `Help` is allowed only when it directly modifies a concrete action such as
    `help buy`, `help build`, or `help pay`; the second verb carries the image.
    When two named actors appear, repeat the relevant name or object instead of
    using an ambiguous `it`, `its`, `they`, or `their`.
    Before ranking finalists, remove any display hook containing `guarantee`,
    `back`, `backing`, `finance`, `financing`, `fund`, `funding`, `secure`,
    `support`, `get money`, `get backing`, or `unlock` unless the ordinary word
    itself is the story and the audience already understands it. A blocked
    display term cannot win by receiving a high score elsewhere. The displayed
    candidate table is the post-cleanup set: blocked drafts may appear only
    under rejected lines with the rejection reason, never as candidates or
    finalists.
    Do not replace source jargon with a coined simplification such as `AI
    factory`, `computer hub`, or another label the audience must also decode.
    Prefer a familiar evidence-backed noun, or move the object detail into
    sentence two. When one company may help a customer obtain that same
    company's product, surface that simple loop directly in the hook.
    After drafting, mark candidates that only restate another line, weaken the
    evidence-backed relationship, or change syntax without changing actor,
    action, consequence, or question opened. Keep them only when their rejection
    reason is visible, and exclude them from the finalist comparison.
  - [ ] Select the winner on immediate comprehension, curiosity, factual
    accuracy, spoken brevity, and first-frame visual potential. It must beat
    the supplied source title on the combined test or remain unlocked. Record
    why the strongest rejected finalists lost.
  - [ ] Bind the winner to the exact first three seconds: on-screen copy,
    voiceover, dominant visual action, and compact evidence qualifier. Preserve
    uncertainty in reported, forecast, alleged, or unsigned developments; do
    not buy drama by turning a possibility into a fact.
    For an applicable hook-lab branch, populate every `Hook Decision` template
    field before returning: the complete candidate table with keep/reject
    reasons, three or more finalists, the criterion-by-criterion source-title
    contest, winner rationale, rejected-finalist reasons, and all four
    first-three-second fields. Missing fields return an incomplete draft or
    blocker, not a silently shortened hook decision.
  - [ ] For a voice-led documentary or editorial reel, load the
    [documentary reel production contract](../remotion/references/documentary-reel.md).
    Usually use five or six compact causal clauses, but derive scene ranges
    from measured narration. Give every scene one viewer-state change, one
    dominant spatial action, background/subject/foreground needs, named
    frame-addressed events, micro-motion, and audio/caption obligations.
  - [ ] If the user needs a full ticket/action list, route back to
    `content-impl-plan` instead of expanding this skill's scope.
- [ ] 4. Write the script and storyboard as one connected plan.
  - [ ] Produce beat sheet, voiceover or on-screen copy, scene-by-scene
    storyboard panels, shot list, motion notes, audio notes, captions or
    supers, and asset requirements.
  - [ ] Make every missing visual requirement searchable by naming the concrete
    subject, material identity, source classes, rights constraint, framing, and
    acceptance check for `asset-advisor`. Do not resolve missing visuals by
    prescribing custom-created SVG animation assets, SVG/JSX illustrations, or
    programmatic vector stand-ins.
  - [ ] Use the available narration and causal beat to make that brief specific
    enough to search now. Do not hide behind generic labels such as “primary
    visual,” “editorial framing,” or “supporting prop” when the clause names a
    recognizable place, person type, object, document, product, or event.
  - [ ] Emit one searchable Asset Advisor row per storyboard scene; each row
    names subject, material identity, source classes, rights constraint,
    framing/crop, and acceptance check. A partial asset list cannot represent a
    scene-complete handoff.
  - [ ] When element realization packets are supplied, map each selected
    story-facing hook/copy/storyboard/format/constraint element ID to a beat or
    panel and condition the visual notes on both its resolved golden example
    and golden recipe. Return incomplete packets instead of using title-only
    reference prose.
  - [ ] Ensure each beat has a viewer job and each shot has a production job.
  - [ ] For narrative video, make the storyboard connected: recurring character
    or explicit no-character rationale, recurring object/motif when useful,
    viewer question -> answer, and scene-to-scene cause/effect.
  - [ ] For `continuous_chain`, include start/end frame handoff pairs for every
    generated clip. For `deliberate_scene_breaks`, load
    [scene-grid production](references/scene-grid-production.md), partition the
    timeline into normally 4-5 second scene units, and create one clean grid,
    one matching annotated grid, and keyed notes per provider clip. Each unit
    gets one dominant action and camera/POV; cross-clip frame continuity is not
    required at an intentional cut. Do not output isolated pretty panels unless
    the format is montage.
  - [ ] Give every scene packet stable panel IDs, start/action/end state,
    fixed landmark and minimum displacement when motion must be measurable,
    continuity anchors, canonical character path/hash, provider strategy,
    transition/audio obligations, approved asset paths, and `reuse_locked`
    policy. A safety or provider fallback that changes visible identity
    invalidates the affected approval and returns the revised character card
    and grids to human review. Preserve the canonical card/path/hash unchanged,
    create the fallback as a versioned sibling, and leave unaffected approved
    scene packets locked. Use the stable fields `canonical_character_path` and
    `canonical_character_sha256` in both the scene packet and `approved.json`.
- [ ] 5. Select the production route.
  - [ ] Route parent ticket/action-list planning to `content-impl-plan`.
  - [ ] Route asset decomposition, candidate discovery, rights/fit decisions,
    and recreation planning to `asset-advisor`; block Remotion while required
    visual rows lack accepted files. Complete `inspired_generation` /
    `original_generation` packets route image or video owners but never unlock
    Remotion by themselves. Candidate discovery may select a source, produce
    an `inspiration_for_generation` packet with transferable traits and
    must-not-copy constraints, or record `searched_no_reference` and route an
    original raster/video generation brief.
  - [ ] Route persistent presenter or character direction to `avatar-advisor`.
  - [ ] Route voice, music, SFX, Foley, and mix notes to `audio-advisor`.
  - [ ] Route deterministic motion graphics, captions, overlays, and editing to
    `remotion`.
  - [ ] Route model-native footage or generated clips to
    `ai-video-advisor`.
  - [ ] Route a parent action graph to `content-impl-plan`; route platform ad
    specs and distribution copy to `social-content`.
  - [ ] Route captions, launch copy, thread, carousel, or platform copy to
    `social-content`.
- [ ] 6. Make proof and review observable.
  - [ ] For deliberate breaks, make the minimum human review packet an overview
    strip plus every scene's existing, dimension-verified clean-grid and
    annotated-grid image files, keyed notes, and the recurring-character card.
    Ask for feedback on the visual identity and scene packets before production.
    Text-only panels remain a draft. Name
    render, still-frame, storyboard-review, script-review, or
    production-handoff evidence; generation starts only after approval.
  - [ ] For content-impl-plan handoffs, emit low-fidelity visual storyboard
    image paths plus notes tied to element IDs; text-only panels and intended
    paths remain draft-only.
  - [ ] Apply `qa_checklist.md` again before calling the plan production-ready.
  - [ ] Use `review` for material campaign claims, high-visibility output, or
    taste-sensitive plans that will guide real production.
- [ ] 7. Output the handoff without doing production by default.
  - [ ] Return the artifact path or inline creative ticket, the selected
    production route, required assets, proof contract, blockers, and next owner.
<!-- END FARPLANE_IMPORTANT_CHECKLIST -->

## Templates

Storyboard core:

```text
Hook Decision (required for short-form/latest-news/title-led work):
- Source title:
- Candidates (10+, tagged across 6+ lenses):
  | Lens | Hook | keep / reject + reason |
  | --- | --- | --- |
- Finalists (3+):
- Winner:
- Why it beats the source title:
- Rejected finalists + reasons:
- Source-title contest:
  | Line | Immediate meaning | Curiosity | Accuracy | One breath | Drawable first frame | Verdict |
  | --- | --- | --- | --- | --- | --- | --- |
  | Source title | | | | | | |
  | Finalist A | | | | | | |
  | Finalist B | | | | | | |
  | Finalist C | | | | | | |
- First 3 seconds:
  - On-screen copy:
  - Voiceover:
  - Visual action:
  - Evidence qualifier:

Narrative Signatures:
- Hook:
- Tension:
- Turn:
- Proof moment:
- Payoff:
- Final action:

Beat Sheet:
1.

Script:
- Scene 1:

Storyboard:
| Scene | Time | Visual | Copy/VO | Motion | Assets | Proof |
| --- | ---: | --- | --- | --- | --- | --- |

Continuity Handoff:
- Reel / reference type:
- Viewer question -> answer:
- Recurring character / no-character rationale:
- Recurring object or motif:
- Generation topology: continuous_chain | deliberate_scene_breaks | montage
- Frame pairs:
  - Clip 1 start frame -> end frame:
- Scene breaks / transitions:

Scene Grid Packets (required for deliberate_scene_breaks):
| Scene | Target seconds | Clean grid | Annotated grid | Panel IDs | Action / camera / end state | Provider strategy | Transition / audio | Reuse |
| --- | ---: | --- | --- | --- | --- | --- | --- | --- |

## Notes
- Rejected angles:
- Taste notes:
- Blockers:
```

Short positive example: load
`examples/remotion-proof-video/example.md` when the task needs a concrete model
of a Remotion-ready creative ticket.

## Gotchas

- Do not output only a premise, angle, or theme when the user needs production.
  The plan must include beats, script, storyboard panels, asset needs, and
  proof.
- Do not treat an accurate sentence or shortened source headline as a strong
  hook. For applicable short-form work, generate alternatives, compare the
  strongest candidates, and reject openings that require jargon decoding
  before the viewer can feel curiosity or stakes.
- Do not separate script quality from shot feasibility. If the copy implies a
  visual, name the shot or asset; if the shot carries the point, name the copy
  or viewer job.
- Do not claim platform-native quality without current platform evidence,
  supplied examples, or an explicit local-only assumption.
- Do not render, publish, post, upload, or spend external compute unless the
  user explicitly asks for that next action.
- Do not use one whole-video grid as the only input contract for several
  deliberate-break calls. Do not regenerate an approved grid or character
  reference unless the operator requests it or a named scene-local blocker or
  approved edit requires a versioned replacement.
- Do not use custom SVG/JSX drawings as a shortcut around a missing visual.
  Existing accepted SVG media can appear in a storyboard, but sourcing and
  rights belong in the Asset Advisor handoff.

## Reference Map

- `qa_checklist.md` - read at start and finish for storyboard QA.
- `references/plain-language-hook-lab.md` - load for short-form, latest-news,
  title-led, or retention-sensitive work before drafting the script.
- `examples/remotion-proof-video/example.md` - load when a Remotion-ready
  example would improve the creative ticket or proof handoff.
- [scene-grid production](references/scene-grid-production.md) - load when
  deliberate scene breaks map storyboard grids to model-native provider clips.
- `../remotion/references/documentary-reel.md` - load for voice-led
  documentary/editorial reels that need causal clauses, layered scenes,
  frame-addressed choreography, and shared treatment handoff.
- `../remotion/SKILL.md` - route deterministic composition authoring after the
  storyboard names dimensions, duration, assets, scenes, and proof.
- `../social-content/SKILL.md` - route captions, launch copy, threads,
  carousels, or platform distribution drafts after production planning.

## Output

- `script_storyboard`: narrative signatures, beats, script, scenes, shots, and
  visual/audio notes.
- `scene_handoff`: selected route, required assets, scene map, proof
  contract, and next owner.
- `scene_grid_packets`: for deliberate scene breaks, one reviewed clean and
  annotated image grid plus keyed notes, file/dimension receipt, and reuse state
  per provider clip.
- `blocked_report`: missing ICP, proof, platform, asset permission, production
  route, or review/proof condition.
