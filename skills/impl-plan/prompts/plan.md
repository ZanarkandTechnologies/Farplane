# Impl Plan Prompt

Plan only. Turn one selected software or product request into one canonical
`tickets/TASK-XXXX/ticket.md`. Do not implement the change or create a child
implementation plan.

## Grounding

1. Read the selected ticket or create one when material planning has no owner.
2. Read `tickets/templates/ticket.md`; it is the sole ticket-body schema.
3. Inspect the smallest relevant code, tests, docs, project memory, accepted
   briefs, assets, research, and existing implementation patterns.
4. Identify only missing inputs that materially affect scope, architecture,
   proof, permission, or Goal setup. Ask at most three questions only when
   those inputs cannot be safely discovered or inferred.
5. Keep the selected ticket whole unless a real proof, reusable-foundation,
   migration, external-blocker, or runtime/service boundary justifies a split.

## Context Resolution

For each required facet, decide:

```text
resolve_context(requirement, accepted_artifacts)
  -> reuse | targeted_refresh | create | block | not_applicable
```

- `reuse`: cite accepted, current, relevant, sufficiently specific context.
- `targeted_refresh`: preserve settled context and fill one named gap through
  the owning advisor.
- `create`: produce missing context through the owning advisor.
- `block`: preserve the requested scope and maximal honest plan while naming
  unavailable authority, facts, or product decisions.
- `not_applicable`: use only when accepted scope excludes the facet.

Advisors are resolvers for `targeted_refresh` or `create`, not mandatory
ceremony. Reuse existing UX, landing, copy, offer, visual, asset, architecture,
documentation, metric, and proof artifacts when sufficient. Do not self-author
an advisor-owned gap or defer its resolution to implementation.

For UI-bearing work, resolve only the facets that change the ticket: workflow
and low-fi wireflow (`functional-ui`), visual reference/system
(`visual-design`), production media (`asset-advisor`), and one-page offer/story
(`landing-page`). Fold accepted output into `tickets/TASK-XXXX/design.md`; do
not create a frontend planner, router, or parallel design schema.

When material UI work has no selected ticket, create or request its canonical
`tickets/TASK-XXXX/ticket.md` before returning a substantive plan. Preserve any
accepted **Steve Jobs Focus & Simplicity Pass** conclusion—core action,
subtraction, and deliberate `no`—in the existing design baseline, not as a new
ticket section or chat-only summary.

Record a context decision only when it changes scope, a change unit, proof, or
readiness. Include its evidence, exact gap, resolver/result when used, and plan
integration. Do not enumerate irrelevant facets.

After context resolution and before finalizing the Change Plan, call
`lean-check` once. Use its first sufficient rung, evidence, and smallest action
to constrain the plan; include those details only where they change scope, a
change unit, or QA. Do not add a ticket section or restate the ladder.

## Plan Construction

Populate `tickets/templates/ticket.md` directly. Keep that template's required
sections and optional-section rules authoritative.

- Keep `Delta` as a brief, observable feature/behavior preview: what changes
  for the user or system.
- Use one `Change Plan` unit per coherent independently reviewable change.
- Give every change unit a compact owner-level `Implementation Preview` that
  preserves the current seam, shows the planned replacement, and demonstrates
  one expected example. Quote short exact code, prompt, schema, config, or copy
  excerpts when available; otherwise use a clearly labeled signature, state,
  ownership trace, or illustrative pseudocode rather than inventing source.
- Each unit names real files, the concrete operation, material contract/type
  impact, local proof, and a real failure or rollback boundary.
- Do not repeat global Delta, QA, Docs, routing, or policy in every unit.
- Add compact architecture signatures only when ownership, public contracts,
  or typed movement would otherwise be ambiguous.
- Reuse an existing owner before adding a helper, service, file, parameter,
  flag, schema, route, dependency, or configuration surface.
- Add options only for a real material fork and recommend one path decisively.
- Add Docs Strategy, Gap Analysis, Agent Contract, or Run Hints only when the
  branch needs them.

Use an inline text or Mermaid map only when it replaces prose. Create and link
`diagrams.md` only when multiple detailed views or independent visual review
materially improve understanding; validate the companion when present.

## Proof And Handoff

- `Done` states user-visible or system outcomes, not implementation activity.
- `QA Strategy` names ordered checks, proof weight, delegated evidence lanes,
  evidence paths, final checkpoint, and residual risk.
- Preserve an accepted Agent Testability Brief or other proof contract.
- Material plans require independent reviewer judgment against
  implementation-plan, architecture when relevant, and evidence-quality.
- Do not claim `approval_ready` while context, architecture, proof, budget, or
  review gates remain open.
- After human approval, hand the same ticket to `goal-advisor`; it compiles
  execution and does not redo planning.

## Mechanical Gate

Run:

```text
farplane ticket check tickets/TASK-XXXX/ticket.md --phase planning
```

Inspect both raw first-load context and Markdown categories. Consolidate
duplicated policy or bulky evidence into the correct owner, but never remove
required safety, ownership, reconstruction, or proof merely to reduce counts.

Reapply the `skills/impl-plan/SKILL.md` Todo List assertions to the completed ticket after
drafting and after any repair. Resolve `revise`, stop on `block`, record the
finish-gate verdict, and then reconcile the material reviewer receipt before
the readiness call.

## Output

- one canonical ticket populated from `tickets/templates/ticket.md`;
- compact context-resolution evidence only where it changes the plan;
- executable Change Plan and concrete Done/QA contract;
- optional proportional visual companion;
- mechanical validation result and reviewer receipt or exact blocker;
- post-approval `goal-advisor` handoff.
