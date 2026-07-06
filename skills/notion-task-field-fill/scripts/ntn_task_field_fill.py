#!/usr/bin/env python3
"""Run Notion task field-fill through the official ntn CLI."""

from __future__ import annotations

import argparse
import json
import os
import re
import subprocess
import sys
from dataclasses import dataclass
from datetime import datetime, timedelta
from pathlib import Path
from typing import Any, Mapping
from zoneinfo import ZoneInfo

import notion_config


DEFAULT_PRIVATE_CONTEXT = Path("/Users/kenjipcx/.codex/private/docs/notion.md")
DEFAULT_TZ = "Asia/Kuala_Lumpur"
TARGET_FIELDS = ["Act Time", "Project", "Areas", "Attention Required", "Tags"]
TASK_ALLOWED_KEYS = {
    "Name",
    "Status",
    "Act Time",
    "Task Due Date",
    "Project",
    "Areas",
    "Attention Required",
    "Tags",
    "Description",
    "Pinned",
    "Goals",
}


class NtnFieldFillError(RuntimeError):
    """Raised when the ntn-backed field-fill run cannot proceed safely."""


@dataclass(frozen=True)
class NtnResult:
    args: list[str]
    stdout: str
    stderr: str
    data: Any


def read_text(path: Path) -> str:
    try:
        return path.read_text(encoding="utf-8")
    except FileNotFoundError as exc:
        raise NtnFieldFillError(f"private_context_missing: {path}") from exc


def json_block_after_heading(markdown: str, heading_text: str) -> dict[str, Any]:
    pattern = re.compile(
        rf"^###\s+{re.escape(heading_text)}\s*$.*?```json\s*(.*?)\s*```",
        re.DOTALL | re.MULTILINE,
    )
    match = pattern.search(markdown)
    if not match:
        raise NtnFieldFillError(f"private_context_missing: recipe {heading_text!r}")
    try:
        parsed = json.loads(match.group(1))
    except json.JSONDecodeError as exc:
        raise NtnFieldFillError(f"private_context_invalid: recipe {heading_text!r}: {exc}") from exc
    if not isinstance(parsed, dict):
        raise NtnFieldFillError(f"private_context_invalid: recipe {heading_text!r} is not an object")
    return parsed


def replace_window_date(value: Any, local_window_date: str) -> Any:
    if isinstance(value, str):
        return value.replace("<local-window-date>", local_window_date)
    if isinstance(value, list):
        return [replace_window_date(item, local_window_date) for item in value]
    if isinstance(value, dict):
        return {key: replace_window_date(item, local_window_date) for key, item in value.items()}
    return value


def ntn_env(env: Mapping[str, str] | None = None) -> dict[str, str]:
    source = dict(os.environ if env is None else env)
    token = notion_config.require_notion_token(source)
    source["NOTION_API_TOKEN"] = token
    return source


def redact(value: str, env: Mapping[str, str] | None = None) -> str:
    redacted = value
    token = notion_config.notion_token(env)
    if token:
        redacted = redacted.replace(token, "<NOTION_TOKEN>")
    redacted = re.sub(
        r"\b[0-9a-fA-F]{8}-[0-9a-fA-F]{4}-[0-9a-fA-F]{4}-[0-9a-fA-F]{4}-[0-9a-fA-F]{12}\b",
        "<notion-id>",
        redacted,
    )
    redacted = re.sub(r'https://(?:www|app)\.notion\.(?:so|com)/[^\s)>"]+', "<notion-url>", redacted)
    return redacted


def run_ntn(args: list[str], data: dict[str, Any] | None = None, env: Mapping[str, str] | None = None) -> NtnResult:
    cmd = ["ntn", *args]
    input_text = json.dumps(data) if data is not None else None
    completed = subprocess.run(
        cmd,
        input=input_text,
        text=True,
        capture_output=True,
        env=ntn_env(env),
        check=False,
    )
    if completed.returncode != 0:
        stderr = redact(completed.stderr.strip(), env)
        stdout = redact(completed.stdout.strip(), env)
        raise NtnFieldFillError(
            f"ntn_failed: {' '.join(cmd)} rc={completed.returncode} stdout={stdout} stderr={stderr}"
        )
    stdout = completed.stdout.strip()
    parsed: Any = None
    if stdout:
        try:
            parsed = json.loads(stdout)
        except json.JSONDecodeError as exc:
            raise NtnFieldFillError(f"ntn_invalid_json: {' '.join(cmd)}: {exc}") from exc
    return NtnResult(args=cmd, stdout=stdout, stderr=completed.stderr.strip(), data=parsed)


def query_data_source(recipe: dict[str, Any], *, local_window_date: str, env: Mapping[str, str] | None = None) -> NtnResult:
    data_source_id = str(recipe.get("data_source_id") or "").strip()
    if not data_source_id:
        raise NtnFieldFillError("private_context_invalid: missing data_source_id")
    filter_properties = recipe.get("filter_properties")
    if not isinstance(filter_properties, list) or not filter_properties:
        raise NtnFieldFillError("private_context_invalid: missing filter_properties")
    body = replace_window_date(
        {key: value for key, value in recipe.items() if key not in {"data_source_id", "filter_properties"}},
        local_window_date,
    )
    args = ["api", f"/v1/data_sources/{data_source_id}/query", "-X", "POST"]
    for prop in filter_properties:
        args.append(f"filter_properties=={prop}")
    args.extend(["--data", "@-"])
    return run_ntn(args, body, env)


def plain_text(items: Any) -> str:
    if not isinstance(items, list):
        return ""
    chunks: list[str] = []
    for item in items:
        if isinstance(item, dict):
            text = item.get("plain_text")
            if isinstance(text, str):
                chunks.append(text)
    return "".join(chunks).strip()


def property_text(prop: Mapping[str, Any]) -> str:
    kind = prop.get("type")
    if kind == "title":
        return plain_text(prop.get("title"))
    if kind == "rich_text":
        return plain_text(prop.get("rich_text"))
    return ""


def select_name(prop: Mapping[str, Any], key: str) -> str | None:
    value = prop.get(key)
    if isinstance(value, dict):
        name = value.get("name")
        return name if isinstance(name, str) and name else None
    return None


def multi_select_names(prop: Mapping[str, Any]) -> list[str]:
    raw = prop.get("multi_select")
    if not isinstance(raw, list):
        return []
    return [item["name"] for item in raw if isinstance(item, dict) and isinstance(item.get("name"), str)]


def relation_ids(prop: Mapping[str, Any]) -> list[str]:
    raw = prop.get("relation")
    if not isinstance(raw, list):
        return []
    return [item["id"] for item in raw if isinstance(item, dict) and isinstance(item.get("id"), str)]


def date_start(prop: Mapping[str, Any]) -> str | None:
    raw = prop.get("date")
    if isinstance(raw, dict) and isinstance(raw.get("start"), str):
        return raw["start"]
    return None


def checkbox_value(prop: Mapping[str, Any]) -> bool:
    return bool(prop.get("checkbox")) if prop.get("type") == "checkbox" else False


def normalize_task(row: Mapping[str, Any], index: int) -> dict[str, Any]:
    props = row.get("properties")
    if not isinstance(props, dict):
        raise NtnFieldFillError(f"unexpected_task_properties: row {index} missing properties")
    extra_keys = set(props) - TASK_ALLOWED_KEYS
    if extra_keys:
        raise NtnFieldFillError(f"unexpected_task_properties: {', '.join(sorted(extra_keys))}")
    return {
        "task_ref": f"task-{index + 1}",
        "page_id": row.get("id") if isinstance(row.get("id"), str) else "",
        "name": property_text(props.get("Name", {})),
        "status": select_name(props.get("Status", {}), "status") or "",
        "created_time": row.get("created_time") if isinstance(row.get("created_time"), str) else None,
        "act_time": date_start(props.get("Act Time", {})),
        "task_due_date": date_start(props.get("Task Due Date", {})),
        "project_ids": relation_ids(props.get("Project", {})),
        "area_ids": relation_ids(props.get("Areas", {})),
        "description": property_text(props.get("Description", {})),
        "attention_required": select_name(props.get("Attention Required", {}), "select"),
        "tags": multi_select_names(props.get("Tags", {})),
        "pinned": checkbox_value(props.get("Pinned", {})),
        "goal_ids": relation_ids(props.get("Goals", {})),
    }


def normalize_project(row: Mapping[str, Any], index: int) -> dict[str, Any]:
    props = row.get("properties") if isinstance(row.get("properties"), dict) else {}
    return {
        "project_ref": f"project-{index + 1}",
        "page_id": row.get("id") if isinstance(row.get("id"), str) else "",
        "name": property_text(props.get("Name", {})),
        "status": select_name(props.get("Status", {}), "status") or "",
        "focus_this_week": property_text(props.get("Focus This Week", {})),
        "context": property_text(props.get("Context", {})),
        "tags": multi_select_names(props.get("Tags", {})),
        "active_period": date_start(props.get("Active Period", {})),
        "area_ids": relation_ids(props.get("Areas", {})),
    }


def in_window(task: Mapping[str, Any], *, start: datetime, end: datetime) -> bool:
    created = task.get("created_time")
    if isinstance(created, str):
        try:
            parsed = datetime.fromisoformat(created.replace("Z", "+00:00")).astimezone(start.tzinfo)
            if start <= parsed <= end:
                return True
        except ValueError:
            pass
    act_time = task.get("act_time")
    if isinstance(act_time, str) and len(act_time) >= 10:
        try:
            act_date = datetime.fromisoformat(act_time[:10]).date()
            return start.date() <= act_date <= end.date()
        except ValueError:
            return False
    return created is None


def missing_fields(task: Mapping[str, Any], fields: list[str]) -> list[str]:
    missing: list[str] = []
    if "Act Time" in fields and not task.get("act_time"):
        missing.append("Act Time")
    if "Project" in fields and not task.get("project_ids"):
        missing.append("Project")
    if "Areas" in fields and not task.get("area_ids"):
        missing.append("Areas")
    if "Attention Required" in fields and not task.get("attention_required"):
        missing.append("Attention Required")
    if "Tags" in fields and not task.get("tags"):
        missing.append("Tags")
    return missing


def infer_attention(name: str, description: str) -> tuple[str | None, str, list[str]]:
    text = f"{name} {description}".lower()
    if any(term in text for term in ["account", "credential", "manual", "kenji", "review", "call", "meeting", "setup"]):
        return "Foreground", "high", ["task appears to require human judgment, setup, or account access"]
    if any(term in text for term in ["implement", "fix", "build", "run", "script", "code", "qa", "test", "polish", "draft"]):
        return "Delegateable", "high", ["task appears to be bounded agent execution"]
    if any(term in text for term in ["research", "look into", "watch", "monitor"]):
        return "Background", "medium", ["task appears research/watch oriented"]
    return None, "low", ["not enough evidence to infer attention safely"]


def infer_tags(name: str, description: str) -> tuple[list[str], str, list[str]]:
    text = f"{name} {description}".lower()
    tags: list[str] = []
    if "reel" in text or "short" in text or "video" in text:
        tags.extend(["Reel", "Content"] if "reel" in text else ["Content"])
    elif any(term in text for term in ["post", "thread", "pitch", "content"]):
        tags.append("Content")
    if any(term in text for term in ["write", "writing", "draft"]):
        tags.append("Writing")
    if any(term in text for term in ["api", "code", "script", "bug", "fix", "build", "implement", "qa", "test"]):
        tags.append("Technical")
    if "proposal" in text or "pitch" in text:
        tags.append("Proposal")
    if "infrastructure" in text or "infra" in text:
        tags.append("Infrastructure")
    if "autonomous" in text:
        tags.append("Autonomous")
    if "meeting" in text or "call" in text:
        tags.append("Meeting")
    if any(term in text for term in ["research", "look into", "model", "scout"]):
        tags.append("Research")
    if any(term in text for term in ["setup", "account", "admin"]):
        tags.append("Admin")
    deduped = list(dict.fromkeys(tags))
    if not deduped:
        return [], "low", ["no obvious conservative tag from title or description"]
    explicit_high_terms = {
        "Reel": "reel",
        "Writing": "write",
        "Proposal": "proposal",
        "Infrastructure": "infrastructure",
        "Autonomous": "autonomous",
        "Meeting": "meeting",
        "Admin": "admin",
    }
    confidence = "high" if any(term in text for tag, term in explicit_high_terms.items() if tag in deduped) else "medium"
    return deduped, confidence, ["tags inferred conservatively from task text"]


def project_by_id(projects: list[dict[str, Any]]) -> dict[str, dict[str, Any]]:
    return {project["page_id"]: project for project in projects if project.get("page_id")}


def proposal_for_task(
    task: dict[str, Any],
    *,
    projects: list[dict[str, Any]],
    today: str,
    fields: list[str],
) -> dict[str, Any]:
    proposals: dict[str, Any] = {}
    patch: dict[str, Any] = {}
    telegram_required = False
    abstentions: list[dict[str, str]] = []
    missing = missing_fields(task, fields)
    projects_by_id = project_by_id(projects)

    if "Act Time" in fields:
        if task.get("act_time"):
            proposals["Act Time"] = {"status": "already_set", "value": task["act_time"], "confidence": "high", "reasons": ["field already set"], "source_refs": ["task"]}
        else:
            proposals["Act Time"] = {"status": "proposed", "value": today, "confidence": "high", "reasons": ["task is in the active run window and has no conflicting date evidence"], "source_refs": ["task"]}
            patch["Act Time"] = today

    if "Attention Required" in fields:
        if task.get("attention_required"):
            proposals["Attention Required"] = {"status": "already_set", "value": task["attention_required"], "confidence": "high", "reasons": ["field already set"], "source_refs": ["task"]}
        else:
            value, confidence, reasons = infer_attention(task["name"], task["description"])
            status = "proposed" if confidence == "high" else "suggested" if confidence == "medium" else "needs_kenji"
            proposals["Attention Required"] = {"status": status, "value": value, "confidence": confidence, "reasons": reasons, "source_refs": ["task"]}
            if status == "proposed" and value:
                patch["Attention Required"] = value
            if status == "needs_kenji":
                telegram_required = True

    if "Tags" in fields:
        if task.get("tags"):
            proposals["Tags"] = {"status": "already_set", "value": task["tags"], "confidence": "high", "reasons": ["field already set"], "source_refs": ["task"]}
        else:
            values, confidence, reasons = infer_tags(task["name"], task["description"])
            status = "proposed" if confidence == "high" else "suggested" if confidence == "medium" else "needs_kenji"
            proposals["Tags"] = {"status": status, "value": values, "confidence": confidence, "reasons": reasons, "source_refs": ["task"]}
            if status == "proposed" and values:
                patch["Tags"] = values
            if status == "needs_kenji":
                telegram_required = True

    if "Project" in fields:
        if task.get("project_ids"):
            names = [projects_by_id.get(pid, {}).get("name") or "existing project relation" for pid in task["project_ids"]]
            proposals["Project"] = {"status": "already_set", "value": names, "confidence": "high", "reasons": ["field already set"], "source_refs": ["task"]}
        elif "Project" in missing:
            proposals["Project"] = {"status": "needs_kenji", "value": None, "confidence": "low", "reasons": ["no exact project relation evidence from compact context"], "source_refs": ["task"]}
            telegram_required = True

    if "Areas" in fields:
        if task.get("area_ids"):
            proposals["Areas"] = {"status": "already_set", "value": ["existing area relation"], "confidence": "high", "reasons": ["field already set"], "source_refs": ["task"]}
        elif task.get("project_ids"):
            related_projects = [projects_by_id.get(pid) for pid in task["project_ids"]]
            area_ids = [area for project in related_projects if project for area in project.get("area_ids", [])]
            if len(set(area_ids)) == 1:
                area_id = area_ids[0]
                proposals["Areas"] = {"status": "proposed", "value": ["project area relation"], "confidence": "high", "reasons": ["single current project area relation inherited from existing project"], "source_refs": ["task", "projects"]}
                patch["Areas"] = [{"id": area_id}]
            else:
                abstentions.append({"field": "Areas", "reason": "project_area_missing_or_ambiguous", "details": "Project did not expose one clear area relation."})
                proposals["Areas"] = {"status": "abstain", "value": None, "confidence": "none", "reasons": ["project area missing or ambiguous"], "source_refs": ["task", "projects"]}
                telegram_required = True
        elif "Areas" in missing:
            proposals["Areas"] = {"status": "needs_kenji", "value": None, "confidence": "low", "reasons": ["area requires a project or explicit area evidence"], "source_refs": ["task"]}
            telegram_required = True

    return {
        "task": {"name": task["name"], "url": task["task_ref"], "status": task["status"]},
        "missing_fields": missing,
        "field_proposals": proposals,
        "patch": patch,
        "telegram_required": telegram_required,
        "abstentions": abstentions,
        "_page_id": task["page_id"],
    }


def notion_patch_payload(patch: Mapping[str, Any]) -> dict[str, Any]:
    properties: dict[str, Any] = {}
    for field, value in patch.items():
        if field == "Act Time" and isinstance(value, str):
            properties[field] = {"date": {"start": value}}
        elif field == "Attention Required" and isinstance(value, str):
            properties[field] = {"select": {"name": value}}
        elif field == "Tags" and isinstance(value, list):
            properties[field] = {"multi_select": [{"name": item} for item in value if isinstance(item, str)]}
        elif field in {"Project", "Areas"} and isinstance(value, list):
            properties[field] = {"relation": [item for item in value if isinstance(item, dict) and isinstance(item.get("id"), str)]}
    return {"properties": properties}


def readback_matches(page: Mapping[str, Any], patch: Mapping[str, Any]) -> bool:
    props = page.get("properties") if isinstance(page.get("properties"), dict) else {}
    for field, value in patch.items():
        prop = props.get(field, {})
        if field == "Act Time" and date_start(prop) != value:
            return False
        if field == "Attention Required" and select_name(prop, "select") != value:
            return False
        if field == "Tags":
            current = set(multi_select_names(prop))
            if not set(value).issubset(current):
                return False
        if field in {"Project", "Areas"}:
            expected = {item["id"] for item in value if isinstance(item, dict) and isinstance(item.get("id"), str)}
            if expected and not expected.issubset(set(relation_ids(prop))):
                return False
    return True


def write_artifacts(path: Path, proposal: dict[str, Any], summary_md: str, telegram_md: str) -> None:
    path.mkdir(parents=True, exist_ok=True)
    (path / "proposal.json").write_text(json.dumps(proposal, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    (path / "proposal.md").write_text(render_proposal_markdown(proposal), encoding="utf-8")
    (path / "run-summary.md").write_text(summary_md, encoding="utf-8")
    (path / "low-confidence-telegram.md").write_text(telegram_md, encoding="utf-8")


def render_proposal_markdown(proposal: Mapping[str, Any]) -> str:
    lines = ["# Notion Task Field Fill Proposal", ""]
    run = proposal.get("run", {})
    lines.append(f"- Mode: {run.get('mode', '')}")
    lines.append(f"- Candidate count: {proposal.get('summary', {}).get('candidate_count', 0)}")
    lines.append(f"- High-confidence patch count: {proposal.get('summary', {}).get('high_confidence_patch_count', 0)}")
    lines.append("")
    for item in proposal.get("candidates", []):
        task = item.get("task", {})
        lines.append(f"## {task.get('name', 'Untitled task')}")
        lines.append(f"- Status: {task.get('status', '')}")
        lines.append(f"- Missing: {', '.join(item.get('missing_fields', [])) or 'none'}")
        for field, field_proposal in item.get("field_proposals", {}).items():
            lines.append(
                f"- {field}: {field_proposal.get('status')} / {field_proposal.get('confidence')} -> {field_proposal.get('value')}"
            )
        lines.append("")
    return "\n".join(lines).rstrip() + "\n"


def telegram_message(proposal: Mapping[str, Any], artifact_dir: Path) -> str:
    messages: list[str] = []
    for item in proposal.get("candidates", []):
        if not item.get("telegram_required"):
            continue
        task = item.get("task", {})
        fields = [
            field
            for field, field_proposal in item.get("field_proposals", {}).items()
            if field_proposal.get("status") in {"needs_kenji", "abstain"}
        ]
        messages.append(
            f"- {task.get('name', 'Untitled task')}: needs {', '.join(fields) or 'field'} review. See {artifact_dir}/proposal.md"
        )
    if not messages:
        return "No low-confidence Notion task fields need Telegram review.\n"
    return "Notion task fields need Kenji review:\n" + "\n".join(messages) + "\n"


def summarize_query_ledger(ledger: list[dict[str, Any]]) -> str:
    lines = ["## Query Ledger"]
    for item in ledger:
        props = ", ".join(item.get("property_names", []))
        lines.append(
            f"- {item['purpose']}: page_size={item['page_size']}; properties={props}; candidates={item['result_count']}; has_more={item['has_more']}; raw_rows_discarded=yes"
        )
    return "\n".join(lines)


def run(args: argparse.Namespace) -> int:
    now = datetime.now(ZoneInfo(args.timezone))
    if args.this_week:
        start = (now - timedelta(days=now.weekday())).replace(hour=0, minute=0, second=0, microsecond=0)
    else:
        start = now - timedelta(hours=args.hours)
    local_window_date = start.date().isoformat()
    today = now.date().isoformat()
    artifact_dir = Path(args.artifact_dir)
    fields = args.fields or TARGET_FIELDS

    private_context = read_text(Path(args.private_context))
    task_recipe = json_block_after_heading(private_context, "### `notion-task-field-fill` Tasks candidates".removeprefix("### "))
    projects_recipe = json_block_after_heading(private_context, "### `notion-task-field-fill` Projects context".removeprefix("### "))

    query_ledger: list[dict[str, Any]] = []
    task_result = query_data_source(task_recipe, local_window_date=local_window_date)
    task_rows = task_result.data.get("results", []) if isinstance(task_result.data, dict) else []
    tasks = [normalize_task(row, index) for index, row in enumerate(task_rows) if isinstance(row, dict)]
    tasks = [
        task
        for task in tasks
        if task.get("status") not in {"Done"}
        and in_window(task, start=start, end=now)
        and missing_fields(task, fields)
    ]
    query_ledger.append(
        {
            "purpose": "Tasks candidates",
            "page_size": task_recipe.get("page_size", 25),
            "property_names": sorted(TASK_ALLOWED_KEYS),
            "result_count": len(tasks),
            "has_more": bool(task_result.data.get("has_more")) if isinstance(task_result.data, dict) else False,
        }
    )

    projects: list[dict[str, Any]] = []
    if any("Project" in missing_fields(task, fields) or "Areas" in missing_fields(task, fields) for task in tasks):
        projects_result = query_data_source(projects_recipe, local_window_date=local_window_date)
        project_rows = projects_result.data.get("results", []) if isinstance(projects_result.data, dict) else []
        projects = [normalize_project(row, index) for index, row in enumerate(project_rows) if isinstance(row, dict)]
        query_ledger.append(
            {
                "purpose": "Projects context",
                "page_size": projects_recipe.get("page_size", 20),
                "property_names": ["Name", "Status", "Focus This Week", "Context", "Tags", "Active Period", "Areas", "Goals"],
                "result_count": len(projects),
                "has_more": bool(projects_result.data.get("has_more")) if isinstance(projects_result.data, dict) else False,
            }
        )

    candidates = [proposal_for_task(task, projects=projects, today=today, fields=fields) for task in tasks]
    writes: list[dict[str, Any]] = []
    if args.mode == "live-high-confidence":
        write_count = 0
        for candidate in candidates:
            if write_count >= args.max_live_writes:
                break
            patch = candidate.get("patch") or {}
            if args.live_field and args.live_field not in patch:
                continue
            if not patch:
                continue
            page_id = candidate.get("_page_id")
            if not page_id:
                continue
            payload = notion_patch_payload(patch)
            if not payload["properties"]:
                continue
            run_ntn(["api", f"/v1/pages/{page_id}", "-X", "PATCH", "--data", "@-"], payload)
            readback = run_ntn(["api", f"/v1/pages/{page_id}", "-X", "GET"])
            verified = isinstance(readback.data, dict) and readback_matches(readback.data, patch)
            writes.append(
                {
                    "task_name": candidate["task"]["name"],
                    "mode": args.mode,
                    "patch": patch,
                    "readback_status": "verified" if verified else "failed",
                }
            )
            if not verified:
                raise NtnFieldFillError(f"readback_failed: {candidate['task']['name']}")
            write_count += 1

    for candidate in candidates:
        candidate.pop("_page_id", None)
    high_count = sum(len(item.get("patch", {})) for item in candidates)
    medium_count = sum(
        1
        for item in candidates
        for field_proposal in item.get("field_proposals", {}).values()
        if field_proposal.get("confidence") == "medium"
    )
    low_count = sum(1 for item in candidates if item.get("telegram_required"))
    abstention_count = sum(len(item.get("abstentions", [])) for item in candidates)
    proposal = {
        "run": {
            "id": artifact_dir.name,
            "mode": args.mode,
            "window": {"start": start.isoformat(), "end": now.isoformat(), "timezone": args.timezone},
            "target_fields": fields,
            "connector_status": {"notion": "ok", "telegram": "not_attempted"},
        },
        "context": {"source_refs": ["notion.tasks.source", "notion.projects.source"], "context_gaps": []},
        "candidates": candidates,
        "notifications": [],
        "writes": writes,
        "summary": {
            "candidate_count": len(candidates),
            "high_confidence_patch_count": high_count,
            "medium_suggestion_count": medium_count,
            "low_confidence_request_count": low_count,
            "abstention_count": abstention_count,
            "live_write_count": len(writes),
        },
    }
    summary = "\n".join(
        [
            "# Notion Task Field Fill Run Summary",
            "",
            f"- Mode: {args.mode}",
            f"- Window: {start.isoformat()} through {now.isoformat()}",
            f"- Candidate count: {len(candidates)}",
            f"- Live write count: {len(writes)}",
            "",
            summarize_query_ledger(query_ledger),
            "",
        ]
    )
    write_artifacts(artifact_dir, proposal, summary, telegram_message(proposal, artifact_dir))
    print(json.dumps({"artifact_dir": str(artifact_dir), "summary": proposal["summary"]}, indent=2, sort_keys=True))
    return 0


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--mode", choices=("dry-run", "notify", "weekly-preflight", "live-high-confidence"), default="dry-run")
    parser.add_argument("--hours", type=int, default=6)
    parser.add_argument("--this-week", action="store_true")
    parser.add_argument("--timezone", default=DEFAULT_TZ)
    parser.add_argument("--fields", nargs="+", choices=TARGET_FIELDS)
    parser.add_argument("--artifact-dir", required=True)
    parser.add_argument("--private-context", default=str(DEFAULT_PRIVATE_CONTEXT))
    parser.add_argument("--max-live-writes", type=int, default=1)
    parser.add_argument("--live-field", choices=TARGET_FIELDS, help="limit live writes to candidates with this high-confidence field")
    return parser


def main(argv: list[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)
    try:
        return run(args)
    except NtnFieldFillError as exc:
        print(f"error: {redact(str(exc))}", file=sys.stderr)
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
