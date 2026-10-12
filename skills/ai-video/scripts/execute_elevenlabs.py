#!/usr/bin/env python3
"""Execute one validated ElevenLabs audio packet and write a sanitized receipt."""

from __future__ import annotations

import argparse
import hashlib
import json
import os
import subprocess
import sys
import urllib.error
import urllib.parse
import urllib.request
from pathlib import Path
from typing import Any, Callable

from validate_audio_packet import validate_path


API_ROOT = "https://api.elevenlabs.io"
SAFE_RESPONSE_HEADERS = ("request-id", "character-cost", "song-id")


def default_output_format(kind: str) -> str:
    return "mp3_48000_192" if kind == "music" else "mp3_44100_128"


def sha256_path(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def resolve_path(raw: str) -> Path:
    path = Path(raw).expanduser()
    if not path.is_absolute():
        path = Path.cwd() / path
    return path.resolve()


def build_request(packet: dict[str, Any], api_key: str) -> urllib.request.Request:
    parameters = packet["parameters"]
    kind = packet["kind"]
    output_format = parameters.get("output_format", default_output_format(kind))
    if kind == "voice":
        voice_id = parameters.get("public_voice_id")
        if not isinstance(voice_id, str) or not voice_id:
            raise ValueError("voice packet requires parameters.public_voice_id")
        encoded_voice_id = urllib.parse.quote(voice_id, safe="")
        url = (
            f"{API_ROOT}/v1/text-to-speech/{encoded_voice_id}"
            f"?output_format={urllib.parse.quote(output_format, safe='')}"
        )
        body = {
            "text": packet["prompt_or_script"],
            "model_id": parameters["model"],
            "voice_settings": parameters.get("voice_settings", {}),
        }
    elif kind == "sfx":
        url = (
            f"{API_ROOT}/v1/sound-generation"
            f"?output_format={urllib.parse.quote(output_format, safe='')}"
        )
        body = {
            "text": packet["prompt_or_script"],
            "model_id": parameters["model"],
            "duration_seconds": parameters["duration_seconds"],
            "prompt_influence": parameters.get("prompt_influence", 0.3),
            "loop": parameters.get("loop", False),
        }
    elif kind == "music":
        url = (
            f"{API_ROOT}/v1/music"
            f"?output_format={urllib.parse.quote(output_format, safe='')}"
        )
        duration_seconds = parameters.get(
            "duration_seconds", packet["timing"]["duration_seconds"]
        )
        body = {
            "prompt": packet["prompt_or_script"],
            "music_length_ms": round(float(duration_seconds) * 1000),
            "model_id": parameters["model"],
            "force_instrumental": parameters.get("force_instrumental", False),
        }
    else:
        raise ValueError(f"ElevenLabs executor does not support kind {kind!r}")
    return urllib.request.Request(
        url,
        data=json.dumps(body).encode("utf-8"),
        headers={
            "xi-api-key": api_key,
            "Content-Type": "application/json",
            "Accept": "audio/mpeg",
        },
        method="POST",
    )


def probe_audio(path: Path) -> dict[str, Any]:
    completed = subprocess.run(
        [
            "ffprobe",
            "-v",
            "error",
            "-show_entries",
            "format=format_name,duration:stream=codec_type,sample_rate,channels",
            "-of",
            "json",
            str(path),
        ],
        check=True,
        capture_output=True,
        text=True,
    )
    payload = json.loads(completed.stdout)
    audio_streams = [
        stream
        for stream in payload.get("streams", [])
        if stream.get("codec_type") == "audio"
    ]
    if not audio_streams:
        raise ValueError("generated artifact has no audio stream")
    stream = audio_streams[0]
    return {
        "format_name": payload["format"]["format_name"],
        "duration_seconds": float(payload["format"]["duration"]),
        "sample_rate": int(stream["sample_rate"]),
        "channels": int(stream["channels"]),
    }


def acceptance(packet: dict[str, Any], observed: dict[str, Any]) -> dict[str, Any]:
    duration = observed["duration_seconds"]
    target = float(packet["timing"]["duration_seconds"])
    if packet["kind"] == "voice":
        duration_pass = target - 0.5 <= duration <= target
    else:
        duration_pass = 0 < duration <= target + 0.35
    return {
        "duration_target_seconds": target,
        "duration_delta_seconds": round(duration - target, 3),
        "duration_pass": duration_pass,
        "manual_creative_review_pending": True,
        "accepted": False,
    }


def execute(
    packet_path: Path,
    receipt_path: Path,
    api_key: str,
    opener: Callable[..., Any] = urllib.request.urlopen,
) -> dict[str, Any]:
    packet = json.loads(packet_path.read_text())
    request = build_request(packet, api_key)
    try:
        with opener(request, timeout=180) as response:
            audio_bytes = response.read()
            safe_headers = {
                key: response.headers.get(key)
                for key in SAFE_RESPONSE_HEADERS
                if response.headers.get(key) is not None
            }
            response_status = getattr(response, "status", 200)
    except urllib.error.HTTPError as exc:
        body = exc.read().decode("utf-8", errors="replace")[:1000]
        raise RuntimeError(f"ElevenLabs HTTP {exc.code}: {body}") from exc
    if not audio_bytes:
        raise RuntimeError("ElevenLabs returned an empty audio artifact")

    output_path = resolve_path(packet["output"]["path"])
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_bytes(audio_bytes)
    observed = probe_audio(output_path)
    result = {
        "schema": "farplane-audio-execution-receipt-v1",
        "provider": "elevenlabs",
        "kind": packet["kind"],
        "capability": packet["capability"],
        "model": packet["parameters"]["model"],
        "public_voice_alias": (
            packet["parameters"].get("public_voice_alias")
            if packet["kind"] == "voice"
            else None
        ),
        "packet_path": str(packet_path.resolve()),
        "packet_sha256": sha256_path(packet_path),
        "artifact_path": str(output_path),
        "artifact_sha256": sha256_path(output_path),
        "artifact_bytes": len(audio_bytes),
        "observed": observed,
        "response": {"status": response_status, "safe_headers": safe_headers},
        "acceptance": acceptance(packet, observed),
        "credential_recorded": False,
    }
    receipt_path.parent.mkdir(parents=True, exist_ok=True)
    receipt_path.write_text(json.dumps(result, indent=2) + "\n")
    return result


def dry_run(packet_path: Path) -> dict[str, Any]:
    packet = json.loads(packet_path.read_text())
    parameters = packet["parameters"]
    return {
        "execution_mode": "dry_run",
        "provider": "elevenlabs",
        "kind": packet["kind"],
        "model": parameters["model"],
        "output_format": parameters.get("output_format", default_output_format(packet["kind"])),
        "output_path": str(resolve_path(packet["output"]["path"])),
        "credential_present": bool(os.environ.get("ELEVENLABS_API_KEY")),
        "external_call_made": False,
    }


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("packet", type=Path)
    parser.add_argument("--receipt", type=Path)
    parser.add_argument("--dry-run", action="store_true")
    args = parser.parse_args()

    errors = validate_path(args.packet)
    if errors:
        print("\n".join(errors), file=sys.stderr)
        return 1
    packet = json.loads(args.packet.read_text())
    if packet.get("provider") != "elevenlabs":
        print("packet provider must be elevenlabs", file=sys.stderr)
        return 1
    if args.dry_run:
        print(json.dumps(dry_run(args.packet), indent=2))
        return 0
    if packet.get("execution_mode") != "authorized_execution":
        print("packet is not authorized for execution", file=sys.stderr)
        return 1
    if not args.receipt:
        print("--receipt is required for authorized execution", file=sys.stderr)
        return 1
    api_key = os.environ.get("ELEVENLABS_API_KEY")
    if not api_key:
        print("ELEVENLABS_API_KEY is missing from the managed runtime", file=sys.stderr)
        return 1
    try:
        result = execute(args.packet, args.receipt, api_key)
    except (OSError, ValueError, RuntimeError, subprocess.CalledProcessError) as exc:
        print(str(exc), file=sys.stderr)
        return 1
    print(json.dumps(result, indent=2))
    return 0 if result["acceptance"]["duration_pass"] else 2


if __name__ == "__main__":
    raise SystemExit(main())
