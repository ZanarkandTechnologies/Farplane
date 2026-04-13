---
ticket_id: TASK-0070
title: add loop skill surface
phase: complete
status: done
owner: codex
priority: high
depends_on:
  - TASK-0060
blocked_by: []
ready: false
approval_required: false
created_at: 2026-04-13T20:41:00Z
updated_at: 2026-04-13T20:44:15Z
next_action: none; loop skill surface landed and the public docs now match the shipped runtime contract
last_verification: `python3 tickets/scripts/check_ticket_metadata.py`; `python3 bin/check_harness_invariants.py`; `python3 bin/check_doc_parity.py`; `git diff --check`
linked_docs:
  - README.md
  - docs/specs/runtime-surface.md
  - tickets/TASK-0060-define-loop-mode-separate-from-impl.md
---

# TASK-0070: add loop skill surface

## Summary
Ship the missing operator-facing `skills/loop` artifact for the `$loop` runtime
that landed in TASK-0060.

## Scope
- In:
  - `skills/loop/SKILL.md`
  - repo-standard `skills/loop/README.md` and `skills/loop/AGENTS.md`
  - public docs and durable memory updates needed so `$loop` is treated as a
    real live skill surface
- Out:
  - changing loop runtime semantics
  - widening loop v1 beyond the existing deterministic predicate contract
  - tmux-backed loop workers or new predicate families

## User Story
- `Actor:` Codexter operator using the public skill surfaces
- `Need:` a real visible `loop` skill artifact that matches the documented
  `$loop` control surface
- `Outcome:` the public contract is legible and the repo no longer claims a
  ghost skill that only exists in runtime code

## User Pain / JTBD
- `Current pain:` TASK-0060 was marked complete even though no `skills/loop`
  package existed
- `Why now:` the missing artifact was caught immediately and leaves the public
  skill story inconsistent

## Non-Goals
- `Do not solve:` a second planning pass for loop semantics, runtime changes,
  or a broader rework of control-skill discovery

## High-Fidelity Example
- `Example flow/artifact:` an operator can open `skills/loop/SKILL.md`, see the
  supported `done_when` contract and stop commands, and use `$loop` without
  reverse-engineering `bin/user_turn.py`

## What Good Looks Like
- `Quality bar:` the repo has a real `skills/loop` module, README canonical
  links point to it, and no live invariant or public-surface doc implies `$loop`
  without a matching skill artifact

## Proof Target
- `Reviewer-visible proof:` `skills/loop/*` exists, docs reference it, and the
  repo validators pass

## Plan

### Human

#### Decision
- `Req:` close the public-surface gap without reopening the loop runtime design
- `Best:` add the missing `skills/loop` package and align the visible docs with
  the already-shipped runtime contract
- `Why:` the runtime behavior is already implemented; the failure is missing
  artifact packaging and inconsistent repo truth
- `Tradeoff accepted:` this follow-up is mostly doc and skill packaging work,
  not a new runtime feature
- `Not chosen:` treating the runtime-only control surface as sufficient and
  leaving the public skill story inconsistent

#### Diagram
- `Required:` no
- `Legend:` keep | change | add | remove

#### Signature Sketch
- `skills/loop/SKILL.md / public operator contract`
- `README.md / canonical live-skill entrypoints`
- `docs/specs/harness-techniques.md / implemented-surface inventory`
- `docs/MEMORY.md / control-skill and public-skill invariants`

#### B -> A
- `Before:` `$loop` exists in runtime and docs, but not as a real skill module
- `After:` `$loop` has a visible skill package and the public story matches the
  shipped repo
- `Outcome:` less operator confusion and stronger ticket-completion truth

#### Proof
- `P1:` `skills/loop/SKILL.md` exists and is executable without reading runtime
  code first
- `P2:` README/inventory/memory surfaces reference the live skill package
- `Risk:` duplicate or contradictory wording between the skill and runtime docs
- `Rollback:` keep the skill contract narrow and copy only already-shipped v1
  behavior

#### Ask
- `Ready: yes`
- `Next:` implement the skill package and doc writeback directly

### Agent

#### Delta
- `Touch:` `skills/loop/*`, `README.md`, `docs/specs/harness-techniques.md`,
  `docs/MEMORY.md`, `docs/HISTORY.md`, `docs/TROUBLES.md`, and ticket writeback
- `Keep:` the existing loop runtime contract and stop-hook predicate behavior
- `Change:` public-surface packaging and durability of the loop skill story
- `Delete/Avoid:` inventing new runtime semantics or turning this into another
  planning ticket

#### Execution Plan
```pseudo
create a narrow follow-up ticket
author the loop skill package from the shipped runtime contract
sync the public docs and durable invariants
run repo validators
write the review packet and close the ticket
```

#### Risk / Rollback
- `Primary risk:` the skill text could drift from the actual parser/runtime
- `Containment:` ground the skill in current `bin/user_turn.py` and
  `bin/stop_hook.py` behavior only
- `Rollback:` trim the skill back to the minimal invocation and guardrails

#### Plan Review
- `Refs:` `tickets/TASK-0060-define-loop-mode-separate-from-impl.md`,
  `bin/user_turn.py`, `bin/stop_hook.py`, `docs/specs/runtime-surface.md`
- `Checks:` no new runtime semantics; public docs point to the real skill; the
  control-skill invariant includes `$loop`
- `Fixes:` close the artifact gap left by TASK-0060

#### Options Appendix
- `Option 1:` add a full `skills/loop` package now
- `Pros:` closes the public-surface gap cleanly
- `Cons:` requires follow-up writeback on multiple doc surfaces
- `Why not chosen:` chosen
- `Option 2:` leave `$loop` runtime-only and rewrite docs to stop calling it a
  skill
- `Pros:` fewer files
- `Cons:` conflicts with the repo's public skill-first surface pattern
- `Why not chosen:` keeps the operator story weak and inconsistent
- `Option 3:` reopen TASK-0060 and fold this work into it without a new ticket
- `Pros:` one fewer ticket
- `Cons:` hides the correction and weakens board traceability
- `Why not chosen:` the missing artifact is now distinct follow-up work

#### Delegation
- `Need:` Not needed
- `Why:` localized artifact and docs correction
- `Artifact:` n/a

#### Ticket Move
- `Now:` `status: done`, `phase: complete`
- `On approval:` already executed
- `Follow-ups:` none expected for loop v1 packaging
- `Blocked in building?:` no

## Acceptance Criteria
- [x] AC-1: `skills/loop/SKILL.md` exists and describes the shipped `$loop` v1
  contract
- [x] AC-2: repo-standard `skills/loop/README.md` and `skills/loop/AGENTS.md`
  exist
- [x] AC-3: README and current-state docs reference `skills/loop` as a live
  public skill surface
- [x] AC-4: ticket/doc/invariant validators pass after the writeback

## Working Notes
- This is a correction ticket created after the operator noticed that TASK-0060
  completed without a real `skills/loop` artifact.

## Implementation Notes
- Touched areas: `skills/loop/*`, `README.md`,
  `docs/specs/harness-techniques.md`, `docs/MEMORY.md`, `docs/HISTORY.md`,
  `docs/TROUBLES.md`, and `tickets/TASK-0060-define-loop-mode-separate-from-impl.md`
- Reused patterns: `skills/advise`, `skills/pr-splitting`,
  `docs/specs/runtime-surface.md`
- Guardrails: do not widen loop semantics beyond the shipped local predicate set

## Evidence
- [x] Tests
- [ ] Typecheck
- [ ] Lint
- [x] QA / manual verification
- `Commands:` `python3 tickets/scripts/check_ticket_metadata.py`; `python3 bin/check_harness_invariants.py`; `python3 bin/check_doc_parity.py`; `git diff --check`
- `Not run:` TypeScript/typecheck and app/runtime tests were not applicable for this skill-packaging and docs-only correction

## Review Packet
- `work_type:` `["skills","docs","workflow"]`
- `search_scope:` `{changed_files: ["tickets/TASK-0070-add-loop-skill-surface.md", "skills/loop/SKILL.md", "skills/loop/README.md", "skills/loop/AGENTS.md", "README.md", "docs/specs/harness-techniques.md", "docs/MEMORY.md", "docs/HISTORY.md", "docs/TROUBLES.md", "tickets/TASK-0060-define-loop-mode-separate-from-impl.md"], related_files: ["bin/user_turn.py", "bin/stop_hook.py", "docs/specs/runtime-surface.md"], invariants_checked: ["MEM-0029", "MEM-0038"], docs_checked: ["skills/review/references/review-rubric-index.md", "skills/review/references/user-intent-satisfaction.md", "skills/review/references/evidence-quality.md", "skills/review/references/integration-readiness.md", "skills/review/references/desloppify.md", "docs/specs/runtime-surface.md"]}`
- `reviewed_at:` `2026-04-13 21:44 +0100`
- `rubrics_used:` `["user-intent-satisfaction", "evidence-quality", "integration-readiness"]`
- `overall_score:` `4.5`
- `overall_threshold:` `4.0`
- `overall_verdict:` `pass`
- `rerun_required:` `false`
- `evidence_quality:` `pass`
- `integration_readiness:` `pass`
- `traceability:` `pass`
- `freshness:` `pass`
- `hard_gate_failures:` `[]`
- `finding_log:` `[]`
- `blocking_findings:` `[]`
- `next_action:` `archive this ticket when convenient; no further loop v1 packaging work is required`

  `rubric_sections:`
  {"name":"user-intent-satisfaction","score":4.6,"threshold":4.0,"pass":true,"dimension_scores":{"ask-fidelity":4.7,"outcome-completeness":4.4,"worth-it-feel":4.4,"impressiveness":4.3,"evidence-confidence":4.6},"findings":["The missing operator-facing `loop` artifact now exists and the README exposes it as a live execution surface.","The skill text stays tightly aligned to the shipped runtime contract instead of inventing a second `loop` story."],"next_action":"Keep future `$loop` docs changes grounded in `bin/user_turn.py`, `bin/stop_hook.py`, and `docs/specs/runtime-surface.md`."}
  {"name":"evidence-quality","score":4.3,"threshold":4.0,"pass":true,"dimension_scores":{"sufficiency":4.2,"reproducibility":4.3,"traceability":4.4,"consistency":4.4,"inspectability":4.3},"findings":["The correction is backed by concrete repo artifacts plus passing ticket, invariant, and doc-parity validators.","The ticket now records both the correction reason and the exact validation commands, so a reviewer can audit the change quickly."],"next_action":"If `$loop` runtime semantics change later, add targeted runtime tests or contract examples in the same ticket rather than relying on doc-only proof."}
  {"name":"integration-readiness","score":4.5,"threshold":4.0,"pass":true,"dimension_scores":{"integration_safety":4.6,"contract_correctness":4.5,"dependency_readiness":4.4,"coupling_risk":4.4,"merge_readiness":4.5},"findings":["The new skill package is additive and does not widen runtime behavior, keeping blast radius low.","The memory and canonical-doc surfaces now agree that `$loop` is both a public control skill and a real skill module."],"next_action":"Preserve the invariant that public skill surfaces should ship with matching `skills/<name>/` artifacts before marking similar tickets complete."}

## Blockers
- none

## Handoff
- Current state: complete. `skills/loop/` now exists, canonical docs point to
  it, and the repo validators pass.
- Resume from: archive this ticket or reopen only if `$loop` gains new runtime
  semantics that require expanding the skill contract.

## Writeback
- Update this ticket as work progresses.
- If the ticket changes queue state, update `status` and `phase` in frontmatter.
  Do not move the file.
- When implementation and verification pass, move `phase` to `documenting`,
  write durable docs, then move the ticket into `tickets/archive/` or set
  `status: done` briefly if you intentionally keep a short-lived visible
  completion state first.
