#!/usr/bin/env python3
"""Compatibility entrypoint for the canonical `farplane validate` command."""

from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "bin"))

from farplane import main


if __name__ == "__main__":
    raise SystemExit(main(["farplane", "validate", *sys.argv[1:]]))
