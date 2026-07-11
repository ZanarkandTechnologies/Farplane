from __future__ import annotations

import importlib.util
import tempfile
import unittest
from pathlib import Path

import yaml


MODULE_PATH = Path(__file__).resolve().parents[1] / "core" / "farplane_reward_migration.py"
SPEC = importlib.util.spec_from_file_location("migrate_reward_rows", MODULE_PATH)
assert SPEC and SPEC.loader
MIGRATE = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(MIGRATE)


def reward_rows(markdown: str) -> list[dict[str, object]]:
    section = MIGRATE.REWARD_SECTION.search(markdown)
    assert section
    fence = MIGRATE.YAML_FENCE.search(section.group(0))
    assert fence
    payload = yaml.safe_load(fence.group(1))
    return payload["kpi_rewards"]


class RewardMigrationTests(unittest.TestCase):
    def test_score_only_rows_receive_ids_but_remain_unresolved(self) -> None:
        markdown = """# Ticket

## Reward

```yaml
kpi_rewards:
  - kpi_id: accepted_evidence_cycles
    expected_reward: one accepted result
    check_in_at: 2026-07-19T00:00:00Z
    actual_result: looked positive
    reward_score: 1
    reward_score_reason: legacy judgment
guard: evidence required
```

## Done / Proof
- proof
"""

        migrated, stats = MIGRATE.migrate_markdown(markdown)
        row = reward_rows(migrated)[0]

        self.assertEqual(row["reward_id"], "accepted-evidence-cycles-2026-07-19-00-00-00-00-00")
        self.assertIsNone(row["decision"])
        self.assertNotIn("reward_score", row)
        self.assertNotIn("reward_score_reason", row)
        self.assertEqual(stats["unresolved"], 1)
        self.assertEqual(stats["removed_scores"], 1)

    def test_generated_ids_are_stable_across_row_reordering(self) -> None:
        rows = [
            {
                "kpi_id": "retention",
                "expected_reward": "seven day retention",
                "check_in_at": "2026-07-19T00:00:00Z",
            },
            {
                "kpi_id": "retention",
                "expected_reward": "thirty day retention",
                "check_in_at": "2026-07-19T00:00:00Z",
            },
        ]
        first = MIGRATE.assign_reward_ids(rows)
        second = MIGRATE.assign_reward_ids(list(reversed(rows)))
        by_expectation_first = {
            rows[index]["expected_reward"]: reward_id for index, reward_id in first.items()
        }
        reversed_rows = list(reversed(rows))
        by_expectation_second = {
            reversed_rows[index]["expected_reward"]: reward_id
            for index, reward_id in second.items()
        }
        self.assertEqual(by_expectation_first, by_expectation_second)

    def test_project_migration_is_dry_run_until_write_and_idempotent_after(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            ticket = root / "tickets" / "TASK-0001" / "ticket.md"
            ticket.parent.mkdir(parents=True)
            ticket.write_text(
                """## Reward

```yaml
kpi_rewards:
  - kpi_id: quality
    expected_reward: useful result
```
""",
                encoding="utf-8",
            )
            original = ticket.read_text(encoding="utf-8")

            dry_run = MIGRATE.migrate_project(root, write=False)
            self.assertEqual(dry_run["changed_count"], 1)
            self.assertEqual(ticket.read_text(encoding="utf-8"), original)

            written = MIGRATE.migrate_project(root, write=True)
            rerun = MIGRATE.migrate_project(root, write=False)

        self.assertEqual(written["changed_count"], 1)
        self.assertEqual(rerun["changed_count"], 0)


if __name__ == "__main__":
    unittest.main()
