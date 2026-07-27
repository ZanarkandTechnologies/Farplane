---
title: Scene-Grid Production Contract
status: active
owner: video-production
kind: reference
created_at: 2026-07-16
updated_at: 2026-07-16
applies_to:
  - model-native-video
  - deliberate-scene-breaks
  - storyboard-review
  - remotion-assembly
---

# Scene-Grid Production Contract

Load this reference when a multi-scene video uses model-native clips and the
chosen generation topology is `deliberate_scene_breaks`. It defines the shared
artifact passed from `content-impl-plan` to `storyboard`, `ai-video-advisor`, and
`remotion`.

```text
scene_grid_plan(video, topology = deliberate_scene_breaks)
  -> scene_packet[] + approval_packet

approved(scene_packet[], budget)
  -> generate_one_clip_per_packet -> remotion_master
```

## Scene Boundary

A scene packet is one generation unit with one dominant action, one camera
setup or POV, and one intended cut at its boundary. Target 4–5 seconds by
default because short clips reduce continuity burden and make failures local.
Override that range only when the selected provider, narration beat, action, or
approved pacing requires it; record the reason in the packet.

Do not force cross-scene pose, camera, or background continuity when a deliberate
cut makes the change legible. Preserve only the continuity anchors the story
needs, such as the recurring character, wardrobe, prop, palette, or causal
state. Use `continuous_chain` with explicit first/end frames when an action must
cross the clip boundary without a cut. Use `montage` when causal continuity is
intentionally absent.

## Scene Packet

Each planned provider call gets one packet and one collocated folder:

```text
storyboards/
  SC01/
    clean-grid.png
    annotated-grid.png
    notes.md
    inputs/
    approved.json
```

```yaml
scene_id: SC01
target_clip_seconds: 4-5
duration_override_reason:
dominant_action:
camera_or_pov:
clean_grid: storyboards/SC01/clean-grid.png
annotated_grid: storyboards/SC01/annotated-grid.png
panel_ids: [P01, P02, P03]
notes:
  start_state:
  action:
  fixed_landmark:
  minimum_displacement:
  end_state:
  camera:
  end_hold_seconds:
motion_bindings:
  - id:
    points_to:
    panel_id:
    instruction:
    overlay_type: subject_point | landmark_point | motion_arrow | endpoint
continuity_anchors: []
canonical_character_path:
canonical_character_sha256:
approved_character_variant_path:
approved_character_variant_sha256:
transition_in:
transition_out:
audio_obligations:
  voiceover_range:
  caption_range:
  sfx_cues: []
conditioning_strategy: storyboard_only | endpoint_pinned | video_conditioned
provider_inputs:
  reference_images: []
  first_frame:
  last_frame:
  reference_video:
approved_assets: []
reuse_policy: reuse_locked
approval:
  approval_id:
  operator_approved: false
  approved_at:
  approval_scope: storyboard_and_identity
  invalidated_at:
  invalidation_reason:
  supersedes_approval_id:
```

The clean grid is the appearance and staging authority. It must contain no
arrows, IDs, notes, captions, or gutters that the model could reproduce as
scene content. The annotated grid uses the same images with stable panel IDs,
motion arrows, landmarks, and endpoint marks. `notes.md` defines every mark in
plain language and ties it to the panel ID. The provider prompt names the
active IDs and forbids rendering the annotation layer.

Treat that prohibition as a clip-review gate, not merely prompt wording.
Colored arrows, point IDs, panel IDs, rulers, or note text that survive into
the provider output are annotation leakage. Prefer the clean grid as the
pixel-bearing input and repeat the keyed bindings in the prompt; use the
annotated grid only as a control reference when the provider needs it. A clip
with visible control marks must be repaired, deliberately accepted as part of
the final visual language, or excluded from the final edit.

Annotations are an executable spatial contract, not decoration. Every moving
subject or moving body part gets a short point ID placed on that object. Every
landmark used to prove displacement gets its own fixed ID placed on the
landmark. Each motion arrow begins at the moving point or its current position
and terminates in the intended direction; every required final state gets a
visible endpoint such as `E1`. The keyed notes map each ID to exactly one
literal provider instruction, and the provider prompt repeats those bindings.
An arrow drawn only between panels, a legend with no in-frame point, or prose
that does not name the visible IDs fails the packet.

Minimum keyed example:

```text
L1 = character torso center; keep on one diagonal path
H1 = grabbing hand; close briefly at fixed rail point R1
P1 = arrow from L1 through the rail without redirection
E1 = mandatory endpoint one body width past the rail; hold one second
```

Choose the smallest conditioning route that can express the scene:

- `storyboard_only`: clean grid + annotated grid + keyed notes. Default for one
  readable action and ordinary camera movement.
- `endpoint_pinned`: add explicit first and last frames when the start or end
  state must be exact.
- `video_conditioned`: add an authorized, rights-safe reference clip only when
  articulated motion, camera choreography, or rhythm remains hard to describe.

## Human Review And Approval

The minimum pre-generation review packet contains:

1. One overview strip showing the scene order and hook-to-payoff arc.
2. Every scene's clean grid and annotated grid.
3. Keyed notes with the action, start/end state, camera/POV, and transition and
   audio obligations.
4. The recurring-character card or an explicit no-character rationale.
5. The provider strategy and any runtime video reference that would be uploaded.

The human-facing overview must make the keyed overlays readable at review size.
Showing only clean grids or first-frame thumbnails does not satisfy review when
the annotated boards are the motion contract.

Approval of this packet authorizes generation and Remotion assembly within the
already accepted ticket scope and spend budget. It does not authorize publishing,
extra spend, a new identity/likeness use, or a different runtime reference.

Review is visual, not implied by prose. Show the recurring-character identity
sheet beside the overview and scene grids, and ask for feedback at this point.
Record `canonical_character_path` and `canonical_character_sha256` in every
character-bearing scene packet.
`operator_approved: true` applies only to those exact inputs.

If a provider safety, privacy, moderation, upload, or format blocker requires a
new reference image, character variant, wardrobe, face treatment, silhouette,
or conditioning route, invalidate approval for every affected packet. Create a
versioned replacement, show the revised character card and affected grids, and
obtain fresh approval before production spend. A smoke-test fallback cannot
silently become the recurring production identity.

## Asset Reuse Lock

After approval, reuse the exact clean grids, annotated grids, panel crops,
character/environment references, and prompt notes in provider calls. Do not
silently regenerate or replace them because a new image seems prettier.

Regeneration is allowed only when the operator explicitly requests it, an
approved edit changes that scene, or a named provider/input blocker makes the
asset unusable. Preserve the prior asset, create a versioned sibling, record the
reason, and return only the changed scene packet for review. Unchanged scenes
remain locked.

Before each provider call, compare the actual input paths and hashes with the
approved packet. Reject the call when the canonical character reference is
missing, its hash changed, or a fallback is present without a fresh approval
record. Prompt strength and seed reuse are not substitutes for an identity
reference.

## Approval And Generation Envelope

`approved.json` is the checkable approval record, not a loose boolean. It uses
the same identity field names as the scene packet:

```json
{
  "scene_id": "SC01",
  "approval": {
    "approval_id": "SC01-v2",
    "operator_approved": true,
    "approved_at": "2026-07-17",
    "invalidated_at": null,
    "invalidation_reason": null,
    "supersedes_approval_id": "SC01-v1"
  },
  "canonical_character_path": "characters/late-90s-everyperson/identity-sheet.png",
  "canonical_character_sha256": "<sha256>",
  "approved_character_variant_path": "characters/late-90s-everyperson/provider-safe-v2.png",
  "approved_character_variant_sha256": "<sha256>",
  "approved_asset_sha256": {
    "clean-grid.png": "<sha256>",
    "annotated-grid.png": "<sha256>"
  }
}
```

Build a local generation envelope before reducing it to the provider API
schema:

```yaml
scene_id: SC01
approval_id: SC01-v2
canonical_character_path: characters/late-90s-everyperson/identity-sheet.png
canonical_character_sha256: <sha256>
effective_character_path: characters/late-90s-everyperson/provider-safe-v2.png
effective_character_sha256: <sha256>
approved_asset_sha256: {clean_grid: <sha256>, annotated_grid: <sha256>}
provider_input:
  reference_images:
    - <clean_grid_path>
    - <annotated_grid_path>
    - <effective_character_path>
preflight_receipt:
  operator_approved: true
  approval_not_invalidated: true
  canonical_character_hash_matches: true
  effective_character_hash_matches: true
  approved_grid_hashes_match: true
  effective_character_present_in_reference_images: true
  pass: true
```

Only `provider_input` is sent to Seedance. The local envelope retains approval
and hashes that the provider schema does not accept. Do not submit unless every
preflight receipt field passes.

## Remotion Assembly Contract

`ai-video-advisor` or the selected provider route generates one clip per scene
packet. `audio-advisor` may accept operator-approved or generate voice, music, or SFX assets;
Remotion places them. Remotion then:

- probes each clip's actual duration, fps, dimensions, and frame count;
- sequences observed frames instead of assuming every clip is exactly 4–5 seconds;
- applies the named hard cut, match cut, fade, slide, wipe, overlay, light VFX,
  or other deliberate transition without decorating every cut by default;
- aligns voiceover, imported transcript/captions, SFX, Foley, and music on one
  master timeline with ducking and silence obligations;
- trims weak handles and holds without inventing primary character motion; and
- produces local still/MP4 proof plus visual and audio QA evidence.

The storyboard owns why the scene changes. Remotion owns how the accepted clips
and audio assets are timed across that change. A failed primary action returns
to the affected scene packet; it is not hidden with transition effects.

## Recurring Character Placement

Style-specific characters live with their style profile:

```text
references/explainer-styles/<profile-id>/characters/<character-id>/
```

Cross-style characters live under:

```text
references/characters/<character-id>/
```

Each character package should contain a manifest, identity sheet, expression
and pose sheets, immutable anchors, allowed variation, negative constraints,
provenance/rights notes, and provider-safe variants when needed. Scene packets
reference those files; they do not copy or mutate the canonical character
package.

## Positive And Negative Example

Positive: a 24-second explainer becomes six independently reviewable 4-second
scene packets. A new POV at each cut is intentional. Six accepted clips are
stitched with two hard cuts, one match cut, captions, VO, and generated SFX.

Negative: one 24-second contact sheet is attached to six calls with no active
panel IDs, the model invents different shot order each time, approved character
art is regenerated between calls, and Remotion is expected to conceal failed
actions with wipes. This fails the packet, reuse, and ownership contracts.
