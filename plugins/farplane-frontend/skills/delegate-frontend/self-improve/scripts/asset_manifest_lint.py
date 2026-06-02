#!/usr/bin/env python3
"""Lint generated-media asset manifests before implementation starts."""

from __future__ import annotations

import argparse
import json
import re
import stat
from pathlib import Path
from typing import Any

import artifact_summary


BLOCKED_STRATEGIES = {
    "",
    "missing",
    "none",
    "placeholder",
    "code-native-canvas",
    "css-only",
}

GENERATED_KIND_RE = re.compile(r"generated|rendered|frame|image|video", re.I)
FRAME_OR_VIDEO_RE = re.compile(r"frame|video|sequence|scrub", re.I)
ROLE_GROUPS = {
    "hero_desktop": re.compile(r"hero|desktop|primary", re.I),
    "mobile": re.compile(r"mobile|phone|portrait", re.I),
    "reduced_motion": re.compile(r"reduced|poster|fallback", re.I),
    "support": re.compile(r"support|detail|dock|proof|secondary", re.I),
}
MEDIA_EXTENSIONS = {".avif", ".gif", ".jpg", ".jpeg", ".mp4", ".png", ".webm", ".webp"}


def load_manifest(path: Path) -> dict[str, Any]:
    try:
        value = json.loads(path.read_text(encoding="utf-8"))
    except OSError as exc:
        raise SystemExit(f"unable to read asset manifest {path}: {exc}") from exc
    except json.JSONDecodeError as exc:
        raise SystemExit(f"invalid asset manifest JSON {path}: {exc}") from exc
    if not isinstance(value, dict):
        raise SystemExit(f"invalid asset manifest {path}: expected a JSON object")
    return value


def local_asset_summary(
    *,
    asset: dict[str, Any],
    manifest_path: Path,
    project_root: Path,
    allow_remote: bool,
) -> tuple[list[str], dict[str, Any]]:
    errors: list[str] = []
    raw_path = str(asset.get("path", "")).strip()
    path_info: dict[str, Any] = {"path": raw_path, "kind": "missing", "size": 0}
    if not raw_path:
        errors.append("asset is missing path")
        return errors, path_info
    if re.match(r"^https?://", raw_path):
        if not allow_remote:
            errors.append(f"{raw_path}: remote asset paths are not implementation-ready")
        path_info = {"path": raw_path, "kind": "remote", "size": 0}
        return errors, path_info
    resolved = artifact_summary.resolve_path(raw_path, project_root, manifest_path.parent)
    path_info = artifact_summary.file_summary(resolved)
    if not artifact_summary.is_relative_to_path(resolved, project_root):
        errors.append(f"{raw_path}: referenced file escapes the declared asset project root")
    if not resolved.exists():
        errors.append(f"{raw_path}: referenced file does not exist")
        return errors, path_info
    try:
        mode = resolved.lstat().st_mode
    except OSError:
        errors.append(f"{raw_path}: unable to stat referenced file")
        return errors, path_info
    if stat.S_ISLNK(mode):
        errors.append(f"{raw_path}: referenced file is a symlink")
    elif not stat.S_ISREG(mode):
        errors.append(f"{raw_path}: referenced path is not a regular file")
    elif resolved.stat().st_size <= 0:
        errors.append(f"{raw_path}: referenced file is empty")
    elif resolved.suffix.lower() in MEDIA_EXTENSIONS and not has_media_signature(resolved):
        errors.append(f"{raw_path}: referenced media file does not have a recognized media signature")
    return errors, path_info


def has_media_signature(path: Path) -> bool:
    try:
        data = path.read_bytes()[:32]
    except OSError:
        return False
    suffix = path.suffix.lower()
    if suffix == ".webp":
        return data.startswith(b"RIFF") and data[8:12] == b"WEBP"
    if suffix == ".png":
        return data.startswith(b"\x89PNG\r\n\x1a\n")
    if suffix in {".jpg", ".jpeg"}:
        return data.startswith(b"\xff\xd8\xff")
    if suffix == ".gif":
        return data.startswith((b"GIF87a", b"GIF89a"))
    if suffix == ".mp4":
        return len(data) >= 12 and data[4:8] == b"ftyp"
    if suffix == ".webm":
        return data.startswith(b"\x1aE\xdf\xa3")
    if suffix == ".avif":
        return len(data) >= 12 and data[4:8] == b"ftyp" and b"avif" in data[:32]
    return True


def is_generated_asset(asset: dict[str, Any]) -> bool:
    text = " ".join(
        str(asset.get(key, ""))
        for key in ("kind", "role", "source_prompt", "prompt", "generator", "tool")
    )
    return bool(GENERATED_KIND_RE.search(text))


def role_text(asset: dict[str, Any]) -> str:
    return " ".join(str(asset.get(key, "")) for key in ("kind", "role", "path", "label", "id"))


def numeric_positive(value: Any) -> bool:
    try:
        return float(value) > 0
    except (TypeError, ValueError):
        return False


def lint_manifest(
    manifest_path: Path,
    project_root: Path,
    *,
    min_assets: int = 4,
    min_generated_assets: int = 4,
    allow_remote: bool = False,
) -> dict[str, Any]:
    manifest = load_manifest(manifest_path)
    summary = artifact_summary.summarize_asset_manifest(manifest_path, project_root)
    errors: list[str] = []
    warnings: list[str] = []
    strategy = str(summary.get("asset_strategy", ""))
    if strategy in BLOCKED_STRATEGIES:
        errors.append(f"asset_strategy `{strategy or 'missing'}` is not final-quality media")
    assets_value = manifest.get("assets", [])
    assets = assets_value if isinstance(assets_value, list) else []
    if not isinstance(assets_value, list):
        errors.append("assets must be a list")
    if len(assets) < min_assets:
        errors.append(f"asset count {len(assets)} is below required minimum {min_assets}")

    generated_assets = [asset for asset in assets if isinstance(asset, dict) and is_generated_asset(asset)]
    if len(generated_assets) < min_generated_assets:
        errors.append(
            f"generated/rendered asset count {len(generated_assets)} is below required minimum {min_generated_assets}"
        )
    source_prompt_count = 0
    path_summaries: list[dict[str, Any]] = []
    for index, asset in enumerate(assets, start=1):
        if not isinstance(asset, dict):
            errors.append(f"asset {index} is not an object")
            continue
        asset_errors, path_info = local_asset_summary(
            asset=asset,
            manifest_path=manifest_path,
            project_root=project_root,
            allow_remote=allow_remote,
        )
        path_summaries.append(path_info)
        errors.extend(asset_errors)
        source_prompt = str(asset.get("source_prompt", "") or asset.get("prompt", "")).strip()
        if is_generated_asset(asset) and not source_prompt:
            errors.append(f"asset {index} is generated/rendered but lacks source_prompt")
        if source_prompt:
            source_prompt_count += 1
        kind_text = str(asset.get("kind", ""))
        if GENERATED_KIND_RE.search(kind_text) and (
            not numeric_positive(asset.get("width")) or not numeric_positive(asset.get("height"))
        ):
            warnings.append(f"asset {index} should include positive width and height for deterministic layout")

    if int(summary.get("broken_refs", 0)) > 0:
        errors.append(f"broken refs detected: {summary.get('broken_refs')}")
    if int(summary.get("unsafe_refs", 0)) > 0:
        errors.append(f"unsafe refs detected: {summary.get('unsafe_refs')}")
    if not bool(summary.get("has_mobile_fallback")):
        errors.append("missing mobile fallback asset or manifest flag")
    if not bool(summary.get("has_reduced_motion_fallback")):
        errors.append("missing reduced-motion/poster fallback asset or manifest flag")
    if source_prompt_count < len(generated_assets):
        errors.append(
            f"source prompts {source_prompt_count} are below generated/rendered asset count {len(generated_assets)}"
        )
    if not any(FRAME_OR_VIDEO_RE.search(role_text(asset)) for asset in generated_assets):
        errors.append("no generated frame/video/sequence asset is available for scroll scrubbing")
    for group, pattern in ROLE_GROUPS.items():
        if not any(pattern.search(role_text(asset)) for asset in generated_assets):
            errors.append(f"missing generated asset role group: {group}")

    return {
        "passed": not errors,
        "manifest_path": str(manifest_path),
        "summary": summary,
        "errors": errors,
        "warnings": warnings,
        "path_summaries": path_summaries,
    }


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("manifest")
    parser.add_argument("--project-root", default=str(Path(__file__).resolve().parents[4]))
    parser.add_argument("--min-assets", type=int, default=4)
    parser.add_argument("--min-generated-assets", type=int, default=4)
    parser.add_argument("--allow-remote", action="store_true")
    parser.add_argument("--json", action="store_true")
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    result = lint_manifest(
        Path(args.manifest).resolve(),
        Path(args.project_root).resolve(),
        min_assets=args.min_assets,
        min_generated_assets=args.min_generated_assets,
        allow_remote=args.allow_remote,
    )
    if args.json:
        print(json.dumps(result, indent=2, sort_keys=True))
    else:
        status = "PASS" if result["passed"] else "FAIL"
        print(f"asset_manifest_lint={status}")
        for error in result["errors"]:
            print(f"ERROR: {error}")
        for warning in result["warnings"]:
            print(f"WARN: {warning}")
    return 0 if result["passed"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
