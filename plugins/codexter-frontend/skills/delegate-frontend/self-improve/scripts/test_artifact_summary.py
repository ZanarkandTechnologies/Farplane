from __future__ import annotations

import json
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parent
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

import artifact_summary


class ArtifactSummaryTests(unittest.TestCase):
    def test_delegate_run_summary_detects_ready_complete_phase(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            run_dir = root / "run"
            run_dir.mkdir()
            output = root / "SPEC.md"
            output.write_text("# Spec\n\n" + "x" * 240, encoding="utf-8")
            (run_dir / "session_files.json").write_text(
                json.dumps({"session_files": [str(run_dir / "sessions" / "one.jsonl")]}),
                encoding="utf-8",
            )
            (run_dir / "exit_code.txt").write_text("0\n", encoding="utf-8")
            (run_dir / "handoff.md").write_text(
                "## Changed Files\n\n- `SPEC.md`\n\n"
                "## Verification\n\n- checked\n\n"
                "## Risks\n\n- none\n",
                encoding="utf-8",
            )
            (run_dir / "first_write.json").write_text(
                json.dumps({"status": "pass", "expected_outputs": [str(output)]}),
                encoding="utf-8",
            )

            self.assertEqual(artifact_summary.summarize_startup(run_dir)["status"], "ready")
            phase = artifact_summary.summarize_phase_completion(run_dir, root)
            self.assertEqual(phase["status"], "complete")
            self.assertEqual(phase["first_write_status"], "pass")

    def test_short_regular_output_can_complete_startup_probe(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            run_dir = root / "run"
            run_dir.mkdir()
            output = root / "PROBE.md"
            output.write_text("ready\n", encoding="utf-8")
            (run_dir / "exit_code.txt").write_text("0\n", encoding="utf-8")
            (run_dir / "handoff.md").write_text(
                "## Changed Files\n\n- `PROBE.md`\n\n"
                "## Verification\n\n- first-write pass\n\n"
                "## First-Write Evidence\n\n- observed output: `PROBE.md`\n\n"
                "## Risks\n\n- startup only\n",
                encoding="utf-8",
            )
            (run_dir / "first_write.json").write_text(
                json.dumps({"status": "pass", "expected_outputs": [str(output)]}),
                encoding="utf-8",
            )

            phase = artifact_summary.summarize_phase_completion(run_dir, root)
            self.assertEqual(phase["status"], "complete")
            self.assertTrue(phase["handoff_contract"]["first_write_evidence"])

    def test_delegate_run_summary_marks_no_session_and_stub(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            run_dir = root / "run"
            run_dir.mkdir()
            output = root / "SPEC.md"
            output.write_text("stub", encoding="utf-8")
            (run_dir / "session_files.json").write_text(
                json.dumps({"session_files": []}),
                encoding="utf-8",
            )
            (run_dir / "exit_code.txt").write_text("124\n", encoding="utf-8")
            (run_dir / "first_write.json").write_text(
                json.dumps({"status": "pass", "expected_outputs": [str(output)]}),
                encoding="utf-8",
            )

            startup = artifact_summary.summarize_startup(run_dir)
            phase = artifact_summary.summarize_phase_completion(run_dir, root)
            self.assertEqual(startup["status"], "failed")
            self.assertEqual(startup["failure_reason"], "no_session_file")
            self.assertEqual(phase["status"], "stub")

    def test_phase_completion_rejects_placeholder_handoff(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            run_dir = root / "run"
            run_dir.mkdir()
            output = root / "SPEC.md"
            output.write_text("# Spec\n\n" + "x" * 240, encoding="utf-8")
            (run_dir / "session_files.json").write_text(
                json.dumps({"session_files": [str(run_dir / "sessions" / "one.jsonl")]}),
                encoding="utf-8",
            )
            (run_dir / "exit_code.txt").write_text("0\n", encoding="utf-8")
            (run_dir / "handoff.md").write_text(
                "# External CLI Handoff\n\n"
                "## Changed Files\n\n"
                "- none reported yet\n\n"
                "## Behavior Built\n\n"
                "- pending live external CLI run\n",
                encoding="utf-8",
            )
            (run_dir / "first_write.json").write_text(
                json.dumps({"status": "pass", "expected_outputs": [str(output)]}),
                encoding="utf-8",
            )

            phase = artifact_summary.summarize_phase_completion(run_dir, root)
            self.assertEqual(phase["status"], "stub")
            self.assertEqual(phase["handoff_path"], "")
            self.assertEqual(phase["handoff_status"], "placeholder")
            self.assertIn("pending live external cli run", phase["handoff_placeholder_markers"])

    def test_asset_manifest_summary_counts_generated_assets_and_refs(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            asset = root / "assets" / "frame.webp"
            asset.parent.mkdir()
            asset.write_bytes(b"fake")
            manifest = root / "assets" / "asset-manifest.json"
            manifest.write_text(
                json.dumps(
                    {
                        "asset_strategy": "generated-frame-sequence",
                        "assets": [
                            {
                                "path": "assets/frame.webp",
                                "kind": "frame",
                                "role": "mobile reduced poster",
                                "source_prompt": "warehouse yard",
                            }
                        ],
                    }
                ),
                encoding="utf-8",
            )
            summary = artifact_summary.summarize_asset_manifest(manifest, root)
            self.assertEqual(summary["generated_or_rendered_count"], 1)
            self.assertEqual(summary["broken_refs"], 0)
            self.assertTrue(summary["has_mobile_fallback"])
            self.assertTrue(summary["has_reduced_motion_fallback"])

    def test_spec_summary_reads_table_and_numbered_sections(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            spec_path = Path(tmp) / "SPEC.md"
            spec_path.write_text(
                "# Compiled Spec\n\n"
                "| Field | Value |\n"
                "|---|---|\n"
                "| **Offer** | Warehouse computer vision operating system |\n"
                "| **Audience** | Enterprise logistics executives |\n"
                "| **Carrier object / world** | Camera-instrumented yard and dock world |\n\n"
                "- **Recipe ID:** `cinematic-industrial-scroll`\n"
                "- **Taste Profile ID:** `terminal-mission-control`\n"
                "- **Effect Stack ID:** `video-frame-sequence-scroll-scrub`\n\n"
                "| # | Section | Narrative Role |\n"
                "|---|---|---|\n"
                "| 1 | Hero | Yard |\n"
                "| 2 | Tension | Delay |\n"
                "| 3 | Command | AI |\n"
                "| 4 | Missions | Proof |\n"
                "| 5 | CTA | Convert |\n\n"
                "### Asset 1\n### Asset 2\n### Asset 3\n### Asset 4\n\n"
                "## 9. QA Plan\n\n"
                "Run desktop, mobile, reduced motion, scroll-scrub, geometry, and review checks.\n\n"
                "0% 25% 50% 75% 95%\n",
                encoding="utf-8",
            )
            summary = artifact_summary.summarize_spec(spec_path)
            self.assertEqual(summary["status"], "complete")
            self.assertEqual(summary["asset_prompts"], 4)
            self.assertEqual(summary["sections"], 5)
            self.assertEqual(summary["recipe_id"], "cinematic-industrial-scroll")
            self.assertEqual(summary["taste_profile_id"], "terminal-mission-control")
            self.assertEqual(summary["effect_stack_id"], "video-frame-sequence-scroll-scrub")

    def test_spec_summary_does_not_parse_route_ids_from_plain_prose(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            spec_path = Path(tmp) / "SPEC.md"
            spec_path.write_text(
                "# Stub Spec\n\n"
                "This placeholder mentions registry slugs in prose, but it "
                "does not select them: cinematic-industrial-scroll, "
                "terminal-mission-control, and "
                "video-frame-sequence-scroll-scrub are only examples. It has "
                "no offer, audience, selected recipe, taste profile, effect "
                "stack, asset prompts, section plan, motion checkpoints, or "
                "QA plan.\n",
                encoding="utf-8",
            )
            summary = artifact_summary.summarize_spec(spec_path)
            self.assertEqual(summary["status"], "stub")
            self.assertEqual(summary["recipe_id"], "")
            self.assertEqual(summary["taste_profile_id"], "")
            self.assertEqual(summary["effect_stack_id"], "")

    def test_spec_summary_reads_snake_case_route_and_beat_asset_headings(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            spec_path = Path(tmp) / "SPEC.md"
            spec_path.write_text(
                "# Spec\n\n"
                "## Route\n"
                "- **recipe_id**: `cinematic-industrial-scroll`\n"
                "- **taste_profile_id**: `terminal-mission-control`\n"
                "- **effect_stack_id**: `video-frame-sequence-scroll-scrub`\n\n"
                "## Offer\nEnterprise warehouse CV platform.\n\n"
                "## Audience\nOperations leaders.\n\n"
                "## Carrier Object / World\nWarehouse yard becomes a command surface.\n\n"
                "### Beat 1\n### Beat 2\n### Beat 3\n### Beat 4\n### Beat 5\n\n"
                "## Asset Prompts\n"
                "**A1 — Desktop Hero**\nPrompt: yard\n"
                "**A2 — Mobile Hero**\nPrompt: mobile\n"
                "**A3 — Support Loop**\nPrompt: manifest\n"
                "**A4 — Reduced Still**\nPrompt: still\n\n"
                "## QA Plan\nRun desktop, mobile, reduced motion, scroll-scrub, and review.\n\n"
                "0% 25% 50% 75% 95%\n",
                encoding="utf-8",
            )
            summary = artifact_summary.summarize_spec(spec_path)
            self.assertEqual(summary["status"], "complete")
            self.assertEqual(summary["recipe_id"], "cinematic-industrial-scroll")
            self.assertEqual(summary["taste_profile_id"], "terminal-mission-control")
            self.assertEqual(summary["effect_stack_id"], "video-frame-sequence-scroll-scrub")
            self.assertEqual(summary["sections"], 5)
            self.assertEqual(summary["asset_prompts"], 4)

    def test_handoff_summary_accepts_first_write_proof_and_findings_risks(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            handoff = Path(tmp) / "handoff.md"
            handoff.write_text(
                "## Changed Files\n\n- `SPEC.md`\n\n"
                "## Wrapper First-Write Evidence\n\n- pass\n\n"
                "## Verification\n\n- checked\n\n"
                "## Findings / Risks\n\n- timeout risk\n",
                encoding="utf-8",
            )
            summary = artifact_summary.summarize_handoff(handoff)
            self.assertEqual(summary["status"], "complete")
            self.assertTrue(summary["sections"]["first_write_evidence"])
            self.assertTrue(summary["sections"]["risks"])

    def test_handoff_summary_accepts_live_asset_handoff_headings(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            handoff = Path(tmp) / "handoff.md"
            handoff.write_text(
                "## Changed / Produced Files\n\n"
                "- `assets/asset-manifest.json`\n\n"
                "## Self-Review Findings\n\n"
                "- asset manifest lint passed\n\n"
                "## Risks\n\n"
                "- implementation phase still pending\n",
                encoding="utf-8",
            )
            summary = artifact_summary.summarize_handoff(handoff)
            self.assertEqual(summary["status"], "complete")
            self.assertTrue(summary["sections"]["changed_files"])
            self.assertTrue(summary["sections"]["verification"])
            self.assertTrue(summary["sections"]["risks"])

    def test_handoff_summary_rejects_nonempty_handoff_without_required_sections(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            handoff = Path(tmp) / "handoff.md"
            handoff.write_text("done\n", encoding="utf-8")
            summary = artifact_summary.summarize_handoff(handoff)
            self.assertEqual(summary["status"], "incomplete")
            self.assertFalse(summary["sections"]["changed_files"])
            self.assertFalse(summary["sections"]["verification"])
            self.assertFalse(summary["sections"]["risks"])

    def test_handoff_summary_rejects_heading_only_sections(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            handoff = Path(tmp) / "handoff.md"
            handoff.write_text(
                "## Changed Files\n\n"
                "## Verification\n\n"
                "## Risks / Followups\n\n",
                encoding="utf-8",
            )
            summary = artifact_summary.summarize_handoff(handoff)
            self.assertEqual(summary["status"], "incomplete")
            self.assertFalse(summary["sections"]["changed_files"])
            self.assertFalse(summary["sections"]["verification"])
            self.assertFalse(summary["sections"]["risks"])

    def test_asset_manifest_summary_counts_unsafe_refs(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            outside = root.parent / "outside-summary.webp"
            outside.write_bytes(b"RIFF0000WEBPVP8 fixture")
            manifest = root / "assets" / "asset-manifest.json"
            manifest.parent.mkdir()
            manifest.write_text(
                json.dumps(
                    {
                        "asset_strategy": "generated-frame-sequence",
                        "assets": [
                            {
                                "path": str(outside),
                                "kind": "generated-frame",
                                "role": "desktop hero mobile reduced support frame",
                                "width": 1920,
                                "height": 1080,
                                "source_prompt": "escaped frame",
                            }
                        ],
                    }
                ),
                encoding="utf-8",
            )
            summary = artifact_summary.summarize_asset_manifest(manifest, root)
            self.assertEqual(summary["broken_refs"], 0)
            self.assertEqual(summary["unsafe_refs"], 1)

    def test_scroll_qa_summary_reads_visual_geometry(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            qa_path = Path(tmp) / "scroll-scrub-qa.json"
            qa_path.write_text(
                json.dumps({"visualGeometry": {"hero_object_fill_ratio": 0.7, "nav_overflow": False}}),
                encoding="utf-8",
            )
            summary = artifact_summary.summarize_scroll_qa(qa_path)
            self.assertEqual(summary["hero_object_fill_ratio"], 0.7)
            self.assertFalse(summary["nav_overflow"])


if __name__ == "__main__":
    unittest.main()
