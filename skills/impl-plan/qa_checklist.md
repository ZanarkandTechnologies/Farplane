---
title: Impl Plan QA Checklist
owner: impl-plan
status: active
kind: qa-checklist
created_at: 2026-06-22
updated_at: 2026-08-04
applies_to: [implementation-plans, coding-tickets]
---

# Impl Plan QA Checklist

Apply this after material planning and after changes to `impl-plan`. The
canonical body schema is `tickets/templates/ticket.md`; this checklist judges
decision and execution quality without restating that template.

```text
impl_plan_qa(ticket, inspected_context, proof_weight)
  -> pass | revise | block + exact_fix
```

## Checks

1. `ticket-first`
   - Material planning is durable in one selected ticket, not chat or a child
     implementation plan. When no ticket is supplied, the planner creates or
     requests the canonical ticket before returning a substantive plan.

2. `canonical-template-owner`
   - The ticket follows `tickets/templates/ticket.md`; no skill-local active
     schema, decorative duplicate section, or parallel contract exists.
   - Summary, Scope, Delta, Change Plan, Done, QA Strategy, and State carry the
     executable contract. Every additional section names the decision,
     evidence, or resume need that would be lost if it were removed.
   - The required Contract Diagram is type-appropriate, simulatable, consistent
     with Scope/Delta, and referenced by Change Plan assertions and proof.

3. `objective-and-scope`
   - Summary, in/out boundaries, constraints, Before/After/Example, and the
     smallest faithful slice are decisive. Real forks have one recommendation
     and accepted tradeoff.

4. `lean-receipt`
   - After inspecting nearby code, tests, docs, helpers, components, assets,
     and accepted planning artifacts, the planner calls `lean-check` once.
     The receipt names the first sufficient rung, evidence, and smallest action
     or an honest blocker.

5. `context-resolution`
   - Required facets resolve as `reuse | targeted_refresh | create | block |
     not_applicable`. Only decisions affecting scope, implementation, proof, or
     blockers are recorded; advisor-owned gaps are not self-authored.
   - For UI work, only unresolved interaction, visual, media, or landing
     facets call their bounded owner. The resulting decisions are merged into
     the ticket design baseline; a frontend router or child plan is a failure.
   - For material UI work, the accepted **Steve Jobs Focus & Simplicity Pass**
     conclusion—core action, subtraction, and deliberate `no`—is preserved in
     that existing baseline; `impl-plan` does not recreate the judgment or add
     a second ticket section.
  - Every UI-bearing ticket has ticket-local `design.md` with copy-complete
    ASCII screens/states before approval: literal visible copy, reader question,
    proof, intended takeaway, action, and observable assertion. Its QA Strategy
    compares observed captures and behavior against that baseline.

6. `architecture-and-locality`
   - Material ownership, public contracts, and typed movement are visible when
     needed. Each change unit names real files, operation, local contract
     impact, proof, and failure/rollback boundary without repeating the global
     Delta, QA, Docs, or route policy.

7. `least-control-surface`
   - New helpers, functions, files, parameters, flags, schemas, services, and
     config exist only when the lean receipt reaches `minimum_new_code`; the
     plan follows the receipt's smallest action and extends existing owners when
     they fit.

8. `done-and-proof`
   - Done states observable outcomes. QA Strategy names ordered checks,
     delegated capture/judgment lanes, evidence, final checkpoint, and residual
     risk. UI claims require runtime and visual evidence; material claims do
     not self-approve.

9. `docs-and-grounding`
   - Docs ownership and validation are explicit only when non-obvious or
     changed. Implementation-critical external APIs use current official or
     maintained evidence; local-only work says why.

10. `goal-handoff`
    - The approved ticket contains enough task, files, proof, and state for
      `goal-advisor` without transcript memory or duplicated Goal sidecars.

11. `presentation-fit`
    - The Contract Diagram stays compact. A linked `diagrams.md` is required
      only when multiple detailed architecture views or independent diagram
      review materially help, and it validates when present.
    - Empty headings, placeholder `none` rows, and template instructions are
      absent from live tickets.

12. `context-budget`
    - `farplane validate ticket ... --phase planning` passes. Raw context and
      Markdown category counts are inspected; consolidation moves bulky proof
      or execution history without deleting required safety or evidence.

13. `independent-review`
    - A material plan has a reconciled reviewer receipt against
      implementation-plan, architecture when relevant, and evidence-quality.

14. `readiness-consistency`
    - `approval_ready` appears only when context, architecture, proof, budget,
      and review gates pass; otherwise the exact blocker and owner are named.

## Failure Rules

- `revise`: duplicated policy, avoidable ceremony, missing local detail, weak
  proof, or a smaller faithful plan can be repaired during planning.
- `block`: objective, ownership, authority, external fact, architecture, or
  proof route cannot be resolved safely.
- Line count alone never authorizes deleting required proof or hiding prose in
  Mermaid, sidecars, or links.

## Finish Gate

```text
plan_qa:
  canonical_template_owner: pass | revise | block
  lean_receipt_and_context_resolution: pass | revise | block
  executable_change_plan: pass | revise | block
  least_control_surface: pass | revise | block
  done_and_proof: pass | revise | block
  presentation_fit: pass | revise | block
  context_budget: pass | revise | block
  independent_review: pass | revise | block
  readiness: approval_ready | revise | block
  highest_risk:
  exact_fix_or_deferral:
```

For changes to this skill, also apply `docs/review/rubrics/skill-contract.md`, run
the canonical eval rows, record before/after line counts, and require an
independent reviewer before claiming readiness.
