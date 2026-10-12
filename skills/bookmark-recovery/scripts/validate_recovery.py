#!/usr/bin/env python3
"""Validate a bookmark-recovery inbox without provider access."""

from __future__ import annotations

import argparse
import json
from pathlib import Path

ALLOWED_COVERAGE = {"complete", "partial", "blocked", "empty"}
ALLOWED_PRIORITY = {"high", "medium", "low"}
ALLOWED_ROUTES = {"intelligest_candidate", "resource_bank_candidate", "dismiss", "needs_review"}
ALLOWED_CONFIDENCE = {"high", "medium", "low"}
ALLOWED_RELATIONS = {"addresses_constraint", "supports_next_commitment", "project_opportunity"}
PERSON_RELATION = "may_solve_problem"


def _ref_path(ref: str) -> str:
    return ref.split("#", 1)[0]


def load_policy(context_path: Path) -> dict:
    context = json.loads(context_path.read_text(encoding="utf-8"))
    root = context_path.parent
    configured_sources = set(context.get("sources") or [])
    source_refs: dict[str, set[str]] = {source: set() for source in configured_sources}
    for ref in context.get("cache_refs") or []:
        path = _ref_path(ref)
        name = Path(path).name
        source = name.removesuffix(".sources.json")
        if source in source_refs:
            cache = json.loads((root / path).read_text(encoding="utf-8"))
            source_refs[source].update(cache.get("evidence_refs") or [])
    projects: dict[str, dict] = {}
    for ref in context.get("project_memory_refs") or []:
        path = root / _ref_path(ref)
        cache = json.loads(path.read_text(encoding="utf-8"))
        for project in cache.get("projects") or []:
            project_id = project.get("project_id")
            if isinstance(project_id, str) and project_id:
                projects[project_id] = {
                    "project_name": project.get("project_name"),
                    "evidence_refs": set(project.get("evidence_refs") or []),
                }
    problems: dict[str, dict] = {}
    for ref in context.get("wiki_problem_refs") or []:
        cache = json.loads((root / _ref_path(ref)).read_text(encoding="utf-8"))
        for problem in cache.get("problems") or []:
            problem_id = problem.get("problem_id")
            if isinstance(problem_id, str) and problem_id:
                problems[problem_id] = {
                    "person_ids": set(problem.get("person_ids") or []),
                    "evidence_refs": set(problem.get("evidence_refs") or []),
                }
    return {
        "run_id": context.get("run_id"),
        "generated_at": context.get("generated_at"),
        "candidate_limit": context.get("candidate_limit"),
        "project_match_limit": context.get("project_match_limit"),
        "sources": configured_sources,
        "source_refs": source_refs,
        "projects": projects,
        "problems": problems,
    }


def validate(payload: dict, policy: dict | None = None) -> list[str]:
    errors: list[str] = []
    if policy is None:
        errors.append("frozen context validation policy is required")
        policy = {"sources": set(), "source_refs": {}, "projects": {}}
    if payload.get("schema_version") != 2:
        errors.append("schema_version must equal 2")
    for field in ("run_id", "generated_at"):
        if not isinstance(payload.get(field), str) or not payload[field].strip():
            errors.append(f"{field} must be a non-empty string")
        elif payload[field] != policy.get(field):
            errors.append(f"{field} must match frozen context")
    candidate_limit = payload.get("candidate_limit")
    if not isinstance(candidate_limit, int) or isinstance(candidate_limit, bool) or candidate_limit < 1:
        errors.append("candidate_limit must be a positive integer")
        candidate_limit = 0
    elif candidate_limit != policy.get("candidate_limit"):
        errors.append("candidate_limit must match frozen context")
    project_match_limit = payload.get("project_match_limit")
    if not isinstance(project_match_limit, int) or isinstance(project_match_limit, bool) or project_match_limit < 1:
        errors.append("project_match_limit must be a positive integer")
        project_match_limit = 0
    elif project_match_limit != policy.get("project_match_limit"):
        errors.append("project_match_limit must match frozen context")
    coverage = payload.get("coverage")
    if not isinstance(coverage, list):
        errors.append("coverage must be a list")
        coverage = []
    sources: set[str] = set()
    for index, row in enumerate(coverage):
        source = row.get("source") if isinstance(row, dict) else None
        status = row.get("status") if isinstance(row, dict) else None
        if not isinstance(source, str) or not source:
            errors.append(f"coverage[{index}].source is required")
        elif source in sources:
            errors.append(f"duplicate coverage source: {source}")
        else:
            sources.add(source)
        if status not in ALLOWED_COVERAGE:
            errors.append(f"coverage[{index}].status is invalid")
    expected_sources = policy.get("sources") or set()
    if sources != expected_sources:
        errors.append("coverage sources must exactly match frozen context sources")
    candidates = payload.get("candidates")
    if not isinstance(candidates, list):
        errors.append("candidates must be a list")
        candidates = []
    if candidate_limit and len(candidates) > candidate_limit:
        errors.append("candidates exceeds candidate_limit")
    keys: set[str] = set()
    categorized_counts = {source: 0 for source in sources}
    for index, item in enumerate(candidates):
        if not isinstance(item, dict):
            errors.append(f"candidates[{index}] must be an object")
            continue
        key = item.get("canonical_key")
        if not isinstance(key, str) or not key:
            errors.append(f"candidates[{index}].canonical_key is required")
        elif key in keys:
            errors.append(f"duplicate candidate canonical_key: {key}")
        else:
            keys.add(key)
        if item.get("source") not in sources:
            errors.append(f"candidates[{index}].source lacks coverage")
        else:
            categorized_counts[item["source"]] += 1
        if item.get("priority") not in ALLOWED_PRIORITY:
            errors.append(f"candidates[{index}].priority is invalid")
        if item.get("route") not in ALLOWED_ROUTES:
            errors.append(f"candidates[{index}].route is invalid")
        use = item.get("possible_use")
        if use is not None and (not isinstance(use, dict) or use.get("kind") != "ai_hypothesis"):
            errors.append(f"candidates[{index}].possible_use must be an ai_hypothesis")
        elif isinstance(use, dict) and use.get("confidence") not in ALLOWED_CONFIDENCE:
            errors.append(f"candidates[{index}].possible_use.confidence is invalid")
        refs = item.get("evidence_refs")
        if not isinstance(refs, list) or not refs or not all(isinstance(ref, str) and ref for ref in refs):
            errors.append(f"candidates[{index}].evidence_refs must be a non-empty string list")
        elif not set(refs).intersection(policy.get("source_refs", {}).get(item.get("source")) or set()):
            errors.append(f"candidates[{index}].evidence_refs must resolve to its frozen source cache")
    for field in ("duplicates", "excluded"):
        rows = payload.get(field)
        if not isinstance(rows, list):
            errors.append(f"{field} must be a list")
            continue
        for index, item in enumerate(rows):
            if not isinstance(item, dict):
                errors.append(f"{field}[{index}] must be an object")
                continue
            key = item.get("canonical_key")
            source = item.get("source")
            if not isinstance(key, str) or not key:
                errors.append(f"{field}[{index}].canonical_key is required")
            elif key in keys:
                errors.append(f"canonical_key appears in multiple dispositions: {key}")
            else:
                keys.add(key)
            if source not in sources:
                errors.append(f"{field}[{index}].source lacks coverage")
            else:
                categorized_counts[source] += 1
            if not isinstance(item.get("reason"), str) or not item["reason"].strip():
                errors.append(f"{field}[{index}].reason is required")
    matches = payload.get("project_matches")
    if not isinstance(matches, list):
        errors.append("project_matches must be a list")
        matches = []
    candidate_keys = {
        item.get("canonical_key") for item in candidates
        if isinstance(item, dict) and isinstance(item.get("canonical_key"), str)
    }
    match_counts: dict[str, int] = {}
    match_keys: set[tuple[str, str, str]] = set()
    for index, item in enumerate(matches):
        if not isinstance(item, dict):
            errors.append(f"project_matches[{index}] must be an object")
            continue
        canonical_key = item.get("canonical_key")
        project_id = item.get("project_id")
        relation = item.get("relation")
        if canonical_key not in candidate_keys:
            errors.append(f"project_matches[{index}].canonical_key must reference a candidate")
        if not isinstance(project_id, str) or not project_id:
            errors.append(f"project_matches[{index}].project_id is required")
        project = (policy.get("projects") or {}).get(project_id)
        if project is None:
            errors.append(f"project_matches[{index}].project_id is not eligible in frozen Project Memory")
        if not isinstance(item.get("project_name"), str) or not item["project_name"].strip():
            errors.append(f"project_matches[{index}].project_name is required")
        elif project is not None and item["project_name"] != project.get("project_name"):
            errors.append(f"project_matches[{index}].project_name does not match frozen Project Memory")
        if relation not in ALLOWED_RELATIONS:
            errors.append(f"project_matches[{index}].relation is invalid")
        match_key = (canonical_key, project_id, relation)
        if all(isinstance(part, str) and part for part in match_key):
            if match_key in match_keys:
                errors.append(f"duplicate project match: {match_key}")
            match_keys.add(match_key)
        reason = item.get("reason")
        if not isinstance(reason, dict) or reason.get("kind") != "ai_hypothesis":
            errors.append(f"project_matches[{index}].reason must be an ai_hypothesis")
        elif reason.get("confidence") not in ALLOWED_CONFIDENCE:
            errors.append(f"project_matches[{index}].reason.confidence is invalid")
        refs = item.get("evidence_refs")
        if not isinstance(refs, list) or len(refs) < 2 or not all(isinstance(ref, str) and ref for ref in refs):
            errors.append(f"project_matches[{index}].evidence_refs must cite source and Project Memory")
        else:
            candidate = next(
                (row for row in candidates if isinstance(row, dict) and row.get("canonical_key") == canonical_key),
                None,
            )
            candidate_refs = set(candidate.get("evidence_refs") or []) if candidate else set()
            project_refs = project.get("evidence_refs") if project else set()
            if not candidate_refs.intersection(refs) or not project_refs.intersection(refs):
                errors.append(f"project_matches[{index}].evidence_refs must resolve to candidate and Project Memory")
        if isinstance(canonical_key, str):
            match_counts[canonical_key] = match_counts.get(canonical_key, 0) + 1
    if project_match_limit:
        for canonical_key, count in match_counts.items():
            if count > project_match_limit:
                errors.append(f"project matches for {canonical_key} exceeds project_match_limit")
    # Useful to someone: a save may address an open Wiki problem owned by a person.
    person_matches = payload.get("person_matches", [])
    if not isinstance(person_matches, list):
        errors.append("person_matches must be a list")
        person_matches = []
    person_counts: dict[str, int] = {}
    for index, item in enumerate(person_matches):
        label = f"person_matches[{index}]"
        if not isinstance(item, dict):
            errors.append(f"{label} must be an object")
            continue
        canonical_key = item.get("canonical_key")
        if canonical_key not in candidate_keys:
            errors.append(f"{label}.canonical_key must reference a candidate")
        problem = (policy.get("problems") or {}).get(item.get("problem_id"))
        if problem is None:
            errors.append(f"{label}.problem_id is not an open problem in the frozen Wiki cache")
        person_ids = item.get("person_ids")
        if not isinstance(person_ids, list) or not person_ids or not all(isinstance(pid, str) and pid for pid in person_ids):
            errors.append(f"{label}.person_ids must be a non-empty string list")
        elif problem is not None and not set(person_ids) <= problem["person_ids"]:
            errors.append(f"{label}.person_ids must be people linked to that problem")
        if item.get("relation") != PERSON_RELATION:
            errors.append(f"{label}.relation must be {PERSON_RELATION}")
        reason = item.get("reason")
        if not isinstance(reason, dict) or reason.get("kind") != "ai_hypothesis":
            errors.append(f"{label}.reason must be an ai_hypothesis")
        elif reason.get("confidence") not in ALLOWED_CONFIDENCE:
            errors.append(f"{label}.reason.confidence is invalid")
        refs = item.get("evidence_refs")
        candidate = next((row for row in candidates if isinstance(row, dict) and row.get("canonical_key") == canonical_key), None)
        candidate_refs = set(candidate.get("evidence_refs") or []) if candidate else set()
        problem_refs = problem["evidence_refs"] if problem else set()
        if not isinstance(refs, list) or not candidate_refs.intersection(refs) or not problem_refs.intersection(refs):
            errors.append(f"{label}.evidence_refs must resolve to candidate and Wiki problem")
        if isinstance(canonical_key, str):
            person_counts[canonical_key] = person_counts.get(canonical_key, 0) + 1
    if project_match_limit:
        for canonical_key, count in person_counts.items():
            if count > project_match_limit:
                errors.append(f"person matches for {canonical_key} exceeds project_match_limit")
    if not isinstance(payload.get("limitations"), list):
        errors.append("limitations must be a list")
    for index, row in enumerate(coverage):
        if not isinstance(row, dict) or row.get("source") not in sources:
            continue
        item_count = row.get("item_count")
        if not isinstance(item_count, int) or isinstance(item_count, bool) or item_count < 0:
            errors.append(f"coverage[{index}].item_count must be a non-negative integer")
            continue
        if categorized_counts[row["source"]] != item_count:
            errors.append(
                f"coverage[{index}].item_count does not reconcile: "
                f"{item_count} observed vs {categorized_counts[row['source']]} categorized"
            )
    return errors


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("path", type=Path)
    parser.add_argument("--context", type=Path, required=True)
    args = parser.parse_args()
    payload = json.loads(args.path.read_text(encoding="utf-8"))
    errors = validate(payload, load_policy(args.context))
    print(json.dumps({"valid": not errors, "errors": errors}, indent=2))
    return 0 if not errors else 1


if __name__ == "__main__":
    raise SystemExit(main())
