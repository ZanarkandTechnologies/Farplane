#!/usr/bin/env python3
"""Generate a repo-wide Farplane docs/backlink graph and audit report."""

from __future__ import annotations

import argparse
import json
import re
import subprocess
from collections import Counter, defaultdict
from pathlib import Path
from typing import Any

from graph_ir import GraphBundle, GraphEdge, GraphNode, edge_counts, node_kind_counts, utc_timestamp, write_js, write_json
from graph_projection_config import get_projection_config


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

IGNORE_PREFIXES = (
    "docs/archive/",
    "docs/doc-audit/",
    "docs/futureideas/",
)

GENERATED_PATHS = {
    "skills/skill-maintenance/graph/skill-graph.json",
    "skills/skill-maintenance/graph/skill-graph.js",
    "skills/skill-maintenance/graph/skill-docs.json",
    "skills/skill-maintenance/graph/skill-docs.js",
    "skills/skill-maintenance/graph/harness-graph.json",
    "skills/skill-maintenance/graph/harness-graph.js",
    "skills/skill-maintenance/graph/farplane-framework-core-graph.json",
    "skills/skill-maintenance/graph/farplane-framework-core-graph.js",
    "docs/doc-audit/generated/doc-reference-report.md",
}

MARKDOWN_LINK_RE = re.compile(r"!?\[[^\]]*]\(([^)\s]+)(?:\s+\"[^\"]*\")?\)")
LOCAL_PATH_RE = re.compile(
    r"(?<![\w/.-])"
    r"((?:\.\./|./)?"
    r"(?:docs|skills|tickets|templates|agents|bin|rules|qa|experiments|farplane)/"
    r"[A-Za-z0-9_./#@:+%=-]+"
    r"|(?:AGENTS|README|ARCHITECTURE|PROJECT_RULES)\.md)"
)


def rel(path: Path, repo_root: Path) -> str:
    return path.resolve().relative_to(repo_root.resolve()).as_posix()


def ignored_prefix(path: str) -> bool:
    return path.startswith(IGNORE_PREFIXES)


def should_scan(path: Path, repo_root: Path) -> bool:
    rel_path = rel(path, repo_root)
    if rel_path in GENERATED_PATHS:
        return False
    if ignored_prefix(rel_path):
        return False
    if any(part in IGNORE_PARTS for part in path.parts):
        return False
    if path.name.startswith("."):
        return False
    return path.is_file() and path.suffix in TEXT_SUFFIXES


def git_cached_rel_paths(repo_root: Path) -> set[str] | None:
    try:
        result = subprocess.run(
            ["git", "ls-files", "-z", "--cached"],
            cwd=repo_root,
            check=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.DEVNULL,
        )
    except (subprocess.CalledProcessError, FileNotFoundError):
        return None
    return {raw.decode() for raw in result.stdout.split(b"\0") if raw}


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
        repo_root / "farplane",
        repo_root / "rules",
        repo_root / "tickets" / "README.md",
    ]
    cached_rel_paths = git_cached_rel_paths(repo_root)
    tracked_paths = None
    if cached_rel_paths is not None:
        tracked_paths = {(repo_root / raw).resolve() for raw in cached_rel_paths}

    files: list[Path] = []
    for root in roots:
        if root.is_file() and should_scan(root, repo_root):
            if tracked_paths is None or root.resolve() in tracked_paths:
                files.append(root)
        elif root.is_dir():
            files.extend(
                path
                for path in root.rglob("*")
                if should_scan(path, repo_root)
                and (tracked_paths is None or path.resolve() in tracked_paths)
            )
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


def resolve_local_ref(ref: str, source: Path, repo_root: Path) -> tuple[str | None, str | None, bool]:
    cleaned = clean_ref(ref)
    if not cleaned or cleaned.startswith("#") or is_external(cleaned):
        return None, None, False
    path_part = cleaned.split("#", 1)[0]
    if not path_part:
        return None, None, False
    if any(marker in path_part for marker in ("TASK-XXXX", "<", ">", "{", "}")):
        return None, None, False
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
                return None, path_part, False
    elif path_part.startswith("../") or path_part.startswith("./"):
        candidate = (source.parent / path_part).resolve()
    else:
        candidate = (repo_root / path_part).resolve()
    try:
        local = candidate.relative_to(repo_root.resolve()).as_posix()
    except ValueError:
        return None, path_part, False
    if ignored_prefix(local):
        return None, None, False
    if candidate.exists():
        if candidate.is_dir():
            for name in ("README.md", "SKILL.md"):
                index = candidate / name
                if index.exists():
                    return rel(index, repo_root), None, False
            return local, None, True
        return local, None, False
    return None, local, False


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
    if path.startswith("dir:docs/review/rubrics") or path.startswith("docs/review/rubrics/"):
        return "review-rubric"
    if path.startswith("docs/"):
        return "doc"
    if path.startswith("templates/"):
        return "template"
    if path.startswith("farplane/"):
        return "file"
    if path.startswith("agents/"):
        return "agent"
    if path.startswith("bin/"):
        return "script"
    if "/" not in path:
        return "root-doc"
    return "file"


def build_graph(repo_root: Path) -> dict[str, Any]:
    files = iter_scan_files(repo_root)
    cached_rel_paths = git_cached_rel_paths(repo_root)
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
            if ignored_prefix(clean_ref(raw_ref)):
                continue
            target_path, missing, is_directory = resolve_local_ref(raw_ref, path, repo_root)
            if missing:
                unresolved.append({"source": local_source, "raw_ref": clean_ref(raw_ref), "candidate": missing})
                continue
            if not target_path:
                continue
            if cached_rel_paths is not None:
                if is_directory:
                    prefix = target_path.rstrip("/") + "/"
                    if not any(path.startswith(prefix) for path in cached_rel_paths):
                        continue
                elif target_path not in cached_rel_paths:
                    continue
            target = f"dir:{target_path}" if is_directory else f"file:{target_path}"
            nodes.setdefault(
                target,
                {
                    "id": target,
                    "label": target_path + ("/" if is_directory else ""),
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
            if is_directory:
                directory = repo_root / target_path
                for child in sorted(directory.iterdir()):
                    if not child.is_file() or child.suffix not in {".md", ".jsonl", ".py"}:
                        continue
                    child_path = rel(child, repo_root)
                    if cached_rel_paths is not None and child_path not in cached_rel_paths:
                        continue
                    child_target = f"file:{child_path}"
                    nodes.setdefault(
                        child_target,
                        {
                            "id": child_target,
                            "label": child_path,
                            "kind": node_kind(child_target),
                            "path": child_path,
                        },
                    )
                    child_key = (target, child_target, "directory-contains", target_path)
                    if child_key in seen_edges:
                        continue
                    seen_edges.add(child_key)
                    edges.append(
                        {
                            "source": target,
                            "target": child_target,
                            "type": "directory-contains",
                            "from_file": target_path,
                            "raw_ref": target_path,
                        }
                    )

    ir_nodes = [
        GraphNode(
            id=node["id"],
            label=node["label"],
            kind=node.get("kind", ""),
            path=node.get("path", ""),
        ).as_dict()
        for node in nodes.values()
    ]
    ir_edges = [
        GraphEdge(
            source=edge["source"],
            target=edge["target"],
            type=edge["type"],
            metadata={"from_file": edge["from_file"], "raw_ref": edge["raw_ref"]},
        ).as_dict()
        for edge in edges
    ]
    counts = {
        "nodes": len(nodes),
        "edges": len(edges),
        "scanned_files": len(files),
        "unresolved_refs": len(unresolved),
        "node_kinds": node_kind_counts(ir_nodes),
        "edge_types": edge_counts(ir_edges),
    }
    return GraphBundle(
        nodes=sorted(ir_nodes, key=lambda node: (node["kind"], node["label"])),
        edges=sorted(ir_edges, key=lambda edge: (edge["source"], edge["target"], edge["type"], edge["from_file"])),
        generated_at=utc_timestamp(),
        counts=counts,
        extras={"unresolved_refs": sorted(unresolved, key=lambda item: (item["source"], item["raw_ref"]))[:200]},
    ).as_dict()


def local_doc_paths(repo_root: Path) -> list[str]:
    docs = [
        rel(path, repo_root)
        for path in (repo_root / "docs").rglob("*")
        if path.is_file() and path.suffix in {".md", ".jsonl", ".py"} and not ignored_prefix(rel(path, repo_root))
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
    harness_math = "docs/fundamentals/harness-algebra.md"

    top_docs = [["Doc", "All refs", "Skill refs"]]
    for path, count in inbound.most_common(20):
        top_docs.append([f"`{path}`", str(count), str(skill_inbound[path])])

    specs = [["Spec", "All refs", "Skill refs", "Suggested status"]]
    for path in sorted(spec_paths):
        specs.append([f"`{path}`", str(inbound[path]), str(skill_inbound[path]), "keep active"])

    global_bundle = [["Doc", "Why"]]
    for path in [
        "docs/fundamentals/harness-algebra.md",
        "docs/fundamentals/harness-engineering-doctrine.md",
        "docs/specs/self-improvement-contracts.md",
        "docs/specs/invocation-and-adapters.md",
        "docs/skills/README.md",
        "docs/skills/system.md",
        "docs/skills/best-practices.md",
        "docs/review/rubrics/review-rubric-index.md",
        "docs/review/rubrics/reviewer-handoff.md",
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

1. Reduce unresolved local-looking refs that point to missing active surfaces,
   especially template-era `docs/progress.md` and old external repo paths.
2. Keep `docs/review/rubrics/*` as canonical docs even when individual family
   files are primarily reached through the directory and rubric index.
3. Move temporary research and speculative notes to tickets, experiments, or
   `tmp/**`; keep tracked docs for live contracts and generated inventories.
4. Use this report before deleting or moving docs: redirect active inbound refs
   first, then remove the superseded file.
"""


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--repo-root", default=".")
    parser.add_argument("--out", default="skills/skill-maintenance/graph/harness-graph.json")
    parser.add_argument("--js-out", default="skills/skill-maintenance/graph/harness-graph.js")
    parser.add_argument("--report-out", default="docs/doc-audit/generated/doc-reference-report.md")
    parser.add_argument("--projection", default="harness-reference", help="projection profile name")
    args = parser.parse_args()

    config = get_projection_config(args.projection)
    if config.output_schema != "harness_graph":
        raise SystemExit(f"{args.projection} is not a harness graph projection")

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
