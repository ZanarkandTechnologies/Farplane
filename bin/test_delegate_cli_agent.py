from __future__ import annotations

import json
import sys
import tempfile
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
            self.assertEqual(profile.default_checkout, "worktree")

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
            self.assertIn("--model", command)
            self.assertTrue(run.prompt_path.exists())
            self.assertTrue((run.durable_artifact_dir / "prompt.md").exists())
            self.assertTrue((run.durable_artifact_dir / "stdout.log").exists())
            command_json = json.loads((run.durable_artifact_dir / "command.json").read_text(encoding="utf-8"))
            self.assertEqual(command_json["command"][0], "pi")

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
                delegate_cli_agent.missing_live_env(profile, {}),
                ["OPENROUTER_API_KEY"],
            )
            self.assertEqual(
                delegate_cli_agent.missing_live_env(profile, {"OPENROUTER_API_KEY": "set"}),
                [],
            )


if __name__ == "__main__":
    unittest.main()
