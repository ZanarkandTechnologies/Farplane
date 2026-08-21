from __future__ import annotations

import sys
import tempfile
import unittest
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parents[2]
CORE_DIR = ROOT / "bin" / "core"
if str(CORE_DIR) not in sys.path:
    sys.path.insert(0, str(CORE_DIR))

from farplane_capability_profiles import (
    CapabilityProfileError,
    global_profiles_path,
    project_profiles_path,
    record_capability_profile_snapshot,
    resolve_capability_profiles,
    write_capability_profiles,
)


class CapabilityProfilesTest(unittest.TestCase):
    def setUp(self) -> None:
        self.temporary = tempfile.TemporaryDirectory()
        self.root = Path(self.temporary.name)
        self.project = self.root / "project"
        self.project.mkdir()
        self.farplane_home = self.root / "farplane-home"
        self.codex_home = self.root / "codex-home"
        self.codex_home.mkdir()
        (self.codex_home / "config.toml").write_text(
            """[[skills.config]]
name = "research"
enabled = true

[[skills.config]]
name = "eval"
enabled = true

[mcp_servers.Ref]
url = "https://example.test/ref"

[mcp_servers.safe]
command = "safe"
""",
            encoding="utf-8",
        )

    def tearDown(self) -> None:
        self.temporary.cleanup()

    def resolve(self) -> dict:
        return resolve_capability_profiles(
            self.project,
            farplane_home=self.farplane_home,
            codex_home=self.codex_home,
        )

    def test_missing_documents_mean_full_access_without_runtime_override(self) -> None:
        payload = self.resolve()

        self.assertEqual(payload["enforcement"]["state"], "full_access")
        self.assertIsNone(payload["active_profile"])
        self.assertNotIn("thread_start_config", payload["enforcement"])

    def test_global_profile_resolves_portable_allowlist(self) -> None:
        global_path = global_profiles_path(self.farplane_home)
        global_path.parent.mkdir(parents=True)
        global_path.write_text(
            yaml.safe_dump(
                {
                    "version": 1,
                    "profiles": {
                        "research-only": {
                            "label": "Research only",
                            "allow": {"skill_ids": ["research"], "mcp_server_ids": ["Ref"]},
                        }
                    },
                },
                sort_keys=False,
            ),
            encoding="utf-8",
        )
        project_path = project_profiles_path(self.project)
        project_path.parent.mkdir()
        project_path.write_text("version: 1\nprofiles: {}\nactive_profile_ref: global:research-only\n", encoding="utf-8")

        payload = self.resolve()
        self.assertEqual(payload["active_profile"]["ref"], "global:research-only")
        self.assertEqual(
            payload["active_profile"]["allow"],
            {"skill_ids": ["research"], "mcp_server_ids": ["Ref"]},
        )
        self.assertNotIn("thread_start_config", payload["enforcement"])

    def test_project_extension_is_intersected_with_its_global_parent(self) -> None:
        write_capability_profiles(
            self.project,
            "global",
            {
                "version": 1,
                "profiles": {
                    "safe-base": {
                        "label": "Safe base",
                        "allow": {"skill_ids": ["research"], "mcp_server_ids": ["Ref"]},
                    }
                },
            },
            farplane_home=self.farplane_home,
            codex_home=self.codex_home,
        )
        payload = write_capability_profiles(
            self.project,
            "project",
            {
                "version": 1,
                "profiles": {
                    "customer-safe": {
                        "label": "Customer safe",
                        "extends": "global:safe-base",
                        "allow": {"skill_ids": ["eval"], "mcp_server_ids": ["safe"]},
                    }
                },
                "active_profile_ref": "project:customer-safe",
            },
            farplane_home=self.farplane_home,
            codex_home=self.codex_home,
        )

        self.assertEqual(payload["active_profile"]["allow"], {"skill_ids": [], "mcp_server_ids": []})

    def test_runtime_specific_ids_remain_portable_until_launch(self) -> None:
        path = project_profiles_path(self.project)
        path.parent.mkdir()
        payload = write_capability_profiles(
            self.project,
            "project",
            {
                "version": 1,
                "profiles": {
                    "portable": {
                        "label": "Portable",
                        "allow": {
                            "skill_ids": ["plugin-owned-skill"],
                            "mcp_server_ids": ["future-runtime-server"],
                        },
                    }
                },
                "active_profile_ref": "project:portable",
            },
            farplane_home=self.farplane_home,
            codex_home=self.codex_home,
        )

        self.assertEqual(
            payload["active_profile"]["allow"],
            {
                "skill_ids": ["plugin-owned-skill"],
                "mcp_server_ids": ["future-runtime-server"],
            },
        )

    def test_duplicate_yaml_key_is_rejected(self) -> None:
        path = project_profiles_path(self.project)
        path.parent.mkdir()
        path.write_text("version: 1\nprofiles: {}\nprofiles: {}\n", encoding="utf-8")

        with self.assertRaisesRegex(CapabilityProfileError, "duplicate_key"):
            self.resolve()

    def test_global_document_cannot_bind_a_project(self) -> None:
        with self.assertRaisesRegex(CapabilityProfileError, "active_profile_ref_not_allowed"):
            write_capability_profiles(
                self.project,
                "global",
                {"version": 1, "profiles": {}, "active_profile_ref": "global:any"},
                farplane_home=self.farplane_home,
                codex_home=self.codex_home,
            )

    def test_thread_policy_snapshot_is_immutable_and_idempotent(self) -> None:
        digest = "a" * 64
        first = record_capability_profile_snapshot(
            self.project,
            thread_id="thread-123",
            profile_ref="project:customer-safe",
            policy_digest=digest,
        )
        second = record_capability_profile_snapshot(
            self.project,
            thread_id="thread-123",
            profile_ref="project:customer-safe",
            policy_digest=digest,
        )

        self.assertTrue(first["recorded"])
        self.assertFalse(second["recorded"])
        with self.assertRaisesRegex(CapabilityProfileError, "snapshot_conflict"):
            record_capability_profile_snapshot(
                self.project,
                thread_id="thread-123",
                profile_ref=None,
                policy_digest=digest,
            )


if __name__ == "__main__":
    unittest.main()
