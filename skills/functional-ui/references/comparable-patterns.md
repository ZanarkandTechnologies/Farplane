# Comparable Patterns

Use this when grounding a UI recommendation in proven examples.

## What To Inspect

Pick 2-4 examples from:

- Direct competitors or adjacent products.
- OS-native patterns.
- Mature SaaS/app patterns.
- Design-system examples already used by the repo.
- Latest public examples when the user asks for current/SOTA references.

For material, unsettled, current, or SOTA workflows, operate the examples with
[`agent-browser`](../../agent-browser/SKILL.md) instead of relying on memory or
search snippets. Stay within public access or an already-authorized user
session; record login walls and inaccessible states rather than bypassing them.

Executable start:

```bash
agent-browser skills get core
agent-browser open <public-comparable-url>
agent-browser snapshot -i -u
# interact with visible filters, categories, screens, or flow entries
agent-browser snapshot -i -u
agent-browser close
```

Use a named session per source when operating several sites concurrently. Do
not declare browser operation blocked merely because no authenticated session
exists: inspect the public surface first, then record the exact login wall if a
deeper state is unavailable.

## Established Source Roles

Use the smallest useful mix:

- Direct products or competitors: strongest evidence for actual current
  behavior, defaults, copy, state transitions, and recovery.
- Mobbin: screen, UI-element, state, category, and product-flow discovery.
  Public browsing can support reconnaissance; record when deeper inspection
  requires an account.
- Page Flows: recorded end-to-end journeys, annotations, and sequence evidence.
- OS-native and maintained design-system examples: platform conventions and
  accessibility behavior.
- Pinterest, Savee, and aesthetic galleries: visual/taste discovery only. They
  may route to `visual-design` or `ingest-content`, but never satisfy the
  functional comparable requirement by themselves.

Source availability and product behavior can change. Preserve the inspected
URL, date, and access limit in the evidence receipt.

## What To Extract

Compare workflows, not vibes:

- Entry point: how users arrive.
- Primary action: how the key job is presented.
- Defaults: what is preselected or hidden.
- State coverage: empty/loading/error/success/max-content.
- Navigation: tabs, sidebars, command palettes, drill-downs, inline expansion.
- Feedback: toasts, inline status, optimistic updates, undo.
- Density: how much information is visible before scrolling.

## Output Shape

```text
Comparable Evidence Receipt
- Example A: URL + user job/query + observed sequence/states + evidence ref
- Example B: URL + user job/query + observed sequence/states + evidence ref
- Example C: URL + user job/query + observed sequence/states + evidence ref

Access limits
- login wall, unavailable state, or inspection constraint

Borrow
- adopt: pattern to reuse directly
- adapt: pattern to change for local constraints

Avoid
- reject: pattern that does not fit this product and why
```

Do not move to the recommendation until every selected comparable has a receipt
row or an explicit access blocker. For a skipped tiny/settled/pure-visual path,
emit `comparable_research_skipped: <reason>` instead of an empty receipt.
When browser tooling itself is unavailable, emit
`browser_operation: blocked: <exact reason>` and label any docs-only synthesis
`provisional`; documentation is useful grounding but is not an operated flow.
The blocker receipt must name the attempted command/method, exact error or
missing capability, evidence ref, and public URLs attempted. A generic claim
that the fixture lacks a browser is not enough.
