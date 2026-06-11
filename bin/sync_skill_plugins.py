#!/usr/bin/env python3
"""Generate one Codex plugin package per Farplane skill."""

from __future__ import annotations

import argparse
import json
import shutil
import sys
from dataclasses import dataclass
from pathlib import Path
from typing import Sequence

BIN_DIR = Path(__file__).resolve().parent
if str(BIN_DIR) not in sys.path:
    sys.path.insert(0, str(BIN_DIR))

from install_selected_skills import Skill, discover_skills


MARKER = ".farplane-skill-plugin"
MARKETPLACE_PATH = Path(".agents/plugins/marketplace.json")
PLUGIN_ROOT = Path("plugins")
DEFAULT_OUTPUT_ROOT = Path(".farplane/generated/skill-plugins")
LOCAL_PLUGIN_ROOT = Path(".codex/plugins/farplane")
PERSONAL_MARKETPLACE_PATH = Path(".agents/plugins/marketplace.json")
PLUGIN_VERSION = "0.1.0"


@dataclass(frozen=True)
class SkillPlugin:
    name: str
    skills: tuple[Skill, ...]
    display_name: str
    description: str
    keywords: tuple[str, ...]


GROUP_DEFINITIONS: tuple[dict[str, object], ...] = (
    {
        "name": "farplane-core",
        "display_name": "Farplane Core",
        "description": "Core reasoning skills plus compatibility phase wrappers and review protocol.",
        "skills": (
            "advise",
            "reference-grounding",
            "prototyping",
            "research",
            "plan",
            "execute",
            "review",
            "brainstorm",
            "documentation",
            "external-patterns",
        ),
        "keywords": ("core", "planning", "review"),
    },
    {
        "name": "farplane-coding-workflow",
        "display_name": "Farplane Coding Workflow",
        "description": "Ticket, implementation, QA, review, and closeout workflow skills.",
        "skills": (
            "deep-init-project",
            "prd",
            "spec-to-ticket",
            "impl-plan",
            "impl",
            "qa",
            "demo",
            "close-ticket",
            "ralph",
            "work",
            "goal-crafter",
            "runtime-debugging",
            "agent-qa-test",
            "testing",
            "codebase-analysis",
            "commit-message",
        ),
        "keywords": ("coding", "tickets", "qa"),
    },
    {
        "name": "farplane-frontend",
        "display_name": "Farplane Frontend",
        "description": "Frontend, product UI, visual design, landing page, and visual QA skills.",
        "skills": (
            "frontend-craft",
            "functional-ui",
            "visual-design",
            "landing-page",
            "frontend-design",
            "visual-qa",
            "web-design-guidelines",
            "vercel-react-best-practices",
            "data-viz",
            "react-flow",
            "delegate-frontend",
            "deep-ui-design",
        ),
        "keywords": ("frontend", "ui", "design"),
    },
    {
        "name": "farplane-research",
        "display_name": "Farplane Research",
        "description": "Research, source ingestion, synthesis, scouting, and summarization skills.",
        "skills": (
            "research",
            "best-of-worlds",
            "harness-scout",
            "feed-scout",
            "media-ingest",
            "video-understanding",
            "summarize",
            "apify",
            "documentation",
            "external-patterns",
            "find-skills",
        ),
        "keywords": ("research", "sources", "synthesis"),
    },
    {
        "name": "farplane-media-content",
        "display_name": "Farplane Media and Content",
        "description": "Image, video, Remotion, social, product photography, and content production skills.",
        "skills": (
            "image-generation",
            "video-generation",
            "remotion",
            "remotion-render",
            "video-production",
            "social-content",
            "reel-collage",
            "product-photography",
            "data-viz",
        ),
        "keywords": ("media", "content", "generation"),
    },
    {
        "name": "farplane-harness-engineering",
        "display_name": "Farplane Harness Engineering",
        "description": "Harness improvement, skill maintenance, delegation, invocation, and self-improvement skills.",
        "skills": (
            "harness-advisor",
            "skill-maintenance",
            "skill-creator",
            "skill-registry-ui",
            "agent-behavior-test",
            "agent-testability-plan",
            "farplane-invocation",
            "delegate-cli",
            "autoresearch-plan",
            "autoresearch-exec",
            "self-improve",
            "desloppify",
            "diagramming",
            "coderabbit-review",
        ),
        "keywords": ("harness", "skills", "maintenance"),
    },
)

GROUP_PLUGIN_NAMES = frozenset(str(definition["name"]) for definition in GROUP_DEFINITIONS)


@dataclass(frozen=True)
class SyncResult:
    plugin_count: int
    bundle_count: int
    skill_count: int
    marketplace_path: Path
    plugins_dir: Path
    changed: bool


def display_name(name: str) -> str:
    return " ".join(part.capitalize() for part in name.replace("_", "-").split("-"))


def truncate(text: str, limit: int) -> str:
    collapsed = " ".join(text.split())
    if len(collapsed) <= limit:
        return collapsed
    return collapsed[: limit - 3].rstrip() + "..."


def default_prompt(skill: Skill) -> str:
    prompt = f"Use {skill.name} for this task."
    return truncate(prompt, 128)


def render_manifest(plugin: SkillPlugin) -> dict[str, object]:
    short_description = truncate(plugin.description, 120)
    return {
        "name": plugin.name,
        "version": PLUGIN_VERSION,
        "description": short_description,
        "author": {"name": "Farplane"},
        "license": "MIT",
        "keywords": ["farplane", "skill", *plugin.keywords],
        "skills": "./skills/",
        "interface": {
            "displayName": plugin.display_name,
            "shortDescription": short_description,
            "longDescription": plugin.description,
            "developerName": "Farplane",
            "category": "Productivity",
            "capabilities": ["Skills"],
            "defaultPrompt": [truncate(f"Use {plugin.name} for this task.", 128)],
        },
    }


def single_skill_plugin(skill: Skill) -> SkillPlugin:
    description = skill.description or f"Use the {skill.name} skill."
    keywords = tuple(value for value in (skill.source, skill.tier) if value)
    return SkillPlugin(
        name=skill.name,
        skills=(skill,),
        display_name=display_name(skill.name),
        description=description,
        keywords=keywords,
    )


def group_plugins(skills: Sequence[Skill]) -> list[SkillPlugin]:
    by_name = {skill.name: skill for skill in skills}
    plugins: list[SkillPlugin] = []
    for definition in GROUP_DEFINITIONS:
        requested = tuple(definition["skills"])  # type: ignore[arg-type]
        members = tuple(by_name[name] for name in requested if name in by_name)
        if not members:
            continue
        plugins.append(
            SkillPlugin(
                name=str(definition["name"]),
                skills=members,
                display_name=str(definition["display_name"]),
                description=str(definition["description"]),
                keywords=tuple(str(value) for value in definition["keywords"]),  # type: ignore[arg-type]
            )
        )
    return plugins


def build_plugins(skills: Sequence[Skill]) -> list[SkillPlugin]:
    bundles = group_plugins(skills)
    return [*bundles, *(single_skill_plugin(skill) for skill in skills)]


def parse_plugin_names(raw: str | None, repeated: Sequence[str] | None) -> list[str]:
    values: list[str] = []
    if raw:
        values.extend(raw.split(","))
    if repeated:
        for item in repeated:
            values.extend(item.split(","))
    return sorted(dict.fromkeys(value.strip() for value in values if value.strip()))


def select_plugins(
    plugins: Sequence[SkillPlugin],
    selected_names: Sequence[str] | None,
) -> list[SkillPlugin]:
    if not selected_names:
        return list(plugins)

    by_name = {plugin.name: plugin for plugin in plugins}
    missing = [name for name in selected_names if name not in by_name]
    if missing:
        known = ", ".join(sorted(by_name))
        raise ValueError(
            f"Unknown plugin(s): {', '.join(missing)}\nKnown plugins: {known}"
        )
    return [by_name[name] for name in selected_names]


def plugin_listing(plugins: Sequence[SkillPlugin]) -> str:
    bundles = [plugin for plugin in plugins if plugin.name in GROUP_PLUGIN_NAMES]
    individuals = [plugin for plugin in plugins if plugin.name not in GROUP_PLUGIN_NAMES]
    lines = ["Bundle plugins:"]
    lines.extend(f"- {plugin.name}: {plugin.description}" for plugin in bundles)
    lines.append("")
    lines.append("Individual skill plugins:")
    lines.extend(f"- {plugin.name}: {plugin.description}" for plugin in individuals)
    return "\n".join(lines)


def render_marketplace(
    plugins: Sequence[SkillPlugin],
    source_base_path: str = "./plugins",
) -> dict[str, object]:
    return {
        "name": "farplane-skills",
        "interface": {"displayName": "Farplane Skills"},
        "plugins": [
            {
                "name": plugin.name,
                "source": {
                    "source": "local",
                    "path": f"{source_base_path.rstrip('/')}/{plugin.name}",
                },
                "policy": {
                    "installation": "AVAILABLE",
                    "authentication": "ON_INSTALL",
                },
                "category": "Productivity",
            }
            for plugin in plugins
        ],
    }


def write_json(path: Path, payload: dict[str, object]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, indent=2, sort_keys=False) + "\n", encoding="utf-8")


def ignore_generated_copy(_: str, names: list[str]) -> set[str]:
    return {name for name in names if name in {"__pycache__", ".DS_Store", ".codex-plugin"}}


def copy_skill(skill: Skill, plugin_root: Path) -> None:
    skill_dest = plugin_root / "skills" / skill.name
    if skill_dest.exists():
        shutil.rmtree(skill_dest)
    skill_dest.parent.mkdir(parents=True, exist_ok=True)
    shutil.copytree(skill.path, skill_dest, ignore=ignore_generated_copy)


def copy_review_rubrics(repo: Path, plugin_root: Path) -> None:
    source = repo / "docs/review/rubrics"
    if not source.exists():
        return
    dest = plugin_root / "docs/review/rubrics"
    if dest.exists():
        shutil.rmtree(dest)
    dest.parent.mkdir(parents=True, exist_ok=True)
    shutil.copytree(source, dest, ignore=ignore_generated_copy)


def write_plugin(plugin: SkillPlugin, repo: Path, plugins_dir: Path) -> None:
    plugin_root = plugins_dir / plugin.name
    if plugin_root.exists():
        shutil.rmtree(plugin_root)
    (plugin_root / ".codex-plugin").mkdir(parents=True)
    (plugin_root / MARKER).write_text("generated by bin/sync_skill_plugins.py\n", encoding="utf-8")
    write_json(plugin_root / ".codex-plugin/plugin.json", render_manifest(plugin))
    for skill in plugin.skills:
        copy_skill(skill, plugin_root)
    if any(skill.name == "review" for skill in plugin.skills):
        copy_review_rubrics(repo, plugin_root)


def sync_skill_plugins(
    repo: Path,
    clean: bool = True,
    selected_names: Sequence[str] | None = None,
    output_root: Path | None = None,
    plugins_dir: Path | None = None,
    marketplace_path: Path | None = None,
    source_base_path: str = "./plugins",
) -> SyncResult:
    repo = repo.resolve()
    skills = discover_skills(repo / "skills")
    all_plugins = build_plugins(skills)
    selected_plugins = select_plugins(all_plugins, selected_names)
    resolved_output_root = (
        (repo / output_root).resolve()
        if output_root is not None
        else (repo / DEFAULT_OUTPUT_ROOT).resolve()
    )
    resolved_plugins_dir = (
        plugins_dir.expanduser().resolve()
        if plugins_dir is not None
        else (resolved_output_root / PLUGIN_ROOT).resolve()
    )
    resolved_marketplace_path = (
        marketplace_path.expanduser().resolve()
        if marketplace_path is not None
        else (resolved_output_root / MARKETPLACE_PATH).resolve()
    )
    expected_names = {plugin.name for plugin in all_plugins}
    changed = False

    resolved_plugins_dir.mkdir(parents=True, exist_ok=True)

    if clean:
        for child in resolved_plugins_dir.iterdir():
            if not child.is_dir() or child.name in expected_names:
                continue
            if (child / MARKER).exists():
                shutil.rmtree(child)
                changed = True

    for plugin in selected_plugins:
        if (resolved_plugins_dir / plugin.name).exists():
            changed = True
        write_plugin(plugin, repo, resolved_plugins_dir)
        changed = True

    before = (
        resolved_marketplace_path.read_text(encoding="utf-8")
        if resolved_marketplace_path.exists()
        else None
    )
    write_json(
        resolved_marketplace_path,
        render_marketplace(selected_plugins, source_base_path=source_base_path),
    )
    after = resolved_marketplace_path.read_text(encoding="utf-8")
    changed = changed or before != after

    return SyncResult(
        plugin_count=len(selected_plugins),
        bundle_count=sum(1 for plugin in selected_plugins if plugin.name in GROUP_PLUGIN_NAMES),
        skill_count=len(skills),
        marketplace_path=resolved_marketplace_path,
        plugins_dir=resolved_plugins_dir,
        changed=changed,
    )


def sync_personal_skill_plugins(
    repo: Path,
    home: Path,
    clean: bool = True,
    selected_names: Sequence[str] | None = None,
) -> SyncResult:
    home = home.expanduser().resolve()
    return sync_skill_plugins(
        repo=repo,
        clean=clean,
        selected_names=selected_names,
        plugins_dir=home / LOCAL_PLUGIN_ROOT,
        marketplace_path=home / PERSONAL_MARKETPLACE_PATH,
        source_base_path=f"./{LOCAL_PLUGIN_ROOT.as_posix()}",
    )


def check_in_sync(repo: Path) -> list[str]:
    with TemporarySync(repo) as temp_repo:
        result = sync_skill_plugins(temp_repo, clean=True)
        errors: list[str] = []
        if result.plugin_count == 0:
            errors.append("no skill plugins generated")
        if not result.marketplace_path.exists():
            errors.append("generated marketplace is missing")
        if not result.plugins_dir.exists():
            errors.append("generated plugin directory is missing")
        return errors


class TemporarySync:
    def __init__(self, repo: Path) -> None:
        self.repo = repo.resolve()
        self.tmp_root: Path | None = None

    def __enter__(self) -> Path:
        import tempfile

        self.tmp_root = Path(tempfile.mkdtemp(prefix="farplane-skill-plugins-"))
        shutil.copytree(
            self.repo / "skills",
            self.tmp_root / "skills",
            ignore=ignore_generated_copy,
        )
        review_rubrics = self.repo / "docs/review/rubrics"
        if review_rubrics.exists():
            shutil.copytree(
                review_rubrics,
                self.tmp_root / "docs/review/rubrics",
                ignore=ignore_generated_copy,
            )
        return self.tmp_root

    def __exit__(self, *_: object) -> None:
        if self.tmp_root is not None:
            shutil.rmtree(self.tmp_root)


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Generate Codex plugin packages for Farplane skills."
    )
    parser.add_argument(
        "--repo",
        type=Path,
        default=Path(__file__).resolve().parent.parent,
        help="Farplane repo root. Defaults to this script's repo.",
    )
    parser.add_argument(
        "--check",
        action="store_true",
        help="Generate plugins in a temp copy and fail if packaging is broken.",
    )
    parser.add_argument(
        "--no-clean",
        action="store_true",
        help="Do not remove stale generated plugin directories.",
    )
    parser.add_argument(
        "--list",
        action="store_true",
        help="List available bundle and individual skill plugins without writing files.",
    )
    parser.add_argument(
        "--output-root",
        type=Path,
        default=DEFAULT_OUTPUT_ROOT,
        help="Root for generated repo-local plugin output. Defaults to .farplane/generated/skill-plugins.",
    )
    parser.add_argument(
        "--install-local",
        action="store_true",
        help="Generate a personal Codex marketplace in ~/.agents and plugin copies in ~/.codex/plugins/farplane.",
    )
    parser.add_argument(
        "--home",
        type=Path,
        default=Path.home(),
        help="Home directory for --install-local. Primarily for tests.",
    )
    parser.add_argument(
        "--plugins",
        help="Comma-separated plugin names to expose in the generated marketplace.",
    )
    parser.add_argument(
        "--plugin",
        action="append",
        help="Plugin name to expose in the generated marketplace. May be repeated.",
    )
    parser.add_argument("--json", action="store_true", help="Print JSON output.")
    return parser


def main(argv: Sequence[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    repo = args.repo.resolve()
    selected_names = parse_plugin_names(args.plugins, args.plugin)

    if args.list:
        skills = discover_skills(repo / "skills")
        plugins = build_plugins(skills)
        if args.json:
            print(
                json.dumps(
                    [
                        {
                            "name": plugin.name,
                            "display_name": plugin.display_name,
                            "description": plugin.description,
                            "skills": [skill.name for skill in plugin.skills],
                            "kind": "bundle"
                            if plugin.name in GROUP_PLUGIN_NAMES
                            else "individual",
                        }
                        for plugin in plugins
                    ],
                    indent=2,
                )
            )
        else:
            print(plugin_listing(plugins))
        return 0

    if args.check:
        if selected_names:
            print("--check does not support selected marketplaces", file=sys.stderr)
            return 2
        errors = check_in_sync(repo)
        if errors:
            for error in errors:
                print(error, file=sys.stderr)
            return 1
        print("skill plugin generation ok")
        return 0

    try:
        if args.install_local:
            result = sync_personal_skill_plugins(
                repo,
                home=args.home,
                clean=not args.no_clean,
                selected_names=selected_names,
            )
        else:
            result = sync_skill_plugins(
                repo,
                clean=not args.no_clean,
                selected_names=selected_names,
                output_root=args.output_root,
            )
    except ValueError as error:
        print(error, file=sys.stderr)
        return 2
    if args.json:
        print(
            json.dumps(
                {
                    "plugin_count": result.plugin_count,
                    "bundle_count": result.bundle_count,
                    "skill_count": result.skill_count,
                    "marketplace_path": str(result.marketplace_path),
                    "plugins_dir": str(result.plugins_dir),
                    "changed": result.changed,
                    "selected_plugins": selected_names,
                },
                indent=2,
            )
        )
    else:
        print(
            f"generated {result.plugin_count} plugins "
            f"({result.bundle_count} bundles selected from {result.skill_count} skills)"
        )
        print(f"plugins: {result.plugins_dir}")
        print(f"marketplace: {result.marketplace_path}")
        if args.install_local:
            print("restart Codex, open /plugins, and choose the Farplane Skills marketplace.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
