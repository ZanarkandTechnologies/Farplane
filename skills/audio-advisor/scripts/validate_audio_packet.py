#!/usr/bin/env python3
"""Validate audio-advisor provider packets, blockers, and secret redaction."""

from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path
from typing import Any
from urllib.parse import urlparse


CAPABILITIES = {
    "fish": {"voice"},
    "elevenlabs": {"voice", "music", "sfx"},
}
CAPABILITY_LABELS = {
    "voice": "text-to-speech",
    "music": "music",
    "sfx": "sound-effects",
}
BLOCKER_CODES = {
    "unsupported_provider_kind_pair": {"pair": "unsupported", "mode": "dry_run", "external_call": False},
    "missing_runtime_secret": {"pair": "supported", "mode": "authorized_execution", "external_call": False},
    "unresolved_voice_consent": {"pair": "supported_voice", "mode": "authorized_execution", "external_call": False},
    "missing_execution_authority": {"pair": "supported", "mode": "dry_run", "external_call": False},
    "brief_not_approved": {"pair": "supported", "mode": "dry_run", "external_call": False},
    "artifact_verification_failed": {"pair": "supported", "mode": "authorized_execution", "external_call": True},
}
FORBIDDEN_KEY_PARTS = {
    "access_key", "api_key", "auth", "authorization", "cookie",
    "credential", "password", "private_key", "secret", "session_cookie",
    "signing_key", "token",
}
SECRET_VALUE_PATTERNS = (
    re.compile(r"^Bearer\s+\S+", re.I),
    re.compile(r"-----BEGIN (?:RSA |EC |OPENSSH )?PRIVATE KEY-----"),
    re.compile(r"^(?:sk|api|token|secret)[-_][A-Za-z0-9_-]{12,}$", re.I),
    re.compile(r"^AKIA[A-Z0-9]{16}$"),
    re.compile(r"^gh[pousr]_[A-Za-z0-9]{20,}$"),
    re.compile(r"^xox[baprs]-[A-Za-z0-9-]{10,}$"),
)
SOURCE_RECEIPT_USES = {"personal", "noncommercial", "public", "client", "commercial"}
SOURCE_RIGHTS_STATUSES = {"personal_noncommercial_terms", "separately_cleared"}


def normalize(key: str) -> str:
    return key.lower().replace("-", "_")


def forbidden_key(key: str) -> bool:
    normalized = normalize(key)
    return normalized in FORBIDDEN_KEY_PARTS or any(
        normalized.endswith(f"_{part}") for part in FORBIDDEN_KEY_PARTS
    )


def secret_errors(value: Any, path: str = "packet") -> list[str]:
    errors: list[str] = []
    if isinstance(value, dict):
        for key, child in value.items():
            child_path = f"{path}.{key}"
            if forbidden_key(str(key)):
                errors.append(f"{child_path}: credential-bearing field is forbidden")
            else:
                errors.extend(secret_errors(child, child_path))
    elif isinstance(value, list):
        for index, child in enumerate(value):
            errors.extend(secret_errors(child, f"{path}[{index}]"))
    elif isinstance(value, str) and any(pattern.search(value) for pattern in SECRET_VALUE_PATTERNS):
        errors.append(f"{path}: value resembles a credential")
    return errors


def validate_source_receipt(payload: dict[str, Any]) -> list[str]:
    errors = secret_errors(payload, "source_receipt")
    required = {
        "result", "source", "item_title", "item_page_url", "retrieved_at",
        "original_filename", "saved_path", "sha256", "observed", "cue_ref", "retrieved_by",
        "intended_use", "rights_status", "rights_basis", "manual_audio_review",
        "residual_risk",
    }
    missing = sorted(key for key in required if key not in payload)
    if missing:
        errors.append(f"source_receipt: missing required fields: {', '.join(missing)}")
    if payload.get("source") != "soundbuttonsworld":
        errors.append("source_receipt.source: must be 'soundbuttonsworld'")
    if payload.get("retrieved_by") != "operator":
        errors.append("source_receipt.retrieved_by: must be 'operator'")
    page_url = payload.get("item_page_url")
    if not isinstance(page_url, str) or not page_url.strip():
        errors.append("source_receipt.item_page_url: non-empty URL required")
    else:
        parsed = urlparse(page_url)
        if parsed.scheme != "https" or parsed.hostname not in {
            "soundbuttonsworld.com", "www.soundbuttonsworld.com"
        } or not parsed.path.startswith("/sound-button/"):
            errors.append("source_receipt.item_page_url: must be an HTTPS SoundButtonsWorld item page")
    for field in (
        "item_title", "retrieved_at", "original_filename", "saved_path",
        "cue_ref", "rights_basis", "residual_risk",
    ):
        if not isinstance(payload.get(field), str) or not payload.get(field, "").strip():
            errors.append(f"source_receipt.{field}: non-empty string required")
    checksum = payload.get("sha256")
    if not isinstance(checksum, str) or re.fullmatch(r"[0-9a-f]{64}", checksum) is None:
        errors.append("source_receipt.sha256: lowercase 64-character SHA-256 required")
    observed = payload.get("observed")
    if not isinstance(observed, dict):
        errors.append("source_receipt.observed: object required")
    else:
        if observed.get("format") != "mp3":
            errors.append("source_receipt.observed.format: must be 'mp3'")
        duration = observed.get("duration_seconds")
        if not isinstance(duration, (int, float)) or isinstance(duration, bool) or duration <= 0:
            errors.append("source_receipt.observed.duration_seconds: positive number required")
    intended_use = payload.get("intended_use")
    if intended_use not in SOURCE_RECEIPT_USES:
        errors.append("source_receipt.intended_use: unknown usage scope")
    rights_status = payload.get("rights_status")
    if rights_status not in SOURCE_RIGHTS_STATUSES:
        errors.append("source_receipt.rights_status: must be personal_noncommercial_terms or separately_cleared")
    elif rights_status == "personal_noncommercial_terms" and intended_use not in {
        "personal", "noncommercial"
    }:
        errors.append("source_receipt: site terms cannot clear public, client, or commercial use")
    if payload.get("manual_audio_review") not in {"pass", "fail", "pending"}:
        errors.append("source_receipt.manual_audio_review: must be pass, fail, or pending")
    return errors


def validate_packet(payload: dict[str, Any]) -> list[str]:
    if payload.get("result") == "source_receipt":
        return validate_source_receipt(payload)
    errors = secret_errors(payload)
    kind = payload.get("kind")
    provider = payload.get("provider")

    if payload.get("result") == "blocked_report":
        required = {
            "result", "code", "kind", "provider", "requested_capability",
            "execution_mode", "brief_ref", "reason", "silent_provider_switch",
            "next_action", "external_call_made",
        }
        missing = sorted(key for key in required if key not in payload)
        if missing:
            errors.append(f"blocked_report: missing required fields: {', '.join(missing)}")
        if provider not in CAPABILITIES:
            errors.append(f"blocked_report.provider: unknown provider {provider!r}")
        if kind not in CAPABILITY_LABELS:
            errors.append(f"blocked_report.kind: unknown kind {kind!r}")
        pair_supported = provider in CAPABILITIES and kind in CAPABILITIES[provider]
        code = payload.get("code")
        rule = BLOCKER_CODES.get(str(code))
        if rule is None:
            errors.append(f"blocked_report.code: unknown blocker code {code!r}")
        elif rule["pair"] == "unsupported" and pair_supported:
            errors.append("blocked_report: unsupported-pair blocker requires an unsupported provider/kind pair")
        elif rule["pair"] in {"supported", "supported_voice"} and not pair_supported:
            errors.append("blocked_report: safety blocker requires a supported provider/kind pair")
        elif rule["pair"] == "supported_voice" and kind != "voice":
            errors.append("blocked_report: unresolved voice consent requires kind voice")
        if payload.get("requested_capability") != kind:
            errors.append("blocked_report.requested_capability: must match kind")
        if rule is not None and payload.get("execution_mode") != rule["mode"]:
            errors.append(f"blocked_report.execution_mode: must be {rule['mode']} for {code!r}")
        if not isinstance(payload.get("brief_ref"), str) or not payload.get("brief_ref", "").strip():
            errors.append("blocked_report.brief_ref: non-empty string required")
        if payload.get("silent_provider_switch") is not False:
            errors.append("blocked_report: silent_provider_switch must be false")
        if rule is not None and payload.get("external_call_made") is not rule["external_call"]:
            errors.append(
                "blocked_report.external_call_made: must be "
                f"{str(rule['external_call']).lower()} for {code!r}"
            )
        for field in ("reason", "next_action"):
            if not isinstance(payload.get(field), str) or not payload.get(field, "").strip():
                errors.append(f"blocked_report.{field}: non-empty string required")
        return errors

    required = {
        "kind", "provider", "capability", "execution_mode", "brief_ref",
        "prompt_or_script", "profile_ref", "parameters", "timing", "output", "rights_and_consent",
        "acceptance_checks", "secret_source",
    }
    missing = sorted(key for key in required if key not in payload)
    if missing:
        errors.append(f"packet: missing required fields: {', '.join(missing)}")
    if provider not in CAPABILITIES or kind not in CAPABILITIES.get(str(provider), set()):
        errors.append(f"packet: unsupported provider/kind pair {provider!r}/{kind!r}")
    if kind in CAPABILITY_LABELS and payload.get("capability") != CAPABILITY_LABELS[kind]:
        errors.append(f"packet.capability: must be {CAPABILITY_LABELS[kind]!r} for {kind!r}")
    if payload.get("execution_mode") not in {"dry_run", "authorized_execution"}:
        errors.append("packet.execution_mode: must be dry_run or authorized_execution")
    if payload.get("secret_source") != "runtime_environment_only":
        errors.append("packet.secret_source: must be runtime_environment_only")
    for field in ("brief_ref", "prompt_or_script"):
        if not isinstance(payload.get(field), str) or not payload.get(field, "").strip():
            errors.append(f"packet.{field}: non-empty string required")
    if payload.get("profile_ref") is not None and (
        not isinstance(payload.get("profile_ref"), str) or not payload.get("profile_ref", "").strip()
    ):
        errors.append("packet.profile_ref: must be null or a non-empty string")
    if not isinstance(payload.get("parameters"), dict) or not payload.get("parameters"):
        errors.append("packet.parameters: non-empty object required")
    timing = payload.get("timing")
    if not isinstance(timing, dict):
        errors.append("packet.timing: object required")
    else:
        duration = timing.get("duration_seconds")
        if not isinstance(duration, (int, float)) or isinstance(duration, bool) or duration <= 0:
            errors.append("packet.timing.duration_seconds: positive number required")
        if not isinstance(timing.get("cue_ref"), str) or not timing.get("cue_ref", "").strip():
            errors.append("packet.timing.cue_ref: non-empty string required")
    output = payload.get("output")
    if not isinstance(output, dict):
        errors.append("packet.output: object required")
    else:
        for field in ("owner", "path", "format"):
            if not isinstance(output.get(field), str) or not output.get(field, "").strip():
                errors.append(f"packet.output.{field}: non-empty string required")
    rights = payload.get("rights_and_consent")
    if not isinstance(rights, dict) or not rights:
        errors.append("packet.rights_and_consent: non-empty object required")
    elif not isinstance(rights.get("status"), str) or not rights.get("status", "").strip():
        errors.append("packet.rights_and_consent.status: non-empty string required")
    checks = payload.get("acceptance_checks")
    if not isinstance(checks, list) or not checks or any(
        not isinstance(check, str) or not check.strip() for check in checks
    ):
        errors.append("packet.acceptance_checks: non-empty string array required")
    return errors


def validate_path(path: Path) -> list[str]:
    try:
        payload = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, UnicodeError, json.JSONDecodeError) as exc:
        return [f"{path}: invalid JSON: {exc}"]
    if not isinstance(payload, dict):
        return [f"{path}: top-level JSON must be an object"]
    return [f"{path}: {error}" for error in validate_packet(payload)]


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("paths", nargs="+", type=Path)
    args = parser.parse_args()
    errors = [error for path in args.paths for error in validate_path(path)]
    if errors:
        print("\n".join(errors), file=sys.stderr)
        return 1
    print(f"audio packets OK: {len(args.paths)} file(s)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
