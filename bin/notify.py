#!/usr/bin/env python3
import json
import shutil
import subprocess
import sys


def speak_espeak_ng(message: str) -> int:
    espeak = shutil.which("espeak-ng")
    if not espeak:
        return 1

    completed = subprocess.run(
        [espeak, "-s", "165", message],
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
        check=False,
    )
    return completed.returncode


def speak_windows_tts(message: str) -> int:
    powershell = shutil.which("powershell.exe")
    if not powershell:
        return 1

    command = (
        "Add-Type -AssemblyName System.Speech; "
        "$speaker = New-Object System.Speech.Synthesis.SpeechSynthesizer; "
        f"$speaker.Speak('{message}');"
    )

    completed = subprocess.run(
        [powershell, "-NoProfile", "-NonInteractive", "-Command", command],
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
        check=False,
    )
    return completed.returncode


def main() -> int:
    if len(sys.argv) != 2:
        return 1

    try:
        notification = json.loads(sys.argv[1])
    except json.JSONDecodeError:
        return 1

    if notification.get("type") != "agent-turn-complete":
        return 0

    message = "Task completed successfully"

    if speak_espeak_ng(message) == 0:
        return 0

    if speak_windows_tts(message) == 0:
        return 0

    sys.stdout.write("\a")
    sys.stdout.flush()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
