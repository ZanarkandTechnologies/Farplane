---
template_uses:
  skill-qa-checklist: "0.1.1"
---

# Audio Advisor QA Checklist

- [ ] Voice, music, SFX/Foley, silence, and mix/ducking needs are separated.
- [ ] Each audio cue is tied to a scene, timestamp/frame range, purpose, route,
  and acceptance check.
- [ ] Copyright, source, voice, likeness, or consent risks are named when
  relevant.
- [ ] Avatar/lipsync audio is routed through `avatar-advisor`; provider-specific
  audio/video generation through `ai-video-advisor`; final placement through
  `remotion`.
- [ ] The Remotion handoff includes files or blockers, cue timing, volume/mix
  notes, and proof expectations.
