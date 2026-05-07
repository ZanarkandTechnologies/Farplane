from __future__ import annotations

import argparse
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parent
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

import phase_prompt_compiler
import startup_probe


class PhasePromptCompilerTests(unittest.TestCase):
    def test_spec_prompt_is_bounded_and_first_write_oriented(self) -> None:
        args = argparse.Namespace(
            phase="spec",
            brief="Enterprise warehouse CV landing page.",
            brief_file="",
            owned_output=["SPEC.md"],
            handoff_path="handoff.md",
            recipe_id="cinematic-industrial-scroll",
            taste_profile_id="terminal-mission-control",
            effect_stack_id="video-frame-sequence-scroll-scrub",
            acceptance=[],
            output="",
        )
        prompt = phase_prompt_compiler.compile_prompt(args)
        self.assertIn("Your first external tool call must create or modify `SPEC.md`", prompt)
        self.assertIn("recipe_id: cinematic-industrial-scroll", prompt)
        self.assertIn("taste_profile_id: terminal-mission-control", prompt)
        self.assertIn("effect_stack_id: video-frame-sequence-scroll-scrub", prompt)
        self.assertIn("include at least 5 sections or beats", prompt)
        self.assertIn("do not implement the page", prompt)
        self.assertIn("Do not build outside this phase.", prompt)
        summary = phase_prompt_compiler.summarize_prompt(
            prompt=prompt,
            phase="spec",
            owned_outputs=["SPEC.md"],
            recipe_id="cinematic-industrial-scroll",
            taste_profile_id="terminal-mission-control",
            effect_stack_id="video-frame-sequence-scroll-scrub",
        )
        self.assertTrue(summary["contains_first_write"])
        self.assertTrue(summary["contains_selected_route"])
        self.assertTrue(summary["forbids_broad_reference_before_first_write"])
        self.assertTrue(summary["forbids_full_page_build"])

    def test_startup_probe_prompt_exits_after_probe(self) -> None:
        args = argparse.Namespace(
            phase="startup",
            brief="Probe only.",
            brief_file="",
            owned_output=[".harness/delegate-frontend/startup-probe/PROBE.md"],
            handoff_path=".harness/external-cli/runs/probe/handoff.md",
            recipe_id="cinematic-industrial-scroll",
            taste_profile_id="terminal-mission-control",
            effect_stack_id="video-frame-sequence-scroll-scrub",
            acceptance=[],
            output="",
        )
        prompt = phase_prompt_compiler.compile_prompt(args)
        self.assertIn("prove the external CLI can start", prompt)
        self.assertIn("do not analyze at length", prompt)
        self.assertIn("exit after the probe; do not start implementation", prompt)
        self.assertIn(".harness/delegate-frontend/startup-probe/PROBE.md", prompt)
        self.assertIn("parent directories", prompt)

    def test_asset_prompt_uses_exact_owned_manifest_path(self) -> None:
        args = argparse.Namespace(
            phase="assets",
            brief="Asset phase.",
            brief_file="",
            owned_output=[".harness/delegate-frontend/asset-runs/live/assets/asset-manifest.json"],
            handoff_path="handoff.md",
            recipe_id="cinematic-industrial-scroll",
            taste_profile_id="terminal-mission-control",
            effect_stack_id="video-frame-sequence-scroll-scrub",
            acceptance=[],
            output="",
        )
        prompt = phase_prompt_compiler.compile_prompt(args)
        self.assertIn(
            "create or modify `.harness/delegate-frontend/asset-runs/live/assets/asset-manifest.json`",
            prompt,
        )
        self.assertIn(
            "record at least 4 generated/rendered frame, image, or video assets in .harness/delegate-frontend/asset-runs/live/assets/asset-manifest.json",
            prompt,
        )
        self.assertIn("do not use `mkdir` as the first tool call", prompt)
        self.assertNotIn("record at least 4 generated/rendered frame, image, or video assets in assets/asset-manifest.json", prompt)

    def test_asset_prompt_extracts_asset_relevant_brief_from_full_spec(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            spec = Path(tmp) / "SPEC.md"
            spec.write_text(
                "# Full Spec\n\n"
                "## Offer\nEnterprise CV.\n\n"
                "## Long Section\n" + ("noise\n" * 200) + "\n"
                "## Asset Plan\n"
                "### Asset Prompts\n"
                "**A1** desktop hero.\n\n"
                "## Motion Plan\n"
                "Frame sequence scroll scrub.\n\n",
                encoding="utf-8",
            )
            args = argparse.Namespace(
                phase="assets",
                brief="",
                brief_file=str(spec),
                owned_output=["asset-manifest.json"],
                handoff_path="handoff.md",
                recipe_id="cinematic-industrial-scroll",
                taste_profile_id="terminal-mission-control",
                effect_stack_id="video-frame-sequence-scroll-scrub",
                acceptance=[],
                output="",
            )
            prompt = phase_prompt_compiler.compile_prompt(args)
            self.assertIn("## Asset Plan", prompt)
            self.assertIn("## Motion Plan", prompt)
            self.assertNotIn("## Long Section", prompt)

    def test_startup_probe_builds_delegate_cli_dry_run_command(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            artifact_dir = Path(tmp)
            args = argparse.Namespace(
                profile="frontend-pi-kimi",
                run_id="probe-test",
                probe_output=".harness/delegate-frontend/startup-probe/PROBE.md",
                artifact_dir=artifact_dir,
                thinking="low",
                first_write_timeout_seconds=90,
                timeout_seconds=150,
                dry_run=True,
            )
            prompt_path = artifact_dir / "startup-probe-prompt.md"
            startup_probe.write_probe_prompt(args, prompt_path)
            command = startup_probe.build_probe_command(args, prompt_path)
            self.assertIn("--dry-run", command)
            self.assertIn("--expect-output", command)
            self.assertIn("--thinking", command)
            self.assertIn("low", command)
            self.assertIn(".harness/delegate-frontend/startup-probe/PROBE.md", command)
            self.assertTrue(prompt_path.exists())

    def test_handoff_only_prompt_does_not_claim_first_write(self) -> None:
        args = argparse.Namespace(
            phase="visual-review",
            brief="Review screenshots only.",
            brief_file="",
            owned_output=[],
            handoff_path="handoff.md",
            recipe_id="cinematic-industrial-scroll",
            taste_profile_id="terminal-mission-control",
            effect_stack_id="video-frame-sequence-scroll-scrub",
            acceptance=[],
            output="",
        )
        prompt = phase_prompt_compiler.compile_prompt(args)
        self.assertIn("No owned output was supplied", prompt)
        self.assertIn("write only the requested handoff", prompt)
        self.assertIn("- none; this phase should only write the handoff", prompt)
        self.assertNotIn("the named owned output", prompt)

    def test_repair_prompt_is_micro_patch_oriented(self) -> None:
        owned_output = ".harness/warehouse-cv-scrollscrub-pi-kimi-v2/index.html"
        args = argparse.Namespace(
            phase="repair",
            brief="Repair the warehouse CV overlay and support videos.",
            brief_file="",
            owned_output=[owned_output],
            handoff_path="handoff.md",
            recipe_id="cinematic-industrial-scroll",
            taste_profile_id="terminal-mission-control",
            effect_stack_id="video-frame-sequence-scroll-scrub",
            acceptance=[],
            output="",
        )
        prompt = phase_prompt_compiler.compile_prompt(args)
        self.assertIn(f"Your first external tool call must create or modify `{owned_output}`", prompt)
        self.assertIn("make one bounded repair patch", prompt)
        self.assertIn("do not read scroll_scrub_qa.cjs", prompt)
        self.assertIn("do not read sibling prototype pages", prompt)
        self.assertIn("never replace a built page with a minimal dark text stub", prompt)
        self.assertIn("style scrub must change computed transform", prompt)
        self.assertIn("hasSupportVideoDom and hasMissionSupportVideos", prompt)
        self.assertIn("hasMobileHeroPhraseSeparation", prompt)
        summary = phase_prompt_compiler.summarize_prompt(
            prompt=prompt,
            phase="repair",
            owned_outputs=[owned_output],
            recipe_id="cinematic-industrial-scroll",
            taste_profile_id="terminal-mission-control",
            effect_stack_id="video-frame-sequence-scroll-scrub",
        )
        self.assertTrue(summary["contains_repair_micro_patch"])
        self.assertTrue(summary["forbids_qa_script_read"])
        self.assertTrue(summary["forbids_sibling_prototype_read"])
        self.assertTrue(summary["requires_style_scrub"])
        self.assertTrue(summary["requires_support_video_metric"])
        self.assertTrue(summary["requires_mobile_phrase_separation"])
        self.assertTrue(summary["preserves_existing_surface"])

    def test_startup_probe_defaults_are_run_id_derived(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            args = argparse.Namespace(
                profile="frontend-pi-kimi",
                run_id="probe-derived",
                probe_output="",
                artifact_dir="",
                thinking="low",
                first_write_timeout_seconds=90,
                timeout_seconds=150,
                dry_run=True,
            )
            startup_probe.resolve_paths(args, root)
            self.assertEqual(
                args.probe_output,
                ".harness/delegate-frontend/startup-probes/probe-derived/PROBE.md",
            )
            self.assertEqual(
                args.artifact_dir,
                root / ".harness" / "external-cli" / "runs" / "probe-derived",
            )


if __name__ == "__main__":
    unittest.main()
