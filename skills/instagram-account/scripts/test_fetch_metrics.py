#!/usr/bin/env python3
"""Exercise the browser-safe account identity emitted beside Instagram metrics."""

from __future__ import annotations

import importlib.util
import sys
import unittest
from pathlib import Path
from unittest.mock import patch


SCRIPT = Path(__file__).with_name("fetch_metrics.py")
if str(SCRIPT.parent) not in sys.path:
    sys.path.insert(0, str(SCRIPT.parent))
SPEC = importlib.util.spec_from_file_location("instagram_fetch_metrics", SCRIPT)
assert SPEC and SPEC.loader
MODULE = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(MODULE)


class InstagramFetchMetricsTests(unittest.TestCase):
    def test_records_provider_account_identity_without_credentials(self) -> None:
        profile = {"id": "17841400000000000", "username": "kenji", "followers_count": 921}
        with (
            patch.object(MODULE, "load_runtime_values", return_value={"FARPLANE_INSTAGRAM_LOGIN_ACCESS_TOKEN": "secret"}),
            patch.object(MODULE, "instagram_get", side_effect=[profile, {"data": []}]),
        ):
            payload = MODULE.fetch_metrics("2026-08-12", 10, ["views"])

        self.assertEqual(
            payload["payload"]["distribution_account"],
            {"platform": "instagram", "account_id": "17841400000000000", "label": "@kenji"},
        )
        self.assertNotIn("secret", str(payload))

    def test_marks_missing_provider_account_identity_without_dropping_metrics(self) -> None:
        with (
            patch.object(MODULE, "load_runtime_values", return_value={"FARPLANE_INSTAGRAM_LOGIN_ACCESS_TOKEN": "secret"}),
            patch.object(MODULE, "instagram_get", side_effect=[{"followers_count": 921}, {"data": []}]),
        ):
            payload = MODULE.fetch_metrics("2026-08-12", 10, ["views"])

        self.assertNotIn("distribution_account", payload["payload"])
        self.assertIn("instagram_distribution_account_identity_unavailable", payload["gaps"])
        self.assertEqual(payload["observations"][0]["metric_id"], "instagram_followers")


if __name__ == "__main__":
    unittest.main()
