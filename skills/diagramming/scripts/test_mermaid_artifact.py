import unittest

from mermaid_artifact import build


class MermaidArtifactTest(unittest.TestCase):
    def test_markdown_keeps_prose_and_escapes_mermaid(self):
        page, count = build(
            "---\nstatus: companion\n---\n# Retry Plan\n\nWhy it **fails**.\n\n"
            "```mermaid\nflowchart LR\n  a[\"<input>\"] --> b\n```\n\n- one\n- two\n",
            "diagrams.md",
            None,
        )
        self.assertEqual(count, 1)
        self.assertIn("<title>Retry Plan</title>", page)
        self.assertNotIn("status: companion", page)
        self.assertIn('<pre class="mermaid">', page)
        self.assertIn("&lt;input&gt;", page)
        self.assertIn("<strong>fails</strong>", page)
        self.assertIn("<ul><li>one</li><li>two</li></ul>", page)
        self.assertNotIn("<script", page)

    def test_bare_mmd_gets_a_heading_and_title(self):
        page, count = build("stateDiagram-v2\n  [*] --> Done\n", "webhook-retries.mmd", None)
        self.assertEqual(count, 1)
        self.assertIn("<title>Webhook Retries</title>", page)
        self.assertIn("<h1>Webhook Retries</h1>", page)

    def test_other_fences_stay_code(self):
        _, count = build("# T\n\n```text\na -> b\n```\n", "t.md", None)
        self.assertEqual(count, 0)


if __name__ == "__main__":
    unittest.main()
