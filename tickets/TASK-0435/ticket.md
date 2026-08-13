---
template_id: ticket-template
template_version: "0.2.7"
feature_refs:
  - FEAT-0007
  - FEAT-0008
ticket_id: TASK-0435
title: Add a Steve Jobs Focus & Simplicity Pass to UI planning
status: awaiting_review
created_at: 2026-08-14T01:09:29+08:00
updated_at: 2026-08-14T01:48:00+08:00
depends_on: []
---

# TASK-0435: Add a Steve Jobs Focus & Simplicity Pass to UI planning

## Summary

Give Farplane UI planning an explicit, named subtraction lens so agents make
the customer benefit and core action obvious, remove nonessential complexity,
and record the deliberate "no" without adding a global prompt rule or another
skill.

## Scope

- In: `functional-ui`, `visual-design`, and `impl-plan` contracts; focused
  skill-local behavioral evals; a compact audit and independent review.
- Out: a literal persona simulation, `AGENTS.md` or global-template policy,
  a standalone Steve Jobs skill, visual implementation, or changes to
  `lean-check`.
- Constraints: preserve user evidence, accessibility, states, safety, and
  proof; `lean-check` remains the first-sufficient-rung implementation gate.

## Delta

> **Before:** UI planning can satisfy workflow and visual requirements without
> naming what must be removed, deferred, or explicitly rejected to protect the
> primary user action.
>
> **After:** Material UI planning applies the Steve Jobs Focus & Simplicity
> Pass in the existing UX and visual owners; `impl-plan` carries the accepted
> conclusion into the ticket design baseline.
>
> **Example:** An incident triage screen retains the assignment action and
> removes a permanent activity column and decorative metric card that do not
> help an operator assign the incident.

## Change Plan

### Change 1: Add the named UX and visual pass

```yaml
files:
  edit:
    - skills/functional-ui/SKILL.md
    - skills/functional-ui/qa_checklist.md
    - skills/functional-ui/references/implementation-handoff.md
    - skills/visual-design/SKILL.md
    - skills/visual-design/references/design-brief.md
    - skills/visual-design/references/critique-audit.md
operation: Add a compact, owner-specific Steve Jobs Focus & Simplicity Pass
  that states customer benefit, core action or focal hierarchy, subtraction,
  and a deliberate no; retain required accessibility, state, safety, and proof.
proof: Focused skill eval rows and first-load/QA checks show that a material UI
  recommendation preserves the core job while removing nonessential complexity.
failure: A pass that merely imitates Jobs's style, hides required controls, or
  replaces user/comparable evidence is rejected.
```

### Change 2: Preserve the result in implementation planning

```yaml
files:
  edit:
    - skills/impl-plan/SKILL.md
    - skills/impl-plan/prompts/plan.md
    - skills/impl-plan/qa_checklist.md
operation: Require UI planning to merge accepted pass conclusions into the
  ticket design baseline without inventing a parallel ticket section.
proof: A plan eval reuses the owned UI result and retains the chosen core action
  and rejected complexity in one Change Plan.
failure: A planner redoes UI judgment, drops the deliberate no, or adds a
  second schema instead of using the canonical ticket.
```

### Change 3: Add behavioral proof and review

```yaml
files:
  edit:
    - skills/functional-ui/evals/evals.json
    - skills/visual-design/evals/evals.json
    - skills/impl-plan/evals/evals.json
    - skills/visual-design/SKILL.md
    - tickets/TASK-0435/artifacts/review/
operation: Add one natural, owner-local regression case per affected skill,
  register the visual-design suite, run static and focused eval checks, and
  capture independent review.
proof: JSON, query-spoiler, package validation, registry sync, focused eval
  receipts, and independent reviewer verdict pass.
failure: A query leaks the check's expected answer, or a failing run holds the
  ticket for repair rather than being treated as proof.
```

## Done

- [x] Material UX and visual direction names the Steve Jobs Focus & Simplicity
      Pass and returns an actionable conclusion.
- [x] The pass preserves required accessibility, states, safety, and evidence;
      it is not a style imitation or a request to make things merely smaller.
- [x] UI tickets retain the accepted core action and rejected complexity in
      their existing design baseline.
- [x] Focused behavioral evals, package/registry validation, and independent
      review pass.

## QA Strategy

```yaml
proof_weight: hybrid
checks:
  - focused JSON and eval-query spoiler validation
  - quick skill package validation for all three owners
  - skill registry regeneration and link validation
  - focused Codex skill evals where the configured runner is available
  - independent review of cross-skill ownership, eval quality, and proof
delegated_lanes: [reviewer]
evidence_paths:
  - tickets/TASK-0435/artifacts/review/
  - skills/functional-ui/evals/evals.json
  - skills/visual-design/evals/evals.json
  - skills/impl-plan/evals/evals.json
final_checkpoint: reviewer
residual_risk: The named lens may not reduce real rework until it is trialed on
  production UI plans; the first use should verify a concrete subtraction.
```

## State

- Current: implementation, proof, and independent `TAS-A` review complete.
- Next: operator review / normal ticket closeout.
- Blockers: none.

## Links

- `program:` `none`
- `progress:` `none`
- `artifacts:` `tickets/TASK-0435/artifacts/`
- `related:` `skills/functional-ui/SKILL.md`, `skills/visual-design/SKILL.md`,
  `skills/impl-plan/SKILL.md`, `skills/lean-check/SKILL.md`
- `proof:` `tickets/TASK-0435/artifacts/2026-08-14-focus-simplicity-proof.md`
- `review:` `tickets/TASK-0435/artifacts/review/2026-08-14-review.md`

## Notes

- Lean receipt: `reuse_local` — the existing UX, visual, and implementation
  owners already cover the lifecycle; only their shared named subtraction
  decision is absent. A new skill, global rule, hook, or validator would add
  duplicate routing or false determinism.
- Grounding: local UI-skill contracts and Farplane placement doctrine; Steve
  Jobs's focus/customer-benefit framing was checked against the Steve Jobs
  Archive and the 1997 WWDC transcript.
