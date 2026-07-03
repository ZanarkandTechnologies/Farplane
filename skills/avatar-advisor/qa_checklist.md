---
template_uses:
  skill-qa-checklist: "0.1.1"
---

# Avatar Advisor QA Checklist

- [ ] Identity, likeness, voice, and consent/usage constraints are explicit.
- [ ] Persistence requirements cover face/character, wardrobe, framing,
  gesture, voice, and retake criteria.
- [ ] Script beats are mapped to performance, expression, lipsync, and audio
  needs.
- [ ] Provider execution is routed to `ai-video-advisor`; still references to
  `ai-image-advisor`; audio to `audio-advisor`; final stitching to `remotion`.
- [ ] The output includes acceptance checks and blockers before generation.
