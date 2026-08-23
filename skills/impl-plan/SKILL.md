---
name: impl-plan
description: "Turn one selected software or product request into a repository-grounded, context-resolved Change Plan, test strategy, and proof contract."
tier: 3
source: local
template_uses:
  skill-template: "0.3.0"
  skill-eval-task: "0.2.0"
group: operations
common_chains:
  after: ["goal-advisor"]
allowed-tools: Read, Glob, Grep
---

# Impl Plan

## Context

`impl-plan` is the ticket-first planning compiler for material software and
product work. It resolves accepted intent and repository context into one
approval-ready `tickets/TASK-XXXX/ticket.md`; it does not implement the change
or create child implementation plans. Tiny reversible fixes may bypass it with
a reason, while vague epics route to discovery or ticketization first.

The canonical ticket body is owned only by
[tickets/templates/ticket.md](../../tickets/templates/ticket.md). This skill
owns how planning decisions are reached, not a second ticket schema. Accepted
UX, landing, copy, visual, asset, research, and technical artifacts are inputs;
advisors fill only bounded missing or stale facets. `goal-advisor` compiles the
approved ticket for execution and does not redo planning.

For UI-bearing work, resolve four independent context facets only when they
are missing or stale: `functional-ui` for interaction evidence and wireflow,
`visual-design` for reference-backed visual direction, `asset-advisor` for
actual media needs, and `landing-page` for a one-page offer/story. This skill
merges accepted results into one ticket and `design.md`; it is not a frontend
router or a second design author. When either UI facet is material, preserve
its accepted **Steve Jobs Focus & Simplicity Pass** conclusion in the ticket's
existing design baseline rather than adding a second ticket section.

## Skill Signature

```text
impl_plan(ticket_or_request, proof_weight?)
  -> canonical_ticket + context_decisions + lean_verdict + reviewer_receipt

state:
  reads(ticket?, accepted artifacts, relevant code/tests/docs, project memory?)
  writes(ticket.md, required UI design.md?, optional diagrams.md, approval handoff)

gates:
  ticket_bound; internal_reuse_inspected; required_context_resolved_or_blocked;
  code_seams_named; change_order_executable; done_and_proof_concrete;
  ui_design_baseline_copy_complete_or_approval_blocked; lean_receipt_passed;
  ticket_context_budget_checked; material_review_reconciled

fails:
  chat_only_material_plan; parallel_ticket_schema; repeated_advisor_work;
  advisor_owned_gap_self_authored; blocked_facet_erases_honest_plan;
  duplicated_global_and_per_change_policy; proof_weakened_for_line_count;
  readiness_with_open_gate; implementation_before_approval
```

A buyer-facing UI handoff is not approval-ready without its ticket-local,
copy-complete `design.md`; if final copy or proof is missing, name that file as
blocked rather than offering a ticket-shaped implementation plan.

## Phase Boundary

Resolve each required planning facet before drafting:

```text
resolve_context(requirement, accepted_artifacts)
  -> reuse | targeted_refresh | create | block | not_applicable
```

- `reuse`: accepted, current, relevant, consistent, and specific enough.
- `targeted_refresh`: preserve settled context and fill one named stale,
  incomplete, or conflicting facet through its owner.
- `create`: produce missing context that can be safely derived through its
  owner.
- `block`: operator authority, external facts, or a material product decision
  are unavailable. Preserve the requested scope and maximal honest plan.
- `not_applicable`: accepted scope explicitly excludes the facet.

Advisors run only for `targeted_refresh` or `create`. They return bounded
inputs; this skill alone merges the Change Plan. A named omission is a gap, not
permission to drop scope. When a resolver cannot run, record `block` rather
than inventing its result.

For a material request with no selected ticket, create or request the canonical
`tickets/TASK-XXXX/ticket.md` before returning a substantive plan. When
accepted UI context includes a **Steve Jobs Focus & Simplicity Pass**, preserve
its core action, subtraction, and deliberate `no` in the ticket's existing
design baseline; never replace it with a chat-only summary or a new schema.

<!-- BEGIN FARPLANE_IMPORTANT_CHECKLIST -->
## Todo List

- [ ] 1. Bind the objective and ticket.
  - [ ] Read or create the selected ticket; resolve only missing inputs that
    materially change scope, architecture, proof, permission, or Goal setup.
  - [ ] Read the first-load Todo List guardrails before material planning.
- [ ] 2. Inspect the minimum repository and accepted context.
  - [ ] Name real code/test/doc seams, typed movement when relevant, existing
    helpers/components/assets, and implementation evidence.
  - [ ] Inventory accepted planning artifacts and capture material chat-only
    decisions durably before treating them as reusable.
- [ ] 3. Resolve only required context facets.
  - [ ] Record the decision, evidence, exact gap, resolver/result when used,
    and how it changes scope, a change unit, or proof. Omit irrelevant ledgers.
  - [ ] Reuse settled UX, landing, copy, visual, asset, architecture, metric,
    documentation, and proof context. Call the narrow owner only for a real
    `targeted_refresh` or `create`; do not self-author its output.
  - [ ] Common owners are [functional-ui](../functional-ui/SKILL.md),
    [landing-page](../landing-page/SKILL.md),
    [copywriting-advisor](../copywriting-advisor/SKILL.md),
    [personalized-offer](../personalized-offer/SKILL.md),
    [visual-design](../visual-design/SKILL.md),
    [asset-advisor](../asset-advisor/SKILL.md),
    [research](../research/SKILL.md), [deep-system-design](../deep-system-design/SKILL.md),
    and the `metric-advisor` skill.
  - [ ] For UI work, reuse or resolve only the relevant facet: interaction
    model/low-fi wireflow (`functional-ui`), visual reference and system
    (`visual-design`), production media (`asset-advisor`), or one-page offer
    and section architecture (`landing-page`). Load
    [UI implementation evidence](references/ui-implementation.md) only after
    those decisions identify a real component, theme, registry, framework, or
    chart requirement.
  - [ ] For material UI work, merge the accepted **Steve Jobs Focus & Simplicity
    Pass** conclusion—core action, subtraction, and deliberate `no`—into the
    existing design baseline; do not recreate UI judgment or add ticket schema.
- [ ] 4. Populate the canonical ticket template.
  - [ ] Load [tickets/templates/ticket.md](../../tickets/templates/ticket.md)
    and keep its required sections and optional-section rules authoritative.
  - [ ] Start from the compact spine. Add an optional section only when its
    admission test passes; delete empty headings and placeholder rows.
  - [ ] Make each Change Plan unit name files, operation, mapped Contract
    Diagram IDs, contract/type impact when material, observable assertions,
    local proof, and a real failure/rollback boundary. Do not
    repeat global Delta, QA, Docs, or route policy in every unit.
  - [ ] Keep architecture signatures compact and only when ownership, public
    contracts, or typed movement would otherwise be ambiguous.
- [ ] 5. Make completion observable.
  - [ ] `Done` states outcomes; `QA Strategy` names ordered checks, delegated
    lanes, evidence, final checkpoint, and residual risk; `Docs Strategy` is
    present only when docs ownership is non-obvious or changes.
  - [ ] Preserve existing proof briefs and use QA, visual QA, agent QA, demo,
    and reviewer lanes when the claim requires independent evidence.
  - [ ] For UI-bearing tickets, set `ui_scope: true` and create or update
    ticket-local `design.md` with copy-complete ASCII screens/states before
    approval. Use the [design baseline template](references/design-template.md):
    literal visible copy, reader question, proof, takeaway, action, and
    assertion. Make QA compare captures and behavior against its IDs and
    assertions; a link alone is not proof.
- [ ] 6. Keep presentation proportional.
  - [ ] Keep the required Contract Diagram compact and type-appropriate. Create
    `diagrams.md` only when multiple detailed architecture views or independent
    diagram review materially help; validate it when linked.
  - [ ] Move execution history and bulky proof to `progress.md` or `artifacts/`.
- [ ] 7. Run minimality and mechanical gates.
  - [ ] Call the Lean Check direct command once after context resolution
    and before finalizing the Change Plan. Preserve its first sufficient rung,
    evidence, and smallest action only where they change scope, a change unit,
    or QA; do not create a parallel ticket schema.
  - [ ] Run `farplane ticket check <ticket> --phase planning`; inspect raw
    first-load and Markdown category counts, then consolidate duplicated policy
    or bulky evidence when pressure is reported.
- [ ] 8. Review and hand off.
  - [ ] Reapply the first-load Todo List guardrails to the completed ticket
    after drafting and after any repair. Resolve every `revise`, stop on
    `block`, and record the finish-gate verdict before reviewer handoff.
  - [ ] Material plans require native reviewer judgment against
    implementation-plan, architecture when relevant, and evidence-quality.
    Reconcile findings before `approval_ready`.
  - [ ] After human approval, hand the same canonical ticket to `goal-advisor`.
<!-- END FARPLANE_IMPORTANT_CHECKLIST -->

## Templates

- Ticket body: [tickets/templates/ticket.md](../../tickets/templates/ticket.md).
- UI baseline: [design baseline template](references/design-template.md).
- Optional detailed visual companion:
  [visual companion template](references/visual-companion-template.md).

## Gotchas

- Do not implement, return a material chat-only plan, or create another
  implementation planner.
- Do not enumerate every irrelevant context facet; record only decisions that
  affect scope, implementation, proof, or blockers.
- Do not repeat ticket-template instructions in this skill, its prompt, or a
  second active reference template.
- Do not treat raw or prose line count as quality. Required safety, ownership,
  reconstruction, and proof survive compaction.
- Do not accept a decorative Contract Diagram or hide prose inside ASCII. It
  must expose the states, boundaries, branches, and proof needed for the ticket.

## Reference Map

- [plan prompt](prompts/plan.md) — compact invocation prompt kept aligned with
  this decision flow.
- [examples](references/examples.md) — load only for output calibration.
- Render necessary compact diagrams inline. The operator may explicitly invoke
  the diagramming shortcut for an optional complex companion.

## Output

- One canonical ticket populated from `tickets/templates/ticket.md`.
- Compact context-resolution and reuse evidence only where it changes the plan.
- Executable Change Plan, concrete Done/QA contract, mechanical budget result,
  reviewer receipt or blocker, and post-approval `goal-advisor` handoff.
- For UI work, name the ticket-local `design.md` and show one representative
  `state -> reader question -> literal copy -> proof/takeaway/action/assertion`
  row in the visible handoff. If any required literal copy or proof is not
  approved, return `approval: blocked` with the missing item; do not turn that
  gap into an implementation decision.
