#!/usr/bin/env python3
"""Provenance-bearing two-phase scorer for TASK-0378 full-video evidence."""

from __future__ import annotations

import argparse
import hashlib
import json
import subprocess
from pathlib import Path
from typing import Any


def fail(code: str, **details: Any) -> None:
    raise SystemExit(json.dumps({"error": code, **details}, indent=2))


def read_json(path: Path, label: str) -> dict[str, Any]:
    try:
        value = json.loads(path.read_text())
    except (OSError, json.JSONDecodeError) as exc:
        fail("invalid_json", label=label, path=str(path), reason=str(exc))
    if not isinstance(value, dict):
        fail("invalid_json_object", label=label, path=str(path))
    return value


def resolve_path(value: Any, label: str) -> Path:
    if not isinstance(value, str) or not value.strip():
        fail("invalid_path", label=label, value=value)
    path = Path(value).expanduser()
    if not path.is_absolute():
        path = Path.cwd() / path
    return path.resolve()


def sha256_path(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def canonical_sha256(value: dict[str, Any]) -> str:
    payload = json.dumps(value, sort_keys=True, separators=(",", ":")).encode()
    return hashlib.sha256(payload).hexdigest()


def probe_media(path: Path) -> dict[str, Any]:
    if not path.is_file():
        fail("missing_full_video", path=str(path))
    if path.suffix.lower() != ".mp4":
        fail("artifact_not_mp4", path=str(path))
    command = [
        "ffprobe",
        "-v",
        "error",
        "-show_entries",
        "format=format_name,duration:stream=codec_type,width,height",
        "-of",
        "json",
        str(path),
    ]
    try:
        completed = subprocess.run(
            command, check=True, capture_output=True, text=True
        )
        payload = json.loads(completed.stdout)
    except (FileNotFoundError, subprocess.CalledProcessError, json.JSONDecodeError) as exc:
        fail("artifact_media_probe_failed", path=str(path), reason=str(exc))

    streams = payload.get("streams", [])
    video_streams = [stream for stream in streams if stream.get("codec_type") == "video"]
    audio_streams = [stream for stream in streams if stream.get("codec_type") == "audio"]
    if not video_streams or not audio_streams:
        fail(
            "full_video_streams_missing",
            path=str(path),
            has_video=bool(video_streams),
            has_audio=bool(audio_streams),
        )
    video = video_streams[0]
    try:
        duration = float(payload["format"]["duration"])
        width = int(video["width"])
        height = int(video["height"])
    except (KeyError, TypeError, ValueError) as exc:
        fail("invalid_media_metadata", path=str(path), reason=str(exc))
    format_name = str(payload.get("format", {}).get("format_name", ""))
    if "mp4" not in format_name:
        fail("artifact_container_not_mp4", path=str(path), container=format_name)
    if not 45.0 <= duration <= 50.0:
        fail("artifact_duration_out_of_range", path=str(path), duration_seconds=duration)
    if width <= 0 or height <= 0 or abs((width / height) - (9 / 16)) > 0.002:
        fail(
            "artifact_aspect_ratio_not_9_16",
            path=str(path),
            width=width,
            height=height,
        )
    return {
        "container": format_name,
        "duration_seconds": duration,
        "width": width,
        "height": height,
        "aspect_ratio": "9:16",
        "has_video": True,
        "has_audio": True,
    }


def validate_media_receipt(
    receipt_path: Path,
    artifact_path: Path,
    artifact_sha256: str,
    observed: dict[str, Any],
) -> None:
    if not receipt_path.is_file():
        fail("missing_media_receipt", path=str(receipt_path))
    receipt = read_json(receipt_path, "media_receipt")
    receipt_artifact = resolve_path(receipt.get("artifact_path"), "media_receipt.artifact_path")
    expected = {
        "artifact_kind": "full_video",
        "artifact_sha256": artifact_sha256,
        "aspect_ratio": "9:16",
        "has_video": True,
        "has_audio": True,
    }
    mismatches: dict[str, Any] = {}
    if receipt_artifact != artifact_path:
        mismatches["artifact_path"] = {
            "expected": str(artifact_path),
            "observed": str(receipt_artifact),
        }
    for key, value in expected.items():
        if receipt.get(key) != value:
            mismatches[key] = {"expected": value, "observed": receipt.get(key)}
    for key in ("width", "height"):
        if receipt.get(key) != observed[key]:
            mismatches[key] = {"expected": observed[key], "observed": receipt.get(key)}
    try:
        receipt_duration = float(receipt.get("duration_seconds"))
    except (TypeError, ValueError):
        receipt_duration = -1.0
    if abs(receipt_duration - observed["duration_seconds"]) > 0.05:
        mismatches["duration_seconds"] = {
            "expected": observed["duration_seconds"],
            "observed": receipt.get("duration_seconds"),
        }
    if mismatches:
        fail("media_receipt_mismatch", path=str(receipt_path), mismatches=mismatches)


def validate_evidence_row(
    row: Any,
    row_id: str,
    expected_owner: str,
) -> dict[str, Any]:
    if not isinstance(row, dict):
        fail("invalid_evidence_row", row_id=row_id, reason="row must be an object")
    value = row.get("value")
    owner = row.get("owner")
    evidence_refs = row.get("evidence_refs")
    rationale = row.get("rationale")
    if not isinstance(value, bool):
        fail("invalid_evidence_value", row_id=row_id, value=value)
    if owner != expected_owner:
        fail(
            "invalid_evidence_owner",
            row_id=row_id,
            expected_owner=expected_owner,
            observed_owner=owner,
        )
    if not isinstance(rationale, str) or len(rationale.strip()) < 8:
        fail("missing_evidence_rationale", row_id=row_id)
    if not isinstance(evidence_refs, list) or not evidence_refs:
        fail("missing_evidence_refs", row_id=row_id)
    resolved_refs: list[dict[str, str]] = []
    for index, raw_ref in enumerate(evidence_refs):
        ref = resolve_path(raw_ref, f"{row_id}.evidence_refs[{index}]")
        if not ref.is_file():
            fail("missing_evidence_file", row_id=row_id, path=str(ref))
        resolved_refs.append({"path": str(ref), "sha256": sha256_path(ref)})
    return {
        "value": value,
        "owner": owner,
        "evidence_refs": resolved_refs,
        "rationale": rationale.strip(),
    }


def build_pre_review_result(
    rubric: dict[str, Any], submitted: dict[str, Any]
) -> dict[str, Any]:
    artifact = submitted.get("artifact")
    if not isinstance(artifact, dict):
        fail("invalid_artifact_contract", reason="artifact must be an object")
    if artifact.get("kind") != "full_video":
        fail(
            "artifact_kind_not_full_video",
            observed_kind=artifact.get("kind"),
        )
    artifact_path = resolve_path(artifact.get("path"), "artifact.path")
    observed = probe_media(artifact_path)
    artifact_sha256 = sha256_path(artifact_path)
    if artifact.get("sha256") != artifact_sha256:
        fail(
            "artifact_sha256_mismatch",
            expected=artifact_sha256,
            observed=artifact.get("sha256"),
        )
    media_receipt_path = resolve_path(
        artifact.get("media_receipt"), "artifact.media_receipt"
    )
    validate_media_receipt(
        media_receipt_path, artifact_path, artifact_sha256, observed
    )

    assertion_values = submitted.get("assertions")
    gate_values = submitted.get("hard_gates")
    if not isinstance(assertion_values, dict) or not isinstance(gate_values, dict):
        fail("invalid_score_packet", reason="assertions and hard_gates must be objects")

    expected_assertions = [
        assertion
        for assertions in rubric["facets"].values()
        for assertion in assertions
    ]
    expected_gates = rubric["pre_review_hard_gates"]
    missing_assertions = sorted(set(expected_assertions) - set(assertion_values))
    extra_assertions = sorted(set(assertion_values) - set(expected_assertions))
    missing_gates = sorted(set(expected_gates) - set(gate_values))
    extra_gates = sorted(set(gate_values) - set(expected_gates))
    if missing_assertions or extra_assertions or missing_gates or extra_gates:
        fail(
            "invalid_score_packet_keys",
            missing_assertions=missing_assertions,
            extra_assertions=extra_assertions,
            missing_gates=missing_gates,
            extra_gates=extra_gates,
        )

    normalized_assertions: dict[str, dict[str, Any]] = {}
    for facet, assertion_ids in rubric["facets"].items():
        owner = rubric["facet_owners"][facet]
        for assertion_id in assertion_ids:
            normalized_assertions[assertion_id] = validate_evidence_row(
                assertion_values[assertion_id], assertion_id, owner
            )

    normalized_gates: dict[str, dict[str, Any]] = {}
    for gate_id in expected_gates:
        normalized_gates[gate_id] = validate_evidence_row(
            gate_values[gate_id], gate_id, rubric["hard_gate_owners"][gate_id]
        )

    facets: dict[str, dict[str, Any]] = {}
    for facet, assertion_ids in rubric["facets"].items():
        passed = sum(normalized_assertions[item]["value"] for item in assertion_ids)
        score = passed / len(assertion_ids)
        facets[facet] = {
            "owner": rubric["facet_owners"][facet],
            "passed": passed,
            "total": len(assertion_ids),
            "score": score,
            "accepted": score >= rubric["per_facet_threshold"],
        }

    overall_passed = sum(
        normalized_assertions[item]["value"] for item in expected_assertions
    )
    overall = overall_passed / len(expected_assertions)
    hard_gates_pass = all(row["value"] for row in normalized_gates.values())
    pre_review_pass = (
        overall >= rubric["overall_threshold"]
        and all(item["accepted"] for item in facets.values())
        and hard_gates_pass
    )
    return {
        "schema": rubric["schema"],
        "phase": "pre_review",
        "artifact": {
            "kind": "full_video",
            "path": str(artifact_path),
            "sha256": artifact_sha256,
            "media_receipt": {
                "path": str(media_receipt_path),
                "sha256": sha256_path(media_receipt_path),
            },
            "observed": observed,
        },
        "score_packet_sha256": canonical_sha256(submitted),
        "facets": facets,
        "overall": {
            "passed": overall_passed,
            "total": len(expected_assertions),
            "score": overall,
        },
        "hard_gates": normalized_gates,
        "non_review_hard_gates_pass": hard_gates_pass,
        "pre_review_pass": pre_review_pass,
        "accepted": False,
        "acceptance_blocker": (
            "independent_completion_review_pending"
            if pre_review_pass
            else "facet_or_non_review_gate_failed"
        ),
    }


def build_final_result(
    rubric: dict[str, Any],
    submitted: dict[str, Any],
    pre_review_path: Path,
    review_path: Path,
) -> dict[str, Any]:
    current_pre = build_pre_review_result(rubric, submitted)
    saved_pre = read_json(pre_review_path, "pre_review_receipt")
    if saved_pre != current_pre:
        fail("pre_review_receipt_stale_or_mutated", path=str(pre_review_path))
    if not current_pre["pre_review_pass"]:
        fail("pre_review_not_passed", path=str(pre_review_path))
    pre_review_sha256 = sha256_path(pre_review_path)
    review = read_json(review_path, "independent_review_receipt")
    required_review = rubric["final_review_gate"]
    expected = {
        "review_type": "independent_completion_review",
        "owner": required_review["owner"],
        "tas": required_review["required_tas"],
        "verdict": "PASS",
        "artifact_sha256": current_pre["artifact"]["sha256"],
        "score_packet_sha256": current_pre["score_packet_sha256"],
        "pre_review_receipt_sha256": pre_review_sha256,
    }
    mismatches = {
        key: {"expected": value, "observed": review.get(key)}
        for key, value in expected.items()
        if review.get(key) != value
    }
    evidence_refs = review.get("evidence_refs")
    normalized_review_refs: list[dict[str, str]] = []
    if not isinstance(evidence_refs, list) or not evidence_refs:
        mismatches["evidence_refs"] = {
            "expected": "one or more existing independent review evidence files",
            "observed": evidence_refs,
        }
    else:
        for index, raw_ref in enumerate(evidence_refs):
            if not isinstance(raw_ref, dict):
                mismatches[f"evidence_refs[{index}]"] = {
                    "expected": "object with path and sha256",
                    "observed": raw_ref,
                }
                continue
            ref = resolve_path(raw_ref.get("path"), f"review.evidence_refs[{index}].path")
            if not ref.is_file():
                mismatches[f"evidence_refs[{index}]"] = {
                    "expected": "existing file",
                    "observed": str(ref),
                }
                continue
            observed_sha256 = sha256_path(ref)
            if raw_ref.get("sha256") != observed_sha256:
                mismatches[f"evidence_refs[{index}].sha256"] = {
                    "expected": observed_sha256,
                    "observed": raw_ref.get("sha256"),
                }
                continue
            normalized_review_refs.append(
                {"path": str(ref), "sha256": observed_sha256}
            )
    if mismatches:
        fail("invalid_independent_review_receipt", path=str(review_path), mismatches=mismatches)

    return {
        **current_pre,
        "phase": "final",
        "independent_completion_review": {
            "path": str(review_path.resolve()),
            "sha256": sha256_path(review_path),
            "owner": review["owner"],
            "tas": review["tas"],
            "verdict": review["verdict"],
            "evidence_refs": normalized_review_refs,
        },
        "accepted": True,
        "acceptance_blocker": None,
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--rubric", type=Path, required=True)
    parser.add_argument("--scores", type=Path, required=True)
    parser.add_argument("--mode", choices=("pre_review", "finalize"), required=True)
    parser.add_argument("--pre-review-receipt", type=Path)
    parser.add_argument("--review-receipt", type=Path)
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()

    rubric = read_json(args.rubric, "rubric")
    submitted = read_json(args.scores, "scores")
    if args.mode == "pre_review":
        if args.pre_review_receipt or args.review_receipt:
            fail("unexpected_finalize_argument_in_pre_review")
        result = build_pre_review_result(rubric, submitted)
    else:
        if not args.pre_review_receipt or not args.review_receipt:
            fail("missing_finalize_receipt")
        result = build_final_result(
            rubric, submitted, args.pre_review_receipt, args.review_receipt
        )

    rendered = json.dumps(result, indent=2) + "\n"
    if args.output:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(rendered)
    print(rendered, end="")


if __name__ == "__main__":
    main()
