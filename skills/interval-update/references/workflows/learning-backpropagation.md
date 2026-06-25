---
title: "Learning Backpropagation Workflow"
status: active
owner: interval-update
kind: workflow-reference
template_uses:
  skill-template: "0.3.2"
---

# Learning Backpropagation Workflow

## Context

Use this workflow when an interval needs to convert qualitative execution
feedback into durable harness improvements. It replaces the old standalone
learning-drain compatibility path. Weekly Interval is the default caller
because enough evidence has accumulated to distinguish one-off noise from
repeatable skill, eval, checklist, ticket, or process updates.

This workflow selects and routes learning. It does not edit skills directly
unless the parent interval explicitly enters a `skill-maintenance` subtask.

## Workflow Signature

```text
learning_backpropagation(context_bundle, review_window, planning_window,
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
fails: invokes legacy learning-drain; reprocesses old rows; deletes ledgers;
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
  - [ ] Route testable behavior claims to [eval](../../eval/SKILL.md).
  - [ ] Route broad harness behavior gaps to
        [optimize-harness](../../optimize-harness/SKILL.md).
  - [ ] Route unclear owner surfaces to
        [gap-analysis](../../gap-analysis/SKILL.md) or a ticket delta.
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

## Templates

Harden-skill handoff:

```text
edited_skill:
expected_behavior:
current_behavior:
evidence_refs:
lesson_or_trouble_refs:
mode: harden_skill
recommended_guardrail:
proof_required:
```

Learning row:

```text
- finding:
  source_refs:
  class: repeated_failure | proof_gap | planning_miss | skill_ambiguity |
         eval_gap | checklist_gap | one_off | unclear_owner
  owner_route:
  disposition: harden_skill | eval | optimize_harness | ticket_delta |
               deferred | no_change
  reason:
```

## Gotchas

- Do not call `learning-drain`; this workflow is the active feedback updater.
- Do not use append-only ledgers as a todo list. Keep processing state separate.
- Do not harden a skill from one ambiguous anecdote unless the failure is high
  severity and the guardrail is cheap.
- Do not let weekly backpropagation create an unbounded improvement queue.

## Reference Map

- Parent interval update loads this file only when
  `report_workflows.learning_backpropagation` is enabled.
- [skill-maintenance](../../../skill-maintenance/SKILL.md) owns
  `harden_skill`, eval/gotcha/checklist updates, registry sync, and proof.
- [../../../../docs/specs/minimal-autonomy-loop.md](../../../../docs/specs/minimal-autonomy-loop.md)
  defines the overall Pulse/Daily/Weekly feedback loop.

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
