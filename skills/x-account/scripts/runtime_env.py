#!/usr/bin/env python3
"""Read X credentials from the injected process environment."""

from __future__ import annotations

import base64
import json
import os
from pathlib import Path
from urllib.parse import urlencode
from urllib.request import Request, urlopen

TOKEN_URL = "https://api.x.com/2/oauth2/token"
ROTATED_KEYS = ("FARPLANE_X_OAUTH2_ACCESS_TOKEN", "FARPLANE_X_OAUTH2_REFRESH_TOKEN")


def oauth2_state_path() -> Path:
    home = (os.environ.get("FARPLANE_STATE_DIR") or os.environ.get("FARPLANE_CONFIG_HOME") or "").strip()
    return (Path(home).expanduser() if home else Path.home() / ".farplane") / "state" / "x-oauth2.json"


def load_runtime_values() -> dict[str, str]:
    values = {key: value for key, value in os.environ.items() if key.startswith("FARPLANE_X_")}
    # X rotates the refresh token on every use, so the last rotated pair wins over injected secrets.
    try:
        rotated = json.loads(oauth2_state_path().read_text(encoding="utf-8"))
    except (OSError, ValueError):
        rotated = {}
    values.update({key: str(rotated[key]) for key in ROTATED_KEYS if rotated.get(key)})
    return values


def refresh_oauth2_access_token(values: dict[str, str]) -> str:
    """Exchange the refresh token, persist the rotated pair privately, and return the new access token."""
    refresh = values.get("FARPLANE_X_OAUTH2_REFRESH_TOKEN")
    client_id = values.get("FARPLANE_X_OAUTH2_CLIENT_ID")
    if not refresh or not client_id:
        raise RuntimeError("FARPLANE_X_OAUTH2_REFRESH_TOKEN and FARPLANE_X_OAUTH2_CLIENT_ID are required to refresh")
    headers = {"Content-Type": "application/x-www-form-urlencoded", "User-Agent": "Farplane x-account"}
    secret = values.get("FARPLANE_X_OAUTH2_CLIENT_SECRET")
    if secret:
        headers["Authorization"] = "Basic " + base64.b64encode(f"{client_id}:{secret}".encode()).decode()
    body = urlencode({"grant_type": "refresh_token", "refresh_token": refresh, "client_id": client_id}).encode()
    with urlopen(Request(TOKEN_URL, data=body, headers=headers, method="POST"), timeout=30) as response:
        payload = json.loads(response.read().decode("utf-8"))
    access = str(payload.get("access_token") or "")
    if not access:
        raise RuntimeError("X token refresh returned no access token")
    rotated = {"FARPLANE_X_OAUTH2_ACCESS_TOKEN": access,
               "FARPLANE_X_OAUTH2_REFRESH_TOKEN": str(payload.get("refresh_token") or refresh)}
    path = oauth2_state_path()
    path.parent.mkdir(parents=True, exist_ok=True)
    fd = os.open(path, os.O_WRONLY | os.O_CREAT | os.O_TRUNC, 0o600)
    with os.fdopen(fd, "w", encoding="utf-8") as handle:
        json.dump(rotated, handle)
    values.update(rotated)
    return access


def env_value(key: str, runtime_values: dict[str, str] | None = None) -> str | None:
    return os.environ.get(key) or (runtime_values or {}).get(key) or None
