---
title: Impl Plan QA Checklist
owner: impl-plan
status: active
kind: qa-checklist
created_at: 2026-06-22
updated_at: 2026-06-23
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
  -> block when the objective, architecture boundary, or proof route is still unknown
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

8. `goal-packet-preview`
   - Question: For Goal-backed work, does the approval surface include the
     Goal Packet preview: `ticket.md`, `program.md`, `progress.md`, `Files`,
     `Budget`, `Metric`, `Proof Route`, `Drift Policy`, `Final Evidence`, and
     native `/goal` prompt?
   - Violation: The human approves only the ticket plan, while the Goal Packet
     is compiled later without review.

9. `clarifying-questions`
   - Question: Did the planner ask up to 3 blocking clarifying questions when
     objective, acceptance criteria, constraints, target files, proof weight,
     permissions, human gates, or destructive/deploy/spend boundaries were
     missing?
   - Violation: The plan guesses at a materially branching input without
     asking or recording a safe assumption.

10. `proof-route-explicit`
   - Question: Does `Done / Proof` name checks, manual evidence, delegated
     lanes, review gates, and final artifacts?
   - Violation: The plan says only "run tests" or "verify manually".

11. `documentation-closeout-route`
   - Question: Does the plan name the final docs/closeout route: `close-ticket`
     for ticket writeback and durable docs changed, plus `documentation` only
     when substantive durable doc writing or revision is in scope?
   - Violation: The plan omits docs closeout entirely, or calls
     `documentation` for routine ticket writeback that `close-ticket` owns.

12. `ui-design-baseline`
   - Question: For UI/design work, does the ticket reference `design.md` or a
     clear no-design-needed reason?
   - Violation: Visual proof depends on unstated taste or layout assumptions.

13. `subagent-proof`
   - Question: Are QA, visual judgment, adversarial proof, and review assigned
     to their owner lanes when material?
   - Violation: The implementation executor can self-approve those claims.

14. `final-evidence`
   - Question: Does UI/user-visible proof require final image evidence or an
     explicit blocker?
   - Violation: The final report can pass without showing the UI state.

## Finish Gate

For material plans, include a compact readiness note in the ticket `State` or
handoff:

```text
plan_qa:
  minimal_required_version: pass | revise | block
  reuse_before_new_surface: pass | revise | block
  least_parameters: pass | revise | block
  new_files_functions_justified: pass | revise | block
  goal_packet_preview: pass | revise | block | not_applicable
  clarifying_questions: pass | revise | block
  proof_route_explicit: pass | revise | block
  documentation_closeout_route: pass | revise | block
  highest_risk:
  fix_or_deferral:
```
