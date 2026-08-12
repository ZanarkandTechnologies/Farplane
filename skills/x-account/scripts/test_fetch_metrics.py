#!/usr/bin/env python3
"""Exercise the browser-safe account identity emitted beside X metrics."""

from __future__ import annotations

import importlib.util
import sys
import unittest
from pathlib import Path
from unittest.mock import patch


SCRIPT = Path(__file__).with_name("fetch_metrics.py")
if str(SCRIPT.parent) not in sys.path:
    sys.path.insert(0, str(SCRIPT.parent))
SPEC = importlib.util.spec_from_file_location("x_fetch_metrics", SCRIPT)
assert SPEC and SPEC.loader
MODULE = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(MODULE)


class XFetchMetricsTests(unittest.TestCase):
    def test_records_provider_account_identity_without_credentials(self) -> None:
        def api_get(path: str, _auth: str, _params: dict[str, str]) -> dict:
            if path.startswith("/users/by/username/"):
                return {"data": {"id": "123456", "username": "kenji", "public_metrics": {"followers_count": 265}}}
            if path == "/users/123456/tweets":
                return {"data": []}
            raise AssertionError(path)

        with (
            patch.object(
                MODULE,
                "load_runtime_values",
                return_value={"FARPLANE_X_BEARER_TOKEN": "secret", "FARPLANE_X_USERNAME": "kenji"},
            ),
            patch.object(MODULE, "api_get", side_effect=api_get),
        ):
            payload = MODULE.fetch_metrics("2026-08-12", 10)

        self.assertEqual(
            payload["payload"]["distribution_account"],
            {"platform": "x", "account_id": "123456", "label": "@kenji"},
        )
        self.assertNotIn("secret", str(payload))


if __name__ == "__main__":
    unittest.main()
