#!/usr/bin/env python3

from __future__ import annotations

import json
import sys
import unittest
from email.message import EmailMessage
from pathlib import Path
from tempfile import TemporaryDirectory


sys.path.insert(0, str(Path(__file__).resolve().parent))
from mechanical import load_piece, scan
from outbound_check import judge, judge_request, load_rows, merge, overall


# The delivered copy of a welcome email that shipped broken: the platform's
# sample sequence text around our copy and a link to a preview deployment.
BROKEN_WELCOME = """Sequences are an automated series of emails.
You can add more emails by clicking "Add Email" on the right and arrange
emails by dragging them to the proper order.

Hi Sam,
Here's your free plan: https://acme-ab12cd3ef-team-projects.vercel.app/plan/
Rather we run it for you? Message us: https://wa.me/15550100

Within this popover, you can also choose which days this email is sent on.
"""

CLEAN_WELCOME = """Hi Sam,
Here's your free plan: https://plan.acme.co/plan/
Rather we run it for you? Message us: https://wa.me/15550100
"""


def levels(findings, level):
    return [(label, detail) for found, _, label, detail in findings if found == level]


def fake_fetch(responses):
    def fetch(url):
        status, final_url = responses.get(url, (200, url))
        return status, final_url, ""
    return fetch


class MechanicalTest(unittest.TestCase):
    def test_broken_welcome_email_is_blocked_offline(self):
        findings = scan(BROKEN_WELCOME, [], follow=False)
        rows = {row for level, row, _, _ in findings if level == "BLOCKER"}
        self.assertEqual(rows, {1, 3})
        self.assertTrue(levels(findings, "WARN"), "editor instructions should warn")

    def test_preview_link_is_still_followed_for_its_wall(self):
        fetch = fake_fetch({"https://acme-ab12cd3ef-team-projects.vercel.app/plan/":
                            (200, "https://vercel.com/login?next=x")})
        findings = scan(BROKEN_WELCOME, [], fetch=fetch)
        self.assertIn((("BLOCKER", 4)), {(level, row) for level, row, _, _ in findings})

    def test_clean_email_has_no_blockers(self):
        findings = scan(CLEAN_WELCOME, [], fetch=fake_fetch({}))
        self.assertEqual(levels(findings, "BLOCKER"), [])
        self.assertEqual(len(levels(findings, "OK")), 2)

    def test_placeholders_and_empty_greeting_block(self):
        text = "Hi ,\nYour code is {{ coupon }} for *|FNAME|* at [Company]. TODO: price\n[PENDING] Credential line 1"
        labels = {label for label, _ in levels(scan(text, [], follow=False), "BLOCKER")}
        self.assertTrue({"greeting with an empty name", "unrendered template tag",
                         "unrendered merge field", "bracket placeholder",
                         "unfinished marker"} <= labels)
        self.assertIn("[PENDING]", [d for label, d in levels(scan(text, [], follow=False), "BLOCKER")])
        self.assertEqual(levels(scan("Our todo list app", [], follow=False), "BLOCKER"), [])

    def test_login_wall_broken_and_refused_links(self):
        text = "Doc: https://docs.acme.co/a Old: https://acme.co/gone Site: https://www.linkedin.com/in/x"
        fetch = fake_fetch({
            "https://docs.acme.co/a": (200, "https://accounts.google.com/v3/signin"),
            "https://acme.co/gone": (404, "https://acme.co/gone"),
            "https://www.linkedin.com/in/x": (999, "https://www.linkedin.com/in/x"),
        })
        findings = scan(text, [], fetch=fetch)
        blockers = " ".join(label for label, _ in levels(findings, "BLOCKER"))
        self.assertIn("login wall", blockers)
        self.assertIn("404", blockers)
        self.assertEqual(len(levels(findings, "WARN")), 1)

    def test_eml_reads_html_and_never_follows_unsubscribe(self):
        msg = EmailMessage()
        msg["Subject"] = "Your plan"
        msg["From"] = "Sam <sam@acme.co>"
        msg.set_content("Hi Sam, your plan: https://plan.acme.co/plan/")
        msg.add_alternative(
            '<html><body><p>Hi Sam</p><a href="https://plan.acme.co/plan/">Open your plan</a>'
            '<a href="https://mail.acme.co/u/123">Unsubscribe</a>'
            '<img src="http://localhost:3000/hero.png"></body></html>',
            subtype="html",
        )
        with TemporaryDirectory() as tmp:
            path = Path(tmp) / "welcome.eml"
            path.write_bytes(bytes(msg))
            piece = load_piece(str(path))
        followed = []

        def fetch(url):
            followed.append(url)
            return 200, url, ""

        findings = scan(piece.text, piece.links, fetch=fetch)
        self.assertIn("Subject: Your plan", piece.text)
        self.assertIn("<a href", piece.html)
        self.assertNotIn("https://mail.acme.co/u/123", followed)
        self.assertNotIn("http://localhost:3000/hero.png", followed)
        self.assertTrue(levels(findings, "SKIP"))
        self.assertIn("local address", [label for label, _ in levels(findings, "BLOCKER")])


class VerdictTest(unittest.TestCase):
    def setUp(self):
        self.rows = load_rows()

    def test_checklist_is_the_single_row_source(self):
        self.assertEqual([row["id"] for row in self.rows], list(range(1, 11)))

    def test_fixed_rule_blocker_beats_a_judge_pass(self):
        findings = [("a.eml", "BLOCKER", 3, "Vercel preview deployment", "https://x")]
        judged = {row["id"]: {"id": row["id"], "verdict": "PASS", "evidence": "ok"} for row in self.rows}
        merged = merge(self.rows, findings, judged, None)
        self.assertEqual(merged[2]["verdict"], "FAIL")
        self.assertEqual(overall(merged), "hold")

    def test_missing_judge_is_never_ready(self):
        merged = merge(self.rows, [], {}, "OPENROUTER_API_KEY is not set")
        self.assertEqual({row["verdict"] for row in merged}, {"NOT_PROVABLE"})
        self.assertEqual(overall(merged), "check")
        self.assertIn("OPENROUTER_API_KEY", merged[0]["evidence"])

    def test_all_pass_is_ready(self):
        judged = {row["id"]: {"id": row["id"], "verdict": "PASS", "evidence": "ok"} for row in self.rows}
        self.assertEqual(overall(merge(self.rows, [], judged, None)), "ready")

    def test_judge_parses_fenced_json_and_reports_gaps(self):
        body = judge_request(self.rows, [load_piece_text(CLEAN_WELCOME)], [], "Sender: Acme", [], "m")
        self.assertIn("CHECKLIST:", body["messages"][1]["content"][0]["text"])
        reply = {"choices": [{"message": {"content": "```json\n" + json.dumps(
            {"rows": [{"id": 5, "verdict": "FAIL", "evidence": "Seattle address", "fix": "use ours"},
                      {"id": 6, "verdict": "MAYBE", "evidence": "?"}]}) + "\n```"}}],
                 "usage": {"cost": 0.02}}
        rows, gap, cost = judge(body, {"OPENROUTER_API_KEY": "k"}, post=lambda b, k: reply)
        self.assertEqual((list(rows), gap, cost), ([5], None, 0.02))
        self.assertIn("not set", judge(body, {}, post=lambda b, k: reply)[1])
        failing = judge(body, {"OPENROUTER_API_KEY": "k"}, post=lambda b, k: {"choices": []})
        self.assertEqual(failing[0], {})
        self.assertIn("judge call failed", failing[1])

    def test_judge_retries_once_on_invalid_json(self):
        body = judge_request(self.rows, [load_piece_text(CLEAN_WELCOME)], [], "", [], "m")
        good = json.dumps({"rows": [{"id": 1, "verdict": "PASS", "evidence": "ok"}]})
        replies = [{"choices": [{"message": {"content": '{"rows": [{"id": 1, "evidence": "say "hi""}]}'}}],
                    "usage": {"cost": 0.01}},
                   {"choices": [{"message": {"content": good}}], "usage": {"cost": 0.02}}]
        sent = []

        def post(request_body, key):
            sent.append(request_body)
            return replies[len(sent) - 1]

        rows, gap, cost = judge(body, {"OPENROUTER_API_KEY": "k"}, post=post)
        self.assertEqual((list(rows), gap, round(cost, 2)), ([1], None, 0.03))
        self.assertEqual(sent[1]["messages"][-1]["role"], "user")
        self.assertIn("not valid JSON", sent[1]["messages"][-1]["content"])


def load_piece_text(text):
    with TemporaryDirectory() as tmp:
        path = Path(tmp) / "copy.txt"
        path.write_text(text)
        return load_piece(str(path))


if __name__ == "__main__":
    unittest.main()
