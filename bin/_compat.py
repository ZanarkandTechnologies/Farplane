from __future__ import annotations

import runpy
import sys
from pathlib import Path


def run_script(relative_path: str) -> None:
    script = Path(__file__).resolve().parent / relative_path
    script_dir = str(script.parent)
    if script_dir not in sys.path:
        sys.path.insert(0, script_dir)
    runpy.run_path(str(script), run_name="__main__")
