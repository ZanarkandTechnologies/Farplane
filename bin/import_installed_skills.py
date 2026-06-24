#!/usr/bin/env python3
"""Compatibility wrapper for skills/skill-maintenance/scripts/import_installed_skills.py."""

from __future__ import annotations

import importlib.util
import sys
from pathlib import Path


SCRIPT = (
    Path(__file__).resolve().parents[1]
    / "skills"
    / "skill-maintenance"
    / "scripts"
    / "import_installed_skills.py"
)


def _load_main():
    if str(SCRIPT.parent) not in sys.path:
        sys.path.insert(0, str(SCRIPT.parent))
    spec = importlib.util.spec_from_file_location("farplane_import_installed_skills", SCRIPT)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"could not load import_installed_skills script from {SCRIPT}")
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module.main


if __name__ == "__main__":
    raise SystemExit(_load_main()())
