#!/usr/bin/env python3

from __future__ import annotations

import json
import subprocess
import sys
import unittest
from pathlib import Path


SCRIPT = Path(__file__).with_name("calculate_value.py")


def run_calculator(*args: str) -> dict[str, str]:
    result = subprocess.run(
        [sys.executable, str(SCRIPT), *args],
        check=True,
        capture_output=True,
        text=True,
    )
    return json.loads(result.stdout)


class CalculateValueTests(unittest.TestCase):
    def test_people_time_anchor(self) -> None:
        result = run_calculator(
            "people-time",
            "--people", "3",
            "--hours", "10",
            "--rate", "40",
            "--periods", "52",
        )
        self.assertEqual(result["annual_value"], "62400.00")
        self.assertEqual(result["recommended_price"], "9500.00")
        self.assertEqual(result["client_return_multiple"], "6.6")

    def test_consequence_anchor(self) -> None:
        result = run_calculator(
            "consequence",
            "--incidents", "2",
            "--cost", "1000",
            "--periods", "12",
        )
        self.assertEqual(result["annual_value"], "24000.00")
        self.assertEqual(result["recommended_price"], "3500.00")
        self.assertEqual(result["client_return_multiple"], "6.9")

    def test_direct_annual_anchor_with_override(self) -> None:
        result = run_calculator(
            "--share", "0.10",
            "annual",
            "--amount", "100000",
        )
        self.assertEqual(result["recommended_price"], "10000.00")
        self.assertEqual(result["client_return_multiple"], "10.0")

    def test_rejects_non_positive_values(self) -> None:
        result = subprocess.run(
            [sys.executable, str(SCRIPT), "annual", "--amount", "0"],
            capture_output=True,
            text=True,
        )
        self.assertNotEqual(result.returncode, 0)


if __name__ == "__main__":
    unittest.main()
