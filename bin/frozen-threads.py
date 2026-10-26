#!/usr/bin/env python3
"""Catch Claude app threads that stopped answering, within minutes.

A thread is frozen when the newest event in its transcript is something the
model must answer (Kenji's message, another session's message, a background
job's notice, a tool result, a stop-hook rewrite request or an API retry) and
no reply has come for --minutes. On 26 Oct 2026 one thread sat like this for
8.8 hours while Kenji's own "hi" went unanswered; the Thread Sweeper runs only
every 2 hours and looks for quiet threads, not stuck ones.

  frozen-threads.py check [--minutes 10] [--notify] [--dry-run]
  frozen-threads.py check --now 2026-10-26T01:20:00Z --transcript <file.jsonl>   replay one transcript
  frozen-threads.py install [--every 300]   launchd agent com.farplane.frozen-threads
  frozen-threads.py uninstall

Reads the app's thread records and transcripts only; never touches a thread.
It alerts Kenji on Telegram once when a thread freezes and once more if it is
still frozen an hour later. State: ~/.farplane/frozen-threads/state.json.
"""

from __future__ import annotations

import argparse
import json
import os
import re
import subprocess
import sys
import time
from datetime import datetime, timezone
from pathlib import Path

HOME = Path.home()
APP = HOME / "Library" / "Application Support" / "Claude"
SESSIONS = APP / "claude-code-sessions"
TRANSCRIPTS = HOME / ".claude" / "projects"
STATE_DIR = HOME / ".farplane" / "frozen-threads"
STATE = STATE_DIR / "state.json"
LABEL = "com.farplane.frozen-threads"
PLIST = HOME / "Library" / "LaunchAgents" / f"{LABEL}.plist"
SENDER = Path(__file__).resolve().parent.parent / "skills" / "notify" / "scripts" / "send_message.py"

LOOKBACK_S = 48 * 3600      # threads idle longer than this are not watched
TAIL_BYTES = 512 * 1024     # enough of a transcript's end to find its last event
REMIND_AFTER_S = 3600       # one reminder if the same event is still unanswered


def ts(s: str) -> float:
    return datetime.fromisoformat(s.replace("Z", "+00:00")).timestamp()


def text_of(content) -> str:
    if isinstance(content, str):
        return content
    if isinstance(content, list):
        return " ".join(b.get("text", "") for b in content if isinstance(b, dict) and b.get("type") == "text")
    return ""


def read_events(path: Path, whole: bool) -> list[dict]:
    with open(path, "rb") as f:
        if not whole:
            f.seek(max(0, os.path.getsize(path) - TAIL_BYTES))
            f.readline()  # drop the partial first line
        raw = f.read().decode("utf-8", "replace").splitlines()
    out = []
    for line in raw:
        try:
            e = json.loads(line)
        except ValueError:
            continue
        if e.get("type") in ("user", "assistant", "system") and not e.get("isSidechain") and e.get("timestamp"):
            out.append(e)
    return out


def tools_still_running(events: list[dict], j: int, now: float) -> bool:
    """True when the model's last request started tools whose results have not all come back by `now`."""
    for k in range(j - 1, -1, -1):
        if events[k]["type"] == "assistant":
            mid = events[k]["message"].get("id")
            break
    else:
        return False
    asked, first = set(), None
    for k in range(j - 1, -1, -1):
        e = events[k]
        if e["type"] == "assistant" and e["message"].get("id") == mid:
            first = k
            asked |= {b["id"] for b in e["message"].get("content") or [] if isinstance(b, dict) and b.get("type") == "tool_use"}
        elif e["type"] == "assistant":
            break
    got = set()
    for e in events[first:]:
        if ts(e["timestamp"]) > now:
            break
        if e["type"] == "user" and isinstance(e["message"].get("content"), list):
            got |= {b.get("tool_use_id") for b in e["message"]["content"] if isinstance(b, dict) and b.get("type") == "tool_result"}
    return bool(asked - got)


def pending(events: list[dict], now: float) -> dict | None:
    """The event still waiting on the model at `now`, or None when the thread is not waiting on it."""
    for j in range(len(events) - 1, -1, -1):
        e = events[j]
        if ts(e["timestamp"]) > now:
            continue
        kind = e["type"]
        if kind == "assistant":
            return None  # the model answered; a tool it called may still be running, which is not a freeze
        if kind == "system":
            sub = e.get("subtype")
            if sub == "api_error":
                return e
            if sub == "stop_hook_summary":
                # a blocking hook sends a rewrite request next; a passing one ends the turn
                return None if not e.get("hookErrors") else e
            continue  # informational, compaction markers and the like
        content = e["message"].get("content")
        blocks = content if isinstance(content, list) else []
        results = [b for b in blocks if isinstance(b, dict) and b.get("type") == "tool_result"]
        if results:
            if any(text_of(b.get("content")).startswith("The user doesn't want to proceed")
                   or str(b.get("content", "")).startswith("The user doesn't want to proceed") for b in results):
                return None  # a refused tool ends the turn
            return None if tools_still_running(events, j, now) else e
        text = text_of(content).lstrip()
        if text.startswith(("[Request interrupted", "<local-command-", "<command-name>")):
            return None  # an interrupt or a local slash command: nothing for the model to answer
        if e.get("turnOrigin") or e.get("isMeta") or text.startswith("Your response above was cut off"):
            return e
        continue  # notes the app writes without starting a turn, such as background-shell cleanup notices
    return None


def describe(e: dict) -> str:
    if e["type"] == "system":
        err = e.get("error") or {}
        return "an API retry (" + (err.get("formatted") or err.get("message") or "error") + ")"
    blocks = e["message"].get("content")
    if isinstance(blocks, list) and any(isinstance(b, dict) and b.get("type") == "tool_result" for b in blocks):
        return "a tool result"
    t = text_of(blocks).strip()
    if t.startswith("Stop hook feedback"):
        return "a stop-hook rewrite request"
    if t.startswith("<task-notification>"):
        return "a background job's done-notice"
    if t.startswith("Another Claude session") or t.startswith("<system-reminder>"):
        return "a message from another session"
    t = re.sub(r"\s+", " ", t)
    return "Kenji's message “" + (t[:60] + "…" if len(t) > 60 else t) + "”"


def records(since: float = 0) -> list[dict]:
    """Thread records of the signed-in account (the app mirrors them into other accounts' folders).

    Records not written since `since` are skipped unread: they are large, and an old record is not a live thread."""
    try:
        active = json.load(open(APP / "config.json")).get("lastKnownAccountUuid")
    except (OSError, ValueError):
        active = None
    roots = [SESSIONS / active] if active and (SESSIONS / active).is_dir() else [p for p in SESSIONS.iterdir() if p.is_dir()]
    best: dict[str, dict] = {}
    for root in roots:
        for f in root.glob("*/local_*.json"):
            try:
                if f.stat().st_mtime < since:
                    continue
                r = json.load(open(f))
            except (OSError, ValueError):
                continue
            sid = r.get("sessionId")
            if sid and (sid not in best or r.get("lastActivityAt", 0) > best[sid].get("lastActivityAt", 0)):
                best[sid] = r
    return list(best.values())


def find_frozen(minutes: float, now: float, only: Path | None = None) -> list[dict]:
    if only:
        e = pending(read_events(only, whole=True), now)
        if e and now - ts(e["timestamp"]) >= minutes * 60:
            return [{"session": only.stem, "title": only.stem, "since": e["timestamp"], "uuid": e.get("uuid"),
                     "waiting_on": describe(e), "minutes": round((now - ts(e["timestamp"])) / 60)}]
        return []
    paths = {p.stem: p for p in TRANSCRIPTS.glob("*/*.jsonl")}
    out = []
    for r in records(now - LOOKBACK_S):
        if r.get("isArchived") or now * 1000 - r.get("lastActivityAt", 0) > LOOKBACK_S * 1000:
            continue
        path = paths.get(r.get("cliSessionId", ""))
        if not path:
            continue
        e = pending(read_events(path, whole=False), now)
        if not e or now - ts(e["timestamp"]) < minutes * 60:
            continue
        out.append({"session": r["sessionId"], "title": r.get("title") or "(untitled)", "since": e["timestamp"],
                    "uuid": e.get("uuid"), "waiting_on": describe(e), "minutes": round((now - ts(e["timestamp"])) / 60),
                    "scheduled": bool(r.get("scheduledTaskId"))})
    return sorted(out, key=lambda x: -x["minutes"])


def chat_id() -> str | None:
    try:
        m = re.search(r'allow_from\s*=\s*\[\s*"?(-?\d+)', (HOME / ".farplane" / "config.toml").read_text())
    except OSError:
        return None
    return m.group(1) if m else None


def telegram(text: str) -> bool:
    cid = chat_id()
    if not cid:
        print("telegram: no allow_from chat id in ~/.farplane/config.toml", file=sys.stderr)
        return False
    env = dict(os.environ, TELEGRAM_CHAT_ID=cid)
    r = subprocess.run([sys.executable, str(SENDER), "--raw-telegram", "--disable-preview", "--text", text],
                       env=env, capture_output=True, text=True, timeout=60)
    if r.returncode != 0:
        print("telegram: send failed: " + (r.stderr or r.stdout).strip()[:200], file=sys.stderr)
    return r.returncode == 0


def message(items: list[dict]) -> str:
    lines = ["Frozen threads: no reply for 10+ minutes, boss." if len(items) > 1 else "A thread is frozen: no reply for 10+ minutes, boss."]
    for x in items:
        again = " (still frozen)" if x.get("reminder") else ""
        lines.append(f"• {x['title']}{again}: {x['minutes']} min waiting on {x['waiting_on']}. "
                     f"Open: claude://claude.ai/epitaxy/{x['session']}")
    lines.append("Stop the thread and send your message again; it usually answers then.")
    return "\n".join(lines)


def cmd_check(a: argparse.Namespace) -> int:
    now = ts(a.now) if a.now else time.time()
    found = find_frozen(a.minutes, now, Path(a.transcript) if a.transcript else None)
    print(json.dumps({"checked_at": datetime.fromtimestamp(now, timezone.utc).isoformat(timespec="seconds"),
                      "frozen": found}, indent=2))
    if not (a.notify or a.dry_run) or not found:
        return 0
    STATE_DIR.mkdir(parents=True, exist_ok=True)
    try:
        state = json.load(open(STATE))
    except (OSError, ValueError):
        state = {}
    due = []
    for x in found:
        seen = state.get(x["session"], {})
        if seen.get("uuid") != x["uuid"]:
            due.append(x)
        elif not seen.get("reminded") and x["minutes"] * 60 >= REMIND_AFTER_S:
            due.append(dict(x, reminder=True))
    if not due:
        return 0
    text = message(due)
    if a.dry_run:
        print("--- would send ---\n" + text)
        return 0
    if telegram(text):
        for x in due:
            state[x["session"]] = {"uuid": x["uuid"], "alerted_at": now, "reminded": bool(x.get("reminder"))}
        live = {x["session"] for x in found}
        state = {k: v for k, v in state.items() if k in live}
        json.dump(state, open(STATE, "w"), indent=2)
    return 0


def cmd_install(a: argparse.Namespace) -> int:
    STATE_DIR.mkdir(parents=True, exist_ok=True)
    PLIST.write_text(f"""<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
<plist version="1.0">
<dict>
  <key>Label</key><string>{LABEL}</string>
  <key>ProgramArguments</key>
  <array>
    <string>/usr/bin/python3</string>
    <string>{Path(__file__).resolve()}</string>
    <string>check</string>
    <string>--notify</string>
  </array>
  <key>StartInterval</key><integer>{a.every}</integer>
  <key>RunAtLoad</key><true/>
  <key>StandardOutPath</key><string>{STATE_DIR / 'last-check.json'}</string>
  <key>StandardErrorPath</key><string>{STATE_DIR / 'errors.log'}</string>
</dict>
</plist>
""")
    uid = str(os.getuid())
    subprocess.run(["launchctl", "bootout", f"gui/{uid}", str(PLIST)], capture_output=True)
    r = subprocess.run(["launchctl", "bootstrap", f"gui/{uid}", str(PLIST)], capture_output=True, text=True)
    print(f"installed {PLIST} (every {a.every} s)" if r.returncode == 0 else "launchctl bootstrap failed: " + r.stderr.strip())
    return r.returncode


def cmd_uninstall(_: argparse.Namespace) -> int:
    subprocess.run(["launchctl", "bootout", f"gui/{os.getuid()}", str(PLIST)], capture_output=True)
    PLIST.unlink(missing_ok=True)
    print(f"removed {PLIST}")
    return 0


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = ap.add_subparsers(dest="cmd", required=True)
    c = sub.add_parser("check")
    c.add_argument("--minutes", type=float, default=10)
    c.add_argument("--notify", action="store_true", help="tell Kenji on Telegram (once per freeze, one reminder)")
    c.add_argument("--dry-run", action="store_true", help="print the Telegram message instead of sending it")
    c.add_argument("--now", help="ISO time to judge at, for replays")
    c.add_argument("--transcript", help="judge one transcript file instead of every open thread")
    i = sub.add_parser("install")
    i.add_argument("--every", type=int, default=300, help="seconds between checks")
    sub.add_parser("uninstall")
    a = ap.parse_args()
    return {"check": cmd_check, "install": cmd_install, "uninstall": cmd_uninstall}[a.cmd](a)


if __name__ == "__main__":
    sys.exit(main())
