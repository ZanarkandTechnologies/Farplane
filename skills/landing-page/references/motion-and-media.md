# Motion And Media

## Media Defaults

- Use real product, place, object, or person imagery when the user needs to inspect the subject.
- Use generated bitmap assets through `imagegen` when a bespoke visual world helps and no real asset exists.
- Keep project-bound final assets inside the workspace.
- For product, device, hardware, equipment, or object-focused pages, primary
  media must show realistic product shots or product renders, in-context use,
  and meaningful feature/parts detail. Generic infographics are support visuals
  only.
- For premium, cinematic, Terminal-style, or generated-media pages, the build
  must include filesystem-backed real or generated media evidence. Code-native
  canvas, WebGL, Three.js, and HTML/CSS visuals are support visuals, not proof
  that assets were generated.
- Do not author custom SVG illustrations, SVG diagrams, or SVG data overlays as
  landing-page graphics for premium pages. Use generated/real raster media, or
  build an actual WebGL/Three.js scene when a programmatic visual is warranted.
- Record final asset provenance in `assets/asset-manifest.json`: saved paths,
  prompt/source, poster, reduced-motion still, mobile variant, and QA notes.

## Motion Defaults

- CSS for simple state changes.
- Motion/Framer Motion for React component transitions when already used in the project.
- Official GSAP skills for complex timelines, ScrollTrigger, pinning, scrub, SplitText, Flip, or motion paths.
- Three.js/WebGL for 3D or shader scenes that genuinely carry the experience.

## Video Scrub

Use only when the page narrative earns it. Verify:

- metadata loads,
- hero scrub has enough runtime to feel authored rather than like a short loop,
- scroll checkpoints change the expected frame/state,
- named story beats activate across the scroll range,
- the pinned hero or product panel remains visible at every checkpoint,
- GSAP/WebGL/Three.js/HTML effect layers respond to the same progress when the
  page claims cinematic or Terminal-style motion,
- product pages change meaningful product states instead of only changing labels
  or overlay tint,
- mobile fallback exists,
- reduced-motion path works.

Do not treat media time or frame-source changes as sufficient proof. A broken
page can keep advancing scrub state after the pinned scene has scrolled out of
view. Screenshot the visual region and assert viewport intersection for the
pinned panel and primary visual carrier.

For generated video scrub, produce either:

- a frame sequence with manifest and enough frames for the planned beats, or
- a scrub-friendly video file plus poster and reduced-motion still.

For premium pages, do not call an `ffmpeg` MP4 assembled from Seedream or other
image-generator stills a `generated-video`. That is a `frame-sequence` asset and
must be judged by frame-count/beat quality. True generated video needs
video-generation provenance such as `videoModel`, `videoProvider`,
`sourceVideo`, or a recognized video app/model before local all-keyframe
transcoding.

For premium hero scrub, prefer 8-15+ seconds of generated or edited media, an
all-keyframe/video-seek-friendly encode, or a 96+ frame sequence. Record the
planned beat ranges in the landing spec, for example: context 0-18%, product
arrival 18-36%, parts reveal 36-62%, feature planes 62-82%, final lock 82-100%.

For product/equipment pages, prefer scroll/video sequences that reveal the
object: product in context -> isolated hero product -> exploded/assembly parts
-> feature callouts -> reassembled final state.

## Avoid

- Decorative blobs or generic gradient fields as the primary visual.
- Generic infographics as the primary product demo.
- Custom SVG illustrations or diagram overlays for premium landing-page
  graphics.
- Multiple competing extraordinary effects.
- Heavy canvas/WebGL without lazy load and off-screen pause.
