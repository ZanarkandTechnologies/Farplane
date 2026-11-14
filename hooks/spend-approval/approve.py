#!/usr/bin/env python3
"""Kenji's phone approval for Modal spend (spend_approval.sh).

  approve.py request "<what and why>" --usd 5 --minutes 60   sends a 6-digit code to Kenji's Telegram, prints no code
                                                             ($1 or less opens at once, up to $10 a day; Kenji gets one line)
  approve.py grant <code>                                    opens the window when the code matches
  approve.py status                                          shows the open window or pending request

The code is stored only as a salted hash; three wrong codes or 30 minutes cancel the request.
Every request and grant is appended to ~/.farplane/approvals/log.md.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import os
import re
import secrets
import subprocess
import sys
import time
from pathlib import Path

DIR = Path(os.environ.get("FARPLANE_APPROVALS", Path.home() / ".farplane" / "approvals"))
PENDING, GRANT, LOG = DIR / "pending.json", DIR / "grant", DIR / "log.md"
SENDER = Path(__file__).resolve().parents[2] / "skills" / "notify" / "scripts" / "send_message.py"
CODE_TTL, MAX_TRIES = 30 * 60, 3
# Kenji, 14 Nov 2026: "lets make the rule $1 or less", and tests stay as lean as possible. 15 of the gate's first 27
# requests were $1 or less and most codes were never answered, so those open at once; a day's
# small ones stop at $10.
AUTO_USD, AUTO_DAY = 1.0, 10.0


def stamp() -> str:
    return time.strftime("%Y-%m-%d %H:%M", time.localtime())


def log(line: str) -> None:
    DIR.mkdir(parents=True, exist_ok=True)
    with LOG.open("a", encoding="utf-8") as f:
        f.write(f"- {stamp()} {line}\n")


def digest(code: str, salt: str) -> str:
    return hashlib.sha256((salt + code.strip()).encode()).hexdigest()


def send(text: str) -> None:
    if os.environ.get("FARPLANE_APPROVAL_SEND"):  # tests: a command that receives the text on stdin
        subprocess.run(os.environ["FARPLANE_APPROVAL_SEND"], shell=True, input=text, text=True, check=True)
        return
    cmd = ["doppler", "run", "--project", "farplane", "--config", "dev_personal", "--",
           sys.executable, str(SENDER), "--raw-telegram"]  # raw: no reply-routing record, so the code is stored nowhere
    subprocess.run(cmd, input=text, text=True, check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)


def auto_today() -> float:
    """Dollars opened without a code today, read from the log."""
    if not LOG.exists():
        return 0.0
    day = time.strftime("%Y-%m-%d", time.localtime())
    found = re.findall(rf"^- {day} \S+ opened without a code.*\(up to \$([0-9.]+)\)$", LOG.read_text(encoding="utf-8"), re.M)
    return sum(float(x) for x in found)


def open_small(what: str, usd: float, minutes: int) -> int:
    """A request of $1 or less opens the window at once and tells Kenji in one line."""
    DIR.mkdir(parents=True, exist_ok=True)
    until = int(time.time()) + min(minutes, 60) * 60
    if GRANT.exists():  # never shorten a window Kenji opened with a code
        first = GRANT.read_text(encoding="utf-8").split("\n", 1)[0]
        until = max(until, int(first)) if first.isdigit() else until
    spent = auto_today() + usd
    GRANT.write_text(f"{until}\n{what}\n{usd}\n", encoding="utf-8")
    hour = time.strftime("%H:%M", time.localtime(until))
    log(f"opened without a code until {hour}: {what} (up to ${usd:g})")
    try:
        send(f"Modal spend, no code needed (${AUTO_USD:g} or less)\n{what}\nUp to ${usd:g}; ${spent:g} of ${AUTO_DAY:g} today.")
    except (OSError, subprocess.CalledProcessError):
        log("could not tell Kenji's phone about the line above")
    print(f"Approved without a code until {hour}: {what} (up to ${usd:g}; ${spent:g} of ${AUTO_DAY:g} small spends today). "
          "Log it with `farplane spend add`.")
    return 0


def request(what: str, usd: float, minutes: int) -> int:
    if 0 < usd <= AUTO_USD and auto_today() + usd <= AUTO_DAY:
        return open_small(what, usd, minutes)
    code = f"{secrets.randbelow(10**6):06d}"
    salt = secrets.token_hex(8)
    DIR.mkdir(parents=True, exist_ok=True)
    PENDING.write_text(json.dumps({"hash": digest(code, salt), "salt": salt, "what": what, "usd": usd,
                                   "minutes": minutes, "created": time.time(), "tries": 0}), encoding="utf-8")
    send(f"Modal spend approval\n{what}\nUp to ${usd:g} for {minutes} min.\nCode: {code}\n"
         "Give the code to the thread only if you agree.")
    log(f"requested: {what} (up to ${usd:g}, {minutes} min)")
    print(f"Sent to Kenji's phone: {what} (up to ${usd:g}, {minutes} min). Ask Kenji for the code. "
          f"If a smaller run would answer the same question (one room, one GPU, a cached image), ask for that instead: "
          f"${AUTO_USD:g} or less opens at once.")
    return 0


def grant(code: str) -> int:
    if not PENDING.exists():
        print("No pending request. Run: approve.py request ...")
        return 1
    p = json.loads(PENDING.read_text(encoding="utf-8"))
    if time.time() - p["created"] > CODE_TTL:
        PENDING.unlink()
        log(f"expired: {p['what']}")
        print("The code expired. Make a new request.")
        return 1
    if digest(code, p["salt"]) != p["hash"]:
        p["tries"] += 1
        if p["tries"] >= MAX_TRIES:
            PENDING.unlink()
            log(f"cancelled after {MAX_TRIES} wrong codes: {p['what']}")
            print("Wrong code three times: request cancelled.")
        else:
            PENDING.write_text(json.dumps(p), encoding="utf-8")
            print(f"Wrong code ({MAX_TRIES - p['tries']} tries left).")
        return 1
    until = int(time.time()) + p["minutes"] * 60
    GRANT.write_text(f"{until}\n{p['what']}\n{p['usd']}\n", encoding="utf-8")
    PENDING.unlink()
    log(f"granted until {time.strftime('%H:%M', time.localtime(until))}: {p['what']} (up to ${p['usd']:g})")
    print(f"Approved until {time.strftime('%H:%M', time.localtime(until))}: {p['what']} (up to ${p['usd']:g}).")
    return 0


def status() -> int:
    if GRANT.exists():
        until, what, usd = (GRANT.read_text(encoding="utf-8").splitlines() + ["", "", ""])[:3]
        if until.isdigit() and int(until) > time.time():
            print(f"Open until {time.strftime('%H:%M', time.localtime(int(until)))}: {what} (up to ${usd})")
            return 0
    if PENDING.exists():
        print(f"Waiting for Kenji's code: {json.loads(PENDING.read_text(encoding='utf-8'))['what']}")
        return 0
    print("Closed: Modal run/deploy/serve/shell needs a new approval.")
    return 0


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = ap.add_subparsers(dest="cmd", required=True)
    r = sub.add_parser("request")
    r.add_argument("what")
    r.add_argument("--usd", type=float, required=True)
    r.add_argument("--minutes", type=int, default=60)
    g = sub.add_parser("grant")
    g.add_argument("code")
    sub.add_parser("status")
    a = ap.parse_args()
    if a.cmd == "request":
        return request(a.what, a.usd, max(5, min(a.minutes, 8 * 60)))
    if a.cmd == "grant":
        return grant(a.code)
    return status()


if __name__ == "__main__":
    sys.exit(main())
