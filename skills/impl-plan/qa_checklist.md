---
title: Impl Plan QA Checklist
owner: impl-plan
status: active
kind: qa-checklist
created_at: 2026-06-22
updated_at: 2026-06-27
applies_to:
  - implementation-plans
  - coding-tickets
---

# Impl Plan QA Checklist

Use this after material `impl-plan` changes or before accepting a generated
implementation plan. Treat each item as an active violation scan over the
draft plan: name the violation, fix the plan, or explicitly defer it with the
reason and owner.

```text
impl_plan_qa_checklist(ticket_plan, ticket_scope, inspected_code?, proof_weight?)
  -> checklist_verdicts + plan_fixes + defer_or_block_reason
```

## Threshold

```text
accept_plan(plan)
  -> pass when plan_is_minimal_enough
       and reuse_checked
       and proof_route_observable
       and new_surface_justified
  -> revise when a smaller existing seam can satisfy the ticket
  -> block when the objective, architecture boundary, or QA Strategy route is still unknown
```

## Checks

1. `ticket-first`
   - Question: Is the material plan written into or attached to a selected
     `tickets/TASK-XXXX/ticket.md`?
   - Violation: The plan exists only in chat.

2. `minimal-required-version`
   - Question: Is this the smallest implementation that satisfies the ticket's
     objective, first viable slice, proof/falsification, and non-goals?
   - Violation: The plan adds future-proofing, optional UX, broad cleanup,
     extra modes, or nice-to-have behavior that is not required by the ticket.

3. `reuse-before-new-surface`
   - Question: Did the planner inspect existing similar features, nearby
     helpers, conventions, tests, and docs before proposing new files,
     functions, abstractions, or routes?
   - Violation: The plan creates a new surface while an existing seam could be
     extended, parameterized, or reused with less blast radius.

4. `least-parameters`
   - Question: Are new parameters, flags, config keys, schema fields, env vars,
     and prompt variables limited to values the current ticket truly needs?
   - Violation: The plan introduces knobs for hypothetical variants, broad
     configurability, or caller choice without a current caller and proof path.
   - For canonical structured state, name the natural/composite identity and
     separate authored fields from replaceable projection fields. A derivable
     field is a violation unless the plan names its current snapshot-time,
     query/index, or interchange requirement.

5. `function-breakdown-necessary`
   - Question: Does each proposed helper, function, class, component, or module
     remove real complexity, isolate a side effect, match a local pattern, or
     enable focused tests?
   - Violation: The plan decomposes straightforward logic into extra helpers
     mainly for tidiness, naming, or imagined future reuse.

6. `file-surface-necessary`
   - Question: Is each proposed new or touched file justified by ownership,
     existing layout, testability, generated output, or durable artifact needs?
   - Violation: The plan creates sidecars, references, wrappers, scripts, or
     docs when the existing owner file or ticket body can carry the change.

7. `split-boundary-real`
   - Question: If the plan narrows or splits the ticket, is the boundary forced
     by proof, reuse, blocking risk, external dependency, safety, or runtime
     ownership?
   - Violation: The plan splits only because the work feels large, spans
     multiple commits, or a smaller slice feels more comfortable.

8. `goal-advisor-ready`
   - Question: For Goal-backed work, does the approved ticket contain enough
     structure for `goal-advisor(ticket)` to create `program.md`,
     `progress.md`, and the native `/goal` prompt without transcript memory?
   - Violation: The plan requires hidden chat context, unnamed files, unstated
     budget/proof/metric policy, or a post-approval planning decision before
     `goal-advisor` can compile the Goal Packet.

9. `clarifying-questions`
   - Question: Did the planner ask up to 3 blocking clarifying questions when
     objective, acceptance criteria, constraints, target files, proof weight,
     permissions, human gates, or destructive/deploy/spend boundaries were
     missing?
   - Violation: The plan guesses at a materially branching input without
     asking or recording a safe assumption.

10. `change-plan-locality`
   - Question: Does each material `Change Plan` unit carry its own
     before/after, `read`, `write`, `operation`, routes, and QA expectation so the reader
     does not cross-map Delta, Program, and Map?
   - Violation: The plan puts implementation order, touched files, signatures,
     or QA in separate sections that must be manually reconciled.

11. `change-plan-blocks`
   - Question: Is each material change represented as its own heading plus
     fenced block with plain `fixes:` text instead of synthetic labels?
   - Violation: The plan puts all changes into one large code block, or uses
     address labels that readers must resolve manually.

12. `qa-strategy-explicit`
   - Question: Does `QA Strategy` name proof weight, checks, manual evidence,
     delegated lanes, review gates, goal-advisor inputs, final artifacts, and
     for material feature work, the critical path being claimed with smaller
     ordered sanity checks when full end-to-end proof is too long?
   - Violation: The plan says only "run tests" or "verify manually", or proves
     nearby pieces while leaving the claimed workflow/lifecycle implicit.

13. `architecture-signatures`
   - Question: Does each material plan expose compact top-level
     `architecture_signatures` with module-level seams, main-flow signatures,
     relevant typed data movement, and the builder-owned freeform boundary?
   - Violation: The plan only describes files or prose, omits top-level seams,
     or uses `not_applicable` for work that changes architecture, ownership,
     data flow, proof, or reviewability.

14. `change-plan-signature-linkage`
   - Question: Do the Change Plan units connect to the proposed architecture
     signatures while keeping `signature_or_type_impact` local to each unit?
   - Violation: The architecture block and change units tell separate stories,
     or every change unit duplicates the full architecture map.

15. `docs-strategy`
   - Question: Does the plan include `Docs Strategy` with `outcome`,
     `doc_targets`, `no_docs_reason`, and `validation`, using `doc-advisor`
     when the decision is nontrivial?
   - Violation: The plan omits docs strategy, preserves `close_ticket` or
     `documentation_skill` fields, or uses `no_docs` without a concrete reason.

16. `ui-design-baseline`
   - Question: For UI/design work, does the ticket reference `design.md` or a
     clear no-design-needed reason?
   - Violation: Visual proof depends on unstated taste or layout assumptions.

17. `subagent-proof`
   - Question: Are QA, visual judgment, adversarial proof, and review assigned
     to their owner lanes when material?
   - Violation: The implementation executor can self-approve those claims.

18. `final-evidence`
   - Question: Does UI/user-visible proof require final image evidence or an
     explicit blocker?
   - Violation: The final report can pass without showing the UI state.

19. `minimal-impl-plan-claim`
   - Question: Does the plan explicitly state that this is the minimal
     implementation plan that satisfies the selected ticket?
   - Violation: The plan includes future-proofing, optional artifacts, broad
     cleanup, or unneeded new surfaces without saying why they are required
     now.

20. `existing-service-fit`
   - Question: For every proposed new function, helper, service, or module, did
     the planner prove it cannot belong to an existing service, module, helper,
     or owner surface?
   - Violation: The plan defines a new function or service-shaped surface
     without checking nearby owners first.

21. `grounding-evidence`
   - Question: For implementation feature work, does `QA Strategy` or `Notes` require code
     documentation or maintained implementation evidence before finalizing, using
     Ref MCP, official docs, GitHub code search, maintained examples, or web
     sources unless the ticket is explicitly local-only?
   - Violation: The plan can be completed from local intuition and tests alone
     without naming current source evidence or a local-only reason.

22. `independent-plan-review`
   - Question: Did a material plan request or attach a native `reviewer` lane
     review against declared rubrics before claiming approval-ready state?
   - Violation: The planner self-approves a material plan, relies on a
     skill-local review note as the final gate, or omits the reviewer receipt
     or explicit revise/block status.

23. `visual-companion-boundary`
   - Question: Does every impl-plan ticket have an existing, structurally valid,
     non-blocking `diagrams.md` companion while keeping every diagram format
     and embedded diagram asset out of `ticket.md`?
   - Violation: The ticket embeds a diagram, links a missing or invalid
     companion, uses a not-applicable exemption, or makes diagram review part of the reviewer
     gate without an explicit operator request.

24. `visual-companion-colored-delta`
   - Question: Does `diagrams.md` use explicit `Before` and `After` sections
     with Mermaid `classDef` colors applied to problem/before,
     added/after, changed, and kept boxes?
   - Violation: The companion contains uncolored Mermaid, generic supplemental
     diagrams, or diagrams that do not make the old-to-new difference visible
     from the boxes themselves.

## Finish Gate

For material plans, include a compact readiness note in the ticket handoff or
`Notes` when it needs to remain durable:

```text
plan_qa:
  minimal_required_version: pass | revise | block
  reuse_before_new_surface: pass | revise | block
  least_parameters: pass | revise | block
  canonical_schema_minimality: pass | revise | block | not_applicable
  new_files_functions_justified: pass | revise | block
  minimal_impl_plan_claim: pass | revise | block
  existing_service_fit: pass | revise | block
  goal_advisor_ready: pass | revise | block | not_applicable
  clarifying_questions: pass | revise | block
  architecture_signatures: pass | revise | block | not_applicable
  change_plan_signature_linkage: pass | revise | block
  change_plan_locality: pass | revise | block
  qa_strategy_explicit: pass | revise | block
  docs_strategy: pass | revise | block
  independent_plan_review: pass | revise | block
  visual_companion_boundary: pass | revise | block
  visual_companion_colored_delta: pass | revise | block
  grounding_evidence: pass | revise | block | local_only
  highest_risk:
  fix_or_deferral:
```
