---
template_uses:
  skill-qa-checklist: "0.1.1"
---

# Audio Advisor QA Checklist

- [ ] Voice, music, SFX/Foley, ambience, silence, and mix/ducking are separated;
  multi-clip narrative work uses one time-coded master audio spine with
  motion/edit bindings and acceptance checks.
- [ ] Each interesting/common SFX cue follows `reuse -> candidate discovery ->
  operator decision -> generate`; the final content plan lists up to three item
  links with cue, search phrase, fit, rights risk, and approval status, or an
  explicit `searched_no_fit` result.
- [ ] SoundButtonsWorld discovery uses public indexed results only. The agent
  does not automate site search, open download controls, crawl, or download;
  every candidate remains `awaiting_operator_download_and_approval` and is not
  represented as commercially cleared.
- [ ] Provider routes and safety gates hold: config is read; Fish is voice-only;
  ElevenLabs handles voice/music/SFX; execution requires explicit authority and
  runtime-secret readiness; packets/receipts expose no credential or private
  voice ID and validate with `scripts/validate_audio_packet.py`.
- [ ] Generated or operator-provided files open and match their cue; rights/consent,
  provider receipt, mix notes, volume/ducking, output paths, residual
  risk, and Remotion proof expectations are present before handoff.
