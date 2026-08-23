---
title: Meta Ads QA Checklist
owner: meta-ads
status: active
kind: qa-checklist
applies_to:
  - meta-ads-report
  - blocked-report
---

# Meta Ads QA Checklist

Apply this checklist before live account reads and again before returning a
report. This package is read-only; a request for a write action is a routing
failure, not a reason to bypass the boundary.

```text
meta_ads_check(request, command, report) -> pass | revise | blocked
```

## Checklist

- [ ] The requested command is listed as read-only in `references/cli.md`; no
  raw Graph API mutation is used.
- [ ] `scripts/check_config.py` passed through `farplane run --` before the
  account/API read, and neither output nor artifacts contain a token.
- [ ] A clean-room blocked report that cannot execute the checker explicitly
  names `farplane run -- python3 skills/meta-ads/scripts/check_config.py`,
  `META_ADS_ACCESS_TOKEN`, and the next safe account-discovery command.
- [ ] Account/entity scope and the date window are exact; accounts are
  discovered or explicitly supplied rather than inferred.
- [ ] The report labels source fields, units/currency, date window, and source
  gaps accurately; it does not fabricate a zero or an optimization conclusion.
- [ ] A successful date-preset report records API-returned `date_start` and
  `date_stop`. A blocked report retains the exact date preset and names the
  exact intended read command (including `insights`, entity placeholder, date
  preset, and level) plus its source fields as unavailable so the next run is
  repeatable without inventing dates.
- [ ] Account IDs and raw API results stay in the response or an ignored/
  ticket-scoped evidence path, not a tracked general-purpose artifact.
- [ ] Campaign, creative, targeting, budget, status, or launch advice is routed
  to `ad-advisor`; the report makes that decision boundary explicit and no
  spend-affecting command is issued. A write handoff names the observed entity
  data/requested change and the required thesis, binding, cap, policy,
  measurement, paused/dry-run, and approval gates.

## Reviewer Prompt

```text
Review the Meta Ads report and command evidence against
skills/meta-ads/qa_checklist.md. Return pass, revise, or blocked for each
check, identify any mutation or secret-exposure risk, and verify that observed
data is distinct from campaign advice.
```
