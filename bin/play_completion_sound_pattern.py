#!/usr/bin/env python3
import os
import random
import subprocess
import sys
import time
from pathlib import Path


MESSAGE = "Task completed successfully"
INITIAL_DELAY_SECONDS = 0.8
FOLLOWUP_COUNT = 6
FOLLOWUP_DELAY_SECONDS = 0.4
MIN_FOLLOWUP_JITTER_SECONDS = 0.4
MAX_FOLLOWUP_JITTER_SECONDS = 0.8
SCRIPT_DIR = Path(__file__).resolve().parent


def start_notification() -> subprocess.Popen[str]:
    env = os.environ.copy()
    pythonpath = env.get("PYTHONPATH", "")
    env["PYTHONPATH"] = str(SCRIPT_DIR) if not pythonpath else f"{SCRIPT_DIR}:{pythonpath}"

    return subprocess.Popen(
        [
            sys.executable,
            "-c",
            (
                "import notify; "
                f"raise SystemExit(notify.announce_message({MESSAGE!r}))"
            ),
        ],
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
        env=env,
        text=True,
    )


def launch_followups(count: int) -> None:
    for index in range(count):
        start_notification()
        if index != count - 1:
            time.sleep(
                random.uniform(
                    MIN_FOLLOWUP_JITTER_SECONDS,
                    MAX_FOLLOWUP_JITTER_SECONDS,
                )
            )


def wait_for(process: subprocess.Popen[str]) -> int:
    return process.wait()


def main() -> int:
    time.sleep(INITIAL_DELAY_SECONDS)

    if wait_for(start_notification()) != 0:
        return 1

    time.sleep(FOLLOWUP_DELAY_SECONDS)

    launch_followups(FOLLOWUP_COUNT)

    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except KeyboardInterrupt:
        sys.exit(130)
