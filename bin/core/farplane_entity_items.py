"""Roles, goals, problems and resources kept on Wiki entity pages: normalize, validate, project."""

from __future__ import annotations

import re
from typing import Any

OWNER_ITEM_FIELDS = ("problems", "resources")
PROBLEM_STATUSES = ("open", "solved", "dropped")
PROBLEM_SIZES = ("big",)
HELP_IMPACTS = ("high", "medium", "low")
HELP_STATUSES = ("suggested", "confirmed")
STEP_STATUSES = ("todo", "next", "done", "blocked")
ISO_DATE_PATTERN = re.compile(r"^\d{4}-\d{2}-\d{2}$")


def validate_id(entity_id: str) -> str | None:
    if not entity_id:
        return "missing:id"
    if entity_id.startswith(('.', '-')) or any(char not in "abcdefghijklmnopqrstuvwxyz0123456789-_" for char in entity_id):
        return "invalid_id"
    return None


def entity_roles(frontmatter: dict[str, Any]) -> list[str]:
    """Roles a person or company plays (client, creator, …); a creator is a person with the creator role."""
    value = frontmatter.get("roles")
    if not isinstance(value, list):
        return []
    return sorted({str(role).strip() for role in value if str(role).strip()})


def owner_items(frontmatter: dict[str, Any], field: str) -> list[dict[str, Any]]:
    """Problems or resources kept on their owner's page, normalized; malformed items are left to validation."""
    value = frontmatter.get(field)
    if not isinstance(value, list):
        return []
    items: list[dict[str, Any]] = []
    for raw in value:
        if not isinstance(raw, dict) or validate_id(str(raw.get("id") or "").strip()):
            continue
        item: dict[str, Any] = {"id": str(raw["id"]).strip(), "text": str(raw.get("text") or "").strip()}
        if raw.get("source"):
            item["source"] = str(raw["source"]).strip()
        if field == "problems":
            item["status"] = str(raw.get("status") or "open").strip()
            for key in ("since", "size"):
                if raw.get(key):
                    item[key] = str(raw[key]).strip()
            if raw.get("ongoing") is True:
                item["ongoing"] = True
        else:
            helps = raw.get("helps")
            item["helps"] = [
                {
                    "problem": str(help_item.get("problem") or "").strip(),
                    "impact": str(help_item.get("impact") or "").strip(),
                    "status": str(help_item.get("status") or "suggested").strip(),
                }
                for help_item in (helps if isinstance(helps, list) else [])
                if isinstance(help_item, dict)
            ]
        items.append(item)
    return items


def entity_goals(frontmatter: dict[str, Any]) -> list[dict[str, Any]]:
    """Goals on a company or person page, normalized: each goal's setups carry a critical path of steps."""
    value = frontmatter.get("goals")
    if not isinstance(value, list):
        return []
    goals: list[dict[str, Any]] = []
    for raw in value:
        if not isinstance(raw, dict) or validate_id(str(raw.get("id") or "").strip()):
            continue
        goal: dict[str, Any] = {"id": str(raw["id"]).strip(), "title": str(raw.get("title") or "").strip()}
        for key in ("unit", "deadline"):
            if raw.get(key):
                goal[key] = str(raw[key]).strip()
        target = raw.get("target")
        goal["target"] = target if isinstance(target, (int, float)) and not isinstance(target, bool) else None
        setups: list[dict[str, Any]] = []
        for setup in raw.get("setups") if isinstance(raw.get("setups"), list) else []:
            if not isinstance(setup, dict) or validate_id(str(setup.get("id") or "").strip()):
                continue
            entry: dict[str, Any] = {"id": str(setup["id"]).strip(), "title": str(setup.get("title") or "").strip()}
            for key in ("for", "owner", "done_when", "project"):
                if setup.get(key):
                    entry[key] = str(setup[key]).strip()
            entry["steps"] = [
                {
                    "text": str(step.get("text") or "").strip(),
                    "status": str(step.get("status") or "todo").strip(),
                    **({"owner": str(step["owner"]).strip()} if step.get("owner") else {}),
                }
                for step in (setup.get("steps") if isinstance(setup.get("steps"), list) else [])
                if isinstance(step, dict)
            ]
            setups.append(entry)
        goal["setups"] = setups
        goals.append(goal)
    return goals


def goal_issues(frontmatter: dict[str, Any], known_ids: set[str]) -> list[str]:
    """Validate goals[]: ids, dates, numeric targets, step statuses, and people/company refs."""
    value = frontmatter.get("goals")
    if value is None:
        return []
    if not isinstance(value, list):
        return ["invalid_goals:not_list"]
    issues: list[str] = []
    for raw in value:
        goal_id = str(raw.get("id") or "").strip() if isinstance(raw, dict) else ""
        if validate_id(goal_id):
            issues.append(f"invalid_goal_id:{goal_id or 'missing'}")
            continue
        if not str(raw.get("title") or "").strip():
            issues.append(f"missing_goal_title:{goal_id}")
        if raw.get("deadline") is not None and not ISO_DATE_PATTERN.match(str(raw["deadline"]).strip()):
            issues.append(f"invalid_goal_deadline:{goal_id}")
        target = raw.get("target")
        if target is not None and (isinstance(target, bool) or not isinstance(target, (int, float))):
            issues.append(f"invalid_goal_target:{goal_id}")
        for setup in raw.get("setups") or []:
            setup_id = str(setup.get("id") or "").strip() if isinstance(setup, dict) else ""
            if validate_id(setup_id):
                issues.append(f"invalid_setup_id:{goal_id}:{setup_id or 'missing'}")
                continue
            for key in ("for", "owner"):
                ref = str(setup.get(key) or "").strip()
                if ref and ref not in known_ids:
                    issues.append(f"unresolved_ref:setup_{key}:{ref}")
            for step in setup.get("steps") or []:
                status = str(step.get("status") or "todo").strip() if isinstance(step, dict) else ""
                if status not in STEP_STATUSES:
                    issues.append(f"invalid_step_status:{goal_id}:{setup_id}:{status}")
                owner = str(step.get("owner") or "").strip() if isinstance(step, dict) else ""
                if owner and owner not in known_ids:
                    issues.append(f"unresolved_ref:step_owner:{owner}")
    return issues


def owner_item_issues(frontmatter: dict[str, Any], known_problem_refs: set[str]) -> list[str]:
    """Validate roles, problems[] and resources[]; a help must point at a known `owner#problem`."""
    issues: list[str] = []
    roles = frontmatter.get("roles")
    if roles is not None and (
        not isinstance(roles, list) or any(validate_id(str(role).strip()) for role in roles)
    ):
        issues.append("invalid_roles")
    for field in OWNER_ITEM_FIELDS:
        value = frontmatter.get(field)
        if value is None:
            continue
        if not isinstance(value, list):
            issues.append(f"invalid_{field}:not_list")
            continue
        seen: set[str] = set()
        for raw in value:
            if not isinstance(raw, dict):
                issues.append(f"invalid_{field}:not_object")
                continue
            item_id = str(raw.get("id") or "").strip()
            if validate_id(item_id):
                issues.append(f"invalid_{field}_id:{item_id or 'missing'}")
                continue
            if item_id in seen:
                issues.append(f"duplicate_{field}_id:{item_id}")
            seen.add(item_id)
            if not str(raw.get("text") or "").strip():
                issues.append(f"missing_{field}_text:{item_id}")
            if field == "problems":
                status = str(raw.get("status") or "open").strip()
                if status not in PROBLEM_STATUSES:
                    issues.append(f"invalid_problem_status:{item_id}:{status}")
                since = raw.get("since")
                if since is not None and not ISO_DATE_PATTERN.match(str(since).strip()):
                    issues.append(f"invalid_problem_since:{item_id}")
                if raw.get("size") is not None and str(raw["size"]).strip() not in PROBLEM_SIZES:
                    issues.append(f"invalid_problem_size:{item_id}")
                if raw.get("ongoing") is not None and not isinstance(raw["ongoing"], bool):
                    issues.append(f"invalid_problem_ongoing:{item_id}")
                continue
            helps = raw.get("helps")
            if helps is None:
                continue
            if not isinstance(helps, list):
                issues.append(f"invalid_helps:{item_id}")
                continue
            for help_item in helps:
                if not isinstance(help_item, dict):
                    issues.append(f"invalid_helps:{item_id}")
                    continue
                ref = str(help_item.get("problem") or "").strip()
                if ref not in known_problem_refs:
                    issues.append(f"unresolved_ref:helps:{ref}")
                if str(help_item.get("impact") or "").strip() not in HELP_IMPACTS:
                    issues.append(f"invalid_help_impact:{item_id}:{ref}")
                if str(help_item.get("status") or "suggested").strip() not in HELP_STATUSES:
                    issues.append(f"invalid_help_status:{item_id}:{ref}")
    return issues


def problem_refs(records: list[dict[str, Any]]) -> set[str]:
    """Every `owner#problem` ref a resource's `helps` may point at."""
    return {
        f"{record['id']}#{item['id']}"
        for record in records
        for item in owner_items(record["frontmatter"], "problems")
    }


def item_index_fields(frontmatter: dict[str, Any]) -> dict[str, Any]:
    """Roles, problems, resources and goals for one entity-index entry; empty fields are left out."""
    fields: dict[str, Any] = {"roles": entity_roles(frontmatter)}
    for field in OWNER_ITEM_FIELDS:
        fields[field] = owner_items(frontmatter, field)
    fields["goals"] = entity_goals(frontmatter)
    return {key: value for key, value in fields.items() if value}


def owner_item_graph(record: dict[str, Any], project_id: str, edges_by_key: dict[str, Any]) -> list[dict[str, Any]]:
    """Graph nodes for a page's problems and resources; adds their `owns` and `helps` edges to edges_by_key."""
    frontmatter = record["frontmatter"]
    nodes: list[dict[str, Any]] = []
    owner_key = f"{project_id}:{record['id']}"
    for field, kind in (("problems", "problem"), ("resources", "resource")):
        for item in owner_items(frontmatter, field):
            item_ref = f"{record['id']}#{item['id']}"
            item_key = f"{project_id}:{item_ref}"
            nodes.append({
                "key": item_key,
                "project_id": project_id,
                "entity_id": item_ref,
                "kind": kind,
                "name": item["text"],
                "path": record["path"],
                "owner_entity_id": record["id"],
                **{key: value for key, value in item.items() if key not in ("id", "text", "helps")},
            })
            owns_key = f"{project_id}:owns:{item_ref}"
            edges_by_key[owns_key] = {
                "key": owns_key,
                "project_id": project_id,
                "kind": "owns",
                "directed": True,
                "source_key": owner_key,
                "source_entity_id": record["id"],
                "target_key": item_key,
                "target_entity_id": item_ref,
                "path": record["path"],
            }
            for help_item in item.get("helps", []):
                help_key = f"{project_id}:helps:{item_ref}>{help_item['problem']}"
                edges_by_key[help_key] = {
                    "key": help_key,
                    "project_id": project_id,
                    "kind": "helps",
                    "directed": True,
                    "source_key": item_key,
                    "source_entity_id": item_ref,
                    "target_key": f"{project_id}:{help_item['problem']}",
                    "target_entity_id": help_item["problem"],
                    "impact": help_item["impact"],
                    "status": help_item["status"],
                    "path": record["path"],
                }
    return nodes


def crm_entry(record: dict[str, Any], project_id: str) -> dict[str, Any] | None:
    """A CRM row for a client (the client role) or a funnel-bearing entity; None for everyone else."""
    funnel = record["frontmatter"].get("funnel")
    roles = entity_roles(record["frontmatter"])
    has_funnel = isinstance(funnel, dict) and bool(funnel)
    if not has_funnel and "client" not in roles:
        return None
    entry: dict[str, Any] = {
        "key": f"{project_id}:{record['id']}",
        "project_id": project_id,
        "entity_id": record["id"],
        "kind": record["kind"],
        "name": record["name"],
        "path": record["path"],
        "funnel": funnel if has_funnel else {},
    }
    if roles:
        entry["roles"] = roles
    return entry
