# Outbound Mode

Load this for `qa(target, mode: outbound)`: anything someone outside the team
will receive or see, before it is called live. That covers an email or
sequence, an ad, a social post, a public page, a form and what it triggers, a
proposal, a DM, or a shared document. Outbound proves the delivered copy, not
the pipeline: "the contact entered the sequence" proves an email will be sent;
only the received email proves what it says.

```text
outbound_check(target, channel)
  -> delivered copy + scanner output + mistake rows + verdict + blast radius
```

## 1. Get the delivered copy

| Channel | Delivered copy | Not proof |
| --- | --- | --- |
| Email or sequence | A test send to an inbox you can read, saved as `.eml` or HTML; every step of the sequence | Subscriber counts, "sent" status, the editor view |
| Ad | The platform preview for every placement, and the destination opened from it | The creative file, the campaign config |
| Social post | The platform's draft preview, and each link opened from it | The caption in a doc |
| Public page | The production URL in a logged-out private window, desktop and mobile | localhost, a preview deployment, a logged-in view |
| Form or funnel | One test submission end to end: confirmation, every email or message it triggers, where the lead lands | A 200 from the API |
| Proposal, DM, shared doc | The file or message as the recipient opens it, with their access level | The draft you wrote |

Use a test contact: following links in a test send registers clicks and can
fire link-click automations.

## 2. Scan it

```bash
python3 skills/qa/scripts/check_outbound.py <copy.eml | page.html | copy.txt | - | https://page>
```

The scanner flags the mechanical faults: unrendered merge fields and
placeholders, platform sample text and editor instructions, non-production
links (localhost, preview deployments, tunnels), and links that break or end
at a login wall when followed. It never follows unsubscribe or preference
links; test those by hand from a contact you can lose. `--offline` skips
following links. Exit 1 means blockers. A clean scan is necessary, not
sufficient.

## 3. Read it as the recipient against the common mistakes

Read the whole thing: subject, from name, preview text, body, footer, and every
step after the first. Click every link from the delivered copy, logged out.
Mark each row `PASS | FAIL | not_provable`.

| # | Mistake | Passes when |
| --- | --- | --- |
| 1 | Template or sample text left in | Nothing reads like editor instructions, sample content, or "your text here"; our copy replaced the template rather than being pasted into it |
| 2 | Placeholders and merge fields | No `{{ }}`, `[First Name]`, `TODO`, or `XXX`; an empty name falls back cleanly ("Hi there", not "Hi ,") |
| 3 | Wrong link target | Links use the live domain or a merge field, never a preview, staging, localhost, or personal deployment URL; query values are real |
| 4 | Link opens a wall | Each link opens logged out with no login, request-access, 404, or expired page; shared files are set to the recipient's access |
| 5 | Wrong sender or legal footer | From name, reply-to, and footer postal address are ours; unsubscribe works; a form that collects data links its privacy policy |
| 6 | Test or private data showing | No test names, internal notes, private client names, secrets, or contact details we did not mean to share |
| 7 | Broken promise chain | The ad, the page, and the follow-up name the same offer, price, and next step |
| 8 | Bad rendering | Readable on mobile and in dark mode; images load from public URLs; the preview text and link card are ours, not the platform's default |
| 9 | Only the first piece checked | Every email in the sequence, every ad placement, and every page in the flow got the same check |
| 10 | Copy errors | Names, prices, dates, time zones, and grammar are right; every claim has its proof |

## 4. Verdict and blast radius

A failing row 1-6 is a release blocker: hold the send or pause the automation,
fix, then rerun the check on a fresh delivered copy. When a fault already went
out, record who received it (count, and whether any were outsiders) before
fixing, and stop the later steps of any sequence. Put the scanner output, the
rows, and the copy you checked in the QA report; without an issue, return them
in the reply.

## Worked example

A lead-magnet welcome email was marked verified because the test contact
entered the sequence. The received email showed the platform's sample sequence
instructions above and below our copy, a plan link to a login-protected
preview deployment, and a placeholder postal address in the footer: rows 1, 3,
4, and 5 fail. On the saved copy the scanner reports two template-text
blockers, the preview-deployment blocker, and the login wall when the link is
followed; the footer address needed the read in step 3.
