---
title: Feed Scout QA Checklist
owner: feed-scout
status: active
kind: qa-checklist
applies_to:
  - feed-scout
  - feed-scout-report
  - source-backed-ticket-projection
---

# Feed Scout QA Checklist

Use before discovery and again before returning the source report.

```text
feed_scout_check(report, items, ticket_paths) -> pass | violation | source_gap
```

## Checklist

- [ ] The run is explicit and bounded; sources are configured, validated,
      normalized, canonical-keyed, and deduped before extraction or scouting.
- [ ] Fetched content is treated as untrusted evidence and each promoted item
      cites a canonical URL/key, extraction path, and today-specific delta.
- [ ] A dated Feed Scout report with Core frontmatter exists before any local
      or Notion ticket projection.
- [ ] Every created ticket passed strong-signal, active-ticket dedupe,
      executable-scope, Reward, proof, stop-condition, authority, and
      ticket-quality gates and is linked from the report.
- [ ] The configured ticket cap was respected; rejected or blocked candidates
      remain visible in the report with reasons.
- [ ] Tickets default to `status: awaiting_review` unless explicit local write
      policy grants `status: todo` admission and no human/external gate remains.
- [ ] Live Notion writes include required relation readback; missing routing
      produces `routing_missing` or local-only output.
- [ ] The run did not invoke Goal, Pulse, workers, implementation, publication,
      outreach, unapproved spend, or an endless/background monitor.
