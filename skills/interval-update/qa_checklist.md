---
title: Interval Update QA Checklist
owner: interval-update
status: active
kind: qa-checklist
applies_to:
  - interval-update
  - daily-bau-report
  - weekly-bau-report
---

# Interval Update QA Checklist

Use before an Interval run and again before returning its report.

```text
interval_check(report, evidence, ticket_deltas) -> pass | violation | source_gap
```

## Checklist

- [ ] The run is a bounded Daily, Weekly, or explicitly BAU-only profile and
      writes one dated report with Core report frontmatter.
- [ ] The report contains a Markdown `Problems` checklist; no finding IDs,
      finding frontmatter, or findings registry were added.
- [ ] Feed Scout and other provider outputs were read only as completed report
      refs; the run did not invoke them when missing.
- [ ] The run did not call Dogfood Review, reward check-ins, priority planning,
      leverage planning, harness improvement, Goal, Pulse, or a worker.
- [ ] Every maintenance delta cites evidence finalized before the current
      report, is corrective rather than directional, names proof and a stop
      condition, and has no active duplicate.
- [ ] Problems first recorded in this report remain ledger-only even when they
      look actionable.
- [ ] The dated report existed before any allowed maintenance delta, the cap
      was respected, and all deltas or rejections are linked in the report.
- [ ] Finalized prior reports were not rewritten; unresolved problems were
      carried forward by reference.
