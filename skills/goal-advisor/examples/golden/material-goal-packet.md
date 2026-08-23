---
title: Golden material Goal Packet architecture
status: active
owner: goal-advisor
kind: golden-example
---

# Compile a material UI ticket into a Goal

## Input and context

- Request: “Implement TASK-0421, CSV export for the customer table.”
- Sources: an approved ticket, `program.md`, `progress.md`, `design.md`, and a
  QA Strategy requiring browser capture, visual QA, and completion review.
- State: ticket `updated_at` matches the compiled packet; no deploy or spend is
  authorized; the final CSV workflow has not run yet.

## Accepted output

```text
Goal Architecture: active_goal over one approved coding leaf
Files:
- tickets/TASK-0421/ticket.md
- tickets/TASK-0421/program.md
- tickets/TASK-0421/progress.md
- tickets/TASK-0421/design.md
Trigger: native Goal, one uninterrupted 90-minute window
Metric: ticket critical-path checks + delegated QA/review; no proxy-only finish
Drift Policy: compare ticket/program/progress after each turn
QA Proof Route: qa-tester captures CSV workflow and screenshot -> visual-qa
judges design fidelity -> reviewer judges evidence sufficiency
Compiled Execution Path:
  S1 customer table -> Change 1 expose export action -> D1 action visible
  S2 export request -> Change 2 generate CSV -> D2 correct rows and columns
  S3 download complete -> Change 3 browser delivery -> D3 operated download
  F1 export failure -> Change 3 recovery state -> D4 visible retry path
Reference Manifest:
  ticket.md -> all nodes; owns scope and Done / Proof
  program.md -> loop; owns order, drift, and stopping
  progress.md -> writeback; owns observations and evidence chronology
  design.md -> S1/S3/F1 + visual-qa; owns UI state baseline
Completion Closure:
  D1 -> Change 1 -> screenshot compared with design.md -> pending
  D2 -> Change 2 -> focused CSV assertions -> pending
  D3 -> Change 3 -> operated download trace -> pending
  D4 -> Change 3 -> failure-state capture compared with design.md -> pending
Approval: approved; packet compiled from ticket updated_at 2026-07-16T14:20:00Z
Native Goal Prompt:
  Files: [the four paths above]
  Task: satisfy TASK-0421 scope and Done / Proof.
  Program: read program.md first; it owns budget, proof, drift, and stop policy.
  After each turn: append observations to progress.md and continue, revise, or
  block from file-backed state.
  Completion: run ordered sanity checks, the real CSV workflow, ticket
  validation, QA evidence review, and completion review before stop_complete.
Next Action: start the approved Goal; block if packet freshness changes.
```

## Why it passes QA

- The launcher cites compact file-backed truth and records packet freshness.
- Diagram nodes, changes, exit assertions, and evidence form one traceable path;
  no Done claim floats free of an implementation owner or proof source.
- Every non-core reference has a named consumer, so stale and ornamental refs
  are detectable before execution.
- Proof route, no-self-certification, critical path, and final checkpoint are
  explicit; missing real-workflow evidence cannot be hidden by unit tests.
- Budget, authority boundary, drift, logging, and approval are inspectable.

## Tempting negative

`/goal Work on CSV export until the tests pass. Use the discussion above for
requirements and report when done.`

Why it fails: it hides files in transcript memory, omits `program.md`, approval,
freshness, delegated QA, the real workflow, and the completion checkpoint.

## Transferable invariants

- Material Goals are compact launchers over approved, fresh Goal Packet files.
- The ticket owns scope/proof; the program owns execution policy; progress owns
  observations. Do not duplicate those contracts in prompt prose.
- Name honest metric, authority, drift, delegated proof, and stop conditions.

## Non-copyable facts and wording

- TASK-0421, CSV export, file names beyond the standard packet, timestamps,
  budget, and lane chain are fixture-specific.
- Compile fresh paths and wording from the current ticket and QA Strategy.

## Proof receipt

```yaml
golden_case: goal-advisor/material-goal-packet
source_refs:
  - skills/goal-advisor/SKILL.md
  - skills/goal-advisor/SKILL.md
qa_refs: [file-list-compactness, no-self-certification, critical-path-proof, final-completion-checkpoint]
accepted_because: [fresh_packet, compact_launcher, delegated_proof, explicit_stop_gate]
decisive_nodes: [compiled_execution_path, reference_manifest, completion_closure]
no_skill_comparison: "A generic launcher would preserve the polished prose but miss the stale design, orphan refs, and unsupported Done rows."
heldout_required: true
review_excludes: planner_scratch_reasoning
```
