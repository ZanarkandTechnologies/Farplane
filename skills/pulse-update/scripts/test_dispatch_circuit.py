from __future__ import annotations

import sys
import tempfile
import unittest
from datetime import datetime, timedelta, timezone
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path


SCRIPT_DIR = Path(__file__).resolve().parent
if str(SCRIPT_DIR) not in sys.path:
    sys.path.insert(0, str(SCRIPT_DIR))

from dispatch_circuit import load_state, record_failure, record_success, request_probe


class DispatchCircuitTests(unittest.TestCase):
    def test_two_failures_open_and_success_closes(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            self.assertEqual(load_state(root)["status"], "closed")
            self.assertEqual(record_failure(root, "timeout one")["status"], "closed")
            opened = record_failure(root, "timeout two")
            self.assertEqual(opened["status"], "open")
            self.assertEqual(opened["consecutive_failures"], 2)
            closed = record_success(root)
            self.assertEqual(closed["status"], "closed")
            self.assertEqual(closed["consecutive_failures"], 0)

    def test_open_circuit_allows_one_probe_after_cooldown(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            start = datetime(2026, 7, 13, 7, 0, tzinfo=timezone.utc)
            record_failure(root, "timeout one", now=start)
            record_failure(root, "timeout two", now=start)
            early = request_probe(root, now=start + timedelta(minutes=29))
            self.assertFalse(early["probe_allowed"])
            probe = request_probe(root, now=start + timedelta(minutes=30))
            self.assertTrue(probe["probe_allowed"])
            self.assertEqual(probe["status"], "half_open")
            duplicate = request_probe(root, now=start + timedelta(minutes=31))
            self.assertFalse(duplicate["probe_allowed"])

    def test_failed_probe_reopens_and_successful_probe_closes(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            start = datetime(2026, 7, 13, 7, 0, tzinfo=timezone.utc)
            record_failure(root, "timeout one", now=start)
            record_failure(root, "timeout two", now=start)
            request_probe(root, now=start + timedelta(minutes=30))
            reopened = record_failure(root, "probe failed", now=start + timedelta(minutes=31))
            self.assertEqual(reopened["status"], "open")
            self.assertEqual(reopened["consecutive_failures"], 3)
            request_probe(root, now=start + timedelta(minutes=61))
            closed = record_success(root)
            self.assertEqual(closed["status"], "closed")

    def test_concurrent_half_open_requests_allow_exactly_one_probe(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            start = datetime(2026, 7, 13, 7, 0, tzinfo=timezone.utc)
            record_failure(root, "timeout one", now=start)
            record_failure(root, "timeout two", now=start)
            due = start + timedelta(minutes=30)
            with ThreadPoolExecutor(max_workers=4) as pool:
                results = list(pool.map(lambda _: request_probe(root, now=due), range(4)))
            self.assertEqual(sum(bool(row["probe_allowed"]) for row in results), 1)

    def test_composed_nonreturn_flow_opens_circuit_then_recovers(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            start = datetime(2026, 7, 13, 7, 0, tzinfo=timezone.utc)
            # Wake one: launch is allowed, but a bounded 30-second attempt does
            # not return; Pulse records failure and continues refill.
            self.assertTrue(request_probe(root, now=start)["probe_allowed"])
            first = record_failure(root, "create timed out after 30 seconds", now=start)
            self.assertEqual(first["status"], "closed")
            refill_calls = 1
            # Wake two: one more bounded failure opens the shared circuit.
            self.assertTrue(request_probe(root, now=start + timedelta(minutes=1))["probe_allowed"])
            second = record_failure(root, "lookup timed out after 30 seconds", now=start + timedelta(minutes=1))
            self.assertEqual(second["status"], "open")
            refill_calls += 1
            # Subsequent wakes keep planning but cannot launch until cooldown.
            self.assertFalse(request_probe(root, now=start + timedelta(minutes=20))["probe_allowed"])
            refill_calls += 1
            probe = request_probe(root, now=start + timedelta(minutes=31))
            self.assertTrue(probe["probe_allowed"])
            record_success(root)
            self.assertEqual(load_state(root)["status"], "closed")
            self.assertEqual(refill_calls, 3)


if __name__ == "__main__":
    unittest.main()
