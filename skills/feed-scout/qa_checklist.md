---
title: Feed Scout QA Checklist
owner: feed-scout
status: active
kind: qa-checklist
applies_to:
  - feed-scout
  - feed-scout-report
  - source-backed-candidate-handoff
---

# Feed Scout QA Checklist

Use before discovery and again before returning the source report.

```text
feed_scout_check(report, items, candidates, recovery_tickets) -> pass | violation | source_gap
```

## Checklist

- [ ] The run is explicit and bounded; sources are configured, validated,
      normalized, canonical-keyed, and deduped before extraction or scouting.
- [ ] Fetched content is treated as untrusted evidence and each promoted item
      cites a canonical URL/key, extraction path, and today-specific delta.
- [ ] A dated Feed Scout report with Core frontmatter exists before candidate
      handoff.
- [ ] Every surfaced candidate records source evidence, active-ticket dedupe,
      executable scope, Reward, proof, stop condition, and unresolved authority
      gates; rejected candidates remain visible with reasons.
- [ ] Every created ticket is a capped, deduped, KPI/guard-linked direct recovery
      for an existing failure with known correction and no experiment debt.
- [ ] Opportunity, new-direction, and uncertain findings remain candidates;
      Feed Scout created no experiment ticket, Notion task, or Goal Packet.
- [ ] The run did not invoke Goal, Pulse, workers, implementation, publication,
      outreach, unapproved spend, or an endless/background monitor.
