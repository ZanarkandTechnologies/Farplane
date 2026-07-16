---
profile_id: retro-low-poly-consequence
schema: farplane-video-style-profile
version: "0.3.0"
compatible_methods: [explainer, storyboard]
---

# Retro Low-Poly Consequence

## Intent

Turn an impossible or counterintuitive premise into a fast, uncanny, funny
chain of physical consequences. One original low-poly everyperson acts as the
viewer surrogate and scientific guinea pig while each abstract mechanism
becomes a literal object interaction.

## Observed Source Grammar

- A vertical 45-50 second short opens by reversing an appealing fantasy into
  intimate bodily danger within roughly three seconds.
- Narration moves at about 190-200 words per minute and advances through short
  causal sentences.
- Nearly every two to four seconds earns a new visual proof, gag, close-up,
  object insert, or scale change.
- The recurring character survives across mundane suburban scenes,
  diagram-like mechanism shots, uncomfortable facial close-ups, and a
  cosmic-scale payoff.
- The visual surface resembles a dirty late-1990s first-generation 3D console
  cutscene, not polished contemporary low-poly art: native-240p softness,
  jagged silhouettes, affine texture swimming, vertex jitter, ordered
  dithering, color banding, crushed shadows, coarse baked lightmaps, sparse
  environments, and visibly wrong human proportions.
- Lower-center captions show only the active phrase in bold high-contrast
  lettering synchronized to the narration.

## Inferred Production Translation

- Reproduce the visible low-resolution surface with a coarse hand-painted or
  baked texture atlas rather than copying source textures.
- Treat PS1-era rendering failure as a positive style requirement. Low polygon
  count alone is insufficient: clean topology, smooth normals, PBR materials,
  global illumination, and cinematic depth of field still read as modern CGI.
- Build a text-free overview board, then split it into one clean and one
  annotated scene grid per provider clip using the shared
  `../../scene-grid-production.md` contract. The overview locks the whole arc;
  each scene packet is the actual review and Seedance input unit.
- Generate silent, text-free visual shots. Add one master voiceover, phrase
  captions, and restrained SFX in post so timing and wording remain coherent.
- Treat the narration beat as a story unit and the visual shot as an editing
  unit. A narration beat can require multiple visual proofs.
- When the operator explicitly approves source-conditioned generation, use a
  short muted, caption-cropped excerpt only as runtime motion/editing/style
  conditioning. Pair it with original character/environment bibles and require
  the prompt to replace source identity, wardrobe, location, props, story, and
  exact shot sequence. Keep the excerpt outside the skill package and final edit.

## Reusable Grammar

1. **Hook:** state the impossible premise, then name two or three immediate
   sensory, bodily, or social failures.
2. **Consequence ladder:** for each beat, show rule -> visible mechanism ->
   impact on the everyperson -> question that opens the next beat.
3. **Character continuity:** use one original, simple, emotionally readable
   test-subject silhouette and stable wardrobe palette across every shot. The
   canonical package is
   [Late-90s Everyperson](characters/late-90s-everyperson/manifest.md); bind its
   identity-sheet path and hash into every character-bearing scene packet.
4. **Literal mechanism:** turn invisible rules into moving particles, rays,
   waves, collisions, forces, deformations, or scale changes.
5. **Visual punctuation:** prefer hard conceptual cuts, intrusive close-ups,
   awkward angles, upside-down framing, and sudden wide/cosmic reveals over
   elegant continuous coverage.
6. **Escalation:** begin in an ordinary place, make the problem bodily, then
   expand to environmental and finally catastrophic scale.
7. **Post-owned clarity:** model clips contain no written text. One master
   voiceover, phrase captions, restrained SFX, and final timing are assembled
   after generation.

## Production Topology

Use `deliberate_scene_breaks`, not one continuous model-native clip. Write a
145-160 word voiceover, divide it into six to eight causal narration beats,
then plan roughly 10-12 scene packets and 12-16 edit shots around a locked
original character and environment look bible. Generate each model clip at
normally 4-5 seconds, edit its strongest portion into the timeline, and require all edited shot durations
to sum exactly to the final 45-50 second runtime. A narration beat may contain
one to three visual shots. Voiceover and captions own the final timing.

Seedance owns primary character and mechanism animation. Remotion owns the
edit, exact timing, captions, audio, and light corrective VFX; it must not
silently replace missing model-native animation. Before producing the full
shot batch, prove the topology on one 4–15 second reference-conditioned case.
Freeze one dominant mechanism failure, repair only that failure once, and
promote only after independent visual and rights review.

Generate one physical mechanism per normally 4–5 second Seedance clip. A measured
three-mechanism block produced all requested scenes but made only 3/11 causal
actions readable; single-mechanism repairs recovered the usable shoe, step,
crate, and rail actions. Do not trade clip count for multi-scene prompt density
when the viewer must infer world-relative cause without captions.

For contact mechanisms, prompt against stable scene landmarks. Name the
visible floor seam, rail post, stop line, or other ruler that the moving object
must cross; distinguish world-relative translation from animation in place;
and require a readable final pose held for at least one second.

Load [audio.md](audio.md) for the evidence-backed voice, music, SFX, silence,
mix, caption, and provider handoff. The audio profile is a production grammar,
not permission to clone the source voice or reuse source audio.

## PS1 Surface Lock

The canonical look is an uncanny late-1990s urban-console cutscene. Use:

- a 240p/320x240-like image surface with nearest-neighbor texels, no
  antialiasing, jagged polygon edges, color banding, and visible dithering;
- affine texture warping, texture swimming, subpixel vertex jitter, coarse
  dirty texture atlases, low-bit baked lightmaps, flat fog, and crushed darks;
- structurally coarse silhouettes and planar joints whose low polygon count is
  visible before any pixelation, noise, or downsampling is applied;
- primitive roughly 100-500-polygon humans with gaunt triangular faces,
  asymmetrical vacant eyes, stiff block fingers, dead stares, and slightly
  incorrect anatomy;
- grimy civic concrete, stained walls, sparse street furniture, muted dirty
  teal/ochre/concrete-blue colors, and awkward static gameplay cameras.

The stitched overview board is the authority for whole-video look and scene
language. Each approved clean/annotated scene grid is the staging and motion
authority for one provider clip. Character and environment bibles remain useful
continuity aids, but they must not pull the render toward clean modern Blender
or Unreal low-poly.

Provider-safe motion references do not supersede the canonical character. If a
privacy or safety fallback changes visible face, silhouette, wardrobe, or
species, it invalidates approval for affected scenes and returns the revised
character card and grids to operator review before production generation.

## Negative Constraints

- No creator names in generation prompts; no source logo, exact character
  likeness, exact wardrobe, source voice, catchphrase, branded asset, or
  shot-for-shot reconstruction. A source excerpt may enter the provider only
  under the explicit runtime-conditioning boundary above; it never enters the
  profile package or final edit.
- No glossy modern CGI, clean Blender/Unreal low-poly, PBR materials, smooth
  normals, clean topology, soft global illumination, photoreal faces, smooth
  Pixar-like character design, cinematic depth of field, beauty shots without
  causal work, or generic floating infographic UI.
- No 2D pixel art, global grunge/pixelation overlay, or downsampled modern PBR
  render masquerading as period 3D. Geometry and per-polygon texture
  distortion must create the look before post-processing.
- No generated captions, labels, logos, or readable text inside Seedance
  footage; add typography in post.
- No unrelated montage beat. Every shot must demonstrate or escalate one
  script claim.
- No unsupported certainty about impossible-premise physics; preserve explicit
  speculative language where evidence cannot settle the claim.

## Provenance

Compiled from Resource Bank capture `k975s09kwevmjdv266hby2gsnh8akkj4`,
derived from the operator-supplied Instagram reel
`https://www.instagram.com/p/DYlELbnxFMH/`. Source attribution identifies Low
Poly Shorts (`lowpolyshorts`). The profile stores creator-neutral observations
and inference only; raw video, audio, source frames, logo, character identity,
and source assets are not copied into this package.

## QA Assertions

- The first three seconds pair the premise with a visceral reversal.
- Every spoken causal claim has one legible physical demonstration.
- Six to eight narration beats are rendered through roughly 12-16 visual
  shots; the shot durations sum exactly to the target runtime.
- The same original character silhouette, palette, and proportions persist
  across generated clips.
- Average visual-beat duration is two to four seconds after editing.
- Camera oddity or scale change supports a specific reveal rather than random
  motion.
- Voiceover, captions, and SFX are assembled against one master cue sheet.
- The final beat is the largest consequence and resolves or intentionally
  interrupts the opening question.
- Output remains creator-neutral and uses no copied source media or identity.
- A source-conditioned proof, when authorized, replaces identity/content and
  passes independent visual and rights review before its prompt clauses enter
  the reusable profile.
- Primary animated visuals come from Seedance; Remotion is limited to assembly,
  captions, audio, and light VFX.
