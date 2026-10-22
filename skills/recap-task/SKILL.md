---
name: recap-task
description: "Use for \"catch me up\", \"where were we\", \"recap this task\" or \"play the idea back\": the problem and goal first, then a visual idea playback while shaping or a sourced task recap once work exists."
department: operations
source: local
capability:
  kind: shortcut
template_uses:
  skill-template: "0.6.2"
allowed-tools: Read, Glob, Grep, Bash
---

# Recap Task

## Context

Use this whenever the operator wants to know where a task stands: before a
brainstorm, after one, mid-build, or when returning to a paused task. Every
recap opens with the problem being solved and the goal it serves. While the
task is still being shaped, the recap plays the idea back as one visual model
so misunderstandings surface before requirements are written. Once a ticket,
plan, or change exists, it reconstructs the task from its durable records.
This is read-only: do not edit the task, send a message, or resume execution.

## Skill Signature

```text
recap_task(task_ref?, discussion?, focus?) -> problem_and_goal + (idea_playback | task_recap) + next
reads: conversation, ticket, Goal Packet, evidence, task-scoped changes, supplied artifacts
does: finds the task's stage, states the problem and goal, fills the stage's template
writes: none
returns: problem and goal, a proposed visual model or a source-linked recap, gaps, and one safe next posture
```

<!-- BEGIN FARPLANE_IMPORTANT_CHECKLIST -->
## Todo List

- [ ] **N1 — Resolve the task and its stage.**
  `task_ref + discussion + supplied paths -> source_packet + stage | source_gap`

  Rule: Prefer the issue body (ticket sections, `## Goal program`, `## Current
  Goal state`), then recent Goal turn comments, linked evidence, task-owned
  changes, and finally the conversation. Read every supplied path before
  calling it missing. The stage is `shaping` when only discussion exists (no
  accepted ticket, plan, or change) or the operator asks to see the idea
  played back; otherwise `work`. When neither a task
  boundary nor a discussion is reliable, stop with the `source-gap` template.

  Assert:
  - The stage and every source actually read are explicit.
  - Missing, unreadable, or stale context is named rather than reconstructed from memory.

- [ ] **N2 — State the problem and the goal.**
  `source_packet -> problem + goal + who_benefits`

  Rule: Name the problem in the user's terms (who hurts, and how) and the goal
  as the change in their experience or the outcome being reached. Mark each as
  confirmed, inferred, or still open. When the work has drifted from the
  original problem, say so here.

  Assert:
  - The recap's first lines say what problem is being solved and why it matters.
  - An inferred or contested goal is labelled, not stated as settled.

- [ ] **N3 — Shaping: play the idea back as one visual.**
  `stage=shaping + discussion -> alignment_question + template_id + proposed_visual_model`

  Rule: Frame the one thing the operator must confirm, keeping contradictions
  and open choices visible. Load [idea templates](references/idea-templates.md)
  and pick one view from that question: `journey`, `ui-screen-flow`,
  `lifecycle`, `system-boundary`, `before-after-example`, or
  `comparison-table`. Fill it with discussion-grounded nouns, actions, states,
  and uncertainty; draw it in Mermaid, published as a linked Artifact in
  Claude and inline elsewhere. No ASCII duplicate, second view, or
  implementation plan.

  Example: `dashboard redesign + "what will the lead see?" -> ui-screen-flow`,
  even when the discussion also mentions backend components.

  Assert:
  - The chosen view answers the operator's question rather than cataloguing the product.
  - UI flows include visible content, actions, and material loading, empty, error, or success states.
  - The model is labelled proposed and ends with one to three questions about the riskiest mismatches.

- [ ] **N4 — Work: reconcile what is true now.**
  `stage=work + source_packet -> current_state + delta + attempts + conflicts + freshness`

  Rule: Keep implementation, verification, review, and user acceptance
  separate. A checked box or changed file is not runtime proof. For worktree
  captures, name task-owned paths, excluded noise, the capture time, and that
  the snapshot is historical.

  Example: `fix implemented + unit pass + missing operated receipt -> partial`,
  never "fixed."

  Assert:
  - Before, After, and one supported Example describe any material delta.
  - Each important attempt keeps its symptom, action, observed result, disposition, and remaining impact.

- [ ] **N5 — Render the smallest safe template.**
  `stage + state + caller_need -> idea | quick | full | source-gap`

  Rule: Load [recap templates](references/templates.md). Use `idea` for the
  shaping stage. Use `quick` only when the work packet is coherent; a requested
  full recap, proof conflict, or material failed attempt must select `full`.
  Use `source-gap` when N1 cannot bind reliable evidence. Fill templates with
  task facts, preserve the latest user question and accepted and rejected
  decisions, and end with one safe reply posture, decision, or source request.

  Assert:
  - Every template begins with `Problem & goal`; work templates follow with `Now`, `Delta`, and `Risks & action`.
  - Full mode includes every template section and lists each literal source path on its own ledger bullet before `Safe next`.
  - The recap does not execute work or claim evidence that the packet does not contain.
<!-- END FARPLANE_IMPORTANT_CHECKLIST -->

## Gotchas

- A recap that starts with status and never names the problem has failed, even when every fact is right.
- Architecture is the wrong idea view when the operator asks what an end user sees.
- A polished diagram must not silently resolve a contradiction or open choice; generated prose is not evidence.
- A timeline shows order; an attempt trace shows why a path worked, failed, or was rejected. Full mode may need both.
- Do not treat an old `git status` capture as live state or unrelated changes as task evidence.
- Do not compress a proof conflict into a reassuring summary.

## Reference Map

- [Recap templates](references/templates.md) — load at N5.
- [Idea templates](references/idea-templates.md) — load at N3, shaping stage only.
- [Ticket and Goal Packet contract](../../tickets/README.md) — load when a ticket or Goal Packet is present.

## Output

Return `Problem & goal`, then a filled idea, quick, full, or source-gap
template, then one safe next posture. Keep literal source paths in full mode.
Write nothing.
