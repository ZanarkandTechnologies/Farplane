#!/usr/bin/env python3
"""Generate a named Farplane graph projection."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

from graph_ir import normalized_for_compare, write_js, write_json
from graph_projection import project_graph
from graph_projection_config import get_projection_config, list_projection_configs


def _load_builder(module_name: str):
    return __import__(module_name)


def _check_json(path: Path, value: dict) -> list[str]:
    if not path.exists():
        return [f"{path} does not exist"]
    existing = json.loads(path.read_text())
    if normalized_for_compare(existing) != normalized_for_compare(value):
        return [f"{path} is stale; rerun generator"]
    return []


def _check_js(path: Path, global_name: str, value: dict) -> list[str]:
    from graph_ir import load_js_value

    if not path.exists():
        return [f"{path} does not exist"]
    existing = load_js_value(path, global_name)
    if normalized_for_compare(existing) != normalized_for_compare(value):
        return [f"{path} is stale; rerun generator"]
    return []


def generate_skill_projection(args: argparse.Namespace) -> tuple[dict, dict | None]:
    generator = _load_builder("generate_skill_graph")
    rows = generator.load_registry(Path(args.registry))
    graph = generator.build_graph(rows)
    docs = generator.build_docs(rows)
    return graph, docs


def generate_harness_projection(args: argparse.Namespace) -> tuple[dict, str]:
    generator = _load_builder("generate_harness_graph")
    repo_root = Path(args.repo_root).resolve()
    graph = generator.build_graph(repo_root)
    report = generator.build_report(graph, repo_root)
    return graph, report


def generate_lifecycle_projection(args: argparse.Namespace, projection: str) -> dict:
    generator = _load_builder("farplane_lifecycle_graph")
    config = get_projection_config(projection)
    repo_root = Path(args.repo_root).resolve()
    graph = generator.build_graph(
        repo_root,
        include_gates=args.full or "gates" in config.optional_nodes,
        include_abstract_state=args.full or "abstract_state" in config.optional_nodes,
        include_fsa_nodes=args.full or "fsa_state_nodes" in config.optional_nodes,
    )
    errors = generator.validate_graph(graph)
    if errors:
        raise SystemExit("\n".join(errors))
    return graph


def list_profiles() -> int:
    for config in list_projection_configs():
        print(f"{config.name}\t{config.output_schema}\t{config.description}")
    return 0


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--projection", help="projection profile name")
    parser.add_argument("--list", action="store_true", help="list known projection profiles")
    parser.add_argument("--repo-root", default=".")
    parser.add_argument("--registry", default="docs/skills/registry.jsonl")
    parser.add_argument("--out")
    parser.add_argument("--js-out")
    parser.add_argument("--docs-out")
    parser.add_argument("--docs-js-out")
    parser.add_argument("--report-out")
    parser.add_argument("--check", action="store_true", help="check generated output against on-disk artifacts")
    parser.add_argument("--full", action="store_true", help="include all optional lifecycle nodes")
    args = parser.parse_args()

    if args.list:
        return list_profiles()
    if not args.projection:
        parser.error("--projection is required unless --list is used")

    config = get_projection_config(args.projection)
    repo_root = Path(args.repo_root).resolve()
    out_path = repo_root / (args.out or config.default_out)
    js_out = args.js_out if args.js_out is not None else config.default_js_out
    js_path = repo_root / js_out if js_out else None

    if config.output_schema == "skill_graph":
        graph, docs = generate_skill_projection(args)
        graph = project_graph(graph, config)
        docs_out = repo_root / (args.docs_out or config.docs_out)
        docs_js_out = args.docs_js_out if args.docs_js_out is not None else config.docs_js_out
        docs_js_path = repo_root / docs_js_out if docs_js_out else None
        if args.check:
            errors = _check_json(out_path, graph)
            if js_path:
                errors.extend(_check_js(js_path, config.js_global, graph))
            errors.extend(_check_json(docs_out, docs))
            if docs_js_path:
                errors.extend(_check_js(docs_js_path, config.docs_js_global, docs))
            if errors:
                print("\n".join(errors), file=sys.stderr)
                return 1
            print(f"{config.name} OK ({graph['counts']['nodes']} nodes, {graph['counts']['edges']} edges)")
            return 0
        write_json(out_path, graph)
        if js_path:
            write_js(js_path, config.js_global, graph)
        write_json(docs_out, docs)
        if docs_js_path:
            write_js(docs_js_path, config.docs_js_global, docs)
        print(f"wrote {out_path} and {docs_out}")
        return 0

    if config.output_schema == "harness_graph":
        graph, report = generate_harness_projection(args)
        graph = project_graph(graph, config)
        report_out = repo_root / (args.report_out or config.report_out)
        if args.check:
            errors = _check_json(out_path, graph)
            if js_path:
                errors.extend(_check_js(js_path, config.js_global, graph))
            if errors:
                print("\n".join(errors), file=sys.stderr)
                return 1
            print(f"{config.name} OK ({graph['counts']['nodes']} nodes, {graph['counts']['edges']} edges)")
            return 0
        write_json(out_path, graph)
        if js_path:
            write_js(js_path, config.js_global, graph)
        report_out.parent.mkdir(parents=True, exist_ok=True)
        report_out.write_text(report)
        print(f"wrote {out_path} and {report_out}")
        return 0

    if config.output_schema == "lifecycle_graph":
        graph = generate_lifecycle_projection(args, config.name)
        graph = project_graph(graph, config)
        if args.check:
            errors = _check_json(out_path, graph)
            if js_path:
                errors.extend(_check_js(js_path, config.js_global, graph))
            if errors:
                print("\n".join(errors), file=sys.stderr)
                return 1
            print(f"{config.name} OK ({graph['counts']['nodes']} nodes, {graph['counts']['edges']} edges)")
            return 0
        write_json(out_path, graph)
        if js_path:
            write_js(js_path, config.js_global, graph)
        print(f"wrote {out_path}")
        return 0

    raise SystemExit(f"unsupported projection schema: {config.output_schema}")


if __name__ == "__main__":
    raise SystemExit(main())
