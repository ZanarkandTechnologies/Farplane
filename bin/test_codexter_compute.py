from __future__ import annotations

import sys
import tempfile
import unittest
from dataclasses import dataclass
from pathlib import Path

ROOT = Path(__file__).resolve().parent
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from codexter_compute import select_compute


@dataclass(frozen=True)
class Item:
    identifier: str = "TASK-1234"
    approval_required: bool = False
    blocked_by: tuple[str, ...] = ()
    depends_on: tuple[str, ...] = ()
    status: str = "review"
    compute_target: str | None = None


class ComputeSelectorTests(unittest.TestCase):
    def decide(
        self,
        *,
        item: Item = Item(),
        envelope_target: str | None = None,
        phase: str = "planning",
        workflow_default: str = "local_shared",
        workflow_allowed: tuple[str, ...] = ("local_shared", "local_worktree"),
        root: Path,
        resolved_dependencies: tuple[str, ...] = (),
    ):
        return select_compute(
            item,
            envelope_compute_target=envelope_target,
            phase=phase,
            workflow_default=workflow_default,
            workflow_allowed=workflow_allowed,
            root=root,
            resolved_dependencies=resolved_dependencies,
        )

    def test_envelope_override_wins_over_ticket_and_workflow(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            decision = self.decide(
                item=Item(compute_target="local_worktree"),
                envelope_target="local_shared",
                workflow_default="local_worktree",
                root=Path(tmp),
            )

            self.assertTrue(decision.allowed)
            self.assertEqual(decision.target, "local_shared")
            self.assertEqual(decision.blocker_codes, ())

    def test_ticket_override_wins_over_workflow_default(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            runtime_path = root / ".harness" / "state" / "tickets" / "TASK-1234.runtime.json"
            runtime_path.parent.mkdir(parents=True)
            runtime_path.write_text("{}\n", encoding="utf-8")

            decision = self.decide(item=Item(compute_target="local_worktree"), root=root)

            self.assertTrue(decision.allowed)
            self.assertEqual(decision.target, "local_worktree")
            self.assertEqual(decision.runtime_record_path, str(runtime_path))
            self.assertIn("ticket_runtime.py ensure", " ".join(decision.required_setup))

    def test_worktree_blocks_until_runtime_record_exists(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            decision = self.decide(
                item=Item(compute_target="local_worktree"),
                root=Path(tmp),
            )

            self.assertFalse(decision.allowed)
            self.assertIn("missing_worktree_runtime", decision.blocker_codes)
            self.assertIn("local_worktree requires", " ".join(decision.runtime_hints))

    def test_future_targets_remain_unsupported_even_when_workflow_allows_them(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            decision = self.decide(
                envelope_target="symphony",
                workflow_allowed=("local_shared", "local_worktree", "symphony"),
                root=Path(tmp),
            )

            self.assertFalse(decision.allowed)
            self.assertIn("unsupported_target", decision.blocker_codes)
            self.assertIn("future external adapter", decision.reason)
            self.assertIn("normal Codex with Codexter installed", decision.handoff)

    def test_codex_cloud_target_blocks_with_external_handoff_hint(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            decision = self.decide(
                envelope_target="codex_cloud",
                workflow_allowed=("local_shared", "local_worktree", "codex_cloud"),
                root=Path(tmp),
            )

            self.assertFalse(decision.allowed)
            self.assertIn("unsupported_target", decision.blocker_codes)
            self.assertIn("future external adapter", decision.reason)
            self.assertIn("normal Codex with Codexter installed", decision.handoff)

    def test_build_phase_blocks_on_approval_blockers_and_dependencies(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            decision = self.decide(
                item=Item(
                    approval_required=True,
                    blocked_by=("TASK-0001",),
                    depends_on=("TASK-0002",),
                    status="blocked",
                ),
                phase="building",
                root=Path(tmp),
            )

            self.assertFalse(decision.allowed)
            self.assertIn("approval_required", decision.blocker_codes)
            self.assertIn("blocked_ticket", decision.blocker_codes)
            self.assertIn("dependency_unmet", decision.blocker_codes)

    def test_resolved_dependencies_do_not_block_build_phase(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            decision = self.decide(
                item=Item(depends_on=("TASK-0002",)),
                phase="building",
                root=Path(tmp),
                resolved_dependencies=("TASK-0002",),
            )

            self.assertTrue(decision.allowed)
            self.assertEqual(decision.blocker_codes, ())


if __name__ == "__main__":
    unittest.main()
