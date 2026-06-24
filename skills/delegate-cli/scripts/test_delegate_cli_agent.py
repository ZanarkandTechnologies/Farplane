from __future__ import annotations

import json
import subprocess
import sys
import tempfile
import threading
import time
import unittest
from argparse import Namespace
from dataclasses import replace
from pathlib import Path

ROOT = Path(__file__).resolve().parent
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

import delegate_cli_agent


def write_profile_templates(root: Path) -> None:
    profile_dir = root / "templates" / "external-cli" / "profiles" / "frontend-pi-kimi"
    profile_dir.mkdir(parents=True, exist_ok=True)
    (profile_dir / "APPEND_SYSTEM.md").write_text("system\n", encoding="utf-8")
    (profile_dir / "prompt.md.tpl").write_text(
        "Profile {{profile_name}}\nTicket {{ticket_ref}}\n{{append_system}}\n{{prompt}}\n{{skill_list}}\n{{ticket_context}}\n{{handoff_path}}\n",
        encoding="utf-8",
    )
    (profile_dir / "handoff.md.tpl").write_text(
        "Handoff {{profile_name}} {{run_id}}\n",
        encoding="utf-8",
    )
    (profile_dir / "settings.json.tpl").write_text(
        '{\n  "skills": [\n{{settings_skill_paths}}\n  ]\n}\n',
        encoding="utf-8",
    )


def write_skill_bundle_manifest(root: Path, required: list[str], optional: list[str] | None = None) -> None:
    profile_dir = root / "templates" / "external-cli" / "profiles" / "frontend-pi-kimi"
    (profile_dir / "skill-bundle.json").write_text(
        json.dumps(
            {
                "schema_version": "test",
                "required_skills": required,
                "optional_skills": optional or [],
            },
            indent=2,
        )
        + "\n",
        encoding="utf-8",
    )


def write_skill_sources(root: Path) -> None:
    for name in delegate_cli_agent.DEFAULT_FRONTEND_SKILLS:
        skill_dir = root / "skills" / name
        skill_dir.mkdir(parents=True, exist_ok=True)
        (skill_dir / "SKILL.md").write_text(
            f"---\nname: {name}\ndescription: test skill\n---\n# {name}\n",
            encoding="utf-8",
        )


class DelegateCliAgentTests(unittest.TestCase):
    def test_load_profile_uses_frontend_pi_kimi_contract(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            write_profile_templates(root)
            profile = delegate_cli_agent.load_profile("frontend-pi-kimi", root)
            self.assertEqual(profile.adapter, "pi")
            self.assertEqual(profile.model, "openrouter/moonshotai/kimi-k2.6")
            self.assertIn("frontend-craft", profile.skill_names)
            self.assertIn("image-generation", profile.skill_names)
            self.assertIn("video-generation", profile.skill_names)
            self.assertIn("agent-browser", profile.skill_names)
            self.assertIn("visual-qa", profile.skill_names)
            self.assertIn("review", profile.skill_names)
            self.assertIn("web-design-guidelines", profile.skill_names)
            self.assertNotIn("imagegen", profile.skill_names)
            self.assertEqual(profile.default_checkout, "worktree")

    def test_load_profile_uses_skill_bundle_manifest(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            write_profile_templates(root)
            write_skill_bundle_manifest(
                root,
                ["frontend-craft", "image-generation", "video-generation"],
            )
            profile = delegate_cli_agent.load_profile("frontend-pi-kimi", root)
            self.assertEqual(
                profile.skill_names,
                ("frontend-craft", "image-generation", "video-generation"),
            )

    def test_read_prompt_arg_supports_prompt_file(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            prompt_file = root / "brief.md"
            prompt_file.write_text("phase: implementation\n", encoding="utf-8")
            self.assertEqual(
                delegate_cli_agent.read_prompt_arg("ignored", "brief.md", root),
                "phase: implementation\n",
            )

    def test_resolve_expected_outputs_stays_inside_checkout(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            self.assertEqual(
                delegate_cli_agent.resolve_expected_outputs(["out/app.js"], root),
                [(root / "out" / "app.js").resolve(strict=False)],
            )
            with self.assertRaises(SystemExit):
                delegate_cli_agent.resolve_expected_outputs(["../escape.js"], root)

    def test_first_write_gate_passes_when_expected_file_is_created(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            runtime_dir = root / "runtime"
            runtime_dir.mkdir()
            expected = root / "out.js"
            completed, first_write = delegate_cli_agent.run_with_first_write_gate(
                command=[
                    sys.executable,
                    "-c",
                    "from pathlib import Path; Path('out.js').write_text('ok')",
                ],
                cwd=root,
                env={},
                timeout_seconds=5,
                first_write_timeout_seconds=2,
                expected_outputs=[expected],
                runtime_dir=runtime_dir,
            )
            self.assertEqual(completed.returncode, 0)
            self.assertEqual(first_write["status"], "pass")
            self.assertEqual(first_write["observed_output"], str(expected))

    def test_first_write_gate_can_stop_after_output_and_completed_handoff(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            runtime_dir = root / "runtime"
            runtime_dir.mkdir()
            expected = root / "SPEC.md"
            handoff = runtime_dir / "handoff.md"
            script = (
                "from pathlib import Path\n"
                "import time\n"
                "Path('SPEC.md').write_text('# Spec\\n')\n"
                f"Path({str(handoff)!r}).write_text("
                "'## Changed Files\\n\\n- `SPEC.md`\\n\\n"
                "## Verification\\n\\n- checked\\n\\n"
                "## Risks / Followups\\n\\n- none\\n', encoding='utf-8')\n"
                "time.sleep(10)\n"
            )
            started = time.monotonic()
            completed, first_write = delegate_cli_agent.run_with_first_write_gate(
                command=[sys.executable, "-c", script],
                cwd=root,
                env={},
                timeout_seconds=20,
                first_write_timeout_seconds=5,
                expected_outputs=[expected],
                runtime_dir=runtime_dir,
                handoff_path=handoff,
                complete_when_output_and_handoff=True,
                completion_grace_seconds=0,
            )
            elapsed = time.monotonic() - started
            self.assertLess(elapsed, 5)
            self.assertEqual(completed.returncode, 0)
            self.assertEqual(first_write["status"], "pass")
            self.assertEqual(first_write["completion_reason"], "expected_output_and_handoff")
            self.assertIn("completed handoff", completed.stderr)

    def test_output_quality_gate_rejects_stub_with_completed_handoff(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            runtime_dir = root / "runtime"
            runtime_dir.mkdir()
            expected = root / "media-repair.js"
            handoff = runtime_dir / "handoff.md"
            script = (
                "from pathlib import Path\n"
                "Path('media-repair.js').write_text('// stub\\n')\n"
                f"Path({str(handoff)!r}).write_text("
                "'## Changed Files\\n\\n- `media-repair.js`\\n\\n"
                "## Verification\\n\\n- not run\\n\\n"
                "## Risks / Followups\\n\\n- stub\\n', encoding='utf-8')\n"
            )
            completed, first_write = delegate_cli_agent.run_with_first_write_gate(
                command=[sys.executable, "-c", script],
                cwd=root,
                env={},
                timeout_seconds=5,
                first_write_timeout_seconds=2,
                expected_outputs=[expected],
                runtime_dir=runtime_dir,
                handoff_path=handoff,
                complete_when_output_and_handoff=True,
                completion_grace_seconds=0,
                output_quality_gate=delegate_cli_agent.OutputQualityGate(
                    min_bytes=200,
                    required_substrings=("window.__scrollScrubDebug", "mediaTime"),
                ),
            )
            self.assertEqual(completed.returncode, 126)
            self.assertEqual(first_write["status"], "pass")
            self.assertEqual(first_write["output_quality"]["status"], "failed")
            self.assertIn("output quality gate", completed.stderr)

    def test_output_quality_gate_accepts_complete_sidecar(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            runtime_dir = root / "runtime"
            runtime_dir.mkdir()
            expected = root / "media-repair.js"
            sidecar = (
                "(function(){\\n"
                "  const video = document.createElement('video');\\n"
                "  window.__scrollScrubDebug = { progress: 0, mediaTime: 0, ready: true };\\n"
                "  addEventListener('scroll', () => { window.__scrollScrubDebug.mediaTime = video.currentTime; });\\n"
                "})();\\n"
            )
            completed, first_write = delegate_cli_agent.run_with_expected_output_check(
                command=[
                    sys.executable,
                    "-c",
                    f"from pathlib import Path; Path('media-repair.js').write_text({sidecar!r})",
                ],
                cwd=root,
                env={},
                timeout_seconds=5,
                expected_outputs=[expected],
                output_quality_gate=delegate_cli_agent.OutputQualityGate(
                    min_bytes=120,
                    required_substrings=("window.__scrollScrubDebug", "mediaTime"),
                ),
            )
            self.assertEqual(completed.returncode, 0)
            self.assertEqual(first_write["status"], "pass")
            self.assertEqual(first_write["output_quality"]["status"], "pass")

    def test_output_quality_gate_fails_without_expected_outputs(self) -> None:
        record = delegate_cli_agent.inspect_output_quality(
            [],
            delegate_cli_agent.OutputQualityGate(
                min_bytes=1,
                required_substrings=("window.__scrollScrubDebug",),
            ),
        )
        self.assertEqual(record["status"], "failed")
        self.assertEqual(record["failure_reason"], "no_expected_outputs")

    def test_handoff_completion_signal_rejects_placeholder_template(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            handoff = Path(tmp) / "handoff.md"
            handoff.write_text(
                "## Changed Files\n\n- pending live external CLI run\n\n"
                "## First-Write Evidence\n\n- status: pending\n",
                encoding="utf-8",
            )
            self.assertFalse(delegate_cli_agent.handoff_has_completion_signal(handoff))
            handoff.write_text(
                "## Changed Files\n\n- `SPEC.md`\n\n"
                "## Verification\n\n- checked\n\n"
                "## Risks / Followups\n\n- none\n",
                encoding="utf-8",
            )
            self.assertTrue(
                delegate_cli_agent.handoff_has_completion_signal(handoff, [Path(tmp) / "SPEC.md"])
            )

    def test_handoff_completion_signal_accepts_live_asset_handoff_headings(self) -> None:
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
            self.assertTrue(
                delegate_cli_agent.handoff_has_completion_signal(
                    handoff,
                    [Path(tmp) / "assets" / "asset-manifest.json"],
                )
            )

    def test_handoff_completion_signal_rejects_heading_only_handoff(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            handoff = Path(tmp) / "handoff.md"
            handoff.write_text(
                "## Changed Files\n\n"
                "## Verification\n\n"
                "## Risks / Followups\n\n",
                encoding="utf-8",
            )
            self.assertFalse(
                delegate_cli_agent.handoff_has_completion_signal(handoff, [Path(tmp) / "SPEC.md"])
            )

    def test_handoff_completion_signal_requires_expected_output_reference(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            handoff = Path(tmp) / "handoff.md"
            handoff.write_text(
                "## Changed Files\n\n- `OTHER.md`\n\n"
                "## Verification\n\n- checked\n\n"
                "## Risks / Followups\n\n- none\n",
                encoding="utf-8",
            )
            self.assertFalse(
                delegate_cli_agent.handoff_has_completion_signal(handoff, [Path(tmp) / "SPEC.md"])
            )

    def test_collect_run_appends_wrapper_first_write_evidence_to_handoff(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            write_profile_templates(root)
            profile = delegate_cli_agent.load_profile("frontend-pi-kimi", root)
            run = delegate_cli_agent.build_run(
                profile=profile,
                ticket="",
                checkout_mode="shared",
                prompt="Write SPEC.md",
                run_id="append-first-write-evidence",
                dry_run=False,
                artifact_dir="",
                root=root,
            )
            run.handoff_path.write_text(
                "## Changed Files\n\n- `SPEC.md`\n\n"
                "## Verification\n\n- checked\n\n"
                "## Risks / Followups\n\n- none\n",
                encoding="utf-8",
            )
            first_write = {
                "status": "pass",
                "expected_outputs": [str(root / "SPEC.md")],
                "observed_output": str(root / "SPEC.md"),
            }
            delegate_cli_agent.collect_run_artifacts(
                run,
                ["pi"],
                subprocess.CompletedProcess(["pi"], 0, "", ""),
                first_write,
            )
            handoff = run.handoff_path.read_text(encoding="utf-8")
            self.assertIn("## Wrapper First-Write Evidence", handoff)
            self.assertIn("status: `pass`", handoff)

    def test_first_write_gate_passes_when_expected_regular_file_is_modified(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            runtime_dir = root / "runtime"
            runtime_dir.mkdir()
            expected = root / "out.js"
            expected.write_text("old", encoding="utf-8")
            completed, first_write = delegate_cli_agent.run_with_first_write_gate(
                command=[
                    sys.executable,
                    "-c",
                    "from pathlib import Path; Path('out.js').write_text('new content')",
                ],
                cwd=root,
                env={},
                timeout_seconds=5,
                first_write_timeout_seconds=2,
                expected_outputs=[expected],
                runtime_dir=runtime_dir,
            )
            self.assertEqual(completed.returncode, 0)
            self.assertEqual(first_write["status"], "pass")
            self.assertEqual(first_write["observed_output"], str(expected))

    def test_first_write_gate_fails_when_expected_regular_file_is_unchanged(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            runtime_dir = root / "runtime"
            runtime_dir.mkdir()
            expected = root / "out.js"
            expected.write_text("old", encoding="utf-8")
            completed, first_write = delegate_cli_agent.run_with_first_write_gate(
                command=[sys.executable, "-c", "print('unchanged')"],
                cwd=root,
                env={},
                timeout_seconds=5,
                first_write_timeout_seconds=2,
                expected_outputs=[expected],
                runtime_dir=runtime_dir,
            )
            self.assertEqual(completed.returncode, 125)
            self.assertEqual(first_write["status"], "failed")
            self.assertEqual(first_write["failure_reason"], "process_exited_without_first_write")

    def test_first_write_gate_fails_when_expected_file_is_not_created(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            runtime_dir = root / "runtime"
            runtime_dir.mkdir()
            completed, first_write = delegate_cli_agent.run_with_first_write_gate(
                command=[sys.executable, "-c", "import time; time.sleep(2)"],
                cwd=root,
                env={},
                timeout_seconds=5,
                first_write_timeout_seconds=1,
                expected_outputs=[root / "missing.js"],
                runtime_dir=runtime_dir,
            )
            self.assertEqual(completed.returncode, 125)
            self.assertEqual(first_write["status"], "failed")
            self.assertIn("first-write gate", completed.stderr)

    def test_first_write_gate_fails_zero_exit_without_expected_file(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            runtime_dir = root / "runtime"
            runtime_dir.mkdir()
            completed, first_write = delegate_cli_agent.run_with_first_write_gate(
                command=[sys.executable, "-c", "print('no writes')"],
                cwd=root,
                env={},
                timeout_seconds=5,
                first_write_timeout_seconds=2,
                expected_outputs=[root / "missing.js"],
                runtime_dir=runtime_dir,
            )
            self.assertEqual(completed.returncode, 125)
            self.assertEqual(first_write["failure_reason"], "process_exited_without_first_write")
            self.assertIn("expected regular output file", completed.stderr)

    def test_first_write_gate_rejects_directory_expected_output(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            runtime_dir = root / "runtime"
            runtime_dir.mkdir()
            completed, first_write = delegate_cli_agent.run_with_first_write_gate(
                command=[
                    sys.executable,
                    "-c",
                    "from pathlib import Path; Path('out.js').mkdir()",
                ],
                cwd=root,
                env={},
                timeout_seconds=5,
                first_write_timeout_seconds=2,
                expected_outputs=[root / "out.js"],
                runtime_dir=runtime_dir,
            )
            self.assertEqual(completed.returncode, 125)
            self.assertEqual(first_write["status"], "failed")
            self.assertEqual(first_write["after"][str(root / "out.js")]["kind"], "directory")
            self.assertIn("expected regular output file", completed.stderr)

    def test_first_write_gate_rejects_symlink_expected_output(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            runtime_dir = root / "runtime"
            runtime_dir.mkdir()
            completed, first_write = delegate_cli_agent.run_with_first_write_gate(
                command=[
                    sys.executable,
                    "-c",
                    "from pathlib import Path; Path('real.js').write_text('ok'); Path('out.js').symlink_to('real.js')",
                ],
                cwd=root,
                env={},
                timeout_seconds=5,
                first_write_timeout_seconds=2,
                expected_outputs=[root / "out.js"],
                runtime_dir=runtime_dir,
            )
            self.assertEqual(completed.returncode, 125)
            self.assertEqual(first_write["status"], "failed")
            self.assertEqual(first_write["after"][str(root / "out.js")]["kind"], "symlink")
            self.assertIn("expected regular output file", completed.stderr)

    def test_setup_copies_media_skills_without_codex_native_imagegen(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            write_profile_templates(root)
            write_skill_bundle_manifest(
                root,
                ["frontend-craft", "image-generation", "video-generation"],
            )
            write_skill_sources(root)
            profile = delegate_cli_agent.load_profile("frontend-pi-kimi", root)
            copied = delegate_cli_agent.copy_skill_bundle(profile, root)
            copied_names = {Path(path).name for path in copied}
            self.assertEqual(copied_names, {"frontend-craft", "image-generation", "video-generation"})
            self.assertFalse((root / ".farplane" / "external-cli" / "profiles" / "frontend-pi-kimi" / "skills" / "imagegen").exists())

    def test_profile_copy_waits_for_existing_profile_lock(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            write_profile_templates(root)
            write_skill_sources(root)
            profile = delegate_cli_agent.load_profile("frontend-pi-kimi", root)
            copied: list[list[str]] = []
            started = threading.Event()

            def worker() -> None:
                started.set()
                copied.append(delegate_cli_agent.copy_skill_bundle(profile, root))

            with delegate_cli_agent.profile_write_lock(profile, root):
                thread = threading.Thread(target=worker)
                thread.start()
                self.assertTrue(started.wait(1))
                time.sleep(0.05)
                self.assertEqual(copied, [])

            thread.join(2)
            self.assertFalse(thread.is_alive())
            self.assertEqual(len(copied[0]), len(delegate_cli_agent.DEFAULT_FRONTEND_SKILLS))

    def test_setup_copies_skills_and_writes_settings(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            write_profile_templates(root)
            write_skill_sources(root)
            profile = delegate_cli_agent.load_profile("frontend-pi-kimi", root)
            copied = delegate_cli_agent.copy_skill_bundle(profile, root)
            settings = delegate_cli_agent.write_profile_settings(profile, root)
            self.assertEqual(len(copied), len(delegate_cli_agent.DEFAULT_FRONTEND_SKILLS))
            self.assertTrue(settings.exists())
            settings_text = settings.read_text(encoding="utf-8")
            self.assertIn("frontend-craft", settings_text)
            self.assertIn("agent-browser", settings_text)

    def test_command_run_can_override_skill_bundle_for_one_phase(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            write_profile_templates(root)
            write_skill_bundle_manifest(root, ["frontend-craft", "landing-page", "visual-qa"])
            write_skill_sources(root)
            original_project_root = delegate_cli_agent.project_root
            try:
                delegate_cli_agent.project_root = lambda: root
                payload = delegate_cli_agent.command_run(
                    Namespace(
                        profile="frontend-pi-kimi",
                        model="",
                        thinking="",
                        ticket="",
                        checkout="shared",
                        prompt="Write sidecar",
                        prompt_file="",
                        run_id="phase-skill-override",
                        dry_run=True,
                        artifact_dir="",
                        attach=[],
                        skill=["landing-page", "visual-qa"],
                        compact_prompt=True,
                        expect_output=[],
                        first_write_timeout_seconds=120,
                        complete_when_output_and_handoff=False,
                        completion_grace_seconds=2.0,
                        timeout_seconds=0,
                    )
                )
            finally:
                delegate_cli_agent.project_root = original_project_root

            command = payload["command"]
            mounted = [command[index + 1] for index, arg in enumerate(command) if arg == "--skill"]
            self.assertEqual(len(mounted), 2)
            self.assertTrue(all(Path(path).name in {"landing-page", "visual-qa"} for path in mounted))
            prompt_path = Path(payload["prompt_path"])
            prompt_text = prompt_path.read_text(encoding="utf-8")
            self.assertIn("landing-page", prompt_text)
            self.assertIn("visual-qa", prompt_text)
            self.assertNotIn("frontend-craft", prompt_text)
            self.assertNotIn("## Delegate System Rules", prompt_text)

    def test_dry_run_renders_prompt_command_and_durable_artifacts(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            write_profile_templates(root)
            write_skill_sources(root)
            ticket_dir = root / "tickets" / "TASK-1234"
            ticket_dir.mkdir(parents=True)
            (ticket_dir / "ticket.md").write_text("# TASK-1234: test\n", encoding="utf-8")
            profile = delegate_cli_agent.load_profile("frontend-pi-kimi", root)
            delegate_cli_agent.copy_skill_bundle(profile, root)
            run = delegate_cli_agent.build_run(
                profile=profile,
                ticket="TASK-1234",
                checkout_mode="shared",
                prompt="Build the UI",
                run_id="test-run",
                dry_run=True,
                artifact_dir="",
                root=root,
            )
            delegate_cli_agent.render_prompt(profile, run, root)
            command = delegate_cli_agent.build_pi_command(profile, run, root)
            result = delegate_cli_agent.collect_run_artifacts(run, command, None)
            self.assertEqual(result.status, "dry_run")
            self.assertEqual(command[0], "pi")
            self.assertIn("--session-dir", command)
            self.assertIn("--model", command)
            self.assertIn("-p", command)
            prompt_arg = command[command.index("-p") + 1]
            self.assertIn("Build the UI", prompt_arg)
            self.assertNotEqual(prompt_arg, f"@{run.prompt_path}")
            self.assertTrue(run.prompt_path.exists())
            self.assertTrue((run.durable_artifact_dir / "prompt.md").exists())
            self.assertTrue((run.durable_artifact_dir / "stdout.log").exists())
            self.assertTrue((run.durable_artifact_dir / "session_files.json").exists())
            command_json = json.loads((run.durable_artifact_dir / "command.json").read_text(encoding="utf-8"))
            self.assertEqual(command_json["command"][0], "pi")
            recorded_prompt = command_json["command"][command_json["command"].index("-p") + 1]
            self.assertEqual(recorded_prompt, "<prompt text redacted; see prompt.md>")
            self.assertEqual(result.command[result.command.index("-p") + 1], "<prompt text redacted; see prompt.md>")
            self.assertEqual(result.session_dir, str(run.session_dir))

    def test_doctor_reports_missing_executable_without_failing_templates(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            write_profile_templates(root)
            write_skill_sources(root)
            profile = delegate_cli_agent.load_profile("frontend-pi-kimi", root)
            payload = delegate_cli_agent.doctor_profile(profile, root)
            self.assertIn("ok", payload)
            self.assertTrue(all(payload["templates"].values()))
            self.assertTrue(all(payload["skills"].values()))
            self.assertIn("install_hint", payload)
            self.assertIn("live_ready", payload)

    def test_run_accepts_model_override(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            write_profile_templates(root)
            write_skill_sources(root)
            profile = delegate_cli_agent.load_profile("frontend-pi-kimi", root)
            profile = replace(profile, model="openrouter/example-model")
            delegate_cli_agent.copy_skill_bundle(profile, root)
            run = delegate_cli_agent.build_run(
                profile=profile,
                ticket="",
                checkout_mode="shared",
                prompt="Build the UI",
                run_id="override-run",
                dry_run=True,
                artifact_dir="",
                root=root,
            )
            delegate_cli_agent.render_prompt(profile, run, root)
            command = delegate_cli_agent.build_pi_command(profile, run, root)
            self.assertIn("openrouter/example-model", command)

    def test_worktree_dry_run_records_isolated_checkout_path(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            write_profile_templates(root)
            write_skill_sources(root)
            profile = delegate_cli_agent.load_profile("frontend-pi-kimi", root)
            run = delegate_cli_agent.build_run(
                profile=profile,
                ticket="",
                checkout_mode="worktree",
                prompt="Build the UI",
                run_id="worktree-run",
                dry_run=True,
                artifact_dir="",
                root=root,
            )
            self.assertEqual(run.checkout_path, run.runtime_dir / "checkout")
            self.assertEqual(run.session_dir, run.runtime_dir / "sessions")
            self.assertFalse(run.checkout_path.exists())

    def test_rejects_path_traversal_run_id(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            write_profile_templates(root)
            profile = delegate_cli_agent.load_profile("frontend-pi-kimi", root)
            with self.assertRaises(SystemExit):
                delegate_cli_agent.build_run(
                    profile=profile,
                    ticket="",
                    checkout_mode="shared",
                    prompt="Build the UI",
                    run_id="../escape",
                    dry_run=True,
                    artifact_dir="",
                    root=root,
                )

    def test_rejects_missing_ticket(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            write_profile_templates(root)
            profile = delegate_cli_agent.load_profile("frontend-pi-kimi", root)
            with self.assertRaises(SystemExit):
                delegate_cli_agent.build_run(
                    profile=profile,
                    ticket="TASK-404",
                    checkout_mode="shared",
                    prompt="Build the UI",
                    run_id="missing-ticket",
                    dry_run=True,
                    artifact_dir="",
                    root=root,
                )

    def test_render_prompt_includes_append_system_rules(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            write_profile_templates(root)
            write_skill_sources(root)
            profile = delegate_cli_agent.load_profile("frontend-pi-kimi", root)
            run = delegate_cli_agent.build_run(
                profile=profile,
                ticket="",
                checkout_mode="shared",
                prompt="Build the UI",
                run_id="system-rules",
                dry_run=True,
                artifact_dir="",
                root=root,
            )
            prompt_path = delegate_cli_agent.render_prompt(profile, run, root)
            self.assertIn("system", prompt_path.read_text(encoding="utf-8"))

    def test_missing_live_env_reports_required_provider_key(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            write_profile_templates(root)
            profile = delegate_cli_agent.load_profile("frontend-pi-kimi", root)
            self.assertEqual(
                delegate_cli_agent.missing_live_env(profile, {}, set()),
                ["OPENROUTER_API_KEY"],
            )
            self.assertEqual(
                delegate_cli_agent.missing_live_env(profile, {"OPENROUTER_API_KEY": "set"}, set()),
                [],
            )
            self.assertEqual(
                delegate_cli_agent.missing_live_env(profile, {}, {"openrouter"}),
                [],
            )

    def test_timeout_expired_collects_partial_output(self) -> None:
        completed = subprocess.CompletedProcess(
            ["pi"],
            124,
            "partial out",
            "partial err\nexternal CLI run timed out after 1 seconds\n",
        )
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            write_profile_templates(root)
            profile = delegate_cli_agent.load_profile("frontend-pi-kimi", root)
            run = delegate_cli_agent.build_run(
                profile=profile,
                ticket="",
                checkout_mode="shared",
                prompt="Build the UI",
                run_id="timeout-run",
                dry_run=False,
                artifact_dir="",
                root=root,
            )
            result = delegate_cli_agent.collect_run_artifacts(run, ["pi"], completed)
            self.assertEqual(result.exit_code, 124)
            self.assertEqual(result.status, "failed")
            self.assertIn("timed out", (run.runtime_dir / "stderr.log").read_text(encoding="utf-8"))

    def test_command_run_emits_first_write_artifact_through_public_path(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            write_profile_templates(root)
            write_skill_bundle_manifest(root, ["frontend-craft"])
            write_skill_sources(root)
            original_project_root = delegate_cli_agent.project_root
            original_missing_live_env = delegate_cli_agent.missing_live_env
            original_build_pi_command = delegate_cli_agent.build_pi_command

            def fake_command(
                profile: delegate_cli_agent.DelegateProfile,
                run: delegate_cli_agent.DelegateRun,
                root_arg: Path | None = None,
            ) -> list[str]:
                return [
                    sys.executable,
                    "-c",
                    "from pathlib import Path; Path('out.js').write_text('ok')",
                ]

            try:
                delegate_cli_agent.project_root = lambda: root
                delegate_cli_agent.missing_live_env = lambda profile: []
                delegate_cli_agent.build_pi_command = fake_command
                payload = delegate_cli_agent.command_run(
                    Namespace(
                        profile="frontend-pi-kimi",
                        model="",
                        thinking="",
                        ticket="",
                        checkout="shared",
                        prompt="Write out.js",
                        prompt_file="",
                        run_id="public-first-write",
                        dry_run=False,
                        artifact_dir="",
                        attach=[],
                        expect_output=["out.js"],
                        first_write_timeout_seconds=5,
                        complete_when_output_and_handoff=False,
                        completion_grace_seconds=2.0,
                        timeout_seconds=10,
                    )
                )
            finally:
                delegate_cli_agent.project_root = original_project_root
                delegate_cli_agent.missing_live_env = original_missing_live_env
                delegate_cli_agent.build_pi_command = original_build_pi_command

            self.assertEqual(payload["status"], "success")
            first_write_path = Path(payload["first_write_path"])
            self.assertTrue(first_write_path.exists())
            first_write = json.loads(first_write_path.read_text(encoding="utf-8"))
            self.assertEqual(first_write["status"], "pass")
            self.assertEqual(Path(first_write["observed_output"]).name, "out.js")

    def test_command_run_precreates_expected_output_parent_directories(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            write_profile_templates(root)
            write_skill_bundle_manifest(root, ["frontend-craft"])
            write_skill_sources(root)
            original_project_root = delegate_cli_agent.project_root
            original_missing_live_env = delegate_cli_agent.missing_live_env
            original_build_pi_command = delegate_cli_agent.build_pi_command

            def fake_command(
                profile: delegate_cli_agent.DelegateProfile,
                run: delegate_cli_agent.DelegateRun,
                root_arg: Path | None = None,
            ) -> list[str]:
                return [
                    sys.executable,
                    "-c",
                    "from pathlib import Path; "
                    "assert Path('nested/out').is_dir(); "
                    "Path('nested/out/file.js').write_text('ok')",
                ]

            try:
                delegate_cli_agent.project_root = lambda: root
                delegate_cli_agent.missing_live_env = lambda profile: []
                delegate_cli_agent.build_pi_command = fake_command
                payload = delegate_cli_agent.command_run(
                    Namespace(
                        profile="frontend-pi-kimi",
                        model="",
                        thinking="",
                        ticket="",
                        checkout="shared",
                        prompt="Write nested/out/file.js",
                        prompt_file="",
                        run_id="public-first-write-nested-parent",
                        dry_run=False,
                        artifact_dir="",
                        attach=[],
                        expect_output=["nested/out/file.js"],
                        first_write_timeout_seconds=5,
                        complete_when_output_and_handoff=False,
                        completion_grace_seconds=2.0,
                        timeout_seconds=10,
                    )
                )
            finally:
                delegate_cli_agent.project_root = original_project_root
                delegate_cli_agent.missing_live_env = original_missing_live_env
                delegate_cli_agent.build_pi_command = original_build_pi_command

            self.assertEqual(payload["status"], "success")
            first_write = json.loads(Path(payload["first_write_path"]).read_text(encoding="utf-8"))
            self.assertEqual(first_write["status"], "pass")
            self.assertEqual(Path(first_write["observed_output"]).name, "file.js")

    def test_command_run_timeout_zero_still_emits_first_write_artifact(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            write_profile_templates(root)
            write_skill_bundle_manifest(root, ["frontend-craft"])
            write_skill_sources(root)
            original_project_root = delegate_cli_agent.project_root
            original_missing_live_env = delegate_cli_agent.missing_live_env
            original_build_pi_command = delegate_cli_agent.build_pi_command

            def fake_command(
                profile: delegate_cli_agent.DelegateProfile,
                run: delegate_cli_agent.DelegateRun,
                root_arg: Path | None = None,
            ) -> list[str]:
                return [
                    sys.executable,
                    "-c",
                    "from pathlib import Path; Path('out.js').write_text('ok')",
                ]

            try:
                delegate_cli_agent.project_root = lambda: root
                delegate_cli_agent.missing_live_env = lambda profile: []
                delegate_cli_agent.build_pi_command = fake_command
                payload = delegate_cli_agent.command_run(
                    Namespace(
                        profile="frontend-pi-kimi",
                        model="",
                        thinking="",
                        ticket="",
                        checkout="shared",
                        prompt="Write out.js",
                        prompt_file="",
                        run_id="public-first-write-timeout-zero",
                        dry_run=False,
                        artifact_dir="",
                        attach=[],
                        expect_output=["out.js"],
                        first_write_timeout_seconds=0,
                        complete_when_output_and_handoff=False,
                        completion_grace_seconds=2.0,
                        timeout_seconds=10,
                    )
                )
            finally:
                delegate_cli_agent.project_root = original_project_root
                delegate_cli_agent.missing_live_env = original_missing_live_env
                delegate_cli_agent.build_pi_command = original_build_pi_command

            self.assertEqual(payload["status"], "success")
            first_write_path = Path(payload["first_write_path"])
            first_write = json.loads(first_write_path.read_text(encoding="utf-8"))
            self.assertEqual(first_write["status"], "pass")
            self.assertEqual(first_write["timeout_seconds"], 0)
            self.assertEqual(Path(first_write["observed_output"]).name, "out.js")

    def test_command_run_timeout_zero_fails_without_expected_regular_file_change(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            write_profile_templates(root)
            write_skill_bundle_manifest(root, ["frontend-craft"])
            write_skill_sources(root)
            (root / "out.js").write_text("old", encoding="utf-8")
            original_project_root = delegate_cli_agent.project_root
            original_missing_live_env = delegate_cli_agent.missing_live_env
            original_build_pi_command = delegate_cli_agent.build_pi_command

            def fake_command(
                profile: delegate_cli_agent.DelegateProfile,
                run: delegate_cli_agent.DelegateRun,
                root_arg: Path | None = None,
            ) -> list[str]:
                return [sys.executable, "-c", "print('no write')"]

            try:
                delegate_cli_agent.project_root = lambda: root
                delegate_cli_agent.missing_live_env = lambda profile: []
                delegate_cli_agent.build_pi_command = fake_command
                payload = delegate_cli_agent.command_run(
                    Namespace(
                        profile="frontend-pi-kimi",
                        model="",
                        thinking="",
                        ticket="",
                        checkout="shared",
                        prompt="Write out.js",
                        prompt_file="",
                        run_id="public-first-write-timeout-zero-no-change",
                        dry_run=False,
                        artifact_dir="",
                        attach=[],
                        expect_output=["out.js"],
                        first_write_timeout_seconds=0,
                        complete_when_output_and_handoff=False,
                        completion_grace_seconds=2.0,
                        timeout_seconds=10,
                    )
                )
            finally:
                delegate_cli_agent.project_root = original_project_root
                delegate_cli_agent.missing_live_env = original_missing_live_env
                delegate_cli_agent.build_pi_command = original_build_pi_command

            self.assertEqual(payload["status"], "failed")
            first_write_path = Path(payload["first_write_path"])
            first_write = json.loads(first_write_path.read_text(encoding="utf-8"))
            self.assertEqual(first_write["status"], "failed")
            self.assertEqual(first_write["failure_reason"], "process_exited_without_first_write")

    def test_command_run_can_stop_after_output_and_handoff(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            write_profile_templates(root)
            write_skill_bundle_manifest(root, ["frontend-craft"])
            write_skill_sources(root)
            original_project_root = delegate_cli_agent.project_root
            original_missing_live_env = delegate_cli_agent.missing_live_env
            original_build_pi_command = delegate_cli_agent.build_pi_command

            def fake_command(
                profile: delegate_cli_agent.DelegateProfile,
                run: delegate_cli_agent.DelegateRun,
                root_arg: Path | None = None,
            ) -> list[str]:
                script = (
                    "from pathlib import Path\n"
                    "import time\n"
                    "Path('SPEC.md').write_text('# Spec\\n')\n"
                    f"Path({str(run.handoff_path)!r}).write_text("
                    "'## Changed Files\\n\\n- `SPEC.md`\\n\\n"
                    "## Verification\\n\\n- checked\\n\\n"
                    "## Risks / Followups\\n\\n- none\\n', encoding='utf-8')\n"
                    "time.sleep(10)\n"
                )
                return [sys.executable, "-c", script]

            try:
                delegate_cli_agent.project_root = lambda: root
                delegate_cli_agent.missing_live_env = lambda profile: []
                delegate_cli_agent.build_pi_command = fake_command
                started = time.monotonic()
                payload = delegate_cli_agent.command_run(
                    Namespace(
                        profile="frontend-pi-kimi",
                        model="",
                        thinking="",
                        ticket="",
                        checkout="shared",
                        prompt="Write SPEC.md",
                        prompt_file="",
                        run_id="public-complete-on-handoff",
                        dry_run=False,
                        artifact_dir="",
                        attach=[],
                        expect_output=["SPEC.md"],
                        first_write_timeout_seconds=5,
                        complete_when_output_and_handoff=True,
                        completion_grace_seconds=0,
                        timeout_seconds=20,
                    )
                )
            finally:
                delegate_cli_agent.project_root = original_project_root
                delegate_cli_agent.missing_live_env = original_missing_live_env
                delegate_cli_agent.build_pi_command = original_build_pi_command

            self.assertLess(time.monotonic() - started, 5)
            self.assertEqual(payload["status"], "success")
            first_write = json.loads(Path(payload["first_write_path"]).read_text(encoding="utf-8"))
            self.assertEqual(first_write["completion_reason"], "expected_output_and_handoff")

    def test_run_attachments_are_validated_recorded_and_passed_to_pi(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            write_profile_templates(root)
            write_skill_sources(root)
            attachment = root / "proof.png"
            attachment.write_bytes(b"not really a png")
            profile = delegate_cli_agent.load_profile("frontend-pi-kimi", root)
            run = delegate_cli_agent.build_run(
                profile=profile,
                ticket="",
                checkout_mode="shared",
                prompt="Review attached screenshot",
                run_id="attachment-run",
                dry_run=True,
                artifact_dir="",
                attachments=[str(attachment)],
                root=root,
            )
            delegate_cli_agent.render_prompt(profile, run, root)
            command = delegate_cli_agent.build_pi_command(profile, run, root)
            result = delegate_cli_agent.collect_run_artifacts(run, command, None)
            resolved_attachment = str(attachment.resolve())
            self.assertIn(f"@{resolved_attachment}", command)
            prompt_arg = command[command.index("-p") + 1]
            self.assertIn("Review attached screenshot", prompt_arg)
            self.assertNotIn(f"@{run.prompt_path}", command)
            self.assertIn(f"@{resolved_attachment}", result.command)
            self.assertEqual(result.attachments, [resolved_attachment])
            self.assertTrue((run.runtime_dir / "attachments.json").exists())


if __name__ == "__main__":
    unittest.main()
