---
template_uses:
  skill-qa-checklist: "0.1.1"
---

# Audio Generation QA Checklist

- [ ] `config.toml` was read before provider/default selection, invocation
  overrides won, and no credential, private voice ID, or secret-like key/value
  appears in tracked config or output.
- [ ] The capability route is valid—Fish for voice only; ElevenLabs for voice,
  music, or SFX—and unsupported pairs return a blocker instead of falling back.
  Supported-pair safety blockers use a first-class code such as
  `missing_runtime_secret` or `unresolved_voice_consent`; unsupported-pair
  blockers are not reused for consent, authority, secret, or artifact failures.
- [ ] The packet carries an approved brief, timing/cue binding, output owner,
  provider parameters, acceptance checks, and voice rights/consent when relevant.
- [ ] Provider execution occurred only with explicit upload/spend/generation
  authority and a present runtime secret; otherwise the result is a dry-run
  packet or exact blocker with no external call.
- [ ] Any execution receipt contains artifact path, observed duration/format,
  safe provider metadata, metering when available, and acceptance evidence,
  with credentials and raw authorization headers redacted; JSON packet and
  blocker artifacts pass `scripts/validate_audio_packet.py`.
