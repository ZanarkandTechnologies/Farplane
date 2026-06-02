from __future__ import annotations

import json
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parent
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

import asset_manifest_lint


def media_bytes(path: str) -> bytes:
    suffix = Path(path).suffix.lower()
    if suffix == ".webp":
        return b"RIFF0000WEBPVP8 fixture"
    if suffix == ".mp4":
        return b"\x00\x00\x00\x18ftypisomfixture"
    return b"fixture"


def write_fixture(root: Path, assets: list[dict[str, object]], strategy: str = "generated-frame-sequence") -> Path:
    assets_dir = root / "assets"
    assets_dir.mkdir(parents=True, exist_ok=True)
    for asset in assets:
        raw_path = str(asset.get("path", ""))
        if raw_path and not raw_path.startswith("http"):
            path = assets_dir / raw_path
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_bytes(media_bytes(raw_path))
    manifest = assets_dir / "asset-manifest.json"
    manifest.write_text(
        json.dumps(
            {
                "asset_strategy": strategy,
                "has_mobile_fallback": True,
                "has_reduced_motion_fallback": True,
                "assets": assets,
            }
        ),
        encoding="utf-8",
    )
    return manifest


class AssetManifestLintTests(unittest.TestCase):
    def test_accepts_generated_asset_manifest_with_required_roles(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            manifest = write_fixture(
                root,
                [
                    {
                        "path": "frames/hero-desktop-0001.webp",
                        "kind": "generated-frame",
                        "role": "desktop hero frame sequence",
                        "width": 1920,
                        "height": 1080,
                        "source_prompt": "desktop warehouse yard hero frame",
                    },
                    {
                        "path": "frames/hero-mobile-0001.webp",
                        "kind": "generated-frame",
                        "role": "mobile portrait hero frame sequence",
                        "width": 1080,
                        "height": 1440,
                        "source_prompt": "mobile warehouse yard hero frame",
                    },
                    {
                        "path": "poster/reduced-motion.webp",
                        "kind": "generated-image",
                        "role": "reduced motion poster fallback",
                        "width": 1920,
                        "height": 1080,
                        "source_prompt": "resolved yard poster",
                    },
                    {
                        "path": "loops/dock-support.webp",
                        "kind": "rendered-video",
                        "role": "support dock detail proof loop",
                        "width": 1280,
                        "height": 720,
                        "source_prompt": "dock computer vision support loop",
                    },
                ],
            )
            result = asset_manifest_lint.lint_manifest(manifest, root)
            self.assertTrue(result["passed"], result["errors"])

    def test_rejects_code_native_canvas_and_missing_media(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            manifest = write_fixture(root, [], strategy="code-native-canvas")
            result = asset_manifest_lint.lint_manifest(manifest, root)
            self.assertFalse(result["passed"])
            self.assertTrue(any("code-native-canvas" in error for error in result["errors"]))
            self.assertTrue(any("asset count" in error for error in result["errors"]))

    def test_rejects_remote_paths_by_default(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            manifest = write_fixture(
                root,
                [
                    {
                        "path": "https://example.com/hero.webp",
                        "kind": "generated-frame",
                        "role": "desktop hero mobile reduced support frame",
                        "width": 1920,
                        "height": 1080,
                        "source_prompt": "remote frame",
                    }
                ],
            )
            result = asset_manifest_lint.lint_manifest(manifest, root, min_assets=1, min_generated_assets=1)
            self.assertFalse(result["passed"])
            self.assertTrue(any("remote asset paths" in error for error in result["errors"]))

    def test_rejects_missing_source_prompt_for_generated_asset(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            manifest = write_fixture(
                root,
                [
                    {
                        "path": "frames/hero.webp",
                        "kind": "generated-frame",
                        "role": "desktop hero mobile reduced support frame",
                        "width": 1920,
                        "height": 1080,
                    }
                ],
            )
            result = asset_manifest_lint.lint_manifest(manifest, root, min_assets=1, min_generated_assets=1)
            self.assertFalse(result["passed"])
            self.assertTrue(any("lacks source_prompt" in error for error in result["errors"]))

    def test_rejects_fake_media_extension_without_signature(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            assets_dir = root / "assets"
            media = assets_dir / "frames" / "hero.webp"
            media.parent.mkdir(parents=True)
            media.write_bytes(b"plain text pretending to be webp")
            manifest = assets_dir / "asset-manifest.json"
            manifest.write_text(
                json.dumps(
                    {
                        "asset_strategy": "generated-frame-sequence",
                        "has_mobile_fallback": True,
                        "has_reduced_motion_fallback": True,
                        "assets": [
                            {
                                "path": "frames/hero.webp",
                                "kind": "generated-frame",
                                "role": "desktop hero mobile reduced support frame",
                                "width": 1920,
                                "height": 1080,
                                "source_prompt": "warehouse frame",
                            }
                        ],
                    }
                ),
                encoding="utf-8",
            )
            result = asset_manifest_lint.lint_manifest(manifest, root, min_assets=1, min_generated_assets=1)
            self.assertFalse(result["passed"])
            self.assertTrue(any("recognized media signature" in error for error in result["errors"]))

    def test_rejects_absolute_asset_path_outside_project_root(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            outside = root.parent / "outside-lint.webp"
            outside.write_bytes(media_bytes("outside.webp"))
            manifest = write_fixture(
                root,
                [
                    {
                        "path": str(outside),
                        "kind": "generated-frame",
                        "role": "desktop hero mobile reduced support frame",
                        "width": 1920,
                        "height": 1080,
                        "source_prompt": "escaped absolute frame",
                    }
                ],
            )
            result = asset_manifest_lint.lint_manifest(manifest, root, min_assets=1, min_generated_assets=1)
            self.assertFalse(result["passed"])
            self.assertTrue(any("escapes the declared asset project root" in error for error in result["errors"]))

    def test_rejects_relative_parent_escape_outside_project_root(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            assets_dir = root / "assets"
            assets_dir.mkdir()
            outside = root / "outside-relative.webp"
            outside.write_bytes(media_bytes("outside.webp"))
            manifest = assets_dir / "asset-manifest.json"
            manifest.write_text(
                json.dumps(
                    {
                        "asset_strategy": "generated-frame-sequence",
                        "has_mobile_fallback": True,
                        "has_reduced_motion_fallback": True,
                        "assets": [
                            {
                                "path": "../outside-relative.webp",
                                "kind": "generated-frame",
                                "role": "desktop hero mobile reduced support frame",
                                "width": 1920,
                                "height": 1080,
                                "source_prompt": "parent escape frame",
                            }
                        ],
                    }
                ),
                encoding="utf-8",
            )
            result = asset_manifest_lint.lint_manifest(
                manifest,
                assets_dir,
                min_assets=1,
                min_generated_assets=1,
            )
            self.assertFalse(result["passed"])
            self.assertTrue(any("escapes the declared asset project root" in error for error in result["errors"]))


if __name__ == "__main__":
    unittest.main()
