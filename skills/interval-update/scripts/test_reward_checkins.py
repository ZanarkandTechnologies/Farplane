from __future__ import annotations

import tempfile
import unittest
import importlib.util
from datetime import datetime, timezone
from pathlib import Path

SCRIPT_PATH = Path(__file__).with_name("reward_checkins.py")
SPEC = importlib.util.spec_from_file_location("reward_checkins", SCRIPT_PATH)
assert SPEC and SPEC.loader
reward_checkins = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(reward_checkins)
reward_items = reward_checkins.reward_items


TICKET_TEMPLATE = """---
ticket_id: {ticket_id}
title: {ticket_id}
phase: complete
status: done
owner: test
claimed_by:
priority: medium
depends_on: []
blocked_by: []
ready: false
approval_required: false
created_at: 2026-07-01T00:00:00+08:00
updated_at: 2026-07-08T00:00:00+08:00
next_action: complete
last_verification: test
---

# {ticket_id}

## Reward

```yaml
kpi_rewards:
  - kpi_id: accepted_harness_improvements
    expected_reward: "{expected_reward}"
    check_in_at: "{check_in_at}"
    actual_result: {actual_result}
    reward_score: {reward_score}
    reward_score_reason: {reward_score_reason}
guard: "test"
```
"""


class RewardCheckinsTest(unittest.TestCase):
    def write_ticket(
        self,
        root: Path,
        ticket_id: str,
        check_in_at: str,
        actual_result: str = "",
        reward_score: str = "",
        reward_score_reason: str = "",
    ) -> None:
        ticket_root = root / ticket_id
        ticket_root.mkdir(parents=True)
        actual_yaml = f'"{actual_result}"' if actual_result else ""
        score_reason_yaml = f'"{reward_score_reason}"' if reward_score_reason else ""
        (ticket_root / "ticket.md").write_text(
            TICKET_TEMPLATE.format(
                ticket_id=ticket_id,
                expected_reward="expected result",
                check_in_at=check_in_at,
                actual_result=actual_yaml,
                reward_score=reward_score,
                reward_score_reason=score_reason_yaml,
            ),
            encoding="utf-8",
        )

    def test_due_not_due_and_bad_predictions(self) -> None:
        now = datetime(2026, 7, 8, 0, 0, tzinfo=timezone.utc)
        with tempfile.TemporaryDirectory() as tmp:
            tickets = Path(tmp) / "tickets"
            tickets.mkdir()
            self.write_ticket(tickets, "TASK-0001", "2026-07-07T00:00:00+00:00")
            self.write_ticket(tickets, "TASK-0002", "2026-07-09T00:00:00+00:00")
            self.write_ticket(
                tickets,
                "TASK-0003",
                "2026-07-07T00:00:00+00:00",
                actual_result="missed the expected result",
                reward_score="0.2",
                reward_score_reason="weak match",
            )
            self.write_ticket(
                tickets,
                "TASK-0004",
                "2026-07-07T00:00:00+00:00",
                actual_result="impossible score",
                reward_score="2",
                reward_score_reason="bad score",
            )

            packet = reward_items(tickets, now=now, lookback_days=14, include_archive=True)

        self.assertEqual([item["ticket_id"] for item in packet["due"]], ["TASK-0001", "TASK-0004"])
        self.assertEqual([item["ticket_id"] for item in packet["not_due"]], ["TASK-0002"])
        self.assertEqual([item["ticket_id"] for item in packet["scored"]], ["TASK-0003"])
        self.assertEqual(packet["scored"][0]["reward_score"], 0.2)
        self.assertEqual(packet["gaps"], [{"ticket": "tickets/TASK-0004/ticket.md", "index": 0, "gap": "reward_score_out_of_range"}])


if __name__ == "__main__":
    unittest.main()
