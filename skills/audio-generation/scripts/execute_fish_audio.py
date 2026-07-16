#!/usr/bin/env python3
"""Execute one validated Fish Audio voice packet and write a sanitized receipt."""

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


API_ROOT = "https://api.fish.audio"
REFERENCE_ENV = "FISH_AUDIO_REFERENCE_ID"
SAFE_RESPONSE_HEADERS = ("x-request-id", "traceparent", "content-type")


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


def require_runtime_reference(packet: dict[str, Any], reference_id: str) -> None:
    source = packet["parameters"].get("reference_id_source")
    if source != REFERENCE_ENV:
        raise ValueError(
            f"Fish voice packet requires parameters.reference_id_source={REFERENCE_ENV!r}"
        )
    if not reference_id:
        raise ValueError(f"{REFERENCE_ENV} is missing from the managed runtime")


def build_model_request(reference_id: str, api_key: str) -> urllib.request.Request:
    encoded_reference = urllib.parse.quote(reference_id, safe="")
    return urllib.request.Request(
        f"{API_ROOT}/model/{encoded_reference}",
        headers={"Authorization": f"Bearer {api_key}", "Accept": "application/json"},
        method="GET",
    )


def build_tts_request(
    packet: dict[str, Any], api_key: str, reference_id: str
) -> urllib.request.Request:
    parameters = packet["parameters"]
    allowed_body_fields = (
        "temperature",
        "top_p",
        "prosody",
        "chunk_length",
        "normalize",
        "format",
        "sample_rate",
        "mp3_bitrate",
        "latency",
        "max_new_tokens",
        "repetition_penalty",
        "min_chunk_length",
        "condition_on_previous_chunks",
        "early_stop_threshold",
        "features",
    )
    body: dict[str, Any] = {
        "text": packet["prompt_or_script"],
        "reference_id": reference_id,
    }
    body.update(
        {field: parameters[field] for field in allowed_body_fields if field in parameters}
    )
    return urllib.request.Request(
        f"{API_ROOT}/v1/tts",
        data=json.dumps(body).encode("utf-8"),
        headers={
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json",
            "Accept": "audio/mpeg",
            "model": parameters["model"],
        },
        method="POST",
    )


def public_voice_metadata(payload: dict[str, Any]) -> dict[str, Any]:
    visibility = payload.get("visibility")
    state = payload.get("state")
    voice_type = payload.get("type")
    if visibility != "public" or state != "trained" or voice_type != "tts":
        raise ValueError(
            "configured Fish voice must resolve to a public, trained TTS catalog voice"
        )
    safe_fields = ("visibility", "state", "type", "languages", "tags")
    return {field: payload.get(field) for field in safe_fields if payload.get(field) is not None}


def read_json_response(response: Any) -> dict[str, Any]:
    payload = json.loads(response.read().decode("utf-8"))
    if not isinstance(payload, dict):
        raise ValueError("Fish Audio model response was not an object")
    return payload


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
    duration_pass = target - 0.5 <= duration <= target
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
    reference_id: str,
    opener: Callable[..., Any] = urllib.request.urlopen,
) -> dict[str, Any]:
    packet = json.loads(packet_path.read_text())
    require_runtime_reference(packet, reference_id)
    try:
        with opener(build_model_request(reference_id, api_key), timeout=30) as response:
            voice = public_voice_metadata(read_json_response(response))
        with opener(
            build_tts_request(packet, api_key, reference_id), timeout=240
        ) as response:
            audio_bytes = response.read()
            safe_headers = {
                key: response.headers.get(key)
                for key in SAFE_RESPONSE_HEADERS
                if response.headers.get(key) is not None
            }
            response_status = getattr(response, "status", 200)
    except urllib.error.HTTPError as exc:
        body = exc.read().decode("utf-8", errors="replace")[:1000]
        raise RuntimeError(f"Fish Audio HTTP {exc.code}: {body}") from exc
    if not audio_bytes:
        raise RuntimeError("Fish Audio returned an empty audio artifact")

    output_path = resolve_path(packet["output"]["path"])
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_bytes(audio_bytes)
    observed = probe_audio(output_path)
    result = {
        "schema": "farplane-audio-execution-receipt-v1",
        "provider": "fish",
        "kind": "voice",
        "capability": packet["capability"],
        "model": packet["parameters"]["model"],
        "voice_source": "runtime_public_catalog_reference",
        "voice_metadata": voice,
        "packet_path": str(packet_path.resolve()),
        "packet_sha256": sha256_path(packet_path),
        "artifact_path": str(output_path),
        "artifact_sha256": sha256_path(output_path),
        "artifact_bytes": len(audio_bytes),
        "observed": observed,
        "response": {"status": response_status, "safe_headers": safe_headers},
        "metering": {
            "model_tier": "free_developer",
            "charged_usd": 0,
            "basis": "official s2.1-pro-free model contract",
        },
        "acceptance": acceptance(packet, observed),
        "private_reference_recorded": False,
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
        "provider": "fish",
        "kind": "voice",
        "model": parameters["model"],
        "output_format": parameters.get("format", "mp3"),
        "output_path": str(resolve_path(packet["output"]["path"])),
        "credential_present": bool(os.environ.get("FISH_API_KEY")),
        "runtime_reference_present": bool(os.environ.get(REFERENCE_ENV)),
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
    if packet.get("provider") != "fish" or packet.get("kind") != "voice":
        print("packet provider/kind must be fish/voice", file=sys.stderr)
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
    api_key = os.environ.get("FISH_API_KEY")
    reference_id = os.environ.get(REFERENCE_ENV, "")
    if not api_key:
        print("FISH_API_KEY is missing from the managed runtime", file=sys.stderr)
        return 1
    try:
        result = execute(args.packet, args.receipt, api_key, reference_id)
    except (OSError, ValueError, RuntimeError, subprocess.CalledProcessError) as exc:
        print(str(exc), file=sys.stderr)
        return 1
    print(json.dumps(result, indent=2))
    return 0 if result["acceptance"]["duration_pass"] else 2


if __name__ == "__main__":
    raise SystemExit(main())
