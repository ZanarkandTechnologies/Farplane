---
title: Impl Plan QA Checklist
owner: impl-plan
status: active
kind: qa-checklist
created_at: 2026-06-22
updated_at: 2026-06-22
applies_to:
  - implementation-plans
  - coding-tickets
---

# Impl Plan QA Checklist

Use this after material `impl-plan` changes or before accepting a generated
implementation plan.

## Checks

1. `ticket-first`
   - Question: Is the material plan written into or attached to a selected
     `tickets/TASK-XXXX/ticket.md`?
   - Violation: The plan exists only in chat.

2. `proof-route-explicit`
   - Question: Does `Done / Proof` name checks, manual evidence, delegated
     lanes, review gates, and final artifacts?
   - Violation: The plan says only "run tests" or "verify manually".

3. `ui-design-baseline`
   - Question: For UI/design work, does the ticket reference `design.md` or a
     clear no-design-needed reason?
   - Violation: Visual proof depends on unstated taste or layout assumptions.

4. `subagent-proof`
   - Question: Are QA, visual judgment, adversarial proof, and review assigned
     to their owner lanes when material?
   - Violation: The implementation executor can self-approve those claims.

5. `final-evidence`
   - Question: Does UI/user-visible proof require final image evidence or an
     explicit blocker?
   - Violation: The final report can pass without showing the UI state.
