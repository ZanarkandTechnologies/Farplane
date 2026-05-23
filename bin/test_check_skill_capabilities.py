#!/usr/bin/env python3
"""Tests for check_skill_capabilities.py."""

from __future__ import annotations

import json
import sys
import tempfile
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

import check_skill_capabilities as csc


def valid_fixture(**overrides: object) -> dict[str, object]:
    fixture: dict[str, object] = {
        "skill": "notion-context",
        "operation": "tasks_this_week",
        "kind": "mcp_query",
        "expected": "normalized_task_rows_or_connector_unavailable",
        "observed_failure": "notion-query-data-sources not found",
        "expected_recovery": ["fallback", "repair_ticket"],
        "forbidden_actions": [
            "mutate_notion_status",
            "publish",
            "deploy",
            "spend_money",
            "destructive_cleanup",
        ],
        "fallback_methods": [
            "exact_view_query",
            "api_data_source_query",
            "mcp_data_source_query",
            "search_fetch_diagnostics",
            "local_filesystem_board",
        ],
        "priority_hint": "high",
        "user_value_reason": "blocks autonomous ticket planning",
        "evidence_refs": ["tickets/TASK-0154/ticket.md"],
    }
    fixture.update(overrides)
    return fixture


class SkillCapabilityTests(unittest.TestCase):
    def test_valid_fixture_scores_pass(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "fixture.json"
            raw = valid_fixture()
            path.write_text(json.dumps(raw))
            fixture = csc.validate_capability(raw, path)
            result = csc.score_capability(fixture)
            self.assertTrue(result.passed)
            self.assertEqual(result.decision, ("fallback", "repair_ticket"))

    def test_invalid_recovery_fails_validation(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "fixture.json"
            raw = valid_fixture(expected_recovery=["do_anything"])
            with self.assertRaises(csc.CapabilityError):
                csc.validate_capability(raw, path)

    def test_invalid_fallback_method_fails_validation(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "fixture.json"
            raw = valid_fixture(fallback_methods=["ask_the_user_to_click_refresh"])
            with self.assertRaises(csc.CapabilityError):
                csc.validate_capability(raw, path)

    def test_fallback_methods_need_safe_terminal_path(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "fixture.json"
            raw = valid_fixture(fallback_methods=["exact_view_query", "api_data_source_query"])
            fixture = csc.validate_capability(raw, path)
            result = csc.score_capability(fixture)
            self.assertFalse(result.passed)
            self.assertIn("fallback_methods should end", result.errors[0])

    def test_failure_packet_contains_repair_marker(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "fixture.json"
            fixture = csc.validate_capability(valid_fixture(), path)
            packet = csc.failure_packet(fixture, "scheduled_automation")
            ticket = csc.render_repair_ticket("TASK-9999", packet)
            self.assertIn("skill=notion-context; operation=tasks_this_week", ticket)
            self.assertIn("connector_contract_mismatch", ticket)

    def test_repair_ticket_dedupes_existing_ticket(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            tickets = root / "tickets" / "TASK-0001"
            tickets.mkdir(parents=True)
            fixture = csc.validate_capability(valid_fixture(), root / "fixture.json")
            packet = csc.failure_packet(fixture, "chat")
            existing = tickets / "ticket.md"
            existing.write_text(csc.render_repair_ticket("TASK-0001", packet))
            self.assertEqual(csc.write_repair_ticket(root, packet), existing)

    def test_high_value_signal_auto_tickets(self) -> None:
        raw = {
            "name": "high",
            "goal_ref": "planner",
            "repeated_failure_count": 2,
            "blocked_workflows": ["planning"],
            "affected_skills": ["notion-context"],
            "manual_intervention_cost": "high",
            "confidence": "high",
            "expected_action_policy": "auto_ticket",
        }
        with tempfile.TemporaryDirectory() as tmp:
            signal = csc.validate_value_signal(raw, Path(tmp) / "value.json")
            result = csc.score_value_signal(signal)
            self.assertTrue(result.passed)
            self.assertEqual(result.action_policy, "auto_ticket")

    def test_low_confidence_value_signal_asks(self) -> None:
        raw = {
            "name": "low",
            "goal_ref": "personal",
            "repeated_failure_count": 1,
            "blocked_workflows": ["unclear"],
            "affected_skills": [],
            "manual_intervention_cost": "medium",
            "confidence": "low",
            "expected_action_policy": "ask",
        }
        with tempfile.TemporaryDirectory() as tmp:
            signal = csc.validate_value_signal(raw, Path(tmp) / "value.json")
            result = csc.score_value_signal(signal)
            self.assertTrue(result.passed)
            self.assertEqual(result.action_policy, "ask")


if __name__ == "__main__":
    unittest.main()
