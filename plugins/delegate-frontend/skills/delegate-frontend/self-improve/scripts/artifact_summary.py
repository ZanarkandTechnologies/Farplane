#!/usr/bin/env python3
"""Build replayable delegate-frontend eval summaries from real artifacts."""

from __future__ import annotations

import argparse
import json
import re
import stat
from pathlib import Path
from typing import Any


PLACEHOLDER_HANDOFF_MARKERS = (
    "pending live external cli run",
    "- none reported yet",
    "status: pending",
    "observed output: pending",
)


HANDOFF_SECTION_PATTERNS = {
    "changed_files": re.compile(
        r"^(?:Changed Files|Changed\s*/\s*Produced Files|Produced Files)$",
        re.I,
    ),
    "verification": re.compile(
        r"^(?:Verification(?:\s+Commands\s*&\s*Results)?|Self-Review Findings|Output Contract Compliance)$",
        re.I,
    ),
    "first_write_evidence": re.compile(r"^(?:Wrapper\s+)?First-Write (?:Evidence|Proof)$", re.I),
    "risks": re.compile(r"^(?:Risks(?:\s*/\s*Followups)?|Findings\s*/\s*Risks)$", re.I),
}
REQUIRED_HANDOFF_SECTIONS = ("changed_files", "verification", "risks")


def read_json(path: Path) -> dict[str, Any]:
    try:
        value = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError):
        return {}
    return value if isinstance(value, dict) else {}


def read_int(path: Path) -> int | None:
    try:
        return int(path.read_text(encoding="utf-8").strip())
    except (OSError, ValueError):
        return None


def resolve_path(raw_path: str, project_root: Path, base_dir: Path) -> Path:
    path = Path(raw_path).expanduser()
    if path.is_absolute():
        return path
    root_candidate = (project_root / path).resolve(strict=False)
    if root_candidate.exists():
        return root_candidate
    return (base_dir / path).resolve(strict=False)


def is_relative_to_path(path: Path, parent: Path) -> bool:
    try:
        path.resolve(strict=False).relative_to(parent.resolve(strict=False))
    except ValueError:
        return False
    return True


def file_summary(path: Path) -> dict[str, Any]:
    try:
        path_stat = path.lstat()
    except OSError:
        return {"path": str(path), "exists": False, "kind": "missing", "size": 0}
    mode = path_stat.st_mode
    if stat.S_ISREG(mode):
        kind = "regular_file"
    elif stat.S_ISDIR(mode):
        kind = "directory"
    elif stat.S_ISLNK(mode):
        kind = "symlink"
    else:
        kind = "other"
    return {
        "path": str(path),
        "exists": True,
        "kind": kind,
        "size": path_stat.st_size,
    }


def summarize_handoff(path: Path) -> dict[str, Any]:
    try:
        text = path.read_text(encoding="utf-8")
    except OSError:
        return {
            "status": "missing",
            "path": str(path),
            "size": 0,
            "placeholder_markers": [],
            "sections": {name: False for name in HANDOFF_SECTION_PATTERNS},
        }
    lowered = text.lower()
    marker_hits = [marker for marker in PLACEHOLDER_HANDOFF_MARKERS if marker in lowered]
    section_bodies = markdown_sections(text)
    section_presence = {name: bool(section_bodies.get(name, "").strip()) for name in HANDOFF_SECTION_PATTERNS}
    has_required_sections = all(section_presence.get(name, False) for name in REQUIRED_HANDOFF_SECTIONS)
    if marker_hits:
        status_value = "placeholder"
    elif text.strip() and has_required_sections:
        status_value = "complete"
    else:
        status_value = "incomplete"
    return {
        "status": status_value,
        "path": str(path),
        "size": len(text.encode("utf-8")),
        "placeholder_markers": marker_hits,
        "sections": section_presence,
    }


def markdown_sections(text: str) -> dict[str, str]:
    matched: dict[str, list[str]] = {}
    current_name = ""
    for line in text.splitlines():
        heading = re.match(r"^#+\s+(.+?)\s*$", line.strip())
        if heading:
            current_name = ""
            title = heading.group(1).strip()
            for name, pattern in HANDOFF_SECTION_PATTERNS.items():
                if pattern.fullmatch(title):
                    current_name = name
                    matched.setdefault(name, [])
                    break
            continue
        if current_name:
            matched[current_name].append(line)
    return {name: "\n".join(lines).strip() for name, lines in matched.items()}


def summarize_startup(run_dir: Path) -> dict[str, Any]:
    session_info = read_json(run_dir / "session_files.json")
    session_files = session_info.get("session_files", [])
    if not isinstance(session_files, list):
        session_files = []
    exit_code = read_int(run_dir / "exit_code.txt")
    status = "ready" if session_files else "failed"
    failure_reason = ""
    if not session_files:
        failure_reason = "no_session_file"
    elif exit_code not in (None, 0):
        failure_reason = "process_failed"
    return {
        "status": status,
        "session_files": len(session_files),
        "exit_code": exit_code,
        "failure_reason": failure_reason,
    }


def summarize_phase_completion(
    run_dir: Path,
    project_root: Path,
    min_output_bytes: int = 1,
) -> dict[str, Any]:
    first_write = read_json(run_dir / "first_write.json")
    first_write_status = str(first_write.get("status", "missing"))
    raw_outputs = first_write.get("expected_outputs", [])
    expected_outputs = [str(item) for item in raw_outputs] if isinstance(raw_outputs, list) else []
    output_details = [
        file_summary(resolve_path(raw_path, project_root, run_dir))
        for raw_path in expected_outputs
    ]
    handoff_path = run_dir / "handoff.md"
    handoff = summarize_handoff(handoff_path)
    handoff_complete = handoff.get("status") == "complete"
    exit_code = read_int(run_dir / "exit_code.txt")
    has_owned_output = any(
        item.get("kind") == "regular_file" and int(item.get("size", 0)) >= min_output_bytes
        for item in output_details
    )
    if first_write_status != "pass":
        status_value = "failed"
    elif exit_code == 0 and handoff_complete and has_owned_output:
        status_value = "complete"
    else:
        status_value = "stub"
    return {
        "status": status_value,
        "owned_outputs": expected_outputs,
        "output_details": output_details,
        "handoff_path": str(handoff_path) if handoff_complete else "",
        "handoff_status": str(handoff.get("status", "missing")),
        "handoff_placeholder_markers": handoff.get("placeholder_markers", []),
        "handoff_contract": handoff.get("sections", {}),
        "first_write_status": first_write_status,
        "exit_code": exit_code,
    }


def alternatives_pattern(names: list[str]) -> str:
    ordered = sorted(names, key=len, reverse=True)
    return "|".join(re.escape(name) for name in ordered)


def section_value(markdown: str, names: list[str]) -> str:
    alternatives = alternatives_pattern(names)
    heading = re.search(
        rf"(?ims)^#+\s*(?:{alternatives})\s*$\n(?P<body>.*?)(?=^#+\s|\Z)",
        markdown,
    )
    if heading:
        for line in heading.group("body").splitlines():
            stripped = line.strip(" -:\t")
            if stripped:
                return stripped
    label = re.search(rf"(?im)^\s*(?:{alternatives})\s*:\s*(?P<value>.+)$", markdown)
    return label.group("value").strip() if label else ""


def clean_inline_value(value: str) -> str:
    cleaned = value.strip().strip("|").strip()
    if cleaned.startswith("`") and "`" in cleaned[1:]:
        return cleaned[1:].split("`", 1)[0].strip()
    return cleaned.strip("`").strip("*").strip()


def field_value(markdown: str, names: list[str]) -> str:
    alternatives = alternatives_pattern(names)
    table = re.search(
        rf"(?im)^\|\s*\*{{0,2}}(?:{alternatives})\*{{0,2}}\s*\|\s*(?P<value>[^|]+)\|",
        markdown,
    )
    if table:
        return clean_inline_value(table.group("value"))
    inline = re.search(
        rf"(?im)^\s*[-*]?\s*(?:"
        rf"\*\*(?:{alternatives})\s*:\*\*|"
        rf"\*\*(?:{alternatives})\*\*\s*:|"
        rf"(?:{alternatives})\s*:"
        rf")\s*(?P<value>.+)$",
        markdown,
    )
    if inline:
        return clean_inline_value(inline.group("value"))
    return clean_inline_value(section_value(markdown, names))


def has_heading(markdown: str, names: list[str]) -> bool:
    alternatives = alternatives_pattern(names)
    return bool(re.search(rf"(?im)^#+\s*(?:\d+\.\s*)?(?:{alternatives})\s*$", markdown))


def summarize_spec(spec_path: Path) -> dict[str, Any]:
    try:
        markdown = spec_path.read_text(encoding="utf-8")
    except OSError:
        return {"status": "missing"}
    list_sections = len(re.findall(r"(?im)^\s*[-*]\s*(?:section|beat)\b", markdown))
    table_sections = len(re.findall(r"(?m)^\|\s*\d+\s*\|", markdown))
    headed_beats = len(re.findall(r"(?im)^###\s+Beat\s+\d+\b", markdown))
    prompted_assets = len(re.findall(r"(?im)\bprompt\b\s*:", markdown))
    headed_assets = len(re.findall(r"(?im)^###\s+Asset\s+\d+\b", markdown))
    labeled_assets = len(re.findall(r"(?im)^\*\*A\d+\s+[—-]", markdown))
    qa_plan = field_value(markdown, ["QA plan", "Visual QA plan"])
    if not qa_plan and has_heading(markdown, ["QA Plan", "Visual QA plan"]):
        qa_plan = "QA Plan section present"
    summary = {
        "offer": field_value(markdown, ["Offer"]),
        "audience": field_value(markdown, ["Audience"]),
        "carrier_world": field_value(markdown, ["Carrier object / world", "Carrier world", "Carrier object"]),
        "recipe_id": field_value(markdown, ["Recipe route", "Recipe ID", "recipe_id", "Recipe"]),
        "taste_profile_id": field_value(markdown, ["Taste Profile ID", "taste_profile_id", "Taste profile"]),
        "effect_stack_id": field_value(markdown, ["Effect Stack ID", "effect_stack_id", "Effect stack"]),
        "qa_plan": qa_plan,
        "asset_prompts": max(prompted_assets, headed_assets, labeled_assets),
        "sections": max(list_sections, table_sections, headed_beats),
        "motion_checkpoints": len(re.findall(r"(?im)\b(?:0|25|50|75|95)%", markdown)),
    }
    complete = (
        all(str(summary[key]).strip() for key in ("offer", "audience", "carrier_world", "recipe_id", "taste_profile_id", "effect_stack_id", "qa_plan"))
        and summary["asset_prompts"] >= 4
        and summary["sections"] >= 5
        and summary["motion_checkpoints"] >= 5
    )
    summary["status"] = "complete" if complete else "stub"
    return summary


def summarize_asset_manifest(manifest_path: Path, project_root: Path) -> dict[str, Any]:
    manifest = read_json(manifest_path)
    if not manifest:
        return {"asset_strategy": "missing", "assets": [], "generated_or_rendered_count": 0, "broken_refs": 1}
    assets = manifest.get("assets", [])
    if not isinstance(assets, list):
        assets = []
    strategy = str(manifest.get("asset_strategy") or manifest.get("strategy") or "")
    generated_count = 0
    source_prompt_count = 0
    broken_refs = 0
    unsafe_refs = 0
    for asset in assets:
        if not isinstance(asset, dict):
            continue
        kind = str(asset.get("kind", ""))
        role = str(asset.get("role", ""))
        source_prompt = str(asset.get("source_prompt", "") or asset.get("prompt", ""))
        if source_prompt:
            source_prompt_count += 1
        if source_prompt or re.search(r"generated|rendered|frame|video", f"{kind} {role}", re.I):
            generated_count += 1
        raw_path = str(asset.get("path", ""))
        if raw_path and not re.match(r"^https?://", raw_path):
            resolved = resolve_path(raw_path, project_root, manifest_path.parent)
            if not is_relative_to_path(resolved, project_root):
                unsafe_refs += 1
            if not resolved.exists():
                broken_refs += 1
    joined = " ".join(
        f"{asset.get('path', '')} {asset.get('kind', '')} {asset.get('role', '')}"
        for asset in assets
        if isinstance(asset, dict)
    ).lower()
    return {
        "asset_strategy": strategy,
        "assets": assets,
        "generated_or_rendered_count": generated_count,
        "broken_refs": broken_refs,
        "unsafe_refs": unsafe_refs,
        "has_mobile_fallback": bool(manifest.get("has_mobile_fallback")) or "mobile" in joined,
        "has_reduced_motion_fallback": bool(manifest.get("has_reduced_motion_fallback")) or "reduced" in joined or "poster" in joined,
        "source_prompt_count": source_prompt_count,
    }


def summarize_scroll_qa(qa_path: Path) -> dict[str, Any]:
    qa = read_json(qa_path)
    geometry = qa.get("visualGeometry") or qa.get("visual_geometry") or {}
    return geometry if isinstance(geometry, dict) else {}


def build_summary(args: argparse.Namespace) -> dict[str, Any]:
    project_root = Path(args.project_root).resolve()
    payload: dict[str, Any] = {"id": args.id, "output": args.output}
    if args.run_dir:
        run_dir = Path(args.run_dir).resolve()
        payload["startup"] = summarize_startup(run_dir)
        payload["phase_completion"] = summarize_phase_completion(
            run_dir,
            project_root,
            min_output_bytes=args.min_output_bytes,
        )
        first_write = read_json(run_dir / "first_write.json")
        if first_write:
            payload["first_write"] = first_write
    if args.spec:
        payload["spec"] = summarize_spec(Path(args.spec).resolve())
    if args.asset_manifest:
        payload["asset_manifest"] = summarize_asset_manifest(Path(args.asset_manifest).resolve(), project_root)
    if args.scroll_qa:
        payload["visual_geometry"] = summarize_scroll_qa(Path(args.scroll_qa).resolve())
    return payload


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--id", required=True)
    parser.add_argument("--output", default="")
    parser.add_argument("--project-root", default=str(Path(__file__).resolve().parents[4]))
    parser.add_argument("--run-dir", default="")
    parser.add_argument("--spec", default="")
    parser.add_argument("--asset-manifest", default="")
    parser.add_argument("--scroll-qa", default="")
    parser.add_argument("--min-output-bytes", type=int, default=1)
    return parser.parse_args()


def main() -> int:
    payload = build_summary(parse_args())
    print(json.dumps(payload, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
