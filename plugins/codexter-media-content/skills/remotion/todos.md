# Remotion Todos

Use this as the ordered checklist whenever `remotion` is active.

- [ ] Classify the Remotion job: composition authoring, timing, sequencing, captions, audio, motion graphics, data visualization, UI animation, HTML-in-canvas, or render-readiness check.
- [ ] State the composition name, dimensions, fps, duration, assets, props, output intent, and handoff path before authoring code.
- [ ] Use [research:official-docs](../research/SKILL.md#researchofficial-docs) or [research:code-patterns](../research/SKILL.md#researchcode-patterns) when Remotion API behavior, official docs, local code patterns, or source assets shape the implementation.
- [ ] Use [plan](../plan/SKILL.md) when choosing authoring route, animation structure, asset route, render route, or scope cut.
- [ ] Load the relevant Remotion rule file from `rules/` before implementing specialized behavior such as captions, audio, sequencing, timing, transitions, images, videos, fonts, HTML-in-canvas, measurement, or 3D.
- [ ] Use frame math with `useCurrentFrame()`, `interpolate()`, `Sequence`, and Remotion APIs; do not use CSS transitions, CSS animations, or Tailwind animation utilities for frame-accurate motion.
- [ ] Route still assets through `imagegen` or [image-generation](../image-generation/SKILL.md).
- [ ] Route model-native footage or avatar clips through [video-generation](../video-generation/SKILL.md).
- [ ] Route MP4 rendering through [remotion-render](../remotion-render/SKILL.md) only when a rendered output is requested and external compute is acceptable.
- [ ] Keep source code, props, local assets, notes, and any render inputs inside the workspace.
- [ ] Confirm external compute, spend, uploads, or API usage is explicitly acceptable before running render jobs outside local project commands.
- [ ] If the video is embedded in a frontend, route integration and visual proof through [frontend-craft](../frontend-craft/SKILL.md) and [visual-qa](../visual-qa/SKILL.md) when layout or taste is affected.
- [ ] Follow the [execute](../execute/SKILL.md) proof and writeback loop before claiming animation, composition, render-readiness, or final video quality.
