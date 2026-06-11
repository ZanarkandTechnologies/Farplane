#!/usr/bin/env python3
"""Generate a repo-wide Farplane docs/backlink graph and audit report."""

from __future__ import annotations

import argparse
import json
import re
from collections import Counter, defaultdict
from datetime import UTC, datetime
from pathlib import Path
from typing import Any


TEXT_SUFFIXES = {
    ".md",
    ".mdx",
    ".txt",
    ".json",
    ".jsonl",
    ".toml",
    ".py",
    ".sh",
    ".js",
    ".ts",
    ".tsx",
    ".html",
    ".css",
}

IGNORE_PARTS = {
    ".git",
    ".venv",
    "node_modules",
    "__pycache__",
}

GENERATED_PATHS = {
    "skills/skill-maintenance/graph/skill-graph.json",
    "skills/skill-maintenance/graph/skill-graph.js",
    "skills/skill-maintenance/graph/skill-docs.json",
    "skills/skill-maintenance/graph/skill-docs.js",
    "skills/skill-maintenance/graph/harness-graph.json",
    "skills/skill-maintenance/graph/harness-graph.js",
    "docs/doc-audit/generated/doc-reference-report.md",
}

MARKDOWN_LINK_RE = re.compile(r"!?\[[^\]]*]\(([^)\s]+)(?:\s+\"[^\"]*\")?\)")
LOCAL_PATH_RE = re.compile(
    r"(?<![\w/.-])"
    r"((?:\.\./|./)?"
    r"(?:docs|skills|tickets|templates|agents|bin|rules|qa|experiments)/"
    r"[A-Za-z0-9_./#@:+%=-]+"
    r"|(?:AGENTS|README|ARCHITECTURE|PROJECT_RULES)\.md)"
)


def rel(path: Path, repo_root: Path) -> str:
    return path.resolve().relative_to(repo_root.resolve()).as_posix()


def should_scan(path: Path, repo_root: Path) -> bool:
    rel_path = rel(path, repo_root)
    if rel_path in GENERATED_PATHS:
        return False
    if any(part in IGNORE_PARTS for part in path.parts):
        return False
    if path.name.startswith("."):
        return False
    return path.is_file() and path.suffix in TEXT_SUFFIXES


def iter_scan_files(repo_root: Path) -> list[Path]:
    roots = [
        repo_root / "AGENTS.md",
        repo_root / "ARCHITECTURE.md",
        repo_root / "README.md",
        repo_root / "PROJECT_RULES.md",
        repo_root / "docs",
        repo_root / "skills",
        repo_root / "templates",
        repo_root / "agents",
        repo_root / "bin",
        repo_root / "rules",
        repo_root / "tickets" / "README.md",
    ]
    files: list[Path] = []
    for root in roots:
        if root.is_file() and should_scan(root, repo_root):
            files.append(root)
        elif root.is_dir():
            files.extend(path for path in root.rglob("*") if should_scan(path, repo_root))
    return sorted(set(files))


def clean_ref(ref: str) -> str:
    ref = ref.strip().strip("<>").strip("'\"`")
    ref = ref.split("?", 1)[0]
    ref = ref.rstrip(".,;:)]}")
    if ref.startswith("file://"):
        ref = ref.removeprefix("file://")
    return ref


def is_external(ref: str) -> bool:
    return bool(re.match(r"^[a-zA-Z][a-zA-Z0-9+.-]*:", ref)) and not ref.startswith("file:")


def resolve_local_ref(ref: str, source: Path, repo_root: Path) -> tuple[str | None, str | None]:
    cleaned = clean_ref(ref)
    if not cleaned or cleaned.startswith("#") or is_external(cleaned):
        return None, None
    path_part = cleaned.split("#", 1)[0]
    if not path_part:
        return None, None
    if any(marker in path_part for marker in ("TASK-XXXX", "<", ">", "{", "}")):
        return None, None
    path_part = path_part.replace("%20", " ")
    candidate = Path(path_part)
    if candidate.is_absolute():
        try:
            resolved = candidate.resolve().relative_to(repo_root.resolve())
            candidate = repo_root / resolved
        except ValueError:
            parts = candidate.parts
            if "Farplane" in parts:
                suffix = parts[parts.index("Farplane") + 1 :]
                candidate = (repo_root / Path(*suffix)).resolve()
            else:
                return None, path_part
    elif path_part.startswith("../") or path_part.startswith("./"):
        candidate = (source.parent / path_part).resolve()
    else:
        candidate = (repo_root / path_part).resolve()
    try:
        local = candidate.relative_to(repo_root.resolve()).as_posix()
    except ValueError:
        return None, path_part
    if candidate.exists():
        if candidate.is_dir():
            for name in ("README.md", "SKILL.md"):
                index = candidate / name
                if index.exists():
                    return rel(index, repo_root), None
        return local, None
    return None, local


def extract_refs(text: str) -> list[tuple[str, str]]:
    refs: list[tuple[str, str]] = []
    for match in MARKDOWN_LINK_RE.finditer(text):
        refs.append((match.group(1), "markdown-link"))
    for match in LOCAL_PATH_RE.finditer(text):
        refs.append((match.group(1), "literal-path"))
    return refs


def source_node(path: Path, repo_root: Path) -> str:
    local = rel(path, repo_root)
    parts = local.split("/")
    if len(parts) >= 2 and parts[0] == "skills":
        return f"skill:{parts[1]}"
    return f"file:{local}"


def node_kind(node_id: str) -> str:
    path = node_id.removeprefix("file:").removeprefix("skill:")
    if node_id.startswith("skill:"):
        return "skill"
    if path.startswith("docs/specs/"):
        return "spec"
    if path.startswith("docs/skills/"):
        return "skill-doc"
    if path.startswith("docs/research/"):
        return "research"
    if path.startswith("docs/"):
        return "doc"
    if path.startswith("templates/"):
        return "template"
    if path.startswith("agents/"):
        return "agent"
    if path.startswith("bin/"):
        return "script"
    if "/" not in path:
        return "root-doc"
    return "file"


def build_graph(repo_root: Path) -> dict[str, Any]:
    files = iter_scan_files(repo_root)
    nodes: dict[str, dict[str, Any]] = {}
    edges: list[dict[str, Any]] = []
    unresolved: list[dict[str, str]] = []
    seen_edges: set[tuple[str, str, str, str]] = set()

    for path in files:
        local_source = rel(path, repo_root)
        source = source_node(path, repo_root)
        nodes.setdefault(
            source,
            {
                "id": source,
                "label": source.removeprefix("skill:").removeprefix("file:"),
                "kind": node_kind(source),
                "path": local_source if source.startswith("file:") else f"skills/{source.removeprefix('skill:')}/SKILL.md",
            },
        )
        try:
            text = path.read_text(errors="ignore")
        except UnicodeDecodeError:
            continue
        for raw_ref, ref_type in extract_refs(text):
            target_path, missing = resolve_local_ref(raw_ref, path, repo_root)
            if missing:
                unresolved.append({"source": local_source, "raw_ref": clean_ref(raw_ref), "candidate": missing})
                continue
            if not target_path:
                continue
            target = f"file:{target_path}"
            nodes.setdefault(
                target,
                {
                    "id": target,
                    "label": target_path,
                    "kind": node_kind(target),
                    "path": target_path,
                },
            )
            key = (source, target, ref_type, local_source)
            if key in seen_edges:
                continue
            seen_edges.add(key)
            edges.append(
                {
                    "source": source,
                    "target": target,
                    "type": ref_type,
                    "from_file": local_source,
                    "raw_ref": clean_ref(raw_ref),
                }
            )

    edge_type_counts = Counter(edge["type"] for edge in edges)
    kind_counts = Counter(node["kind"] for node in nodes.values())
    return {
        "schema_version": "1.0.0",
        "generated_at": datetime.now(UTC).isoformat(timespec="seconds"),
        "counts": {
            "nodes": len(nodes),
            "edges": len(edges),
            "scanned_files": len(files),
            "unresolved_refs": len(unresolved),
            "node_kinds": dict(sorted(kind_counts.items())),
            "edge_types": dict(sorted(edge_type_counts.items())),
        },
        "nodes": sorted(nodes.values(), key=lambda node: (node["kind"], node["label"])),
        "edges": sorted(edges, key=lambda edge: (edge["source"], edge["target"], edge["type"], edge["from_file"])),
        "unresolved_refs": sorted(unresolved, key=lambda item: (item["source"], item["raw_ref"]))[:200],
    }


def local_doc_paths(repo_root: Path) -> list[str]:
    docs = [
        rel(path, repo_root)
        for path in (repo_root / "docs").rglob("*")
        if path.is_file() and path.suffix in {".md", ".jsonl", ".py"}
    ]
    return sorted(docs)


def inbound_counts(graph: dict[str, Any]) -> Counter[str]:
    counts: Counter[str] = Counter()
    for edge in graph["edges"]:
        target_path = edge["target"].removeprefix("file:")
        if target_path.startswith("docs/"):
            counts[target_path] += 1
    return counts


def skill_doc_counts(graph: dict[str, Any]) -> Counter[str]:
    counts: Counter[str] = Counter()
    for edge in graph["edges"]:
        if not edge["source"].startswith("skill:"):
            continue
        target_path = edge["target"].removeprefix("file:")
        if target_path.startswith("docs/"):
            counts[target_path] += 1
    return counts


def write_json(path: Path, value: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value, indent=2, sort_keys=True) + "\n")


def write_js(path: Path, global_name: str, value: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(f"window.{global_name} = " + json.dumps(value, indent=2, sort_keys=True) + ";\n")


def markdown_table(rows: list[list[str]]) -> str:
    if not rows:
        return "_None._\n"
    header = rows[0]
    divider = ["---"] * len(header)
    body = rows[1:]
    lines = ["| " + " | ".join(header) + " |", "| " + " | ".join(divider) + " |"]
    lines.extend("| " + " | ".join(row) + " |" for row in body)
    return "\n".join(lines) + "\n"


def build_report(graph: dict[str, Any], repo_root: Path) -> str:
    inbound = inbound_counts(graph)
    skill_inbound = skill_doc_counts(graph)
    doc_paths = local_doc_paths(repo_root)
    unreferenced = [path for path in doc_paths if inbound[path] == 0]
    spec_paths = [path for path in doc_paths if path.startswith("docs/specs/") and path.endswith(".md")]
    generated_at = graph["generated_at"]
    harness_math = "docs/specs/harness-algebra.md"

    top_docs = [["Doc", "All refs", "Skill refs"]]
    for path, count in inbound.most_common(20):
        top_docs.append([f"`{path}`", str(count), str(skill_inbound[path])])

    specs = [["Spec", "All refs", "Skill refs", "Suggested status"]]
    consolidation_candidates = {
        "docs/specs/case-based-memory-context-graph.md": "merge into harness-algebra or filesystem-lifecycle if the context graph stays conceptual",
        "docs/specs/meta-harness-automation.md": "merge active pieces into harness-techniques and self-improvement-contracts",
        "docs/specs/orchestrator-subagent-loop.md": "merge durable gates into spec-first-execution-loop and review-gates",
        "docs/specs/runtime-surface.md": "merge current runtime boundaries into invocation-and-adapters",
        "docs/specs/skill-self-healing.md": "merge into self-improvement-contracts, eval, and skill-maintenance docs",
    }
    for path in sorted(spec_paths):
        status = consolidation_candidates.get(path, "keep active")
        specs.append([f"`{path}`", str(inbound[path]), str(skill_inbound[path]), status])

    global_bundle = [["Doc", "Why"]]
    for path in [
        "docs/specs/harness-algebra.md",
        "docs/specs/harness-engineering-doctrine.md",
        "docs/specs/self-improvement-contracts.md",
        "docs/skills/README.md",
        "docs/skills/system.md",
        "docs/skills/best-practices.md",
        "docs/specs/filesystem-lifecycle.md",
    ]:
        global_bundle.append([f"`{path}`", "high leverage for installed skills or harness placement"])

    unreferenced_rows = [["Doc", "Note"]]
    for path in unreferenced[:40]:
        note = "keep if loaded by directory convention" if path.endswith("AGENTS.md") else "review before archive or merge"
        unreferenced_rows.append([f"`{path}`", note])

    return f"""---
title: "Docs Reference Audit"
status: generated
owner: skill-maintenance
created_at: 2026-06-11
updated_at: 2026-06-11
tags:
  - docs
  - harness-map
  - skill-maintenance
refs:
  - skills/skill-maintenance/scripts/generate_harness_graph.py
  - skills/skill-maintenance/graph/harness-graph.json
---

# Docs Reference Audit

Generated at `{generated_at}` from local Markdown links and literal repo-path
references. This is a navigation and cleanup aid, not a deletion authority.

## Harness Math Doc

The harness math doc is `{harness_math}`.

- All inbound refs: `{inbound[harness_math]}`
- Skill-origin refs: `{skill_inbound[harness_math]}`
- Cleanup rule: keep this as the canonical equation/model surface and point
  workflow docs back to it instead of duplicating the algebra.

## Counts

- Scanned files: `{graph["counts"]["scanned_files"]}`
- Nodes: `{graph["counts"]["nodes"]}`
- Edges: `{graph["counts"]["edges"]}`
- Unresolved local-looking refs: `{graph["counts"]["unresolved_refs"]}`

## Most Referenced Docs

{markdown_table(top_docs)}
## Spec Status Preview

{markdown_table(specs)}
## Suggested Global Docs Bundle

These are the first docs to ship or copy alongside installed skills if a skill
needs local doc references outside its own package.

{markdown_table(global_bundle)}
## Unreferenced Docs Preview

Unreferenced here means no local link or literal-path reference was detected in
the scanned files. Directory-loaded files, validators, and historical evidence
can still be worth keeping.

{markdown_table(unreferenced_rows)}
## Next Cleanup Pass

1. Merge active content from the consolidation candidates into the target
   canonical specs.
2. Update references.
3. Move superseded files under `docs/archive/` only after the graph shows their
   important inbound refs have been redirected.
4. Keep `docs/research/**` as historical evidence unless a source registry row
   or active spec requires a new location.
"""


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--repo-root", default=".")
    parser.add_argument("--out", default="skills/skill-maintenance/graph/harness-graph.json")
    parser.add_argument("--js-out", default="skills/skill-maintenance/graph/harness-graph.js")
    parser.add_argument("--report-out", default="docs/doc-audit/generated/doc-reference-report.md")
    args = parser.parse_args()

    repo_root = Path(args.repo_root).resolve()
    graph = build_graph(repo_root)
    write_json(repo_root / args.out, graph)
    write_js(repo_root / args.js_out, "HARNESS_GRAPH", graph)
    report = build_report(graph, repo_root)
    (repo_root / args.report_out).parent.mkdir(parents=True, exist_ok=True)
    (repo_root / args.report_out).write_text(report)
    print(
        "wrote "
        f"{args.out} ({graph['counts']['nodes']} nodes, {graph['counts']['edges']} edges), "
        f"{args.js_out}, and {args.report_out}"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
