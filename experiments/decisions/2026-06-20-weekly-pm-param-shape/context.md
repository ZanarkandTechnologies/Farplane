---
kind: council-context
decision: weekly-pm-param-shape
created_at: 2026-06-20
owner: deliberative-advice
status: draft
---

# Weekly PM Parameter Shape Council Context

## Decision

Decide how Kenji's current `weekly-strategy-analysis` automation should become
a call to the generic `weekly-pm-plan` without maintaining two skills or
creating an overly large parameter/profile system.

## Why This Matters

The operator wants one maintainable weekly planning surface. Too many params
are hard to manage; a separate profile file may become another artifact to
remember. The automation should express the specialization at the call site
when possible.

## Prior Discussion Summary

- `weekly-pm-plan` is the generic weekly strategy skill.
- `weekly-strategy-analysis` is currently a personal/Kenji-specific weekly
  strategy skill and live automation.
- The desired direction is to retire the separate skill and represent Kenji's
  weekly planning as a parameterized call to `weekly-pm-plan`.
- The operator prefers not to split the config into a separate profile file if
  the automation can express the function call cleanly.

## Current Behavior

- Live automation:
  `/Users/kenjipcx/.codex/automations/weekly-opportunity-deep-research/automation.toml`
  calls `weekly-strategy-analysis` with a long prompt.
- Generic skill:
  `skills/weekly-pm-plan/SKILL.md` accepts `context_refs`, reports, policy, and
  window, and now owns report/context templates plus goals promotion.

## Expected Behavior

The live automation should be expressible as a call such as:

```text
weekly_pm_plan.strategy(
  project_root = ...,
  context_refs = ...,
  mode = ...,
  lanes = ...,
  report_shape = ...,
  guardrails = ...,
  instructions = ...
)
```

The call should avoid a broad external profile object unless reuse pressure
appears.

## Options Under Consideration

1. Separate profile file: `profiles/kenji-weekly-strategy.md`.
2. Inline automation function call with a compact `profile { ... }` object.
3. Minimal inline call with only 4-6 semantic params and one `instructions`
   block for specialization.

## Evidence Refs

- `skills/weekly-pm-plan/SKILL.md`
- `farplane/automations.md`
- `/Users/kenjipcx/.codex/automations/weekly-opportunity-deep-research/automation.toml`
- `skills/weekly-strategy-analysis/SKILL.md`

## Constraints / Non-goals

- No two long-term weekly strategy skills.
- Avoid too many named params.
- Avoid hidden profile state when the automation call can be self-contained.
- Do not lose source-specific details: Notion, meetings, Codex drift,
  opportunity scan, privacy gates, report order.
- Do not mutate live automation in this advice-only decision.

## Lane Briefs

- Operator value: minimize maintenance and make the live automation readable.
- Engineering risk: keep enough structure for compilation, eval, and future
  migration.
- Systems fit: put generic behavior in `weekly-pm-plan`; keep call-site
  specialization local to the automation.
- Evidence skeptic: resist overfitting the parameter system before there are
  multiple consumers.

## Output Shape

- Recommendation.
- Strongest dissent.
- Function signature.
- Suggested automation call shape.
- Next owner.
