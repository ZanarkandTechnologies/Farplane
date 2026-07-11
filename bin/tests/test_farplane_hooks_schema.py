from __future__ import annotations

import json
import tempfile
import unittest
from pathlib import Path

from bin.validators.check_farplane_project_files import validate_hooks_file


class FarplaneHooksSchemaTests(unittest.TestCase):
    def test_file_event_contract_is_valid(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            farplane = root / "farplane"
            farplane.mkdir()
            path = farplane / "hooks.json"
            path.write_text(
                json.dumps(
                    {
                        "version": 1,
                        "file_events": {
                            "enabled": True,
                            "events": ["farplane.ticket.completed"],
                            "patterns": ["tickets/TASK-*/ticket.md"],
                        },
                    }
                ),
                encoding="utf-8",
            )

            self.assertEqual(validate_hooks_file(root, path), [])

    def test_legacy_or_unsafe_contract_is_rejected(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            farplane = root / "farplane"
            farplane.mkdir()
            path = farplane / "hooks.json"
            path.write_text('{"version": 1, "hooks": {}}', encoding="utf-8")

            legacy_errors = validate_hooks_file(root, path)
            self.assertTrue(any("unsupported top-level keys: hooks" in row for row in legacy_errors))
            self.assertTrue(any("file_events must be an object" in row for row in legacy_errors))

            path.write_text(
                '{"version": 1, "file_events": {"enabled": true, '
                '"events": ["farplane.unknown"], "patterns": ["../secret"]}}',
                encoding="utf-8",
            )
            unsafe_errors = validate_hooks_file(root, path)
            self.assertTrue(any("unsupported values: farplane.unknown" in row for row in unsafe_errors))
            self.assertTrue(any("unsafe values: ../secret" in row for row in unsafe_errors))


if __name__ == "__main__":
    unittest.main()
