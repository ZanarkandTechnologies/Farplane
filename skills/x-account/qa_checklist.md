---
title: X Account QA Checklist
owner: x-account
status: active
kind: qa-checklist
---

# X Account QA Checklist

Apply Universal QA plus only the selected branch QA. Do not force a metrics run
to satisfy publish checks, or a validation-only run to produce KPI snapshots.

## Universal QA

- [ ] No token, secret, cookie, account ID, or raw private payload is copied to
  tracked files.
- [ ] Account alias, selected branch, and source artifact or blocker are named.
- [ ] Credential source is private env/runtime only and is redacted in outputs.
- [ ] Broad discovery, competitor reading, or attention-graph work is routed to
  `apify` or `feed-scout`.
- [ ] Output includes proof path or blocker, timestamp, and branch QA verdict.

## Validation Branch QA

- [ ] Draft payload is parseable as a post or thread artifact.
- [ ] X-specific constraints were checked: text length, thread order, media
  assumptions, and publish boundary.
- [ ] No account mutation occurred.
- [ ] Blocking issues and non-blocking warnings are separated.
- [ ] Suggested fixes preserve the original artifact intent.

## Metrics Branch QA

- [ ] Input source is recorded: API endpoint, export file, screenshot/report
  artifact, or manual source.
- [ ] Output observations match the Farplane KPI shape used by
  `.farplane/metrics/ui/latest.json`.
- [ ] Missing values use `source_gap`, not fake zero.
- [ ] JSON parses and can be consumed by `farplane metrics snapshot`.
- [ ] Raw credential-bearing API/export payload is not persisted in tracked
  files.

## Publish Branch QA

- [ ] Explicit approval names exact account alias, draft artifact, and action.
- [ ] Validation branch passed before publish.
- [ ] Credentials came from private env/runtime only.
- [ ] Post IDs, URLs, timestamp, and account alias are recorded.
- [ ] No raw credential-bearing response is persisted.
