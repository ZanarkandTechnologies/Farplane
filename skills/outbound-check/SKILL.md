---
name: outbound-check
description: "Use for \"check this before it goes out\", \"is this email ready to send\" or \"check the ad and funnel\": one command grades the delivered copy on ten common mistakes and returns ready, check or hold."
source: local
department: delivery
template_uses:
  skill-template: "0.6.6"
  skill-eval-task: "0.2.0"
allowed-tools: Read, Glob, Grep, Bash
---

# Outbound Check

## Context

Use this before anything someone outside the team receives goes live: an email
or sequence, an ad, a social post, a public page, a form and what it triggers,
a proposal, a DM, or a shared document. It proves the delivered copy, not the
pipeline: "the contact entered the sequence" proves an email will be sent; only
the received email proves what it says. One command runs the fixed-rule checks,
screenshots HTML at phone width in light and dark mode, and has an independent
model grade every row of [the checklist](references/checklist.md), because most
rows (a wrong address, a broken promise, a test name) need judgment. It does
not write copy (`copywriting`), publish (`ads`, `zernio`), or prove ticket work
(`qa`).

## Skill Signature

```text
outbound_check(delivered_copies, sender_facts) -> report.md + result.json + verdict: ready | check | hold
reads: saved emails (.eml), HTML or text files, preview images, page URLs, the sender's facts
does: runs fixed-rule checks, renders the copy, has a separate model grade the ten checklist rows
writes: .farplane/outbound-check/<run>/ with report.md, result.json and screenshots
returns: verdict, each failing row with evidence and fix, each row to check by hand
```

<!-- BEGIN FARPLANE_IMPORTANT_CHECKLIST -->
## Todo List

- [ ] **N1 — Get the delivered copy, not the pipeline.**
  `outbound target -> one saved copy per piece | blocked`

  Rule: The copy is what the recipient gets: a test send to an inbox you can
  read, saved as `.eml`, for every step of a sequence; the platform preview of
  each ad placement or post, saved as an image or text; a page's production URL.
  Use a test contact, because following links registers clicks and can fire
  link-click automations. The editor view, a subscriber count, or a "sent"
  status is not a copy. The checklist's channel table lists each case.

  Example: `"contact entered the sequence (step 0 of 4)" -> test-send all four
  emails, save each .eml -> four copies`

  Assert:
  - Every piece the recipient gets has a saved copy, or is named as missing.
- [ ] **N2 — Write the sender facts the judge checks against.**
  `project + brand + offer -> sender facts`

  Rule: The judge can fail a wrong address or a broken promise only when it
  knows the right one. Fill the facts from what is already recorded (project
  docs, the live page, the offer): sender name and postal address, live
  domains, intended contact links, offer and price, audience, how many pieces
  the flow has, and the test contact's name so a rendered merge field is not
  mistaken for test data. Ask only for a fact nothing records.

  Example: `--context "Sender: Acme Studio, 12 Harbour Road, Singapore. Live:
  plan.acme.co. Offer: free plan, then done-for-you. Sequence: 4 emails. Test
  contact: Sam."`

  Assert:
  - Live domain, postal address, and piece count are given or marked unknown.
- [ ] **N3 — Run the one command on the whole flow.**
  `copies + facts -> .farplane/outbound-check/<run>/report.md + result.json`

  Rule: Run `farplane run -- python3 skills/outbound-check/scripts/outbound_check.py
  <copy...> --context "<facts>"` (or `--context-file`). Pass the ad, page, and
  every email of one flow together so the judge can compare the promise across
  them. Two judge passes run in parallel and each row keeps its worst grade
  (about a minute for a two-page flow, on the subscription). Text in hidden elements
  is a warning and still reaches the judge, since a script may reveal it.
  Fixed-rule blockers fail their row whatever the judge says. Without
  a signed-in `claude` CLI (the judge runs on the Claude Code subscription) or a headless browser, the affected rows come back
  `NOT_PROVABLE`, never passed. `--offline` skips following links.

  Assert:
  - The run printed `OUTBOUND_CHECK: verdict=...`; a missing judge or browser is named in the report.
- [ ] **N4 — Act on the verdict.**
  `report -> hold + fixes | check rows by hand | ready`

  Rule: `hold`: do not send or publish. If it is already live, pause it, count
  who got the faulty copy and whether any were outsiders, fix, then rerun on a
  fresh delivered copy. `check`: do each `NOT_PROVABLE` row by hand, such as
  clicking unsubscribe from a test contact, and record what you saw. `ready`:
  hand the report to the publish gate (`ads`, `zernio`, or the operator).

  Assert:
  - Nothing goes live on `hold`, and `ready` always comes from a run on the final copy.
<!-- END FARPLANE_IMPORTANT_CHECKLIST -->

## Gotchas

- Checking the editor or a draft doc: platform sample text and default preview
  text show only in what was actually sent.
- Checking one piece at a time: the judge cannot see that the ad promised a
  price the email changes.
- Treating zero fixed-rule blockers as done: they cover placeholders and links,
  not a wrong address, a test name, or a broken promise.

## Reference Map

- [checklist](references/checklist.md) - the ten rows the judge grades, how to
  get the delivered copy per channel, and a worked example.

## Output

The command prints the report and ends with
`OUTBOUND_CHECK: verdict=<ready|check|hold> report=<path>`; it exits 1 on hold.
Reply with the verdict, each failing row with its evidence and fix, each row to
check by hand, and the report path.
