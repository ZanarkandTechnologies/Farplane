# Fish Audio Voice Route

Load this reference only after `kind = voice` and `provider = fish` resolve.
Fish is not a music or SFX route in this skill.

## Provider contract

- Runtime secret: `FISH_API_KEY`, resolved from the managed environment and
  checked only for presence before an authorized execution.
- Endpoint/SDK capability: text-to-speech.
- Farplane default: `s2.1-pro-free`, selected through the required `model`
  request header. Fish documents this as the S2.1 Pro engine on the free
  developer tier.
- Voice input: a rights-safe `reference_id`, or explicitly authorized reference
  audio plus transcript. Treat private voice handles as private context.
- Keep the engine and voice identifiers distinct: `model` selects the TTS
  engine (for example `s2.1-pro-free`), while `reference_id` selects the voice
  catalog entry (for example the ID copied from a Fish `modelId` URL).
- Useful packet parameters: `model`, `format`, `sample_rate`, `mp3_bitrate`,
  `latency`, `prosody.speed`, `prosody.volume`, normalization, and optional
  sampling controls.

## Execution notes

Use `farplane run -- <provider command>` or `doppler run -- <provider command>`
from the project checkout. Do not print the environment, authorization header,
or serialized request. For long narration, preserve scene boundaries in the
packet so generated files can be measured and aligned independently.

Sanitized receipts may retain the provider, model, format, artifact path,
duration, safe request/trace identifiers, and observed acceptance result.

## Official grounding

- Fish Audio text-to-speech guide:
  https://docs.fish.audio/features/text-to-speech
- Fish Audio TTS API reference:
  https://docs.fish.audio/api-reference/endpoint/openapi-v1/text-to-speech
- Official agent-skill install source (research input, not a Farplane runtime
  dependency): `npx skills add https://docs.fish.audio --skill fish-audio-api -a codex`
