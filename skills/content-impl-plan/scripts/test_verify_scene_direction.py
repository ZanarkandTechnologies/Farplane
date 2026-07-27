#!/usr/bin/env python3
"""Regression tests for the mechanical constrained-variance verifier."""

from __future__ import annotations

import unittest
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
from verify_scene_direction import verify


def scene(scene_id: str, start: float, main: str, foreground: str) -> dict:
    return {
        "id": scene_id,
        "start_seconds": start,
        "end_seconds": start + 4.5,
        "state_change": "before -> after",
        "concepts": [
            {"id": f"{scene_id}-a", "relationship_type": "literal_evidence"},
            {"id": f"{scene_id}-b", "relationship_type": "causal_physical", "rejection_reason": "less direct"},
            {"id": f"{scene_id}-c", "relationship_type": "context_scale", "rejection_reason": "less causal"},
        ],
        "selected_concept_id": f"{scene_id}-a",
        "reveals": [
            {"kind": "introduce", "story_bearing": True},
            {"kind": "transform", "story_bearing": True},
        ],
        "main_topic": {"family_id": main},
        "foreground": {
            "family_id": foreground,
            "geometry_receipt": {
                "final_resolution": True,
                "visible_bbox_frame_ratio": 0.28,
                "visible_pixel_ratio": 0.18,
                "tight_alpha_bounds": True,
                "edge_contacts": ["bottom"],
                "semantic_relevance": True,
            },
        },
        "treatment_receipt": {
            "final_resolution": True,
            "background_clean": True,
            "subject_halftone": True,
            "crisp_alpha": True,
            "registration_restrained": True,
            "global_distress": False,
        },
        "readiness": "creative_lock_passed",
    }


class VerifySceneDirectionTest(unittest.TestCase):
    def test_valid_manifest_passes(self) -> None:
        result = verify({"scenes": [scene("S01", 0, "m1", "f1"), scene("S02", 4.5, "m2", "f2")]})
        self.assertTrue(result["pass"], result["failures"])
        self.assertEqual(result["judgment_required"][0], "specificity")

    def test_transparent_canvas_and_adjacent_reuse_fail(self) -> None:
        first = scene("S01", 0, "m1", "f1")
        second = scene("S02", 4.5, "m1", "f1")
        second["foreground"]["geometry_receipt"]["visible_bbox_frame_ratio"] = 0.04
        second["foreground"]["geometry_receipt"]["tight_alpha_bounds"] = False
        result = verify({"scenes": [first, second]})
        checks = {failure["check"] for failure in result["failures"]}
        self.assertFalse(result["pass"])
        self.assertIn("adjacent_variance", checks)
        self.assertIn("foreground_geometry", checks)

    def test_declared_transformed_motif_can_repeat(self) -> None:
        result = verify(
            {
                "intentional_motifs": [
                    {
                        "family_id": "source-page",
                        "causal_function": "state carrier",
                        "transformations": ["inspected", "compressed"],
                    }
                ],
                "scenes": [scene("S01", 0, "source-page", "f1"), scene("S02", 4.5, "source-page", "f2")],
            }
        )
        self.assertTrue(result["pass"], result["failures"])


if __name__ == "__main__":
    unittest.main()
