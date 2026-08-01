#!/usr/bin/env python3
"""Validate commit-safe, skill-local config.toml files."""

from __future__ import annotations

import argparse
import re
import sys
import tomllib
from pathlib import Path
from typing import Any


SCHEMA_VERSION = "0.1.0"
ALLOWED_ROOT_KEYS = {"schema_version", "skill", "defaults", "profiles", "providers"}
TABLE_ROOT_KEYS = {"defaults", "profiles", "providers"}
FORBIDDEN_KEYS = {
    "access_key",
    "access_key_id",
    "api_key",
    "auth",
    "authorization",
    "authorization_header",
    "cookie",
    "credential",
    "credentials",
    "encryption_key",
    "password",
    "private_key",
    "secret",
    "secret_access_key",
    "session_cookie",
    "signing_key",
    "token",
    "webhook_secret",
}
FORBIDDEN_SUFFIXES = (
    "_api_key",
    "_credential",
    "_credentials",
    "_password",
    "_private_key",
    "_secret",
    "_token",
)
SECRET_VALUE_PATTERNS = (
    re.compile(r"^Bearer\s+\S+", re.I),
    re.compile(r"-----BEGIN (?:RSA |EC |OPENSSH )?PRIVATE KEY-----"),
    re.compile(r"^(?:sk|api|token|secret)[-_][A-Za-z0-9_-]{12,}$", re.I),
    re.compile(r"^AKIA[A-Z0-9]{16}$"),
    re.compile(r"^gh[pousr]_[A-Za-z0-9]{20,}$"),
    re.compile(r"^xox[baprs]-[A-Za-z0-9-]{10,}$"),
)
SCALAR_TYPES = (str, int, float, bool)


def normalized_key(key: str) -> str:
    return key.strip().lower().replace("-", "_")


def key_is_forbidden(key: str) -> bool:
    normalized = normalized_key(key)
    return normalized in FORBIDDEN_KEYS or normalized.endswith(FORBIDDEN_SUFFIXES)


def scalar_errors(value: Any, path: str) -> list[str]:
    if isinstance(value, SCALAR_TYPES):
        if isinstance(value, str) and any(pattern.search(value) for pattern in SECRET_VALUE_PATTERNS):
            return [f"{path}: value resembles a credential and must come from runtime env/Doppler"]
        return []
    if isinstance(value, list):
        errors: list[str] = []
        for index, item in enumerate(value):
            if isinstance(item, (dict, list)):
                errors.append(f"{path}[{index}]: arrays may contain TOML scalar values only")
            else:
                errors.extend(scalar_errors(item, f"{path}[{index}]"))
        return errors
    return [f"{path}: values must be TOML scalars or scalar arrays, got {type(value).__name__}"]


def nested_errors(value: Any, path: str) -> list[str]:
    if not isinstance(value, dict):
        return scalar_errors(value, path)

    errors: list[str] = []
    for key, child in value.items():
        child_path = f"{path}.{key}"
        if key_is_forbidden(key):
            errors.append(f"{child_path}: credential-bearing key is forbidden in tracked skill config")
            continue
        errors.extend(nested_errors(child, child_path))
    return errors


def validate_config(path: Path) -> list[str]:
    try:
        payload = tomllib.loads(path.read_text(encoding="utf-8"))
    except (OSError, UnicodeError, tomllib.TOMLDecodeError) as exc:
        return [f"{path}: invalid TOML: {exc}"]

    errors: list[str] = []
    unknown = sorted(set(payload) - ALLOWED_ROOT_KEYS)
    if unknown:
        errors.append(f"{path}: unsupported root keys: {', '.join(unknown)}")
    if payload.get("schema_version") != SCHEMA_VERSION:
        errors.append(f"{path}: schema_version must be {SCHEMA_VERSION!r}")
    if payload.get("skill") != path.parent.name:
        errors.append(f"{path}: skill must match owning directory {path.parent.name!r}")

    for key in TABLE_ROOT_KEYS:
        if key in payload and not isinstance(payload[key], dict):
            errors.append(f"{path}: {key} must be a TOML table")

    for key, value in payload.items():
        if key_is_forbidden(key):
            errors.append(f"{path}.{key}: credential-bearing key is forbidden in tracked skill config")
        elif key in TABLE_ROOT_KEYS:
            errors.extend(nested_errors(value, f"{path}.{key}"))
        elif key in {"schema_version", "skill"}:
            errors.extend(scalar_errors(value, f"{path}.{key}"))
    return errors


def config_paths(root: Path) -> list[Path]:
    paths: list[Path] = []
    for parent in (root / "skills", root / ".agents" / "skills"):
        if parent.is_dir():
            paths.extend(parent.glob("*/config.toml"))
    return sorted(paths)


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", type=Path, default=Path.cwd())
    args = parser.parse_args()

    paths = config_paths(args.root.resolve())
    errors = [error for path in paths for error in validate_config(path)]
    if errors:
        print("\n".join(errors), file=sys.stderr)
        return 1
    print(f"skill configs OK: {len(paths)} file(s)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
