from __future__ import annotations

import json
import subprocess
import sys
import tempfile
import threading
import time
import unittest
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
        "Profile {{profile_name}}\nTicket {{ticket_ref}}\n{{append_system}}\n{{skill_list}}\n{{ticket_context}}\n{{handoff_path}}\n",
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
            self.assertFalse((root / ".harness" / "external-cli" / "profiles" / "frontend-pi-kimi" / "skills" / "imagegen").exists())

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
            self.assertTrue(run.prompt_path.exists())
            self.assertTrue((run.durable_artifact_dir / "prompt.md").exists())
            self.assertTrue((run.durable_artifact_dir / "stdout.log").exists())
            self.assertTrue((run.durable_artifact_dir / "session_files.json").exists())
            command_json = json.loads((run.durable_artifact_dir / "command.json").read_text(encoding="utf-8"))
            self.assertEqual(command_json["command"][0], "pi")
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
            self.assertEqual(result.attachments, [resolved_attachment])
            self.assertTrue((run.runtime_dir / "attachments.json").exists())


if __name__ == "__main__":
    unittest.main()
