---
name: asset-advisor
description: "Turn a storyboard, reference video, Tasty Pack, or source material into a production-ready asset inventory and recreation plan."
tier: 3
group: marketing
source: local
template_uses:
  skill-template: "0.3.7"
  skill-eval-task: "0.2.0"
  skill-surface-budget: "0.1.0"
common_chains:
  after: ["storyboard", "ai-image-advisor", "ai-video-advisor", "avatar-advisor", "audio-advisor"]
allowed-tools: Read, Grep, Glob, Bash
---

# Asset Advisor

## Context

Use this skill when a content plan needs to know what assets exist, what must be
created, what can be recreated from references, and which production skill owns
each asset. It is the decomposition layer for Tasty Pack outputs, swipe files,
example videos, storyboards, and source media.

This skill owns the asset lane: asset inventory, recreation strategy, route
selection, rights and source notes, candidate discovery, accepted files, and
asset-receipt packaging. It must search
for useful existing assets before routing generation unless the brief
explicitly requires an original generated asset. Search is not stock-only: it
may select a rights-cleared source or create a bounded inspiration packet for
original raster/video generation. It may route image, video, avatar, and audio
realization children, but Content Impl Plan remains the orchestrator. It does
not author storyboards, edit direction, Remotion timelines, rendered proof, or
publication.

## Skill Signature

```text
asset_advisor(storyboard_or_reference, element_realization_packets?, source_assets?, platform?, constraints?, artifact_owner?)
  -> asset_inventory + recreation_plan + generation_routes
   + accepted_asset_files + provenance + asset_receipts | blocked_report

state:
  reads(user brief, storyboard/reference material, complete element realization
        packets, source asset paths or URLs, the first-load Todo List guardrails)
  writes(asset plan artifact when durable handoff is requested)

gates:
  source_material_named; rights_or_usage_risk_noted; asset_units_decomposed;
  source_usage_role_and_rights_status_separated;
  candidate_discovery_receipt_complete; asset_resolution_decision_complete;
  inspiration_packet_complete_when_used; moodboard_traits_accepted_before_prompt;
  no_custom_svg_animation_assets;
  reference_elements_mapped; golden_examples_and_recipes_bound;
  recreate_reuse_generate_decisions_made;
  route_owner_selected; downstream_asset_handoff_ready

routes:
  storyboard | ai-image-advisor | ai-video-advisor | avatar-advisor |
  audio-advisor | media-ingest | video-understanding | review

fails:
  vague_asset_bucket; reference_copy_without_rights_note;
  generation_prompt_without_asset_inventory; downstream_handoff_without_files;
  one_tool_for_every_asset; css_text_only_for_inspiration_led_video;
  inspiration_elements_unmapped; title_only_element_handoff;
  ungrounded_generation_without_explicit_brief; inspiration_without_trait_map;
  reference_copy_disguised_as_generation; custom_svg_animation_asset;
  jsx_or_programmatic_drawing_as_asset_substitute;
  invalid_discovery_result; expected_output_is_directory
```

## Phase Boundary

Use `media-ingest` or `video-understanding` when the input is raw media that
needs metadata, transcripts, or representative frames before decomposition. Use
`review` when a recreation plan copies a specific reference closely or will
drive a high-visibility campaign.

When the user has approved execution and search tools are available, candidate
discovery is an action in the current run, not a future recommendation. Execute
the searches, inspect useful candidates, and populate the receipt. If the
storyboard is too vague to search, first turn each scene into a concrete asset
need from the available narration/reference; block only the unresolved rows. If
search tooling or required scene meaning is genuinely unavailable, return an
exact blocker rather than a production-ready plan or a table whose only result
is `pending`. Tool unavailability is not `searched_no_reference`; that result
requires an executed search receipt with specific candidate pages or asset IDs
and fit decisions.

For Brand Kit or Tasty Pack inputs, treat complete element realization packets
as the source of truth. Every relevant `visual`, `storyboard`, `character`,
`audio`, or `format` element that implies a file must either map to a concrete
asset decision or appear in `Missing inputs`. Editing patterns remain owned by
the sibling Editing Advisor; this skill maps only their explicit media
dependencies. Map pinned elements first because they are the operator's
taste signal; preserve unpinned elements as context decisions or
blockers rather than treating every element equally. For inspiration-led videos, return a
`blocked_report` when the plan only offers generic CSS/text/cards without
source, generated, linked, captured, or explicitly composed assets justified by
the reference leverage map.

For each selected element, require its complete realization packet. Use the
resolved `goldenExample` plus `goldenRecipe` together to choose `reuse`,
`source`, `inspired_generation`, `original_generation`, `capture`, or
`compose`; return an incomplete handoff instead of reducing the element to
title/description.

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
  - [ ] Read the first-load Todo List guardrails as preflight guardrails.
- [ ] 2. Decompose the asset graph.
  - [ ] Classify every supplied or discovered reference on two independent
    axes before deciding whether to use it: `usage_role` is one of
    `production_source`, `cinematic_reference`, `taste_discovery`,
    `archive_reference`, or `generated`; `rights_status` is one of `cleared`,
    `restricted_reference_only`, `per_item_verification_required`, or
    `unknown`. A useful reference is not automatically licensed production
    media. Load [source roles and moodboard gate](references/source-roles.md)
    when the brief mixes source libraries, film frames, galleries, or social
    discovery.
  - [ ] Before choosing generation, search for useful existing assets unless
    the brief explicitly requires an original generated asset. Inspect
    supplied/local media and Resource Bank/reference anchors, then suitable
    web, stock, archive, icon/illustration, footage, texture, or overlay
    libraries for the asset class. Record the exact queries, candidate URLs or
    asset IDs, preview/metadata evidence, rights or license status, fit/reject
    rationale, and one result:
    `selected_source`, `inspiration_for_generation`, or
    `searched_no_reference`. A search-results page is not a candidate URL;
    retain the specific asset page and verify its rights basis. “Custom is
    faster” is not a search result.
  - [ ] Complete every Asset Discovery Receipt row before moving on. Each row
    must contain source class, `usage_role`, `rights_status`, exact query,
    specific candidate URL/ID or exact missing-input blocker, fit decision,
    result, owner, a concrete expected output file path, and acceptance check.
    Do not shorten the required table or move owner/output/acceptance into
    unrelated prose.
  - [ ] Use only the three allowed discovery results. Put unavailable-tool or
    missing-input state in the blocker/fit explanation; never invent `blocked`
    as a fourth Result value. Every expected output ends in a concrete file
    name and extension, never a directory.
  - [ ] Resolve every missing visual with the hybrid decision ladder:
    `reuse -> source -> inspired_generation -> original_generation`.
    `inspired_generation` requires a rights-safe reference set plus a
    transferable-trait map for composition, lighting, palette, texture,
    material, or camera relationship; it must also name protected expression,
    likeness, logos, signatures, or exact composition that the output must not
    copy. Present that map as the moodboard decision, record
    `moodboard_traits_accepted_at`, and compile the generation prompt only
    after the traits are accepted by the operator or controlling approved
    spec. `original_generation` is valid after `searched_no_reference` or when
    the brief explicitly requires generation, and still needs a concrete
    prompt, owner, output path, rights/likeness note, and acceptance check.
  - [ ] In an approved execution run, perform those searches now with the
    available image/web/library/Resource Bank tools. Do not return every row as
    `pending discovery` and call the handoff ready. Preserve at least the
    strongest fit, the strongest rejected alternative, and the reason for the
    selection or no-fit decision for each material asset need.
  - [ ] List footage, stills, frames, clips, avatars, voiceover, music, SFX,
    captions, overlays, fonts, logos, data, product shots, motion/edit
    references, and final render needs.
  - [ ] Mark each asset as `reuse`, `source`, `inspired_generation`,
    `original_generation`, `capture`, `compose`, or `unknown`.
  - [ ] Treat `compose` as arranging or treating accepted source media, not
    drawing new content assets. Ban custom-created SVG animation assets and
    SVG/JSX/programmatic vector substitutes for scene illustrations,
    characters, props, backgrounds, textures, or diagrams. Existing
    user-supplied, brand-owned, licensed, or discovered SVG files may be
    accepted as static source media with provenance and rights recorded.
  - [ ] Map each relevant Brand Kit or Tasty Pack element to an asset row,
    generation route, or missing-input blocker, prioritizing pinned elements
    before ordinary context elements.
  - [ ] For every selected element, carry its ID/provenance, description,
    whyItWorks, resolved golden example, golden recipe, planned use, and
    acceptance check into the asset decision and downstream generation packet.
  - [ ] Resolve `assetId + anchor` into media refs when possible; otherwise
    create regeneration packets for pinned visual/audio elements before the
    parent production plan can order downstream work. For editing patterns,
    resolve only explicitly required media dependencies and leave edit
    direction to Editing Advisor.
  - [ ] For narrative video, create continuity assets: character bible or
    no-character rationale, recurring prop/object bible, location/lighting
    anchors, and start/end frame assets for each model-native clip handoff.
  - [ ] For a layered documentary/editorial reel, load the
    [documentary reel production contract](../remotion/references/documentary-reel.md).
    Inventory background, dominant subject, foreground, and overlay media per
    scene. For particles, haze, dust, scratches, light artifacts, mattes, and
    shadows, own sourcing and preparation: provenance, rights, dimensions,
    alpha or black-background suitability, level/edge/loop cleanup, expected
    blend behavior, accepted file, and acceptance check.
- [ ] 3. Add recreation constraints.
  - [ ] Note rights, likeness, brand, source quality, duration, aspect ratio,
    visual continuity, audio continuity, and platform-specific constraints.
- [ ] 4. Choose owner routes.
  - [ ] Route still image creation or editing to `ai-image-advisor` or
    `imagegen` when the chosen result is `inspired_generation` or
    `original_generation`, or when the brief explicitly requires generation.
    Pass the complete inspiration or original-generation packet and request
    raster/project media outputs rather than custom SVG animation assets. Every
    packet must explicitly reject SVG, JSX, canvas, and programmatic-vector
    scene substitutes.
  - [ ] Route model-native clips to `ai-video-advisor`.
  - [ ] Route persistent presenter or character direction to `avatar-advisor`.
  - [ ] Route voice, music, SFX, Foley, and mix notes to `audio-advisor`.
  - [ ] Return accepted asset files and receipts to the parent production plan;
    the parent separately orders Editing Advisor and Remotion lanes.
- [ ] 5. Produce the handoff.
  - [ ] Include an asset table, file/source map, generation prompts or prompt
    briefs, acceptance checks, missing inputs, and next production owner.
  - [ ] For every generation packet, name the expected final raster/video path,
    keep `accepted_file_ref` empty until the output is inspected, and emit
    `downstream_asset_handoff: blocked_pending_accepted_file`. A prompt or successful provider job never
    counts as an accepted scene asset.
  - [ ] Apply the first-load Todo List guardrails again before calling the asset plan ready.
<!-- END FARPLANE_IMPORTANT_CHECKLIST -->

## Output Template

```text
## Asset Inventory
| Asset | Role | Source | Decision | Owner | Acceptance Check |
| --- | --- | --- | --- | --- | --- |

## Asset Discovery Receipt
| Asset Need | Source Class | Usage Role | Rights Status | Queries | Candidate Links / IDs | Fit Decision | Result | Owner | Expected Output | Acceptance Check |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |

Result is exactly `selected_source`, `inspiration_for_generation`, or
`searched_no_reference`.

## Moodboard Decision
| Packet | Inspiration Refs | Transferable Traits | Must Not Copy | Status | Accepted At | Approval Source |
| --- | --- | --- | --- | --- | --- | --- |

Status is `pending` or `accepted`. While pending, emit
`prompt_compilation: blocked_until_moodboard_accepted` and do not write the
generation prompt. A controlling approved spec may supply the acceptance
source and timestamp.

Do not render `Generation Packets` for a pending moodboard. Replace the whole
section with `generation_packets: blocked_until_moodboard_accepted`; render the
table below only after acceptance exists.

Even while prompt compilation is blocked, `Expected Output` is a concrete
future file path with a filename and extension, not a directory, `direction
packet`, `TBD`, or another planning label. Blocked state belongs in the fit or
blocker explanation; it is never a fourth discovery Result value.
Preserve supplied candidate URLs verbatim; if a URL/file was not supplied,
write the exact missing-input blocker instead of inventing one.

## Generation Packets
| Packet | Decision | Inspiration refs | Transferable traits | Moodboard Accepted At | Must not copy | Prompt / Direction | Owner | Expected Output | Accepted File | Downstream Asset Handoff | Acceptance Check |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |

## Inspiration Element Map
| Element | Anchor | Asset Decision | Output / Blocker |
| --- | --- | --- | --- |

## Regeneration Packets
| Packet | Source Element | Anchor | Owner | Prompt / Direction | Acceptance Check |
| --- | --- | --- | --- | --- | --- |

## Overlay Media Preparation
| Scene | Overlay | File / Blocker | Alpha / Background | Cleanup | Expected Blend | Acceptance |
| --- | --- | --- | --- | --- | --- | --- |

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
- Downstream asset handoff:

## Done / Proof
- ready_when:
- evidence:
- residual_risk:
```

## Gotchas

- Do not treat a viral reference as permission to clone exact visuals,
  likenesses, music, or protected assets. Name the risk and recreate the
  underlying pattern.
- Do not return a vague mood board to the parent production plan. Downstream
  lanes need accepted files, durations, scene roles, dimensions, and
  acceptance checks.
- Do not collapse the moodboard decision and generation prompt into one
  response when no acceptance source exists. Return the complete pending
  moodboard receipt and the blocked prompt-compilation state first.
- Do not return an inspiration-led asset plan where every visual is
  generic CSS/text/cards unless the run is explicitly labeled `technical_smoke`
  or `text_only_format` and the content claim is downgraded.
- Do not discard Tasty Pack anchors. If the pack says `frame_03_8.42s` or
  `contact_sheet`, the asset plan must either resolve that media or regenerate
  from it; a verbal paraphrase is not enough for production.
- Do not collapse avatar, audio, stills, and model-native clips into one generic
  prompt. Each asset class has different continuity and proof needs.
- Do not respond to missing assets by drawing custom SVG/JSX illustrations or
  procedural vector stand-ins. Search first when the brief allows it, then
  either use the selected source, convert the strongest references into a
  bounded inspiration packet for original generation, or route
  original-generation after an evidenced no-reference result. Inspiration
  transfers attributes, not a specific photograph's protected expression.

## Reference Map

- the first-load Todo List guardrails - read at start and finish for asset-plan QA.
- [references/source-roles.md](references/source-roles.md) - classify how a
  reference is used separately from its rights, then accept transferable
  moodboard traits before prompt compilation.
- `../storyboard/SKILL.md` - route narrative, script, and scene planning before
  asset decomposition when the creative plan is not ready.
- `../ai-image-advisor/SKILL.md` - route still generation, edits, upscales, and
  cutouts.
- `../ai-video-advisor/SKILL.md` - route model-native clip generation or edits.
- `../avatar-advisor/SKILL.md` - route persistent presenter, character,
  likeness, or lipsync direction.
- `../audio-advisor/SKILL.md` - route voice, music, Foley, SFX, and mix plans.
- `../remotion/references/documentary-reel.md` - load for layered
  documentary/editorial reel media preparation and the explicit boundary
  between overlay assets and deterministic compositing.
- `../content-impl-plan/SKILL.md` - parent orchestration that orders sibling
  Editing Advisor and Remotion lanes after accepted assets are returned.

## Output

- `asset_inventory`: decomposed asset table with source, decision, owner, and
  acceptance check.
- `asset_discovery_receipt`: searched source classes, exact queries, candidate
  links or IDs, independent usage-role and rights-status decisions, selected
  files, inspiration references, accepted moodboard traits, and evidenced
  `searched_no_reference` rows.
- `recreation_plan`: what to preserve, change, regenerate, source, or compose.
- `generation_routes`: concrete next-owner handoffs for each asset class.
- `blocked_report`: missing source material, rights uncertainty, missing
  storyboard, unsupported asset class, absent render route, or unmapped
  Inspiration Pack elements.
