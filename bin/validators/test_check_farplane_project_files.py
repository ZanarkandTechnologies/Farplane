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
                        "farplane/products.md",
                        "farplane/ops-memory.md",
                        "farplane/automations.toml",
                        "farplane/bindings.yaml",
                        "farplane/hooks.json",
                        ".agents/skills/README.md",
                        "tickets/templates/ticket.md",
                    ],
                    "ignored": [".farplane/state/run-ledger.json", ".farplane/project/ui/"],
                },
                "optional": {
                    "tracked": ["farplane/pm.json"],
                    "ignored": [".farplane/reviews/"],
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

    for name in ("README.md", "ops-memory.md"):
        (farplane / name).write_text(
            "---\nframework_template_version: \"0.1.0\"\n---\n\n# Test\n",
            encoding="utf-8",
        )
    (farplane / "goals.yaml").write_text(
        'kind: project-goals\nframework_template_version: "0.1.0"\ngoals: {}\n',
        encoding="utf-8",
    )
    (farplane / "hooks.json").write_text('{"version": 1, "hooks": {}}\n', encoding="utf-8")
    skills_dir = root / ".agents" / "skills"
    skills_dir.mkdir(parents=True)
    (skills_dir / "README.md").write_text(
        "---\nkind: local-product-skills-index\nframework_template_version: \"0.1.0\"\n---\n\n# Local Product Skills\n",
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
    (farplane / "products.md").write_text(
        """---
kind: project-products
framework_template_version: "0.1.0"
---

# Products

## Team

| Field | Value |
| --- | --- |
| Archetype | test_project |

## Products

| ID | Product | Audience | Output | Reward |
| --- | --- | --- | --- | --- |
| test | Test product | users | artifact | signal |

## Work Lanes

| Lane | Default Weight | Purpose |
| --- | ---: | --- |
| experiment | 50 | Test a product hypothesis. |

## Constraints

- Products are not chores.
""",
        encoding="utf-8",
    )

    (farplane / "bindings.yaml").write_text(
        'kind: project-bindings\nframework_template_version: "0.1.0"\nproject: {}\n',
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


def test_missing_products_file_fails(tmp_path: Path) -> None:
    farplane = tmp_path / "farplane"
    farplane.mkdir()
    write_framework_manifest(farplane)
    write_required_project_files(tmp_path)
    (farplane / "products.md").unlink()

    errors = validate(tmp_path)

    assert "farplane/products.md is required for project product catalogs." in errors


def test_malformed_products_file_fails(tmp_path: Path) -> None:
    farplane = tmp_path / "farplane"
    farplane.mkdir()
    write_framework_manifest(farplane)
    write_required_project_files(tmp_path)
    (farplane / "products.md").write_text(
        "---\nframework_template_version: \"0.1.0\"\n---\n\n# Products\n\n## Products\n",
        encoding="utf-8",
    )

    errors = validate(tmp_path)

    assert "farplane/products.md must use front matter kind: project-products." in errors
    assert any(error.startswith("farplane/products.md missing required headings:") for error in errors)
    assert "farplane/products.md Products must use the standard product table columns." in errors


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


def test_hooks_file_shape_is_validated(tmp_path: Path) -> None:
    farplane = tmp_path / "farplane"
    farplane.mkdir()
    write_framework_manifest(farplane)
    write_required_project_files(tmp_path)
    (farplane / "hooks.json").write_text('{"version": 1, "hooks": {"file_growth": {"rules": {}}}}\n', encoding="utf-8")

    errors = validate(tmp_path)

    assert "farplane/hooks.json hooks.file_growth.rules must be a list when present." in errors


def test_retired_file_growth_hook_config_fails(tmp_path: Path) -> None:
    farplane = tmp_path / "farplane"
    farplane.mkdir()
    write_framework_manifest(farplane)
    write_required_project_files(tmp_path)
    (farplane / "file-growth-hook.json").write_text("{}\n", encoding="utf-8")

    errors = validate(tmp_path)

    assert "farplane/file-growth-hook.json is retired; use farplane/hooks.json." in errors


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

    assert "farplane/goals.yaml KPI ids lack bindings.yaml metric recipes: unknown_metric." in errors


def test_metric_product_without_product_row_fails(tmp_path: Path) -> None:
    farplane = tmp_path / "farplane"
    farplane.mkdir()
    write_framework_manifest(farplane)
    write_required_project_files(tmp_path)
    (farplane / "bindings.yaml").write_text(
        """kind: project-bindings
framework_template_version: "0.1.0"
project: {}
metrics:
  accepted_harness_improvements:
    product: missing_product
""",
        encoding="utf-8",
    )

    errors = validate(tmp_path)

    assert "farplane/bindings.yaml metric products are not in products.md: missing_product." in errors


def test_goal_kpi_metric_recipe_without_product_fails(tmp_path: Path) -> None:
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
      - id: productless_kpi
        kpis:
          - id: accepted_harness_improvements
""",
        encoding="utf-8",
    )
    (farplane / "bindings.yaml").write_text(
        """kind: project-bindings
framework_template_version: "0.1.0"
project: {}
metrics:
  accepted_harness_improvements:
    label: Accepted harness improvements
""",
        encoding="utf-8",
    )

    errors = validate(tmp_path)

    assert (
        "farplane/goals.yaml KPI ids have bindings.yaml metric recipes without product: accepted_harness_improvements."
        in errors
    )


def test_metric_recipe_requires_description_and_valid_types(tmp_path: Path) -> None:
    farplane = tmp_path / "farplane"
    farplane.mkdir()
    write_framework_manifest(farplane)
    write_required_project_files(tmp_path)
    (farplane / "bindings.yaml").write_text(
        """kind: project-bindings
framework_template_version: "0.1.0"
project: {}
metrics:
  accepted_harness_improvements:
    label: Accepted harness improvements
    product: test
    kind: weekly_magic
    unit: improvements
    display: sparkles
    pinned: "true"
    refresh: Count tickets.
""",
        encoding="utf-8",
    )

    errors = validate(tmp_path)

    assert "farplane/bindings.yaml metrics.accepted_harness_improvements.description must be a non-empty string." in errors
    assert "farplane/bindings.yaml metrics.accepted_harness_improvements.kind must be one of: daily, daily_count, point." in errors
    assert "farplane/bindings.yaml metrics.accepted_harness_improvements.display must be one of: bar_plus_cumulative, line, reading." in errors
    assert "farplane/bindings.yaml metrics.accepted_harness_improvements.pinned must be boolean when present." in errors


def write_metric_binding(farplane: Path, metric_id: str = "instagram_views") -> None:
    (farplane / "bindings.yaml").write_text(
        f"""kind: project-bindings
framework_template_version: "0.1.0"
project: {{}}
metrics:
  {metric_id}:
    label: Instagram views
    description: Daily aggregate Instagram views.
    product: test
    kind: daily_count
    unit: views
    display: bar_plus_cumulative
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
        ".farplane/metrics/observations/instagram_account_metrics/2026-07-03.json observation metric_ids lack bindings.yaml metric recipes: unknown_views."
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
          - id: ready_unclaimed_ticket_count
            direction: below
""",
        encoding="utf-8",
    )
    (farplane / "bindings.yaml").write_text(
        """kind: project-bindings
framework_template_version: "0.1.0"
project: {}
metrics:
  accepted_harness_improvements:
    product: test
    unit: improvements
  ready_unclaimed_ticket_count:
    product: test
    unit: tickets
""",
        encoding="utf-8",
    )

    errors = validate(tmp_path)

    assert "farplane/goals.yaml KPI ids need explicit target values: ready_unclaimed_ticket_count." in errors
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
    (farplane / "bindings.yaml").write_text(
        """kind: project-bindings
framework_template_version: "0.1.0"
project: {}
metrics:
  accepted_harness_improvements:
    product: test
""",
        encoding="utf-8",
    )

    errors = validate(tmp_path)

    assert (
        "farplane/goals.yaml KPI ids have bindings.yaml metric recipes without unit: accepted_harness_improvements."
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
        "farplane/products.md",
        "tickets/templates/ticket.md",
    ]:
        assert path in missing_surface_error


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
