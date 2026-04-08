---
ticket_id: TASK-0032
title: strengthen anti-self-agreement review loop
phase: complete
status: done
owner: codex
priority: high
depends_on: []
blocked_by: []
ready: true
approval_required: false
created_at: 2026-04-08T01:54:29Z
updated_at: 2026-04-08T04:56:52Z
next_action: archived; use the new Review Packet and evidence-reviewer gates as the canonical Ralph completion path
last_verification: py_compile passed, ticket metadata passed, and Ralph smoke evals passed after adding timestamp-based staleness and fail-closed evidence-reviewer gate checks
linked_docs:
  - docs/specs/harness-techniques.md
  - docs/specs/review-gates.md
  - docs/specs/orchestrator-subagent-loop.md
  - tickets/README.md
  - docs/specs/ralph-judge-verdict.schema.json
---

# TASK-0032: strengthen anti-self-agreement review loop

## Summary
Harden the current review loop so the system is less likely to praise its own work, approve weak evidence, or stop after shallow QA.

## Scope
- In: stronger reviewer/evidence-check skepticism, stricter evidence thresholds, and a sharper repeat path when proof is weak
- Out: multi-ticket runtime or dispatcher work

## Plan

### Pitch
- `Req:` harden the live Ralph completion path so weak, contradictory, stale, or untraceable proof cannot pass as complete
- `Bet:` make the loop depend on a locked evidence bundle plus a narrow evidence-quality review pass, not just optimistic prose, checked boxes, or a generic review rubric sitting unused in docs
- `Win:` same-ticket repeats happen for bad proof automatically, and completion requires both checklist completeness and a passing evidence-quality gate

### B -> A
- `Before:` the live Ralph judge in `bin/stop_hook.py` mainly relies on `RALPH_RESULT` plus acceptance/evidence checkboxes, while the broader review surfaces already describe stronger evidence-quality concepts
- `After:` an evidence-collector subagent captures a higher-fidelity evidence bundle, an evidence-review subagent scores that bundle, and the Ralph judge only allows completion when both checklist proof and the evidence-quality packet pass
- `Outcome:` the highest-leverage false-pass seam is hardened without redesigning the entire review stack

### Delta
- `Touch:` `tickets/templates/ticket.md`, `tickets/README.md`, `agents/qa-tester.toml`, a narrow evidence-reviewer role prompt, `skills/review/SKILL.md`, `skills/review/references/review-rubric-index.md`, `docs/specs/review-gates.md`, `docs/specs/ralph-judge-verdict.schema.json`, `bin/stop_hook.py`, `experiments/run_ralph_smoke_evals.py`
- `Keep:` builder / reviewer / QA / evidence-check role separation and the broader `review` skill as the rich review surface
- `Change:` make the live Ralph judge consume a minimal canonical `Review Packet` projection backed by a higher-fidelity evidence bundle and an explicit evidence-review lane
- `Delete/Avoid:` adding a second stop-hook-only evidence schema or broadening this ticket into a full review-system rewrite

### Core Flow
```pseudo
evidence collector runs the ticket's declared test flow
collector locks a relevant evidence bundle:
  logs, errors, commands, snapshots, screenshots, and video-ready storyboard frames
evidence reviewer scores that bundle against evidence-quality and integration-readiness
write minimal Review Packet fields into the ticket
parse selected ticket at stop time
read acceptance/evidence checklist gaps
read minimal Review Packet fields from the ticket body
if blockers exist:
  block
if Review Packet is missing or malformed:
  repeat_ralph
if Review Packet says evidence is weak, contradictory, stale, or untraceable:
  repeat_ralph
if acceptance/evidence checklists still have gaps:
  repeat_ralph
otherwise:
  allow advance/complete path
```

### Proof
- `P1:` hermetic judge fixtures force `repeat_ralph` for missing packet, malformed packet, stale packet, contradictory packet, and low-traceability packet cases
- `P2:` a completion path only succeeds when checklist proof and `Review Packet` hard gates both pass
- `Risk:` contract sprawl or a second source of truth for review/evidence
- `Rollback:` keep the packet minimal and treat it as the single structured projection the Ralph judge consumes, with the evidence collector and evidence reviewer feeding that packet rather than inventing parallel verdicts

### Plan Review
- `Refs:` OpenAI evaluator/invariant emphasis, Anthropic hard evaluator thresholds, Cursor role separation, `review-gates.md`, `orchestrator-subagent-loop.md`, `skills/review`, `tickets/README.md`, `bin/stop_hook.py`
- `Scope:` the live Ralph judge path plus the ticket/review contract surfaces it consumes; not a whole-stack review redesign
- `Proof:` hermetic machine-readable fixture assertions in `experiments/run_ralph_smoke_evals.py`
- `Guardrails:` do not create a second review schema; do not let the thin stop-hook reviewer become authoritative for completion; keep the evidence-quality reviewer narrow and artifact-driven
- `Fixes:` architect review narrowed the seam and removed the extra-schema idea; critic review forced explicit packet fields, precedence rules, and fixture coverage; user clarified the need for a richer evidence collector plus separate evidence-review pass

### Delegation
- `Need:` yes
- `Why:` architect and critic review were used to harden the plan before approval
- `Artifact:` architect feedback on seam selection and source-of-truth design; critic feedback on packet contract, precedence, and proof coverage

### Ask
- `Ready: yes`
- `Next:` implement the minimal `Review Packet` contract plus Ralph-judge hard-fail rules

### Ticket Move
- `Now:` `status: done`, `phase: complete`
- `On approval:` n/a
- `Follow-ups:` may split broader `review` skill cleanup from the judge slice if the contract alignment grows beyond one commit
- `Blocked in building?:` no

## Acceptance Criteria
- [x] AC-1: the ticket template and canonical ticket docs define a minimal machine-readable `Review Packet` with required fields: `reviewed_at`, `overall_verdict`, `rerun_required`, `blocking_findings`, `next_action`, `evidence_quality`, and `integration_readiness`
- [x] AC-1a: the planning/QA contract defines a higher-fidelity evidence bundle for relevant test runs, including exact commands, detailed logs, snapshots, screenshots, and video-ready storyboard frames or equivalent sequential visual artifacts
- [x] AC-2: the live Ralph judge path in `bin/stop_hook.py` forces `repeat_ralph` when the `Review Packet` is missing, malformed, stale, contradictory, weak, or untraceable, even if checkboxes look complete
- [x] AC-3: the live Ralph judge only allows `complete_ticket` when both checklist proof and `Review Packet` hard gates pass
- [x] AC-4: the evidence collector and evidence-review roles are explicitly separated, with the reviewer scoring the collected bundle rather than recollecting proof
- [x] AC-5: the Stop hook can invoke a narrow evidence-quality reviewer subagent that returns rubric-backed gate fields for completion decisions
- [x] AC-6: hermetic smoke fixtures assert the machine-readable verdicts for missing packet, malformed packet, stale packet, contradictory packet, and low-traceability packet cases
- [x] AC-7: repeat paths surface concrete repair reasons instead of generic approval or self-congratulatory review language

## Working Notes
- Main weakness: the system still agrees with itself too easily.
- Blog technique mapping: Anthropic’s hard evaluator thresholds, Cursor’s clearer role separation, OpenAI’s emphasis on turning guardrails into real checks.
- The thin stop-hook `reviewer` role remains a routing fallback for ambiguous/no-`RALPH_RESULT` cases; this ticket should not make it a second independent source of completion truth.
- The canonical source of truth for this slice is one minimal `Review Packet` projection shared across ticket/spec/review surfaces, not a new stop-hook-only schema.
- The missing thing is not “another rubric file.” The missing thing is a mechanically consumed evidence packet backed by richer artifacts and a dedicated evidence-quality review pass.
- For relevant UI or user-story runs, the evidence bundle should be good enough to:
  - tell the full user story from logs plus screenshots
  - preserve snapshot state and detailed logs for debugging
  - produce a short video or storyboard without recollecting the run

## Inspiration
- Source: Ryan Lopopolo, "Extreme Harness Engineering for the 1B token/day Dark Factory" on Latent Space. Video: https://www.youtube.com/watch?v=CeOXx-XTYek
- Transcript: https://www.latent.space/p/harness-eng
- Relevant takeaway: failures should route back into harness improvements or concrete repair work, not be washed out by optimistic self-review.

### Higher-Fidelity Example

What exists today:

- The richer `review` skill already has:
  - a markdown workflow in `skills/review/SKILL.md`
  - rubric-family references in `skills/review/references/review-rubric-index.md`
  - hard-gate concepts like weak `evidence-quality` and weak `integration-readiness`
  - a `Review Packet` section in the ticket template
- But the live Ralph judge in `bin/stop_hook.py` mainly decides from:
  - `RALPH_RESULT`
  - acceptance checkboxes
  - evidence checkboxes
  - blockers
  - and only a thin stop-time routing reviewer outside the richer artifact bundle you actually want

What is missing:

- the judge does not yet treat the structured `Review Packet` as required completion input
- the evidence collector does not yet guarantee a locked, high-fidelity bundle for the exact relevant test run
- there is no separate evidence-review pass that scores the captured bundle and writes the gate fields back
- the canonical ticket docs do not yet fully define `Review Packet` as part of the enforced ticket contract
- there is no explicit precedence when:
  - checkboxes say complete
  - but review says evidence is weak or contradictory
- there is no hard failure rule for:
  - missing packet
  - malformed packet
  - stale packet
  - untraceable packet
- the replay suite does not yet assert these false-pass cases hermetically

Concrete today-vs-after example:

```text
Today:
1. Builder finishes and emits:
   RALPH_RESULT: status=build_complete next=building reason=done
2. QA uploads a screenshot or two plus a short note, and ticket checkboxes are all marked complete:
   - [x] AC-1
   - [x] Tests
   - [x] QA / manual verification
3. Review Packet says:
   - overall_verdict: revise
   - rerun_required: true
   - evidence_quality: weak
   - blocking_findings: ["Empty-state proof is missing; screenshots only cover happy path"]
4. Current judge path can still complete because it mainly sees the checked boxes and `build_complete`.

After this ticket:
1. Evidence collector runs the relevant test flow and locks:
   - exact commands run
   - detailed logs / errors
   - snapshots
   - storyboard-grade screenshots or short video-ready frame sequence
2. Evidence-review subagent scores that bundle and writes the minimal Review Packet:
   - evidence_quality: weak
   - integration_readiness: fail
   - rerun_required: true
   - blocking_findings: ["Empty state missing", "No traceable log for failure branch"]
3. The same ticket is parsed by the Ralph judge.
4. Judge reads checklist state AND the minimal Review Packet.
5. Judge sees:
   - evidence_quality: weak
   - rerun_required: true
6. Verdict becomes:
   - decision: repeat_ralph
   - reason: review packet marks evidence as weak
   - missing_evidence / blocking findings propagated
7. Ticket cannot complete until both:
   - checkboxes are complete
   - Review Packet hard gates pass
```

Why this is different from “we already have a review skill”:

- the `review` skill currently defines how a reviewer should think
- this ticket makes the live Ralph completion path mechanically depend on a high-fidelity evidence bundle plus structured review output
- without this ticket, review remains guidance; with this ticket, review becomes a hard gate in the judge
- without this ticket, the evidence artifacts themselves are still too loose to support a skeptical review or high-quality user-story playback

## Implementation Notes
- Touched areas: ticket/review contract docs, QA evidence bundle contract, narrow evidence-review role prompt, Ralph judge parsing/precedence, verdict schema, hermetic replay fixtures
- Reused patterns: current `review-gates` model, ticket-first progress surface, existing QA artifact conventions, existing Ralph smoke-eval harness
- Guardrails: avoid adding a new hidden orchestrator, duplicate evidence schema, or broad freeform stop-time reviewer

## Evidence
- [x] Tests
- [ ] Typecheck
- [ ] Lint
- [x] QA / manual verification
- Validation details:
  - ran `python3 -m py_compile bin/stop_hook.py experiments/run_ralph_smoke_evals.py tickets/scripts/check_ticket_metadata.py`
  - ran `python3 tickets/scripts/check_ticket_metadata.py`
  - ran `python3 experiments/run_ralph_smoke_evals.py` outside the sandbox because the tmux branch requires unrestricted local tmux access
  - confirmed new fixture coverage for missing packet, malformed packet, stale timestamp packet, contradictory packet, low-traceability packet, and valid-packet-plus-checkbox-gap cases
  - confirmed the no-`RALPH_RESULT` fallback still biases toward same-ticket continuation when the reviewer role is unavailable

## Review Packet
- `reviewed_at:` 2026-04-08 04:56 +0100
- `rubrics_used:` ["implementation-plan", "evidence-quality", "integration-readiness"]
- `overall_score:` 4.5
- `overall_threshold:` 4.0
- `overall_verdict:` pass
- `rerun_required:` false
- `evidence_quality:` pass
- `integration_readiness:` pass
- `traceability:` pass
- `freshness:` pass
- `hard_gate_failures:` []
- `blocking_findings:` []
- `next_action:` archive the ticket and use the new hook gates on future Ralph build/documenting completions

## Blockers
- none

## Handoff
- Current state: implemented and verified; the live Ralph judge now requires a passing Review Packet and can invoke a narrow evidence-reviewer role on the completion path.
- Resume from: `bin/stop_hook.py`, `agents/evidence-reviewer.md`, `tickets/templates/ticket.md`, `docs/specs/review-gates.md`, and `experiments/run_ralph_smoke_evals.py`

## Writeback
- Update this ticket as work progresses.
- If the ticket changes queue state, update `status` and `phase` in frontmatter. Do not move the file.
- When implementation and verification pass, move `phase` to `documenting`, write durable docs, then move the ticket into `tickets/archive/` or set `status: done` briefly if you intentionally keep a short-lived visible completion state first.
