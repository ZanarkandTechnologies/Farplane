# Implementation Handoff

Use this at the end of `functional-ui`.

## Handoff Fields

- `Recommended model:` chosen interaction model.
- `Why it wins:` one concrete reason tied to the user story.
- `Steve Jobs Focus & Simplicity Pass:` customer benefit, core action, what is
  removed or deferred, and deliberate `no`.
- `Screens/components:` what needs to exist.
- `States:` default, loading, empty, error, success, disabled, edge cases.
- `Controls:` buttons, inputs, tabs, filters, menus, keyboard/touch needs.
- `Data/content ranges:` min, typical, max.
- `Copy needs:` labels, helper text, error text, empty-state text.
- `Implementation notes:` reusable components, local state, server/client boundaries if known.
- `Low-fi wireflow:` include only when flow or hierarchy needs an ASCII map.
- `Visual gap:` name unresolved visual context rather than choosing taste here.

## Handoff Rule

Do not hand off vague advice like "make it cleaner." Convert the UX decision
into specific behavior and state requirements that `impl-plan` can incorporate
into one Change Plan.
