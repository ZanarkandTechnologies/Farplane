from __future__ import annotations

import importlib.util
import unittest
from pathlib import Path
from unittest import mock

SCRIPT = Path(__file__).resolve().parents[1] / "runpod-idle-watch.py"
spec = importlib.util.spec_from_file_location("runpod_idle_watch", SCRIPT)
watch = importlib.util.module_from_spec(spec)
spec.loader.exec_module(watch)

NOW = 1_800_000_000.0


def pod(pid, util=None, uptime=3600, status="RUNNING", gpus=1, volume=0, runtime=True):
    rt = {"uptimeInSeconds": uptime, "gpus": [{"gpuUtilPercent": util}] if gpus else []} if runtime else None
    return {"id": pid, "name": f"pod-{pid}", "desiredStatus": status, "costPerHr": 1.79,
            "gpuCount": gpus, "volumeInGb": volume, "lastStatusChange": "", "runtime": rt}


def account(*pods, balance=50.0, volumes=()):
    return {"clientBalance": balance, "currentSpendPerHr": 0, "pods": list(pods), "networkVolumes": list(volumes)}


class GuardTests(unittest.TestCase):
    def test_busy_pod_keeps_running(self):
        self.assertIsNone(watch.guard_reason(NOW, None, NOW + 3 * 3600, 6))

    def test_idle_twenty_minutes_stops(self):
        self.assertIn("GPU under", watch.guard_reason(NOW, NOW + 3600, NOW + 3600 + 1200, 6))
        self.assertIsNone(watch.guard_reason(NOW, NOW + 3600, NOW + 3600 + 1100, 6))

    def test_never_stops_a_just_booted_pod_for_idle(self):
        self.assertIsNone(watch.guard_reason(NOW, NOW, NOW + 1199, 6))

    def test_hard_limit_stops_even_when_busy(self):
        self.assertIn("6 h limit", watch.guard_reason(NOW, None, NOW + 6 * 3600, 6))
        self.assertIsNone(watch.guard_reason(NOW, None, NOW + 100 * 3600, 0))


class IdleWatchTests(unittest.TestCase):
    def run_check(self, acct, state, now=NOW):
        with mock.patch.object(watch, "stop_pod", return_value="stopped") as stop:
            out, new_state = watch.check(acct, state, now, act=True)
        return out, new_state, stop

    def test_idle_pod_warns_then_stops_on_second_check(self):
        out, state, stop = self.run_check(account(pod("a", util=0)), {})
        self.assertEqual(out["stopped"], [])
        self.assertEqual(len(out["warnings"]), 1)
        out, state, stop = self.run_check(account(pod("a", util=1)), state, NOW + 1200)
        stop.assert_called_once_with("a")
        self.assertEqual(out["stopped"][0]["id"], "a")

    def test_busy_gpu_resets_streak(self):
        _, state, _ = self.run_check(account(pod("a", util=0)), {})
        _, state, _ = self.run_check(account(pod("a", util=90)), state)
        out, _, stop = self.run_check(account(pod("a", util=0)), state)
        stop.assert_not_called()
        self.assertTrue(out["warnings"])

    def test_kept_and_fresh_pods_are_not_stopped(self):
        state = {"keep": {"a": NOW + 3600}, "idle": {"a": 5, "b": 5}}
        out, _, stop = self.run_check(account(pod("a", util=0), pod("b", util=0, uptime=300)), state)
        stop.assert_not_called()
        self.assertEqual(out["stopped"], [])

    def test_stuck_initializing_pod_stops_after_threshold(self):
        _, state, stop = self.run_check(account(pod("a", runtime=False)), {})
        stop.assert_not_called()
        _, _, stop = self.run_check(account(pod("a", runtime=False)), state, NOW + watch.INIT_STUCK_S)
        stop.assert_called_once_with("a")

    def test_cpu_pod_is_flagged_not_stopped(self):
        out, _, stop = self.run_check(account(pod("a", gpus=0, uptime=7 * 3600)), {"idle": {"a": 9}})
        stop.assert_not_called()
        self.assertIn("CPU pod", out["warnings"][0])

    def test_storage_flags_send_once_per_day(self):
        acct = account(pod("s", status="EXITED", volume=100), balance=2,
                       volumes=[{"id": "v", "name": "vol", "size": 500, "dataCenterId": "EU"}])
        out, state, _ = self.run_check(acct, {})
        self.assertEqual(len(out["daily"]), 3)
        self.assertTrue(out["notify"])
        out, _, _ = self.run_check(acct, state, NOW + 1200)
        self.assertEqual(out["daily"], [])
        self.assertFalse(out["notify"])


if __name__ == "__main__":
    unittest.main()
