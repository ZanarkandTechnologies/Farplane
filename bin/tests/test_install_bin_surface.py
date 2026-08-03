from __future__ import annotations

import re
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
INSTALL = ROOT / "install.sh"


def shell_array(name: str) -> tuple[str, ...]:
    text = INSTALL.read_text(encoding="utf-8")
    match = re.search(rf"^{name}=\(\n(?P<body>.*?)^\)$", text, re.MULTILINE | re.DOTALL)
    if not match:
        raise AssertionError(f"missing shell array: {name}")
    return tuple(line.strip() for line in match.group("body").splitlines() if line.strip())


class InstallBinSurfaceTests(unittest.TestCase):
    def test_installed_bin_allowlist_contains_only_cli_and_required_edges(self) -> None:
        self.assertEqual(
            shell_array("INSTALL_BIN_FILES"),
            ("_compat.py", "capture_user_turn.py", "farplane", "farplane.py", "notify.py"),
        )

    def test_removed_standalone_commands_are_retired_on_install(self) -> None:
        retired = set(shell_array("RETIRED_INSTALL_PATHS"))
        self.assertTrue(
            {
                "bin/ticket-runtime",
                "bin/farplane_boards.py",
                "bin/farplane_compute.py",
                "bin/farplane_invocation.py",
                "bin/runtime_telemetry.py",
                "bin/user_turn.py",
                "skills/pr-runtime",
                "skills/farplane-invocation",
            }.issubset(retired)
        )

    def test_installed_hook_allowlist_contains_checkout_guard(self) -> None:
        self.assertEqual(
            shell_array("INSTALL_HOOK_FILES"),
            ("farplane_console_ping.py", "shared_checkout_guard.py"),
        )

    def test_removed_runtime_and_invocation_sources_do_not_exist(self) -> None:
        removed = (
            "bin/ticket-runtime",
            "bin/core/farplane_ticket_runtime.py",
            "bin/core/farplane_boards.py",
            "bin/core/farplane_compute.py",
            "bin/core/farplane_invocation.py",
            "skills/pr-runtime/SKILL.md",
            "skills/farplane-invocation/SKILL.md",
            "WORKFLOW.md",
        )
        self.assertEqual([path for path in removed if (ROOT / path).exists()], [])


if __name__ == "__main__":
    unittest.main()
