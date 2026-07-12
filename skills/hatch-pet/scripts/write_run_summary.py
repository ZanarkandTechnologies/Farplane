#!/usr/bin/env python3
"""Write the final hatch-pet QA summary from durable run artifacts."""

from __future__ import annotations

import argparse
import json
from pathlib import Path


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--run-dir", required=True)
    parser.add_argument("--package", required=True)
    args = parser.parse_args()

    run_dir = Path(args.run_dir).expanduser().resolve()
    request_path = run_dir / "pet_request.json"
    if not request_path.is_file():
        raise SystemExit(f"pet request not found: {request_path}")

    request = json.loads(request_path.read_text(encoding="utf-8"))
    summary = {
        "ok": True,
        "run_dir": str(run_dir),
        "spritesheet": str(run_dir / "final/spritesheet.webp"),
        "validation": str(run_dir / "final/validation.json"),
        "contact_sheet": str(run_dir / "qa/contact-sheet.png"),
        "review": str(run_dir / "qa/review.json"),
        "package": str(Path(args.package).expanduser().resolve()),
    }
    if request.get("person_discovery_path"):
        summary["person_discovery_path"] = request["person_discovery_path"]
    if request.get("profile_sources"):
        summary["profile_sources"] = request["profile_sources"]

    output = run_dir / "qa/run-summary.json"
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(json.dumps(summary, indent=2) + "\n", encoding="utf-8")
    print(output)


if __name__ == "__main__":
    main()
