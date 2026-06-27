---
title: "Skill Hardening Workflow"
status: active
owner: interval-update
kind: workflow-reference
template_uses:
  skill-template: "0.3.2"
---

# Skill Hardening Workflow

## Context

Use this workflow when an interval needs to convert fresh execution feedback into
durable skill prevention. Weekly Interval is the default caller because enough
evidence has usually accumulated to separate repeated failures from one-off
noise.

This workflow selects and routes hardening. It does not edit skills directly
unless the parent interval explicitly enters a `skill-maintenance` subtask.

## Workflow Signature

```text
skill_hardening(context_bundle, review_window, planning_window,
                workflow_findings?, cap?)
  -> harden_skill_handoffs
   + eval_candidates
   + checklist_guardrails
   + improvement_tickets
   + processed_state_delta
   + deferred_learning
   + source_gaps

state: reads(context_bundle, tickets/**/progress.md, ticket closeout notes,
             pulse_reports, interval_reports, docs/TROUBLES.md?,
             docs/LESSONS.md?, eval/review/QA artifacts?);
       writes(parent_interval_update_report_section,
              optional .farplane/state/skill-maintenance/processed-learning.jsonl
              when the project uses processed-state idempotence)
gates: source_rows_deduped; cap_respected; no_raw_transcripts;
       owner_surface_named; harden_skill_handoff_clear;
       one_off_noise_deferred; processed_or_deferred_recorded
routes: skill-maintenance:harden_skill | eval | optimize-harness |
        gap-analysis | ticket delta | direct no-change
fails: invokes a compatibility drain; reprocesses old rows; deletes ledgers;
       spawns unbounded hardening work; treats every note as a skill bug
```

## Source Contract

Default sources from the context bundle:

- `tickets/**/progress.md` and closeout notes inside `review_window`.
- Pulse reports and interval reports inside `review_window`.
- `docs/TROUBLES.md` for raw repeated misses, blockers, and correction pain.
- `docs/LESSONS.md` for distilled prevention lessons.
- linked eval, QA, review, and proof artifacts.

Optional sources:

- processed-state records under `.farplane/state/skill-maintenance/`.
- skill-local audits when a learning row names a target skill.
- workflow findings from plan progress, ticket board drift, attention drift,
  goal drift, metric snapshot, or compounding leverage review.

## Todo List

- [ ] 1. Bind the learning window.
  - [ ] Confirm `review_window`, `planning_window`, and `cap`.
  - [ ] Read ticket progress logs, Pulse reports, interval reports, lessons,
        troubles, and linked proof artifacts.
  - [ ] Read processed-state records when present.
  - [ ] Mark missing optional sources as source gaps.
- [ ] 2. Normalize feedback.
  - [ ] Group findings by repeated failure, one-off blocker, proof gap,
        planning miss, skill ambiguity, eval gap, checklist gap, or unclear
        owner surface.
  - [ ] Pair related lesson and trouble rows when the lesson resolves the
        trouble.
  - [ ] Dedupe against processed-state and already-fixed evidence.
  - [ ] Exclude raw private transcript text from outputs and state.
- [ ] 3. Route actionable learning.
  - [ ] Route existing skill failures, unclear first-load behavior, missing
        gotchas, QA checklist gaps, eval-to-QA sync gaps, or registry drift to
        [skill-maintenance](../../../skill-maintenance/SKILL.md) with
        `mode: harden_skill`.
  - [ ] Route testable behavior claims to [eval](../../../eval/SKILL.md).
  - [ ] Route broad harness behavior gaps to
        [optimize-harness](../../../optimize-harness/SKILL.md).
  - [ ] Route unclear owner surfaces to
        [gap-analysis](../../../gap-analysis/SKILL.md) or a ticket delta.
  - [ ] Mark weak, duplicate, already-fixed, or ownerless findings as deferred
        instead of creating work.
- [ ] 4. Bound the work.
  - [ ] Default cap is 5 actionable hardening follow-ups per weekly run.
  - [ ] Prefer the smallest durable prevention change: eval row, gotcha,
        checklist guardrail, ticket, or compact skill edit.
  - [ ] Do not start implementation inside the interval report unless the
        caller explicitly invoked `skill-maintenance`.
- [ ] 5. Record the result.
  - [ ] Write harden-skill handoffs, eval candidates, improvement tickets,
        deferred learning, source gaps, and processed-state decisions into the
        interval report.
  - [ ] If processed-state idempotence is enabled, append sanitized records to
        `.farplane/state/skill-maintenance/processed-learning.jsonl`.

## Output

```text
harden_skill_handoffs:
  - edited_skill:
    evidence_refs:
    recommended_guardrail:
eval_candidates:
checklist_guardrails:
improvement_tickets:
processed_state_delta:
deferred_learning:
source_gaps:
```
