#!/usr/bin/env python3
"""Evidence switch: how much proof a thread gathers before it finishes.

awake  = minimal proof: the operator is at the Mac and tests by hand.
asleep = maximum proof: nobody is watching, so the thread proves everything itself.
auto   = asleep while the lid is closed, or 01:00-09:00 Amsterdam with no operator message for 30 min; else awake.

  evidence                 show the mode and why
  evidence awake|asleep    set it by hand; it holds until `evidence auto`
  evidence auto            follow the lid and the clock again
  evidence --mode          print only awake or asleep (for scripts such as a repo's done-check)
  evidence --hook          UserPromptSubmit: note the operator's message, print the mode line for this turn
"""
from __future__ import annotations

import datetime as dt
import json
import os
import subprocess
import sys
from pathlib import Path
from zoneinfo import ZoneInfo

STATE = Path(os.environ.get("FARPLANE_EVIDENCE_DIR", Path.home() / ".farplane" / "evidence"))
ZONE = ZoneInfo("Europe/Amsterdam")
NIGHT = (1, 9)  # local hours [start, end)
QUIET_MIN = 30

LINES = {
    "awake": (
        "Evidence: awake ({why}). Kenji tests by hand: prove with the smallest check. Run the changed area's quick "
        "tests; add one screenshot only when something visible changed; no recordings, no walkthroughs, no re-runs "
        "of judges or benchmarks unless the task is the measurement."
    ),
    "asleep": (
        "Evidence: asleep ({why}). Nobody is watching: prove everything yourself before you finish. Run every check "
        "of each changed area, its builds and the full walk; step screenshots for visible changes and one raw "
        "recording (under 20 s, never edited) for a new feature; for research, rerun the judge or benchmark and "
        "give before/after numbers."
    ),
}


def lid_closed() -> bool:
    if os.environ.get("FARPLANE_EVIDENCE_LID") in ("closed", "open"):
        return os.environ["FARPLANE_EVIDENCE_LID"] == "closed"
    try:
        out = subprocess.run(["ioreg", "-r", "-k", "AppleClamshellState", "-d", "4"],
                             capture_output=True, text=True, timeout=2).stdout
    except (OSError, subprocess.SubprocessError):
        return False
    return '"AppleClamshellState" = Yes' in out


def now() -> dt.datetime:
    fake = os.environ.get("FARPLANE_EVIDENCE_NOW")
    return dt.datetime.fromisoformat(fake) if fake else dt.datetime.now(ZONE)


def read(name: str) -> str:
    try:
        return (STATE / name).read_text().strip()
    except OSError:
        return ""


def resolve() -> tuple[str, str]:
    """(mode, why) for this moment."""
    manual = read("mode")
    if manual in LINES:
        return manual, "set by hand; `evidence auto` to follow the lid and clock"
    if lid_closed():
        return "asleep", "auto: the lid is closed"
    t = now().astimezone(ZONE)
    if NIGHT[0] <= t.hour < NIGHT[1]:
        last = read("last-prompt")
        quiet = (t.timestamp() - float(last)) / 60 if last else 1e9
        if quiet >= QUIET_MIN:
            return "asleep", f"auto: night and no message for {min(int(quiet), 999)} min"
        return "awake", "auto: night, but Kenji wrote recently"
    return "awake", "auto: daytime with the lid open"


def main(argv: list[str]) -> int:
    arg = argv[1] if len(argv) > 1 else ""
    STATE.mkdir(parents=True, exist_ok=True)
    if arg == "--hook":
        try:
            payload = json.loads(sys.stdin.read() or "{}")
        except ValueError:
            payload = {}
        if str(payload.get("prompt", "")).strip():
            (STATE / "last-prompt").write_text(str(now().timestamp()))
        mode, why = resolve()
        print(LINES[mode].format(why=why))
        return 0
    if arg == "--mode":
        print(resolve()[0])
        return 0
    if arg in ("awake", "asleep"):
        (STATE / "mode").write_text(arg + "\n")
    elif arg == "auto":
        (STATE / "mode").unlink(missing_ok=True)
    elif arg not in ("", "status"):
        print(__doc__.strip(), file=sys.stderr)
        return 2
    mode, why = resolve()
    print(f"{mode} ({why})")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
