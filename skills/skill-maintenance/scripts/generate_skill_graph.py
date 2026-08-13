#!/usr/bin/env python3
"""Generate graph and document data for the Farplane skill registry."""

from __future__ import annotations

import argparse
import json
import os
import sys
from collections import defaultdict
from datetime import UTC, datetime, timedelta
from pathlib import Path
from typing import Any

from graph_ir import GraphBundle, GraphEdge, GraphNode, edge_counts, utc_timestamp, write_js, write_json
from graph_projection_config import get_projection_config

SCRIPT_ROOT = Path(__file__).resolve().parents[3]
if str(SCRIPT_ROOT) not in sys.path:
    sys.path.insert(0, str(SCRIPT_ROOT))

from bin.core.skill_departments import (
    load_skill_departments,
    load_skill_workflow_labels,
    load_skill_workflow_roots,
)

SKILL_HEAT_EVENT_TYPES = {
    "control_surface_detected",
    "hook_result",
    "skill_requested",
}
DEFAULT_SKILL_HEAT_WINDOW_DAYS = 30
DEFAULT_SKILL_HEAT_RECENT_DAYS = 7
DEFAULT_SKILL_HEAT_TOP_N = 25
CAPABILITY_MAP_METHOD_CLASS = "artifact"


def configured_positive_int(env_name: str, default: int) -> int:
    raw = os.environ.get(env_name, "").strip()
    if not raw:
        return default
    try:
        value = int(raw)
    except ValueError:
        return default
    return value if value > 0 else default


def configured_skill_heat_event_types() -> set[str]:
    raw = os.environ.get("FARPLANE_SKILL_HEAT_EVENT_TYPES", "").strip()
    if not raw:
        return set(SKILL_HEAT_EVENT_TYPES)
    configured = {item.strip() for item in raw.replace("\n", ",").split(",") if item.strip()}
    return configured or set(SKILL_HEAT_EVENT_TYPES)


def skill_heat_config_from_env() -> dict[str, Any]:
    window_days = configured_positive_int("FARPLANE_SKILL_HEAT_WINDOW_DAYS", DEFAULT_SKILL_HEAT_WINDOW_DAYS)
    recent_days = configured_positive_int("FARPLANE_SKILL_HEAT_RECENT_DAYS", DEFAULT_SKILL_HEAT_RECENT_DAYS)
    if recent_days > window_days:
        recent_days = window_days
    return {
        "window_days": window_days,
        "recent_days": recent_days,
        "default_top_n": configured_positive_int("FARPLANE_SKILL_HEAT_TOP_N", DEFAULT_SKILL_HEAT_TOP_N),
        "event_types": sorted(configured_skill_heat_event_types()),
    }


def load_registry(path: Path) -> list[dict[str, Any]]:
    return [json.loads(line) for line in path.read_text().splitlines() if line.strip()]


def find_repo_root(start: Path) -> Path:
    for candidate in [start, *start.parents]:
        if (candidate / "docs" / "skills" / "registry.jsonl").exists() and (candidate / "skills").exists():
            return candidate
    return Path.cwd()


def skill_ref_name(ref: str) -> str:
    base = ref.split("#", 1)[0]
    return base.split(":", 1)[0]


def parse_event_timestamp(value: object) -> datetime | None:
    if not isinstance(value, str) or not value.strip():
        return None
    try:
        parsed = datetime.fromisoformat(value.strip().replace("Z", "+00:00"))
    except ValueError:
        return None
    if parsed.tzinfo is None:
        return parsed.replace(tzinfo=UTC)
    return parsed.astimezone(UTC)


def event_invocation_key(event: dict[str, Any]) -> tuple[str, ...]:
    skill_name = str(event.get("skill_name") or "")
    session_id = str(event.get("session_id") or "")
    turn_id = str(event.get("turn_id") or "")
    ticket_id = str(event.get("ticket_id") or "")
    event_id = str(event.get("event_id") or "")
    anchor = turn_id or ticket_id or event_id
    return (skill_name, session_id, anchor)


def load_skill_heat(
    repo_root: Path,
    skill_names: set[str],
    now: datetime | None = None,
    config: dict[str, Any] | None = None,
) -> dict[str, dict[str, Any]]:
    event_dir = repo_root / ".farplane" / "events"
    heat_config = config or skill_heat_config_from_env()
    window_days = int(heat_config.get("window_days") or DEFAULT_SKILL_HEAT_WINDOW_DAYS)
    recent_days = int(heat_config.get("recent_days") or DEFAULT_SKILL_HEAT_RECENT_DAYS)
    counted_event_types = set(heat_config.get("event_types") or SKILL_HEAT_EVENT_TYPES)
    heat: dict[str, dict[str, Any]] = {
        name: {
            "invocation_count_all": 0,
            "invocation_count_recent": 0,
            "invocation_count_window": 0,
            "observed_event_count_all": 0,
            "distinct_threads_window": 0,
            "distinct_tickets_window": 0,
            "last_invoked_at": "",
            "window_days": window_days,
            "recent_days": recent_days,
        }
        for name in skill_names
    }
    if not event_dir.exists():
        return heat

    records: list[tuple[datetime, dict[str, Any]]] = []
    for path in sorted(event_dir.glob("*.jsonl")):
        if not path.is_file() or path.name == "failed-sync.jsonl":
            continue
        for line in path.read_text(encoding="utf-8").splitlines():
            if not line.strip():
                continue
            try:
                event = json.loads(line)
            except json.JSONDecodeError:
                continue
            if not isinstance(event, dict):
                continue
            skill_name = str(event.get("skill_name") or "")
            event_type = str(event.get("event_type") or "")
            if skill_name not in skill_names or event_type not in counted_event_types:
                continue
            timestamp = parse_event_timestamp(event.get("timestamp"))
            if timestamp is None:
                continue
            records.append((timestamp, event))

    clock = now.astimezone(UTC) if now else datetime.now(UTC)
    recent_window = clock - timedelta(days=recent_days)
    main_window = clock - timedelta(days=window_days)
    seen_all: set[tuple[str, ...]] = set()
    seen_recent: set[tuple[str, ...]] = set()
    seen_window: set[tuple[str, ...]] = set()
    threads_window: dict[str, set[str]] = defaultdict(set)
    tickets_window: dict[str, set[str]] = defaultdict(set)

    for timestamp, event in records:
        skill_name = str(event.get("skill_name") or "")
        item = heat[skill_name]
        item["observed_event_count_all"] += 1
        if not item["last_invoked_at"] or timestamp.isoformat() > str(item["last_invoked_at"]):
            item["last_invoked_at"] = timestamp.isoformat().replace("+00:00", "Z")

        key = event_invocation_key(event)
        if key not in seen_all:
            seen_all.add(key)
            item["invocation_count_all"] += 1
        if timestamp >= recent_window and key not in seen_recent:
            seen_recent.add(key)
            item["invocation_count_recent"] += 1
        if timestamp >= main_window and key not in seen_window:
            seen_window.add(key)
            item["invocation_count_window"] += 1
            session_id = str(event.get("session_id") or "")
            ticket_id = str(event.get("ticket_id") or "")
            if session_id:
                threads_window[skill_name].add(session_id)
            if ticket_id:
                tickets_window[skill_name].add(ticket_id)

    for skill_name, item in heat.items():
        item["distinct_threads_window"] = len(threads_window.get(skill_name, set()))
        item["distinct_tickets_window"] = len(tickets_window.get(skill_name, set()))
    return heat


def direct_heat_signal(heat: dict[str, Any]) -> dict[str, Any]:
    return {
        "invocation_count_window": int(heat.get("invocation_count_window") or 0),
        "invocation_count_recent": int(heat.get("invocation_count_recent") or 0),
        "distinct_threads_window": int(heat.get("distinct_threads_window") or 0),
        "distinct_tickets_window": int(heat.get("distinct_tickets_window") or 0),
        "last_invoked_at": str(heat.get("last_invoked_at") or ""),
    }


def build_composition_heat(
    edges: list[dict[str, Any]],
    skill_heat: dict[str, dict[str, Any]],
) -> dict[str, dict[str, Any]]:
    referrers_by_target: dict[str, set[str]] = defaultdict(set)
    for edge in edges:
        source = str(edge.get("source") or "")
        target = str(edge.get("target") or "")
        if source and target and source != target:
            referrers_by_target[target].add(source)

    composition: dict[str, dict[str, Any]] = {}
    for target, referrers in referrers_by_target.items():
        hot_referrers: list[dict[str, Any]] = []
        total_window_invocations = 0
        last_referenced_at = ""
        for source in sorted(referrers):
            heat = skill_heat.get(source, {})
            invocation_count = int(heat.get("invocation_count_window") or 0)
            if invocation_count <= 0:
                continue
            total_window_invocations += invocation_count
            invoked_at = str(heat.get("last_invoked_at") or "")
            if invoked_at > last_referenced_at:
                last_referenced_at = invoked_at
            hot_referrers.append(
                {
                    "skill": source,
                    "invocation_count_window": invocation_count,
                    "last_invoked_at": invoked_at,
                }
            )
        hot_referrers.sort(
            key=lambda item: (
                -int(item["invocation_count_window"]),
                str(item["skill"]),
            )
        )
        composition[target] = {
            "incoming_ref_count": len(referrers),
            "hot_referrer_count": len(hot_referrers),
            "window_referrer_invocations": total_window_invocations,
            "last_referenced_at": last_referenced_at,
            "top_referrers": hot_referrers[:5],
        }
    return composition


def maintenance_burden_signal(row: dict[str, Any]) -> dict[str, Any]:
    findings: list[str] = []
    if row.get("source", "local") == "local":
        if not row.get("eval"):
            findings.append("missing_eval")
        if not row.get("qa_checklist"):
            findings.append("missing_qa_checklist")
    if row.get("skill_template_status") == "stale":
        findings.append("stale_template")

    if len(findings) >= 2:
        status = "high"
    elif findings:
        status = "moderate"
    else:
        status = "low"
    return {
        "status": status,
        "findings": findings,
        "has_checklist": bool(row.get("has_checklist")),
        "has_eval": bool(row.get("eval")),
        "has_qa_checklist": bool(row.get("qa_checklist")),
        "template_version": str(row.get("skill_template_version") or row.get("version") or ""),
    }


def uniqueness_signal(row: dict[str, Any], composition_heat: dict[str, Any]) -> dict[str, Any]:
    methods = row.get("methods", [])
    outgoing_refs = {
        skill_ref_name(str(ref))
        for ref in [
            *row.get("skill_links", []),
            *row.get("todo_skill_refs", []),
            *row.get("common_chains", {}).get("after", []),
        ]
        if ref
    }
    return {
        "tier": row.get("tier"),
        "source": row.get("source", "local"),
        "group": row.get("group", ""),
        "method_count": len(methods) if isinstance(methods, list) else 0,
        "outgoing_ref_count": len(outgoing_refs),
        "incoming_ref_count": int(composition_heat.get("incoming_ref_count") or 0),
        "has_skill_ui": bool(row.get("skill_ui")),
    }


def maintenance_recommendation(
    direct_heat: dict[str, Any],
    composition_heat: dict[str, Any],
    maintenance_burden: dict[str, Any],
    uniqueness: dict[str, Any],
) -> str:
    direct_count = int(direct_heat.get("invocation_count_window") or 0)
    composed_count = int(composition_heat.get("window_referrer_invocations") or 0)
    incoming_refs = int(composition_heat.get("incoming_ref_count") or 0)
    burden_status = str(maintenance_burden.get("status") or "low")
    is_unique = (
        uniqueness.get("tier") == 1
        or int(uniqueness.get("method_count") or 0) > 0
        or int(uniqueness.get("outgoing_ref_count") or 0) >= 3
        or bool(uniqueness.get("has_skill_ui"))
    )

    if direct_count == 0 and composed_count == 0 and incoming_refs == 0:
        return "keep" if is_unique else "retire_review"
    if direct_count == 0 and composed_count == 0 and is_unique:
        return "keep"
    if direct_count == 0 and composed_count == 0:
        return "watch"
    if burden_status == "high" and (direct_count > 0 or composed_count > 0):
        return "refine"
    if burden_status == "moderate" and (direct_count > 0 or composed_count > 0):
        return "harden"
    if direct_count > 0 or composed_count > 0 or is_unique:
        return "keep"
    return "watch"


def build_skill_signals(
    row: dict[str, Any],
    heat: dict[str, Any],
    composition_heat: dict[str, Any],
) -> dict[str, Any]:
    direct_heat = direct_heat_signal(heat)
    maintenance_burden = maintenance_burden_signal(row)
    uniqueness = uniqueness_signal(row, composition_heat)
    return {
        "direct_heat": direct_heat,
        "composition_heat": composition_heat,
        "maintenance_burden": maintenance_burden,
        "uniqueness": uniqueness,
        "maintenance_recommendation": maintenance_recommendation(
            direct_heat,
            composition_heat,
            maintenance_burden,
            uniqueness,
        ),
    }


def build_graph(
    rows: list[dict[str, Any]],
    skill_heat: dict[str, dict[str, Any]] | None = None,
    skill_heat_config: dict[str, Any] | None = None,
) -> dict[str, Any]:
    skill_names = {row["name"] for row in rows}
    skill_heat = skill_heat or {}

    edges: list[dict[str, Any]] = []
    seen: set[tuple[str, str, str, str]] = set()

    def add_edge(
        source: str,
        target_ref: str,
        edge_type: str,
        label: str,
        metadata: dict[str, Any] | None = None,
    ) -> None:
        target = skill_ref_name(target_ref)
        if target not in skill_names or source == target:
            return
        key = (source, target, edge_type, label)
        if key in seen:
            return
        seen.add(key)
        edges.append(
            GraphEdge(
                source=source,
                target=target,
                type=edge_type,
                label=label,
                metadata={"target_ref": target_ref, **(metadata or {})},
            ).as_dict()
        )

    for row in rows:
        source = row["name"]
        for link in row.get("skill_links", []):
            label = link if "#" in link or ":" in link else "markdown-ref"
            add_edge(source, link, "markdown-ref", label)
        for target_ref in row.get("common_chains", {}).get("after", []):
            add_edge(source, target_ref, "common-chain", "common_chains.after")
        for order, target_ref in enumerate(row.get("todo_skill_refs", []), start=1):
            add_edge(
                source,
                target_ref,
                "todo-chain",
                f"todo.{order}",
                {"order": order, "chain_source": "todo_list"},
            )

    composition_heat = build_composition_heat(edges, skill_heat)
    nodes = [
        GraphNode(
            id=row["name"],
            label=row["name"],
            attributes={
                "tier": row.get("tier"),
                "source": row.get("source", "local"),
                "group": row.get("group", ""),
                "todo_skill_refs": row.get("todo_skill_refs", []),
                "methods": row.get("methods", []),
                "has_checklist": bool(row.get("has_checklist")),
                "eval": row.get("eval", ""),
                "qa_checklist": row.get("qa_checklist", ""),
                "skill_ui": row.get("skill_ui", ""),
                "path": row.get("path", ""),
                "description": row.get("description", ""),
                "heat": skill_heat.get(row["name"], {}),
                "signals": build_skill_signals(
                    row,
                    skill_heat.get(row["name"], {}),
                    composition_heat.get(
                        row["name"],
                        {
                            "incoming_ref_count": 0,
                            "hot_referrer_count": 0,
                            "window_referrer_invocations": 0,
                            "last_referenced_at": "",
                            "top_referrers": [],
                        },
                    ),
                ),
            },
        ).as_dict()
        for row in rows
    ]

    nodes.sort(key=lambda node: (int(node.get("tier") or 9), node["label"]))
    edges.sort(key=lambda edge: (edge["source"], edge["target"], edge["type"], edge["label"]))

    counts = {
        "nodes": len(nodes),
        "edges": len(edges),
        "tiers": {},
        "sources": {},
        "edge_types": edge_counts(edges),
        "skill_heat_config": skill_heat_config or skill_heat_config_from_env(),
        "skill_heat_event_types": (skill_heat_config or skill_heat_config_from_env()).get("event_types"),
    }
    for node in nodes:
        tier = str(node.get("tier", "unknown"))
        counts["tiers"][tier] = counts["tiers"].get(tier, 0) + 1
        source = str(node.get("source", "unknown"))
        counts["sources"][source] = counts["sources"].get(source, 0) + 1

    return GraphBundle(nodes=nodes, edges=edges, generated_at=utc_timestamp(), counts=counts).as_dict()


def build_capability_graph(
    rows: list[dict[str, Any]],
    department_labels: dict[str, str] | None = None,
    workflow_roots: dict[str, tuple[str, ...]] | None = None,
    workflow_labels: dict[str, str] | None = None,
) -> dict[str, Any]:
    """Project configured real workflow roots and their declared artifact methods."""
    nodes: list[dict[str, Any]] = []
    edges: list[dict[str, Any]] = []
    capability_classes: dict[str, int] = defaultdict(int)
    departments = department_labels or {}
    if not departments:
        raise ValueError("capability projection requires declared departments")
    if workflow_roots is None:
        raise ValueError("capability projection requires configured workflow roots")
    workflow_labels = workflow_labels or {}

    unknown_root_departments = sorted(set(workflow_roots).difference(departments))
    missing_root_departments = sorted(set(departments).difference(workflow_roots))
    if unknown_root_departments or missing_root_departments:
        details: list[str] = []
        if unknown_root_departments:
            details.append(f"unknown workflow-root departments: {', '.join(unknown_root_departments)}")
        if missing_root_departments:
            details.append(f"missing workflow-root departments: {', '.join(missing_root_departments)}")
        raise ValueError("capability projection " + "; ".join(details))

    rows_by_name = {str(row.get("name") or ""): row for row in rows}
    department_ids = list(departments)
    selected_rows: list[tuple[str, dict[str, Any]]] = []
    selected_names: set[str] = set()
    for department_id in department_ids:
        roots = workflow_roots[department_id]
        if not roots:
            raise ValueError(f"capability projection requires a root for {department_id}")
        for skill_id in roots:
            if skill_id in selected_names:
                raise ValueError(f"capability projection duplicate workflow root {skill_id!r}")
            row = rows_by_name.get(skill_id)
            if row is None:
                raise ValueError(f"capability projection unknown workflow root {skill_id!r}")
            if row.get("tier") != 3:
                raise ValueError(f"capability projection root {skill_id!r} must be Tier 3")
            if row.get("group") != department_id:
                raise ValueError(
                    f"capability projection root {skill_id!r} must belong to {department_id!r}"
                )
            declared_methods = [method for method in row.get("methods", []) if isinstance(method, dict)]
            if declared_methods and not any(
                method.get("class") == CAPABILITY_MAP_METHOD_CLASS for method in declared_methods
            ):
                raise ValueError(
                    f"capability projection root {skill_id!r} declares no artifact method"
                )
            selected_names.add(skill_id)
            selected_rows.append((department_id, row))

    for department_id in department_ids:
        nodes.append(
            GraphNode(
                id=f"department:{department_id}",
                label=departments.get(department_id, department_id.replace("-", " ").title()),
                kind="department",
                tags=("department", department_id),
                attributes={"department_id": department_id},
            ).as_dict()
        )

    for department_id, row in selected_rows:
        skill_id = str(row["name"])
        nodes.append(
            GraphNode(
                id=f"skill:{skill_id}",
                label=workflow_labels.get(skill_id, skill_id),
                kind="workflow",
                tags=("workflow", department_id),
                attributes={
                    "skill_id": skill_id,
                    "tier": row.get("tier"),
                    "group": department_id,
                    "description": row.get("description", ""),
                    "source": row.get("source", ""),
                },
            ).as_dict()
        )
        edges.append(
            GraphEdge(
                source=f"department:{department_id}",
                target=f"skill:{skill_id}",
                type="member-of",
                label="workflow-root",
                confidence="explicit",
            ).as_dict()
        )
        methods = [
            method
            for method in row.get("methods", [])
            if isinstance(method, dict) and method.get("class") == CAPABILITY_MAP_METHOD_CLASS
        ]

        for method in sorted(methods, key=lambda item: str(item.get("id") or "")):
            method_id = str(method["id"])
            method_class = CAPABILITY_MAP_METHOD_CLASS
            output = str(method["output"])
            capability_classes[method_class] += 1
            nodes.append(
                GraphNode(
                    id=f"method:{method_id}",
                    label=output,
                    kind=method_class,
                    tags=(method_class, str(row.get("group") or "ungrouped")),
                    attributes={
                        "method_id": method_id,
                        "parent_skill": skill_id,
                        "output": output,
                        "tier": row.get("tier"),
                        "group": department_id,
                    },
                ).as_dict()
            )
            edges.append(
                GraphEdge(
                    source=f"skill:{skill_id}",
                    target=f"method:{method_id}",
                    type="contains",
                    label=method_class,
                    confidence="explicit",
                ).as_dict()
            )

    nodes.sort(
        key=lambda node: (
            str(node.get("department_id") or node.get("group") or ""),
            str(node.get("parent_skill") or node.get("skill_id") or ""),
            node["id"],
        )
    )
    edges.sort(key=lambda edge: (edge["source"], edge["target"]))
    return GraphBundle(
        nodes=nodes,
        edges=edges,
        generated_at=utc_timestamp(),
        counts={
            "nodes": len(nodes),
            "edges": len(edges),
            "node_kinds": {
                "artifact": capability_classes[CAPABILITY_MAP_METHOD_CLASS],
                "department": len(department_ids),
                "workflow": len(selected_rows),
            },
            "capability_classes": dict(sorted(capability_classes.items())),
        },
        extras={
            "source": {
                "contract": "rules/skill-workflows.toml roots/labels + skills/*/SKILL.md frontmatter group + methods[]",
                "link_semantics": "explicit selected workflow membership and parent artifact containment only",
                "omits": "unselected skills, integration/internal methods, Todo references, inferred execution dependencies, and process order",
            }
        },
    ).as_dict()


def parse_frontmatter(markdown: str) -> tuple[dict[str, Any], str, str]:
    if not markdown.startswith("---\n"):
        return {}, "", markdown
    end = markdown.find("\n---\n", 4)
    if end == -1:
        return {}, "", markdown
    raw = markdown[4:end]
    body = markdown[end + 5 :].lstrip("\n")
    return parse_simple_yaml(raw), raw, body


def parse_scalar(value: str) -> Any:
    value = value.strip()
    if not value:
        return ""
    if value in {"true", "false"}:
        return value == "true"
    if value.startswith("[") and value.endswith("]"):
        try:
            return json.loads(value.replace("'", '"'))
        except json.JSONDecodeError:
            inner = value[1:-1].strip()
            return [part.strip().strip("\"'") for part in inner.split(",") if part.strip()]
    if value.startswith(("\"", "'")) and value.endswith(("\"", "'")):
        return value[1:-1]
    try:
        return int(value)
    except ValueError:
        return value


def parse_simple_yaml(raw: str) -> dict[str, Any]:
    parsed: dict[str, Any] = {}
    current_map: str | None = None
    current_list: str | None = None
    current_list_item: dict[str, Any] | None = None

    for line in raw.splitlines():
        if not line.strip() or line.lstrip().startswith("#"):
            continue
        indentation = len(line) - len(line.lstrip(" "))
        stripped = line.strip()
        if indentation == 2 and stripped.startswith("- ") and current_list:
            item_value = stripped[2:].strip()
            item_key, separator, raw_item_value = item_value.partition(": ")
            if not isinstance(parsed.get(current_list), list):
                parsed[current_list] = []
            if separator:
                current_list_item = {item_key.strip(): parse_scalar(raw_item_value)}
                parsed.setdefault(current_list, []).append(current_list_item)
            else:
                current_list_item = None
                parsed.setdefault(current_list, []).append(parse_scalar(item_value))
            continue
        if indentation >= 4 and current_list_item is not None and ":" in stripped:
            key, _, value = stripped.partition(":")
            if key:
                current_list_item[key.strip()] = parse_scalar(value)
            continue
        if indentation == 2 and current_map:
            current_list_item = None
            key, _, value = stripped.partition(":")
            if key and value:
                if not isinstance(parsed.get(current_map), dict):
                    parsed[current_map] = {}
                parsed.setdefault(current_map, {})[key] = parse_scalar(value)
            continue

        current_map = None
        current_list = None
        current_list_item = None
        key, _, value = line.partition(":")
        key = key.strip()
        if not key:
            continue
        if value.strip():
            parsed[key] = parse_scalar(value)
        else:
            current_map = key
            current_list = key
            parsed[key] = {}
    return parsed


def build_docs(rows: list[dict[str, Any]]) -> dict[str, Any]:
    docs: dict[str, Any] = {
        "schema_version": "1.0.0",
        "generated_at": utc_timestamp(),
        "skills": {},
    }
    for row in rows:
        path = Path(row.get("path", ""))
        if not path.exists():
            continue
        markdown = path.read_text()
        frontmatter, frontmatter_raw, body = parse_frontmatter(markdown)
        docs["skills"][row["name"]] = {
            "name": row["name"],
            "path": str(path),
            "frontmatter": frontmatter,
            "frontmatter_raw": frontmatter_raw,
            "body": body,
        }
    docs["counts"] = {"skills": len(docs["skills"])}
    return docs


def write_graph(graph: dict[str, Any], output_path: Path, js_path: Path | None) -> None:
    write_json(output_path, graph)
    if js_path is not None:
        write_js(js_path, "SKILL_GRAPH", graph)


def write_docs(docs: dict[str, Any], output_path: Path, js_path: Path | None) -> None:
    write_json(output_path, docs)
    if js_path is not None:
        write_js(js_path, "SKILL_DOCS", docs)


def main() -> int:
    config = get_projection_config("skill-registry")
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--registry", default="docs/skills/registry.jsonl")
    parser.add_argument("--out", default=config.default_out)
    parser.add_argument("--js-out", default=config.default_js_out)
    parser.add_argument("--docs-out", default=config.docs_out)
    parser.add_argument("--docs-js-out", default=config.docs_js_out)
    parser.add_argument("--projection", default="skill-registry", help="projection profile name")
    args = parser.parse_args()

    config = get_projection_config(args.projection)
    if config.output_schema != "skill_graph":
        raise SystemExit(f"{args.projection} is not a skill graph projection")

    registry_path = Path(args.registry)
    rows = load_registry(registry_path)
    repo_root = find_repo_root(registry_path.resolve())
    skill_heat_config = skill_heat_config_from_env()
    skill_heat = load_skill_heat(repo_root, {row["name"] for row in rows}, config=skill_heat_config)
    graph = build_graph(rows, skill_heat=skill_heat, skill_heat_config=skill_heat_config)
    docs = build_docs(rows)
    write_graph(graph, Path(args.out), Path(args.js_out) if args.js_out else None)
    write_docs(docs, Path(args.docs_out), Path(args.docs_js_out) if args.docs_js_out else None)
    print(
        "wrote "
        f"{args.out} ({graph['counts']['nodes']} nodes, "
        f"{graph['counts']['edges']} edges) and "
        f"{args.docs_out} ({docs['counts']['skills']} skill docs)"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
