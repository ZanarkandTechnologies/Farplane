# Documentary Reel Production Contract

Load this reference for a voice-led documentary or editorial reel built from
layered stills, prepared overlay media, deterministic motion, and a shared film
treatment. Do not load it for ordinary talking-head edits, model-native
continuous footage, or a simple text-only format.

This contract preserves a production grammar, not a source's expression.
Scripts, imagery, people, voices, logos, music, branded compositions, and
source frames must be original, licensed, or explicitly approved for reuse.

```text
documentary_reel(locked_voice, storyboard, asset_manifest, cue_sheet)
  -> frame_addressed_scenes + shared_treatment + master_composition + proof
gates:
  original_expression; observed_voice_timing; causal_scene_units;
  asset_discovery_receipts_complete; no_custom_svg_animation_assets;
  background_subject_foreground_ready; overlay_media_prepared;
  deterministic_treatment; caption_hierarchy_preserved
```

## Planning and timing

- Lock the short voice-led causal spine before final scene construction.
  Usually five or six compact clauses are enough for a short reel, but clause
  count and scene duration follow the actual narration rather than a fixed
  five-second template.
- Give each scene one viewer-state change and one dominant spatial action.
  Derive zero-based, half-open frame ranges from observed voice timestamps.
- Address choreography with named frame events, not vague speed words:
  `subject_enters`, `foreground_reveals`, `weld_complete`,
  `subject_detaches`, `practical_flicker`, `scene_out`.
- Keep scenes independently previewable and assemble them against one master
  audio timeline. Reuse components and motion functions; do not force every
  scene into the same composition.

```text
documentary_scene:
  scene_id:
  voice_clause:
  frames: [start, end)
  viewer_state: before -> after
  background:
  dominant_subject:
  foreground_or_atmosphere:
  spatial_action:
    - event:
      frame:
      state_before:
      state_after:
  micro_motion:
  overlay_media:
  audio_cues:
  caption_safe_area:
```

## Ownership split

`asset-advisor` owns overlay media and preparation:

- identify the source, provenance, rights basis, scene role, dimensions, and
  expected blend behavior;
- search supplied/local media, Resource Bank/reference anchors, and suitable
  archive/stock/library sources; retain candidate links or asset IDs,
  rights/fit decisions, and the selected file or evidenced `searched_no_fit`;
- source particles, haze, dust, scratches, light artifacts, mattes, shadows,
  texture plates, backgrounds, subjects, and foregrounds as concrete files;
  after `searched_no_fit`, route raster/video generation to its owning advisor;
- inspect alpha or black-background suitability, unwanted gray levels, hard
  edges, loops, and resolution; prescribe crop, level cleanup, matte, feather,
  or regeneration work with an acceptance check;
- hand Remotion prepared media or an exact missing-file blocker.

Custom-created SVG animation assets, SVG/JSX illustrations, and procedural
vector stand-ins are forbidden for documentary-reel scene content. Existing
user-supplied, brand-owned, licensed, or discovered SVG files remain valid
static source media when provenance and rights are recorded.

`remotion` owns deterministic treatment and compositing:

- implement blend modes, masks, opacity, levels, feathering, crop, placement,
  looping, and frame-addressed entrances from the accepted overlay handoff;
- apply the shared grade, grain, vignette, gate-weave/drift, and restrained
  flicker through one reusable treatment wrapper or parameter set;
- keep treatment values deterministic, inspectable, and consistent across
  independently authored scenes;
- keep captions and proof-bearing details outside destructive treatment when
  the treatment would reduce legibility.
- animate accepted media; do not fill a missing layer by drawing a new SVG or
  JSX illustration.

Do not create a separate effects owner. Asset preparation returns to
`asset-advisor`; treatment or timeline problems stay with `remotion`.

## Motion and depth

- Maintain a readable three-plane composition: environment/background,
  dominant subject, and foreground prop or atmosphere. Typography does not
  substitute for a missing visual plane.
- Keep the frame alive with restrained, non-identical motion: slow background
  drift, subtle subject scale/position/rotation change, foreground parallax,
  and atmosphere moving on another rate or axis.
- Stagger repeated entrances and vary their timing or distance so the scene
  does not feel mechanically duplicated.
- Ground floating subjects with a projected or contact shadow whose position,
  scale, blur, and opacity follow the subject.
- Use stepped or held flicker only for a practical light or intentional
  emphasis. Avoid full-frame random flicker and high-amplitude motion that
  competes with narration or captions.

All motion must derive from `useCurrentFrame()` and composition fps. Seed any
noise or generate it deterministically; a render of the same props must not
change between runs.

## Shared treatment shape

```text
DocumentaryTreatment:
  grade:
    saturation:
    contrast:
    tint:
  grain:
    asset_or_seed:
    opacity:
    scale:
  vignette:
    strength:
  gate_motion:
    x_amplitude:
    y_amplitude:
    cadence_frames:
  practical_flicker:
    cue_frames:
    held_values:
  exclusions:
    captions:
    proof_details:
```

Use the smallest treatment that makes the scenes cohere. Grain, tint, vignette,
and movement are optional parameters, not a mandatory vintage preset.

For a black-background particle plate, start from a screen-like blend only when
the accepted asset handoff supports it. Correct residual gray, crop or mask
edges, and feather the composite deliberately; never use blend mode alone as
evidence that the overlay is clean.

## Assembly and proof

1. Preview each scene at its first frame, action midpoint, and final held frame.
2. Preview adjacent scene boundaries against the measured narration.
3. Assemble scene sequences, captions, accepted overlays, and audio cues on the
   master frame timeline.
4. Render representative opening, mechanism, treatment, choreography, and
   payoff stills before the final MP4.
5. Inspect caption hierarchy, unintended seams or gray boxes, frozen-looking
   subjects, repeated entrance timing, parallax direction, shadow grounding,
   flicker intensity, and audio synchronization.

The completion receipt names the composition, fps, duration, observed timing
master, scene ranges, accepted overlay files, treatment parameters,
representative stills, final render, and media/audio probes.
