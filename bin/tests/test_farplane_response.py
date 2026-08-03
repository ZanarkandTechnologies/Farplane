from __future__ import annotations

import json
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest


ROOT = Path(__file__).resolve().parents[2]
CORE = ROOT / "bin" / "core"
if str(CORE) not in sys.path:
    sys.path.insert(0, str(CORE))

from farplane_response import check_response, measure_response


class ResponseMeasureTests(unittest.TestCase):
    def test_plain_prose_and_blank_lines(self) -> None:
        result = measure_response("one two\n\nthree")
        self.assertEqual(result.prose_words, 3)
        self.assertEqual(result.prose_nonblank_lines, 2)
        self.assertEqual(result.total_nonblank_lines, 2)

    def test_closed_mermaid_block_is_excluded(self) -> None:
        markdown = "Result.\n```mermaid\nflowchart LR\nA --> B\n```"
        result = measure_response(markdown)
        self.assertEqual(result.prose_words, 1)
        self.assertEqual(result.prose_nonblank_lines, 1)
        self.assertEqual(result.mermaid_blocks, 1)
        self.assertEqual(result.mermaid_nonblank_lines, 4)

    def test_non_mermaid_and_unclosed_mermaid_fences_count_as_prose(self) -> None:
        ordinary = measure_response("```python\nprint(1)\n```")
        unclosed = measure_response("```mermaid\nflowchart LR\nA --> B")
        self.assertEqual(ordinary.prose_nonblank_lines, 3)
        self.assertEqual(ordinary.mermaid_blocks, 0)
        self.assertEqual(unclosed.prose_nonblank_lines, 3)
        self.assertEqual(unclosed.mermaid_blocks, 0)

    def test_exact_image_and_video_embeds_are_excluded(self) -> None:
        markdown = (
            "![image](</tmp/demo image.png>)\n"
            "![video](https://example.com/demo.mp4?download=1)"
        )
        result = measure_response(markdown)
        self.assertEqual(result.media_embeds, 2)
        self.assertEqual(result.prose_words, 0)

    def test_caption_inline_text_and_unproven_media_types_count(self) -> None:
        markdown = (
            "Caption: ![image](/tmp/demo.png)\n"
            "![audio](/tmp/demo.mp3)\n"
            "See [proof](/tmp/proof.md)."
        )
        result = measure_response(markdown)
        self.assertEqual(result.media_embeds, 0)
        self.assertEqual(result.prose_nonblank_lines, 3)

    def test_final_link_only_references_are_excluded(self) -> None:
        markdown = (
            "Worked.\n\n### References\n"
            "- [Review](</tmp/review.md>)\n"
            "- [Proof](https://example.com/proof)"
        )
        result = measure_response(markdown)
        self.assertEqual(result.prose_words, 1)
        self.assertEqual(result.reference_entries, 2)
        self.assertEqual(result.reference_nonblank_lines, 3)

    def test_mixed_or_nonfinal_references_count_as_prose(self) -> None:
        mixed = measure_response("Worked.\nReferences:\n- [Proof](/tmp/p.md)\nResidual remains.")
        nonfinal = measure_response("References:\n- [Proof](/tmp/p.md)\n\nWorked.")
        self.assertEqual(mixed.reference_entries, 0)
        self.assertEqual(mixed.prose_nonblank_lines, 4)
        self.assertEqual(nonfinal.reference_entries, 0)
        self.assertEqual(nonfinal.prose_nonblank_lines, 3)

    def test_combined_categories_and_limits(self) -> None:
        markdown = (
            "Worked now.\n"
            "![demo](/tmp/demo.webp)\n"
            "```mermaid\nflowchart LR\nA --> B\n```\n"
            "References:\n- [Proof](/tmp/proof.md)"
        )
        payload = check_response(markdown, max_prose_words=2, max_prose_lines=1)
        self.assertTrue(payload["ok"])
        self.assertEqual(payload["counts"]["prose_words"], 2)
        self.assertEqual(payload["excluded"]["mermaid_blocks"], 1)
        self.assertEqual(payload["excluded"]["media_embeds"], 1)
        self.assertEqual(payload["excluded"]["reference_entries"], 1)

    def test_violation_names_are_stable(self) -> None:
        payload = check_response("one two\nthree", max_prose_words=2, max_prose_lines=1)
        self.assertFalse(payload["ok"])
        self.assertEqual(payload["violations"], ["prose_words", "prose_nonblank_lines"])


class ResponseCliTests(unittest.TestCase):
    def run_cli(self, *args: str, stdin: str = "") -> subprocess.CompletedProcess[str]:
        return subprocess.run(
            [sys.executable, str(ROOT / "bin" / "farplane.py"), "response", "check", *args],
            input=stdin,
            text=True,
            capture_output=True,
            check=False,
        )

    def test_stdin_and_path_return_identical_json(self) -> None:
        markdown = "Worked.\n![demo](/tmp/demo.png)\nReferences:\n- [Proof](/tmp/p.md)"
        stdin_result = self.run_cli("--stdin", "--json", stdin=markdown)
        with tempfile.TemporaryDirectory() as temp_dir:
            path = Path(temp_dir) / "response.md"
            path.write_text(markdown, encoding="utf-8")
            path_result = self.run_cli(str(path), "--json")
        self.assertEqual(stdin_result.returncode, 0)
        self.assertEqual(path_result.returncode, 0)
        self.assertEqual(json.loads(stdin_result.stdout), json.loads(path_result.stdout))

    def test_over_budget_exits_one(self) -> None:
        result = self.run_cli("--stdin", "--json", "--max-words", "1", stdin="one two")
        self.assertEqual(result.returncode, 1)
        self.assertEqual(json.loads(result.stdout)["violations"], ["prose_words"])

    def test_default_hard_ceiling_is_five_hundred_words(self) -> None:
        at_limit = self.run_cli("--stdin", "--json", stdin=" ".join(["word"] * 500))
        over_limit = self.run_cli("--stdin", "--json", stdin=" ".join(["word"] * 501))
        self.assertEqual(at_limit.returncode, 0)
        self.assertEqual(over_limit.returncode, 1)
        self.assertEqual(json.loads(over_limit.stdout)["limits"]["prose_words"], 500)

    def test_conflicting_inputs_exit_two(self) -> None:
        result = self.run_cli("missing.md", "--stdin", "--json")
        self.assertEqual(result.returncode, 2)
        self.assertIn("choose either", result.stderr)

    def test_nonpositive_limits_exit_two(self) -> None:
        result = self.run_cli("--stdin", "--max-words", "0", stdin="worked")
        self.assertEqual(result.returncode, 2)
        self.assertIn("limits must be positive", result.stderr)


if __name__ == "__main__":
    unittest.main()
