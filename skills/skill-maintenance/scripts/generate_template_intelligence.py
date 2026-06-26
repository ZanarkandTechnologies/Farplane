#!/usr/bin/env python3
"""Generate skill-template history, rollout, feature, and eval signals.

Ownership: skill-maintenance owns this generated governance artifact. Inputs are
local Farplane files plus git history; outputs are UI-ready JSON/JS graph assets
and archived template snapshots. The script does not edit skill packages or
registry rows.
"""

from __future__ import annotations

import argparse
import json
import re
import subprocess
import sys
from collections import Counter
from dataclasses import dataclass
from datetime import UTC, datetime
from pathlib import Path
from typing import Any


SCRIPT_PATH = Path(__file__).resolve()
REPO_ROOT = SCRIPT_PATH.parents[3]
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from bin.validators.template_usage import normalize_template_uses, template_target_basis
CURRENT_TEMPLATE_VERSION = "0.3.2"
TEMPLATE_PATH = Path("docs/skills/templates/SKILL_TEMPLATE.md")
DEFAULT_OUT = Path("skills/skill-maintenance/graph/skill-template-intelligence.json")
DEFAULT_JS_OUT = Path("skills/skill-maintenance/graph/skill-template-intelligence.js")
DEFAULT_ARCHIVE_DIR = Path("skills/skill-maintenance/templates/archive")
PROJECT_ROOTS = (
    Path("."),
    Path("../Farplane-UI"),
)


@dataclass(frozen=True)
class TemplateSnapshot:
    version: str
    source_commit: str
    introduced_at: str
    subject: str
    text: str


def parse_scalar(value: str) -> Any:
    value = value.strip()
    if not value:
        return ""
    if value in {"true", "false"}:
        return value == "true"
    if value.startswith(("\"", "'")) and value.endswith(("\"", "'")):
        return value[1:-1]
    return value


def parse_simple_yaml(raw: str) -> dict[str, Any]:
    parsed: dict[str, Any] = {}
    current_key: str | None = None
    current_subkey: str | None = None
    for line in raw.splitlines():
        if not line.strip() or line.lstrip().startswith("#"):
            continue
        if not line.startswith(" "):
            current_subkey = None
            key, _, value = line.partition(":")
            key = key.strip()
            parsed[key] = {} if not value.strip() else parse_scalar(value)
            current_key = key
            continue
        if current_key is None:
            continue
        current_value = parsed.get(current_key)
        stripped = line.strip()
        if stripped.startswith("- "):
            item = parse_scalar(stripped[2:].strip())
            if current_subkey and isinstance(current_value, dict):
                current_value.setdefault(current_subkey, []).append(item)
            else:
                if not isinstance(current_value, list):
                    current_value = []
                    parsed[current_key] = current_value
                current_value.append(item)
            continue
        if ":" in stripped:
            subkey, _, value = stripped.partition(":")
            if not isinstance(current_value, dict):
                current_value = {}
                parsed[current_key] = current_value
            current_value[subkey.strip()] = [] if not value.strip() else parse_scalar(value)
            current_subkey = subkey.strip()
    return parsed


def split_template_metadata(text: str) -> tuple[dict[str, Any], str]:
    if not text.startswith("---\n"):
        return {}, text
    first_end = text.find("\n---\n", 4)
    if first_end == -1:
        return {}, text
    raw = text[4:first_end]
    body = text[first_end + len("\n---\n") :].lstrip("\n")
    if body.startswith("---\n"):
        return parse_simple_yaml(raw), body
    return {}, text


def run_git(args: list[str], repo_root: Path = REPO_ROOT) -> str:
    result = subprocess.run(
        ["git", *args],
        cwd=repo_root,
        check=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True,
    )
    return result.stdout


def load_jsonl(path: Path) -> list[dict[str, Any]]:
    if not path.exists():
        return []
    rows: list[dict[str, Any]] = []
    for line in path.read_text(encoding="utf-8").splitlines():
        if line.strip():
            rows.append(json.loads(line))
    return rows


def parse_template_version(text: str) -> str:
    metadata, body = split_template_metadata(text)
    template_version = metadata.get("template_version")
    if isinstance(template_version, str) and template_version:
        return template_version
    match = re.search(r"skill_template_version:\s*[\"']?([^\"'\n]+)", body)
    return match.group(1).strip() if match else "unknown"


def template_metadata_summary(text: str) -> dict[str, Any]:
    metadata, _body = split_template_metadata(text)
    return {
        "template_id": metadata.get("template_id", ""),
        "template_version": metadata.get("template_version", ""),
        "feature_refs": metadata.get("feature_refs", []),
        "surface_fields": metadata.get("surface_fields", {}),
    }


def section_names(markdown: str) -> list[str]:
    names: list[str] = []
    in_fence = False
    for line in markdown.splitlines():
        if line.startswith("```"):
            in_fence = not in_fence
            continue
        if in_fence:
            continue
        if line.startswith("## "):
            names.append(line[3:].strip())
    return names


def changed_section_names(previous: str | None, current: str) -> list[str]:
    current_sections = set(section_names(current))
    if previous is None:
        return sorted(current_sections)
    previous_sections = set(section_names(previous))
    return sorted(current_sections.symmetric_difference(previous_sections))


def discover_history_snapshots(repo_root: Path) -> list[TemplateSnapshot]:
    log_output = run_git(
        [
            "log",
            "--follow",
            "--format=%H%x09%cs%x09%s",
            "--",
            str(TEMPLATE_PATH),
        ],
        repo_root,
    )
    snapshots: dict[tuple[str, str], TemplateSnapshot] = {}
    for line in log_output.splitlines():
        if not line.strip():
            continue
        commit, date, subject = line.split("\t", 2)
        try:
            text = run_git(["show", f"{commit}:{TEMPLATE_PATH}"], repo_root)
        except subprocess.CalledProcessError:
            continue
        version = parse_template_version(text)
        key = (version, commit[:12])
        snapshots[key] = TemplateSnapshot(
            version=version,
            source_commit=commit,
            introduced_at=date,
            subject=subject,
            text=text,
        )

    current_text = (repo_root / TEMPLATE_PATH).read_text(encoding="utf-8")
    current_commit = run_git(["rev-parse", "HEAD"], repo_root).strip()
    snapshots[(parse_template_version(current_text), "working-tree")] = TemplateSnapshot(
        version=parse_template_version(current_text),
        source_commit=current_commit,
        introduced_at=datetime.now(UTC).date().isoformat(),
        subject="working tree current template",
        text=current_text,
    )
    return sorted(
        snapshots.values(),
        key=lambda snapshot: (snapshot.introduced_at, snapshot.version, snapshot.source_commit),
    )


def archive_name(snapshot: TemplateSnapshot) -> str:
    safe_version = re.sub(r"[^A-Za-z0-9_.-]+", "-", snapshot.version)
    return f"skill-template-{safe_version}-{snapshot.source_commit[:12]}.md"


def write_template_archive(
    snapshots: list[TemplateSnapshot], archive_dir: Path, repo_root: Path
) -> dict[str, str]:
    archive_dir.mkdir(parents=True, exist_ok=True)
    paths: dict[str, str] = {}
    for snapshot in snapshots:
        output_path = archive_dir / archive_name(snapshot)
        header = (
            "<!-- Generated by skills/skill-maintenance/scripts/"
            "generate_template_intelligence.py. Do not edit by hand. -->\n\n"
        )
        output_path.write_text(header + snapshot.text, encoding="utf-8")
        paths[snapshot.source_commit] = str(output_path.relative_to(repo_root))
    return paths


def summarize_epochs(
    snapshots: list[TemplateSnapshot], archive_paths: dict[str, str]
) -> list[dict[str, Any]]:
    epochs: list[dict[str, Any]] = []
    previous_text: str | None = None
    for snapshot in snapshots:
        sections = section_names(snapshot.text)
        changed_sections = changed_section_names(previous_text, snapshot.text)
        epochs.append(
            {
                "version": snapshot.version,
                "source_commit": snapshot.source_commit[:12],
                "introduced_at": snapshot.introduced_at,
                "summary": snapshot.subject,
                "section_count": len(sections),
                "sections": sections,
                "changed_sections": changed_sections,
                "snapshot_path": archive_paths.get(snapshot.source_commit, ""),
            }
        )
        previous_text = snapshot.text
    return epochs


def summarize_template_versions(
    snapshots: list[TemplateSnapshot], archive_paths: dict[str, str]
) -> list[dict[str, Any]]:
    versions: dict[str, list[TemplateSnapshot]] = {}
    for snapshot in snapshots:
        versions.setdefault(snapshot.version, []).append(snapshot)

    summaries: list[dict[str, Any]] = []
    for version, version_snapshots in sorted(versions.items()):
        ordered = sorted(
            version_snapshots,
            key=lambda snapshot: (snapshot.introduced_at, snapshot.source_commit),
        )
        first = ordered[0]
        latest = ordered[-1]
        summaries.append(
            {
                "version": version,
                "introduced_at": first.introduced_at,
                "latest_at": latest.introduced_at,
                "source_commit": first.source_commit[:12],
                "latest_commit": latest.source_commit[:12],
                "release_count": len(ordered),
                "summary": first.subject,
                "latest_summary": latest.subject,
                "sections": section_names(latest.text),
                "snapshot_path": archive_paths.get(latest.source_commit, ""),
                "template_metadata": template_metadata_summary(latest.text),
                "snapshots": [
                    {
                        "source_commit": snapshot.source_commit[:12],
                        "introduced_at": snapshot.introduced_at,
                        "summary": snapshot.subject,
                        "snapshot_path": archive_paths.get(snapshot.source_commit, ""),
                    }
                    for snapshot in ordered
                ],
            }
        )
    return summaries


def feature_summaries(feature_rows: list[dict[str, Any]]) -> list[dict[str, Any]]:
    summaries = []
    for row in feature_rows:
        if row.get("category") != "skills":
            continue
        summaries.append(
            {
                "id": row.get("id", ""),
                "name": row.get("name", ""),
                "status": row.get("status", ""),
                "surfaces": row.get("surfaces", []),
                "evidence_refs": row.get("evidence_refs", []),
                "metrics": row.get("metrics", []),
                "known_limits": row.get("known_limits", ""),
                "last_verified": row.get("last_verified", ""),
            }
        )
    return sorted(summaries, key=lambda row: row["id"])


def rollout_rows(skill_rows: list[dict[str, Any]], current_version: str) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for row in skill_rows:
        version = str(row.get("skill_template_version") or "missing")
        source = str(row.get("source") or "local")
        if source == "external":
            status = "external"
        elif version == "missing":
            status = "missing"
        elif version == current_version:
            status = "current"
        else:
            status = "stale"
        rows.append(
            {
                "skill_id": row.get("name", ""),
                "path": row.get("path", ""),
                "source": source,
                "tier": row.get("tier"),
                "template_version": version,
                "eval": row.get("eval", ""),
                "qa_checklist": row.get("qa_checklist", ""),
                "skill_ui": row.get("skill_ui", ""),
                "has_checklist": bool(row.get("has_checklist")),
                "status": status,
            }
        )
    return sorted(rows, key=lambda row: (str(row["status"]), str(row["skill_id"])))


def template_uses_from_row(row: dict[str, Any]) -> dict[str, str]:
    return normalize_template_uses(row, row.get("path", "<row>"))


def skill_template_consumers(skill_rows: list[dict[str, Any]]) -> list[dict[str, Any]]:
    consumers: list[dict[str, Any]] = []
    for row in skill_rows:
        if row.get("source") == "external":
            continue
        template_uses = template_uses_from_row(row)
        consumers.append(
            {
                "consumer_id": row.get("name", ""),
                "consumer_scope": "skill",
                "path": row.get("path", ""),
                "template_uses": template_uses,
                "surfaces": {
                    "skill": bool(template_uses.get("skill-template")),
                    "eval": bool(row.get("eval")),
                    "qa_checklist": bool(row.get("qa_checklist")),
                },
            }
        )
    return consumers


def load_json_template_uses(path: Path, display_path: str) -> dict[str, str]:
    if not path.exists():
        return {}
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except json.JSONDecodeError:
        return {}
    if not isinstance(data, dict):
        return {}
    return normalize_template_uses(data, display_path, include_legacy=False)


def project_template_consumers(repo_root: Path) -> list[dict[str, Any]]:
    consumers: list[dict[str, Any]] = []
    for project_root_ref in PROJECT_ROOTS:
        project_root = (repo_root / project_root_ref).resolve()
        manifest_path = project_root / "farplane" / "manifest.json"
        if not manifest_path.exists():
            continue
        try:
            display_path = manifest_path.relative_to(repo_root).as_posix()
        except ValueError:
            display_path = project_root_ref.joinpath("farplane/manifest.json").as_posix()
        project_name = project_root.name
        template_uses = load_json_template_uses(manifest_path, display_path)
        consumers.append(
            {
                "consumer_id": project_name,
                "consumer_scope": "project",
                "path": display_path,
                "template_uses": template_uses,
                "surfaces": {"project": True},
            }
        )
    return consumers


def template_applies_to_consumer(template_row: dict[str, Any], consumer: dict[str, Any]) -> bool:
    scope = template_row.get("consumer_scope")
    if scope in {"skill", "project"} and consumer.get("consumer_scope") != scope:
        return False
    template_id = str(template_row.get("template_id") or "")
    surfaces = consumer.get("surfaces", {})
    if template_id == "skill-eval-task":
        return bool(isinstance(surfaces, dict) and surfaces.get("eval"))
    if template_id == "skill-qa-checklist":
        return bool(isinstance(surfaces, dict) and surfaces.get("qa_checklist"))
    if template_id == "skill-template":
        return bool(isinstance(surfaces, dict) and surfaces.get("skill"))
    return True


def template_rollout_rows(
    template_rows: list[dict[str, Any]], consumers: list[dict[str, Any]]
) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for template in template_rows:
        if template.get("consumer_scope") not in {"skill", "project", "mixed"}:
            continue
        template_id = str(template.get("template_id") or "")
        current_version = str(template.get("template_version") or "")
        if not template_id or not current_version:
            continue
        for consumer in consumers:
            if not template_applies_to_consumer(template, consumer):
                continue
            template_uses = consumer.get("template_uses", {})
            used_version = template_uses.get(template_id) if isinstance(template_uses, dict) else None
            if used_version == current_version:
                status = "current"
            elif used_version:
                status = "stale"
            else:
                status = "missing"
            rows.append(
                {
                    "template_id": template_id,
                    "current_version": current_version,
                    "feature_refs": template.get("feature_refs", []),
                    "target_basis": template_target_basis(template_id),
                    "consumer_id": consumer.get("consumer_id", ""),
                    "consumer_scope": consumer.get("consumer_scope", ""),
                    "path": consumer.get("path", ""),
                    "used_version": used_version or "",
                    "status": status,
                }
            )
    return sorted(
        rows,
        key=lambda row: (
            str(row["template_id"]),
            str(row["status"]),
            str(row["consumer_scope"]),
            str(row["consumer_id"]),
        ),
    )


def template_rollout_summary(rows: list[dict[str, Any]]) -> dict[str, Any]:
    summary: dict[str, Any] = {}
    for row in rows:
        template_id = str(row["template_id"])
        current = summary.setdefault(
            template_id,
            {
                "current_version": row["current_version"],
                "feature_refs": row["feature_refs"],
                "target_basis": row["target_basis"],
                "total_consumers": 0,
                "by_status": {},
                "by_scope": {},
            },
        )
        current["total_consumers"] += 1
        current["by_status"][row["status"]] = current["by_status"].get(row["status"], 0) + 1
        scope = row["consumer_scope"]
        current["by_scope"][scope] = current["by_scope"].get(scope, 0) + 1
    return summary


def rollout_summary(rows: list[dict[str, Any]]) -> dict[str, Any]:
    by_status = Counter(str(row["status"]) for row in rows)
    by_version = Counter(str(row["template_version"]) for row in rows)
    by_source = Counter(str(row["source"]) for row in rows)
    return {
        "total_skills": len(rows),
        "by_status": dict(sorted(by_status.items())),
        "by_template_version": dict(sorted(by_version.items())),
        "by_source": dict(sorted(by_source.items())),
    }


COMMON_EVALS = [
    {
        "id": "routing_clarity",
        "behavior": "routing",
        "title": "Routing clarity",
        "expected_signals": [
            "description uses verb/input/output/call-condition guidance",
            "trigger catalogs stay out of frontmatter",
        ],
        "required_patterns": [r"Verb input/context into output/artifact", r"<=220 chars"],
    },
    {
        "id": "todo_executability",
        "behavior": "todo_executability",
        "title": "Todo executability",
        "expected_signals": [
            "top-level todos use visible numbered checkbox actions",
            "policy prose is not treated as a top-level todo",
        ],
        "required_patterns": [r"- \[ \] 1\.", r"observable result|named proof command|evidence surface"],
    },
    {
        "id": "phase_boundary",
        "behavior": "phase_boundary",
        "title": "Phase boundary",
        "expected_signals": [
            "phase-like skills are externalized only when their artifact is needed",
            "same-scope recursion is forbidden",
        ],
        "required_patterns": [r"## Phase Boundary", r"Externalized phase calls must shrink"],
    },
    {
        "id": "proof_contract",
        "behavior": "proof_contract",
        "title": "Proof contract",
        "expected_signals": [
            "the finish gate names proof, blockers, or evidence",
            "output contract is explicit",
        ],
        "required_patterns": [r"Verify with the named proof command", r"## Output"],
    },
    {
        "id": "eval_qa_sync",
        "behavior": "eval_qa_sync",
        "title": "Eval / QA sync",
        "expected_signals": [
            "eval_task.json is a first-class special file",
            "qa_checklist.md is a repeatable runtime guardrail only when warranted",
        ],
        "required_patterns": [r"eval_task\.json", r"qa_checklist\.md"],
    },
]


def evaluate_template(snapshot: TemplateSnapshot) -> list[dict[str, Any]]:
    results: list[dict[str, Any]] = []
    for definition in COMMON_EVALS:
        missing = [
            pattern
            for pattern in definition["required_patterns"]
            if not re.search(pattern, snapshot.text, re.IGNORECASE)
        ]
        results.append(
            {
                "template_version": snapshot.version,
                "source_commit": snapshot.source_commit[:12],
                "eval_id": definition["id"],
                "behavior": definition["behavior"],
                "title": definition["title"],
                "verdict": "pass" if not missing else "fail",
                "missing_signals": missing,
                "expected_signals": definition["expected_signals"],
                "caveat": "Heuristic template-structure signal; not a universal skill quality score.",
            }
        )
    return results


def build_payload(repo_root: Path, archive_dir: Path, write_archive: bool) -> dict[str, Any]:
    snapshots = discover_history_snapshots(repo_root)
    archive_paths = (
        write_template_archive(snapshots, archive_dir, repo_root)
        if write_archive
        else {snapshot.source_commit: str((archive_dir / archive_name(snapshot)).relative_to(repo_root)) for snapshot in snapshots}
    )
    skill_rows = load_jsonl(repo_root / "docs/skills/registry.jsonl")
    feature_rows = load_jsonl(repo_root / "docs/features/registry.jsonl")
    template_rows = load_jsonl(repo_root / "docs/templates/registry.jsonl")
    rollout = rollout_rows(skill_rows, CURRENT_TEMPLATE_VERSION)
    template_consumers = [
        *skill_template_consumers(skill_rows),
        *project_template_consumers(repo_root),
    ]
    template_rollout = template_rollout_rows(template_rows, template_consumers)
    eval_results: list[dict[str, Any]] = []
    for snapshot in snapshots:
        eval_results.extend(evaluate_template(snapshot))

    return {
        "schema_version": "1.0.0",
        "generated_at": datetime.now(UTC).isoformat(timespec="seconds"),
        "current_template_version": CURRENT_TEMPLATE_VERSION,
        "source": {
            "repo": str(repo_root),
            "template_path": str(TEMPLATE_PATH),
            "skill_registry_path": "docs/skills/registry.jsonl",
            "feature_registry_path": "docs/features/registry.jsonl",
        },
        "caveats": [
            "Template evals are hidden research signals until real eval-run artifacts can be joined to template release windows.",
            "Git mining is a recovery path; future template changes should archive snapshots at change time.",
            "Skill-applicable features remain owned by spec feature_records_json metadata; docs/features/registry.jsonl is generated output.",
            "Template-level features are declared by the versioned skill template; skill rows expose local eval, QA checklist, and UI surfaces.",
        ],
        "epochs": summarize_epochs(snapshots, archive_paths),
        "template_versions": summarize_template_versions(snapshots, archive_paths),
        "features": feature_summaries(feature_rows),
        "rollout_summary": rollout_summary(rollout),
        "rollout": rollout,
        "template_consumers": template_consumers,
        "template_rollout_summary": template_rollout_summary(template_rollout),
        "template_rollout": template_rollout,
        "eval_definitions": [
            {
                "id": definition["id"],
                "behavior": definition["behavior"],
                "title": definition["title"],
                "expected_signals": definition["expected_signals"],
            }
            for definition in COMMON_EVALS
        ],
        "evals": eval_results,
    }


def write_json(path: Path, payload: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def write_js(path: Path, payload: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(
        "window.SKILL_TEMPLATE_INTELLIGENCE = "
        + json.dumps(payload, indent=2, sort_keys=True)
        + ";\n",
        encoding="utf-8",
    )


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--out", default=str(DEFAULT_OUT))
    parser.add_argument("--js-out", default=str(DEFAULT_JS_OUT))
    parser.add_argument("--archive-dir", default=str(DEFAULT_ARCHIVE_DIR))
    parser.add_argument("--no-archive", action="store_true")
    args = parser.parse_args()

    payload = build_payload(REPO_ROOT, REPO_ROOT / args.archive_dir, not args.no_archive)
    write_json(REPO_ROOT / args.out, payload)
    if args.js_out:
        write_js(REPO_ROOT / args.js_out, payload)
    print(
        "wrote "
        f"{args.out} ({len(payload['epochs'])} epochs, "
        f"{len(payload['rollout'])} rollout rows, "
        f"{len(payload['evals'])} eval results)"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
