#!/usr/bin/env python3
"""Executable boundary regressions for the TASK-0378 facet scorer."""

from __future__ import annotations

import hashlib
import json
import shutil
import subprocess
import tempfile
import unittest
from pathlib import Path


HERE = Path(__file__).resolve().parent
SCORER = HERE / "score_facets.py"
RUBRIC = HERE / "rubric.json"


def sha256_path(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


class FacetScorerBoundaryTests(unittest.TestCase):
    def setUp(self) -> None:
        if not shutil.which("ffmpeg") or not shutil.which("ffprobe"):
            self.skipTest("ffmpeg and ffprobe are required")
        self.temp = tempfile.TemporaryDirectory()
        self.root = Path(self.temp.name)
        self.rubric = json.loads(RUBRIC.read_text())
        self.full_video = self.root / "complete.mp4"
        self.probe_video = self.root / "probe.mp4"
        self._make_video(self.full_video, 47)
        self._make_video(self.probe_video, 4)
        self.evidence = {}
        for owner in sorted(
            set(self.rubric["facet_owners"].values())
            | set(self.rubric["hard_gate_owners"].values())
        ):
            path = self.root / f"{owner}.json"
            path.write_text(json.dumps({"owner": owner, "verdict": "PASS"}))
            self.evidence[owner] = path

    def tearDown(self) -> None:
        self.temp.cleanup()

    def _make_video(self, output: Path, duration: int) -> None:
        subprocess.run(
            [
                "ffmpeg",
                "-loglevel",
                "error",
                "-y",
                "-f",
                "lavfi",
                "-i",
                f"color=c=black:s=90x160:r=5:d={duration}",
                "-f",
                "lavfi",
                "-i",
                f"sine=frequency=440:sample_rate=8000:duration={duration}",
                "-shortest",
                "-c:v",
                "mpeg4",
                "-q:v",
                "31",
                "-c:a",
                "aac",
                "-b:a",
                "16k",
                str(output),
            ],
            check=True,
        )

    def _media_receipt(self, video: Path) -> Path:
        probe = subprocess.run(
            [
                "ffprobe",
                "-v",
                "error",
                "-show_entries",
                "format=duration",
                "-of",
                "json",
                str(video),
            ],
            check=True,
            capture_output=True,
            text=True,
        )
        duration = float(json.loads(probe.stdout)["format"]["duration"])
        path = self.root / f"{video.stem}-media-receipt.json"
        path.write_text(
            json.dumps(
                {
                    "artifact_kind": "full_video",
                    "artifact_path": str(video),
                    "artifact_sha256": sha256_path(video),
                    "container": "mov,mp4,m4a,3gp,3g2,mj2",
                    "duration_seconds": duration,
                    "width": 90,
                    "height": 160,
                    "aspect_ratio": "9:16",
                    "has_video": True,
                    "has_audio": True,
                }
            )
        )
        return path

    def _packet(self, video: Path | None = None) -> dict:
        video = video or self.full_video
        assertions = {}
        for facet, ids in self.rubric["facets"].items():
            owner = self.rubric["facet_owners"][facet]
            for assertion_id in ids:
                assertions[assertion_id] = {
                    "value": True,
                    "owner": owner,
                    "evidence_refs": [str(self.evidence[owner])],
                    "rationale": f"Independent {owner} fixture supports {assertion_id}.",
                }
        gates = {}
        for gate_id in self.rubric["pre_review_hard_gates"]:
            owner = self.rubric["hard_gate_owners"][gate_id]
            gates[gate_id] = {
                "value": True,
                "owner": owner,
                "evidence_refs": [str(self.evidence[owner])],
                "rationale": f"Independent {owner} fixture supports {gate_id}.",
            }
        return {
            "artifact": {
                "kind": "full_video",
                "path": str(video),
                "sha256": sha256_path(video),
                "media_receipt": str(self._media_receipt(video)),
            },
            "assertions": assertions,
            "hard_gates": gates,
        }

    def _write_packet(self, packet: dict, name: str = "scores.json") -> Path:
        path = self.root / name
        path.write_text(json.dumps(packet, indent=2))
        return path

    def _run(self, *args: str, expect_success: bool) -> subprocess.CompletedProcess[str]:
        result = subprocess.run(
            ["python3", str(SCORER), "--rubric", str(RUBRIC), *args],
            capture_output=True,
            text=True,
        )
        if expect_success and result.returncode != 0:
            self.fail(result.stderr or result.stdout)
        if not expect_success and result.returncode == 0:
            self.fail(f"expected scorer failure, received: {result.stdout}")
        return result

    def test_reference_layer_cannot_enter_pre_review(self) -> None:
        packet = self._packet()
        packet["artifact"] = {
            "kind": "reference_layer",
            "path": str(self.evidence["visual-qa"]),
        }
        result = self._run(
            "--scores", str(self._write_packet(packet)), "--mode", "pre_review",
            expect_success=False,
        )
        self.assertIn("artifact_kind_not_full_video", result.stderr)

    def test_probe_cannot_enter_pre_review(self) -> None:
        packet = self._packet(self.probe_video)
        result = self._run(
            "--scores", str(self._write_packet(packet)), "--mode", "pre_review",
            expect_success=False,
        )
        self.assertIn("artifact_duration_out_of_range", result.stderr)

    def test_missing_assertion_evidence_is_rejected(self) -> None:
        packet = self._packet()
        packet["assertions"]["story_1"]["evidence_refs"] = []
        result = self._run(
            "--scores", str(self._write_packet(packet)), "--mode", "pre_review",
            expect_success=False,
        )
        self.assertIn("missing_evidence_refs", result.stderr)

    def test_self_asserted_review_receipt_is_rejected(self) -> None:
        packet_path = self._write_packet(self._packet())
        pre_path = self.root / "pre-review.json"
        self._run(
            "--scores", str(packet_path), "--mode", "pre_review",
            "--output", str(pre_path), expect_success=True,
        )
        pre = json.loads(pre_path.read_text())
        review_path = self.root / "review.json"
        review_path.write_text(
            json.dumps(
                {
                    "review_type": "independent_completion_review",
                    "owner": "executor",
                    "tas": "TAS-A",
                    "verdict": "PASS",
                    "artifact_sha256": pre["artifact"]["sha256"],
                    "score_packet_sha256": pre["score_packet_sha256"],
                    "pre_review_receipt_sha256": sha256_path(pre_path),
                    "evidence_refs": [
                        {
                            "path": str(self.evidence["visual-qa"]),
                            "sha256": sha256_path(self.evidence["visual-qa"]),
                        }
                    ],
                }
            )
        )
        result = self._run(
            "--scores", str(packet_path), "--mode", "finalize",
            "--pre-review-receipt", str(pre_path),
            "--review-receipt", str(review_path), expect_success=False,
        )
        self.assertIn("invalid_independent_review_receipt", result.stderr)

    def test_complete_provenance_bundle_finalizes(self) -> None:
        packet_path = self._write_packet(self._packet())
        pre_path = self.root / "pre-review.json"
        pre_result = self._run(
            "--scores", str(packet_path), "--mode", "pre_review",
            "--output", str(pre_path), expect_success=True,
        )
        pre = json.loads(pre_result.stdout)
        self.assertTrue(pre["pre_review_pass"])
        self.assertFalse(pre["accepted"])
        review_evidence = self.root / "independent-review.md"
        review_evidence.write_text("PASS / TAS-A independent completion review\n")
        review_path = self.root / "review.json"
        review_path.write_text(
            json.dumps(
                {
                    "review_type": "independent_completion_review",
                    "owner": "reviewer",
                    "tas": "TAS-A",
                    "verdict": "PASS",
                    "artifact_sha256": pre["artifact"]["sha256"],
                    "score_packet_sha256": pre["score_packet_sha256"],
                    "pre_review_receipt_sha256": sha256_path(pre_path),
                    "evidence_refs": [
                        {
                            "path": str(review_evidence),
                            "sha256": sha256_path(review_evidence),
                        }
                    ],
                }
            )
        )
        final_result = self._run(
            "--scores", str(packet_path), "--mode", "finalize",
            "--pre-review-receipt", str(pre_path),
            "--review-receipt", str(review_path), expect_success=True,
        )
        final = json.loads(final_result.stdout)
        self.assertTrue(final["accepted"])
        self.assertEqual(final["phase"], "final")

    def test_post_review_evidence_mutation_is_rejected(self) -> None:
        packet_path = self._write_packet(self._packet())
        pre_path = self.root / "pre-review.json"
        pre_result = self._run(
            "--scores", str(packet_path), "--mode", "pre_review",
            "--output", str(pre_path), expect_success=True,
        )
        pre = json.loads(pre_result.stdout)
        review_evidence = self.root / "independent-review.md"
        review_evidence.write_text("PASS / TAS-A independent completion review\n")
        review_path = self.root / "review.json"
        review_path.write_text(
            json.dumps(
                {
                    "review_type": "independent_completion_review",
                    "owner": "reviewer",
                    "tas": "TAS-A",
                    "verdict": "PASS",
                    "artifact_sha256": pre["artifact"]["sha256"],
                    "score_packet_sha256": pre["score_packet_sha256"],
                    "pre_review_receipt_sha256": sha256_path(pre_path),
                    "evidence_refs": [
                        {
                            "path": str(review_evidence),
                            "sha256": sha256_path(review_evidence),
                        }
                    ],
                }
            )
        )
        self.evidence["visual-qa"].write_text(
            json.dumps({"owner": "visual-qa", "verdict": "MUTATED"})
        )
        result = self._run(
            "--scores", str(packet_path), "--mode", "finalize",
            "--pre-review-receipt", str(pre_path),
            "--review-receipt", str(review_path), expect_success=False,
        )
        self.assertIn("pre_review_receipt_stale_or_mutated", result.stderr)


if __name__ == "__main__":
    unittest.main(verbosity=2)
