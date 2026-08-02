from __future__ import annotations

import hashlib
import importlib.util
import json
import tempfile
import unittest
from pathlib import Path

from PIL import Image


MODULE_PATH = Path(__file__).with_name("visual_workspace.py")
SPEC = importlib.util.spec_from_file_location("visual_workspace", MODULE_PATH)
assert SPEC and SPEC.loader
visual_workspace = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(visual_workspace)


def digest(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


class VisualWorkspaceTest(unittest.TestCase):
    def setUp(self) -> None:
        self.tempdir = tempfile.TemporaryDirectory()
        self.root = Path(self.tempdir.name)
        self.source = self.root / "input.png"
        Image.new("RGB", (120, 80), "white").save(self.source)
        self.workspace = self.root / "workspace"

    def tearDown(self) -> None:
        self.tempdir.cleanup()

    def test_init_preserves_source_and_creates_checkpoint_zero(self) -> None:
        state = visual_workspace.init_workspace(self.source, self.workspace)

        self.assertEqual(state["checkpoint_count"], 1)
        self.assertEqual(state["operation_receipt_count"], 0)
        self.assertEqual((state["width"], state["height"]), (120, 80))
        self.assertEqual(digest(self.workspace / "source.png"), digest(self.workspace / "checkpoints/000.png"))
        self.assertEqual(digest(self.workspace / "latest.png"), digest(self.workspace / "checkpoints/000.png"))

    def test_sequential_batches_keep_prior_checkpoints_immutable(self) -> None:
        visual_workspace.init_workspace(self.source, self.workspace)
        source_digest = digest(self.workspace / "source.png")
        zero_digest = digest(self.workspace / "checkpoints/000.png")

        first = visual_workspace.apply_operations(
            self.workspace,
            {
                "operations": [
                    {"op": "point", "at": [0.2, 0.3], "label": "one"},
                    {"op": "box", "box": [0.5, 0.2, 0.8, 0.7], "label": "target"},
                ]
            },
        )
        one_digest = digest(self.workspace / "checkpoints/001.png")
        self.assertEqual(first["checkpoint_count"], 2)
        self.assertEqual(digest(self.workspace / "latest.png"), one_digest)

        second = visual_workspace.apply_operations(
            self.workspace,
            {
                "operations": [
                    {"op": "path", "points": [[0.1, 0.8], [0.4, 0.6], [0.7, 0.8]]},
                    {"op": "arrow", "points": [[0.2, 0.1], [0.7, 0.1]], "label": "direction"},
                    {"op": "label", "at": [0.02, 0.02], "text": "scan"},
                    {"op": "grid", "rows": 3, "columns": 4, "color": "#0066ff"},
                ]
            },
        )

        self.assertEqual(second["checkpoint_count"], 3)
        self.assertEqual(second["operation_receipt_count"], 2)
        self.assertEqual(digest(self.workspace / "source.png"), source_digest)
        self.assertEqual(digest(self.workspace / "checkpoints/000.png"), zero_digest)
        self.assertEqual(digest(self.workspace / "checkpoints/001.png"), one_digest)
        self.assertEqual(digest(self.workspace / "latest.png"), digest(self.workspace / "checkpoints/002.png"))

        receipt = json.loads((self.workspace / "operations/002.json").read_text())
        self.assertEqual(receipt["base_checkpoint"], "checkpoints/001.png")
        self.assertEqual(receipt["result_checkpoint"], "checkpoints/002.png")
        self.assertEqual(len(receipt["operations"]), 4)

    def test_crop_changes_latest_dimensions_without_losing_history(self) -> None:
        visual_workspace.init_workspace(self.source, self.workspace)
        zero_digest = digest(self.workspace / "checkpoints/000.png")

        state = visual_workspace.apply_operations(
            self.workspace,
            {"operations": [{"op": "crop", "box": [0.25, 0.25, 0.75, 0.75]}]},
        )

        self.assertEqual((state["width"], state["height"]), (60, 40))
        self.assertEqual(digest(self.workspace / "checkpoints/000.png"), zero_digest)
        with Image.open(self.workspace / "source.png") as source:
            self.assertEqual(source.size, (120, 80))

    def test_invalid_batch_publishes_nothing(self) -> None:
        visual_workspace.init_workspace(self.source, self.workspace)
        latest_digest = digest(self.workspace / "latest.png")

        with self.assertRaises(visual_workspace.WorkspaceError):
            visual_workspace.apply_operations(
                self.workspace,
                {"operations": [{"op": "point", "at": [1.4, 0.2]}]},
            )

        state = visual_workspace.inspect_workspace(self.workspace)
        self.assertEqual(state["checkpoint_count"], 1)
        self.assertEqual(state["operation_receipt_count"], 0)
        self.assertEqual(digest(self.workspace / "latest.png"), latest_digest)

    def test_reinitialize_and_missing_receipt_are_rejected(self) -> None:
        visual_workspace.init_workspace(self.source, self.workspace)
        with self.assertRaises(visual_workspace.WorkspaceError):
            visual_workspace.init_workspace(self.source, self.workspace)

        visual_workspace.apply_operations(
            self.workspace,
            {"operations": [{"op": "label", "at": [0.1, 0.1], "text": "x"}]},
        )
        (self.workspace / "operations/001.json").unlink()
        with self.assertRaises(visual_workspace.WorkspaceError):
            visual_workspace.inspect_workspace(self.workspace)


if __name__ == "__main__":
    unittest.main()
