# Retro Low-Poly Consequence Prompts

## Cross-Stage Input Packet

Bind this packet once and carry the same keys through scripting, shot planning,
generation, and assembly:

```yaml
premise:
audience:
factual_basis:
uncertainty_boundary:
immediate_failures:
mechanisms:
failed_workaround:
final_consequence:
final_duration_seconds: 45-50
narrative_beat_count: 6-8
visual_shot_count: 12-16
generation_duration_seconds: 4-5
edited_duration_seconds: 2-4
aspect_ratio: "9:16"
canonical_character_path: ./characters/late-90s-everyperson/identity-sheet.png
character_manifest_path: ./characters/late-90s-everyperson/manifest.md
canonical_character_sha256: 8ce13c3aff557aac962cfca88bf1b85a58ec80821731c5f580771469e1b94d8a
approved_character_variant_path:
approved_character_variant_sha256:
environment_bible_path:
visual_storyboard_reference_path: canonical stitched text-free 3x3 scene board
scene_packet_root: one collocated clean grid, annotated grid, and notes file per clip
clean_scene_grid_path:
annotated_motion_board_path: matching scene grid with stable IDs and motion arrows
motion_board_notes_path: scene-local ID-to-motion instruction index
provider_safe_motion_reference_path: optional non-human panel-pair fallback after documented privacy false positive
shot_panel_reference_path: optional crop of the matching storyboard panel
reference_video_path: optional runtime-only muted/caption-cropped excerpt
reference_scope: motion/editing/style only
source_replacement_constraints: identity, wardrobe, location, props, story,
                                captions, exact shot sequence
```

## 1. Script And Beat Compiler

```text
Write a {final_duration_seconds}-second speculative explainer for {audience} about:
{premise}.

Use this causal structure:
1. In the first sentence, offer the premise as an exciting fantasy, then
   immediately reverse it into 2-3 intimate failures: {immediate_failures}.
2. Explain each failure through one concrete physical mechanism from
   {mechanisms}. Every sentence must earn a visible object interaction.
3. Let the recurring everyperson attempt {failed_workaround}; show why the same
   rule defeats it.
4. Escalate from body -> nearby environment -> planetary or cosmic consequence:
   {final_consequence}.
5. End on a short payoff or an intentional interrupted phrase that the final
   visual completes.

Target 145-160 words, about 190-200 words per minute. Use short causal
sentences, plain vocabulary, deadpan delivery, and no filler. Ground ordinary
claims in {factual_basis}; phrase unresolved impossible-premise claims within
{uncertainty_boundary}.

Return: exact narration, {narrative_beat_count} numbered narration beats,
seconds per beat, the literal visual proofs needed by each beat, and the
phrase-caption chunks for post-production. Beat durations must sum exactly to
{final_duration_seconds}.
```

## 2. Original Look-Bible Prompt

Create two creator-neutral reference images before video generation:

```text
Character sheet: an original late-1990s first-generation console everyperson
who can act as a comic scientific test subject. Primitive 100-500-polygon
body, gaunt triangular face, asymmetrical vacant eyes, stiff block fingers,
slightly incorrect anatomy, limited joints, and a dirty nearest-neighbor
texture atlas. Preserve a simple readable silhouette and stable wardrobe
colors across front/side/back views and three expressions. Show jagged edges,
affine texture warp, vertex jitter, dithering, and color banding. Do not
resemble any source creator or source character; avoid a red jacket with blue
jeans and avoid clean modern low-poly rendering. Low polygon count must be
structural: planar joints and coarse silhouettes remain visible before any
pixelation, noise, or downsampling.

Environment sheet: an original mundane liminal location rendered like a dirty
late-1990s first-generation 3D console cutscene: stained civic courtyard or
sparse urban street, primitive trees and buildings, coarse baked lightmaps,
crushed shadows, flat fog, dirty low-resolution texture atlases, muted teal,
ochre, concrete, and faded blue, wide view plus object-detail crops. Show
240p-like softness, jagged edges, affine texture swimming, vertex jitter,
dithering, and color banding. No logos, signs, readable text,
source-location reconstruction, PBR, smooth normals, global illumination, or
cinematic depth of field. Reject 2D pixel art, a global grime/pixelation filter,
and any downsampled modern PBR render; require per-polygon texture distortion.
```

Then create a text-free 3x3 stitched overview board from the approved shot
plan. Keep one character, courtyard, palette, dirty PS1 rendering surface, and
awkward static camera grammar across all panels. Use black gutters and no
labels. Next group the approved frames into one scene packet per normally 4–5
second provider clip. Save its clean grid, matching annotated grid, and keyed
notes together under `{scene_packet_root}`. The overview owns whole-video look;
the approved scene packet owns the individual Seedance call.

## 3. Shot Planner

Split the {narrative_beat_count} narration beats into {visual_shot_count}
visual shots. A beat may use one to three shots. For each shot, output:

```text
shot_id:
narrative_beat_id:
generation_duration_seconds: {generation_duration_seconds}
edited_duration_seconds: {edited_duration_seconds}
claim:
literal_mechanism:
character_action:
setting:
camera: one of static-wide | abrupt-close-up | over-shoulder | object-insert |
        odd-high-angle | upside-down-punctuation | sudden-cosmic-wide
start_state:
end_state:
continuity_anchors: character silhouette, wardrobe palette, texture style,
                    lighting direction, recurring prop
post_caption_phrase:
sfx_obligation:
canonical_character_path: {canonical_character_path}
canonical_character_sha256: {canonical_character_sha256}
approved_character_variant_path: {approved_character_variant_path}
approved_character_variant_sha256: {approved_character_variant_sha256}
environment_bible_path: {environment_bible_path}
visual_storyboard_reference_path: {visual_storyboard_reference_path}
shot_panel_reference_path: {shot_panel_reference_path}
clean_scene_grid_path: {clean_scene_grid_path}
annotated_motion_board_path: {annotated_motion_board_path}
motion_board_notes_path: {motion_board_notes_path}
aspect_ratio: {aspect_ratio}
```

Use a hard conceptual cut between shots unless a start/end state genuinely
needs first/last-frame interpolation. Do not force cross-shot camera continuity.
The `edited_duration_seconds` values must sum exactly to
`{final_duration_seconds}`.

## 4. Seedance 2.0 Per-Shot Prompt

```text
Vertical {aspect_ratio} retro-console low-poly 3D explanatory shot. Use
{canonical_character_path} only as the original character identity authority and
{environment_bible_path} only as the original environment/look bible. Preserve
the character silhouette, wardrobe
palette, coarse texture atlas, faceted proportions, and hard daylight, but
compose a new scene.

Use `{visual_storyboard_reference_path}` as the canonical rendering, palette,
character, environment, framing, and sequence reference. When
`{shot_panel_reference_path}` is present, use that crop as the staging
authority for this shot. Animate the causal action; do not merely pan across
or reproduce the still board.

Use `{annotated_motion_board_path}` only as a motion-instruction overlay. Read
the active `{panel_id}` and its arrow meaning from `{motion_board_notes_path}`.
Arrows indicate world-relative displacement, not camera motion. Never render
the contact-sheet grid, black gutters, panel IDs, arrows, labels, or notes in
the output video.

When `{reference_video_path}` is present, use `@Video1` only for awkward
retro-engine motion, editing cadence, camera punctuation, and rendering style.
Do not reproduce its person, face, wardrobe, location, props, captions, story,
or exact sequence. The original character and environment bibles remain the
identity and setting authority.

BEAT CLAIM: {claim}
VISIBLE ACTION: {character_action}
PHYSICAL MECHANISM: {literal_mechanism}
SETTING: {setting}
CAMERA: {camera}; immediate readable staging, one dominant action, no slow
cinematic orbit.
TEMPORAL DIRECTION: begin with {start_state}; over
{generation_duration_seconds} seconds the mechanism visibly causes the change;
end with {end_state} held clearly so the editor can retain
{edited_duration_seconds} seconds.

MECHANISM EVIDENCE: use {world_landmark} as an objective ruler. Make
{moving_contact} cross {minimum_visible_displacement} relative to that fixed
landmark; do not animate in place. Hold the causal end state for at least one
second.

Art direction: intentionally dirty late-1990s first-generation 3D console
cutscene. Render a 240p/320x240-like surface with nearest-neighbor texels,
affine texture swimming, subpixel vertex jitter, no antialiasing, jagged
silhouettes, ordered dithering, color banding, crushed shadows, coarse low-bit
baked lightmaps, and flat fog. Use primitive polygon humans with gaunt
triangular faces, asymmetrical vacant eyes, stiff block fingers, slightly
incorrect anatomy, sparse grimy civic concrete, and a muted dirty
teal/ochre/concrete-blue palette. Make the abstract rule physically legible.
No readable text, captions, logos, watermark, source character likeness, clean
modern Blender or Unreal low-poly, PBR materials, smooth normals, clean
topology, global illumination, photoreal skin, smooth Pixar styling, cinematic
depth of field, floating UI, random camera motion, or unrelated background
action. Do not simulate the period look with 2D pixel art, a global grunge or
pixelation overlay, or a downsampled modern PBR render. The geometry itself
must remain structurally coarse and texture distortion must vary by polygon.
```

## 5. Live Seedance Packet

The live app version `bytedance/seedance-2-0@0ht4cj4b` was schema- and
execution-checked on 2026-07-15. Verify the current version with `belt app get`
before spend. The measured run accepted original `reference_images`, one
runtime `reference_videos` entry, and an optional first-frame `image` together;
do not preserve a stale mutual-exclusion assumption when the live schema and a
small proof run disagree.

```json
{
  "prompt": "<filled per-shot prompt>",
  "duration": "<generation_duration_seconds integer>",
  "generate_audio": false,
  "ratio": "<aspect_ratio>",
  "reference_images": [
    "<visual_storyboard_reference_path>",
    "<annotated_motion_board_path>",
    "<optional_shot_panel_reference_path>",
    "<effective_character_path_from_approved_generation_envelope>",
    "<environment_bible_path>"
  ],
  "reference_videos": [
    "<optional_runtime_reference_video_path>"
  ],
  "resolution": "720p",
  "seed": 18427,
  "safety_filter": true,
  "safety_identifier": "<stable-hashed-user-id>",
  "watermark": false
}
```

Omit unavailable optional inputs entirely. Never send
`<optional_shot_panel_reference_path>` or
`<optional_runtime_reference_video_path>` as literal placeholder strings, and
do not retain an empty optional entry in either array.

If the provider rejects an original synthetic human-shaped board as
real-person privacy content, do not disable or repeatedly fight the upstream
privacy detector. Generate and review a narrow panel-pair fallback with an
obviously non-human faceted mannequin head, preserve the accepted PS1 world and
motion grammar, restore `safety_filter: true`, and pass only
`{provider_safe_motion_reference_path}` for that proof. This fallback is
motion/style proof only. It does not inherit approval as the recurring
character. If a production call would show it, invalidate the affected scene
approval, create a provider-safe variant under the canonical character
package, and show the revised character plus affected scene grids for explicit
human approval before spend.

Keep the approved clean scene grid first and its annotated scene grid second in
`reference_images` for each call; use the overview board only as an additional
look anchor when needed. Add only the matching panel crop when stronger staging
is needed. Keep the
same bibles, approved style-reference excerpt, and base seed family across
related shots; vary only when a shot repeatedly inherits an unwanted
composition. Seed alone is not an identity guarantee—the storyboard board,
visual bibles, and explicit continuity anchors are. Keep `generate_audio:
false`; source audio is never uploaded as part of this style-conditioning
route.

## 6. Assembly Workflow

1. Lock narration and beat timings before model spend.
2. Generate the original character and environment bibles.
3. Split the narration beats into normally 4–5 second scene packets and the
   planned edit-shot count; verify edited durations sum exactly to the final
   duration. Show the overview plus every clean/annotated grid and notes file
   beside the canonical character identity sheet for human approval, then lock
   their exact paths and hashes for reuse. Any identity-affecting fallback
   returns the revised character and affected grids to this review gate.
4. Produce one Seedance generation per approved scene packet with
   `generate_audio: false`. Before the batch, prove one representative
   reference-conditioned mechanism shot and allow one bounded repair.
5. Keep one physical mechanism in each normally 4–5 second provider call. Do not group
   several mechanisms behind internal hard cuts; the measured three-scene
   blocks made only 3/11 causal actions readable without captions.
6. Reject clips with identity drift, smooth modern CGI, illegible mechanisms,
   accidental text, or an unclear end-state hold.
7. Cut model clips to the narration, often using only the strongest 2-4 seconds
   from each generation.
8. Generate or record one master voiceover; add phrase captions in bold yellow
   with a heavy dark outline, lower-center safe-zone placement.
9. Add restrained mechanism SFX only when each cue binds to visible motion.
10. Reuse accepted clips and storyboard assets; regenerate only a named,
    versioned scene-local edit or blocker. Assemble and verify transitions,
    timing, imported transcript/captions, audio, light VFX, and final
   {aspect_ratio} render in Remotion. Seedance remains the owner of primary
   animation; no source footage is used in the output.
