#!/usr/bin/env python3

from __future__ import annotations

import sys
import unittest
from email.message import EmailMessage
from pathlib import Path
from tempfile import TemporaryDirectory


sys.path.insert(0, str(Path(__file__).resolve().parent))
from check_outbound import load_copy, scan


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
    return [(label, detail) for found, label, detail in findings if found == level]


def fake_fetch(responses):
    def fetch(url):
        status, final_url = responses.get(url, (200, url))
        return status, final_url, ""
    return fetch


class CheckOutboundTest(unittest.TestCase):
    def test_broken_welcome_email_is_blocked_offline(self):
        findings = scan(BROKEN_WELCOME, [], follow=False)
        labels = [label for label, _ in levels(findings, "BLOCKER")]
        self.assertIn("template sample text", labels)
        self.assertIn("Vercel preview deployment, not the live domain", labels)
        self.assertTrue(levels(findings, "WARN"), "editor instructions should warn")

    def test_clean_email_has_no_blockers(self):
        findings = scan(CLEAN_WELCOME, [], fetch=fake_fetch({}))
        self.assertEqual(levels(findings, "BLOCKER"), [])
        self.assertEqual(len(levels(findings, "OK")), 2)

    def test_placeholders_and_empty_greeting_block(self):
        text = "Hi ,\nYour code is {{ coupon }} for *|FNAME|* at [Company]. TODO: price"
        labels = {label for label, _ in levels(scan(text, [], follow=False), "BLOCKER")}
        self.assertTrue({"greeting with an empty name", "unrendered template tag",
                         "unrendered merge field", "bracket placeholder",
                         "unfinished marker"} <= labels)

    def test_login_wall_and_broken_links_block(self):
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

    def test_eml_reads_html_links_and_never_follows_unsubscribe(self):
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
            text, links = load_copy(str(path))
        followed = []

        def fetch(url):
            followed.append(url)
            return 200, url, ""

        findings = scan(text, links, fetch=fetch)
        self.assertIn("Subject: Your plan", text)
        self.assertNotIn("https://mail.acme.co/u/123", followed)
        self.assertTrue(levels(findings, "SKIP"))
        self.assertIn("local address", [label for label, _ in levels(findings, "BLOCKER")])


if __name__ == "__main__":
    unittest.main()
