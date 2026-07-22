---
name: asset-advisor
description: "Turn a storyboard, reference video, Tasty Pack, or source material into a production-ready asset inventory and recreation plan."
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
  after: ["storyboard", "ai-image-advisor", "ai-video-advisor", "avatar-advisor", "audio-advisor", "remotion"]
allowed-tools: Read, Grep, Glob, Bash
---

# Asset Advisor

## Context

Use this skill when a content plan needs to know what assets exist, what must be
created, what can be recreated from references, and which production skill owns
each asset. It is the decomposition layer for Tasty Pack outputs, swipe files,
example videos, storyboards, and source media.

This skill owns asset inventory, recreation strategy, route selection, rights
and source notes, and handoff packaging. It does not generate images, render
videos, compose Remotion timelines, record audio, or publish content.

## Skill Signature

```text
asset_advisor(storyboard_or_reference, element_realization_packets?, source_assets?, platform?, constraints?, artifact_owner?)
  -> asset_inventory + recreation_plan + generation_routes | blocked_report

state:
  reads(user brief, storyboard/reference material, complete element realization
        packets, source asset paths or URLs, qa_checklist.md)
  writes(asset plan artifact when durable handoff is requested)

gates:
  source_material_named; rights_or_usage_risk_noted; asset_units_decomposed;
  reference_elements_mapped; golden_examples_and_recipes_bound;
  recreate_reuse_generate_decisions_made;
  route_owner_selected; remotion_handoff_ready_when_stitching_needed

routes:
  storyboard | ai-image-advisor | ai-video-advisor | avatar-advisor |
  audio-advisor | remotion | media-ingest | video-understanding | review

fails:
  vague_asset_bucket; reference_copy_without_rights_note;
  generation_prompt_without_asset_inventory; remotion_handoff_without_files;
  one_tool_for_every_asset; css_text_only_for_inspiration_led_video;
  inspiration_elements_unmapped; title_only_element_handoff
```

## Phase Boundary

Use `media-ingest` or `video-understanding` when the input is raw media that
needs metadata, transcripts, or representative frames before decomposition. Use
`review` when a recreation plan copies a specific reference closely or will
drive a high-visibility campaign.

For Brand Kit or Tasty Pack inputs, treat complete element realization packets
as the source of truth. Every relevant `visual`, `storyboard`, `editing`, `format`, or
`constraint` element must either map to a concrete asset decision or appear in
`Missing inputs`. Map pinned elements first because they are the operator's
taste signal; preserve unpinned elements as context decisions or
blockers rather than treating every element equally. For inspiration-led videos, return a
`blocked_report` when the plan only offers generic CSS/text/cards without
source, generated, linked, captured, or explicitly composed assets justified by
the reference leverage map.

For each selected element, require its complete realization packet. Use the
resolved `goldenExample` plus `goldenRecipe` together to choose `reuse`,
`source`, `regenerate`, `capture`, or `compose`; return an incomplete handoff
instead of reducing the element to title/description.

When a Tasty Pack element includes an `anchor` such as `contact_sheet`,
`frame_08_28.58s`, `frames 1-4`, or `OG thumbnail`, first try to resolve
`source.assetId + anchor` into a concrete media ref. If no media ref is
available, emit a regeneration packet with the pinned element, anchor,
reference source, rights notes, and acceptance check. Do not let anchored
visual/audio/editing elements collapse into generic Remotion drawings unless
the output is explicitly downgraded to `semantic_storyboard_only`.

<!-- BEGIN FARPLANE_IMPORTANT_CHECKLIST -->
## Todo List

- [ ] 1. Bind the source and target.
  - [ ] Identify the storyboard, reference/Inspiration Pack capture, creative
    elements, source handles/assets, target platform, dimensions, duration, style
    constraints, and artifact owner.
  - [ ] Read `qa_checklist.md` as preflight guardrails.
- [ ] 2. Decompose the asset graph.
  - [ ] List footage, stills, frames, clips, avatars, voiceover, music, SFX,
    captions, overlays, fonts, logos, data, product shots, motion/edit
    references, and final render needs.
  - [ ] Mark each asset as `reuse`, `source`, `regenerate`, `capture`,
    `compose`, or `unknown`.
  - [ ] Map each relevant Brand Kit or Tasty Pack element to an asset row,
    generation route, or missing-input blocker, prioritizing pinned elements
    before ordinary context elements.
  - [ ] For every selected element, carry its ID/provenance, description,
    whyItWorks, resolved golden example, golden recipe, planned use, and
    acceptance check into the asset decision and downstream generation packet.
  - [ ] Resolve `assetId + anchor` into media refs when possible; otherwise
    create regeneration packets for pinned visual/audio/editing elements before
    Remotion.
  - [ ] For narrative video, create continuity assets: character bible or
    no-character rationale, recurring prop/object bible, location/lighting
    anchors, and start/end frame assets for each model-native clip handoff.
- [ ] 3. Add recreation constraints.
  - [ ] Note rights, likeness, brand, source quality, duration, aspect ratio,
    visual continuity, audio continuity, and platform-specific constraints.
- [ ] 4. Choose owner routes.
  - [ ] Route still image creation or editing to `ai-image-advisor` or
    `imagegen`.
  - [ ] Route model-native clips to `ai-video-advisor`.
  - [ ] Route persistent presenter or character direction to `avatar-advisor`.
  - [ ] Route voice, music, SFX, Foley, and mix notes to `audio-advisor`.
  - [ ] Route deterministic assembly, captions, overlays, and local render
    proof to `remotion`.
- [ ] 5. Produce the handoff.
  - [ ] Include an asset table, file/source map, generation prompts or prompt
    briefs, acceptance checks, missing inputs, and next production owner.
  - [ ] Apply `qa_checklist.md` again before calling the asset plan ready.
<!-- END FARPLANE_IMPORTANT_CHECKLIST -->

## Output Template

```text
## Asset Inventory
| Asset | Role | Source | Decision | Owner | Acceptance Check |
| --- | --- | --- | --- | --- | --- |

## Inspiration Element Map
| Element | Anchor | Asset Decision | Output / Blocker |
| --- | --- | --- | --- |

## Regeneration Packets
| Packet | Source Element | Anchor | Owner | Prompt / Direction | Acceptance Check |
| --- | --- | --- | --- | --- | --- |

## Recreation Plan
- Reference pattern:
- What to preserve:
- What to change:
- Continuity anchors:
- Start/end frame plan:
- Rights / likeness notes:
- Missing inputs:

## Routes
- Images:
- Video clips:
- Avatar:
- Audio:
- Remotion:

## Done / Proof
- ready_when:
- evidence:
- residual_risk:
```

## Gotchas

- Do not treat a viral reference as permission to clone exact visuals,
  likenesses, music, or protected assets. Name the risk and recreate the
  underlying pattern.
- Do not hand Remotion a vague mood board. It needs files, durations, scene
  roles, dimensions, captions, and acceptance checks.
- Do not hand Remotion an inspiration-led asset plan where every visual is
  generic CSS/text/cards unless the run is explicitly labeled `technical_smoke`
  or `text_only_format` and the content claim is downgraded.
- Do not discard Tasty Pack anchors. If the pack says `frame_03_8.42s` or
  `contact_sheet`, the asset plan must either resolve that media or regenerate
  from it; a verbal paraphrase is not enough for production.
- Do not collapse avatar, audio, stills, and model-native clips into one generic
  prompt. Each asset class has different continuity and proof needs.

## Reference Map

- `qa_checklist.md` - read at start and finish for asset-plan QA.
- `../storyboard/SKILL.md` - route narrative, script, and scene planning before
  asset decomposition when the creative plan is not ready.
- `../ai-image-advisor/SKILL.md` - route still generation, edits, upscales, and
  cutouts.
- `../ai-video-advisor/SKILL.md` - route model-native clip generation or edits.
- `../avatar-advisor/SKILL.md` - route persistent presenter, character,
  likeness, or lipsync direction.
- `../audio-advisor/SKILL.md` - route voice, music, Foley, SFX, and mix plans.
- `../remotion/SKILL.md` - route final deterministic composition and local
  render proof after assets are specified.

## Output

- `asset_inventory`: decomposed asset table with source, decision, owner, and
  acceptance check.
- `recreation_plan`: what to preserve, change, regenerate, source, or compose.
- `generation_routes`: concrete next-owner handoffs for each asset class.
- `blocked_report`: missing source material, rights uncertainty, missing
  storyboard, unsupported asset class, absent render route, or unmapped
  Inspiration Pack elements.
