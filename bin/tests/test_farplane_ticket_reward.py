from __future__ import annotations

import unittest

from bin.core.farplane_ticket_reward import validate_reward_markdown


def ticket_with_reward(check_in_at: str, *, decision: str = "") -> str:
    return f"""# Ticket

## Reward

```yaml
kpi_rewards:
  - reward_id: fixture-reward
    kpi_id: fixture_metric
    expected_reward: improve the fixture metric
    check_in_at: {check_in_at}
    actual_result:
    decision: {decision}
    evaluated_at:
    evaluation_key:
    supersedes_evaluation_key:
    evidence_refs: []
guard: preserve delayed check-in safety
```
"""


class TicketRewardValidationTests(unittest.TestCase):
    def test_accepts_timezone_bearing_schedule(self) -> None:
        for value in ('"2026-07-20T09:00:00+08:00"', "2026-07-20T09:00:00+08:00"):
            with self.subTest(value=value):
                self.assertEqual(validate_reward_markdown(ticket_with_reward(value)), [])

    def test_accepts_explicit_unscheduled_state(self) -> None:
        self.assertEqual(validate_reward_markdown(ticket_with_reward("unscheduled")), [])

    def test_reproduces_pending_blank_timestamp_as_malformed(self) -> None:
        errors = validate_reward_markdown(ticket_with_reward("null"))
        self.assertIn("literal 'unscheduled'", "\n".join(errors))

    def test_reproduces_terminal_null_timestamp_as_malformed(self) -> None:
        errors = validate_reward_markdown(ticket_with_reward("null", decision="kill"))
        self.assertIn("fixture-reward", "\n".join(errors))

    def test_rejects_naive_or_non_datetime_schedule(self) -> None:
        for value in ('"2026-07-20T09:00:00"', '"after review"'):
            with self.subTest(value=value):
                self.assertTrue(validate_reward_markdown(ticket_with_reward(value)))

    def test_ticket_without_reward_is_out_of_scope(self) -> None:
        self.assertEqual(validate_reward_markdown("# Manual ticket\n"), [])


if __name__ == "__main__":
    unittest.main()
