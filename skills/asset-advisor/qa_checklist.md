---
template_uses:
  skill-qa-checklist: "0.1.1"
---

# Asset Advisor QA Checklist

- [ ] The plan decomposes the reference/storyboard into concrete asset units and
  maps relevant Inspiration Pack `captures[].elements` to asset rows,
  generation routes, source handles, or explicit missing-input blockers,
  prioritizing pinned elements when present. For
  narrative video, it includes continuity assets: character bible or
  no-character rationale, recurring prop/object bible, location/lighting
  anchors, and start/end frame files or blockers for AI-video handoffs.
  Anchored Tasty Pack elements such as contact sheets, frame timestamps, frame
  ranges, thumbnails, clips, audio, or transcripts are resolved into media refs
  or regeneration packets with owner skill, prompt/direction, and acceptance
  checks.
- [ ] Each asset has a source, decision, owner route, and acceptance check.
- [ ] Rights, likeness, brand, platform, duration, and aspect-ratio risks are
  named when relevant.
- [ ] Remotion handoff includes files or missing-file blockers, scene roles,
  timing, captions/overlays, proof expectations, and no generic CSS/text-only
  pass for inspiration-led video unless explicitly downgraded.
- [ ] The output separates stills, model-native clips, avatar, audio, and
  composition work instead of routing everything to one skill.
