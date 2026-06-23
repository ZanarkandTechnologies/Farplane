---
kind: project-automations-index
status: draft
project: TODO
created_at: TODO
updated_at: TODO
framework_template_version: "0.2.0"
owner: project-pm-automation
canonical_manifest: farplane/automations.json
ledger: .farplane/state/run-ledger.json
bindings: farplane/bindings.md
---

# Project Automations

The canonical recurring automation manifest is
[automations.json](automations.json). This Markdown file is the human index and
compatibility pointer for older references that still load
`farplane/automations.md`.

## Lane Model

```text
pulse lane -> pulse-update
  interval: minutes/hours
  job: immediate attention, triage, reward reconciliation, one bounded action
  drift_against: active task + rhythm plan

rhythm lane -> rhythm-update
  interval: days
  job: day-range operating plan, priority lanes, ticket-drainer placement
  drift_against: horizon plan + current milestone

horizon lane -> horizon-update
  interval: n weeks, default n = 1
  job: strategy, original-goal drift, memory/context updates, scheduled actions
  drift_against: original goals + mission + current milestone
```

Legacy compatibility aliases:

```text
pm-heartbeat    -> pulse-update
daily-pm-plan   -> rhythm-update
weekly-pm-plan  -> horizon-update
```
