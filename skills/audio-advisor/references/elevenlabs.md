# ElevenLabs Voice, Music, and SFX Routes

Load this reference only after `provider = elevenlabs` resolves. ElevenLabs
supports voice, music, and SFX in this skill; choose exactly one capability per
packet.

## Shared provider contract

- Runtime secret: `ELEVENLABS_API_KEY`, resolved from the managed environment
  and checked only for presence before an authorized execution.
- Never store personal voice IDs, credentials, raw headers, or full provider
  request bodies in tracked config or receipts.
- Retain safe request/trace IDs and provider metering metadata when returned.

## Capability parameters

### Voice

Require text, a rights-safe voice/profile handle, model, output format, and
scene/cue timing. The tracked default uses `eleven_v3` and
`mp3_44100_128`; confirm current official docs before changing them.

### Music

Require musical job, duration, structure, instrumentation/style traits, tempo
or energy arc, vocal policy, loop/end behavior, and cue/mix acceptance checks.
Execution always requires explicit spend authority. The tracked default uses
`music_v2` with `mp3_48000_192`; current API defaults may differ during the
v1-to-v2 transition, so the packet must carry the selected model explicitly.
The local executor calls `POST /v1/music` with `prompt`, `music_length_ms`,
`model_id`, and optional `force_instrumental`, matching the current official
compose endpoint. Music API access requires a paid ElevenLabs plan.

### SFX

Require the event/texture, duration when bounded, loop policy, prompt influence
when intentionally overridden, placement cue, and acceptance check. The
tracked default uses `eleven_text_to_sound_v2`; effects may be up to 30 seconds
per current official documentation.

## Official grounding

- Agent tooling and official skill collection:
  https://elevenlabs.io/docs/eleven-api/resources/agent-tooling
- Text-to-speech quickstart:
  https://elevenlabs.io/docs/eleven-api/quickstart/
- Music quickstart:
  https://elevenlabs.io/docs/eleven-api/guides/cookbooks/music
- Compose Music API:
  https://elevenlabs.io/docs/api-reference/music/compose
- Sound-effects quickstart:
  https://elevenlabs.io/docs/eleven-api/guides/cookbooks/sound-effects
- Official upstream skills (research inputs, not Farplane runtime
  dependencies): `npx skills add elevenlabs/skills --skill text-to-speech`,
  `--skill music`, or `--skill sound-effects`.
