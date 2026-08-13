---
title: Steve Jobs Focus & Simplicity Pass proof
ticket: TASK-0435
status: reviewed
created_at: 2026-08-14T01:42:00+08:00
owners:
  - skills/functional-ui
  - skills/visual-design
  - skills/impl-plan
---

# Steve Jobs Focus & Simplicity Pass proof

> **Before:** UI planning could meet workflow and visual requirements without
> explicitly protecting one user action by naming the complexity to remove,
> defer, or reject.
>
> **After:** `functional-ui` and `visual-design` now run a named Steve Jobs
> Focus & Simplicity Pass; `impl-plan` carries its accepted result into the
> existing ticket design baseline.
>
> **Example:** Incident triage keeps **Assign owner** primary while deferring a
> permanent activity column and rejecting decorative metric cards, nested
> panels, and an animated background.

## Owner-local behavior

- `functional-ui` records user benefit, core action, subtraction/deferment,
  and a deliberate no; its guardrail preserves required states, accessibility,
  safety, evidence, and recovery.
- `visual-design` records the same decision at the visual level: one focal
  action, layers removed or deferred, and a deliberate no. Its brief and
  critique references make the conclusion implementable.
- `impl-plan` preserves an accepted material UI conclusion in the ticket's
  existing design baseline. It must not re-author design, invent a second
  ticket section, or return a substantive chat-only plan when no ticket exists.
- `lean-check` is unchanged: it still owns implementation minimality, not
  customer-action or visual-focus judgment.

## Verification

| Check | Result |
| --- | --- |
| Eval JSON parse and eval-query spoiler lint | pass |
| Package validation: `functional-ui`, `visual-design`, `impl-plan` | pass |
| Skill metadata, registry, and link validation | pass; registry regenerated |
| `git diff --check` | pass |
| Ticket planning validation | pass |
| Functional focus eval | A / 1.0 — `20260813-171429-task-0435-functional-ui-focus-judged-rerun` |
| Visual focus eval | A / 1.0 — `20260813-171529-task-0435-visual-design-focus-judged` |
| Plan preservation eval | A / 1.0 — `20260813-171948-task-0435-impl-plan-focus-repair-3` |

The configured runner exceeded this terminal's single-command time window for
some two-call agent-plus-judge runs. Those were completed as bounded stages:
the recorded agent answer was passed to the configured judge, which produced
the A receipts above. The final planner rerun completed end-to-end.

## Repair retained as evidence

The first planner eval found a real defect: when no ticket was selected it
preserved the subtraction decision only in chat. `impl-plan` and its prompt/QA
now require creating or requesting a canonical ticket before a substantive
plan, then carrying the accepted result in the existing baseline. The revised
natural ticket-drafting scenario passed A.

## Grounding

Placement and behavior were grounded in the local UI skills, the Farplane
harness-placement doctrine, the Steve Jobs Archive, and the 1997 WWDC
transcript. The named pass is a bounded focus-and-subtraction mnemonic, not a
literal persona simulation or a substitute for user evidence.

## Review request

Independent review returned `pass-ready` / `TAS-A`; see
`review/2026-08-14-review.md`.
