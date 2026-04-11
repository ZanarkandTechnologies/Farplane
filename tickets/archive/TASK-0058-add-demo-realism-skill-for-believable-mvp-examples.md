---
ticket_id: TASK-0058
title: add demo-realism skill for believable mvp examples
phase: complete
status: done
owner: codex
claimed_by:
priority: high
depends_on: []
blocked_by: []
ready: false
approval_required: false
created_at: 2026-04-11T02:18:55+0100
updated_at: 2026-04-11T02:27:00+0100
next_action: none; archive the finished demo-realism skill ticket after the docs-only proof surface is recorded
last_verification: `python3 tickets/scripts/check_ticket_metadata.py`; `git diff --check`; `python3 -m py_compile tickets/scripts/check_ticket_metadata.py`; fallback standard-library contract validation for `skills/demo-realism`; manual read-through of the skill output contract and rubric
linked_docs:
  - skills/demo-realism/SKILL.md
  - skills/demo-realism/README.md
  - skills/demo-realism/AGENTS.md
  - skills/demo-realism/references/architecture.md
  - skills/demo-realism/references/workflows.md
  - skills/demo-realism/references/gotchas.md
  - skills/demo-realism/references/rubric.md
  - docs/HISTORY.md
---

# TASK-0058: add demo-realism skill for believable mvp examples

## Summary
Create a new `demo-realism` skill that helps agents infer believable operating context, define a pitch-worthy MVP slice, derive realistic workflows/screens/demo data, and score the result with a presentation-worthiness rubric before design or implementation begins.

## Scope
- In:
  - one new skill focused on believable client-demo examples and realistic demo data
  - a realism-first workflow from app slice -> workflow -> screen/state -> data pack
  - a rubric for operational plausibility and presentation-worthiness
  - local skill docs and references that keep the contract easy to trigger and follow
- Out:
  - final UI/design execution
  - factual client research guarantees
  - automatic workflow engines or persisted todo state
  - seeded database scripts in the first pass

## User Story
- `Actor:` Codexter operator shaping an MVP or prototype for a client-facing demo
- `Need:` the system to make the demo feel believable instead of generic by inferring realistic workflows and demo data from how the client plausibly operates
- `Outcome:` the resulting product brief and example data feel good enough to present, even if they are future-state approximations rather than exact client truth

## User Pain / JTBD
- `Current pain:` agents can produce screens, flows, and mock data that technically work but still feel fake because the workflow and operational context were never made believable
- `Why now:` a deep-interview pass clarified that the missing layer is a realism-first composite skill, not just better UI planning or generic mock-data generation

## Non-Goals
- `Do not solve:` exact client-truth reconstruction, final visual design, persisted workflow orchestration, or a research-only verification pass that blocks useful demo synthesis

## High-Fidelity Example
- `Example flow/artifact:` for a warehouse ops demo, the skill infers a plausible day-to-day operating model, chooses a pitch-worthy MVP slice such as “regional inbound exception triage,” breaks that into workflows and screens, derives realistic shipment/exception/user records, and returns a rubric that can score whether the resulting demo would actually feel believable to a warehouse director

## What Good Looks Like
- `Quality bar:` a user can invoke the skill and receive a believable operating hypothesis, a realistic app/workflow decomposition, a concrete demo-data pack shape, and a rubric that explains whether the result feels presentable rather than fake

## Proof Target
- `Reviewer-visible proof:` the new skill can be read and followed directly, clearly states its aggressive-inference boundary, hands off before final design/build, and includes realism/rubric guidance strong enough to shape real MVP demos

## Plan

### Pitch
- `Req:` add the missing realism layer between vague app idea and polished client-facing MVP
- `Bet:` a composite skill that infers believable operating reality and derives a realism pack is more valuable than a narrower “mock data generator”
- `Win:` agents stop building fake-feeling MVPs and instead shape examples that feel like plausible operational software

### Recommendation
- `Best:` create a new `demo-realism` skill that owns realism synthesis and hands off to `functional-ui`, `frontend-design`, `impl-plan`, or `impl`
- `Why:` this fills a gap that existing skills do not cover cleanly, while still reusing those skills for downstream workflow, design, and build work
- `Tradeoff accepted:` the skill will infer aggressively and therefore optimize for pitch potential over exact operational truth

### B -> A
- `Before:` product and UI skills can shape workflows, but no skill explicitly owns believable operational context, realistic states, and pitch-worthy demo data
- `After:` the repo has one realism-first skill that turns a client/demo ask into a usable realism brief, decomposition ladder, data pack, and rubric
- `Outcome:` MVP examples become easier to present and harder to dismiss as obviously fake

### Delta
- `Touch:` a new skill folder plus ticket/docs writeback
- `Keep:` existing workflow, review, and design skills as downstream consumers
- `Change:` add a realism-first planning surface before final UI/design/build execution
- `Delete/Avoid:` no database seeding scripts, no hidden engine, no research-only gating in the first pass

### Core Flow
```pseudo
capture the client or industry context
infer a believable operating model
choose the pitch-worthy MVP slice
decompose app -> workflow -> screen/state
derive realistic entities, records, timelines, and edge cases
score the result with the realism rubric
hand off to the next skill for design or implementation
```

### Proof
- `P1:` the skill contract clearly explains when to use `demo-realism` instead of `functional-ui` or `review`
- `P2:` the skill outputs a believable realism brief plus a concrete data/rubric package
- `Risk:` the skill drifts into generic product ideation or fake-precision client research
- `Rollback:` keep the first slice narrow to realism synthesis and hand off before final design/build

### Plan Review
- `Refs:` deep-interview transcript in chat, `skills/functional-ui/SKILL.md`, `skills/review/SKILL.md`, `skills/skill-creator/*`
- `Scope:` one new skill with local references and docs only
- `Proof:` skill validation plus manual read-through against the clarified user ask
- `Guardrails:` no final design ownership, no exact-client-truth claims, no hidden state engine
- `Fixes:` separate realism synthesis from both UI planning and review so the missing layer is explicit

### Options Appendix
- `Option 1:` extend `functional-ui`
- `Pros:` fewer skills
- `Cons:` buries the realism/data/rubric layer inside a workflow skill that already owns user stories and comparable apps
- `Why not chosen:` too indirect
- `Option 2:` create `demo-realism` as a composite skill
- `Pros:` clear trigger, explicit realism boundary, reusable across MVPs and client demos
- `Cons:` adds one more skill surface to maintain
- `Why not chosen:` chosen option
- `Option 3:` extend `review`
- `Pros:` would reuse the rubric surface
- `Cons:` review happens too late; this problem starts before implementation and design
- `Why not chosen:` wrong phase

### Delegation
- `Need:` Not needed
- `Why:` the skill content and docs are small enough for one direct implementation pass
- `Artifact:` n/a

### Ask
- `Ready: yes`
- `Next:` already implemented in the first skill slice

### Ticket Move
- `Now:` `status: done`, `phase: complete`, ready for `tickets/archive/`
- `On approval:` approval captured from the user’s direct `$impl` request
- `Follow-ups:` seed-data generators or stricter realism validation only if this first skill proves useful
- `Blocked in building?:` no

## Acceptance Criteria
- [x] AC-1: Codexter has a new `demo-realism` skill with a clear trigger description and first-load workflow
- [x] AC-2: the skill defines a realism-first decomposition from app slice -> workflow -> screen/state -> demo data
- [x] AC-3: the skill includes a realism/presentation-worthiness rubric that can judge whether an MVP example feels believable
- [x] AC-4: the skill explicitly hands off before final UI/design/build and states that pitch potential matters more than exact client-truth reconstruction in the first pass

## Working Notes
- Deep-interview outcome: the user wants believable future-state demos, not exact carbon copies of the client’s operation.
- Aggressive inference is allowed if it produces a stronger pitch-worthy MVP.
- The skill should still distinguish itself from `functional-ui`: realism and demo-data ownership are the key missing pieces.

## Inspiration
- Source: direct user deep-interview on 2026-04-11 about creating a skill for high-fidelity MVP examples, believable operating assumptions, realistic demo data, and a presentation-worthiness rubric.

## Implementation Notes
- Touched areas:
  - `skills/demo-realism/*`
  - `docs/HISTORY.md`
- Reused patterns:
  - local skill module docs (`AGENTS.md`, `README.md`)
  - reference-backed skill structure
  - explicit handoff to downstream skills instead of owning the whole delivery stack
- Guardrails:
  - no hidden state
  - no final UI/design ownership
  - no factual-truth guarantee language

## Evidence
- [x] Tests
- [ ] Typecheck
- [ ] Lint
- [x] QA / manual verification

- `python3 tickets/scripts/check_ticket_metadata.py`
- `git diff --check`
- `python3 -m py_compile tickets/scripts/check_ticket_metadata.py`
- `python3 -c 'from pathlib import Path; import re, sys; root=Path("skills/demo-realism"); skill=(root/"SKILL.md").read_text(); required=[root/"AGENTS.md", root/"README.md", root/"references/architecture.md", root/"references/workflows.md", root/"references/gotchas.md", root/"references/rubric.md"]; missing=[str(p) for p in required if not p.is_file()]; checks=[skill.startswith("---\\n"), bool(re.search(r"^name:\\s*demo-realism$", skill, re.M)), bool(re.search(r"^description:\\s*.+$", skill, re.M)), "## First-Load Checklist" in skill, "## Workflow" in skill, "## Output Contract" in skill, "presentation-worthiness" in skill]; ok=not missing and all(checks); print("demo-realism skill contract OK" if ok else f"FAILED missing={missing} checks={checks}"); sys.exit(0 if ok else 1)'`
- `rg -n "demo-realism|presentation-worthiness|operating hypothesis|workflow ladder|screen/state ladder|demo-data pack" skills/demo-realism tickets/TASK-0057-add-demo-realism-skill-for-believable-mvp-examples.md`
- Manual verification: confirmed the skill clearly owns realism synthesis, stops before final design/build, includes a hierarchical decomposition ladder, and carries a believable-demo rubric rather than generic mock-data advice
- `Typecheck:` not run; this slice is docs/markdown-only plus an existing Python validator already checked via `py_compile`
- `Lint:` not run; no dedicated lint target exists for this docs-only skill slice
- `Note:` `python3 skills/skill-creator/scripts/quick_validate.py skills/demo-realism` was attempted but the local environment lacks `PyYAML` (`ModuleNotFoundError: No module named 'yaml'`), so validation used the standard-library fallback contract check above

## Review Packet
- Scores use the anchored `1.0`-to-`5.0` rubric scale.
- `work_type:` `["skill-definition","docs-contract"]`
- `search_scope:` `{changed_files: ["skills/demo-realism/SKILL.md", "skills/demo-realism/AGENTS.md", "skills/demo-realism/README.md", "skills/demo-realism/references/architecture.md", "skills/demo-realism/references/workflows.md", "skills/demo-realism/references/gotchas.md", "skills/demo-realism/references/rubric.md"], related_files: ["skills/functional-ui/SKILL.md", "skills/review/SKILL.md", "skills/skill-creator/SKILL.md", "tickets/templates/ticket.md"], invariants_checked: ["skill hands off before final design/build", "aggressive inference is allowed but not framed as client truth", "output contract stays hierarchical"], docs_checked: ["docs/HISTORY.md", "skills/demo-realism/README.md"]}`
- `reviewed_at:` `2026-04-11 02:27 +0100`
- `rubrics_used:` `["spec-contract","implementation-plan","debloatability"]`
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
- `next_action:` `archive the completed ticket`

## Blockers
- none

## Handoff
- Current state: the first `demo-realism` skill slice is complete. The repo now has a realism-first skill for believable MVP examples and demo data, plus a dedicated realism rubric and downstream handoff rules.
- Resume from: no resume required unless a follow-up ticket adds seeded generators, example prompts, or stricter validation for realism packs.

## Writeback
- Update this ticket as work progresses.
- If the ticket changes queue state, update `status` and `phase` in frontmatter. Do not move the file.
- When implementation and verification pass, move `phase` to `documenting`, write durable docs, then move the ticket into `tickets/archive/` or set `status: done` briefly if you intentionally keep a short-lived visible completion state first.
