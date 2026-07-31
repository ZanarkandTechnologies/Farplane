---
title: Scene Asset Bundles
status: active
owner: content-impl-plan
kind: reference
created_at: 2026-07-27
updated_at: 2026-07-27
---

# Scene Asset Bundles

Load this reference for every visual scene in editorial, explainer,
documentary, narrative, launch, and reference-led motion work. It turns visual
direction into concrete files and prevents cards, labels, and layout boxes from
being mistaken for gathered assets.

## Contract

```text
gather_scene_assets(scene, shared_world, beat, evidence)
  -> SceneAssetBundle
   + readiness_state
   + representative_frame_check
```

```text
SceneAssetBundle {
  scene_id
  beat_id
  shared_background: AssetLayer
  main_topic_asset: AssetLayer
  foreground_asset: AssetLayer
  layer_order
  reveal_order
  readiness_state:
    storyboard_draft_ready | asset_packet_ready | creative_lock_passed
  representative_frame_ref
}

AssetLayer {
  asset_id
  asset_family_id
  story_role
  job
  discovery_receipt_ref
  discovery_result:
    selected_source | inspiration_for_generation |
    searched_no_reference | explicit_generation_requirement
  source_ref_or_generation_packet
  owner
  rights_note
  expected_output_path
  accepted_file_ref
  acceptance_check
}
```

`asset_family_id` identifies perceptual source identity, not filenames.
Renames, recolors, flips, crops, small rotations, and minor retouches of one
source remain one family.

## Non-negotiable three-layer formula

Every production scene resolves:

1. `shared_background`: the continuous visual world. Reuse one background
   across scenes unless the story justifies a visible world change.
2. `main_topic_asset`: the dominant subject or proof object in the midground,
   such as a transparent person cutout, chart, map, document, product capture,
   or physical object.
3. `foreground_asset`: a separate closer structure, scenery, object, or
   attention/depth element, such as a podium, microphones, building edge,
   crane, shelf, hand, foliage, desk edge, waterline, architecture, or product
   prop.

The foreground must carry a concrete depth, context, attention, or transition
job. A caption or border does not become an asset because it is placed in
front.

A chart can be the main-topic asset, but it is never the whole scene. It still
needs the shared background and a genuine foreground asset with separate
visual provenance, rights, and acceptance. Chart data provenance remains
separate from chart-artwork and foreground-asset provenance.

For real people, prefer a licensed, public-domain, or operator-approved source
image. Make the main-topic output a transparent grayscale or halftone cutout
with restrained accent treatment for editorial public-decision-maker scenes
unless an approved Brand Kit or explicit visual direction requires another
treatment. Record the grayscale/contrast curve, halftone scale, alpha-edge
check, accent boundary, likeness ownership, and a rights-safe generic
substitute or explicit blocker. A generic silhouette is draft-only.

## Professional editorial selection

The three-layer count is necessary but not sufficient. Select the layers as one
coherent visual world:

```text
choose_scene_assets(narration_clause, claim, adjacent_scenes)
  -> quiet_world_background
   + literal_dominant_subject
   + physically_related_foreground
   + sparse_annotation
```

### 1. Keep the background quiet

The shared background is a stage, not a topic. Prefer a high-key neutral field,
subtle grid, restrained paper grain, map field, wall, sky, or other low-entropy
world that preserves negative space. Apply only enough texture to avoid a
sterile digital canvas.

Reject a background when its stains, collage seams, handwriting, tears,
scratches, splatters, diagrams, or props compete with the scene subject. Do not
combine parchment, distressed paper, ragged edges, ink splatter, binder clips,
and red scribbles as a default editorial style. That cluster reads as
scrapbook, conspiracy board, or pirate ephemera rather than a professional
explainer.

### 2. Pick the narration's concrete subject

Extract the concrete noun, person, place, proof object, or measured claim that
carries the clause. Make the highest-recognition rights-safe representation of
that subject the dominant asset:

- named person or actor -> recognizable licensed/generic cutout;
- physical object or place -> crisp isolated photo or scene crop;
- quantity or comparison -> chart, map, or literal object plus sparse number;
- workflow state -> real sanitized artifact fragment or concrete exchange;
- abstract mechanism -> the smallest physical reconstruction that shows the
  change, not a generic icon or decorative metaphor.

Score candidates on semantic centrality, recognition at thumbnail size,
silhouette, cropability, perspective compatibility, provenance, rights, and
whether they can occupy roughly half the frame without becoming muddy. Reject
an asset that merely matches the mood while another available asset more
directly names the clause.

### 3. Derive the foreground from the same world

The foreground should be physically or causally attached to the main topic:
ocean for a ship, architecture for political leaders, military hardware for a
spending comparison, a clean desk or receiving hand for a document handoff.
It may direct attention, establish scale, or provide depth, but it should still
belong in the scene if all typography disappears.

Do not reach for generic torn paper, newspaper piles, tape, clips, desk clutter,
foliage, or a random prop merely to fill the foreground slot. If the narration
is literally about damaged paper or archival ephemera, those materials may be
story assets; otherwise they are decoration and fail the slot.

The foreground should usually create a large, close depth mass: start with
roughly 20-45% of the lower visible frame or an equivalent edge-spanning form,
then calibrate against the reference and narration. This is not a universal
aesthetic law. Measure rendered nontransparent pixels, tight alpha bounding
box, frame-edge contact, and actual occlusion at final resolution. Transparent
canvas area, one-pixel borders, or a mostly empty wide PNG cannot satisfy the
gate.

### 4. Scope the surface treatment

Use grayscale, halftone, posterization, or a restrained accent to unify subject
assets. Keep alpha edges crisp. Background grain stays subtle and global;
strong texture belongs on selected subjects, not across every pixel. One
accent family may identify causal or editorial emphasis, but it must not become
an outline around every object.

At creative lock, retain a final-resolution background crop and dominant-subject
crop. The background crop must remain quiet and high-key; the subject crop must
show controlled halftone or dithering, deliberate grayscale/contrast, crisp
alpha, and any restrained registration offset. Global noise, sepia, stains,
tears, splatters, and full-frame distress cannot satisfy subject treatment.

Typography is an annotation layer, not a substitute for imagery. Prefer one
short statistic, claim, or label in the available negative space. If the text
and the image compete, enlarge the image and shorten the text.

## Genuine-asset rule

An accepted layer must point to a concrete existing file. A complete
generation/source packet may make the row `asset_packet_ready`, but it is not
an accepted layer and cannot pass creative lock. Every missing layer first
needs an Asset Advisor discovery receipt with candidate links or asset IDs,
rights/fit decisions, and either a selected source,
`inspiration_for_generation`, `searched_no_reference`, or an explicit brief
requirement for generation. The last three outcomes may route raster/video
generation; inspired generation must include transferable traits and explicit
must-not-copy constraints.

Custom-created SVG animation assets, SVG/JSX scene illustrations, and
programmatic vector stand-ins never satisfy the layer contract. Existing
user-supplied, brand-owned, licensed, or discovered SVG files remain eligible
as provenance-bearing static source media.

These do **not** count as accepted background, main-topic, or foreground
assets by themselves:

- CSS rectangles, rounded cards, frames, panels, or gradients;
- text blocks, captions, semantic labels, or callouts;
- chart containers or dashboard cards;
- generic document or laptop mockups;
- generic silhouettes or placeholder icons;
- a filename that has not been materialized and inspected.

They may remain annotations or low-fi layout aids. Renaming one `foreground`
does not satisfy the contract.

## Mandatory scene manifest

Emit this table for every production plan, even while assets remain blocked:

| Scene | Beat | Shared background | Main-topic asset | Foreground asset | Layer/reveal order | Source or generation packet | Owner | Rights note | Expected output | Accepted file | Acceptance check | Readiness |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |

One row per production scene is mandatory. A separate layer table may expand
details, but it cannot replace the scene-level triad view.

Add `main_topic_family_id`, `foreground_family_id`, `foreground_geometry_receipt`,
and `treatment_receipt` as adjacent columns or fields in the expanded manifest.

## Constrained variance

For production scenes, excluding title-only cards and the shared background:

- adjacent main-topic family overlap must be zero;
- adjacent foreground family overlap must be zero;
- start with >=80% unique main-topic families and >=85% unique foreground
  families across the production;
- random props do not earn novelty unless they have a narration-specific job.

A recurring motif may be excluded only when its changing state carries the
causal story. Declare the family, appearances, story function, and visible
transformation at every appearance. The motif may remain dominant when the
story requires it, but at least two other dimensions—foreground, composition,
scale, camera relationship, or reveal behavior—must change. A shared background
does not count as reuse, and “brand consistency” cannot turn unrelated repeated
assets into a motif.

## Readiness state machine

```text
storyboard_draft_ready
  -> asset_packet_ready
  -> creative_lock_passed
  -> Remotion production handoff
```

- `storyboard_draft_ready`: the story, visual roles, and intended packets are
  named. Planned prompts and placeholder paths are not accepted assets.
- `asset_packet_ready`: all three layer packets are complete, with owners,
  Asset Advisor discovery receipts, rights notes, expected outputs, and
  acceptance checks. A generation packet is complete only when discovery
  records `inspiration_for_generation`, `searched_no_reference`, or the brief
  explicitly requires generation.
  Outputs may still be missing or unaccepted, so this state never unlocks
  Remotion.
- `creative_lock_passed`: all three accepted files exist, their dimensions and
  transparency/readability are verified, and a representative assembled frame
  proves one background world, one dominant topic, and one foreground depth or
  attention layer. Final-resolution visible-pixel geometry and separate
  subject/background treatment receipts also pass.

Do not advance a whole production when one scene is behind. Record readiness
per row, and use the lowest scene state as the production state.

## Layering and motion

Default order is background → main topic → foreground. Reveal the world first,
then the subject, then the closer contextual/depth element when that order
supports comprehension. Use restrained parallax or staggered entrance so the
layers read as one composition rather than three boxes.

The representative frame fails when:

- the composition reads as a dashboard or grid of cards;
- multiple equal-weight rectangles compete for attention;
- the foreground is only a label, border, or container;
- the main topic is too small to dominate;
- the background changes arbitrarily between adjacent scenes;
- the background has more visual entropy than the topic;
- the foreground is a generic decorative prop with no physical or causal
  relationship to the topic;
- parchment, torn edges, stains, splatters, clips, handwriting, or scrapbook
  seams appear without a story-specific reason;
- texture is applied uniformly enough to make the whole frame look dirty;
- the main topic is a mood match rather than the narration's most concrete
  available subject;
- typography dominates while the scene's literal subject remains small;
- a layer lacks traceable source/generation evidence.

## Compile before blocking

Never respond to missing visuals with only “gather assets.” Emit the provisional
story, every scene row, concrete source or generation packets, owners, paths,
rights notes, checks, ordered actions, and exact blockers. Then stop at the
correct readiness state.

For requests to skip directly to Remotion, classify supplied assets into their
actual slot and compile packets for every missing slot. A supplied chart or PNG
is normally the `main_topic_asset`, not permission to omit the other layers.
Infer the smallest safe concrete packets when the brief permits it instead of
leaving them as category labels:

```text
shared_background_packet:
  owner: asset-advisor -> ai-image-advisor after inspired_generation or original_generation
  discovery_receipt: queries + candidate links/IDs + rights/fit decisions
  source_or_generation: selected source or complete raster generation prompt
  rights_note: required license/receipt
  expected_output: concrete path
  acceptance: continuity, contrast, dimensions

foreground_packet:
  owner: asset-advisor -> ai-image-advisor after inspired_generation or original_generation
  discovery_receipt: queries + candidate links/IDs + rights/fit decisions
  source_or_generation: selected source or complete raster generation prompt
  rights_note: required license/receipt
  expected_output: concrete transparent path
  acceptance: clean alpha, story role, occlusion, depth
```

When the supplied main topic is usable and both missing packets above are
complete, set the row to `asset_packet_ready` even though their output files are
not yet accepted. Use `storyboard_draft_ready` only while a required packet
field itself remains unresolved.

The response must show actual packet values, not the schema. For a neutral
editorial chart scene, a safe inferred example is:

```text
shared_background_packet:
  owner: asset-advisor -> ai-image-advisor
  discovery_result: searched_no_reference
  source_or_generation: "16:9 continuous editorial paper/map plate,
    low-contrast grayscale, no text, no panels or frames"
  rights_note: generated output receipt; no protected marks
  expected_output: assets/shared/editorial-world-bg.png
  acceptance: 1920x1080; supports chart contrast; matches adjacent scenes

foreground_packet:
  owner: asset-advisor -> ai-image-advisor
  discovery_result: searched_no_reference
  source_or_generation: "rights-safe transparent contextual object tied to
    the chart claim; clean isolated cutout; no card, label, or container"
  rights_note: licensed/public-domain source or generated-output receipt
  expected_output: assets/scenes/<scene>/foreground-context.png
  acceptance: clean alpha; concrete depth/attention job; does not obscure data

readiness_state: asset_packet_ready
```

Adapt the contextual object to the claim. If the claim is too vague to choose
an honest object, use a concrete neutral evidence-context prop and mark that
choice for storyboard review; do not omit the packet.
