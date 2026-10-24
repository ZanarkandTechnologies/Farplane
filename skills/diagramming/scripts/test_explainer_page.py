import unittest

from explainer_page import build, validate

SPEC = {
    "title": "Learning Rate Steps",
    "question": "How does the learning rate change where gradient descent lands?",
    "control": {"label": "Learning rate", "min": 0.01, "max": 1.2, "step": 0.01, "value": 0.1},
    "caption": "Above 1.0 each step overshoots further.",
    "draw": "ctx.fillStyle = c.accent; ctx.fillRect(0, 0, w * v, 10); return '</script>' + v;",
}


class ExplainerPageTest(unittest.TestCase):
    def test_page_has_one_control_and_escaped_draw(self):
        page = build(SPEC)
        self.assertIn("<title>Learning Rate Steps</title>", page)
        self.assertEqual(page.count('type="range"'), 1)
        self.assertIn('min="0.01" max="1.2" step="0.01" value="0.1"', page)
        self.assertEqual(page.count("</script>"), 1)
        self.assertIn("prefers-color-scheme: dark", page)

    def test_validate_names_missing_fields(self):
        self.assertEqual(validate(SPEC), [])
        bad = {**SPEC, "control": {"label": "x", "min": 0, "max": 1, "step": 0.1, "value": 3}}
        self.assertEqual(validate(bad), ["control value is outside min..max"])
        self.assertIn("missing draw", validate({k: v for k, v in SPEC.items() if k != "draw"}))


if __name__ == "__main__":
    unittest.main()
