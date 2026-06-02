# Composed Scroll Animation

Use `frontend-craft:composed-scroll-animation` when a frontend section needs a
layered generated-media scene with scroll or timed transitions.

## Algebra

```text
ComposedScrollAnimation := Brief + LayerManifest + Timeline + DebugHooks + Proof

Layer := id + asset + role + z + initial_state + final_state + responsive_rule + fallback

Timeline := driver + phases + transitions + reduced_motion

ExecutionPacket := section + layers + asset_routes + implementation_steps + qa
```

## Use When

- the scene needs 6-12 separate visual/UI layers
- generated images, cutouts, background removal, or isolated layers are part of
  the build
- readable text, controls, nav, labels, or proof chips must stay as HTML/UI
  overlays
- motion is scroll-linked or timed across named phases
- QA needs source-frame, checkpoint, or state comparison

Avoid when a normal image, video, GSAP timeline, or Three.js scene is the
clearer single carrier.

## Method Todos

- [ ] Read the source brief, section matrix row, selected frames/checkpoints,
  and confidence limits.
- [ ] Define `LayerManifest` with 6-12 layers, z-order, asset route,
  transform/opacity states, responsive constraints, and fallback.
- [ ] Route still generation through `imagegen` or `image-generation`; route
  cutouts/background removal/upscales through `image-generation` when needed.
- [ ] Keep readable text and controls in HTML/UI layers unless the brief
  explicitly requires baked pixels.
- [ ] Define `Timeline` with driver, named phases, scroll/time ranges,
  transition states, and reduced-motion still.
- [ ] Add debug hooks for phase, progress, active layers, frame/state, ready,
  and reduced motion.
- [ ] Verify with screenshots/checkpoints, source-frame comparison notes, and a
  gap report.

## Layer Manifest Shape

```json
{
  "layers": [
    {
      "id": "portal-background",
      "role": "background",
      "asset": "public/assets/portal-bg.webp",
      "z": 0,
      "initial": { "opacity": 1, "scale": 1 },
      "final": { "opacity": 1, "scale": 1.08 },
      "responsive": "cover center",
      "fallback": "reduced-motion still"
    }
  ]
}
```

## Timeline Shape

```text
driver := scroll | timed | hybrid

phase :=
  id + range + layer_states + html_overlay_states + qa_checkpoint
```

Prefer one driver. Use `hybrid` only when the brief needs both scroll and timed
artifact replay.

## Debug Contract

Expose a small inspectable state when the project allows it:

```text
window.__composedScrollDebug = {
  progress,
  phase,
  activeLayers,
  ready,
  reducedMotion
}
```

Use existing project patterns for debug exposure when a global is inappropriate.

## Proof

Required proof for a runnable build:

- layer manifest or equivalent implementation map
- generated/cutout asset provenance
- desktop and mobile screenshots for initial, transition, and final states
- source-frame or checkpoint comparison notes
- reduced-motion fallback proof
- visual QA or ticket QA artifact

For source-video-derived work, record misses honestly in a gap report instead
of claiming a perfect clone.
