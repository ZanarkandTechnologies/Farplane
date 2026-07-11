import json
from pathlib import Path

from bin.validators.check_farplane_project_files import validate

RETIRED_INTEGRATIONS_REF = "farplane/" + "integrations.md"


def write_framework_manifest(farplane: Path) -> None:
    (farplane / "manifest.json").write_text(
        json.dumps(
            {
                "schema": "farplane_project",
                "spec_version": "1.1.0",
                "template_uses": {
                    "farplane-framework": "1.2.0",
                },
                "project": {
                    "name": "Test Project",
                    "description": "Test project description.",
                    "archetype": "test_project",
                },
                "standard": {
                    "tracked": [
                        "AGENTS.md",
                        "PROJECT_RULES.md",
                        "ARCHITECTURE.md",
                        "farplane/README.md",
                        "farplane/manifest.json",
                        "farplane/harness.md",
                        "farplane/goals.yaml",
                        "farplane/metrics.yaml",
                        "farplane/automations.toml",
                        "farplane/bindings.yaml",
                        ".agents/skills/README.md",
                        "tickets/templates/ticket.md",
                    ],
                    "ignored": [".farplane/project/ui/"],
                },
                "optional": {
                    "tracked": ["farplane/hooks.json", "farplane/pm.json"],
                    "ignored": [],
                },
            }
        ),
        encoding="utf-8",
    )


def write_automations_toml(farplane: Path) -> None:
    (farplane / "automations.toml").write_text(
        '''schema = "farplane_project_automations"
framework_template_version = "1.0.0"
updated_at = "2026-07-02"
owner = "automation-advisor"

[[automations]]
id = "project-pulse"
name = "Project Pulse"
kind = "heartbeat"
status = "active"
prompt = """
Use $pulse-update.

Params:
project_root = "/tmp/project"
"""

[automations.target]
thread_id = "thread-123"

[automations.schedule]
type = "interval"
interval_minutes = 30
''',
        encoding="utf-8",
    )


def write_required_project_files(root: Path) -> None:
    farplane = root / "farplane"
    for path in ("AGENTS.md", "PROJECT_RULES.md", "ARCHITECTURE.md"):
        (root / path).write_text(f"# {path}\n", encoding="utf-8")

    for name in ("README.md",):
        (farplane / name).write_text(
            "---\nframework_template_version: \"0.1.0\"\n---\n\n# Test\n",
            encoding="utf-8",
        )
    (farplane / "goals.yaml").write_text(
        'kind: project-goals\nframework_template_version: "0.1.0"\ngoals: {}\n',
        encoding="utf-8",
    )
    (farplane / "metrics.yaml").write_text(
        'kind: project-metrics\nframework_template_version: "0.1.0"\nmetrics: {}\n',
        encoding="utf-8",
    )
    (farplane / "hooks.json").write_text('{"version": 1, "hooks": {}}\n', encoding="utf-8")
    skills_dir = root / ".agents" / "skills"
    skills_dir.mkdir(parents=True)
    (skills_dir / "README.md").write_text(
        "---\nkind: local-capability-skills-index\nframework_template_version: \"0.1.0\"\n---\n\n# Local Capability Skills\n",
        encoding="utf-8",
    )
    (farplane / "harness.md").write_text(
        """---
kind: project-harness
framework_template_version: "0.2.0"
---

# Test Harness

## Mission

Test mission.

## Human Thesis

Test thesis.

## Operating Principles

- Prefer visible artifacts.

## Static Leverage Commitments

| Commitment | Why It Compounds | Evidence To Seek | Pivot Signal |
| --- | --- | --- | --- |
| Test | compounds | evidence | pivot |

## Non-Tradeoffs

- Do not silently rewrite the thesis.

## Agent Authority

- Agents may propose charter deltas.

## Change Rule

Static charter changes require approval.

## Allocation Guardrails

| Guardrail | Rule |
| --- | --- |
| Proof | Keep proof work nonzero. |
""",
        encoding="utf-8",
    )
    (farplane / "bindings.yaml").write_text(
        'kind: project-bindings\nframework_template_version: "0.1.0"\nproject: {}\nmetric_bindings: {}\n',
        encoding="utf-8",
    )
    write_automations_toml(farplane)
    tickets = root / "tickets" / "templates"
    tickets.mkdir(parents=True)
    (tickets / "ticket.md").write_text("# Ticket\n", encoding="utf-8")
    state = root / ".farplane" / "state"
    state.mkdir(parents=True)
    (state / "run-ledger.json").write_text("{\"runs\": []}\n", encoding="utf-8")
    (root / ".farplane" / "project" / "ui").mkdir(parents=True)


def test_missing_automations_file_fails(tmp_path: Path) -> None:
    farplane = tmp_path / "farplane"
    farplane.mkdir()
    write_framework_manifest(farplane)

    errors = validate(tmp_path)

    assert "farplane/automations.toml is required for full Codex automation configs." in errors


def test_missing_metrics_file_fails(tmp_path: Path) -> None:
    farplane = tmp_path / "farplane"
    farplane.mkdir()
    write_framework_manifest(farplane)
    write_required_project_files(tmp_path)
    (farplane / "metrics.yaml").unlink()

    errors = validate(tmp_path)

    assert "farplane/metrics.yaml is required for project metric definitions." in errors


def test_malformed_automations_toml_fails(tmp_path: Path) -> None:
    farplane = tmp_path / "farplane"
    farplane.mkdir()
    write_framework_manifest(farplane)
    write_required_project_files(tmp_path)
    (farplane / "automations.toml").write_text(
        '''schema = "farplane_project_automations"
framework_template_version = "1.0.0"

[[automations]]
id = "project-pulse"
name = "Project Pulse"
kind = "heartbeat"
status = "active"
last_run_at = "2026-07-02T00:00:00Z"
[automations.schedule]
type = "interval"
''',
        encoding="utf-8",
    )

    errors = validate(tmp_path)

    assert "farplane/automations.toml automations[1].prompt must be a non-empty string." in errors
    assert "farplane/automations.toml automations[1].target must be a table with workspace or thread_id." in errors
    assert "farplane/automations.toml automations[1].schedule.interval_minutes must be an integer." in errors
    assert "farplane/automations.toml automations[1] must not store runtime state keys: last_run_at." in errors


def test_retired_product_files_fail(tmp_path: Path) -> None:
    farplane = tmp_path / "farplane"
    farplane.mkdir()
    write_framework_manifest(farplane)
    write_required_project_files(tmp_path)
    (farplane / "products.json").write_text("{}\n", encoding="utf-8")
    (farplane / "products").mkdir()

    errors = validate(tmp_path)

    assert "farplane/products.json is retired; metrics, goals, and tickets are the project primitives." in errors
    assert "farplane/products/ is retired; keep reusable artifact workflows as skills." in errors


def test_missing_harness_file_fails(tmp_path: Path) -> None:
    farplane = tmp_path / "farplane"
    farplane.mkdir()
    write_framework_manifest(farplane)
    write_required_project_files(tmp_path)
    (farplane / "harness.md").unlink()

    errors = validate(tmp_path)

    assert "farplane/harness.md is required for the static human charter." in errors


def test_malformed_harness_file_fails(tmp_path: Path) -> None:
    farplane = tmp_path / "farplane"
    farplane.mkdir()
    write_framework_manifest(farplane)
    write_required_project_files(tmp_path)
    (farplane / "harness.md").write_text(
        "---\nframework_template_version: \"0.1.0\"\n---\n\n# Harness\n\n## Human Thesis\n",
        encoding="utf-8",
    )

    errors = validate(tmp_path)

    assert "farplane/harness.md must use front matter kind: project-harness." in errors
    assert any(error.startswith("farplane/harness.md missing required static-charter headings:") for error in errors)


def test_harness_program_dsl_fails(tmp_path: Path) -> None:
    farplane = tmp_path / "farplane"
    farplane.mkdir()
    write_framework_manifest(farplane)
    write_required_project_files(tmp_path)
    with (farplane / "harness.md").open("a", encoding="utf-8") as handle:
        handle.write("\n```harness-program\nproject \"Legacy\" {}\n```\n")

    errors = validate(tmp_path)

    assert (
        "farplane/harness.md must not use fenced harness-program DSL; "
        "use YAML front matter plus Markdown charter sections."
    ) in errors


def test_duplicate_project_charter_fails(tmp_path: Path) -> None:
    farplane = tmp_path / "farplane"
    farplane.mkdir()
    write_framework_manifest(farplane)
    write_required_project_files(tmp_path)
    (farplane / "project.md").write_text("---\nframework_template_version: \"0.1.0\"\n---\n", encoding="utf-8")

    errors = validate(tmp_path)

    assert (
        "farplane/project.md would duplicate the active static charter; use farplane/harness.md "
        "unless a versioned framework migration replaces it."
    ) in errors


def test_retired_integrations_file_fails(tmp_path: Path) -> None:
    farplane = tmp_path / "farplane"
    farplane.mkdir()
    write_framework_manifest(farplane)
    write_automations_toml(farplane)
    (farplane / "bindings.yaml").write_text(
        'kind: project-bindings\nframework_template_version: "0.1.0"\nproject: {}\n',
        encoding="utf-8",
    )
    (farplane / "integrations.md").write_text("# old\n", encoding="utf-8")

    errors = validate(tmp_path)

    assert f"{RETIRED_INTEGRATIONS_REF} is retired; use farplane/bindings.yaml." in errors


def test_retired_bindings_markdown_fails(tmp_path: Path) -> None:
    farplane = tmp_path / "farplane"
    farplane.mkdir()
    write_framework_manifest(farplane)
    write_required_project_files(tmp_path)
    (farplane / "bindings.md").write_text("# old bindings\n", encoding="utf-8")

    errors = validate(tmp_path)

    assert "farplane/bindings.md is retired; use farplane/bindings.yaml." in errors


def test_retired_steer_files_fail(tmp_path: Path) -> None:
    farplane = tmp_path / "farplane"
    farplane.mkdir()
    write_framework_manifest(farplane)
    write_required_project_files(tmp_path)
    (farplane / "steer.config.toml").write_text("schema = \"farplane_steer_config\"\n", encoding="utf-8")
    state = tmp_path / ".farplane" / "state"
    state.mkdir(parents=True, exist_ok=True)
    (state / "steer-scheduler.json").write_text("{\"jobs\": {}}\n", encoding="utf-8")

    errors = validate(tmp_path)

    assert "farplane/steer.config.toml is retired; use farplane/automations.toml." in errors
    assert ".farplane/state/steer-scheduler.json is retired; Codex automation cadence owns scheduling." in errors


def test_automations_require_exactly_one_pulse_heartbeat(tmp_path: Path) -> None:
    farplane = tmp_path / "farplane"
    farplane.mkdir()
    write_framework_manifest(farplane)
    write_required_project_files(tmp_path)
    with (farplane / "automations.toml").open("a", encoding="utf-8") as handle:
        handle.write(
            '''

[[automations]]
id = "second-heartbeat"
name = "Second Heartbeat"
kind = "heartbeat"
status = "active"
prompt = "Use $dogfood-review."
[automations.target]
workspace = "/tmp/project"
[automations.schedule]
type = "interval"
interval_minutes = 60
'''
        )

    errors = validate(tmp_path)

    assert "farplane/automations.toml must define exactly one heartbeat record for Work Pulse; found 2." in errors


def test_retired_file_growth_hook_config_fails(tmp_path: Path) -> None:
    farplane = tmp_path / "farplane"
    farplane.mkdir()
    write_framework_manifest(farplane)
    write_required_project_files(tmp_path)
    (farplane / "file-growth-hook.json").write_text("{}\n", encoding="utf-8")

    errors = validate(tmp_path)

    assert (
        "farplane/file-growth-hook.json is retired; use the deterministic changed-file gate in "
        "rules/git-review-gates.toml."
    ) in errors


def test_valid_versioned_files_pass(tmp_path: Path) -> None:
    farplane = tmp_path / "farplane"
    farplane.mkdir()
    write_framework_manifest(farplane)
    write_required_project_files(tmp_path)

    assert validate(tmp_path) == []


def test_goal_kpi_without_metric_recipe_fails(tmp_path: Path) -> None:
    farplane = tmp_path / "farplane"
    farplane.mkdir()
    write_framework_manifest(farplane)
    write_required_project_files(tmp_path)
    (farplane / "goals.yaml").write_text(
        """kind: project-goals
framework_template_version: "0.1.0"
goals:
  test_axis:
    smart_goals:
      - id: missing_recipe
        kpis:
          - id: unknown_metric
""",
        encoding="utf-8",
    )

    errors = validate(tmp_path)

    assert "farplane/goals.yaml KPI ids lack metrics.yaml definitions: unknown_metric." in errors


def test_goal_product_refs_are_retired(tmp_path: Path) -> None:
    farplane = tmp_path / "farplane"
    farplane.mkdir()
    write_framework_manifest(farplane)
    write_required_project_files(tmp_path)
    (farplane / "goals.yaml").write_text(
        """kind: project-goals
framework_template_version: "0.1.0"
goals:
  test_axis:
    smart_goals:
      - id: direct_kpi_goal
        product_refs: [old_product]
""",
        encoding="utf-8",
    )

    errors = validate(tmp_path)

    assert (
        "farplane/goals.yaml goals.test_axis.smart_goals.0.product_refs is retired; goals point directly to KPI ids."
        in errors
    )


def test_metric_product_owner_is_retired(tmp_path: Path) -> None:
    farplane = tmp_path / "farplane"
    farplane.mkdir()
    write_framework_manifest(farplane)
    write_required_project_files(tmp_path)
    (farplane / "metrics.yaml").write_text(
        """kind: project-metrics
framework_template_version: "0.1.0"
metrics:
  accepted_harness_improvements:
    label: Accepted harness improvements
    description: Accepted improvements with ticket proof.
    product: old_product
    kind: daily_count
    unit: improvements
    display: bar_plus_cumulative
""",
        encoding="utf-8",
    )
    (farplane / "bindings.yaml").write_text(
        """kind: project-bindings
framework_template_version: "0.1.0"
project: {}
metric_bindings:
  accepted_harness_improvements:
    refresh: Count ticket Reward rows.
""",
        encoding="utf-8",
    )

    errors = validate(tmp_path)

    assert (
        "farplane/metrics.yaml metrics.accepted_harness_improvements.product is retired; "
        "metrics are project-level definitions."
        in errors
    )


def test_goal_kpi_metric_recipe_does_not_require_product_owner(tmp_path: Path) -> None:
    farplane = tmp_path / "farplane"
    farplane.mkdir()
    write_framework_manifest(farplane)
    write_required_project_files(tmp_path)
    (farplane / "goals.yaml").write_text(
        """kind: project-goals
framework_template_version: "0.1.0"
goals:
  test_axis:
    smart_goals:
      - id: project_kpi
        kpis:
          - id: accepted_harness_improvements
            target: 20
            direction: above
""",
        encoding="utf-8",
    )
    (farplane / "metrics.yaml").write_text(
        """kind: project-metrics
framework_template_version: "0.1.0"
metrics:
  accepted_harness_improvements:
    label: Accepted harness improvements
    description: Accepted improvements with ticket proof.
    kind: daily_count
    unit: improvements
    display: bar_plus_cumulative
""",
        encoding="utf-8",
    )
    (farplane / "bindings.yaml").write_text(
        """kind: project-bindings
framework_template_version: "0.1.0"
project: {}
metric_bindings:
  accepted_harness_improvements:
    refresh: Count ticket Reward rows.
""",
        encoding="utf-8",
    )

    errors = validate(tmp_path)

    assert errors == []


def test_metric_recipe_requires_description_and_valid_types(tmp_path: Path) -> None:
    farplane = tmp_path / "farplane"
    farplane.mkdir()
    write_framework_manifest(farplane)
    write_required_project_files(tmp_path)
    (farplane / "metrics.yaml").write_text(
        """kind: project-metrics
framework_template_version: "0.1.0"
metrics:
  accepted_harness_improvements:
    label: Accepted harness improvements
    kind: weekly_magic
    unit: improvements
    display: sparkles
    pinned: "true"
""",
        encoding="utf-8",
    )
    (farplane / "bindings.yaml").write_text(
        """kind: project-bindings
framework_template_version: "0.1.0"
project: {}
metric_bindings:
  accepted_harness_improvements:
    refresh: Count tickets.
""",
        encoding="utf-8",
    )

    errors = validate(tmp_path)

    assert "farplane/metrics.yaml metrics.accepted_harness_improvements.description must be a non-empty string." in errors
    assert "farplane/metrics.yaml metrics.accepted_harness_improvements.kind must be one of: daily, daily_count, point." in errors
    assert "farplane/metrics.yaml metrics.accepted_harness_improvements.display must be one of: bar_plus_cumulative, line, reading." in errors
    assert "farplane/metrics.yaml metrics.accepted_harness_improvements.pinned must be boolean when present." in errors


def test_metric_definitions_and_bindings_require_exact_id_parity(tmp_path: Path) -> None:
    farplane = tmp_path / "farplane"
    farplane.mkdir()
    write_framework_manifest(farplane)
    write_required_project_files(tmp_path)
    (farplane / "metrics.yaml").write_text(
        """kind: project-metrics
framework_template_version: "0.1.0"
metrics:
  defined_only:
    label: Defined only
    description: Missing its refresh binding.
    kind: point
    unit: score
    display: reading
""",
        encoding="utf-8",
    )
    (farplane / "bindings.yaml").write_text(
        """kind: project-bindings
framework_template_version: "0.1.0"
project: {}
metric_bindings:
  bound_only:
    refresh: Refresh an undefined metric.
""",
        encoding="utf-8",
    )

    errors = validate(tmp_path)

    assert "farplane/metrics.yaml definitions lack bindings.yaml metric_bindings rows: defined_only." in errors
    assert "farplane/bindings.yaml metric_bindings lack metrics.yaml definitions: bound_only." in errors


def test_old_bindings_metrics_and_semantic_binding_fields_are_rejected(tmp_path: Path) -> None:
    farplane = tmp_path / "farplane"
    farplane.mkdir()
    write_framework_manifest(farplane)
    write_required_project_files(tmp_path)
    (farplane / "bindings.yaml").write_text(
        """kind: project-bindings
framework_template_version: "0.1.0"
project: {}
metrics: {}
metric_bindings:
  semantic_leak:
    label: This belongs in metrics.yaml
    refresh: Refresh it.
""",
        encoding="utf-8",
    )

    errors = validate(tmp_path)

    assert "farplane/bindings.yaml metrics is retired; semantic definitions belong in farplane/metrics.yaml." in errors
    assert (
        "farplane/bindings.yaml metric_bindings.semantic_leak contains semantic fields owned by "
        "farplane/metrics.yaml: label."
        in errors
    )


def write_metric_binding(farplane: Path, metric_id: str = "instagram_views") -> None:
    (farplane / "metrics.yaml").write_text(
        f"""kind: project-metrics
framework_template_version: "0.1.0"
metrics:
  {metric_id}:
    label: Instagram views
    description: Daily aggregate Instagram views.
    kind: daily_count
    unit: views
    display: bar_plus_cumulative
""",
        encoding="utf-8",
    )
    (farplane / "bindings.yaml").write_text(
        f"""kind: project-bindings
framework_template_version: "0.1.0"
project: {{}}
metric_bindings:
  {metric_id}:
    refresh: Fetch platform views.
""",
        encoding="utf-8",
    )


def test_metric_observation_batch_schema_validates(tmp_path: Path) -> None:
    farplane = tmp_path / "farplane"
    farplane.mkdir()
    write_framework_manifest(farplane)
    write_required_project_files(tmp_path)
    write_metric_binding(farplane)
    path = tmp_path / ".farplane" / "metrics" / "observations" / "instagram_account_metrics" / "2026-07-03.json"
    path.parent.mkdir(parents=True)
    path.write_text(
        json.dumps(
            {
                "schema_version": 1,
                "date": "2026-07-03",
                "source_id": "instagram_account_metrics",
                "status": "available",
                "observations": [
                    {
                        "metric_id": "instagram_views",
                        "date": "2026-07-03",
                        "value": 12,
                        "status": "available",
                        "payload": {"items": []},
                    }
                ],
                "gaps": [],
            }
        ),
        encoding="utf-8",
    )

    errors = validate(tmp_path)

    assert not [error for error in errors if "instagram_account_metrics" in error]


def test_metric_observation_batch_unknown_metric_fails(tmp_path: Path) -> None:
    farplane = tmp_path / "farplane"
    farplane.mkdir()
    write_framework_manifest(farplane)
    write_required_project_files(tmp_path)
    write_metric_binding(farplane)
    path = tmp_path / ".farplane" / "metrics" / "observations" / "instagram_account_metrics" / "2026-07-03.json"
    path.parent.mkdir(parents=True)
    path.write_text(
        json.dumps(
            {
                "schema_version": 1,
                "date": "2026-07-03",
                "source_id": "instagram_account_metrics",
                "status": "available",
                "observations": [
                    {"metric_id": "unknown_views", "date": "2026-07-03", "value": 12, "status": "available"}
                ],
                "gaps": [],
            }
        ),
        encoding="utf-8",
    )

    errors = validate(tmp_path)

    assert (
        ".farplane/metrics/observations/instagram_account_metrics/2026-07-03.json observation metric_ids lack metrics.yaml definitions: unknown_views."
        in errors
    )


def test_metric_observation_batch_duplicate_metric_fails(tmp_path: Path) -> None:
    farplane = tmp_path / "farplane"
    farplane.mkdir()
    write_framework_manifest(farplane)
    write_required_project_files(tmp_path)
    write_metric_binding(farplane)
    path = tmp_path / ".farplane" / "metrics" / "observations" / "instagram_account_metrics" / "2026-07-03.json"
    path.parent.mkdir(parents=True)
    row = {"metric_id": "instagram_views", "date": "2026-07-03", "value": 12, "status": "available"}
    path.write_text(
        json.dumps(
            {
                "schema_version": 1,
                "date": "2026-07-03",
                "source_id": "instagram_account_metrics",
                "status": "available",
                "observations": [row, row],
                "gaps": [],
            }
        ),
        encoding="utf-8",
    )

    errors = validate(tmp_path)

    assert (
        ".farplane/metrics/observations/instagram_account_metrics/2026-07-03.json duplicates metric observations: instagram_views@2026-07-03."
        in errors
    )


def test_goal_kpi_without_complete_target_fails(tmp_path: Path) -> None:
    farplane = tmp_path / "farplane"
    farplane.mkdir()
    write_framework_manifest(farplane)
    write_required_project_files(tmp_path)
    (farplane / "goals.yaml").write_text(
        """kind: project-goals
framework_template_version: "0.1.0"
goals:
  test_axis:
    smart_goals:
      - id: partial_target
        kpis:
          - id: accepted_harness_improvements
            target: 20
          - id: todo_unclaimed_ticket_count
            direction: below
""",
        encoding="utf-8",
    )
    (farplane / "metrics.yaml").write_text(
        """kind: project-metrics
framework_template_version: "0.1.0"
metrics:
  accepted_harness_improvements:
    label: Accepted harness improvements
    description: Accepted improvements.
    kind: daily_count
    unit: improvements
    display: bar_plus_cumulative
  todo_unclaimed_ticket_count:
    label: Ready unclaimed tickets
    description: Ready unclaimed tickets.
    kind: point
    unit: tickets
    display: reading
""",
        encoding="utf-8",
    )
    (farplane / "bindings.yaml").write_text(
        """kind: project-bindings
framework_template_version: "0.1.0"
project: {}
metric_bindings:
  accepted_harness_improvements:
    refresh: Count accepted improvements.
  todo_unclaimed_ticket_count:
    refresh: Count ready unclaimed tickets.
""",
        encoding="utf-8",
    )

    errors = validate(tmp_path)

    assert "farplane/goals.yaml KPI ids need explicit target values: todo_unclaimed_ticket_count." in errors
    assert "farplane/goals.yaml KPI ids need explicit target directions: accepted_harness_improvements." in errors


def test_goal_kpi_metric_recipe_without_unit_fails(tmp_path: Path) -> None:
    farplane = tmp_path / "farplane"
    farplane.mkdir()
    write_framework_manifest(farplane)
    write_required_project_files(tmp_path)
    (farplane / "goals.yaml").write_text(
        """kind: project-goals
framework_template_version: "0.1.0"
goals:
  test_axis:
    smart_goals:
      - id: missing_unit
        kpis:
          - id: accepted_harness_improvements
            target: 20
            direction: above
""",
        encoding="utf-8",
    )
    (farplane / "metrics.yaml").write_text(
        """kind: project-metrics
framework_template_version: "0.1.0"
metrics:
  accepted_harness_improvements:
    label: Accepted harness improvements
    description: Accepted improvements.
    kind: daily_count
    display: bar_plus_cumulative
""",
        encoding="utf-8",
    )
    (farplane / "bindings.yaml").write_text(
        """kind: project-bindings
framework_template_version: "0.1.0"
project: {}
metric_bindings:
  accepted_harness_improvements:
    refresh: Count accepted improvements.
""",
        encoding="utf-8",
    )

    errors = validate(tmp_path)

    assert (
        "farplane/goals.yaml KPI ids have metrics.yaml definitions without unit: accepted_harness_improvements."
        in errors
    )


def test_stale_project_snapshot_fails(tmp_path: Path) -> None:
    farplane = tmp_path / "farplane"
    farplane.mkdir()
    write_framework_manifest(farplane)
    write_required_project_files(tmp_path)
    snapshot = tmp_path / ".farplane" / "project" / "ui" / "latest.json"
    snapshot.write_text(
        json.dumps(
            {
                "sources": [
                    {
                        "path": "farplane/goals.yaml",
                        "hash": "sha256:not-current",
                    }
                ]
            }
        ),
        encoding="utf-8",
    )

    errors = validate(tmp_path)

    assert ".farplane/project/ui/latest.json is stale for farplane/goals.yaml; regenerate project snapshot." in errors


def test_missing_pm_manifest_passes(tmp_path: Path) -> None:
    farplane = tmp_path / "farplane"
    farplane.mkdir()
    write_framework_manifest(farplane)
    write_required_project_files(tmp_path)

    assert validate(tmp_path) == []


def test_missing_framework_manifest_fails(tmp_path: Path) -> None:
    farplane = tmp_path / "farplane"
    farplane.mkdir()

    assert "farplane/manifest.json is required for Farplane project manifests." in validate(tmp_path)


def test_framework_manifest_shape_is_validated(tmp_path: Path) -> None:
    farplane = tmp_path / "farplane"
    farplane.mkdir()
    (farplane / "manifest.json").write_text(
        json.dumps(
            {
                "schema": "other",
                "spec_version": "",
                "project": {"name": "", "description": "", "archetype": ""},
                "standard": {
                    "tracked": ["farplane/manifest.json", "farplane/manifest.json", ".farplane/state/run-ledger.json"],
                    "ignored": [".farplane/state/run-ledger.json"],
                },
                "optional": {
                    "tracked": "farplane/pm.json",
                    "ignored": [""],
                },
            }
        ),
        encoding="utf-8",
    )

    errors = validate(tmp_path)

    assert "farplane/manifest.json schema must be farplane_project." in errors
    assert "farplane/manifest.json spec_version must be a non-empty string." in errors
    assert "farplane/manifest.json template_uses.farplane-framework must be a non-empty string." in errors
    assert "farplane/manifest.json project.name must be a non-empty string." in errors
    assert "farplane/manifest.json project.description must be a non-empty string." in errors
    assert "farplane/manifest.json project.archetype must be a non-empty string." in errors
    assert "farplane/manifest.json standard.tracked must not contain duplicate paths." in errors
    assert "farplane/manifest.json optional.tracked must be a list." in errors
    assert "farplane/manifest.json optional.ignored must contain only non-empty strings." in errors
    assert "farplane/manifest.json paths cannot be both tracked and ignored: .farplane/state/run-ledger.json." in errors
    missing_surface_error = next(
        error for error in errors if error.startswith("farplane/manifest.json missing required standard paths:")
    )
    for path in [
        "AGENTS.md",
        "PROJECT_RULES.md",
        "ARCHITECTURE.md",
        "farplane/README.md",
        "farplane/metrics.yaml",
        "tickets/templates/ticket.md",
    ]:
        assert path in missing_surface_error


def test_framework_manifest_rejects_generic_review_state(tmp_path: Path) -> None:
    farplane = tmp_path / "farplane"
    farplane.mkdir()
    write_framework_manifest(farplane)
    write_required_project_files(tmp_path)
    manifest_path = farplane / "manifest.json"
    manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    manifest["optional"]["ignored"] = [".farplane/reviews/"]
    manifest_path.write_text(json.dumps(manifest), encoding="utf-8")

    errors = validate(tmp_path)

    assert (
        "farplane/manifest.json must not declare retired generic review paths: .farplane/reviews/; "
        "review evidence belongs in tickets/<ticket>/artifacts/."
        in errors
    )


def test_valid_pm_manifest_passes(tmp_path: Path) -> None:
    farplane = tmp_path / "farplane"
    farplane.mkdir()
    write_framework_manifest(farplane)
    write_required_project_files(tmp_path)
    (farplane / "pm.json").write_text(
        json.dumps(
            {
                "version": 1,
                "name": "Project PM",
                "role": "founder_operator",
                "threads": {
                    "chats": ["019ecbfb-26dd-77d1-8f7d-b0fe2f8c7ea4"],
                    "automations": ["019ecbfb-9d19-7058-a516-f96f4a3515d4"],
                },
            }
        ),
        encoding="utf-8",
    )

    assert validate(tmp_path) == []


def test_pm_manifest_shape_is_validated(tmp_path: Path) -> None:
    farplane = tmp_path / "farplane"
    farplane.mkdir()
    write_framework_manifest(farplane)
    (farplane / "pm.json").write_text(
        json.dumps(
            {
                "version": 2,
                "name": "",
                "role": "operator",
                "threads": {
                    "chats": ["chat-1", "chat-1"],
                    "automations": [123],
                    "extra": [],
                },
                "unsupported": True,
            }
        ),
        encoding="utf-8",
    )

    errors = validate(tmp_path)

    assert "farplane/pm.json has unsupported keys: unsupported." in errors
    assert "farplane/pm.json version must be 1." in errors
    assert "farplane/pm.json name must be a non-empty string." in errors
    assert "farplane/pm.json role must be founder_operator." in errors
    assert "farplane/pm.json threads has unsupported keys: extra." in errors
    assert "farplane/pm.json threads.automations must contain only non-empty strings." in errors
    assert "farplane/pm.json threads.chats must not contain duplicate thread IDs." in errors
