---
name: tech-impl-plan
version: 1.3.0
description: "Approval-first implementation planning skill. Produces a compact pitch with req understanding, before -> after, touched areas, core pseudocode, proof, an automatic plan-quality review, and a clear yes/no handoff."
allowed-tools: Read, Glob, Grep
---

# Tech Impl Plan

Use for implementation planning. Optimize for approval speed. Plan only the next commit.

<!-- MEM-0007 decision: planning output should be approval-first and compact: pitch, before->after, delta, core flow, proof, ask. -->
<!-- MEM-0016 decision: every plan should run a built-in quality pass before handoff so missing references, weak proof, or hidden scope drift are caught before approval. -->
<!-- MEM-0008 decision: root AGENTS should stay repo-only and terse; skill internals belong in skills, not repo contract text. -->

## Core Prompt Wording

0a. Study `@docs/prd.md` for outcomes + constraints.  
0b. Study `@docs/specs/*` for spec truth.  
0c. Study the active ticket in `@tickets/review/*` first; if none exists, inspect `@tickets/todo/*`.  
0d. Study `@docs/MEMORY.md` for durable constraints.  
0e. Study `@docs/TROUBLES.md` for repeated planning/execution misses when present.  
0f. Search the codebase before assuming anything is missing.

## First-Load Contract

### Trigger Conditions

- user asks for a plan, proposal, implementation approach, or approval-ready change summary
- feature/refactor work needs a human yes/no before moving a ticket from `review` to `building`
- request is large enough that `B -> A` and proof should be made explicit

### Workflow (7 Steps)

1. **Scope**: choose the next smallest executable slice.
2. **Split check**: if not one commit, stop and ask to split.
3. **Pitch**: show `Req`, `Bet`, `Win`.
4. **Delta**: show `Before -> After`, touched areas, and keep/change/delete.
5. **Teach**: show core pseudocode; add diagram or appendix only if the path is new or risky.
6. **Review**: run the plan through the quality gate; fix weak spots before handoff.
7. **Proof + ask**: show proof points, plan review result, main risk, delegation note, and `Ready: yes/no`.

### Core Decision Branches

- **Low risk / obvious fit** -> keep plan short; no appendix.
- **High ambiguity / risk** -> keep short top section; push details below fold.
- **Multi-commit work** -> split before planning in detail.
- **Docs-only / rule-text-only** -> no specialized QA delegation.

### Top 3 Gotchas

1. Do not implement; this skill is plan-only.
2. Do not bury `Before -> After` below long explanation.
3. Do not default to diagrams, dry-runs, or deep rationale when pseudocode is enough.

### Outcome Contract

Every plan must include:

1. `Pitch`
   - `Req:` what I think you want
   - `Bet:` better option if any
   - `Win:` why this shape
2. `B -> A`
   - before
   - after
   - user/dev outcome
3. `Delta`
   - touched files/modules
   - keep/change/delete
4. `Core Flow`
   - 6-12 lines of pseudocode
   - optional diagram only for new/risky paths
5. `Proof`
   - 2-4 concrete checks
   - main risk / rollback note
6. `Plan Review`
   - `Refs:` confirm which sources were actually used: PRD/spec/ticket/memory/troubles/code
   - `Checks:` pass/fix for scope, proof, guardrails, and rollback clarity
   - `Fixes:` what was tightened before handoff, or `none`
7. `Ask`
   - `Ready: yes/no`
   - next step after approval
8. `Delegation`
   - skill/subagent only if needed
   - otherwise `Not needed`
9. `Ticket Move`
   - where the ticket should live now
   - any spawned follow-up tickets
   - whether it is blocked in `building/` or returned to `review/`

## Efficiency Rules

- Lead with the approval surface, not the appendix.
- Prefer symbols and compact labels over repeated prose.
- Reuse existing modules; justify every new file or abstraction in one line.
- Keep deeper implementation detail below the top section.
- If the plan cannot be understood from `Pitch + B -> A + Core Flow`, it is not ready.
- If planning reveals overflow scope, split it into new `tickets/todo/` follow-ups instead of stretching one ticket.

## Plan Quality Gate

Before returning the plan, run these checks against the drafted output:

1. **Reference coverage**
   - Did the plan actually use the relevant PRD, spec, ticket, memory, troubles, and local code context?
   - If a source was skipped, is that omission safe and explicit?
2. **Scope discipline**
   - Is this really one commit?
   - If not, stop and split instead of hiding extra scope in prose.
3. **Guardrail fit**
   - Does the plan reuse existing patterns?
   - Does it avoid speculative abstractions, silent migrations, and unnecessary new files?
4. **Proof quality**
   - Are the checks concrete and observable?
   - Would a reviewer know exactly how to tell success from failure?
5. **Risk clarity**
   - Is the main risk named?
   - Is rollback or containment clear enough for the size of the change?

If any check fails, tighten the plan before presenting it. The final output should show the review result, not the draft that failed it.

## References

- [prompts/plan.md](prompts/plan.md)
- [references/template.md](references/template.md)
- [references/examples.md](references/examples.md)
- [references/review.md](references/review.md)

## Final Check

Before handoff, read `references/review.md` and tighten the plan until it passes those checks.
