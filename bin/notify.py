#!/usr/bin/env python3
import json
import shutil
import subprocess
import sys
from pathlib import Path


MACOS_SOUND_PATH = Path("/System/Library/Sounds/Glass.aiff")
COMMAND_TIMEOUT_SECONDS = 5


def run_quiet(command: list[str]) -> int:
    try:
        completed = subprocess.run(
            command,
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
            check=False,
            timeout=COMMAND_TIMEOUT_SECONDS,
        )
    except subprocess.TimeoutExpired:
        return 1
    return completed.returncode


def play_macos_sound() -> int:
    afplay = shutil.which("afplay")
    if afplay and MACOS_SOUND_PATH.exists():
        return run_quiet([afplay, str(MACOS_SOUND_PATH)])

    osascript = shutil.which("osascript")
    if osascript:
        return run_quiet([osascript, "-e", "beep"])

    return 1


def speak_macos(message: str) -> int:
    say = shutil.which("say")
    if not say:
        return 1

    return run_quiet([say, message])


def speak_espeak_ng(message: str) -> int:
    espeak = shutil.which("espeak-ng")
    if not espeak:
        return 1

    return run_quiet([espeak, "-s", "165", message])


def speak_windows_tts(message: str) -> int:
    powershell = shutil.which("powershell.exe")
    if not powershell:
        return 1

    command = (
        "Add-Type -AssemblyName System.Speech; "
        "$speaker = New-Object System.Speech.Synthesis.SpeechSynthesizer; "
        f"$speaker.Speak('{message}');"
    )

    return run_quiet([powershell, "-NoProfile", "-NonInteractive", "-Command", command])


def announce_message(message: str) -> int:
    play_macos_sound()

    if speak_macos(message) == 0:
        return 0

    if speak_espeak_ng(message) == 0:
        return 0

    if speak_windows_tts(message) == 0:
        return 0

    # Stop-hook callers reserve stdout for machine-readable JSON only.
    sys.stderr.write("\a")
    sys.stderr.flush()
    return 0


def notification_message(notification: dict[str, object]) -> str | None:
    if notification.get("type") != "agent-turn-complete":
        return None

    return "Task completed successfully"


def main() -> int:
    if len(sys.argv) != 2:
        return 1

    try:
        notification = json.loads(sys.argv[1])
    except json.JSONDecodeError:
        return 1

    message = notification_message(notification)
    if message is None:
        return 0

    return announce_message(message)


if __name__ == "__main__":
    raise SystemExit(main())
