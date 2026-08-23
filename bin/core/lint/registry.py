"""The one authoritative registry for Farplane's pure static contracts."""

from __future__ import annotations

from fnmatch import fnmatchcase
import sys

from .models import LintContext, LintResult, LintScope, LintSpec
from .source import lint_source_syntax


class LintRegistry:
    """Reject duplicate checks and select contracts by public scope and paths."""

    def __init__(self, specs: tuple[LintSpec, ...]) -> None:
        self._specs = tuple(sorted(specs, key=lambda spec: spec.check_id))
        ids = [spec.check_id for spec in self._specs]
        if len(ids) != len(set(ids)):
            raise ValueError("duplicate lint check id")

    def specs(self) -> tuple[LintSpec, ...]:
        return self._specs

    def select(self, *, scope: str, changed_paths: tuple[str, ...] | None) -> tuple[LintSpec, ...]:
        if scope == "all":
            scopes = {"skills", "docs", "evals", "project", "tickets"}
        elif scope in {"skills", "docs", "evals", "project"}:
            scopes = {scope}
        else:
            raise ValueError(f"unknown lint scope: {scope}")
        selected: list[LintSpec] = []
        for spec in self._specs:
            if not spec.scopes & scopes:
                continue
            if changed_paths is not None and not spec.always_on_changed:
                if not any(
                    fnmatchcase(path, pattern)
                    for path in changed_paths
                    for pattern in spec.path_globs
                ):
                    continue
            selected.append(spec)
        return tuple(selected)


def _command(path: str, *arguments: str):
    def build(context: LintContext) -> tuple[str, ...]:
        return (sys.executable, str(context.root / path), *arguments)

    return build


def _source_syntax(context: LintContext) -> LintResult:
    errors = lint_source_syntax(context.root, changed=context.changed, base=context.base)
    return LintResult(
        "source_yaml_json_syntax",
        not errors,
        "\n".join(errors) or f"source YAML/JSON syntax OK",
    )


def _check(
    check_id: str,
    scopes: frozenset[LintScope],
    path_globs: tuple[str, ...],
    script: str,
    *arguments: str,
) -> LintSpec:
    return LintSpec(
        check_id,
        scopes,
        path_globs,
        command=_command(script, *arguments),
    )


def build_registry() -> LintRegistry:
    """Return every repository-wide pure static check exactly once."""

    shared_lint_paths = (
        "bin/core/lint/**",
        "bin/core/farplane_lint.py",
        "bin/core/farplane_cli_parser.py",
        "bin/farplane.py",
    )
    skill_paths = (
        "skills/**",
        "docs/skills/**",
        "bin/core/skill_contract.py",
        "bin/validators/check_skill_*.py",
        "bin/validators/sync_skill_registry.py",
        "rules/skill-*.toml",
        *shared_lint_paths,
    )
    doc_paths = (
        "docs/**",
        "templates/**",
        "rules/template-*.toml",
        "bin/validators/check_doc_*.py",
        "bin/validators/check_template_version_metadata.py",
        "bin/validators/sync_template_registry.py",
        "docs/features/validate_features.py",
        "docs/sources/validate_sources.py",
        *shared_lint_paths,
    )
    eval_paths = (
        "skills/**/evals/**",
        "bin/core/eval_contract.py",
        "bin/validators/check_eval_contract.py",
        "skills/eval/**",
        *shared_lint_paths,
    )
    project_paths = (
        "AGENTS.md",
        "farplane/**",
        "agents/**",
        "rules/**",
        "templates/global/**",
        "bin/**",
        "docs/systems/**",
        "tickets/templates/**",
        *shared_lint_paths,
    )
    return LintRegistry(
        (
            LintSpec(
                "source_yaml_json_syntax",
                frozenset({"project"}),
                ("*.json", "*.yaml", "*.yml", "**/*.json", "**/*.yaml", "**/*.yml"),
                run=_source_syntax,
                always_on_changed=True,
            ),
            _check(
                "skill_checklists",
                frozenset({"skills"}),
                skill_paths,
                "skills/skill-maintenance/scripts/sync_skill_checklists.py",
                "--repo",
                ".",
            ),
            _check("skill_registry", frozenset({"skills"}), skill_paths, "bin/validators/sync_skill_registry.py", "--check"),
            _check("skill_contract", frozenset({"skills"}), skill_paths, "bin/validators/check_skill_frontmatter.py", "--root", "."),
            _check("skill_todo_tiers", frozenset({"skills"}), skill_paths, "bin/validators/check_skill_todo_tiers.py", "--allow-peer-tier3"),
            _check("skill_phase_protocol", frozenset({"skills"}), skill_paths, "bin/validators/check_tier0_phase_protocol.py"),
            _check("skill_surface_budget", frozenset({"skills"}), skill_paths, "bin/validators/check_skill_surface_budget.py", "--root", "."),
            _check("skill_capabilities", frozenset({"skills"}), skill_paths, "bin/validators/check_skill_capabilities.py", "validate"),
            _check("skill_method_references", frozenset({"skills"}), skill_paths, "skills/skill-maintenance/scripts/check_skills.py", "--method-reference-contract"),
            _check("eval_contract", frozenset({"skills", "evals"}), eval_paths, "bin/validators/check_eval_contract.py", "--root", ".", "--check-schema"),
            _check("eval_query_hygiene", frozenset({"skills"}), eval_paths, "skills/eval/scripts/check_eval_queries.py", "--root", "."),
            _check("document_frontmatter", frozenset({"docs"}), doc_paths, "bin/validators/check_doc_frontmatter.py", "--root", "."),
            _check("document_refs", frozenset({"docs", "skills"}), doc_paths, "bin/validators/check_doc_refs.py", "--root", "."),
            _check("document_parity", frozenset({"docs"}), doc_paths, "bin/validators/check_doc_parity.py", "--root", "."),
            _check("feature_and_system_records", frozenset({"docs"}), doc_paths, "docs/features/validate_features.py"),
            _check("source_registry", frozenset({"docs"}), doc_paths, "docs/sources/validate_sources.py"),
            _check("template_registry", frozenset({"docs", "skills"}), doc_paths, "bin/validators/sync_template_registry.py", "--root", ".", "--check"),
            _check("template_metadata", frozenset({"docs"}), doc_paths, "bin/validators/check_template_version_metadata.py", "--root", ".", "--all"),
            _check("project_contract", frozenset({"project"}), project_paths, "bin/validators/check_farplane_project_files.py", "--root", "."),
            _check("capability_profiles", frozenset({"project"}), project_paths, "bin/validators/check_capability_profiles.py", "--project-root", "."),
            _check("harness_invariants", frozenset({"project"}), project_paths, "bin/validators/check_harness_invariants.py", "--root", ".", "--skip-project-contract"),
            _check("ticket_metadata", frozenset({"tickets"}), ("tickets/**",), "tickets/scripts/check_ticket_metadata.py"),
        )
    )
