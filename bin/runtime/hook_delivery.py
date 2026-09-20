"""Bounded, metadata-only lifecycle delivery diagnostics; never gate a turn."""
from __future__ import annotations

import argparse
import json
import os
import sys
import tempfile
import urllib.error
import urllib.request
from datetime import datetime, timezone
from pathlib import Path

CORE_DIR = Path(__file__).resolve().parents[1] / "core"
if str(CORE_DIR) not in sys.path:
    sys.path.insert(0, str(CORE_DIR))
from runtime_config import farplane_home

EVENTS = ("UserPromptSubmit", "Stop", "SubagentStart", "SubagentStop")


def record_status(event: str, status: str, *, reason: str | None = None,
                  http_status: int | None = None) -> None:
    """One atomic latest receipt per known event; errors contain no remote data."""
    row = {"schemaVersion": 1, "hookEventName": event if event in EVENTS else "unknown",
           "status": status, "updatedAt": datetime.now(timezone.utc).isoformat()}
    if reason:
        row["reason"] = reason
    if http_status is not None:
        row["httpStatus"] = http_status
    temporary = None
    try:
        directory = farplane_home() / "state" / "hook-delivery"
        directory.mkdir(parents=True, exist_ok=True)
        with tempfile.NamedTemporaryFile(mode="w", encoding="utf-8", dir=directory,
                                         prefix=".delivery-", delete=False) as handle:
            temporary = Path(handle.name)
            json.dump(row, handle)
            handle.write("\n")
        os.replace(temporary, directory / f"{row['hookEventName']}.json")
    except OSError:
        print("farplane: telemetry diagnostic write failed", file=sys.stderr)
    finally:
        if temporary is not None:
            try:
                temporary.unlink(missing_ok=True)
            except OSError:
                pass


def validate_event(event: dict[str, object], argv: list[str] | None = None) -> bool:
    parser = argparse.ArgumentParser(description="Send classified Farplane lifecycle telemetry")
    parser.add_argument("--expect-event", choices=EVENTS)
    args = parser.parse_args(argv)
    if args.expect_event and event.get("hook_event_name") != args.expect_event:
        record_status(args.expect_event, "failed", reason="event_mismatch")
        print(f"farplane: telemetry event mismatch; expected {args.expect_event}; not sent",
              file=sys.stderr)
        return False
    return True


def deliver(body: dict[str, object], endpoint: str | None, token: str | None) -> None:
    event = str(body.get("hookType", "unknown"))
    if not endpoint:
        record_status(event, "unconfigured", reason="missing_endpoint")
        return
    record_status(event, "attempted")
    try:
        headers = {"content-type": "application/json"}
        if token:
            headers["x-farplane-telemetry-token"] = token
        request = urllib.request.Request(endpoint, data=json.dumps(body).encode("utf-8"),
                                         headers=headers, method="POST")
        with urllib.request.urlopen(request, timeout=2) as response:
            status = response.status
        if 200 <= status < 300:
            record_status(event, "accepted", http_status=status)
        else:
            record_status(event, "failed", reason="http_error", http_status=status)
    except urllib.error.HTTPError as error:
        record_status(event, "failed", reason="http_error", http_status=error.code)
        print(f"farplane: telemetry HTTP failure ({error.code})", file=sys.stderr)
    except Exception:
        record_status(event, "failed", reason="transport_error")
        print("farplane: telemetry transport failure", file=sys.stderr)
