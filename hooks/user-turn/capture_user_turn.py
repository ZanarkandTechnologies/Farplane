#!/usr/bin/env python3
"""UserPromptSubmit entrypoint; shared implementation lives in bin/runtime."""
from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).resolve().parents[2] / "bin"))
from _compat import run_script

run_script("runtime/capture_user_turn.py")
