---
name: remotion
description: "Turn storyboarded assets into Remotion/React compositions, stitched timelines, captions, audio placement, and local render proof."
tier: 3
group: content-video
source: local
template_uses:
  skill-template: "0.3.7"
common_chains:
  after: ["review", "qa"]
metadata:
  tags: remotion, video, react, animation, composition
eval: evals/evals.json
---

# Remotion

<!-- BEGIN FARPLANE_IMPORTANT_CHECKLIST -->
## Todo List

# Remotion Todos

Use this as the ordered checklist whenever `remotion` is active.

- [ ] Classify the Remotion job: composition authoring, final asset stitching, timing, sequencing, captions, audio placement, motion graphics, data visualization, UI animation, HTML-in-canvas, local render proof, or render-readiness check.
- [ ] State the composition name, dimensions, fps, duration, assets, props, output intent, and handoff path before authoring code.
- [ ] Use [research:official-docs](../research/SKILL.md#researchofficial-docs) or [research:code-patterns](../research/SKILL.md#researchcode-patterns) when Remotion API behavior, official docs, local code patterns, or source assets shape the implementation.
- [ ] Use the native planning phase when choosing authoring route, animation structure, asset route, render route, or scope cut.
- [ ] Before designing visual scenes, layouts, promos, motion graphics, or text-heavy videos, load [video-layout](rules/video-layout.md).
- [ ] Load the relevant Remotion rule file from `rules/` before implementing specialized behavior such as captions, audio, sequencing, timing, transitions, images, videos, visual effects, fonts, HTML-in-canvas, measurement, maps, or 3D.
- [ ] Use frame math with `useCurrentFrame()`, `interpolate()`, `Sequence`, and Remotion APIs; prefer `interpolate()` over `spring()` unless physics-based motion is explicitly needed; do not use CSS transitions, CSS animations, or Tailwind animation utilities for frame-accurate motion.
- [ ] For animations that should be editable in Remotion Studio, keep `interpolate()` inline in the `style` prop and use individual transform properties such as `scale`, `translate`, and `rotate` rather than building a `transform` string.
- [ ] If the user asks for Remocn or the task benefits from copy-paste motion primitives, transitions, backgrounds, UI scenes, or demo-video blocks, load [remocn](references/remocn.md) before adding registry components.
- [ ] Route parent production planning through [content-impl-plan](../content-impl-plan/SKILL.md) when the storyboard, assets, advisor actions, or QA gates are not yet compiled.
- [ ] Route asset inventory, candidate discovery, rights/fit decisions, and
  recreation planning through [asset-advisor](../asset-advisor/SKILL.md).
  Block content-production authoring when required visuals have no accepted
  source file or evidenced `searched_no_fit` generation route.
- [ ] Do not create custom SVG animation assets or use SVG/JSX/programmatic
  vector drawings as substitutes for missing scene illustrations, characters,
  props, backgrounds, textures, or diagrams. Existing user-supplied,
  brand-owned, licensed, or discovered SVG files may be consumed as accepted
  static media and animated with Remotion transforms, masks, crops, or
  treatment. A generation route counts only when Asset Advisor records
  candidate discovery and `searched_no_fit` (or the brief explicitly requires
  generation); `regen_ready` without that receipt does not bypass discovery.
- [ ] For a voice-led documentary or editorial reel made from layered stills
  and overlay media, load the
  [documentary reel production contract](references/documentary-reel.md).
  Require prepared overlay files from `asset-advisor`; keep deterministic
  treatment, compositing, micro-motion, and frame-addressed choreography in
  Remotion.
- [ ] Route still assets through `imagegen` or [ai-image-advisor](../ai-image-advisor/SKILL.md).
- [ ] Route model-native footage through [ai-video-advisor](../ai-video-advisor/SKILL.md), persistent avatar clips through [avatar-advisor](../avatar-advisor/SKILL.md), and audio direction through [audio-advisor](../audio-advisor/SKILL.md).
- [ ] For content-production videos using a Brand Kit or Tasty Pack,
  require a locked storyboard, asset manifest, cue sheet, and
  `element_leverage_map` from `content-impl-plan` built from complete
  element capsules; the locked plan must honor pinned elements
  when present. Block or label the run `technical_smoke` when those are missing.
- [ ] Require element realization receipts for every selected Brand Kit or
  Tasty Pack element used in the composition. Each receipt maps element ID,
  golden example, golden recipe, planned use, and accepted output; element names
  or descriptions alone are not grounding proof.
- [ ] For inspiration-led production, require `media_ready` or `regen_ready`
  handoff: pinned visual/audio/editing elements must arrive as resolved media
  refs or generated asset files with acceptance checks. If Remotion only has
  semantic element descriptions, label the render `semantic_storyboard_only`
  and do not claim Tasty Pack asset reuse. For visual scene assets,
  `regen_ready` additionally requires an Asset Advisor discovery receipt ending
  in `searched_no_fit` or an explicit brief requirement for generation; it
  permits the named raster/video generation owner but does not unlock Remotion
  until accepted files exist.
- [ ] For stitched model-native clips, probe every source clip duration,
  framerate, dimensions, and frame count before sequencing; set Remotion
  `Sequence` durations from observed frame counts, not assumed seconds. A
  requested 24 seconds or 720 frames is a target, not composition metadata,
  until probes and transition overlaps reconcile it.
- [ ] When the handoff uses deliberate scene breaks, load
  [scene-grid production](../video-production/references/scene-grid-production.md),
  consume one accepted clip per approved scene packet, and preserve the locked
  grids, character refs, prompts, and clip files. Remotion may trim and assemble
  them but must not regenerate or silently replace them.
- [ ] Require one final audio placement plan for narrative reels: VO/music/SFX
  bed, imported transcript/captions, ducking, transitions/effects, and any
  deliberate muted source clips. Audio providers create assets; Remotion owns
  their timing on the master edit. Do not substitute a premixed file for the
  cue/stem placement and ducking contract unless that premix is itself the
  explicitly approved final master with its source cue sheet attached.
- [ ] Consume the actual selected timing-master media (`voiceover`, `music`, or
  `source_video`) with observed duration/alignment/cues before final sequencing;
  derive scene/caption timing from that receipt and block planned-duration-only
  handoffs. Use `none` only when the locked plan explicitly selects it.

```text
stitched_scene_preflight(clips, target_duration?)
  -> for_each clip: ffprobe(width, height, avg_frame_rate, duration,
                            nb_frames | nb_read_frames)
  -> sequence_ranges: zero-based half-open [start_frame, end_frame)
  -> boundary_rule: next_start = prior_end; never repeat end_frame
  -> duration: sum(observed_ranges) - transition_overlaps

master_audio_timeline:
  voiceover: asset + start_frame + trim + gain
  music: asset + start_frame + trim + gain + ducking_ranges
  sfx[]: asset + cue_frame + trim + gain
  captions: imported timed transcript aligned to voiceover
```

Executable probe shape:

```bash
ffprobe -v error -count_frames -show_entries \
  stream=width,height,avg_frame_rate,nb_frames,nb_read_frames:format=duration \
  -of json <clip-path> > <media-probe-artifact.json>
```

For stitched narrative output, emit both tables even when rows remain blocked:

```text
| Packet ID | Accepted clip | Locked storyboard inputs | Observed media | In/out half-open range | Generation owner | Failure route |
| Scene packet | Approved transition | Approved effect | Frames | Blocker |
| Audio asset | Role | Start frame | End/trim | Gain | Ducking/cue | Blocker |
```

Use `none` for transitions or effects not named by the storyboard; never add an
unnamed effect for polish. Populate voiceover, music, and each SFX asset on the
single frame-based master timeline rather than summarizing that they will be
mixed later. Each scene row must map the packet ID to the accepted clip and
locked storyboard assets. A failed primary action must name its generation
owner and return route. Do not fill duration gaps with playback-rate changes,
loops, frozen-frame holds, or repeated boundary frames unless that exact remedy
is approved in the storyboard packet; otherwise return the affected packet.
- [ ] Render locally with Remotion project commands when a final MP4/still proof is requested and the local project can render.
- [ ] Even at planning time, name exact workspace paths for the representative
  still, final MP4, media probe, visual QA, and audio QA, plus the local render
  commands that will create them; do not leave proof as unnamed intentions.
- [ ] Route MP4 rendering through [remotion-render](../remotion-render/SKILL.md) only for an explicit external inference.sh render path when local rendering is not the chosen route and external compute is acceptable.
- [ ] Keep source code, props, local assets, notes, and any render inputs inside the workspace.
- [ ] Confirm external compute, spend, uploads, or API usage is explicitly acceptable before running render jobs outside local project commands.
- [ ] If the video is embedded in a frontend, route integration and visual proof through [frontend-craft](../frontend-craft/SKILL.md) and [visual-qa](../visual-qa/SKILL.md) when layout or taste is affected.
- [ ] Follow the native execution phase proof and writeback loop before claiming animation, composition, render-readiness, or final video quality.
<!-- END FARPLANE_IMPORTANT_CHECKLIST -->

Author deterministic video with Remotion and React. This skill owns writing the
React composition that stitches final assets, captions, overlays, audio, and
timed scenes into a locally provable video output. It contains the official
Remotion best-practices skill plus Farplane routing notes.

The imported upstream source and refresh note live in `references/upstream-source.md`.

## Farplane Routing

- Use this skill for Remotion code authoring, final asset stitching, timing, composition structure, media handling, captions, audio placement, transitions, effects, Remocn component integration, and local render sanity checks.
- Use `content-impl-plan` before this skill when the parent content ticket,
  advisor action list, or proof path is not ready.
- Use `asset-advisor` when the storyboard/reference still needs an asset
  inventory, candidate search receipt, recreation plan, or owner route map.
- For content-production work, never author custom SVG animation assets or
  SVG/JSX vector scene substitutes. Remotion animates accepted media; it does
  not replace Asset Advisor discovery with locally drawn illustrations.
- Use `imagegen` or `ai-image-advisor` for still assets that will be placed in Remotion `public/`.
- Use `ai-video-advisor` for model-native footage, `avatar-advisor` for
  persistent avatar direction, and `audio-advisor` for voice/music/SFX cue
  planning before Remotion assembles them.
- Use local Remotion render commands for final proof when available. Use
  `remotion-render` only when the Remotion code should be rendered to MP4
  through inference.sh `belt`.
- Use Remocn only as a copied-code component source inside a Remotion project.
  It is not a replacement for Remotion timing, composition ownership, or final
  render proof.
- Do not use CSS transitions, CSS animations, or Tailwind animation utilities for frame-accurate motion; animate with Remotion frame math.
- For inspiration-led content, do not accept generic CSS/text/cards as a final
  creative output unless the caller explicitly downgrades the run to
  `technical_smoke` or `text_only_format`. Production rendering requires a
  passed `creative_lock`, concrete asset files or source handles, resolved
  media refs or generated asset files for pinned visual/audio/editing elements,
  and timed audio or motion obligations from the plan. Do not require separate
  Resource Bank evidence records unless the production task needs direct media
  reuse or audit proof.
- For model-native clip stitching, use media components and exact frame math.
  Verify source clip counts with `ffprobe`/Remotion metadata, prefer
  `OffthreadVideo` for stitched external clips, avoid repeated boundary frames,
  and add transition frames only when the storyboard names a scene break.
- For an approved scene-grid handoff, treat scene packet IDs as stable timeline
  keys. Use the packet's named cut/transition and audio obligations; return a
  failed primary action with its packet ID to `ai-video-advisor` or the named
  provider-generation owner instead of merely flagging it, concealing it with a
  transition, or regenerating its approved storyboard assets.

```text
scene_failure(packet_id, reason)
  -> owner: ai-video-advisor | named_provider_generation_owner
  -> action: regenerate_that_clip_from_locked_assets | request_scene_edit
  -> never: hide_with_transition | silently_replace_storyboard_assets
```

## Reference Routing

- Video-first layout, text sizing, safe spacing, promos, motion graphics, or text-heavy scenes: `rules/video-layout.md`
- Captions or subtitles: `rules/subtitles.md`, `rules/display-captions.md`, `rules/import-srt-captions.md`, or `rules/transcribe-captions.md`
- Audio, SFX, voiceover, visualization, or silence trimming: `rules/audio.md`, `rules/sfx.md`, `rules/voiceover.md`, `rules/audio-visualization.md`, `rules/silence-detection.md`
- Sequencing, timing, transitions, trimming, or transparent videos: `rules/sequencing.md`, `rules/timing.md`, `rules/transitions.md`, `rules/trimming.md`, `rules/transparent-videos.md`
- Visual or pixel effects, light leaks, filters, distortion, glitch, blur, gradients, or shader-like treatments: `rules/effects.md` or `rules/light-leaks.md`
- Images, videos, GIFs, Lottie, fonts, Tailwind, or HTML-in-canvas: `rules/images.md`, `rules/videos.md`, `rules/gifs.md`, `rules/lottie.md`, `rules/google-fonts.md`, `rules/local-fonts.md`, `rules/tailwind.md`, `rules/html-in-canvas.md`
- Dynamic props, dimensions, metadata, or DOM/text measurement: `rules/parameters.md`, `rules/calculate-metadata.md`, `rules/get-video-dimensions.md`, `rules/get-video-duration.md`, `rules/get-audio-duration.md`, `rules/measuring-dom-nodes.md`, `rules/measuring-text.md`
- 3D or maps: `rules/3d.md`, `rules/maplibre.md`
- Remocn copy-paste motion components, transitions, backgrounds, UI scenes, or demo-video blocks: `references/remocn.md`
- Approved model-native scene packets and locked-asset assembly: `../video-production/references/scene-grid-production.md`
- Voice-led documentary/editorial reels using layered stills, prepared
  overlays, shared film treatment, micro-motion, and frame-addressed
  choreography: `references/documentary-reel.md`

## When to use

Use this skill whenever you are dealing with Remotion code to obtain the domain-specific knowledge.

## New project setup

When in an empty folder or workspace with no existing Remotion project, scaffold one using:

```bash
npx create-video@latest --yes --blank --no-tailwind my-video
```

Replace `my-video` with a suitable project name.

## Designing a video

Before designing visual scenes, layouts, promos, motion graphics, or text-heavy
videos, load `rules/video-layout.md` for video-first layout and text sizing
guidance.

Animate properties using `useCurrentFrame()` and `interpolate()`. Prefer
`interpolate()` over `spring()` unless physics-based motion is explicitly
needed. Use `Easing.bezier()` to customize timing, including jumpy or
overshooting motion.

For animations that should be editable in Remotion Studio, keep the
`interpolate()` call inline in the `style` prop and use individual CSS transform
properties such as `scale`, `translate`, and `rotate` instead of composing a
`transform` string.

```tsx
import { Easing, interpolate, useCurrentFrame, useVideoConfig } from "remotion";

export const FadeIn = () => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();

  const opacity = interpolate(frame, [0, 2 * fps], [0, 1], {
    extrapolateRight: "clamp",
    extrapolateLeft: "clamp",
    easing: Easing.bezier(0.16, 1, 0.3, 1),
  });

  return <div style={{ opacity }}>Hello World!</div>;
};
```

CSS transitions or animations are FORBIDDEN - they will not render correctly.
Tailwind animation class names are FORBIDDEN - they will not render correctly.

Place assets in the `public/` folder at your project root.

Use `staticFile()` to reference files from the `public/` folder.

Add images using the `<Img>` component:

```tsx
import { Img, staticFile } from "remotion";

export const MyComposition = () => {
  return <Img src={staticFile("logo.png")} style={{ width: 100, height: 100 }} />;
};
```

Add videos using the `<Video>` component from `@remotion/media`:

```tsx
import { Video } from "@remotion/media";
import { staticFile } from "remotion";

export const MyComposition = () => {
  return <Video src={staticFile("video.mp4")} style={{ opacity: 0.5 }} />;
};
```

Add audio using the `<Audio>` component from `@remotion/media`:

```tsx
import { Audio } from "@remotion/media";
import { staticFile } from "remotion";

export const MyComposition = () => {
  return <Audio src={staticFile("audio.mp3")} />;
};
```

Assets can be also referenced as remote URLs:

```tsx
import { Video } from "@remotion/media";

export const MyComposition = () => {
  return <Video src="https://remotion.media/video.mp4" />
};
```

To delay content wrap it in `<Sequence>` and use `from`.
To limit the duration of an element, use `durationInFrames` of `<Sequence>`.
`<Sequence>` by default is an absolute fill. For inline content, use `layout="none"`.

```tsx
import { Easing, AbsoluteFill, interpolate, Sequence, useCurrentFrame, useVideoConfig } from "remotion";

export const Title = () => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();

  const opacity = interpolate(frame, [0, 2 * fps], [0, 1], {
    extrapolateRight: "clamp",
    extrapolateLeft: "clamp",
    easing: Easing.bezier(0.16, 1, 0.3, 1),
  });

  return <div style={{ opacity }}>Title</div>;
};

export const Subtitle = () => {
  return <div>Subtitle</div>;
};

const Main = () => {
  const {fps} = useVideoConfig();

  return (
    <AbsoluteFill>
      <Sequence>
        <Background />
      </Sequence>
      <Sequence from={1 * fps} durationInFrames={2 * fps} layout="none">
        <Title />
      </Sequence>
      <Sequence from={2 * fps} durationInFrames={2 * fps} layout="none">
        <Subtitle />
      </Sequence>
    </AbsoluteFill>
  );
}
```

The width, height, fps, and duration of a video is defined in `src/Root.tsx`:

```tsx
import { Composition } from "remotion";
import { MyComposition } from "./MyComposition";

export const RemotionRoot = () => {
  return (
    <Composition
      id="MyComposition"
      component={MyComposition}
      durationInFrames={100}
      fps={30}
      width={1080}
      height={1080}
    />
  );
};
```

Metadata can also be calculated dynamically:

```tsx
import { Composition, CalculateMetadataFunction } from "remotion";
import { MyComposition, MyCompositionProps } from "./MyComposition";

const calculateMetadata: CalculateMetadataFunction<
  MyCompositionProps
> = async ({ props, abortSignal }) => {
  const data = await fetch(`https://api.example.com/video/${props.videoId}`, {
    signal: abortSignal,
  }).then((res) => res.json());

  return {
    durationInFrames: Math.ceil(data.duration * 30),
    props: {
      ...props,
      videoUrl: data.url,
    },
    width: 1080,
    height: 1080,
  };
};

export const RemotionRoot = () => {
  return (
    <Composition
      id="MyComposition"
      component={MyComposition}
      fps={30}
      width={1080}
      height={1080}
      defaultProps={{ videoId: "abc123" }}
      calculateMetadata={calculateMetadata}
    />
  );
};
```

## Starting preview

Start the Remotion Studio to preview a video:

```bash
npx remotion studio
```

## Optional: one-frame render check

You can render a single frame with the CLI to sanity-check layout, colors, or timing.
Skip it for trivial edits, pure refactors, or when you already have enough confidence from Studio or prior renders.

```bash
npx remotion still [composition-id] --scale=0.25 --frame=30
```

At 30 fps, `--frame=30` is the one-second mark (`--frame` is zero-based).

## Captions

When dealing with captions or subtitles, load the [./rules/subtitles.md](./rules/subtitles.md) file for more information.

## Using FFmpeg

For some video operations, such as trimming videos or detecting silence, FFmpeg should be used. Load the [./rules/ffmpeg.md](./rules/ffmpeg.md) file for more information.

## Silence detection

When needing to detect and trim silent segments from video or audio files, load the [./rules/silence-detection.md](./rules/silence-detection.md) file.

## Audio visualization

When needing to visualize audio (spectrum bars, waveforms, bass-reactive effects), load the [./rules/audio-visualization.md](./rules/audio-visualization.md) file for more information.

## Sound effects

When needing to use sound effects, load the [./rules/sfx.md](./rules/sfx.md) file for more information.

## 3D content

See [rules/3d.md](rules/3d.md) for 3D content in Remotion using Three.js and React Three Fiber.

## Advanced audio

See [rules/audio.md](rules/audio.md) for advanced audio features like trimming, volume, speed, pitch.

## Dynamic duration, dimensions and data

See [rules/calculate-metadata.md](rules/calculate-metadata.md) for dynamically set composition duration, dimensions, and props.

## Advanced compositions

See [rules/compositions.md](rules/compositions.md) for how to define stills, folders, default props and for how to nest compositions.

## Google Fonts

Is the recommended way to load fonts in Remotion. See [rules/google-fonts.md](rules/google-fonts.md) for how to load Google Fonts.

## Local fonts

See [rules/local-fonts.md](rules/local-fonts.md) for how to load local fonts.

## Getting audio duration

See [rules/get-audio-duration.md](rules/get-audio-duration.md) for getting the duration of an audio file in seconds with Mediabunny.

## Getting video dimensions

See [rules/get-video-dimensions.md](rules/get-video-dimensions.md) for getting the width and height of a video file with Mediabunny.

## Getting video duration

See [rules/get-video-duration.md](rules/get-video-duration.md) for getting the duration of a video file in seconds with Mediabunny.

## GIFs

See [rules/gifs.md](rules/gifs.md) for how to display GIFs synchronized with Remotion's timeline.

## Advanced Images

See [rules/images.md](rules/images.md) for sizing and positioning images, dynamic image paths, and getting image dimensions.

## Light leaks

See [rules/light-leaks.md](rules/light-leaks.md) for light leak overlay effects using `@remotion/light-leaks`.

## Visual and pixel effects

When creating a visual effect, prefer: 1. normal
Remotion/HTML/CSS/filter/blend/mask treatment over accepted media, 2. a listed
effect via [rules/effects.md](rules/effects.md), including on HTML rendered
through `<HtmlInCanvas>`, 3. a custom `createEffect()` via
[rules/effects.md](rules/effects.md) when the user asks for a
reusable/project-specific effect, 4. custom `<HtmlInCanvas onPaint>` via
[rules/html-in-canvas.md](rules/html-in-canvas.md) only if no effect fits.
This effects route does not permit custom SVG/JSX scene-asset authoring.

## Lottie animations

See [rules/lottie.md](rules/lottie.md) for embedding Lottie animations in Remotion.

## HTML in canvas

See [rules/html-in-canvas.md](rules/html-in-canvas.md) if you need to render HTML into a `<canvas>` to apply 2D or WebGL effects via `<HtmlInCanvas>`.

## Measuring DOM nodes

See [rules/measuring-dom-nodes.md](rules/measuring-dom-nodes.md) for measuring DOM element dimensions in Remotion.

## Measuring text

See [rules/measuring-text.md](rules/measuring-text.md) for measuring text dimensions, fitting text to containers, and checking overflow.

## Advanced sequencing

See [rules/sequencing.md](rules/sequencing.md) for more sequencing patterns - delay, trim, limit duration of items.

## TailwindCSS

See [rules/tailwind.md](rules/tailwind.md) for using TailwindCSS in Remotion.

## Text animations

See [rules/text-animations.md](rules/text-animations.md) for typography and text animation patterns.

## Advanced timing

See [rules/timing.md](rules/timing.md) for advanced timing with `interpolate` and Bézier easing, and springs.

## Transitions

See [rules/transitions.md](rules/transitions.md) for scene transition patterns.

## Transparent videos

See [rules/transparent-videos.md](rules/transparent-videos.md) for rendering out a video with transparency.

## Trimming

See [rules/trimming.md](rules/trimming.md) for trimming patterns - cutting the beginning or end of animations.

## Advanced Videos

See [rules/videos.md](rules/videos.md) for advanced knowledge about embedding videos - trimming, volume, speed, looping, pitch.

## Parameterized videos

See [rules/parameters.md](rules/parameters.md) for making a composition parametrizable by adding a Zod schema.

## Maps

For simple maps with little flyovers, consider using static map images.
For complex maps with animated routes or flyovers, load [rules/maplibre.md](rules/maplibre.md).

## Voiceover

See [rules/voiceover.md](rules/voiceover.md) for adding AI-generated voiceover to Remotion compositions using ElevenLabs TTS.
