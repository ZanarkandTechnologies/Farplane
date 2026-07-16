---
template_uses:
  skill-qa-checklist: "0.1.1"
---

# Content Impl Plan QA Checklist

- [ ] The plan starts from idea plus audience/promise, resolves content kind,
  video method, and visual direction as method_default, profile_only,
  inspiration_only, or composed_direction, and blocks incompatible hard
  constraints instead of silently blending them. A named style profile is
  loaded and checked only when supplied. When Inspiration is present, the plan
  converts its material into a `reference_leverage_map`
  from `captures[].elements` mapped to planned shots, assets, audio cues,
  motion cues, copy moves, or narrative beats; for narrative video it also
  names the reference/reel type, viewer question -> answer, continuity spine,
  generation topology before AI-video spend, and reference readiness as
  `media_ready`, `regen_ready`, `semantic_only`, or `blocked`; pinned
  visual/audio/editing elements must have resolved media refs, generation
  packets, or explicit nonuse reasons before Remotion is called production.
- [ ] Storyboard, asset, avatar, audio, image, video, Remotion, review, and QA
  responsibilities are separated instead of hidden in one generic workflow;
  `audio-advisor` owns direction/mix while approved provider-ready voice,
  music, and SFX packets route to `audio-generation`. For deliberate scene
  breaks, one normally 4-5 second provider clip maps to one scene packet with a
  clean grid, annotated grid, keyed notes, transition/audio obligations, and
  provider strategy; the actual dimension-verified image files and notes are
  shown before generation. Text-only panels or intended paths remain draft-only.
- [ ] Every advisor action has an owner skill, input, output, acceptance check,
  blocker, dependency order, and a `creative_lock` gate before Remotion; isolated
  model-native clip batches are blocked unless the selected format is montage.
  Human approval locks unchanged scene assets for reuse; regeneration is an
  explicit, versioned, scene-local edit rather than a silent default.
- [ ] Rights, likeness, music, source, brand, and platform risks are named when
  the reference or assets imply them.
- [ ] The terminal path includes Remotion stitching/local render proof plus
  review or QA gates before a completion claim.
