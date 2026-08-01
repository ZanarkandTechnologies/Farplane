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
            "texture_classification": "operator_requested_style",
            "raster_paper_asset_ref": "assets/paper-scan.jpg",
            "raster_paper_rights_ref": "proof/paper-license.txt",
            "page_or_object_coordinates": True,
            "full_frame_texture_proof_ref": "proof/full-frame.png",
            "close_crop_texture_proof_ref": "proof/close-crop.png",
            "final_resolution_halftone_scale": "6 px cell at 1080x1920",
            "subject_mask_final_resolution_proof_ref": "proof/subject-mask.png",
            "background_crop_final_resolution_proof_ref": "proof/background-crop.png",
            "remotion_compositing_receipt_ref": "proof/remotion-compositing.json",
            "independent_style_review_ref": "proof/style-review.md",
            "rejection_gate": "global noise or a tiny halftone swatch cannot pass",
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

    def test_newsprint_receipt_requires_classification_raster_and_proof_refs(self) -> None:
        missing = scene("S01", 0, "m1", "f1")
        treatment = missing["treatment_receipt"]
        del treatment["texture_classification"]
        del treatment["raster_paper_asset_ref"]
        del treatment["raster_paper_rights_ref"]
        del treatment["full_frame_texture_proof_ref"]
        del treatment["final_resolution_halftone_scale"]
        del treatment["subject_mask_final_resolution_proof_ref"]
        del treatment["background_crop_final_resolution_proof_ref"]
        del treatment["remotion_compositing_receipt_ref"]
        del treatment["independent_style_review_ref"]
        del treatment["rejection_gate"]
        result = verify({"scenes": [missing]})
        messages = "\n".join(failure["message"] for failure in result["failures"])
        self.assertFalse(result["pass"])
        self.assertIn("texture_classification", messages)
        self.assertIn("raster_paper_asset_ref", messages)
        self.assertIn("raster_paper_rights_ref", messages)
        self.assertIn("full_frame_texture_proof_ref", messages)
        self.assertIn("final_resolution_halftone_scale", messages)
        self.assertIn("subject_mask_final_resolution_proof_ref", messages)
        self.assertIn("background_crop_final_resolution_proof_ref", messages)
        self.assertIn("remotion_compositing_receipt_ref", messages)
        self.assertIn("independent_style_review_ref", messages)
        self.assertIn("rejection_gate", messages)

    def test_newsprint_receipt_rejects_unknown_texture_classification(self) -> None:
        invalid = scene("S01", 0, "m1", "f1")
        invalid["treatment_receipt"]["texture_classification"] = "vox_grain_filter"
        result = verify({"scenes": [invalid]})
        self.assertFalse(result["pass"])
        self.assertTrue(
            any("texture_classification must be one of" in failure["message"] for failure in result["failures"])
        )


if __name__ == "__main__":
    unittest.main()
