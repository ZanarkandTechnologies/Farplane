---
title: Lead Scout QA Checklist
owner: lead-scout
status: active
kind: qa-checklist
applies_to:
  - lead-scout
---

# Lead Scout QA Checklist

Use this checklist before scouting and again before claiming a candidate packet
is ready for research or outreach handoff.

```text
lead_scout_check(candidate_packet, source_boundary)
  -> pass | revise | blocked
```

## Preflight

- [ ] Source boundary, outreach goal, qualification filter, rejection criteria,
  scout mode, ICP fit, negative-fit criteria, allowed evidence fields, and
  privacy/safety limits are explicit.

## Candidate Checks

- [ ] The packet uses a visible signal ladder: must-have fit signals,
  high-intent triggers, disqualifiers, weak proxies, forbidden guesses, and
  research-worthy unknowns, plus `why them`, `why now`, and channel fit.
- [ ] Discovery lanes are named and justified, such as repo activity, launch
  pages, event lists, hiring signals, public complaints, tool migrations, or
  community asks; the output is not a generic web-search dump.
- [ ] Each accepted candidate has public/supplied evidence, confidence,
  disqualifiers or unknowns, a next-owner route, and a reason they beat the
  rejected near-misses; broad persona matches without a timely trigger are
  rejected or marked weak.
- [ ] The packet avoids private dossiering, sensitive-attribute inference,
  hidden scoring criteria, unrestricted platform scraping claims, whole-vertical
  dumps, and CRM writeback beyond stable ID, name, description, links, and
  status; candidates are tiered and stage-exit status is visible.

## Reviewer Prompt

```text
Review the candidate packet against skills/lead-scout/qa_checklist.md.
Return pass, revise, or blocked. Focus on source boundary, signal ladder,
evidence quality, ethical qualification, ranking reasons, and next-owner fit.
```
