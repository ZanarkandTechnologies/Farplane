# Example: What If Friction Vanished For One Minute?

```text
method: explainer
profile: retro-low-poly-consequence
generation_topology: deliberate_scene_breaks
model_route: bytedance/seedance-2-0 with original character/environment refs
  plus one approved scene-grid packet per clip and an optional explicitly
  approved runtime-only muted/caption-cropped motion clip
audio_policy: master voiceover and captions in post
final_duration_seconds: 47
narrative_beat_count: 7
visual_shot_count: 14
generation_duration_seconds: 5
edited_duration_seconds: 3-4
aspect_ratio: "9:16"
canonical_character_path: ./characters/late-90s-everyperson/identity-sheet.png
character_manifest_path: ./characters/late-90s-everyperson/manifest.md
canonical_character_sha256: 8ce13c3aff557aac962cfca88bf1b85a58ec80821731c5f580771469e1b94d8a
environment_bible_path: ./original-courtyard-bible.png
visual_storyboard_reference_path: ./visual-references/ps1-zero-friction-storyboard-board.png
annotated_motion_board_path: ./visual-references/ps1-zero-friction-motion-board.png
motion_board_notes_path: ./visual-references/ps1-zero-friction-motion-board.md
provider_safe_motion_reference_path: ./visual-references/ps1-zero-friction-motion-board-seedance-safe.png
scene_packet_root: ./storyboards/
scene_packet_contract: ../../scene-grid-production.md
reference_video_path: ./.farplane/runtime/style-motion-reference-muted-cropped.mp4
reference_scope: motion/editing/style only; replace identity, wardrobe,
  location, props, captions, story, and exact shot sequence
factual_basis:
  scope: idealized zero dry friction between solid surfaces
  claims:
    - static friction enables walking and gripping without relative slip
    - tire-road friction provides braking and lateral steering force
    - without tangential contact force, pushing along a surface cannot create traction
uncertainty_boundary:
  - ignores air drag, adhesion, fluid viscosity, deformation, and active propulsion
  - bodily and city-scale consequences are qualitative illustrations, not a quantitative forecast
```

The stitched 3x3 board at `visual_storyboard_reference_path` is the canonical
overview and look reference for this example. Before generation, group its
approved keyframes into one normally 4–5 second scene packet per Seedance call.
Each packet owns a clean grid, a matching annotated grid, and keyed notes under
`scene_packet_root`; those scene-local assets, not the whole-video board alone,
are the staging and motion authority. The clean grids contain no captions,
labels, IDs, or arrows that Seedance could mistake for scene content.

This is a nine-keyframe overview, not a replacement for the 14-row edit
topology below. A scene packet may cover one or two adjacent edit shots only
when they share one dominant mechanism and camera/POV. The shot table owns edit
identity and duration; the scene packet owns the provider call, explicit start
state, causal action, held end state, transition/audio obligations, and locked
input assets.

Use the clean storyboard board as the look authority and the annotated motion
board only as an instruction layer. The annotated board carries stable panel
IDs and arrows; its companion notes define each arrow. Seedance prompts must
name the active panel IDs and explicitly prohibit reproducing the grid,
gutters, IDs, arrows, or notes in generated footage.

If Seedance rejects the full board with a false-positive real-person privacy
classification, use `provider_safe_motion_reference_path` for the affected
panel transition. It preserves the PS1 world, wardrobe, state pair, IDs, and
arrows while replacing facial anatomy with an obviously fictional faceted
crash-test helmet. Keep the provider safety filter enabled on this fallback.
This asset is proof-only and is not the canonical everyperson. If it or any
other provider-safe variant would be visible in production, mark the affected
packet unapproved and show the revised identity card and scene grids for fresh
operator approval before generation.

## Consequence Ladder And Exact Shot Topology

| Beat | Shot | Seconds | Claim and literal visual |
| --- | --- | ---: | --- |
| 1 Hook | S01 | 0-3 | “No dry friction sounds like effortless speed.” The everyperson grins on an ordinary courtyard path. |
| 1 Hook | S02 | 3-6 | “Until you try to stand.” Their feet slide apart as they rise. |
| 2 Walking | S03 | 6-10 | Abrupt shoe insert: a faceted sole cannot develop tangential grip against the path. |
| 2 Walking | S04 | 10-13 | Wide reaction: each attempted step slides instead of propelling the body forward. |
| 3 Gripping | S05 | 13-16 | A hand tightens around a rail but slides along it because dry surface grip is absent. |
| 3 Gripping | S06 | 16-20 | Object insert: a phone slips between squeezing fingers and skates away after being nudged. |
| 4 Driving | S07 | 20-23 | Tire close-up: a turning wheel cannot transmit useful lateral or braking force to the road. |
| 4 Driving | S08 | 23-27 | Static intersection wide: already-moving cars fail to follow steering inputs or stop at the line. |
| 5 Workaround | S09 | 27-30 | The everyperson drops to hands and knees and tries to crawl. |
| 5 Workaround | S10 | 30-34 | Low side view: palms and knees slide because the same missing tangential contact force defeats crawling. |
| 6 Escalation | S11 | 34-37 | A person pushes a crate; after release it keeps sliding across the idealized surface while air drag is intentionally ignored. |
| 6 Escalation | S12 | 37-41 | Courtyard wide: doors cannot be pulled by their smooth handles and pedestrians cannot redirect themselves through contact. |
| 7 Payoff | S13 | 41-44 | Odd high angle: straight sliding paths cross through the intersection as the test subject reaches for help and cannot grip it. |
| 7 Payoff | S14 | 44-47 | Largest wide: the courtyard becomes a legible city-scale traffic-and-traction failure; narration ends, “So your smoothest minute would be—”. |

The 14 edited shot durations total exactly 47 seconds. Each Seedance generation
targets five seconds, leaving handles for selecting the strongest portion
without asking the model to sustain the whole narration beat.

## Filled Seedance Shot Prompt

```text
Vertical 9:16 retro-console low-poly 3D explanatory shot. Use the canonical
stitched storyboard board as the rendering and sequence authority, the matching
panel crop when supplied as the shot-staging authority, the original angular
everyperson image as the character bible, and the original mundane courtyard
image as the environment bible. Preserve the hero silhouette, teal and ochre
wardrobe palette, coarse texture atlas, faceted proportions, and hard afternoon
lighting, but create and animate a new scene.

BEAT CLAIM: without friction, pushing backward cannot create usable traction.
VISIBLE ACTION: the everyperson lies on the pavement and urgently tries to
crawl; palms and knees slide backward while the torso barely advances.
PHYSICAL MECHANISM: contact points visibly glide over the ground with no grip;
the failed motion is confined to solid-on-solid dry contact.
CAMERA: awkward low side angle, static framing, hands and knees large in the
foreground, face readable in the middle ground.
TEMPORAL DIRECTION: begin with the character planting both hands; over 5
seconds show one failed crawl cycle, then hold the helpless stretched pose for
the cut.

Intentionally dirty late-1990s first-generation 3D console cutscene: a
240p/320x240-like surface, nearest-neighbor texels, affine texture swimming,
subpixel vertex jitter, no antialiasing, jagged silhouettes, ordered dithering,
color banding, crushed shadows, coarse low-bit baked lightmaps, flat fog,
primitive polygon meshes, a gaunt asymmetrical face, vacant eyes, stiff block
hands, slightly incorrect anatomy, and deadpan physical comedy. No readable
text, captions, logos, watermark, source likeness, red jacket and blue jeans,
clean modern Blender or Unreal low-poly, PBR materials, smooth normals,
photoreal skin, family-animation styling, cinematic depth of field, floating
UI, camera orbit, 2D pixel art, a global grunge or pixelation overlay,
downsampled modern CGI, or unrelated background action. The geometry itself
must be structurally coarse and the texture distortion must vary per polygon.
```

## Measured Mechanism Repair Pattern

The first reference-conditioned hook can preserve style and continuity while
still failing mechanism legibility. When a contact action reads as a controlled
stance rather than a slip, change only the causal motion wording:

```text
Keep visible tile seams behind both feet as a fixed ruler. The left shoe slides
left and the right shoe slides right, each crossing at least two tile seams and
two shoe lengths while both soles stay pressed to the solid floor. The pelvis
drops low, the torso tips backward, and the low uncontrolled split holds for
the final two seconds. This is floor-relative translation, not feet skating in
place.
```

This pattern was promoted only after the repaired Seedance clip flipped the
independent mechanism assertion from fail to pass while style, continuity,
text, and source-copy guards remained passing.

## QA

- Hook reverses the fantasy within four seconds.
- Seven narration beats are split into 14 shots whose edited durations total
  exactly 47 seconds.
- Every beat shows at least one causal interaction before it escalates.
- Claims stay inside the stated idealized zero-dry-friction scope and name the
  ignored effects.
- Original character and environment references remain stable across clips.
- A reference-conditioned proof uses the source only for runtime
  motion/editing/style conditioning and passes an independent no-copy review.
- One provider call owns one physical mechanism. The measured multi-scene
  blocks rendered every requested setup but only 3/11 causal actions read
  without captions; short single-mechanism repairs plus sparse post-owned path
  markers produced the passing 14-shot visual assembly.
- Generated footage contains no text; caption phrases follow the master VO in
  post.
- Final output uses no source footage, logo, voice, exact character, wardrobe,
  or shot sequence.
