---
skill: recap-task
date: 2026-08-13
change_type: behavior
owner: skill-maintenance
status: pass
review_route: reviewer
before_ref: tickets/README.md
after_ref: skills/recap-task/SKILL.md
reasoning_basis: advise
proof_artifacts:
  - .farplane/evals/runs/20260813-085123-task-0434-recap-task-final/summary.json
  - tickets/TASK-0434/artifacts/proof/2026-08-13-validation.md
  - tickets/TASK-0434/artifacts/review/2026-08-13-rereview.md
eval_required: yes
---

# Skill Audit

## Change

- Before: a delayed reply depended on manually rediscovering a transcript and
  could lose evidence gaps, rejected paths, and the current user ask.
- After: `recap-task` creates one source-ranked resumption brief from a bounded
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
| `first_load_sufficiency` | pass | The signature, source order, conflict gate, read-only boundary, todo path, proof, and output are present in `SKILL.md`. |
| `reference_load_precision` | pass | The ticket contract, runtime QA, and eval cases each have a specific load condition in `Reference Map`. |
| `missing_context_rate` | pass | `recap_task_names_missing_durable_context_01` received A in the final five-case suite. |
| `noisy_context_rate` | pass | The default path is five top-level todos; examples and full cases live beside the package. |
| `duplicated_instruction_count` | pass | Source hierarchy and runtime checks have one owner each in `SKILL.md` and `qa_checklist.md`. |
| `prompt_size_tokens` | pass | The compact first-load contract retains only routing, source order, output, and guards. |
| `task_success_rate` | pass | Final behavioral suite: 5/5 A at `.farplane/evals/runs/20260813-085123-task-0434-recap-task-final/summary.json`. |
| `review_tas_rate` | pass | Independent rereview returned TAS-A after proof writeback; receipt: `tickets/TASK-0434/artifacts/review/2026-08-13-rereview.md`. |
| `maintenance_locality` | pass | `check_skills.py --write` regenerated the recap-task registry row and all structural checks passed. |
| `composition_clarity` | pass | The signature names one resumption brief, read-only state, gates, failure modes, and routes. |

## Proof Artifacts

- Skill-local evals: final five-case A suite at `.farplane/evals/runs/20260813-085123-task-0434-recap-task-final/summary.json`. An initial four-of-five run exposed a missing dated, source-labeled timeline; the focused repaired case passed at `.farplane/evals/runs/20260813-084902-task-0434-recap-task-timeline-repair/summary.json` before the final full rerun.
- Structure checks: `python3 skills/skill-maintenance/scripts/check_skills.py --write`, JSON parse, ticket metadata, diff whitespace, and eval-query lint all passed; receipt: `tickets/TASK-0434/artifacts/proof/2026-08-13-validation.md`.
- Installed copy: `bash install.sh --skills-only --skills recap-task --target /Users/kenjipcx/.codex` completed and `diff -ru skills/recap-task /Users/kenjipcx/.codex/skills/recap-task` was empty; receipt: `tickets/TASK-0434/artifacts/proof/2026-08-13-validation.md`.
- Reviewer receipt: initial TAS-B review required evidence writeback; the
  reconciled packet received TAS-A at
  `tickets/TASK-0434/artifacts/review/2026-08-13-rereview.md`.
- Validator: pass.
- Eval required: yes.
- Evidence gaps: no gaps in behavior/installation evidence; independent rereview is the final gate.

## Before Behavior

- The ticket contract says transcripts are not canonical resume state, but no
  selected skill consistently turns the packet into a full response briefing.

## After Behavior

- A read-only source order, conflict rule, dated source-labeled chronology, and
  output schema make task recovery repeatable without promoting stale status
  into completion proof.

## Followups

- `no_self_improve_reason`: this is a new baseline contract; collect real
  invocation/eval evidence before opening a measured self-improvement loop.
