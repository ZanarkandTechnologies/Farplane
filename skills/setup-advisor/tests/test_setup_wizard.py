from __future__ import annotations

import subprocess
import tempfile
import unittest
from pathlib import Path


TEMPLATE = Path(__file__).parents[1] / "templates" / "setup-wizard.sh"
MARKER = "# SETUP_ADVISOR_STAGES\n"


class SetupWizardTemplateTests(unittest.TestCase):
    def materialize(self, stages: str) -> Path:
        source = TEMPLATE.read_text()
        self.assertEqual(source.count(MARKER), 1)
        generated = source.split(MARKER, 1)[0] + MARKER + stages
        temp_dir = Path(tempfile.mkdtemp(prefix="setup-advisor-test-"))
        script = temp_dir / "wizard.sh"
        script.write_text(generated)
        script.chmod(0o700)
        self.addCleanup(lambda: temp_dir.rmdir())
        self.addCleanup(lambda: script.unlink(missing_ok=True))
        return script

    def test_template_has_valid_bash_syntax(self) -> None:
        result = subprocess.run(["bash", "-n", str(TEMPLATE)], capture_output=True, text=True)
        self.assertEqual(result.returncode, 0, result.stderr)

    def test_generated_wizard_runs_without_echoing_secret(self) -> None:
        script = self.materialize(
            """TOTAL_STAGES=1
wizard_banner "Example setup"
wizard_stage "Capture provider credential"
wizard_ask_secret EXAMPLE_SECRET "Paste the credential:"
wizard_note "Credential captured for an approved destination."
wizard_finish
unset EXAMPLE_SECRET
"""
        )
        result = subprocess.run(
            ["bash", str(script)],
            input="\nsuper-secret-value\n",
            capture_output=True,
            text=True,
            env={"PATH": "/usr/bin:/bin"},
        )
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertIn("Stage 1/1", result.stdout)
        self.assertNotIn("super-secret-value", result.stdout)
        self.assertNotIn("super-secret-value", result.stderr)


if __name__ == "__main__":
    unittest.main()
