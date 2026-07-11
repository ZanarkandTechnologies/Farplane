---
name: content-impl-plan
description: "Turn a content idea and optional Tasty Pack/reference into a ticket-shaped production plan with storyboard, advisor actions, QA, and Remotion handoff."
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
  after: ["storyboard", "asset-advisor", "avatar-advisor", "audio-advisor", "ai-image-advisor", "ai-video-advisor", "remotion", "review"]
allowed-tools: Read, Grep, Glob, Bash
---

# Content Impl Plan

## Context

Use this skill when an idea, proof point, offer, or Tasty Pack/reference needs
to become an executable content-production ticket. This is the content analogue
to the coding `impl-plan`: it compiles creative intent into a storyboard, asset
decomposition, advisor action list, production order, proof contract, and final
Remotion/review path.

This skill owns the parent plan and action list. It does not generate media,
write Remotion code, render final video, publish posts, or replace the advisor
skills. It calls or routes to the primitives when their outputs are needed.

## Skill Signature

```text
content_impl_plan(idea, inspiration_pack?, icp?, platform?, proof?, constraints?, artifact_owner?)
  -> content_ticket + advisor_action_list + production_program | blocked_report

state:
  reads(user brief, Inspiration Pack/Tasty Pack captures, proof/examples/swipes,
        active ticket?, qa_checklist.md)
  writes(content implementation ticket or ticket-scoped artifact when durable
        execution is requested)

gates:
  idea_bound; audience_and_promise_named; reference_pattern_extracted;
  reference_leverage_map_present; storyboard_route_selected;
  asset_graph_planned; advisor_actions_ordered; creative_lock_passed;
  remotion_terminal_path_named; review_and_qa_contract_observable

routes:
  storyboard | asset-advisor | avatar-advisor | audio-advisor |
  ai-image-advisor | ai-video-advisor | remotion | social-content | review | qa

fails:
  storyboard_as_parent_plan; format_sprawl; vibes_only_action_list;
  advisor_actions_without_owner; remotion_without_assets; qa_afterthought;
  inspiration_pack_as_moodboard; creative_lock_skipped
```

## Big Picture

```text
idea + tasty_pack/reference
  -> content-impl-plan
      -> storyboard: narrative, script, beats, scene map
      -> asset-advisor: asset inventory, recreation plan, owner routes
      -> avatar-advisor: persistent presenter/character direction when needed
      -> audio-advisor: voice, music, SFX, Foley, cue sheet when needed
      -> ai-image-advisor: still image generation/edit/upscale route when needed
      -> ai-video-advisor: model-native clip/avatar execution route when needed
      -> remotion: React composition, stitching, captions, audio placement,
                  local render proof
      -> review/qa: creative plan, asset readiness, render/output proof
```

Inspiration Pack/Tasty Pack outputs are treated as production references, not a
moodboard. The active Resource Bank shape is:

```text
{
  request: { idea?, timeframe, startAtMs?, endAtMs?, filters },
  captures: [{ captureId, source, analysis, elements }],
  meta: { captureCount: number, timeframe: string }
}
```

Core consumer fields are only `captures[].source`, `captures[].analysis`, and
`captures[].elements`; retrieval notes are non-core metadata and must not be
required by production skills. Tags/facets live on `capture.source`. Build
`reference_leverage_map` from `captures[].elements`, focusing more on pinned
elements as the operator taste signal while keeping unpinned elements as
context. Use `analysis.operatorNote` to understand the explicit taste source and
check `meta.warnings`; when an operator note exists but nothing was pinned from
it, state the gap before treating the pack as production guidance. Extract
reusable structure without copying protected assets, likenesses, music, or
exact creative expression. Do not require separate evidence objects, lane
taxonomy, serialized `production_pattern`, or frame/clip records unless the
specific production task needs direct media reuse or audit proof.

For inspiration-led video, classify the pack before production:

```text
reference_readiness(pack)
  -> media_ready | regen_ready | semantic_only | blocked

media_ready:
  pinned visual/audio/editing elements have resolved media refs such as
  frame/contact-sheet/thumbnail/clip/audio/transcript paths or URLs.

regen_ready:
  pinned elements have enough anchors/descriptions to route concrete
  regeneration packets through ai-image-advisor, ai-video-advisor, audio-advisor,
  or avatar-advisor before Remotion.

semantic_only:
  pinned elements describe taste but no media refs, generation prompts, or
  source assets exist yet. Use only for storyboard/plan output, not final
  production claims.
```

Before routing to Remotion, run the creative lock:

```text
creative_lock(idea, inspiration_pack, storyboard, asset_plan, audio_plan)
  -> locked_brief | blocked_report

requires:
  - reference_leverage_map: each used capture element maps to a
    concrete shot, asset, edit rhythm, audio cue, motion cue, or narrative move
  - reference_classification: the chosen reference type, such as product-ad
    parody, myth explainer, process reveal, corporate training, montage, or
    proof demo, plus the rejected nearby formats
  - narrative_spine: hook -> tension -> turn -> proof -> payoff with exact
    script/caption beats and viewer job
  - continuity_spine: recurring character or explicit no-character rationale,
    recurring object/motif when the reference relies on one, scene-to-scene
    visual continuity, and the viewer question -> answer
  - asset_manifest: source/generated/linked assets or explicit missing-asset
    blockers before composition
  - media_or_regen_plan: each pinned visual/audio/editing element either has a
    resolved media ref, a regeneration packet, or an explicit nonuse reason
  - cue_sheet: frame/time-coded audio events and required motion bindings
  - generation_topology: `continuous_chain`, `deliberate_scene_breaks`, or
    `montage`, with start/end frame pairs for chained model-native video clips
    and transition obligations for scene breaks
  - qa_gates: user-intent, video-quality, source-honesty, inspiration-use,
    narrative clarity, asset use, and audio-motion sync

blocks_if:
  - the visual plan is only generic CSS/text/cards for an inspiration-led video
  - the audio plan is only a bed with no motion/edit obligations
  - a narrative reel plans isolated model-native clip generations without
    start/end frame continuity or explicit montage rationale
  - the plan copies reference art direction while dropping the reference's core
    story engine, standout character, recurring prop, or audio/edit structure
  - an inspiration-led video has pinned visual/audio anchors but no resolved
    media refs and no regeneration route before Remotion
  - proof checks only renderability
```

## Phase Boundary

Plan inline by default. Use the child skills only when their output is needed
for the ticket to be executable. Use `review` before execution when the plan
will guide a public campaign, paid spend, high-visibility proof, or close
reference recreation. Use `qa` when a produced artifact needs formal proof.

<!-- BEGIN FARPLANE_IMPORTANT_CHECKLIST -->
## Todo List

- [ ] 1. Bind the implementation brief.
  - [ ] Resolve idea, ICP, viewer promise, proof, platform, Inspiration
    Pack/Tasty Pack/reference material, target artifact, constraints, CTA,
    deadline, and artifact owner.
  - [ ] Read `qa_checklist.md` as preflight guardrails.
- [ ] 2. Extract the reference pattern.
  - [ ] Identify hook stack, timeline beats, story pattern, pacing, format
    affordances, visual/audio/editing/copy/format/constraint elements, and why
    the reference likely works.
  - [ ] Classify the reference/reel type and choose one production pattern;
    explicitly reject nearby patterns that would change the story engine.
  - [ ] Mark what to reuse as structure versus what must be changed for rights,
    brand, audience, or proof.
  - [ ] Build a `reference_leverage_map` from `captures[].elements` to
    specific planned shots, assets, audio cues, motion cues, or narrative beats;
    map pinned elements first and explain any pinned element not reused. If
    `meta.warnings` says an operator note exists but no element was pinned from
    it, state the gap before treating the pack as production guidance.
  - [ ] Classify `reference_readiness` as `media_ready`, `regen_ready`,
    `semantic_only`, or `blocked`; for inspiration-led video, do not route to
    Remotion as production until pinned visual/audio/editing elements have
    resolved media refs or concrete regeneration packets.
- [ ] 3. Create the content ticket shape.
  - [ ] Use `Summary`, `Scope`, `Delta`, `Program`, `Map`, `Done / Proof`,
    `State`, `Links`, and `Notes`.
  - [ ] Make the before/after explicit: idea plus reference to executable
    production program.
- [ ] 4. Route child planning work.
  - [ ] Route narrative, script, beats, and scene map to `storyboard`.
  - [ ] Route asset inventory and recreation decisions to `asset-advisor`.
  - [ ] Route persistent presenter/character needs to `avatar-advisor`.
  - [ ] Route voice, music, SFX, Foley, and mix notes to `audio-advisor`.
  - [ ] Route still or model-native generation details to `ai-image-advisor`
    and `ai-video-advisor` only when generation inputs are needed.
- [ ] 5. Compile the advisor action list.
  - [ ] Order actions by dependency: storyboard, assets, generation/capture,
    audio, Remotion composition, render proof, review/QA.
  - [ ] For narrative video, declare generation topology before spend:
    `continuous_chain`, `deliberate_scene_breaks`, or `montage`; block isolated
    clip batches unless the chosen format is intentionally montage.
  - [ ] Give every action an owner skill, input, output, acceptance check, and
    blocker condition.
- [ ] 6. End with production proof.
  - [ ] Run `creative_lock` and stop with a blocked report when narrative,
    assets, cue timing, inspiration-use evidence, or QA gates are missing.
  - [ ] Route final stitching, captions, overlays, audio placement, and local
    render proof to `remotion` only after `creative_lock` passes.
  - [ ] Name review and QA checklist gates before claiming the plan ready.
  - [ ] Apply `qa_checklist.md` again before completion.
<!-- END FARPLANE_IMPORTANT_CHECKLIST -->

## Ticket Template

```text
## Summary
What content will be produced, for whom, and what proof or marketing job it
must do.

## Scope
- In:
- Out:
- Platform:
- Target artifact:
- Reference / Tasty Pack:
- CTA:

## Delta
- Before:
- After:
- Why now:

## Program
Reference Pattern:
- Hook:
- Hook stack:
- Timeline beats:
- Story / format:
- Visual pattern:
- Audio pattern:
- Motion / edit pattern:
- Proof mechanism:
- Must change:

Reference Leverage Map:
| Capture / Element | Anchor | Reused As | Planned Output | Acceptance Check |
| --- | --- | --- | --- | --- |

Advisor Action List:
| Order | Owner | Input | Output | Acceptance Check | Blocker |
| ---: | --- | --- | --- | --- | --- |

## Map
- Storyboard:
- Assets:
- Avatar:
- Audio:
- Image generation:
- Video generation:
- Remotion:
- Review / QA:

## Done / Proof
- plan_ready_when:
- production_ready_when:
- render_proof:
- review:
- residual_risk:

## State
draft | review | approved | in_production | blocked

## Links
- source proof:
- Tasty Pack / reference:
- child artifacts:
- outputs:

## Notes
- Rejected angles:
- Rights / usage notes:
- Taste notes:
```

## Gotchas

- Do not make `storyboard` carry the whole implementation plan. Storyboard owns
  narrative and scene design; this skill owns the parent ticket and production
  action list.
- Do not create format-specific skills for every trend. Use Tasty Pack or
  references to extract the pattern, then route through stable primitives.
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

- `qa_checklist.md` - read at start and finish for content implementation plan
  QA.
- `../storyboard/SKILL.md` - narrative, script, beat sheet, and scene map.
- `../asset-advisor/SKILL.md` - asset inventory, recreation plan, and owner
  routes.
- `../avatar-advisor/SKILL.md` - persistent avatar, presenter, or lipsync
  direction.
- `../audio-advisor/SKILL.md` - voice, music, SFX, Foley, cue sheet, and mix
  direction.
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
- `production_program`: reference leverage map, storyboard, asset, generation,
  audio, creative lock, Remotion, review, and QA route map.
- `blocked_report`: missing idea, reference, proof, rights, production route,
  owner, or proof gate.
