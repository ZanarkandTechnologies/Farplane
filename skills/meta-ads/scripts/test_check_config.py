#!/usr/bin/env python3
"""Tests for the Meta Ads read-only readiness contract."""

from __future__ import annotations

import contextlib
import io
import json
import os
import unittest
from unittest import mock

import check_config


class CheckConfigTests(unittest.TestCase):
    def run_check(self, values: dict[str, str], cli_path: str | None) -> tuple[int, dict[str, object]]:
        output = io.StringIO()
        with (
            mock.patch.dict(os.environ, values, clear=True),
            mock.patch.object(check_config.shutil, "which", return_value=cli_path),
            contextlib.redirect_stdout(output),
        ):
            status = check_config.main()
        return status, json.loads(output.getvalue())

    def test_missing_token_is_blocked_without_echoing_values(self) -> None:
        status, payload = self.run_check({}, "/opt/bin/meta-ads-open-cli")

        self.assertEqual(status, 1)
        self.assertFalse(payload["ready"])
        self.assertFalse(payload["read_ready"])
        self.assertEqual(payload["missing"], {"read_all_of": [check_config.TOKEN_KEY]})

    def test_token_and_cli_enable_read_only_skill(self) -> None:
        token = "must-not-appear-in-output"
        status, payload = self.run_check(
            {check_config.TOKEN_KEY: token}, "/opt/bin/meta-ads-open-cli"
        )

        self.assertEqual(status, 0)
        self.assertEqual(
            payload,
            {
                "skill": "meta-ads",
                "ready": True,
                "read_ready": True,
                "publish_ready": False,
                "redacted": True,
            },
        )
        self.assertNotIn(token, json.dumps(payload))

    def test_missing_cli_is_a_runtime_blocker(self) -> None:
        status, payload = self.run_check({check_config.TOKEN_KEY: "secret"}, None)

        self.assertEqual(status, 1)
        self.assertEqual(payload["missing"], {"runtime_all_of": [check_config.CLI]})


if __name__ == "__main__":
    unittest.main()
