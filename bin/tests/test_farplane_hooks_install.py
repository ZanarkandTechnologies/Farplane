from __future__ import annotations

import sys
import tempfile
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
BIN_DIR = ROOT / "bin"
ADDED_BIN_PATH = str(BIN_DIR) not in sys.path
if ADDED_BIN_PATH:
    sys.path.insert(0, str(BIN_DIR))

import farplane

if ADDED_BIN_PATH:
    sys.path.remove(str(BIN_DIR))


class FarplaneHooksInstallTests(unittest.TestCase):
    def test_install_retires_obsolete_post_tool_hook_links(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            codex_home = Path(tmp)
            hooks = codex_home / "hooks"
            hooks.mkdir(parents=True)
            for name in farplane.RETIRED_HOOK_FILES:
                (hooks / name).symlink_to(ROOT / "hooks" / name)

            payload = farplane.install_hooks(codex_home)

            self.assertTrue(payload["ok"])
            for name in farplane.RETIRED_HOOK_FILES:
                self.assertFalse((hooks / name).is_symlink())
            retired = [row for row in payload["operations"] if row.get("retired")]
            self.assertEqual(len(retired), 2)
            self.assertTrue(all(Path(row["backup"]).is_symlink() for row in retired))


if __name__ == "__main__":
    unittest.main()
