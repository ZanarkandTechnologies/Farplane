#!/usr/bin/env python3
"""Compile filesystem-backed skill, rollout, and eval health projections."""

from __future__ import annotations

import argparse
import json
import math
import re
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from farplane_metric_schema import metric_observation, write_metric_batch
from farplane_skill_rollout import SkillRolloutError, resolve_skill_rollout_stats


SCHEMA = "farplane_harness_health"
SCHEMA_VERSION = "0.1.0"
DEFAULT_OUTPUT = Path(".farplane/state/harness-health.json")
DEFAULT_GRAPH_ROOT = Path(".farplane/generated/graphs")
EXPECTED_EVAL_COUNT = 5
METRIC_SOURCE_ID = "harness_health"
PRIORITY_SKILL_METRIC_ID = "priority_skill_health_gap_count"
SOURCE_GAP_METRIC_ID = "harness_health_source_gap_count"


class HarnessHealthError(ValueError):
    """Raised when a required health input is malformed."""


def now_utc() -> str:
    return datetime.now(timezone.utc).isoformat().replace("+00:00", "Z")


def today_utc() -> str:
    return datetime.now(timezone.utc).date().isoformat()


def load_object(path: Path) -> dict[str, Any]:
    try:
        value = json.loads(path.read_text(encoding="utf-8"))
    except FileNotFoundError as exc:
        raise HarnessHealthError(f"missing_json:{path}") from exc
    except json.JSONDecodeError as exc:
        raise HarnessHealthError(f"invalid_json:{path}:{exc}") from exc
    if not isinstance(value, dict):
        raise HarnessHealthError(f"invalid_json_shape:{path}:expected_object")
    return value


def load_optional(path: Path, gaps: list[str]) -> dict[str, Any]:
    try:
        return load_object(path)
    except HarnessHealthError as exc:
        gaps.append(str(exc))
        return {}


def numeric(value: Any) -> float:
    try:
        result = float(value)
    except (TypeError, ValueError):
        return 0
    return result if math.isfinite(result) else 0


def clamp_score(value: float) -> int:
    return max(0, min(100, round(value))) if math.isfinite(value) else 0


def normalized_signal(value: Any) -> float:
    result = numeric(value)
    if result <= 0:
        return 0
    if result <= 1:
        return result * 100
    if result <= 10:
        return result * 10
    return result


def heading_section(body: str, pattern: str) -> str:
    matcher = re.compile(pattern, re.I)
    lines = body.splitlines()
    for start, line in enumerate(lines):
        heading = re.match(r"^(#{1,4})\s+(.+)$", line)
        if not heading or not matcher.search(heading.group(2)):
            continue
        level = len(heading.group(1))
        collected: list[str] = []
        for candidate in lines[start + 1 :]:
            next_heading = re.match(r"^(#+)\s+", candidate)
            if next_heading and len(next_heading.group(1)) <= level:
                break
            collected.append(candidate)
        return "\n".join(collected).strip()
    return ""


def checklist_lines(body: str) -> str:
    return "\n".join(
        line for line in body.splitlines() if re.match(r"^\s*[-*]\s+\[[ xX]\]", line)
    ).strip()


def eval_path_for_skill(standard_root: Path, skill_path: str, eval_path: str) -> Path | None:
    if not eval_path:
        return None
    candidate = Path(eval_path)
    if candidate.is_absolute():
        return candidate
    if "/" not in eval_path or eval_path.startswith("evals/"):
        return standard_root / Path(skill_path).parent / candidate
    return standard_root / candidate


def eval_definition_count(standard_root: Path, skill_path: str, eval_path: str) -> int:
    path = eval_path_for_skill(standard_root, skill_path, eval_path)
    if path is None:
        return 0
    try:
        rows = load_object(path).get("evals")
    except HarnessHealthError:
        return 0
    return len(rows) if isinstance(rows, list) else 0


def signal(signal_id: str, label: str, score: float, detail: str) -> dict[str, Any]:
    return {"id": signal_id, "label": label, "score": clamp_score(score), "detail": detail}


def build_skill_rows(
    standard_root: Path,
    graph: dict[str, Any],
    docs: dict[str, Any],
    rollout: dict[str, Any],
) -> list[dict[str, Any]]:
    nodes = [row for row in graph.get("nodes", []) if isinstance(row, dict)]
    edges = [row for row in graph.get("edges", []) if isinstance(row, dict)]
    docs_by_id = docs.get("skills") if isinstance(docs.get("skills"), dict) else {}
    rollout_by_id = {
        str(row.get("skillId") or ""): row
        for row in rollout.get("skills", [])
        if isinstance(row, dict)
    }
    result: list[dict[str, Any]] = []

    for node in nodes:
        skill_id = str(node.get("id") or "")
        if not skill_id:
            continue
        doc = docs_by_id.get(skill_id) if isinstance(docs_by_id.get(skill_id), dict) else {}
        frontmatter = doc.get("frontmatter") if isinstance(doc.get("frontmatter"), dict) else {}
        body = str(doc.get("body") or "")
        rollout_row = rollout_by_id.get(skill_id, {})
        skill_path = str(node.get("path") or doc.get("path") or rollout_row.get("path") or "")
        eval_path = str(rollout_row.get("eval") or node.get("eval") or "")
        eval_count = eval_definition_count(standard_root, skill_path, eval_path)
        heat = node.get("heat") if isinstance(node.get("heat"), dict) else {}
        recent = numeric(heat.get("invocation_count_7d", heat.get("invocation_count_recent")))
        window = max(
            numeric(heat.get("invocation_count_30d")),
            numeric(heat.get("invocation_count_window")),
        )
        breadth = numeric(heat.get("distinct_threads_30d", heat.get("distinct_threads_window")))
        breadth += numeric(heat.get("distinct_tickets_30d", heat.get("distinct_tickets_window")))

        incoming = [edge for edge in edges if str(edge.get("target") or "") == skill_id]
        outgoing = [edge for edge in edges if str(edge.get("source") or "") == skill_id]
        referrers = {str(edge.get("source") or "") for edge in incoming}
        chains = sum(1 for edge in incoming if edge.get("type") == "common-chain")
        markdown_refs = len(incoming) - chains

        checklist = heading_section(body, r"checklist|done\s*/\s*proof") or checklist_lines(body)
        todo = heading_section(body, r"todo|task|program") or checklist_lines(body)
        references = heading_section(body, r"reference|source|link")
        if not references:
            references = "\n".join(match[1] for match in re.findall(r"\[([^\]]+)\]\(([^)]+)\)", body))
        if not references and isinstance(frontmatter.get("feature_refs"), list):
            references = "\n".join(str(ref) for ref in frontmatter["feature_refs"] if ref)
        template_status = str(rollout_row.get("status") or "unknown")

        burden = 0
        burden += 0 if checklist else 14
        burden += 0 if references else 10
        burden += 0 if todo else 10
        burden += max(0, EXPECTED_EVAL_COUNT - eval_count) * 8
        burden += 16 if template_status == "stale" else 20 if template_status == "missing" else 0
        burden += 12 if len(body) > 12_000 else 0

        methods = frontmatter.get("methods") if isinstance(frontmatter.get("methods"), list) else []
        outgoing_targets = {str(edge.get("target") or "") for edge in outgoing}
        proof_surface = eval_count > 0 or bool(checklist)
        description = str(node.get("description") or frontmatter.get("description") or "")
        generic_penalty = 12 if re.match(r"^(plan|review|execute|test|qa|research|summary|status)$", skill_id, re.I) else 0

        signals = [
            signal(
                "direct_heat",
                "Direct heat",
                max(normalized_signal(heat.get("heat_score")), recent * 18, window * 10) + breadth * 6,
                f"{int(window)} invokes / {int(breadth)} breadth",
            ),
            signal(
                "composition_heat",
                "Composition heat",
                len(referrers) * 18 + chains * 8 + markdown_refs * 4,
                f"{len(referrers)} referrers / {len(incoming)} refs",
            ),
            signal(
                "maintainability",
                "Maintainability",
                100 - burden,
                f"{max(0, EXPECTED_EVAL_COUNT - eval_count)} eval gaps / {template_status} template",
            ),
            signal(
                "uniqueness",
                "Uniqueness",
                58
                + min(18, len(methods) * 8)
                + min(12, len(outgoing_targets) * 3)
                + (10 if proof_surface else 0)
                + (8 if description else 0)
                - generic_penalty,
                f"{len(methods)} methods / {len(outgoing_targets)} owned links",
            ),
        ]
        scores = {row["id"]: row["score"] for row in signals}
        if eval_count < EXPECTED_EVAL_COUNT:
            action = "Add eval coverage before broader reuse."
        elif scores["maintainability"] < 70:
            action = "Pay down maintenance debt next."
        elif scores["direct_heat"] > 70 and scores["uniqueness"] > 80:
            action = "Protect this hot distinct workflow."
        elif scores["composition_heat"] > 70:
            action = "Keep stable; many skills compose through it."
        else:
            action = "Monitor; no urgent action."

        result.append(
            {
                "skillId": skill_id,
                "path": skill_path,
                "source": str(node.get("source") or ""),
                "tier": node.get("tier"),
                "score": clamp_score(sum(row["score"] for row in signals) / len(signals)),
                "signals": signals,
                "gaps": [
                    {"id": "eval_coverage", "status": "good" if eval_count >= EXPECTED_EVAL_COUNT else "risk" if eval_count else "missing", "value": f"{min(eval_count, EXPECTED_EVAL_COUNT)} / {EXPECTED_EVAL_COUNT}"},
                    {"id": "template_age", "status": "good" if template_status == "current" else "unknown" if template_status in {"unknown", "external"} else "risk", "value": str(rollout_row.get("templateVersion") or template_status)},
                    {"id": "owner_clarity", "status": "good" if frontmatter.get("owner") or frontmatter.get("group") else "unknown", "value": str(frontmatter.get("owner") or frontmatter.get("group") or "unknown")},
                    {"id": "first_load_size", "status": "risk" if len(body) > 12_000 else "good", "value": f"{round(len(body) / 1000)}k chars" if body else "missing"},
                ],
                "action": action,
                "evidence": {
                    "evalTaskCount": eval_count,
                    "invocationCount30d": int(window),
                    "templateStatus": template_status,
                },
            }
        )
    return sorted(result, key=lambda row: row["skillId"])


def weighted_skill_health(
    graph: dict[str, Any], docs: dict[str, Any], intelligence: dict[str, Any]
) -> dict[str, Any]:
    nodes = {str(row.get("id") or ""): row for row in graph.get("nodes", []) if isinstance(row, dict)}
    docs_by_id = docs.get("skills") if isinstance(docs.get("skills"), dict) else {}
    features = {str(row.get("id")) for row in intelligence.get("features", []) if isinstance(row, dict) and row.get("id")}
    template_refs = {
        str(row.get("version") or ""): {str(ref) for ref in ((row.get("template_metadata") or {}).get("feature_refs") or [])}
        for row in intelligence.get("template_versions", [])
        if isinstance(row, dict)
    }
    weighted_rows: list[tuple[float, float]] = []
    for rollout_row in intelligence.get("rollout", []):
        if not isinstance(rollout_row, dict) or rollout_row.get("source") == "external":
            continue
        skill_id = str(rollout_row.get("skill_id") or "")
        node = nodes.get(skill_id, {})
        heat = node.get("heat") if isinstance(node.get("heat"), dict) else {}
        doc = docs_by_id.get(skill_id) if isinstance(docs_by_id.get(skill_id), dict) else {}
        frontmatter = doc.get("frontmatter") if isinstance(doc.get("frontmatter"), dict) else {}
        refs = set(template_refs.get(str(rollout_row.get("template_version") or ""), set()))
        refs.update(str(ref) for ref in rollout_row.get("feature_refs", []) if ref)
        refs.update(str(ref) for ref in frontmatter.get("feature_refs", []) if ref)
        weight = max(
            1,
            numeric(heat.get("invocation_count_30d", heat.get("invocation_count_window"))),
            numeric(heat.get("heat_score")),
        )
        coverage = len(refs & features) / len(features) if features else 0
        weighted_rows.append((weight, coverage))
    total_weight = sum(weight for weight, _ in weighted_rows)
    score = sum(weight * coverage for weight, coverage in weighted_rows) / total_weight * 100 if total_weight else 0
    return {
        "score": clamp_score(score),
        "totalSkills": len(weighted_rows),
        "weightedSkills": sum(1 for weight, _ in weighted_rows if weight > 1),
        "featureCount": len(features),
        "method": "feature coverage weighted by local invocation or heat, minimum weight one",
    }


def task_detail(evals_root: Path, job_id: str, task_id: str, gaps: list[str]) -> dict[str, Any]:
    return load_optional(evals_root / "runs" / job_id / "tasks" / f"{task_id}.json", gaps)


def task_pass(task: dict[str, Any], detail: dict[str, Any]) -> bool | None:
    if isinstance(task.get("pass"), bool):
        return task["pass"]
    judge = detail.get("judge") if isinstance(detail.get("judge"), dict) else {}
    return judge.get("pass") if isinstance(judge.get("pass"), bool) else None


def task_verdict(task: dict[str, Any], detail: dict[str, Any]) -> str:
    judge = detail.get("judge") if isinstance(detail.get("judge"), dict) else {}
    return str(task.get("verdict") or judge.get("verdict") or "unknown")


def task_tags(task: dict[str, Any], detail: dict[str, Any]) -> list[str]:
    detail_task = detail.get("task") if isinstance(detail.get("task"), dict) else {}
    return list(dict.fromkeys([str(tag) for tag in [*task.get("tags", []), *detail_task.get("tags", [])] if tag]))


def build_eval_health(evals_root: Path, skill_ids: list[str], gaps: list[str]) -> dict[str, Any]:
    index_path = evals_root / "runs" / "index.json"
    try:
        raw_index = json.loads(index_path.read_text(encoding="utf-8"))
    except FileNotFoundError:
        gaps.append(f"missing_json:{index_path}")
        return {"status": "no_runs", "score": None, "skills": []}
    except json.JSONDecodeError as exc:
        gaps.append(f"invalid_json:{index_path}:{exc}")
        return {"status": "source_gap", "score": None, "skills": []}
    entries = raw_index if isinstance(raw_index, list) else raw_index.get("runs", []) if isinstance(raw_index, dict) else []
    entries = [row for row in entries if isinstance(row, dict) and row.get("job_id")]
    if not entries:
        return {"status": "no_runs", "score": None, "skills": []}
    entries.sort(key=lambda row: str(row.get("created_at") or row.get("completed_at") or ""), reverse=True)
    latest = entries[0]
    job_id = str(latest["job_id"])
    summary = load_optional(evals_root / "runs" / job_id / "summary.json", gaps)
    tasks = [row for row in summary.get("tasks", []) if isinstance(row, dict)]
    details = {
        str(task.get("task_id")): task_detail(evals_root, job_id, str(task.get("task_id")), gaps)
        for task in tasks
        if task.get("task_id")
    }
    task_count = int(summary.get("task_count") or len(tasks))
    passed = sum(1 for task in tasks if task_pass(task, details.get(str(task.get("task_id")), {})) is True)
    failed = sum(1 for task in tasks if task_pass(task, details.get(str(task.get("task_id")), {})) is False)
    pass_rate = numeric(summary.get("pass_rate")) if isinstance(summary.get("pass_rate"), (int, float)) else passed / task_count if task_count else 0
    failure_count = failed or max(task_count - passed, 0)
    verdict_counts = summary.get("verdict_counts") if isinstance(summary.get("verdict_counts"), dict) else {}
    hard_failures = int(verdict_counts.get("D") or 0)
    score = clamp_score(pass_rate * 100 - hard_failures * 5)
    status = "healthy" if score >= 90 else "watch" if score >= 75 else "risk" if score >= 50 else "blocked"

    skill_rows: list[dict[str, Any]] = []
    for skill_id in skill_ids:
        normalized = skill_id.lower().replace("_", "-")
        evidence: list[tuple[dict[str, Any], dict[str, Any]]] = []
        for task in tasks:
            task_id = str(task.get("task_id") or "")
            detail = details.get(task_id, {})
            detail_task = detail.get("task") if isinstance(detail.get("task"), dict) else {}
            normalized_task = str(detail_task.get("id") or task_id).lower().replace("_", "-")
            tags = [tag.lower().replace("_", "-") for tag in task_tags(task, detail)]
            if normalized in tags or normalized_task == normalized or normalized_task.startswith(f"{normalized}-"):
                evidence.append((task, detail))
        if not evidence:
            skill_rows.append({"skillId": skill_id, "score": None, "status": "no-coverage", "passedCount": 0, "taskCount": 0, "failureCount": 0})
            continue
        skill_passed = sum(1 for task, detail in evidence if task_pass(task, detail) is True)
        skill_failed = sum(1 for task, detail in evidence if task_pass(task, detail) is False)
        quality = sum({"A": 4, "B": 3, "C": 2, "D": 1}.get(task_verdict(task, detail), 0) for task, detail in evidence) / (len(evidence) * 4) * 100
        skill_score = round(min(quality, skill_passed / len(evidence) * 100))
        skill_status = "healthy" if skill_score >= 90 else "watch" if skill_score >= 75 else "risk" if skill_score >= 50 else "blocked"
        skill_rows.append({"skillId": skill_id, "score": skill_score, "status": skill_status, "passedCount": skill_passed, "taskCount": len(evidence), "failureCount": skill_failed, "evaluatedAt": str(summary.get("created_at") or latest.get("created_at") or ""), "runId": job_id})
    skill_rows.sort(key=lambda row: (row["score"] is not None, row["score"] or 0, row["skillId"]))
    return {
        "status": status,
        "score": score,
        "passRate": pass_rate,
        "taskCount": task_count,
        "failureCount": failure_count,
        "hardFailureCount": hard_failures,
        "loadedDetailCount": len(details),
        "runId": job_id,
        "evaluatedAt": str(summary.get("created_at") or latest.get("created_at") or ""),
        "skills": skill_rows,
    }


def compile_harness_health(
    *, project_root: Path, standard_root: Path, evals_root: Path | None = None
) -> dict[str, Any]:
    project_root = project_root.resolve()
    standard_root = standard_root.resolve()
    evals_root = (evals_root or project_root / ".farplane" / "evals").resolve()
    graph_root = standard_root / DEFAULT_GRAPH_ROOT
    graph_path = graph_root / "skill-graph.json"
    docs_path = graph_root / "skill-docs.json"
    intelligence_path = graph_root / "skill-template-intelligence.json"
    registry_path = standard_root / "docs" / "skills" / "registry.jsonl"
    gaps: list[str] = []
    graph = load_optional(graph_path, gaps)
    docs = load_optional(docs_path, gaps)
    intelligence = load_optional(intelligence_path, gaps)
    try:
        rollout = resolve_skill_rollout_stats(
            standard_root=standard_root,
            registry_path=registry_path,
            intelligence_path=intelligence_path,
        )
    except SkillRolloutError as exc:
        gaps.append(str(exc))
        rollout = {"schema": "farplane_skill_rollout", "schemaVersion": "0.1.0", "counts": {}, "skills": []}
    skills = build_skill_rows(standard_root, graph, docs, rollout)
    eval_health = build_eval_health(evals_root, [row["skillId"] for row in skills], gaps)
    payload = {
        "schema": SCHEMA,
        "schemaVersion": SCHEMA_VERSION,
        "generatedAt": now_utc(),
        "projectRoot": str(project_root),
        "standardRoot": str(standard_root),
        "sources": [
            {"kind": "skill_graph", "path": str(graph_path), "generatedAt": str(graph.get("generated_at") or "")},
            {"kind": "skill_docs", "path": str(docs_path), "generatedAt": str(docs.get("generated_at") or "")},
            {"kind": "skill_template_intelligence", "path": str(intelligence_path), "generatedAt": str(intelligence.get("generated_at") or "")},
            {"kind": "skill_registry", "path": str(registry_path)},
            {"kind": "eval_runs", "path": str(evals_root / "runs"), "generatedAt": str(eval_health.get("evaluatedAt") or "")},
        ],
        "sourceGaps": sorted(set(gaps)),
        "rollout": rollout,
        "skillHealth": {
            "weighted": weighted_skill_health(graph, docs, intelligence),
            "skills": skills,
        },
        "evalHealth": eval_health,
    }
    payload["metricReadings"] = build_metric_readings(payload)
    return payload


def gap_statuses(skill: dict[str, Any]) -> dict[str, str]:
    return {
        str(gap.get("id") or ""): str(gap.get("status") or "unknown")
        for gap in skill.get("gaps", [])
        if isinstance(gap, dict)
    }


def build_metric_readings(payload: dict[str, Any]) -> dict[str, dict[str, Any]]:
    skills = [
        row
        for row in payload.get("skillHealth", {}).get("skills", [])
        if isinstance(row, dict)
    ]
    local_skills = [row for row in skills if str(row.get("source") or "") != "external"]
    priority_skills = [
        row
        for row in local_skills
        if row.get("tier") == 1
        or numeric((row.get("evidence") or {}).get("invocationCount30d")) > 0
    ]
    per_skill: list[dict[str, Any]] = []
    component_counts = {"template": 0, "eval": 0}
    unhealthy_ids: list[str] = []
    healthy_ids: list[str] = []
    for skill in priority_skills:
        statuses = gap_statuses(skill)
        template_gap = statuses.get("template_age") != "good"
        eval_gap = statuses.get("eval_coverage") != "good"
        gaps = [
            name
            for name, present in (("template", template_gap), ("eval", eval_gap))
            if present
        ]
        for gap in gaps:
            component_counts[gap] += 1
        skill_id = str(skill.get("skillId") or "")
        (unhealthy_ids if gaps else healthy_ids).append(skill_id)
        per_skill.append({"skill_id": skill_id, "gaps": gaps})

    source_gaps = [str(gap) for gap in payload.get("sourceGaps", []) if gap]
    tier1_ids = sorted(str(row.get("skillId") or "") for row in local_skills if row.get("tier") == 1)
    directly_used_ids = sorted(
        str(row.get("skillId") or "")
        for row in local_skills
        if numeric((row.get("evidence") or {}).get("invocationCount30d")) > 0
    )
    priority_payload = {
        "provider": "mechanical",
        "cohort_rule": "local Tier 1 skills or local skills with observed 30-day direct usage",
        "priority_skill_count": len(priority_skills),
        "priority_skill_ids": sorted(str(row.get("skillId") or "") for row in priority_skills),
        "unhealthy_skill_ids": sorted(unhealthy_ids),
        "healthy_skill_ids": sorted(healthy_ids),
        "template_gap_count": component_counts["template"],
        "eval_gap_count": component_counts["eval"],
        "per_skill": sorted(per_skill, key=lambda row: row["skill_id"]),
        "cohort_context": {
            "local_skill_count": len(local_skills),
            "tier1_skill_count": len(tier1_ids),
            "tier1_skill_ids": tier1_ids,
            "directly_used_skill_count": len(directly_used_ids),
            "directly_used_skill_ids": directly_used_ids,
        },
        "minimum_meaningful_delta": "one priority skill becomes fully healthy without source or cohort guards regressing",
        "anti_metrics": [
            "changing tier or source only to escape the priority cohort",
            "removing eval requirements to erase a gap",
            "adding meaningless feature refs to inflate a score",
            "retiring or splitting skills only to reduce the count",
        ],
        "source_ref": ".farplane/state/harness-health.json",
    }
    source_payload = {
        "provider": "mechanical",
        "source_gaps": source_gaps,
        "source_count": len(payload.get("sources", [])),
        "source_refs": [
            str(row.get("path") or "")
            for row in payload.get("sources", [])
            if isinstance(row, dict) and row.get("path")
        ],
    }
    return {
        PRIORITY_SKILL_METRIC_ID: {
            "status": "source_gap" if source_gaps else "available",
            "value": None if source_gaps else len(unhealthy_ids),
            "payload": priority_payload,
        },
        SOURCE_GAP_METRIC_ID: {
            "status": "available",
            "value": len(source_gaps),
            "payload": source_payload,
        },
    }


def write_metric_observations(project_root: Path, date: str, payload: dict[str, Any]) -> Path:
    readings = payload["metricReadings"]
    observations = [
        metric_observation(
            metric_id,
            date,
            reading.get("value"),
            reading.get("status", "source_gap"),
            reading.get("payload"),
        )
        for metric_id, reading in readings.items()
    ]
    return write_metric_batch(
        project_root,
        METRIC_SOURCE_ID,
        date,
        observations,
        gaps=payload.get("sourceGaps", []),
        payload={"projection_ref": str(DEFAULT_OUTPUT)},
    )


def write_projection(project_root: Path, payload: dict[str, Any], output: Path | None = None) -> Path:
    path = output or project_root / DEFAULT_OUTPUT
    path.parent.mkdir(parents=True, exist_ok=True)
    temporary = path.with_suffix(path.suffix + ".tmp")
    temporary.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    temporary.replace(path)
    return path


def run_compile(args: argparse.Namespace) -> int:
    project_root = Path(args.project_root).expanduser().resolve()
    payload = compile_harness_health(
        project_root=project_root,
        standard_root=Path(args.standard_root).expanduser().resolve(),
        evals_root=Path(args.evals_root).expanduser().resolve() if args.evals_root else None,
    )
    written = None
    metrics_written = None
    if not args.no_write:
        written = write_projection(project_root, payload, Path(args.output).expanduser().resolve() if args.output else None)
        metrics_written = write_metric_observations(project_root, args.date, payload)
    if args.json:
        print(json.dumps(payload, indent=2, sort_keys=True))
    else:
        counts = payload.get("rollout", {}).get("counts", {})
        weighted = payload["skillHealth"]["weighted"]
        eval_health = payload["evalHealth"]
        print(
            f"farplane harness health: {counts.get('current', 0)}/{counts.get('skills', 0)} skills current, "
            f"weighted skill health {weighted['score']}%, eval health "
            f"{eval_health['score'] if eval_health.get('score') is not None else 'unscored'}"
        )
        if written:
            print(f"wrote {written}")
        if metrics_written:
            print(f"wrote {metrics_written}")
        for gap in payload["sourceGaps"]:
            print(f"- source gap: {gap}")
    return 0


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--project-root", default=str(Path.cwd()))
    parser.add_argument("--standard-root", default=str(Path(__file__).resolve().parents[2]))
    parser.add_argument("--evals-root")
    parser.add_argument("--output")
    parser.add_argument("--date", default=today_utc())
    parser.add_argument("--no-write", action="store_true")
    parser.add_argument("--json", action="store_true")
    return parser


def main(argv: list[str] | None = None) -> int:
    try:
        return run_compile(build_parser().parse_args(argv))
    except HarnessHealthError as exc:
        print(f"farplane harness health: {exc}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
