#!/usr/bin/env python3
from __future__ import annotations

import json
import tempfile
import unittest
from pathlib import Path

import asset_evidence_lint


class AssetEvidenceLintTests(unittest.TestCase):
    def make_site(self, manifest: dict[str, object], files: dict[str, str] | None = None) -> Path:
        root = Path(tempfile.mkdtemp())
        (root / "assets").mkdir()
        for relative_path, contents in (files or {}).items():
            path = root / relative_path
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_text(contents, encoding="utf-8")
        (root / "assets" / "asset-manifest.json").write_text(
            json.dumps(manifest, indent=2),
            encoding="utf-8",
        )
        return root

    def test_generated_media_with_existing_fallback_passes(self) -> None:
        site = self.make_site(
            {
                "page": "premium cinematic medical landing",
                "qualityTarget": "premium",
                "assets": [
                    {
                        "id": "hero",
                        "type": "generated-video",
                        "path": "assets/hero.mp4",
                        "poster": "assets/hero-poster.webp",
                        "reducedMotionStill": "assets/hero-still.webp",
                        "videoModel": "google/veo-3-1",
                        "prompt": "doctor wearing XR glasses in procedure room",
                    }
                ],
            },
            {
                "assets/hero.mp4": "fake video bytes",
                "assets/hero-poster.webp": "fake image bytes",
                "assets/hero-still.webp": "fake image bytes",
            },
        )
        result = asset_evidence_lint.lint_site(site)
        self.assertEqual(result["verdict"], "PASS")
        self.assertEqual(result["primaryAssetCount"], 1)

    def test_product_photography_with_existing_files_passes(self) -> None:
        site = self.make_site(
            {
                "page": "premium medical XR product landing",
                "qualityTarget": "premium",
                "assets": [
                    {
                        "id": "product-photo-set",
                        "type": "product-photography",
                        "paths": ["assets/product.png", "assets/exploded.png"],
                        "poster": "assets/product.png",
                        "reducedMotionStill": "assets/exploded.png",
                        "tool": "product-photography image generation",
                    }
                ],
            },
            {
                "assets/product.png": "fake image bytes",
                "assets/exploded.png": "fake image bytes",
            },
        )
        result = asset_evidence_lint.lint_site(site)
        self.assertEqual(result["verdict"], "PASS")
        self.assertEqual(result["primaryAssetCount"], 1)

    def test_code_rendered_only_manifest_fails(self) -> None:
        site = self.make_site(
            {
                "page": "premium medical XR landing",
                "qualityTarget": "premium",
                "assets": [
                    {
                        "id": "hero-scroll-scrub-canvas",
                        "type": "code-rendered-canvas",
                        "source": "app.js canvas renderer",
                    },
                    {
                        "id": "field-of-view-overlay",
                        "type": "inline-svg",
                        "source": "index.html",
                    },
                ],
            }
        )
        result = asset_evidence_lint.lint_site(site)
        self.assertEqual(result["verdict"], "FAIL")
        self.assertTrue(
            any("hand-authored SVG section graphics are not allowed" in finding for finding in result["findings"])
        )

    def test_declared_generated_media_without_file_fails(self) -> None:
        site = self.make_site(
            {
                "page": "premium logistics landing",
                "qualityTarget": "premium",
                "assets": [
                    {
                        "id": "hero",
                        "type": "generated-image",
                        "path": "assets/missing.webp",
                        "poster": "assets/poster.webp",
                        "prompt": "warehouse computer vision command center",
                    }
                ],
            },
            {"assets/poster.webp": "fake image bytes"},
        )
        result = asset_evidence_lint.lint_site(site)
        self.assertEqual(result["verdict"], "FAIL")
        self.assertTrue(any("no existing workspace media path" in finding for finding in result["findings"]))

    def test_prototype_support_only_manifest_passes(self) -> None:
        site = self.make_site(
            {
                "page": "prototype medical XR landing",
                "qualityTarget": "prototype",
                "assets": [
                    {
                        "id": "hero-scroll-scrub-canvas",
                        "type": "code-rendered-canvas",
                        "source": "app.js canvas renderer",
                    }
                ],
            }
        )
        result = asset_evidence_lint.lint_site(site)
        self.assertEqual(result["verdict"], "PASS")

    def test_missing_fallback_file_fails(self) -> None:
        site = self.make_site(
            {
                "page": "premium cinematic landing",
                "qualityTarget": "premium",
                "assets": [
                    {
                        "id": "hero",
                        "type": "generated-video",
                        "path": "assets/hero.mp4",
                        "poster": "assets/missing-poster.webp",
                        "prompt": "surgical XR hero",
                    }
                ],
            },
            {"assets/hero.mp4": "fake video bytes"},
        )
        result = asset_evidence_lint.lint_site(site)
        self.assertEqual(result["verdict"], "FAIL")
        self.assertTrue(any("fallback path does not exist" in finding for finding in result["findings"]))

    def test_ffmpeg_still_sequence_does_not_count_as_generated_video(self) -> None:
        site = self.make_site(
            {
                "page": "premium cinematic XR product landing",
                "qualityTarget": "premium-cinematic",
                "assets": [
                    {
                        "id": "hero-scrub",
                        "type": "generated-video",
                        "role": "hero primary long scroll-scrub media",
                        "path": "assets/hero.mp4",
                        "poster": "assets/frame-00.png",
                        "reducedMotionStill": "assets/frame-04.png",
                        "prompt": "long hero scroll-scrub assembled from generated product teardown frames",
                        "tool": "ffmpeg all-keyframe MP4 transcode from generated image sequence",
                        "provenance": "created locally from generated Seedream still frames",
                    }
                ],
            },
            {
                "assets/hero.mp4": "fake video bytes",
                "assets/frame-00.png": "fake image bytes",
                "assets/frame-04.png": "fake image bytes",
            },
        )
        result = asset_evidence_lint.lint_site(site)
        self.assertEqual(result["verdict"], "FAIL")
        self.assertTrue(any("missing video-generation provenance" in finding for finding in result["findings"]))
        self.assertTrue(any("ffmpeg still-frame assembly" in finding for finding in result["findings"]))


if __name__ == "__main__":
    unittest.main()
