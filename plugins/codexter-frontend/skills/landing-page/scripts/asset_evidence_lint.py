#!/usr/bin/env python3
"""Validate generated or real media evidence for premium landing pages."""

from __future__ import annotations

import argparse
import glob
import json
import sys
from pathlib import Path
from typing import Any


PRIMARY_MEDIA_TYPES = {
    "generated-video",
    "generated-image",
    "generated-product-shot",
    "product-render",
    "product-photography",
    "assembly-video",
    "exploded-view-sequence",
    "frame-sequence",
    "source-video",
    "filmed-video",
    "photography",
    "real-product-image",
    "edited-image",
}

SUPPORT_ONLY_TYPES = {
    "code-rendered-canvas",
    "html-css-visual",
    "three-js",
    "webgl",
    "procedural",
}
FORBIDDEN_PREMIUM_GRAPHIC_TYPES = {"inline-svg", "custom-svg", "svg-illustration", "svg-diagram"}

PROVENANCE_KEYS = ("prompt", "sourcePrompt", "source", "model", "tool", "provenance", "captureSource")
FALLBACK_KEYS = ("poster", "posterPath", "reducedMotion", "reducedMotionStill", "fallback", "staticFallback")
VIDEO_PROVENANCE_KEYS = (
    "videoModel",
    "videoProvider",
    "videoGenerationTool",
    "sourceVideo",
    "sourceVideoPath",
    "sourceVideoModel",
)
VIDEO_MODEL_TERMS = (
    "veo",
    "runway",
    "kling",
    "luma",
    "dream machine",
    "pika",
    "sora",
    "wan",
    "hailuo",
    "seedance",
    "happyhorse",
    "p-video",
    "grok-imagine-video",
    "text-to-video",
    "image-to-video",
)
STILL_ASSEMBLY_TERMS = (
    "image sequence",
    "still sequence",
    "still frame",
    "still frames",
    "generated still",
    "generated image",
    "frame sequence",
    "product teardown frames",
    "seedream",
)


def as_list(value: Any) -> list[Any]:
    if value is None:
        return []
    if isinstance(value, list):
        return value
    return [value]


def load_manifest(site_dir: Path) -> tuple[Path, dict[str, Any], list[str]]:
    manifest_path = site_dir / "assets" / "asset-manifest.json"
    findings: list[str] = []
    if not manifest_path.exists():
        return manifest_path, {}, ["missing assets/asset-manifest.json"]
    try:
        data = json.loads(manifest_path.read_text(encoding="utf-8"))
    except json.JSONDecodeError as error:
        return manifest_path, {}, [f"asset manifest is invalid JSON: {error}"]
    if not isinstance(data, dict):
        findings.append("asset manifest root must be an object")
        data = {}
    return manifest_path, data, findings


def path_exists(site_dir: Path, raw_path: str) -> bool:
    if not raw_path or raw_path.startswith(("http://", "https://", "data:")):
        return False
    candidate = Path(raw_path)
    if not candidate.is_absolute():
        candidate = site_dir / candidate
    if candidate.exists():
        return True
    if any(char in raw_path for char in "*?["):
        pattern = str(candidate)
        return any(Path(match).exists() for match in glob.glob(pattern))
    return False


def primary_asset_paths(asset: dict[str, Any]) -> list[str]:
    raw_paths: list[str] = []
    for key in ("path", "paths", "src", "sourcePath"):
        for item in as_list(asset.get(key)):
            if isinstance(item, str):
                raw_paths.append(item)
    return raw_paths


def fallback_asset_paths(asset: dict[str, Any]) -> list[str]:
    raw_paths: list[str] = []
    for key in FALLBACK_KEYS:
        for item in as_list(asset.get(key)):
            if isinstance(item, str):
                raw_paths.append(item)
    return raw_paths


def has_provenance(asset: dict[str, Any]) -> bool:
    return any(str(asset.get(key, "")).strip() for key in PROVENANCE_KEYS)


def has_fallback(asset: dict[str, Any]) -> bool:
    return any(str(asset.get(key, "")).strip() for key in FALLBACK_KEYS)


def asset_text(asset: dict[str, Any]) -> str:
    values: list[str] = []
    for key in (
        "id",
        "type",
        "role",
        "prompt",
        "sourcePrompt",
        "source",
        "model",
        "tool",
        "provenance",
        "captureSource",
        *VIDEO_PROVENANCE_KEYS,
    ):
        value = asset.get(key)
        if isinstance(value, str):
            values.append(value)
    return " ".join(values).lower()


def has_video_generation_provenance(asset: dict[str, Any]) -> bool:
    if any(str(asset.get(key, "")).strip() for key in VIDEO_PROVENANCE_KEYS):
        return True
    text = asset_text(asset)
    return any(term in text for term in VIDEO_MODEL_TERMS)


def is_ffmpeg_still_assembly(asset: dict[str, Any]) -> bool:
    text = asset_text(asset)
    return "ffmpeg" in text and any(term in text for term in STILL_ASSEMBLY_TERMS)


def lint_site(site_dir: Path) -> dict[str, Any]:
    site_dir = site_dir.resolve()
    manifest_path, manifest, findings = load_manifest(site_dir)
    assets = manifest.get("assets", []) if isinstance(manifest, dict) else []
    if not isinstance(assets, list):
        assets = []
        findings.append("asset manifest field 'assets' must be a list")

    quality_text = " ".join(
        str(manifest.get(key, ""))
        for key in ("qualityTarget", "quality_target", "landingType", "landing_type", "page")
    ).lower()
    is_prototype = "prototype" in quality_text
    requires_primary_media = not is_prototype and any(
        term in quality_text for term in ("premium", "cinematic", "terminal")
    )
    if not requires_primary_media and not is_prototype:
        # Default to strict because this script should only be called for asset-heavy landing QA.
        requires_primary_media = True

    primary_assets: list[dict[str, Any]] = []
    support_only_assets = 0
    for index, asset in enumerate(assets):
        if not isinstance(asset, dict):
            findings.append(f"asset {index} must be an object")
            continue
        asset_type = str(asset.get("type", "")).strip()
        if requires_primary_media and asset_type in FORBIDDEN_PREMIUM_GRAPHIC_TYPES:
            findings.append(
                f"asset {asset.get('id', index)} invalid: hand-authored SVG section graphics are not allowed for premium landing pages"
            )
        if asset_type in SUPPORT_ONLY_TYPES:
            support_only_assets += 1
        if asset_type not in PRIMARY_MEDIA_TYPES:
            continue
        paths = primary_asset_paths(asset)
        existing_paths = [raw_path for raw_path in paths if path_exists(site_dir, raw_path)]
        fallback_paths = fallback_asset_paths(asset)
        existing_fallbacks = [raw_path for raw_path in fallback_paths if path_exists(site_dir, raw_path)]
        asset_findings: list[str] = []
        if not existing_paths:
            asset_findings.append("no existing workspace media path")
        if not has_provenance(asset):
            asset_findings.append("missing generation or real-asset provenance")
        if not has_fallback(asset):
            asset_findings.append("missing poster or reduced-motion fallback")
        elif fallback_paths and not existing_fallbacks:
            asset_findings.append("fallback path does not exist")
        if asset_type == "generated-video":
            if not has_video_generation_provenance(asset):
                asset_findings.append("missing video-generation provenance")
            if is_ffmpeg_still_assembly(asset):
                asset_findings.append(
                    "ffmpeg still-frame assembly must be declared as frame-sequence/prototype, not generated-video"
                )
        if asset_findings:
            findings.append(f"primary asset {asset.get('id', index)} invalid: {', '.join(asset_findings)}")
        else:
            primary_assets.append(asset)

    if requires_primary_media and not primary_assets:
        findings.append(
            "premium asset evidence requires at least one generated or real filesystem-backed primary media asset"
        )
    if requires_primary_media and assets and support_only_assets == len(assets):
        findings.append("manifest contains only code-native/support visuals")

    return {
        "siteDir": str(site_dir),
        "manifest": str(manifest_path),
        "verdict": "PASS" if not findings else "FAIL",
        "findings": findings,
        "primaryAssetCount": len(primary_assets),
        "assetCount": len(assets),
    }


def main(argv: list[str]) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("site_dir", type=Path)
    parser.add_argument("--json", action="store_true")
    args = parser.parse_args(argv)

    result = lint_site(args.site_dir)
    if args.json:
        print(json.dumps(result, indent=2))
    else:
        print(f"{result['verdict']} {result['siteDir']}")
        for finding in result["findings"]:
            print(f"- {finding}")
    return 0 if result["verdict"] == "PASS" else 1


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
