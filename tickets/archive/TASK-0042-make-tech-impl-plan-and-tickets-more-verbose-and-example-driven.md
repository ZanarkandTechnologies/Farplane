---
ticket_id: TASK-0042
title: make tech impl plan and tickets more verbose and example driven
phase: complete
status: done
owner: codex
priority: high
depends_on: []
blocked_by: []
ready: false
approval_required: false
created_at: 2026-04-08T19:29:01Z
updated_at: 2026-04-09T03:25:19Z
next_action: none; superseded by TASK-0043 and archived after the shared planning-artifact work landed in impl-plan
last_verification: TASK-0043 implemented the merged impl-plan contract, richer ticket template sections, and the related docs/runtime cutover
linked_docs:
  - skills/impl-plan/SKILL.md
  - tickets/templates/ticket.md
  - docs/specs/harness-techniques.md
  - docs/specs/ralph-v2-direction.md
---

# TASK-0042: make tech impl plan and tickets more verbose and example driven

## Summary
Rewrite the planning surface so a human and an agent can quickly understand what a ticket is trying to achieve, why it matters to the user, and what a good implementation looks like from a high-fidelity example.

## Scope
- In: `tech-impl-plan`, the ticket template, and related planning docs that currently optimize too hard for compression
- Out: executing the planned features themselves

## Plan

### RALPLAN-DR Summary
- `Principles:`
  - preserve a concise approval surface near the top
  - add detail only where it helps implementation fidelity
  - keep one primary planning artifact instead of splitting approval and execution briefs
  - improve legibility now without pretending planner-surface overlap is solved
- `Decision Drivers:`
  - the user explicitly said current impl plans are too hard to understand
  - both humans and agents need clearer user-story and behavior grounding
  - the slice must help immediately without expanding into planner-surface consolidation
- `Viable Options:`
  - compact-only tweak with a few new labels
  - separate long-form implementation brief plus short approval plan
  - one richer primary planning artifact with concise top section and structured detail below
- `Chosen:` one richer primary planning artifact with explicit applicability rules and reviewable example depth

### Pitch
- `Req:` make planning artifacts much easier to read by adding richer user-story framing, clearer intent, and concrete examples of the desired implementation quality
- `Bet:` increase detail in the planning surface instead of keeping it aggressively compact
- `Win:` the agent will implement better work because the ticket explains the product story, expected behavior, and proof target with less guesswork

### Recommendation
- `Best:` keep `ralplan` as the current consensus-planning entrypoint, keep `tech-impl-plan` as the separate approval-first planning surface for now, and rewrite `tech-impl-plan` plus the ticket template to use a richer two-layer planning contract
- `Why:` the immediate problem is legibility, not routing. This fixes what the planner outputs now without smuggling planner consolidation into the same ticket
- `Tradeoff accepted:` plans will take longer to read and write, but that is preferable if it materially improves implementation quality

### B -> A
- `Before:` `ralplan` and `tech-impl-plan` both still exist, while `tech-impl-plan` and the ticket template optimize hard for compactness and leave too much implementation intent implicit
- `After:` the current planner surfaces remain separate, but the approval-first artifacts become easier to understand because they add explicit user story, non-goals, realistic examples, and proof targets beneath a concise top section
- `Outcome:` both humans and agents can infer less and execute with higher fidelity

### Delta
- `Touch:` `skills/impl-plan/SKILL.md`, `skills/impl-plan/references/template.md`, `skills/impl-plan/references/examples.md`, `skills/impl-plan/references/review.md`, and `tickets/templates/ticket.md`
- `Keep:` explicit recommendation, proof, and guardrail sections
- `Change:` move from compact pitch-first planning to a two-layer planning artifact with a concise approval surface at the top and richer implementation guidance below
- `Delete/Avoid:` vague shorthand that only makes sense if the planner already remembers the whole context

### Applicability Rule
- `Required when:` the ticket covers material feature work, workflow/tooling changes, ambiguous implementation work, or any change where the implementer would otherwise need to infer desired behavior
- `Can be short or omitted when:` the change is a trivial, single-bug, or narrowly localized fix where the file, symbol, or error already anchors the work concretely

### Section Roles
- `Summary:` smallest executable slice
- `Scope:` explicit in/out boundaries
- `User Story:` who needs what and why now
- `User Pain / JTBD:` what friction or job creates urgency for the change
- `High-Fidelity Example:` one realistic walkthrough of the expected artifact or behavior
- `What Good Looks Like:` concise description of the target quality bar
- `Proof Target:` what evidence would convince a reviewer the ticket is implemented correctly
- `Plan:` how the implementation achieves the result

### Core Flow
```pseudo
read the ticket and current planning skill
keep the top approval surface concise
add explicit user story, JTBD, non-goals, example, and proof-target sections when the work needs them
show how those sections differ from summary/scope/plan
update examples and review guidance so weak narrative sections fail review
verify the sample output is still fast to skim at the top
```

### Proof
- `P1:` a revised ticket template makes it obvious what the user is trying to accomplish without opening multiple extra files
- `P2:` a revised `tech-impl-plan` example demonstrates the target depth on a realistic ticket, not a toy case
- `Risk:` plans become bloated and hide the actual next step in too much prose
- `Rollback:` keep a concise top summary, but allow detailed user-story and example sections below it

### Plan Review
- `Refs:` `skills/impl-plan/SKILL.md`, `skills/impl-plan/references/template.md`, `skills/impl-plan/references/examples.md`, `skills/impl-plan/references/review.md`, `tickets/templates/ticket.md`, `docs/specs/harness-techniques.md`, `docs/specs/ralph-v2-direction.md`, `docs/TROUBLES.md`, `docs/MEMORY.md`
- `Scope:` planning surfaces only
- `Proof:` before/after comparison on one realistic sample ticket or plan
- `Guardrails:` more detailed must not mean less structured; keep clear headings, explicit applicability rules, and a concise top approval surface
- `Fixes:` made planner-surface boundary explicit, added applicability rules, added section-role distinctions, added realistic-example requirement, and added review failure rules for decorative content

### Options Appendix
- `Option 1:` keep the compact structure and only add a few labels
- `Pros:` minimal churn; preserves fast approval flow
- `Cons:` too weak for the current complaint; likely leaves implementation intent implicit
- `Why not chosen:` it preserves the core failure mode
- `Option 2:` create a short approval plan plus a separate long-form implementation brief
- `Pros:` preserves a very skim-friendly top artifact while allowing depth elsewhere
- `Cons:` creates artifact drift risk and makes the planner surface even more fragmented
- `Why not chosen:` the repo already has overlapping planner surfaces; adding another artifact makes that worse
- `Option 3:` keep one primary planning artifact with a concise top section and structured detail below
- `Pros:` addresses legibility immediately without adding a second brief; keeps approval and implementation guidance in one place
- `Cons:` more writing overhead and a risk of policy bloat if examples are not kept tight
- `Why not chosen:` recommended

### Delegation
- `Need:` Not needed
- `Why:` this is a planning-only docs rewrite; the ralplan consensus loop itself already supplied Architect and Critic review
- `Artifact:` n/a

### Ask
- `Ready: yes`
- `Next:` approve the rewrite, then update the planning contract set in scope and keep planner-surface simplification as a separate follow-up

### Ticket Move
- `Now:` `status: review`, `phase: planning`
- `On approval:` set `status: building` and rewrite the planning artifacts
- `Follow-ups:` planner-surface simplification between `ralplan` and `tech-impl-plan` remains a separate follow-up after this ticket
- `Blocked in building?:` no

## Acceptance Criteria
- [ ] AC-1: `tech-impl-plan` explicitly supports a two-layer planning artifact: concise top approval surface plus richer lower implementation-guidance sections
- [ ] AC-2: the template and skill encode an applicability rule that makes `User Story`, `User Pain / JTBD`, `Non-Goals`, `High-Fidelity Example`, `What Good Looks Like`, and `Proof Target` required for material or ambiguous work and optional for trivial localized fixes
- [ ] AC-3: the template distinguishes `Summary`, `Scope`, `User Story`, `High-Fidelity Example`, and `Plan` clearly enough that a reviewer can tell whether each section is doing a distinct job
- [ ] AC-4: the examples include at least one realistic before/after planning artifact at the target depth
- [ ] AC-5: the review guidance explicitly fails generic, duplicated, placeholder-only, or decorative narrative sections
- [ ] AC-6: a human can read one revised planning artifact and understand what the ticket is doing without heavy inference while still being able to skim the top section quickly

## Working Notes
- Direct user complaint: “the impl plan is too hard to understand now i cant get what a ticket is doing.”
- Detail request is explicit: be more verbose, especially around user story and high-fidelity examples.
- Current planner-surface answer: both still exist today. `ralplan` is the current consensus-planning entrypoint, while `tech-impl-plan` remains a separate approval-first planning surface.
- Existing harness-techniques doc already notes that `tech-impl-plan` and `ralplan` overlap conceptually; this ticket improves legibility now but does not resolve that overlap.
- Architect review approved the slice if it stays bounded to planning artifacts and examples.
- Critic approved the revised plan after applicability rules, measurable section distinctions, and concrete verification were added.
- TASK-0043 now absorbs this work while also collapsing the planner surfaces into `impl-plan`.

## Implementation Notes
- Touched areas: planning skill, ticket template, plan examples, maybe review expectations for plan quality
- Reused patterns: recommendation + proof + guardrails
- Guardrails: do not preserve compactness as the top priority when it hurts clarity

## Evidence
- [ ] Tests
- [ ] Typecheck
- [ ] Lint
- [x] QA / manual verification

- `sed -n '1,260p' tickets/TASK-0042-make-tech-impl-plan-and-tickets-more-verbose-and-example-driven.md`
- `sed -n '1,260p' skills/impl-plan/SKILL.md`
- `sed -n '1,260p' tickets/templates/ticket.md`
- `sed -n '1,340p' docs/specs/ralph-v2-direction.md`
- `sed -n '1,240p' docs/TROUBLES.md`
- `sed -n '1,240p' docs/MEMORY.md`
- `sed -n '1,240p' skills/impl-plan/references/template.md`
- `sed -n '1,260p' skills/impl-plan/references/examples.md`
- `sed -n '1,220p' skills/impl-plan/references/review.md`
- `sed -n '1,260p' skills/impl-plan/SKILL.md`
- Architect review run via subagent
- Critic review run via subagent, one iterate cycle, then APPROVE

## Review Packet
- `reviewed_at:` 2026-04-08 21:40 +0100
- `rubrics_used:` implementation-plan,spec-contract
- `overall_score:` 4.8
- `overall_threshold:` 4.0
- `overall_verdict:` pass
- `rerun_required:` false
- `evidence_quality:` pass
- `integration_readiness:` pass
- `traceability:` pass
- `freshness:` pass
- `hard_gate_failures:` []
- `blocking_findings:` []
- `next_action:` hold in review until the rewrite is approved for building

## Blockers
- none

## Handoff
- Current state: superseded by TASK-0043 and archived.
- Resume from: no resume required

## Writeback
- Update this ticket as work progresses.
- If the ticket changes queue state, update `status` and `phase` in frontmatter. Do not move the file.
- When implementation and verification pass, move `phase` to `documenting`, write durable docs, then move the ticket into `tickets/archive/` or set `status: done` briefly if you intentionally keep a short-lived visible completion state first.
