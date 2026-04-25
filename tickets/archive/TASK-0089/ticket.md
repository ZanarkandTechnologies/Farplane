---
ticket_id: TASK-0089
title: make execution routing answer plan or act
phase: complete
status: done
owner: codex
claimed_by:
priority: high
depends_on: []
blocked_by: []
ready: true
approval_required: false
created_at: 2026-04-23T20:55:00Z
updated_at: 2026-04-25T00:42:00Z
next_action: none; action-first routing and planning contract landed, archived locally, push not requested
last_verification: 2026-04-25 01:42 +0100 final closeout checks and review passed; `python3 tickets/scripts/check_ticket_metadata.py`; `python3 bin/check_doc_parity.py`; `python3 bin/check_harness_invariants.py`; `git diff --check -- AGENTS.md templates/global/AGENTS.md docs/HISTORY.md docs/MEMORY.md docs/TROUBLES.md docs/specs/harness-techniques.md skills/repent/SKILL.md skills/impl-plan/AGENTS.md skills/impl-plan/README.md skills/impl-plan/SKILL.md skills/impl-plan/todos.md skills/impl-plan/prompts/plan.md skills/impl-plan/references/template.md skills/impl-plan/references/examples.md skills/impl-plan/references/review.md skills/impl/SKILL.md skills/impl/README.md skills/impl/todos.md skills/review/SKILL.md skills/review/references/review-rubric-index.md skills/review/references/implementation-plan.md skills/review/references/spec-contract.md tickets/templates/ticket.md tickets/archive/TASK-0089/ticket.md`; review artifact `tickets/archive/TASK-0089/artifacts/review-2026-04-25-0142+0100.json`
linked_docs:
  - AGENTS.md
  - templates/global/AGENTS.md
  - docs/specs/spec-first-execution-loop.md
  - docs/specs/orchestrator-subagent-loop.md
  - docs/specs/harness-techniques.md
  - skills/repent/SKILL.md
  - skills/impl/SKILL.md
  - skills/impl-plan/SKILL.md
  - skills/review/SKILL.md
  - skills/review/references/review-rubric-index.md
  - skills/review/references/implementation-plan.md
  - skills/review/references/spec-contract.md
  - tickets/templates/ticket.md
---

# TASK-0089: make execution routing answer plan or act

## Summary
Strengthen the harness so each user turn resolves cleanly into `answer`,
`plan`, or `act`, with direct concrete requests defaulting to execution and
with complaint-shaped missed-work prompts defaulting to recovery instead of
literal explanation-first replies.

## Scope
- In:
  - a compact answer/plan/act routing doctrine
  - stronger action bias for direct user asks
  - complaint-shaped correction handling such as "why are we not doing that"
  - skill-level `todos.md` loading as default prompt scaffolding
  - action-ordered ticket plans with explicit execution steps
  - aligned global and repo-local instruction updates where needed
  - reviewable examples of ambiguous versus direct requests
- Out:
  - a full autonomy dispatcher that selects across the whole board
  - a generic intent classifier service
  - changing the core ticket state machine

## Plan
- `Change:` tighten the shipped routing contract so the harness classifies turns
  into `answer`, `plan`, or `act`, treats complaint-shaped correction prompts
  as recovery-first by default, loads skill `todos.md` checklists early, and
  makes ticket plans carry ordered execution steps
- `Why:` the current harness already gestures toward action bias, but it still
  leaves too much nuance implicit for highly instruction-following GPT models
  that will answer the literal question instead of recovering the missed work
- `Before -> After:` before, the contract said corrections should usually be
  treated as fix-now requests but did not name the challenge-shaped phrasings,
  did not teach the model to load skill todo lists by default, and did not make
  plan action order explicit; after, the routing contract names those cases,
  skill checklists become a default scaffold, and ticket plans show concrete
  ordered steps
- `Touch:` `templates/global/AGENTS.md`, `skills/impl-plan/SKILL.md`,
  `skills/impl-plan/AGENTS.md`, `skills/impl-plan/README.md`,
  `skills/impl-plan/todos.md`, `skills/impl-plan/prompts/plan.md`,
  `skills/impl-plan/references/template.md`,
  `skills/impl-plan/references/review.md`,
  `skills/impl-plan/references/examples.md`, `skills/impl/SKILL.md`,
  `skills/impl/README.md`, `skills/impl/todos.md`, `skills/review/SKILL.md`,
  `skills/review/references/review-rubric-index.md`,
  `skills/review/references/implementation-plan.md`,
  `skills/review/references/spec-contract.md`, `tickets/templates/ticket.md`,
  `docs/specs/harness-techniques.md`, `docs/MEMORY.md`, `docs/TROUBLES.md`,
  `docs/HISTORY.md`, `AGENTS.md`
- `Inspect:` `templates/global/AGENTS.md`, `docs/TROUBLES.md`,
  `docs/MEMORY.md`, `skills/repent/SKILL.md`, `skills/impl-plan/SKILL.md`,
  `skills/impl-plan/README.md`, `skills/impl/SKILL.md`,
  `skills/review/SKILL.md`, `tickets/templates/ticket.md`,
  `docs/specs/spec-first-execution-loop.md`, `docs/specs/harness-techniques.md`
- `Signature delta:`
  - `templates/global/AGENTS.md / routeTurn(turn): answer | plan | act`
  - `templates/global/AGENTS.md / recoverCorrection(turn): recover | explain | ask`
  - `skills/impl-plan/SKILL.md / plan(ticket): TicketPlan`
  - `tickets/templates/ticket.md / planFields(...): PlanSection`
- `Type Sketch:`
  - `TurnMode = "answer" | "plan" | "act"`
  - `CorrectionCheck { reality: "true_miss" | "false_alarm" | "ambiguous", next: "recover" | "show_evidence" | "ask" }`
  - `PlanSection { signatureDelta?: string[], typeSketch?: string[], typedFlowExample?: string[], executionSteps?: string[] }`
- `Typed flow example:`
  - `UserTurn("why are we not doing that") -> TurnMode("act") -> CorrectionCheck("true_miss","recover") -> brief apology -> perform missing task`
  - `SkillUse("impl-plan") -> load SKILL.md -> load todos.md -> draft PlanSection.executionSteps -> write ticket plan`
- `Execution steps:`
  - inspect the current global correction-recovery and skill-loading wording
  - patch the shipped global contract so complaint-shaped prompts trigger a
    recovery-first reality check and skill todo lists load by default
  - patch the canonical ticket-plan surfaces so `Execution steps` become a
    first-class plan field
  - update memory, troubles, history, and this ticket so the rationale is
    visible and durable
  - run targeted validation and a final review pass against the changed
    contract surfaces
- `Recommendation:` fix prompt interpretation, skill checklist loading, and
  plan action order together instead of trying a prompt-only tweak
- `Options considered:`
  - `Option 1:` patch only the global correction wording
    - `Pros:` smallest diff
    - `Cons:` still leaves plan execution order implicit and skill scaffolding
      inconsistent
    - `Why not chosen:` it would fix one symptom without fixing the scaffolds
      the model actually follows
  - `Option 2:` add a new recovery skill or hidden routing template
    - `Pros:` stronger specialized behavior
    - `Cons:` adds another surface to remember and does not improve the default
      contract
    - `Why not chosen:` the miss is in the default contract, so the fix should
      land there first
  - `Option 3:` strengthen the shipped global contract and the canonical
    planning surfaces together
    - `Pros:` fixes interpretation and execution scaffolding at the same time
    - `Cons:` touches several prompt/doc files
    - `Why not chosen:` n/a
- `Blast radius:` future direct-recovery turns, all `impl-plan` tickets, and
  skill-driven workflows will read more action-oriented and more step-based
- `Risks:` the recovery rule could become too aggressive if the ambiguity
  escape hatch is not kept explicit, or `Execution steps` could turn into busy
  work if enforced on trivial fixes

## Acceptance Criteria
- [ ] AC-1: the main instruction surfaces define when the harness should
      answer, plan, or act
- [ ] AC-2: direct concrete user requests default to execution unless ambiguity
      or safety requires otherwise
- [ ] AC-3: challenge-shaped complaints about missed current-task work trigger a
      recovery-first interpretation instead of literal Q&A by default
- [ ] AC-4: the shipped global contract tells the model to load skill
      `todos.md` checklists when they exist
- [ ] AC-5: canonical ticket plans include ordered `Execution steps` for
      non-trivial work

## Verification
- `Tests:` `python3 tickets/scripts/check_ticket_metadata.py`; targeted `rg`
  checks for `Execution steps`, correction-recovery wording, and skill
  `todos.md` loading
- `Manual checks:` read the changed prompt/template surfaces and confirm the
  new behavior is explicit instead of implied
- `Evidence required:` updated instruction and planning surfaces plus passing
  ticket metadata validation
- `Artifacts path:` `tickets/TASK-0089/artifacts/`

## Evidence
- `Artifacts:` `tickets/archive/TASK-0089/artifacts/review-2026-04-25-0135+0100.json`; `tickets/archive/TASK-0089/artifacts/review-2026-04-25-0137+0100.json`; `tickets/archive/TASK-0089/artifacts/review-2026-04-25-0140+0100.json`; `tickets/archive/TASK-0089/artifacts/review-2026-04-25-0142+0100.json`
- `Commands:` `python3 tickets/scripts/check_ticket_metadata.py`; `python3 bin/check_doc_parity.py`; `python3 bin/check_harness_invariants.py`; `git diff --check -- AGENTS.md templates/global/AGENTS.md docs/HISTORY.md docs/MEMORY.md docs/TROUBLES.md docs/specs/harness-techniques.md skills/repent/SKILL.md skills/impl-plan/AGENTS.md skills/impl-plan/README.md skills/impl-plan/SKILL.md skills/impl-plan/todos.md skills/impl-plan/prompts/plan.md skills/impl-plan/references/template.md skills/impl-plan/references/examples.md skills/impl-plan/references/review.md skills/impl/SKILL.md skills/impl/README.md skills/impl/todos.md skills/review/SKILL.md skills/review/references/review-rubric-index.md skills/review/references/implementation-plan.md skills/review/references/spec-contract.md tickets/templates/ticket.md tickets/archive/TASK-0089/ticket.md`
- `Result summary:` Final review verdict `pass` at 4.5 overall across the full contract slice, confirmed again for the archived closeout state by `review-2026-04-25-0142+0100.json`. The routing doctrine, complaint-recovery default, skill todo loading, whole-ticket planning ambition, `Execution steps`, and review visibility all align across the global contract, `impl-plan`, `impl`, `review`, the techniques inventory, durable docs, and the canonical ticket template. Ticket is archived in this closeout commit; push not requested.
- `Ready:` yes

## Blockers
- none
