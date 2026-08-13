---
name: functional-ui
version: 1.2.0
description: "Turn unclear product workflows into operated comparable evidence, an interaction model, optional low-fi wireflow, and a planning handoff."
tier: 3
group: operations
source: local
template_uses:
  skill-qa-checklist: "0.1.0"
  skill-eval-task: "0.2.0"
qa_checklist: qa_checklist.md
eval: evals/evals.json
common_chains:
  after: ["visual-design"]
allowed-tools: Read, Grep, Glob, Bash
---

# Functional UI

<!-- BEGIN FARPLANE_IMPORTANT_CHECKLIST -->
## Todo List

- [ ] State the UI/workflow decision and the artifact being produced:
  diagnosis, UX brief, redesign recommendation, or planning handoff.
- [ ] Read [qa_checklist.md](qa_checklist.md) before execution when the task
  will shape an app screen, panel, dashboard, form, or control surface.
- [ ] Use [research:user-grounding](../research/SKILL.md#researchuser-grounding)
  when users, jobs, contexts, friction, or success signals are not already
  settled.
- [ ] Use [research:competitor](../research/SKILL.md#researchcompetitor) or
  [research:parity](../research/SKILL.md#researchparity) when comparable app
  workflows or established product patterns should shape the options.
- [ ] For a material, unsettled, current, or SOTA workflow, use the Codex
  in-app Browser to operate 2-4 established comparables or direct products and
  capture the actual sequence, states, and access limits. Reuse one browser
  binding with a tab per source; do not substitute web search or documentation
  for this operation step. Record source URL, user job/query, observed
  behavior, evidence
  refs, and `adopt | adapt | reject`. Skip this pass for tiny same-pattern
  fixes, already-settled interaction models, and pure visual polish. Pinterest
  and similar taste surfaces may inform `visual-design` or `ingest-content`,
  but do not count as functional workflow proof. If browser operation itself
  is unavailable, record `browser_operation: blocked` with the exact tool or
  access limit; public docs may support a provisional recommendation but must
  not be labeled operated workflow evidence.
- [ ] If the task already supplies a current browser-operation receipt for the
  same user job, validate its URLs, observed sequence/states, access limits,
  evidence refs, and `adopt | adapt | reject` decisions, then reuse it instead
  of rerunning the same sources. A fresh complete receipt satisfies the
  operation gate; a docs-only summary does not.
- [ ] Diagnose the current UI or planned workflow before proposing visual or
  component changes.
- [ ] Run the **Steve Jobs Focus & Simplicity Pass**: name the customer benefit,
  core action, what can be removed or deferred, and the deliberate `no`; do not
  remove required states, accessibility, safety, or evidence.
- [ ] Use the native planning phase to compare the strongest interaction models
  and choose one recommended workflow.
- [ ] Define screens, states, IA, interaction rules, data/content ranges, and
  edge cases.
- [ ] Draw a low-fi ASCII wireflow only when it resolves a user journey,
  information hierarchy, or responsive transition that a state table cannot.
- [ ] Hand the accepted UX context to [impl-plan](../impl-plan/SKILL.md), which
  decides whether visual or asset context is also unresolved.
- [ ] Apply [qa_checklist.md](qa_checklist.md) again before completion for
  material screen, panel, dashboard, form, or control-surface plans.
- [ ] Use the native execution phase for proof/writeback shape before
  claiming the functional UI plan is ready.
<!-- END FARPLANE_IMPORTANT_CHECKLIST -->

Use this before visual implementation when the question is how the product should work, why a current UI feels wrong, or how a component/flow should be redesigned from proven examples.

## Job

1. Identify the user, context, and top jobs-to-be-done.
2. Diagnose the current UI or planned workflow.
3. Study comparable/latest examples and the workflows they prove.
4. Run the **Steve Jobs Focus & Simplicity Pass**: name the customer benefit,
   core action, what can be removed or deferred, and the deliberate `no`.
5. Compare 3 viable interaction models or redesign paths.
6. Recommend one path clearly.
7. Define states, IA, interaction rules, and implementation handoff.

## Use When

- the user asks for UI or UX direction
- the user says "this UI sucks", "functional-ui this", "redesign this component", or asks why a screen/flow feels wrong
- a screen or flow needs functional structure before styling
- product behavior, IA, or workflow is still open
- the team keeps redesigning common patterns from scratch
- `impl-plan` is planning UI work and no current UX brief settles users, states,
  and interactions

## Do Not Use When

- the workflow is already chosen and the task is purely visual polish
- the request is a landing page narrative; use `landing-page`
- the task is a finished UI review; use `web-design-guidelines`

## Workflow

1. Capture the primary user/persona and the top jobs-to-be-done.
2. Read the PRD, spec, ticket, request, screenshot, or current component to extract states, constraints, and failure modes.
3. Diagnose the current UI using [redesign-diagnosis.md](references/redesign-diagnosis.md) when a broken UI exists.
4. For material, unsettled, current, or SOTA workflows, operate 2-4 comparable
   apps, examples, or established patterns with the Codex in-app Browser using
   [comparable-patterns.md](references/comparable-patterns.md). Capture actual
   workflow/state evidence and access limits; focus on behavior, not surface
   aesthetics. Use settled local patterns without broad research for tiny
   same-pattern corrections.
5. Run the **Steve Jobs Focus & Simplicity Pass** before adding options: state
   the customer benefit, core action, removal or deferral, and deliberate `no`.
   Preserve required states, accessibility, safety, and comparable evidence.
6. Produce 3 grounded UI options with pros and cons.
7. Recommend one workflow and explain why it best fits the user stories.
8. Define screens, states, IA, interaction rules, data/content ranges, and edge cases.
9. Add a low-fi ASCII wireflow only when it materially clarifies flow or
   hierarchy; otherwise keep the state map compact.
10. Hand off with [implementation-handoff.md](references/implementation-handoff.md)
   to `impl-plan` as accepted UX context.

## Decision Branches

| Situation | Output emphasis |
| --- | --- |
| Broken existing component | diagnosis, comparable examples, recommended redesign, implementation handoff |
| New app screen | users, jobs, IA, states, interaction model |
| Repeated workflow | speed, defaults, keyboard/touch paths, empty/error/success states |
| Dense dashboard/tool | scan paths, prioritization, filters, table/list behavior |
| AI/chat/workflow UI | conversation states, tool progress, sources, retry/failure recovery |

## Output

Produce a compact planning artifact with:

- `Users + stories`
- `Current UI diagnosis` when redesigning an existing surface
- `Comparable Evidence Receipt` for material/unsettled/current/SOTA work, with
  2-4 rows containing source URL, user job/query, operated sequence and states,
  evidence ref, access/login limit, and `adopt | adapt | reject`; otherwise an
  explicit `comparable_research_skipped` reason
- `Browser Operation Blocker Receipt` instead of comparable rows only when the
  operation tool cannot run: attempted method/command, exact error or missing
  capability, evidence ref such as captured stderr/tool inventory, public
  surfaces attempted, and `recommendation_status: provisional`
- `Recommendation`
- `Steve Jobs Focus & Simplicity Pass`: customer benefit, core action, removal
  or deferral, and deliberate `no`
- `Key screens/states`, including applicable empty, loading/in-progress,
  partial, success/return, error, and retry/recovery behavior
- `Interaction rules`
- `Low-fi wireflow` when flow or hierarchy needs one; otherwise an explicit
  `wireflow_not_needed` reason
- `Implementation handoff`
- `Options appendix`

## Guardrails

- start from the user story, not the component library
- borrow proven patterns before inventing new ones
- compare workflows, not just visual references
- do not count Pinterest, galleries, or isolated aesthetic screenshots as
  functional workflow proof; route taste evidence to `visual-design` or
  `ingest-content`
- do not bypass login walls or fabricate states hidden behind unavailable
  access; record the limit and continue with accessible comparables
- do not relabel public documentation or search results as browser-operated
  workflow evidence; downgrade the recommendation to provisional when no
  comparable could actually be operated
- always recommend one path; do not stop at inspiration
- use the named pass for disciplined subtraction, not a literal Jobs persona or
  an excuse to hide necessary controls, safety, states, or accessibility
- if the user did not provide a take, assume they want guided product judgment
- do not solve functional failures with visual-only advice
- do not specify final typography/color/motion taste beyond what the interaction model requires; hand that to `visual-design`

## Reference Files

- [redesign-diagnosis.md](references/redesign-diagnosis.md) - diagnose why a current UI fails.
- [comparable-patterns.md](references/comparable-patterns.md) - inspect adjacent products and extract reusable workflow patterns.
- [implementation-handoff.md](references/implementation-handoff.md) - package UX decisions for `impl-plan`.
- [architecture.md](references/architecture.md) - ownership boundary and downstream handoff model.
- [workflows.md](references/workflows.md) - broken UI and new screen/flow paths.
- [gotchas.md](references/gotchas.md) - common functional-UI failure modes.
