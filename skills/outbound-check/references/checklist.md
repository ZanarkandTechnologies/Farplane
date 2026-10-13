# Outbound Checklist

The ten common mistakes in anything an outsider receives. This table is the
single source: `scripts/outbound_check.py` reads it, gives it to the judge,
and reports each row as `PASS`, `FAIL`, or `NOT_PROVABLE`. Keep the table's
three columns; add a row here rather than in code.

| # | Mistake | Passes when |
| --- | --- | --- |
| 1 | Template or sample text left in | Nothing reads like editor instructions, platform sample content, or "your text here"; our copy replaced the template rather than being pasted into it, including the preview text |
| 2 | Placeholders and merge fields | No unrendered tags such as `{{ }}`, `[First Name]`, `TODO`, or `XXX`; the greeting uses the recipient's name or a clean fallback, never "Hi ," or a test name |
| 3 | Wrong link target | Every link uses the live domain or an intended third party, never a preview, staging, localhost, or personal deployment URL; query values look real |
| 4 | Link opens a wall | Every link opens logged out with no login, request-access, 404, or expired page; shared files are open to the recipient |
| 5 | Wrong sender or legal footer | From name, reply-to, and footer postal address match the sender's facts; an email has a working unsubscribe; a form that collects data links its privacy policy |
| 6 | Test or private data showing | No test names, internal notes, private client names, secrets, or contact details the sender did not mean to share |
| 7 | Broken promise chain | The ad, page, and follow-up name the same offer, price, and next step, and each piece delivers what the one before promised |
| 8 | Bad rendering | Readable at phone width in light and dark mode; images load; nothing overlaps, is cut off, or is invisible against its background |
| 9 | Only the first piece checked | Every piece the context says exists (each sequence step, ad placement, page in the flow) was supplied and checked |
| 10 | Copy errors | Names, prices, dates, time zones, spelling, and grammar are right; every claim is plausible and supportable; the tone fits the sender |

## Getting the delivered copy

| Channel | Delivered copy | Not proof |
| --- | --- | --- |
| Email or sequence | A test send to an inbox you can read, saved as `.eml`; every step | Subscriber counts, "sent" status, the editor view |
| Ad | The platform preview for each placement, saved as an image or text, plus the destination URL | The creative file, the campaign config |
| Social post | The platform's draft preview, plus each link in it | The caption in a doc |
| Public page | The production URL, opened logged out | localhost, a preview deployment, a logged-in view |
| Form or funnel | One test submission end to end: confirmation page, every email or message it triggers | A 200 from the API |
| Proposal, DM, shared doc | The file or message as the recipient opens it, with their access level | The draft you wrote |

## Worked example

A lead-magnet welcome email was marked verified because the test contact
entered the sequence. The received email showed the platform's sample sequence
instructions above and below our copy, a plan link to a login-protected preview
deployment, and a placeholder postal address in the footer. The fixed rules
catch rows 1 and 3 and, when the link is followed, row 4; only the judge,
given the sender's real address, catches row 5.
