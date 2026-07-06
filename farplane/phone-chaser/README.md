# Farplane Phone Chaser

LiveKit + Fish Audio outbound reminder agent.

The agent is dispatched with JSON metadata, dials the configured phone number
through the LiveKit outbound SIP trunk, waits for the phone participant to
answer, then speaks the reminder with Fish Audio TTS. After the reminder it
keeps the call open briefly so the recipient can talk back through LiveKit STT
and a compact LLM response policy.

## Run Locally

```bash
cd farplane/phone-chaser
uv sync
uv run src/agent.py dev
```

In another shell:

```bash
lk dispatch create \
  --new-room \
  --agent-name farplane-phone-chaser \
  --metadata '{"phone_number":"+15557654321","message":"Review the waiting Farplane decision. Reply approve, revise, or reject.","urgency":"high"}'
```

## Required Env

These are rendered into `~/.codex/config.toml` from `~/.farplane/config.toml`.

- `LIVEKIT_URL`
- `LIVEKIT_API_KEY`
- `LIVEKIT_API_SECRET`
- `LIVEKIT_SIP_TRUNK_ID`
- `LIVEKIT_SIP_NUMBER`
- `FISH_API_KEY`
- `FISH_AUDIO_REFERENCE_ID`
- `FISH_AUDIO_MODEL`
- `FISH_AUDIO_LATENCY_MODE`
- `FARPLANE_REMINDER_PHONE`
- `FARPLANE_PHONE_REMINDER_AGENT_NAME`

## Optional Env

- `LIVEKIT_STT_MODEL` defaults to `deepgram/flux-general:en`
- `LIVEKIT_LLM_MODEL` defaults to `google/gemma-4-31b-it`
- `LIVEKIT_TURN_DETECTION` defaults to `stt`
- `LIVEKIT_MIN_ENDPOINTING_DELAY` defaults to `0.3`
- `LIVEKIT_MAX_ENDPOINTING_DELAY` defaults to `2.0`
- `LIVEKIT_MIN_INTERRUPTION_DURATION` defaults to `0.5`
- `FARPLANE_PHONE_CHASER_CONVERSATION_SECONDS` defaults to `45`

## Latency Notes

The first reminder is scripted with `session.say(...)`, so delay after pickup is
primarily SIP answer handling, worker/session startup, and TTS startup rather
than LLM generation. The runtime defaults Fish Audio to low-latency mode, uses
Deepgram Flux STT for faster turn endpointing after the reminder, and enables
LiveKit preemptive generation with preemptive TTS for replies. The session is
started before dialing so pickup does not wait for agent-session initialization.

## Skill Entry

Use `skills/phone-chaser/` to dispatch reminder calls through this deployed
agent. Keep deployment code here; keep operator workflow, safety gates, and
call dispatch helpers in the skill package.
