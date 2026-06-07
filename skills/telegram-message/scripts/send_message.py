#!/usr/bin/env python3
"""Send a Telegram message using environment-configured credentials."""

from __future__ import annotations

import argparse
import os
import subprocess
import sys
import urllib.parse
import urllib.request
from pathlib import Path


def read_message(args: argparse.Namespace) -> str:
    if args.text and args.file:
        raise SystemExit("Use only one of --text or --file")
    if args.text:
        return args.text
    if args.file:
        return Path(args.file).read_text(encoding="utf-8")
    if not sys.stdin.isatty():
        return sys.stdin.read()
    raise SystemExit("Provide --text, --file, or stdin")


def send(token: str, chat_id: str, text: str, parse_mode: str, disable_preview: bool) -> None:
    url = f"https://api.telegram.org/bot{token}/sendMessage"
    payload = {
        "chat_id": chat_id,
        "text": text,
        "disable_web_page_preview": "true" if disable_preview else "false",
    }
    if parse_mode != "none":
        payload["parse_mode"] = parse_mode
    data = urllib.parse.urlencode(payload).encode("utf-8")
    request = urllib.request.Request(url, data=data, method="POST")
    with urllib.request.urlopen(request, timeout=20) as response:
        body = response.read().decode("utf-8", errors="replace")
        if response.status >= 300:
            raise RuntimeError(f"Telegram HTTP {response.status}: {body}")


def keychain_token() -> str | None:
    try:
        result = subprocess.run(
            [
                "security",
                "find-generic-password",
                "-a",
                os.environ.get("USER", ""),
                "-s",
                "codex-telegram-bot-token",
                "-w",
            ],
            check=False,
            capture_output=True,
            text=True,
        )
    except FileNotFoundError:
        return None
    if result.returncode != 0:
        return None
    token = result.stdout.strip()
    return token or None


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--text")
    parser.add_argument("--file")
    parser.add_argument("--parse-mode", default="none", choices=["none", "Markdown", "MarkdownV2", "HTML"])
    parser.add_argument("--disable-preview", action="store_true", default=True)
    args = parser.parse_args()

    token = os.environ.get("TELEGRAM_BOT_TOKEN") or keychain_token()
    chat_id = os.environ.get("TELEGRAM_CHAT_ID")
    if not token or not chat_id:
        print(
            "Telegram not configured: TELEGRAM_CHAT_ID is required and TELEGRAM_BOT_TOKEN must be in env or macOS Keychain item codex-telegram-bot-token.",
            file=sys.stderr,
        )
        return 2

    message = read_message(args)
    if not message.strip():
        print("Refusing to send an empty Telegram message.", file=sys.stderr)
        return 2

    send(token, chat_id, message, args.parse_mode, args.disable_preview)
    print("Telegram message sent")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
