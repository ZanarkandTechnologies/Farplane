from __future__ import annotations

import json
import tempfile
import unittest
from pathlib import Path

from bin.validators.check_farplane_project_files import validate
from bin.validators.test_check_farplane_project_files import write_framework_manifest, write_required_project_files


class FarplaneProjectFileValidatorTests(unittest.TestCase):
    def test_goal_kpi_without_metric_recipe_fails(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            farplane = root / "farplane"
            farplane.mkdir()
            write_framework_manifest(farplane)
            write_required_project_files(root)
            (farplane / "goals.md").write_text(
                """---
kind: project-goals
framework_template_version: "0.1.0"
---

# Goals

## Goals

```yaml
goals:
  test_axis:
    smart_goals:
      - id: missing_recipe
        kpis:
          - id: unknown_metric
```
""",
                encoding="utf-8",
            )

            errors = validate(root)

        self.assertIn("farplane/goals.md KPI ids lack bindings.yaml metric recipes: unknown_metric.", errors)

    def test_metric_product_without_product_row_fails(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            farplane = root / "farplane"
            farplane.mkdir()
            write_framework_manifest(farplane)
            write_required_project_files(root)
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

            errors = validate(root)

        self.assertIn("farplane/bindings.yaml metric products are not in products.md: missing_product.", errors)

    def test_stale_project_snapshot_fails(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            farplane = root / "farplane"
            farplane.mkdir()
            write_framework_manifest(farplane)
            write_required_project_files(root)
            snapshot = root / ".farplane" / "project" / "ui" / "latest.json"
            snapshot.write_text(
                json.dumps({"sources": [{"path": "farplane/goals.md", "hash": "sha256:not-current"}]}),
                encoding="utf-8",
            )

            errors = validate(root)

        self.assertIn(".farplane/project/ui/latest.json is stale for farplane/goals.md; regenerate project snapshot.", errors)


if __name__ == "__main__":
    unittest.main()
