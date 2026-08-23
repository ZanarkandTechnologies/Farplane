import json
import tempfile
import unittest
from pathlib import Path

from bin.validators.check_skill_surface_budget import (
    SurfaceLimits,
    collect_budget_results,
)


def write_skill(
    root: Path,
    name: str,
    *,
    subscribed: bool,
    todos: int = 0,
    evals: int = 0,
    numbered: bool = False,
) -> None:
    skill_dir = root / "skills" / name
    skill_dir.mkdir(parents=True)
    template_uses = '  skill-surface-budget: "0.1.0"\n' if subscribed else ""
    todo_lines = "\n".join(
        f"{index}. Todo {index}" if numbered else f"- [ ] {index}. Todo {index}"
        for index in range(1, todos + 1)
    )
    (skill_dir / "SKILL.md").write_text(
        "\n".join(
            [
                "---",
                f"name: {name}",
                "description: Test skill.",
                "tier: 1",
                "source: local",
                "template_uses:",
                '  skill-template: "0.1.0"',
                template_uses.rstrip(),
                "---",
                "",
                f"# {name}",
                "",
                "<!-- BEGIN FARPLANE_IMPORTANT_CHECKLIST -->",
                "## Todo List",
                "",
                todo_lines,
                "<!-- END FARPLANE_IMPORTANT_CHECKLIST -->",
            ]
        ).replace("\n\n---", "\n---"),
        encoding="utf-8",
    )
    if evals:
        eval_path = skill_dir / "evals" / "evals.json"
        eval_path.parent.mkdir(parents=True)
        eval_path.write_text(
            json.dumps(
                {
                    "skill_name": name,
                    "evals": [{"id": str(index)} for index in range(1, evals + 1)],
                }
            ),
            encoding="utf-8",
        )


class SkillSurfaceBudgetTests(unittest.TestCase):
    def test_skips_unsubscribed_over_budget_skill(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            write_skill(root, "plain", subscribed=False, todos=99, evals=99)
            result = collect_budget_results(root)
            self.assertEqual(result.checked, 0)
            self.assertEqual(result.skipped, 1)
            self.assertEqual(result.violations, [])

    def test_subscribed_skill_passes_when_under_budget(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            write_skill(root, "capped", subscribed=True, todos=10, evals=5)
            result = collect_budget_results(root)
            self.assertEqual(result.checked, 1)
            self.assertEqual(result.skipped, 0)
            self.assertEqual(result.violations, [])

    def test_subscribed_numbered_skill_passes_when_under_budget(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            write_skill(root, "numbered", subscribed=True, todos=10, evals=5, numbered=True)
            result = collect_budget_results(root)
            self.assertEqual(result.checked, 1)
            self.assertEqual(result.skipped, 0)
            self.assertEqual(result.violations, [])

    def test_subscribed_skill_reports_all_over_budget_surfaces(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            write_skill(root, "noisy", subscribed=True, todos=11, evals=6)
            result = collect_budget_results(root, limits=SurfaceLimits(10, 5))
            self.assertEqual(result.checked, 1)
            self.assertEqual(
                [violation.surface for violation in result.violations],
                ["skill_todos", "eval_tasks"],
            )


if __name__ == "__main__":
    unittest.main()
