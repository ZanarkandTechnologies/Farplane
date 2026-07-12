import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

from PIL import Image


SCRIPT = Path(__file__).with_name("prepare_pet_run.py")
SUMMARY_SCRIPT = Path(__file__).with_name("write_run_summary.py")


class PreparePetRunTests(unittest.TestCase):
    def test_person_discovery_is_copied_and_sources_recorded(self):
        with tempfile.TemporaryDirectory() as raw_dir:
            root = Path(raw_dir)
            image = root / "friend.png"
            brief = root / "person.md"
            output = root / "run"
            Image.new("RGB", (32, 32), "white").save(image)
            brief.write_text("# Person brief\n", encoding="utf-8")

            subprocess.run(
                [
                    sys.executable,
                    str(SCRIPT),
                    "--reference",
                    str(image),
                    "--person-discovery-file",
                    str(brief),
                    "--profile-source",
                    "https://example.com/person",
                    "--output-dir",
                    str(output),
                ],
                check=True,
                capture_output=True,
                text=True,
            )

            request = json.loads((output / "pet_request.json").read_text())
            self.assertEqual(request["person_discovery_path"], "references/person-discovery.md")
            self.assertEqual(request["profile_sources"], ["https://example.com/person"])
            self.assertTrue((output / "references/person-discovery.md").is_file())

            subprocess.run(
                [
                    sys.executable,
                    str(SUMMARY_SCRIPT),
                    "--run-dir",
                    str(output),
                    "--package",
                    str(root / "installed-pet"),
                ],
                check=True,
                capture_output=True,
                text=True,
            )
            summary = json.loads((output / "qa/run-summary.json").read_text())
            self.assertEqual(summary["person_discovery_path"], "references/person-discovery.md")
            self.assertEqual(summary["profile_sources"], ["https://example.com/person"])

    def test_person_discovery_requires_reference_image(self):
        with tempfile.TemporaryDirectory() as raw_dir:
            root = Path(raw_dir)
            brief = root / "person.md"
            brief.write_text("# Person brief\n", encoding="utf-8")
            result = subprocess.run(
                [
                    sys.executable,
                    str(SCRIPT),
                    "--person-discovery-file",
                    str(brief),
                    "--output-dir",
                    str(root / "run"),
                ],
                capture_output=True,
                text=True,
            )
            self.assertNotEqual(result.returncode, 0)
            self.assertIn("requires at least one --reference image", result.stderr)


if __name__ == "__main__":
    unittest.main()
