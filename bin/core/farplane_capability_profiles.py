"""Capability-profile policy, validation, and portable resolution.

Profiles are optional, restriction-only policy documents.  They are deliberately
separate from ``farplane/pm.json``: PM metadata groups visible work, while a
profile describes the capabilities a runtime adapter may equip on fresh work.
"""

from __future__ import annotations

import hashlib
import json
import os
import re
import tempfile
from datetime import datetime, timezone
import tomllib
from pathlib import Path
from typing import Any, Literal

import yaml
from pydantic import BaseModel, ConfigDict, Field, ValidationError, field_validator

from farplane_cli_base import CORE_ROOT, DEFAULT_CODEX_HOME, DEFAULT_FARPLANE_HOME


CAPABILITY_PROFILES_FILE = "capability-profiles.yaml"
PROJECT_PROFILES_PATH = Path("farplane") / CAPABILITY_PROFILES_FILE
SESSION_SNAPSHOT_ROOT = Path(".farplane") / "capability-profiles" / "sessions"
GLOBAL_PROFILES_PATH = DEFAULT_FARPLANE_HOME / CAPABILITY_PROFILES_FILE
PROFILE_ID_PATTERN = re.compile(r"[a-z0-9]+(?:-[a-z0-9]+)*")


class CapabilityProfileError(ValueError):
    """A human-safe validation or persistence error for profile policy."""


class UniqueKeyLoader(yaml.SafeLoader):
    """Safe YAML loader that rejects duplicate mapping keys."""


class DuplicateKeyError(yaml.constructor.ConstructorError):
    """Raised when authored YAML contains a mapping key more than once."""


def _construct_unique_mapping(
    loader: UniqueKeyLoader,
    node: yaml.nodes.MappingNode,
    deep: bool = False,
) -> dict[Any, Any]:
    mapping: dict[Any, Any] = {}
    for key_node, value_node in node.value:
        key = loader.construct_object(key_node, deep=deep)
        if key in mapping:
            raise DuplicateKeyError(
                "while constructing a mapping",
                node.start_mark,
                f"found duplicate key {key!r}",
                key_node.start_mark,
            )
        mapping[key] = loader.construct_object(value_node, deep=deep)
    return mapping


UniqueKeyLoader.add_constructor(
    yaml.resolver.BaseResolver.DEFAULT_MAPPING_TAG,
    _construct_unique_mapping,
)


class CapabilityAllowlist(BaseModel):
    """The exact skills and MCP servers a restricted profile may use."""

    model_config = ConfigDict(extra="forbid")

    skill_ids: list[str] = Field(default_factory=list)
    mcp_server_ids: list[str] = Field(default_factory=list)

    @field_validator("skill_ids", "mcp_server_ids")
    @classmethod
    def canonical_ids(cls, value: list[str]) -> list[str]:
        if not isinstance(value, list) or not all(isinstance(item, str) for item in value):
            raise ValueError("must be a list of string IDs")
        normalized = [item.strip() for item in value]
        if any(not item for item in normalized):
            raise ValueError("must not contain empty IDs")
        if len(normalized) != len(set(normalized)):
            raise ValueError("must not contain duplicate IDs")
        return sorted(normalized)


class CapabilityProfile(BaseModel):
    """One named restriction policy."""

    model_config = ConfigDict(extra="forbid")

    label: str
    allow: CapabilityAllowlist
    extends: str | None = None

    @field_validator("label")
    @classmethod
    def non_empty_label(cls, value: str) -> str:
        if not isinstance(value, str) or not value.strip():
            raise ValueError("must be a non-empty string")
        return value.strip()

    @field_validator("extends")
    @classmethod
    def canonical_extends(cls, value: str | None) -> str | None:
        if value is None:
            return None
        if not value.strip():
            raise ValueError("must be a non-empty profile reference")
        return value.strip()


class CapabilityProfilesDocument(BaseModel):
    """Tracked global or project capability-profile document."""

    model_config = ConfigDict(extra="forbid")

    version: Literal[1] = 1
    profiles: dict[str, CapabilityProfile] = Field(default_factory=dict)
    active_profile_ref: str | None = None

    @field_validator("profiles")
    @classmethod
    def canonical_profile_ids(cls, value: dict[str, CapabilityProfile]) -> dict[str, CapabilityProfile]:
        invalid = [profile_id for profile_id in value if not PROFILE_ID_PATTERN.fullmatch(profile_id)]
        if invalid:
            raise ValueError(f"invalid profile IDs: {', '.join(sorted(invalid))}")
        return value

    @field_validator("active_profile_ref")
    @classmethod
    def canonical_active_ref(cls, value: str | None) -> str | None:
        if value is None:
            return None
        if not value.strip():
            raise ValueError("must be a non-empty profile reference")
        return value.strip()


def empty_document(*, project: bool) -> CapabilityProfilesDocument:
    return CapabilityProfilesDocument(active_profile_ref=None if project else None)


def project_profiles_path(project_root: Path) -> Path:
    return project_root.expanduser().resolve() / PROJECT_PROFILES_PATH


def global_profiles_path(farplane_home: Path = DEFAULT_FARPLANE_HOME) -> Path:
    return farplane_home.expanduser().resolve() / CAPABILITY_PROFILES_FILE


def _load_yaml_document(path: Path, *, project: bool) -> CapabilityProfilesDocument:
    if not path.exists():
        return empty_document(project=project)
    try:
        raw = yaml.load(path.read_text(encoding="utf-8"), Loader=UniqueKeyLoader)
    except DuplicateKeyError as exc:
        raise CapabilityProfileError(f"invalid_profile_yaml:duplicate_key:{path}") from exc
    except (OSError, yaml.YAMLError) as exc:
        raise CapabilityProfileError(f"invalid_profile_yaml:{path}:{exc.__class__.__name__}") from exc
    if raw is None:
        raw = {}
    if not isinstance(raw, dict):
        raise CapabilityProfileError(f"invalid_profile_document:{path}:expected_object")
    try:
        document = CapabilityProfilesDocument.model_validate(raw)
    except ValidationError as exc:
        raise CapabilityProfileError(f"invalid_profile_document:{path}:{exc.errors(include_url=False)}") from exc
    if not project and document.active_profile_ref is not None:
        raise CapabilityProfileError(f"invalid_global_profile_document:{path}:active_profile_ref_not_allowed")
    return document


def _profile_ref(scope: Literal["global", "project"], profile_id: str) -> str:
    return f"{scope}:{profile_id}"


def _parse_profile_ref(value: str) -> tuple[Literal["global", "project"], str]:
    if ":" not in value:
        raise CapabilityProfileError(f"invalid_profile_ref:{value}")
    scope, profile_id = value.split(":", 1)
    if scope not in {"global", "project"} or not PROFILE_ID_PATTERN.fullmatch(profile_id):
        raise CapabilityProfileError(f"invalid_profile_ref:{value}")
    return scope, profile_id  # type: ignore[return-value]


def _known_skill_ids(codex_home: Path = DEFAULT_CODEX_HOME) -> list[str]:
    skill_ids: set[str] = set()
    registry_path = CORE_ROOT / "docs" / "skills" / "registry.jsonl"
    try:
        for line in registry_path.read_text(encoding="utf-8").splitlines():
            row = json.loads(line)
            if isinstance(row, dict) and isinstance(row.get("name"), str):
                skill_ids.add(row["name"])
    except (OSError, json.JSONDecodeError) as exc:
        raise CapabilityProfileError(f"skill_catalog_unavailable:{exc.__class__.__name__}") from exc

    config_path = codex_home.expanduser().resolve() / "config.toml"
    if config_path.exists():
        try:
            with config_path.open("rb") as handle:
                config = tomllib.load(handle)
            configured_skills = config.get("skills", {}).get("config", [])
            if isinstance(configured_skills, list):
                for entry in configured_skills:
                    if isinstance(entry, dict) and isinstance(entry.get("name"), str):
                        skill_ids.add(entry["name"])
        except (OSError, tomllib.TOMLDecodeError) as exc:
            raise CapabilityProfileError(f"codex_config_unavailable:{exc.__class__.__name__}") from exc
    return sorted(skill_ids)


def _known_mcp_server_ids(codex_home: Path = DEFAULT_CODEX_HOME) -> list[str]:
    config_path = codex_home.expanduser().resolve() / "config.toml"
    if not config_path.exists():
        return []
    try:
        with config_path.open("rb") as handle:
            config = tomllib.load(handle)
    except (OSError, tomllib.TOMLDecodeError) as exc:
        raise CapabilityProfileError(f"codex_config_unavailable:{exc.__class__.__name__}") from exc
    servers = config.get("mcp_servers", {})
    if not isinstance(servers, dict):
        raise CapabilityProfileError("codex_config_invalid:mcp_servers_not_object")
    return sorted(key for key in servers if isinstance(key, str))


def _resolve_global_profile(
    profile_id: str,
    global_document: CapabilityProfilesDocument,
) -> CapabilityProfile:
    profile = global_document.profiles.get(profile_id)
    if profile is None:
        raise CapabilityProfileError(f"unknown_profile_ref:global:{profile_id}")
    if profile.extends is not None:
        raise CapabilityProfileError(f"invalid_capability_profile:global:{profile_id}:global_profiles_must_not_extend")
    return profile


def _resolve_active_profile(
    global_document: CapabilityProfilesDocument,
    project_document: CapabilityProfilesDocument,
) -> tuple[str, CapabilityProfile] | None:
    active_ref = project_document.active_profile_ref
    if active_ref is None:
        return None
    scope, profile_id = _parse_profile_ref(active_ref)
    if scope == "global":
        return active_ref, _resolve_global_profile(
            profile_id,
            global_document,
        )

    profile = project_document.profiles.get(profile_id)
    if profile is None:
        raise CapabilityProfileError(f"unknown_profile_ref:{active_ref}")
    if profile.extends is None:
        return active_ref, profile
    parent_scope, parent_id = _parse_profile_ref(profile.extends)
    if parent_scope != "global":
        raise CapabilityProfileError(f"invalid_capability_profile:{active_ref}:project_extends_must_be_global")
    parent = _resolve_global_profile(
        parent_id,
        global_document,
    )
    allowed_skills = sorted(set(profile.allow.skill_ids) & set(parent.allow.skill_ids))
    allowed_servers = sorted(set(profile.allow.mcp_server_ids) & set(parent.allow.mcp_server_ids))
    return active_ref, CapabilityProfile(
        label=profile.label,
        extends=profile.extends,
        allow={"skill_ids": allowed_skills, "mcp_server_ids": allowed_servers},
    )


def _validate_documents(
    global_document: CapabilityProfilesDocument,
    project_document: CapabilityProfilesDocument,
) -> None:
    """Reject broken references while keeping definitions runtime-portable."""

    if global_document.active_profile_ref is not None:
        raise CapabilityProfileError("invalid_global_profile_document:active_profile_ref_not_allowed")
    for profile_id, profile in global_document.profiles.items():
        _resolve_global_profile(
            profile_id,
            global_document,
        )
    for profile_id, profile in project_document.profiles.items():
        ref = _profile_ref("project", profile_id)
        if profile.extends is None:
            continue
        parent_scope, parent_id = _parse_profile_ref(profile.extends)
        if parent_scope != "global":
            raise CapabilityProfileError(f"invalid_capability_profile:{ref}:project_extends_must_be_global")
        _resolve_global_profile(
            parent_id,
            global_document,
        )


def _document_payload(document: CapabilityProfilesDocument, *, project: bool) -> dict[str, Any]:
    payload = document.model_dump(mode="json", exclude_none=True)
    if project and "active_profile_ref" not in payload:
        payload["active_profile_ref"] = None
    return payload


def _policy_digest(profile_ref: str | None, profile: CapabilityProfile | None) -> str:
    stable = {
        "profile_ref": profile_ref,
        "allow": profile.allow.model_dump(mode="json") if profile else None,
    }
    return hashlib.sha256(json.dumps(stable, sort_keys=True, separators=(",", ":")).encode("utf-8")).hexdigest()


def resolve_capability_profiles(
    project_root: Path,
    *,
    farplane_home: Path = DEFAULT_FARPLANE_HOME,
    codex_home: Path = DEFAULT_CODEX_HOME,
) -> dict[str, Any]:
    """Read portable policy documents and expose local catalog suggestions."""

    root = project_root.expanduser().resolve()
    if not root.is_dir():
        raise CapabilityProfileError(f"project_root_missing:{root}")
    global_path = global_profiles_path(farplane_home)
    project_path = project_profiles_path(root)
    global_document = _load_yaml_document(global_path, project=False)
    project_document = _load_yaml_document(project_path, project=True)
    known_skills = _known_skill_ids(codex_home)
    known_mcp_servers = _known_mcp_server_ids(codex_home)
    _validate_documents(global_document, project_document)
    resolved = _resolve_active_profile(global_document, project_document)
    profile_ref, profile = resolved if resolved is not None else (None, None)
    return {
        "ok": True,
        "project_root": str(root),
        "documents": {
            "global": {"path": str(global_path), "document": _document_payload(global_document, project=False)},
            "project": {"path": str(project_path), "document": _document_payload(project_document, project=True)},
        },
        "catalog": {"skill_ids": known_skills, "mcp_server_ids": known_mcp_servers},
        "active_profile": (
            {
                "ref": profile_ref,
                "label": profile.label,
                "allow": profile.allow.model_dump(mode="json"),
                "extends": profile.extends,
            }
            if profile_ref is not None and profile is not None
            else None
        ),
        "enforcement": {
            "state": "profiled" if profile is not None else "full_access",
            "policy_digest": _policy_digest(profile_ref, profile),
        },
    }


def _atomic_write(path: Path, content: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    descriptor, temporary_name = tempfile.mkstemp(prefix=f".{path.name}.", suffix=".tmp", dir=path.parent)
    try:
        with os.fdopen(descriptor, "w", encoding="utf-8") as handle:
            handle.write(content)
        os.replace(temporary_name, path)
    except OSError:
        try:
            os.unlink(temporary_name)
        except OSError:
            pass
        raise


def write_capability_profiles(
    project_root: Path,
    scope: Literal["global", "project"],
    document_data: dict[str, Any],
    *,
    farplane_home: Path = DEFAULT_FARPLANE_HOME,
    codex_home: Path = DEFAULT_CODEX_HOME,
) -> dict[str, Any]:
    """Validate and atomically write one policy document, then resolve the project."""

    try:
        document = CapabilityProfilesDocument.model_validate(document_data)
    except ValidationError as exc:
        raise CapabilityProfileError(f"invalid_profile_document:input:{exc.errors(include_url=False)}") from exc
    if scope == "global" and document.active_profile_ref is not None:
        raise CapabilityProfileError("invalid_global_profile_document:active_profile_ref_not_allowed")
    root = project_root.expanduser().resolve()
    if not root.is_dir():
        raise CapabilityProfileError(f"project_root_missing:{root}")
    target = global_profiles_path(farplane_home) if scope == "global" else project_profiles_path(root)
    global_document = document if scope == "global" else _load_yaml_document(global_profiles_path(farplane_home), project=False)
    project_document = document if scope == "project" else _load_yaml_document(project_profiles_path(root), project=True)
    _validate_documents(global_document, project_document)
    content = yaml.safe_dump(
        _document_payload(document, project=scope == "project"),
        sort_keys=False,
        allow_unicode=True,
    )
    _atomic_write(target, content)
    payload = resolve_capability_profiles(root, farplane_home=farplane_home, codex_home=codex_home)
    payload["write"] = {"scope": scope, "path": str(target)}
    return payload


def record_capability_profile_snapshot(
    project_root: Path,
    *,
    thread_id: str,
    profile_ref: str | None,
    policy_digest: str,
) -> dict[str, Any]:
    """Persist one immutable launch-policy receipt for an actual Codex thread."""

    root = project_root.expanduser().resolve()
    if not root.is_dir():
        raise CapabilityProfileError(f"project_root_missing:{root}")
    normalized_thread_id = thread_id.strip()
    if not normalized_thread_id or any(character in normalized_thread_id for character in "/\\\0"):
        raise CapabilityProfileError("invalid_thread_id")
    normalized_digest = policy_digest.strip().lower()
    if not re.fullmatch(r"[0-9a-f]{64}", normalized_digest):
        raise CapabilityProfileError("invalid_policy_digest")
    if profile_ref is not None:
        _parse_profile_ref(profile_ref)
    receipt_path = root / SESSION_SNAPSHOT_ROOT / f"{hashlib.sha256(normalized_thread_id.encode('utf-8')).hexdigest()}.json"
    payload = {
        "version": 1,
        "thread_id": normalized_thread_id,
        "profile_ref": profile_ref,
        "policy_digest": normalized_digest,
    }
    if receipt_path.exists():
        try:
            existing = json.loads(receipt_path.read_text(encoding="utf-8"))
        except (OSError, json.JSONDecodeError) as exc:
            raise CapabilityProfileError(f"invalid_profile_snapshot:{receipt_path}:{exc.__class__.__name__}") from exc
        comparison = {key: existing.get(key) for key in payload}
        if comparison != payload:
            raise CapabilityProfileError(f"capability_profile_snapshot_conflict:{normalized_thread_id}")
        return {"ok": True, "recorded": False, "path": str(receipt_path), "snapshot": existing}
    complete_payload = {
        **payload,
        "recorded_at": datetime.now(timezone.utc).isoformat().replace("+00:00", "Z"),
    }
    _atomic_write(receipt_path, json.dumps(complete_payload, indent=2, sort_keys=True) + "\n")
    return {"ok": True, "recorded": True, "path": str(receipt_path), "snapshot": complete_payload}
