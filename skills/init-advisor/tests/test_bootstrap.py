import subprocess
import shutil
import tempfile
import unittest
from pathlib import Path

import yaml


SCRIPT = Path(__file__).parents[1] / "scripts" / "bootstrap.sh"


def read_frontmatter(path: Path) -> dict:
    text = path.read_text(encoding="utf-8")
    _, frontmatter, _ = text.split("---", 2)
    return yaml.safe_load(frontmatter)


class BootstrapTest(unittest.TestCase):
    def run_bootstrap(self, root: Path) -> subprocess.CompletedProcess[str]:
        return subprocess.run(
            ["bash", str(SCRIPT), str(root)],
            check=True,
            capture_output=True,
            text=True,
        )

    def test_fresh_bootstrap_creates_exactly_three_dependent_foundation_tickets(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)

            self.run_bootstrap(root)

            ticket_paths = sorted((root / "tickets").glob("TASK-*/ticket.md"))
            self.assertEqual(
                [path.parent.name for path in ticket_paths],
                ["TASK-0001", "TASK-0002", "TASK-0003"],
            )
            tickets = [read_frontmatter(path) for path in ticket_paths]
            self.assertEqual(
                [ticket["foundation_step"] for ticket in tickets],
                ["find_customer", "deliver_value", "collect_revenue"],
            )
            self.assertEqual(
                [ticket["foundation_sequence"] for ticket in tickets],
                [1, 2, 3],
            )
            self.assertEqual(
                [ticket["depends_on"] for ticket in tickets],
                [[], ["TASK-0001"], ["TASK-0002"]],
            )
            self.assertTrue(all("approval_required" not in ticket for ticket in tickets))
            self.assertNotIn("Draft initial PRD", "\n".join(path.read_text() for path in ticket_paths))

    def test_packaged_ticket_scaffolds_match_canonical_sources(self) -> None:
        repo_root = SCRIPT.parents[3]
        references = SCRIPT.parents[1] / "references"
        self.assertEqual(
            (references / "TICKETS_README_TEMPLATE.md").read_text(encoding="utf-8"),
            (repo_root / "tickets" / "README.md").read_text(encoding="utf-8"),
        )
        self.assertEqual(
            (references / "TICKET_TEMPLATE.md").read_text(encoding="utf-8"),
            (repo_root / "tickets" / "templates" / "ticket.md").read_text(encoding="utf-8"),
        )

    def test_bootstrap_is_self_contained_when_skill_is_installed_alone(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            isolated_skill = root / "init-advisor"
            shutil.copytree(SCRIPT.parents[1], isolated_skill)
            target = root / "project"
            target.mkdir()

            subprocess.run(
                ["bash", str(isolated_skill / "scripts" / "bootstrap.sh"), str(target)],
                check=True,
                capture_output=True,
                text=True,
            )

            self.assertTrue((target / "tickets" / "README.md").is_file())
            self.assertTrue((target / "tickets" / "templates" / "ticket.md").is_file())
            self.assertEqual(
                [path.parent.name for path in sorted((target / "tickets").glob("TASK-*/ticket.md"))],
                ["TASK-0001", "TASK-0002", "TASK-0003"],
            )

    def test_bootstrap_preserves_partial_ticket_collisions_and_reports_them(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            existing = root / "tickets" / "TASK-0002" / "ticket.md"
            existing.parent.mkdir(parents=True)
            existing.write_text("operator-owned ticket\n", encoding="utf-8")

            result = self.run_bootstrap(root)

            self.assertEqual(existing.read_text(encoding="utf-8"), "operator-owned ticket\n")
            self.assertTrue((root / "tickets" / "TASK-0001" / "ticket.md").is_file())
            self.assertTrue((root / "tickets" / "TASK-0003" / "ticket.md").is_file())
            self.assertIn(f"Skip (exists): {existing}", result.stdout)

    def test_bootstrap_is_idempotent_for_foundation_tickets(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            self.run_bootstrap(root)
            ticket_paths = sorted((root / "tickets").glob("TASK-*/ticket.md"))
            before = {path: path.read_text(encoding="utf-8") for path in ticket_paths}

            result = self.run_bootstrap(root)

            self.assertEqual(
                {path: path.read_text(encoding="utf-8") for path in ticket_paths},
                before,
            )
            for path in ticket_paths:
                self.assertIn(f"Skip (exists): {path}", result.stdout)


if __name__ == "__main__":
    unittest.main()
