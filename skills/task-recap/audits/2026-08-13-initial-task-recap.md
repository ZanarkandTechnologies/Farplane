---
skill: task-recap
date: 2026-08-13
change_type: behavior
owner: skill-maintenance
status: draft
review_route: reviewer
before_ref: tickets/README.md
after_ref: skills/task-recap/SKILL.md
reasoning_basis: advise
proof_artifacts: []
eval_required: yes
---

# Skill Audit

## Change

- Before: a delayed reply depended on manually rediscovering a transcript and
  could lose evidence gaps, rejected paths, and the current user ask.
- After: `task-recap` creates one source-ranked resumption brief from a bounded
  task packet, scoped evidence, and available thread context.
- Why: task packets are canonical resume state; an operator needs a reply-ready
  explanation, not an unbounded summary.
- Tradeoff accepted: the skill reports an explicit source gap when durable
  context is unavailable instead of simulating continuity from a topic alone.

## First-Principles Reasoning

- Objective: restore enough trustworthy state to answer a paused task safely.
- Placement logic: a just-in-time reusable procedure belongs in a Tier 3 skill,
  not an always-loaded rule, hook, transcript store, or global memory pass.
- Expected behavior delta: facts, decisions, deltas, failed attempts, conflicts,
  and next action become traceable to named sources.
- Proof needed: static package checks, natural anti-spoiler eval rows, focused
  fixture run, installed-copy inspection, and independent review.

## Binary Rubric

| Check | Verdict | Evidence |
| --- | --- | --- |
| `first_load_sufficiency` | unknown | Pending contract review. |
| `reference_load_precision` | unknown | Pending contract review. |
| `missing_context_rate` | unknown | Pending focused eval. |
| `noisy_context_rate` | unknown | Pending structure review. |
| `duplicated_instruction_count` | unknown | Pending structure review. |
| `prompt_size_tokens` | unknown | Pending structure review. |
| `task_success_rate` | unknown | Pending focused eval artifact. |
| `review_tas_rate` | unknown | Pending reviewer receipt. |
| `maintenance_locality` | unknown | Pending registry sync. |
| `composition_clarity` | unknown | Pending contract review. |

## Proof Artifacts

- Skill-local evals, when needed: `evals/evals.json` with five source-coverage cases.
- Structure evals, when needed: `python3 skills/skill-maintenance/scripts/check_skills.py --write`.
- Reviewer receipt: pending at `tickets/TASK-0434/artifacts/review/`.
- Validator: pending JSON and anti-spoiler checks.
- Eval required: yes.
- Evidence gaps: no focused run artifact or installed-copy inspection yet.

## Before Behavior

- The ticket contract says transcripts are not canonical resume state, but no
  selected skill consistently turns the packet into a full response briefing.

## After Behavior

- A read-only source order, conflict rule, and output schema make task recovery
  repeatable without promoting stale status into completion proof.

## Followups

- `no_self_improve_reason`: this is a new baseline contract; collect real
  invocation/eval evidence before opening a measured self-improvement loop.
