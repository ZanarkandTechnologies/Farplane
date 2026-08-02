#!/usr/bin/env python3
"""Tests for the Instagram account config readiness contract."""

from __future__ import annotations

import contextlib
import io
import json
import os
import unittest
from unittest import mock

import check_config
import runtime_env


class CheckConfigTests(unittest.TestCase):
    def run_check(self, values: dict[str, str]) -> tuple[int, dict[str, object]]:
        output = io.StringIO()
        with (
            mock.patch.dict(os.environ, values, clear=True),
            mock.patch.object(check_config, "load_runtime_values", return_value=values),
            contextlib.redirect_stdout(output),
        ):
            status = check_config.main()
        return status, json.loads(output.getvalue())

    def test_token_only_reports_partial_readiness(self) -> None:
        token = "secret-token-that-must-not-leak"
        status, payload = self.run_check({"FARPLANE_INSTAGRAM_LOGIN_ACCESS_TOKEN": token})

        self.assertEqual(status, 1)
        self.assertFalse(payload["ready"])
        self.assertTrue(payload["read_ready"])
        self.assertFalse(payload["publish_ready"])
        self.assertTrue(payload["redacted"])
        self.assertEqual(payload["missing"]["publish_any_of"], check_config.USER_ID_KEYS)
        self.assertNotIn(token, json.dumps(payload))

    def test_token_and_either_user_id_are_fully_ready(self) -> None:
        status, payload = self.run_check(
            {
                "FARPLANE_INSTAGRAM_LOGIN_ACCESS_TOKEN": "secret-token",
                "FARPLANE_INSTAGRAM_LOGIN_USER_ID": "123456",
            }
        )

        self.assertEqual(status, 0)
        self.assertTrue(payload["ready"])
        self.assertTrue(payload["read_ready"])
        self.assertTrue(payload["publish_ready"])
        self.assertEqual(payload["skill"], "instagram-account")
        self.assertEqual(
            set(payload),
            {"skill", "ready", "read_ready", "publish_ready", "redacted"},
        )

    def test_runtime_loader_reads_only_injected_account_values(self) -> None:
        with mock.patch.dict(
            os.environ,
            {
                "FARPLANE_INSTAGRAM_LOGIN_ACCESS_TOKEN": "runtime-token",
                "UNRELATED": "ignored",
            },
            clear=True,
        ):
            values = runtime_env.load_runtime_values()
        self.assertEqual(values, {"FARPLANE_INSTAGRAM_LOGIN_ACCESS_TOKEN": "runtime-token"})


if __name__ == "__main__":
    unittest.main()
