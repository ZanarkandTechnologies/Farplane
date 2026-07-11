---
template_uses:
  skill-qa-checklist: "0.1.1"
---

# Content Impl Plan QA Checklist

- [ ] The plan starts from idea plus audience/promise and, when present,
  converts Inspiration Pack/Tasty Pack material into a `reference_leverage_map`
  from `captures[].elements` mapped to planned shots, assets, audio cues,
  motion cues, copy moves, or narrative beats; for narrative video it also
  names the reference/reel type, viewer question -> answer, continuity spine,
  generation topology before AI-video spend, and reference readiness as
  `media_ready`, `regen_ready`, `semantic_only`, or `blocked`; pinned
  visual/audio/editing elements must have resolved media refs, generation
  packets, or explicit nonuse reasons before Remotion is called production.
- [ ] Storyboard, asset, avatar, audio, image, video, Remotion, review, and QA
  responsibilities are separated instead of hidden in one generic workflow.
- [ ] Every advisor action has an owner skill, input, output, acceptance check,
  blocker, dependency order, and a `creative_lock` gate before Remotion; isolated
  model-native clip batches are blocked unless the selected format is montage.
- [ ] Rights, likeness, music, source, brand, and platform risks are named when
  the reference or assets imply them.
- [ ] The terminal path includes Remotion stitching/local render proof plus
  review or QA gates before a completion claim.
