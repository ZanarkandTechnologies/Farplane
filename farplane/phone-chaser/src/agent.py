from __future__ import annotations

import json
import os
import asyncio
from dataclasses import dataclass

from dotenv import load_dotenv
from livekit import agents, api
from livekit.agents import Agent, AgentServer, AgentSession, TurnHandlingOptions
from livekit.plugins.fishaudio import TTS

load_dotenv(".env.local")

DEFAULT_STT_MODEL = "deepgram/flux-general:en"
DEFAULT_LLM_MODEL = "google/gemma-4-31b-it"
DEFAULT_FISH_AUDIO_MODEL = "s1"
DEFAULT_FISH_AUDIO_LATENCY_MODE = "low"
DEFAULT_TURN_DETECTION = "stt"
DEFAULT_MIN_ENDPOINTING_DELAY = 0.3
DEFAULT_MAX_ENDPOINTING_DELAY = 2.0
DEFAULT_MIN_INTERRUPTION_DURATION = 0.5

DEFAULT_MESSAGE = (
    "Kenji. This is Farplane. There is a decision waiting. "
    "You only need to reply with one word: approve, revise, or reject. "
    "You can say the answer on this call, or open Codex or Telegram and do it now."
)


@dataclass(frozen=True)
class ReminderDispatch:
    phone_number: str
    message: str
    urgency: str


class PhoneChaser(Agent):
    def __init__(self, reminder: ReminderDispatch) -> None:
        super().__init__(
            instructions=(
                "You are Farplane Phone Chaser, a concise phone reminder agent. "
                "Speak like a direct operational assistant. Do not roleplay a "
                "copyrighted character. Do not chat at length. Your job is to "
                "deliver the reminder, hear the user's answer, confirm the one "
                "concrete action, and end politely. If the user asks a brief "
                "clarifying question, answer it in one or two sentences and "
                "return to the action."
            )
        )
        self.reminder = reminder


def _env(name: str, default: str = "") -> str:
    return os.getenv(name, default).strip()


def _float_env(name: str, default: float) -> float:
    raw_value = _env(name, str(default))
    try:
        return float(raw_value)
    except ValueError:
        return default


def _dispatch_from_metadata(metadata: str) -> ReminderDispatch:
    try:
        raw = json.loads(metadata or "{}")
    except json.JSONDecodeError:
        raw = {}

    phone_number = str(raw.get("phone_number") or _env("FARPLANE_REMINDER_PHONE"))
    message = str(raw.get("message") or DEFAULT_MESSAGE)
    urgency = str(raw.get("urgency") or "normal")
    return ReminderDispatch(
        phone_number=phone_number.strip(),
        message=message.strip(),
        urgency=urgency.strip(),
    )


def _tts() -> TTS:
    return TTS(
        api_key=_env("FISH_API_KEY") or None,
        voice_id=_env("FISH_AUDIO_REFERENCE_ID") or None,
        model=_env("FISH_AUDIO_MODEL", DEFAULT_FISH_AUDIO_MODEL),
        sample_rate=24000,
        latency_mode=_env("FISH_AUDIO_LATENCY_MODE", DEFAULT_FISH_AUDIO_LATENCY_MODE),
    )


def _conversation_seconds() -> float:
    raw_value = _env("FARPLANE_PHONE_CHASER_CONVERSATION_SECONDS", "45")
    try:
        return max(10.0, min(float(raw_value), 180.0))
    except ValueError:
        return 45.0


async def _dial_phone(ctx: agents.JobContext, reminder: ReminderDispatch) -> str:
    if not reminder.phone_number:
        raise RuntimeError("Missing phone_number metadata and FARPLANE_REMINDER_PHONE")

    trunk_id = _env("LIVEKIT_SIP_TRUNK_ID")
    if not trunk_id:
        raise RuntimeError("Missing LIVEKIT_SIP_TRUNK_ID")

    participant_identity = f"phone-{reminder.phone_number.replace('+', '')}"
    try:
        await ctx.api.sip.create_sip_participant(
            api.CreateSIPParticipantRequest(
                room_name=ctx.room.name,
                sip_trunk_id=trunk_id,
                sip_call_to=reminder.phone_number,
                sip_number=_env("LIVEKIT_SIP_NUMBER") or None,
                participant_identity=participant_identity,
                participant_name="Reminder recipient",
                wait_until_answered=True,
            )
        )
    except api.TwirpError as exc:
        print(
            "error creating SIP participant: "
            f"{exc.message}, SIP status: "
            f"{exc.metadata.get('sip_status_code')} {exc.metadata.get('sip_status')}"
        )
        raise
    return participant_identity


server = AgentServer()


@server.rtc_session(agent_name=_env("FARPLANE_PHONE_REMINDER_AGENT_NAME", "farplane-phone-chaser"))
async def phone_chaser(ctx: agents.JobContext) -> None:
    reminder = _dispatch_from_metadata(ctx.job.metadata)
    await ctx.connect()

    session = AgentSession(
        stt=_env("LIVEKIT_STT_MODEL", DEFAULT_STT_MODEL),
        llm=_env("LIVEKIT_LLM_MODEL", DEFAULT_LLM_MODEL),
        tts=_tts(),
        turn_handling=TurnHandlingOptions(
            turn_detection=_env("LIVEKIT_TURN_DETECTION", DEFAULT_TURN_DETECTION),
            endpointing={
                "mode": "fixed",
                "min_delay": _float_env(
                    "LIVEKIT_MIN_ENDPOINTING_DELAY",
                    DEFAULT_MIN_ENDPOINTING_DELAY,
                ),
                "max_delay": _float_env(
                    "LIVEKIT_MAX_ENDPOINTING_DELAY",
                    DEFAULT_MAX_ENDPOINTING_DELAY,
                ),
            },
            interruption={
                "mode": "adaptive",
                "min_duration": _float_env(
                    "LIVEKIT_MIN_INTERRUPTION_DURATION",
                    DEFAULT_MIN_INTERRUPTION_DURATION,
                ),
                "min_words": 0,
            },
            preemptive_generation={"preemptive_tts": True},
        ),
        user_away_timeout=15.0,
    )
    await session.start(room=ctx.room, agent=PhoneChaser(reminder))

    try:
        participant_identity = await _dial_phone(ctx, reminder)
        await ctx.wait_for_participant(identity=participant_identity)
        speech = session.say(reminder.message, allow_interruptions=True)
        await speech.wait_for_playout()
        await asyncio.sleep(_conversation_seconds())
    finally:
        session.shutdown(drain=True)
        ctx.shutdown()


if __name__ == "__main__":
    agents.cli.run_app(server)
