#!/usr/bin/env python3
"""Verify mechanical scene-direction gates without pretending to judge story quality."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any

CONCEPT_TYPES = {"literal_evidence", "causal_physical", "context_scale"}
REVEAL_KINDS = {"introduce", "transform", "connect", "remove", "recontextualize"}
TEXTURE_CLASSIFICATIONS = {
    "source_baked_scan",
    "demonstrated_added_effect",
    "operator_requested_style",
}


def _ratio(values: list[str]) -> float:
    return len(set(values)) / len(values) if values else 1.0


def verify(payload: dict[str, Any]) -> dict[str, Any]:
    scenes = [scene for scene in payload.get("scenes", []) if scene.get("production_scene", True)]
    motif_families = {
        motif.get("family_id")
        for motif in payload.get("intentional_motifs", [])
        if motif.get("family_id") and motif.get("causal_function") and motif.get("transformations")
    }
    failures: list[dict[str, str]] = []
    warnings: list[dict[str, str]] = []

    def fail(check: str, message: str) -> None:
        failures.append({"check": check, "message": message})

    if not scenes:
        fail("scenes_present", "At least one production scene is required.")

    main_families: list[str] = []
    foreground_families: list[str] = []
    previous: dict[str, Any] | None = None

    for scene in scenes:
        scene_id = str(scene.get("id", "<missing-id>"))
        start = scene.get("start_seconds")
        end = scene.get("end_seconds")
        if not isinstance(start, (int, float)) or not isinstance(end, (int, float)) or end <= start:
            fail("duration", f"{scene_id}: invalid start/end seconds.")
        else:
            duration = round(float(end) - float(start), 3)
            if duration < 3.5 or duration > 6.0:
                fail("duration", f"{scene_id}: {duration}s is outside the calibrated 3.5-6.0s band.")
            elif duration < 4.0 or duration > 5.0:
                warnings.append({"check": "duration_target", "message": f"{scene_id}: {duration}s is outside the 4-5s target."})

        if not str(scene.get("state_change", "")).strip():
            fail("state_change", f"{scene_id}: missing one explicit viewer-state change.")

        concepts = scene.get("concepts", [])
        concept_types = {concept.get("relationship_type") for concept in concepts}
        if len(concepts) < 3 or not CONCEPT_TYPES.issubset(concept_types):
            fail("concepts", f"{scene_id}: needs literal_evidence, causal_physical, and context_scale concepts.")
        concept_ids = {concept.get("id") for concept in concepts}
        if scene.get("selected_concept_id") not in concept_ids:
            fail("concept_selection", f"{scene_id}: selected concept must resolve to a concept record.")
        rejected = [concept for concept in concepts if concept.get("id") != scene.get("selected_concept_id")]
        if any(not str(concept.get("rejection_reason", "")).strip() for concept in rejected):
            fail("concept_selection", f"{scene_id}: rejected concepts need reasons.")

        reveals = [reveal for reveal in scene.get("reveals", []) if reveal.get("story_bearing")]
        if len(reveals) not in {2, 3} or any(reveal.get("kind") not in REVEAL_KINDS for reveal in reveals):
            fail("reveals", f"{scene_id}: needs 2-3 story-bearing reveals with allowed reveal kinds.")

        main_family = scene.get("main_topic", {}).get("family_id")
        foreground_family = scene.get("foreground", {}).get("family_id")
        if not main_family:
            fail("asset_family", f"{scene_id}: missing main-topic family_id.")
        elif main_family not in motif_families:
            main_families.append(main_family)
        if not foreground_family:
            fail("asset_family", f"{scene_id}: missing foreground family_id.")
        elif foreground_family not in motif_families:
            foreground_families.append(foreground_family)

        if previous:
            for role, family in (("main_topic", main_family), ("foreground", foreground_family)):
                prior_family = previous.get(role, {}).get("family_id")
                if family and family == prior_family and family not in motif_families:
                    fail("adjacent_variance", f"{previous.get('id')}->{scene_id}: repeated {role} family {family}.")

        if scene.get("readiness") == "creative_lock_passed":
            geometry = scene.get("foreground", {}).get("geometry_receipt", {})
            if not geometry.get("final_resolution"):
                fail("foreground_geometry", f"{scene_id}: missing final-resolution geometry receipt.")
            visible_ratio = geometry.get("visible_bbox_frame_ratio")
            if (
                not isinstance(visible_ratio, (int, float))
                or (visible_ratio < 0.20 and not geometry.get("edge_spanning_equivalent"))
            ):
                fail("foreground_geometry", f"{scene_id}: foreground bbox needs >=0.20 frame ratio or evidenced edge-spanning equivalent.")
            if not geometry.get("tight_alpha_bounds"):
                fail("foreground_geometry", f"{scene_id}: transparent asset lacks tight alpha bounds.")
            if not geometry.get("edge_contacts"):
                fail("foreground_geometry", f"{scene_id}: foreground has no frame-edge contact.")
            if not geometry.get("semantic_relevance"):
                fail("foreground_geometry", f"{scene_id}: foreground lacks a narration-specific job.")

            treatment = scene.get("treatment_receipt", {})
            required = (
                "final_resolution",
                "background_clean",
                "subject_halftone",
                "crisp_alpha",
                "registration_restrained",
                "raster_paper_asset_ref",
                "raster_paper_rights_ref",
                "page_or_object_coordinates",
                "full_frame_texture_proof_ref",
                "close_crop_texture_proof_ref",
                "final_resolution_halftone_scale",
                "subject_mask_final_resolution_proof_ref",
                "background_crop_final_resolution_proof_ref",
                "remotion_compositing_receipt_ref",
                "independent_style_review_ref",
                "rejection_gate",
            )
            missing = [field for field in required if not treatment.get(field)]
            if missing:
                fail("newsprint_treatment", f"{scene_id}: treatment receipt missing {', '.join(missing)}.")
            classification = treatment.get("texture_classification")
            if classification not in TEXTURE_CLASSIFICATIONS:
                fail(
                    "newsprint_treatment",
                    f"{scene_id}: texture_classification must be one of {', '.join(sorted(TEXTURE_CLASSIFICATIONS))}.",
                )
            if treatment.get("global_distress"):
                fail("newsprint_treatment", f"{scene_id}: global distress is not valid subject treatment.")

        previous = scene

    main_unique = _ratio(main_families)
    foreground_unique = _ratio(foreground_families)
    if main_unique < 0.80:
        fail("unique_ratio", f"Main-topic unique-family ratio {main_unique:.3f} is below 0.80.")
    if foreground_unique < 0.85:
        fail("unique_ratio", f"Foreground unique-family ratio {foreground_unique:.3f} is below 0.85.")

    return {
        "pass": not failures,
        "scene_count": len(scenes),
        "metrics": {
            "main_topic_unique_family_ratio": round(main_unique, 3),
            "foreground_unique_family_ratio": round(foreground_unique, 3),
        },
        "failures": failures,
        "warnings": warnings,
        "judgment_required": [
            "specificity",
            "causal_clarity",
            "hierarchy_depth",
            "neighbor_novelty",
            "silent_comprehension",
            "evidence_integrity",
        ],
    }


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("manifest", type=Path)
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()
    result = verify(json.loads(args.manifest.read_text()))
    rendered = json.dumps(result, indent=2) + "\n"
    if args.output:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(rendered)
    else:
        sys.stdout.write(rendered)
    return 0 if result["pass"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
