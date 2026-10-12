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
    load_skill_specialists,
    validate_specialist_membership,
    load_skill_departments,
)
from bin.core.skill_contract import parse_markdown_frontmatter_document

# Skill heat reads the bunker Convex rows the skill-invocation hook and the user-turn hook post:
# `skill_invoked` (a skill actually loaded) and `skill_requested` (a prompt named it), never mentions as use.
SKILL_EVENT_HOOK = "skill-invocation-listener"
SKILL_HEAT_SOURCE = f"convex:modules/hookTelemetry/queries:listHookTelemetryEvents(hookName={SKILL_EVENT_HOOK})"
SKILL_HEAT_ALL_DAYS = 90  # the deployment's longest hook-row read window
SKILL_HEAT_ROW_LIMIT = 5000
DEFAULT_SKILL_HEAT_WINDOW_DAYS = 30
DEFAULT_SKILL_HEAT_RECENT_DAYS = 7
DEFAULT_SKILL_HEAT_TOP_N = 25


def configured_positive_int(env_name: str, default: int) -> int:
    raw = os.environ.get(env_name, "").strip()
    if not raw:
        return default
    try:
        value = int(raw)
    except ValueError:
        return default
    return value if value > 0 else default


def skill_heat_config_from_env() -> dict[str, Any]:
    window_days = min(
        configured_positive_int("FARPLANE_SKILL_HEAT_WINDOW_DAYS", DEFAULT_SKILL_HEAT_WINDOW_DAYS), SKILL_HEAT_ALL_DAYS
    )
    recent_days = configured_positive_int("FARPLANE_SKILL_HEAT_RECENT_DAYS", DEFAULT_SKILL_HEAT_RECENT_DAYS)
    if recent_days > window_days:
        recent_days = window_days
    return {
        "window_days": window_days,
        "recent_days": recent_days,
        "default_top_n": configured_positive_int("FARPLANE_SKILL_HEAT_TOP_N", DEFAULT_SKILL_HEAT_TOP_N),
        "all_days": SKILL_HEAT_ALL_DAYS,
        "source": SKILL_HEAT_SOURCE,
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


def empty_skill_heat(window_days: int, recent_days: int) -> dict[str, Any]:
    return {
        "invocation_count_all": 0,
        "invocation_count_recent": 0,
        "invocation_count_window": 0,
        "requested_count_recent": 0,
        "requested_count_window": 0,
        "distinct_threads_window": 0,
        "last_invoked_at": "",
        "window_days": window_days,
        "recent_days": recent_days,
        "all_days": SKILL_HEAT_ALL_DAYS,
    }


def skill_heat_from_rows(
    rows: list[dict[str, Any]],
    skill_names: set[str],
    now: datetime | None = None,
    config: dict[str, Any] | None = None,
) -> dict[str, dict[str, Any]]:
    """Heat per skill from `skill-invocation-listener` hook rows; only `skill_invoked` is use."""
    heat_config = config or skill_heat_config_from_env()
    window_days = int(heat_config.get("window_days") or DEFAULT_SKILL_HEAT_WINDOW_DAYS)
    recent_days = int(heat_config.get("recent_days") or DEFAULT_SKILL_HEAT_RECENT_DAYS)
    heat = {name: empty_skill_heat(window_days, recent_days) for name in skill_names}
    clock = now.astimezone(UTC) if now else datetime.now(UTC)
    windows = {
        "all": clock - timedelta(days=SKILL_HEAT_ALL_DAYS),
        "window": clock - timedelta(days=window_days),
        "recent": clock - timedelta(days=recent_days),
    }
    seen: set[tuple[str, ...]] = set()
    threads: dict[str, set[str]] = defaultdict(set)
    for row in rows:
        payload = row.get("payload") if isinstance(row.get("payload"), dict) else {}
        kind = str(payload.get("eventType") or "")
        skill = str(payload.get("skillId") or "")
        # A plugin's same-named skill (e.g. `anthropic-skills:skill-creator`) is not the Farplane skill.
        if skill not in skill_names or str(payload.get("plugin") or "farplane") != "farplane":
            continue
        if kind not in {"skill_invoked", "skill_requested"} or not isinstance(row.get("eventAt"), (int, float)):
            continue
        at = datetime.fromtimestamp(float(row["eventAt"]) / 1000, tz=UTC)
        session = str(row.get("sessionId") or "")
        anchor = str(payload.get("turnId") or row.get("eventKey") or row.get("_id") or row["eventAt"])
        if (kind, skill, session, anchor) in seen:
            continue
        seen.add((kind, skill, session, anchor))
        item = heat[skill]
        if kind == "skill_requested":
            item["requested_count_window"] += int(at >= windows["window"])
            item["requested_count_recent"] += int(at >= windows["recent"])
            continue
        item["invocation_count_all"] += int(at >= windows["all"])
        item["invocation_count_window"] += int(at >= windows["window"])
        item["invocation_count_recent"] += int(at >= windows["recent"])
        if at >= windows["window"] and session:
            threads[skill].add(session)
        stamp = at.isoformat().replace("+00:00", "Z")
        if stamp > item["last_invoked_at"]:
            item["last_invoked_at"] = stamp
    for skill, sessions in threads.items():
        heat[skill]["distinct_threads_window"] = len(sessions)
    return heat


def fetch_skill_event_rows() -> tuple[list[dict[str, Any]], str]:
    """The last 90 days of skill rows from Convex, and a gap note when they are missing or capped."""
    from bin.core.farplane_convex import ConvexUnavailable, convex_query

    try:
        rows = convex_query(
            "modules/hookTelemetry/queries:listHookTelemetryEvents",
            {"hookName": SKILL_EVENT_HOOK, "rangeDays": SKILL_HEAT_ALL_DAYS, "limit": SKILL_HEAT_ROW_LIMIT},
        )
    except ConvexUnavailable as exc:
        return [], f"telemetry_unavailable: {exc}"
    rows = [row for row in rows or [] if isinstance(row, dict)]
    gap = f"telemetry_truncated: capped at {SKILL_HEAT_ROW_LIMIT} rows" if len(rows) >= SKILL_HEAT_ROW_LIMIT else ""
    return rows, gap


def load_skill_heat(
    skill_names: set[str],
    now: datetime | None = None,
    config: dict[str, Any] | None = None,
) -> dict[str, dict[str, Any]]:
    rows, gap = fetch_skill_event_rows()
    if gap:
        print(f"farplane: skill heat {gap}", file=sys.stderr)
    return skill_heat_from_rows(rows, skill_names, now=now, config=config)


def direct_heat_signal(heat: dict[str, Any]) -> dict[str, Any]:
    return {
        "invocation_count_window": int(heat.get("invocation_count_window") or 0),
        "invocation_count_recent": int(heat.get("invocation_count_recent") or 0),
        "distinct_threads_window": int(heat.get("distinct_threads_window") or 0),
        "requested_count_window": int(heat.get("requested_count_window") or 0),
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
        "specialist": row.get("specialist", ""),
        "source": row.get("source", "local"),
        "department": row.get("department", ""),
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
        bool(uniqueness.get("specialist"))
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
                "specialist": row.get("specialist", ""),
                "source": row.get("source", "local"),
                "department": row.get("department", ""),
                "capability": row.get("capability", {}),
                "todo_skill_refs": row.get("todo_skill_refs", []),
                "methods": row.get("methods", []),
                "has_checklist": bool(row.get("has_checklist")),
                "eval": row.get("eval", ""),
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

    nodes.sort(key=lambda node: (str(node.get("department") or "~"), node["label"]))
    edges.sort(key=lambda edge: (edge["source"], edge["target"], edge["type"], edge["label"]))

    counts = {
        "nodes": len(nodes),
        "edges": len(edges),
        "departments": {},
        "sources": {},
        "capabilities": {},
        "edge_types": edge_counts(edges),
        "skill_heat_config": skill_heat_config or skill_heat_config_from_env(),
    }
    for node in nodes:
        department = str(node.get("department") or "none")
        counts["departments"][department] = counts["departments"].get(department, 0) + 1
        source = str(node.get("source", "unknown"))
        counts["sources"][source] = counts["sources"].get(source, 0) + 1
        capability = node.get("capability")
        kind = capability.get("kind", "core") if isinstance(capability, dict) else "core"
        counts["capabilities"][kind] = counts["capabilities"].get(kind, 0) + 1

    return GraphBundle(nodes=nodes, edges=edges, generated_at=utc_timestamp(), counts=counts).as_dict()


def build_capability_graph(
    rows: list[dict[str, Any]],
    department_labels: dict[str, str] | None = None,
    specialists: dict[str, dict[str, str]] | None = None,
) -> dict[str, Any]:
    """Project departments, their specialist desks, and declared artifact flow.

    A specialist is one desk (workstation) that lists its member skill variants
    in config/skill-workflows.toml. Member skills with an integration capability are
    drawn as system facilities beside their desk. Unassigned skills are omitted.
    """
    departments = department_labels or {}
    if not departments:
        raise ValueError("capability projection requires declared departments")
    if not specialists:
        raise ValueError("capability projection requires declared specialists")
    errors = validate_specialist_membership(rows, specialists)
    if errors:
        raise ValueError("capability projection " + "; ".join(errors))

    rows_by_name = {str(row.get("name") or ""): row for row in rows}
    members: dict[str, list[dict[str, Any]]] = {
        specialist_id: [rows_by_name[skill] for skill in sorted(entry["skills"])]
        for specialist_id, entry in specialists.items()
    }

    nodes: list[dict[str, Any]] = []
    edges: list[dict[str, Any]] = []
    node_for_skill: dict[str, str] = {}
    desk_counts: dict[str, int] = defaultdict(int)
    facility_counts: dict[str, int] = defaultdict(int)

    for specialist_id, entry in specialists.items():
        department_id = entry["department"]
        member_rows = members[specialist_id]
        desk_id = f"specialist:{specialist_id}"
        produces = sorted({
            artifact
            for row in member_rows
            if isinstance(row.get("capability"), dict) and row["capability"].get("kind") == "artifact"
            for artifact in row["capability"].get("produces", [])
        })
        consumes = sorted({
            artifact
            for row in member_rows
            if isinstance(row.get("capability"), dict) and row["capability"].get("kind") == "artifact"
            for artifact in row["capability"].get("consumes", [])
        })
        nodes.append(
            GraphNode(
                id=desk_id,
                label=entry["label"],
                kind="workstation",
                tags=("workstation", "specialist", department_id),
                attributes={
                    "specialist_id": specialist_id,
                    "skill_id": entry["primary"],
                    "skill_ids": [str(row["name"]) for row in member_rows],
                    "department": department_id,
                    "deliverable": entry["deliverable"],
                    "description": next(
                        (row.get("description", "") for row in member_rows if row["name"] == entry["primary"]), ""
                    ),
                    "role": "workstation",
                    "capability": {"consumes": consumes, "produces": produces},
                },
            ).as_dict()
        )
        desk_counts[department_id] += 1
        edges.append(
            GraphEdge(
                source=f"department:{department_id}",
                target=desk_id,
                type="member-of",
                label="workstation",
                confidence="explicit",
            ).as_dict()
        )
        for row in member_rows:
            skill_id = str(row["name"])
            capability = row.get("capability") if isinstance(row.get("capability"), dict) else {}
            if capability.get("kind") == "integration":
                facility_id = f"skill:{skill_id}"
                nodes.append(
                    GraphNode(
                        id=facility_id,
                        label=skill_id.replace("-", " ").title(),
                        kind="facility",
                        tags=("facility", "integration", department_id),
                        attributes={
                            "skill_id": skill_id,
                            "specialist_id": specialist_id,
                            "department": department_id,
                            "description": row.get("description", ""),
                            "role": "facility",
                            "capability": {"consumes": list(capability.get("consumes", []))},
                        },
                    ).as_dict()
                )
                facility_counts[department_id] += 1
                edges.append(
                    GraphEdge(
                        source=desk_id,
                        target=facility_id,
                        type="member-of",
                        label="facility",
                        confidence="explicit",
                    ).as_dict()
                )
                node_for_skill[skill_id] = facility_id
            else:
                node_for_skill[skill_id] = desk_id

    for department_id, label in departments.items():
        nodes.append(
            GraphNode(
                id=f"department:{department_id}",
                label=label,
                kind="department",
                tags=("department", department_id),
                attributes={
                    "department_id": department_id,
                    "workstation_count": desk_counts[department_id],
                    "facility_count": facility_counts[department_id],
                },
            ).as_dict()
        )

    produced_by: dict[str, set[str]] = defaultdict(set)
    consumed_by: dict[str, set[str]] = defaultdict(set)
    for row in rows:
        skill_id = str(row.get("name") or "")
        node_id = node_for_skill.get(skill_id)
        capability = row.get("capability")
        if not node_id or not isinstance(capability, dict):
            continue
        for artifact in capability.get("produces", []) or []:
            produced_by[artifact].add(node_id)
        for artifact in capability.get("consumes", []) or []:
            consumed_by[artifact].add(node_id)
    flow_keys: set[tuple[str, str, str]] = set()
    for artifact, sources in produced_by.items():
        for source in sources:
            for target in consumed_by.get(artifact, set()):
                if source != target:
                    flow_keys.add((source, target, artifact))
    for source, target, artifact in sorted(flow_keys):
        edges.append(
            GraphEdge(
                source=source,
                target=target,
                type="artifact-flow",
                label=artifact,
                confidence="declared",
            ).as_dict()
        )

    nodes.sort(key=lambda node: (str(node.get("department") or node.get("department_id") or ""), node["id"]))
    edges.sort(key=lambda edge: (edge["source"], edge["target"], edge["type"]))
    workstations = sum(desk_counts.values())
    facilities = sum(facility_counts.values())
    return GraphBundle(
        nodes=nodes,
        edges=edges,
        schema_version="3.0.0",
        generated_at=utc_timestamp(),
        counts={
            "nodes": len(nodes),
            "edges": len(edges),
            "node_kinds": {
                "department": len(departments),
                "facility": facilities,
                "workstation": workstations,
            },
            "roles": {"facility": facilities, "workstation": workstations},
            "assigned_skills": len(node_for_skill),
        },
        extras={
            "source": {
                "contract": "config/skill-workflows.toml specialists (label, department, deliverable, primary, skills) + skills/*/SKILL.md frontmatter department + capability",
                "link_semantics": "department membership of specialist desks, integration facilities beside their desk, and directed artifact-flow edges where a member skill produces an artifact ID another member consumes; flow is a declared handoff contract, not an automatic call or publish action",
                "omits": "skills at no specialist desk, methods, Markdown references, Todo references, runtime files, task state, and delivery state",
            }
        },
    ).as_dict()


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
        frontmatter, frontmatter_raw, body = parse_markdown_frontmatter_document(
            markdown,
            path,
            required=True,
        )
        assert frontmatter is not None
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
    skill_heat = load_skill_heat({row["name"] for row in rows}, config=skill_heat_config)
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
