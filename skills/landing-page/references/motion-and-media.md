# Motion And Media

## Media Defaults

- Use real product, place, object, or person imagery when the user needs to inspect the subject.
- Use generated bitmap assets through `imagegen` when a bespoke visual world helps and no real asset exists.
- Keep project-bound final assets inside the workspace.

## Motion Defaults

- CSS for simple state changes.
- Motion/Framer Motion for React component transitions when already used in the project.
- Official GSAP skills for complex timelines, ScrollTrigger, pinning, scrub, SplitText, Flip, or motion paths.
- Three.js/WebGL for 3D or shader scenes that genuinely carry the experience.

## Video Scrub

Use only when the page narrative earns it. Verify:

- metadata loads,
- scroll checkpoints change the expected frame/state,
- mobile fallback exists,
- reduced-motion path works.

For premium cinematic scroll pages, select an effect stack from
`effect-stacks.json`. The initial `cinematic-frame-sequence` stack covers
generated or rendered hero video, extracted frame sequences, GSAP scroll
pinning/scrub, HTML overlays, debug HUD, fallbacks, and proof checks.

## Avoid

- Decorative blobs or generic gradient fields as the primary visual.
- Multiple competing extraordinary effects.
- Heavy canvas/WebGL without lazy load and off-screen pause.
