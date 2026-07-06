---
title: Phone Chaser Setup Reference
owner: phone-chaser
status: active
kind: reference
---

# Phone Chaser Setup Reference

Read this only when setup, deployment, provider repair, or model choices are in
scope. Normal call dispatches should use `scripts/dispatch_call.py` from the
skill first-load contract.

## Runtime Owner

The deployable worker lives at:

```text
farplane/phone-chaser/
```

The skill owns dispatch workflow and safety gates. The runtime module owns:

- LiveKit agent code in `src/agent.py`
- deployment metadata in `livekit.toml`
- dependency lock in `uv.lock`
- Docker build files
- local ignored `.env.local`

## Required Private Values

These values are rendered by Farplane runtime config or supplied by local env.
Keep real values in private config/env, never in tracked files.

```text
LIVEKIT_URL
LIVEKIT_API_KEY
LIVEKIT_API_SECRET
LIVEKIT_SIP_TRUNK_ID
LIVEKIT_SIP_NUMBER
FISH_API_KEY
FISH_AUDIO_REFERENCE_ID
FISH_AUDIO_MODEL
FISH_AUDIO_LATENCY_MODE
FARPLANE_REMINDER_PHONE
FARPLANE_PHONE_REMINDER_AGENT_NAME
```

Optional model/runtime knobs:

```text
LIVEKIT_STT_MODEL
LIVEKIT_LLM_MODEL
LIVEKIT_TURN_DETECTION
LIVEKIT_MIN_ENDPOINTING_DELAY
LIVEKIT_MAX_ENDPOINTING_DELAY
LIVEKIT_MIN_INTERRUPTION_DURATION
FARPLANE_PHONE_CHASER_CONVERSATION_SECONDS
```

Current defaults favor low-latency reminder calls:

- STT: `deepgram/flux-general:en`
- LLM: `google/gemma-4-31b-it`
- TTS: Fish Audio `latency_mode=low`
- Turn detection: `stt`
- Endpointing: `0.3` minimum delay and `2.0` maximum delay
- Interruption: adaptive mode with `0.5` second minimum interruption duration
- Preemptive generation: enabled with preemptive TTS

Do not switch models during a dispatch-only task; make model changes in the
runtime module with deployment proof.

## Common Commands

Run locally:

```bash
cd farplane/phone-chaser
uv sync
uv run src/agent.py dev
```

Deploy:

```bash
cd farplane/phone-chaser
lk agent deploy . --secrets-file .env.local --ignore-empty-secrets
```

Dispatch through the skill:

```bash
python3 skills/phone-chaser/scripts/dispatch_call.py \
  --message "Kenji. Review the waiting Farplane decision. Reply approve, revise, or reject." \
  --urgency high
```

## Provider Notes

- LiveKit Phone Numbers may be inbound-only; outbound uses the configured SIP
  trunk.
- Telnyx must allow the destination country in the outbound voice profile.
- Fish Audio provides TTS voice only. Talkback also depends on LiveKit STT and
  LLM settings.
- `lk cloud auth` must already be valid for `lk dispatch create` unless
  another authenticated LiveKit workflow is used.
