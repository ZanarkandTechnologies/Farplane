---
kind: council-context-packet
decision: automation-manifest-compactness
created_at: 2026-06-20
status: draft
owner: deliberative-advice
---

# Automation Manifest Compactness Council Context

## Decision

Should `farplane/automations.md` remain a detailed recurring-program runbook,
or should it become a compact cadence manifest that delegates job behavior to
skills and job presets?

## Why This Matters

`farplane/automations.md` is the project source of truth for recurring
automation. If it grows into a duplicated runbook, every skill behavior change
requires updating this file, compiled Codex automations, and the skill itself.
If it becomes too terse, automations may lose enough local contract to run
safely.

## Prior Discussion Summary

Recent design moved Farplane toward cadence-separated automation threads:
weekly PM for strategy and upkeep, daily ticket drainer for ticket selection
and child-thread handoff, and child executor threads for leaf work. The latest
question is whether the manifest now contains too much repeated job detail,
especially for skill hardening, refinement, registry drift, strategy, and
ticket updates.

## Current Behavior

- `farplane/automations.md` is 356 lines.
- It defines project settings, gates, report paths, a cadence thread contract,
  seven `job` blocks, two `cadence` blocks, and the run-ledger contract.
- Job blocks repeat `intent`, `skill`, `freshness`, `reads`, `writes`, and
  `output`.
- Live Codex automation TOML prompts are compiled from the manifest and carry
  a full todo list.

## Expected Behavior

The manifest should preserve:

- project identity and gates
- schedules and target threads
- cadence grouping
- freshness/cache policy
- report handles
- cross-cadence handoff contract
- live automation compile inputs

Reusable job behavior should live in skills or a compact preset catalog unless
the project needs an explicit local override.

## Options Under Consideration

1. Keep the detailed manifest as-is.
2. Make `automations.md` a compact manifest and move job details to skills or
   job presets.
3. Split into `automations.md` plus a separate `automation-jobs.md` runbook.

## Evidence Refs

- `farplane/automations.md`
- `skills/skill-maintenance/SKILL.md`
- `skills/feed-scout/SKILL.md`
- `skills/goal-advisor/SKILL.md`
- `skills/impl-plan/SKILL.md`

## Relevant Files

- `farplane/automations.md`
- `.codex/automations/farplane-ticket-update/automation.toml`
- `.codex/automations/farplane-weekly-pm-update/automation.toml`
- `docs/farplane-framework/README.md`

## Constraints / Non-Goals

- Do not remove the manifest as the source of truth for schedules and cadence
  grouping.
- Do not hide side-effect gates inside skills.
- Do not require every automation prompt to rediscover basic project policy.
- Do not implement the refactor before the shape is chosen.

## Lane Briefs

- Operator value: reduce cognitive load and make the file pleasant to edit.
- Engineering risk: preserve enough explicit contract for compiled automations.
- Evidence skeptic: challenge whether verbosity is harmful or just visible.
- Systems fit: decide which surface owns skill behavior versus cadence wiring.

## Output Shape

Return a council decision note with recommendation, dissent, confidence,
tradeoff, next owner, and proof path.

## Proof / Next Owner

If accepted, next owner is a small direct Farplane docs/config refactor:
compact `farplane/automations.md`, introduce reusable `job_catalog` or
skill-owned job presets, then recompile the two live Codex automations.
