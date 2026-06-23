---
kind: project-automations-index
status: active
project: Farplane
created_at: 2026-06-15
updated_at: 2026-06-22
framework_template_version: "0.2.0"
owner: project-pm-automation
canonical_manifest: farplane/automations.json
ledger: .farplane/state/run-ledger.json
bindings: farplane/bindings.md
---

# Farplane Project Automations

The canonical recurring automation manifest is now
[automations.json](automations.json). This Markdown file is the human index and
compatibility pointer for older references that still load
`farplane/automations.md`.

## Lane Model

Farplane automation is organized by context-isolated lanes, not calendar-named
loop identities.

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

Legacy names remain compatibility aliases during migration:

```text
pm-heartbeat    -> pulse-update
daily-pm-plan   -> rhythm-update
weekly-pm-plan  -> horizon-update
```

## Compiler

Structured JSON does not remove the compiler. It narrows the compiler's job:

```text
compile_lane_automation(lane_json, skill_catalog, reports, gates)
  -> prompt(program, ordered_todo, side_effect_gates, final_output_fields)
```

The compiler turns explicit lane config into live Codex automation prompts with
the exact todo list, target thread, report paths, freshness rules, gates, and
due scheduled actions. It must not become a hidden scheduler, daemon, or cloud
runner.

Quarterly, yearly, and other intervals greater than one week are scheduled
actions inside `horizon-update` by default. Add a separate persistent lane only
after repeated horizon reports prove the horizon context cannot handle that
decision shape.
