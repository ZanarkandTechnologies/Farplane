---
name: impl-plan
description: "Turn one selected coding ticket or material implementation request into an approval-ready ticket plan, test strategy, and proof contract."
tier: 3
source: local
template_uses:
  skill-template: "0.3.0"
  skill-eval-task: "0.1.0"
  skill-qa-checklist: "0.1.0"
group: coding
eval: eval_task.json
qa_checklist: qa_checklist.md
common_chains:
  after: ["goal-advisor"]
allowed-tools: Read, Glob, Grep

---

# Impl Plan

## Context

`impl-plan` is the ticket-first planner for material coding work. Its durable
output is a selected or newly created `tickets/TASK-XXXX/ticket.md` shaped for
approval before build. Tiny, reversible fixes can bypass this skill with a
short reason; vague epics route to discovery, system design, PRD, or
ticketization before planning.

Keep first load small. `SKILL.md` owns trigger, inputs, gates, routes, stop
conditions, and the finish contract. Detailed ticket shape, examples, and plan
self-checks live in references or `qa_checklist.md` and load only when drafting
or checking a material plan. Material plan readiness is reviewed by the native
`reviewer` lane, not by a skill-local review note.

## Skill Signature

```text
impl_plan(ticket_or_request, proof_weight?) -> ticket_plan + architecture_signatures + qa_strategy + reviewer_receipt + goal_advisor_readiness

state:
  reads(active ticket, linked PRD/specs/docs, relevant code,
        docs/MEMORY.md?, docs/TROUBLES.md?, docs/LESSONS.md?,
        optional design.md or Agent Testability Brief)
  writes(ticket.md updates, optional design.md recommendation,
         QA strategy, approval handoff)

gates:
  missing_inputs_resolved_or_asked; ticket_surface_exists; code_context_read;
  architecture_signatures_present_or_not_applicable; done_conditions_concrete;
  qa_strategy_concrete; change_plan_units_local; proof_route_named;
  material_reviewer_gate_passed_or_reconciled;
  goal_advisor_ready_after_approval

routes:
  research:gap | research:parity | deep-system-design |
  metric-advisor | goal-advisor | qa | visual-qa | agent-qa-test | review

fails:
  chat-only material plan; hidden architecture invention; vague "run tests";
  over-scoped new files/functions/parameters without reuse proof;
  missing material architecture signatures; self-certified QA/review for
  material work; transcript-dependent Goal setup; implementation before approval
```

## Phase Boundary

This skill owns approval planning only. It may shape `Summary`, `Scope`,
`Delta`, `Change Plan`, `Done`, `QA Strategy`, `Docs Strategy`, `Links`,
`Notes`, `Agent Contract`, and `Run Hints`, but implementation, QA, visual judgment,
adversarial testing, demo, final review, and Goal Packet sidecars are delegated
to owner surfaces.

Call `goal-advisor` after the ticket plan is approved and ready to become a
Goal Packet. `goal-advisor(ticket)` creates or updates `program.md`,
`progress.md`, and the native `/goal` prompt, then links those sidecars from
the ticket. If the ticket plan changes after approval, rerun this skill first
and then regenerate the Goal Packet.
Call `research:*`, `deep-system-design`, `review`, or other workflow skills only
when the child scope is narrower than the selected ticket and the phase needs
its own artifact, independent judgment, or proof surface.

<!-- BEGIN FARPLANE_IMPORTANT_CHECKLIST -->
## Todo List

- [ ] 1. Resolve missing inputs before planning.
  - [ ] Inspect the ticket/request and local context for missing objective,
    acceptance criteria, constraints, target files, proof weight, permissions,
    human gates, or destructive/deploy/spend boundaries.
  - [ ] Ask up to 3 clarifying questions only when the missing input is
    blocking or materially changes the plan or later Goal Packet; otherwise state the
    assumption in the ticket and continue.
- [ ] 2. Bind or create the ticket surface.
  - [ ] For material work with no selected ticket, create or update
    `tickets/TASK-XXXX/ticket.md` before treating the plan as ready.
  - [ ] For tiny one-turn fixes, state why ticket-backed planning is not needed.
- [ ] 3. Read the minimum planning context.
  - [ ] Read the active ticket first, then linked PRD/specs/docs, memory,
    troubles, lessons, and nearby code.
  - [ ] Read enough code to name real files, seams, signatures, and typed data
    movement; do not plan from intuition.
  - [ ] Load [references/template.md](references/template.md) when drafting or
    rewriting the ticket body.
- [ ] 4. Route unresolved scope.
  - [ ] Use [research:gap](../research/SKILL.md#researchgap) for missing or
    partial feature work whose production expectation is unclear.
  - [ ] Use [research:parity](../research/SKILL.md#researchparity) when peer
    norms determine scope.
  - [ ] Use [deep-system-design](../deep-system-design/SKILL.md) before
    planning if entities, storage ownership, runtime boundaries, or public API
    shape are still being invented.
- [ ] 5. Draft the ticket-as-program plan.
  - [ ] Keep the selected coherent ticket whole unless proof, reuse, blocker
    risk, external dependency, safety, or runtime ownership forces a split.
  - [ ] Use the canonical ticket-body shape: `Summary`, `Scope`, `Delta`,
    `Change Plan`, `Done`, `QA Strategy`, `Docs Strategy`, `Links`, and sparse
    `Notes`.
  - [ ] Make `Delta`, `Change Plan`, `Done`, and `QA Strategy` concrete enough
    that a builder can execute without inventing the order or proof route.
  - [ ] For material plans, add `architecture_signatures` at the top of
    `Change Plan`: module-level seams, main flow signatures, typed data
    movement when relevant, and the builder-owned freeform boundary. Use
    `not_applicable` only for tiny localized fixes with a concrete reason.
  - [ ] Use `Change Plan` units as the merged program and file map: each unit
    carries local before/after, read/write paths, operation, local type or
    signature impact, routes, QA expectations, and real failure modes.
  - [ ] Split `Change Plan` into one heading and one fenced block per coherent
    change. Use `fixes:` in plain language instead of synthetic labels
    unless many-to-many traceability truly needs stable anchors.
  - [ ] Include options only when a real material fork exists, then recommend
    one path and name the accepted tradeoff.
- [ ] 6. Make QA Strategy observable.
  - [ ] Write or refine `Done` with concrete completion conditions.
  - [ ] Write or refine `QA Strategy` with proof weight, mechanical checks or
    `Metrics: none mechanical`, manual checks, delegated lanes, review
    rubric/TAS gates, hard gates, human gates, required evidence, final
    checkpoint, and residual risk.
  - [ ] For material feature work, include critical-path proof in
    `QA Strategy`: name the real workflow or lifecycle being claimed,
    break long end-to-end proof into smaller ordered sanity checks, and require
    evidence plus the next review point for state, data, logs, artifacts, UI, or
    session behavior.
  - [ ] For implementation feature work, include `Grounding evidence:` in
    `QA Strategy` or `Notes`: code documentation or maintained implementation evidence
    from Ref MCP, official docs, GitHub code search, maintained examples, or
    web sources before finalizing, unless the ticket is explicitly local-only.
  - [ ] If the metric or provider is unclear, derive a metric card before
    writing `QA Strategy` or Goal-ready run hints.
  - [ ] Name `QA Strategy.goal_advisor_inputs.proof_route`,
    `final_evidence`, and `final_checkpoint` for material work when QA, visual
    judgment, agent QA, demo, or reviewer evidence is required.
  - [ ] For UI/user-visible work, name the design baseline, key screens/states,
    expected screenshots, runtime entry path, capture lane, visual judgment lane,
    and final image evidence rule.
  - [ ] Name `Docs Strategy` by calling or applying
    [doc-advisor](../doc-advisor/SKILL.md): `update_docs` with targets and
    validation, or `no_docs` with a concrete reason.
- [ ] 7. Leave the ticket ready for `goal-advisor`.
  - [ ] Set up the approved ticket contract so `goal-advisor(ticket)` can infer
    task, files, budget hints, QA Strategy inputs, and sidecar needs without
    transcript memory.
  - [ ] Do not duplicate Goal Packet sidecar content in the ticket body.
  - [ ] If an active Goal Packet already exists, keep `Links` pointing to
    `program.md`, `progress.md`, and any generated prompt artifact.
- [ ] 8. Run the minimality and quality gates.
  - [ ] Run [qa_checklist.md](qa_checklist.md) against material plans before
    accepting them, especially minimal version, reuse, least parameters,
    function/file necessity, split boundary, architecture-signature, and
    proof-route checks.
  - [ ] For material plans, request a native `reviewer` lane using
    `docs/review/rubrics/reviewer-handoff.md` with `implementation-plan`,
    `architecture`, and `evidence-quality` unless the ticket declares a
    stronger review route. Reconcile `revise` findings in the ticket before
    calling the plan approval-ready; block on `block` or `invalid`.
  - [ ] Tighten any failed checklist or review item before presenting the plan;
    record explicit `revise` or `block` only when the issue cannot be resolved
    inside planning.
- [ ] 9. Handoff for one-shot approval, not implementation.
  - [ ] Present the ticket plan as the approval contract that
    `goal-advisor(ticket)` will compile after approval.
  - [ ] Leave material tickets in `review` until the ticket plan is approved.
  - [ ] Include the final `Docs Strategy` in the approval handoff so the Goal
    does not silently skip durable docs or invent closeout ceremony.
  - [ ] End with the decisive readiness call, remaining blocker if any, and the
    next owner surface such as `goal-advisor`, `qa`, `visual-qa`,
    `agent-qa-test`, `doc-advisor`, `close-ticket`, or `review`.
<!-- END FARPLANE_IMPORTANT_CHECKLIST -->

## Templates

Use [references/template.md](references/template.md) for the ticket body. The
approval core is:

```text
Delta(overall_before, overall_after, why_now, problems?)
ArchitectureSignatures(module_level, main_flow, data_flow?, builder_freeform_boundary)
ChangePlan(change_units(read, write, operation, local_signature_or_type_impact, routes, qa, failure_modes))
Done(done_when)
QAStrategy(proof_weight, checks, manual, delegated_lanes, review, evidence, goal_advisor_inputs, residual_risk)
GroundingEvidence(source_class, sources_checked, local_only_reason?)
PlanQA(minimality, reuse, parameters, files_functions, proof_route)
ReviewerGate(task_path, rubric_families, required_tas, hard_gates, receipt)
DocsStrategy(outcome, doc_targets, no_docs_reason, validation)
```

For UI/user-visible proof, include this line in the plan:

```text
Final report: include the best screenshot/image evidence as
![best evidence](ABSOLUTE_SCREENSHOT_PATH), or block/revise with the missing
proof reason.
```

## Gotchas

- Do not implement. This skill plans and gates the handoff.
- Do not return a chat-only plan for material work.
- Do not rewrite a coherent ticket into a smaller first slice just because it
  feels safer; split only on a real proof, reuse, blocker, safety, dependency,
  or runtime boundary.
- Do not invent new files, functions, abstractions, parameters, or config knobs
  without proving reuse was checked and the new surface is required.
- Do not bury the key code seams in prose. Material plans must expose compact
  `architecture_signatures` before the per-change units; change-unit
  `signature_or_type_impact` is only for local deltas.
- Do not add optional ticket sections as decoration. `Gap Analysis`, `Run
  Hints`, `Agent Contract`, sidecar `plan.md`, and citations appear only when
  they reduce ambiguity or prove a decision.
- Do not treat tests alone as UI/user-visible proof when screenshots, logs,
  browser state, or visual judgment are required.
- Do not let material feature plans prove only nearby pieces when the claim is
  a workflow or lifecycle. If the true path is long, plan smaller faithful
  checks first, then state what final path remains unrun or blocked.

## Reference Map

- [references/template.md](references/template.md) - load when drafting or
  rewriting the ticket body.
- [qa_checklist.md](qa_checklist.md) - run against material plans and against
  changes to this skill's planning behavior.
- [../metric-advisor/SKILL.md](../metric-advisor/SKILL.md) - metric cards for
  proof providers, guard metrics, anti-metrics, and no-mechanical-metric
  rationale.
- [references/examples.md](references/examples.md) - load only when examples are
  needed to calibrate output shape.
- [prompts/plan.md](prompts/plan.md) - update when prompt wording must stay in
  sync with this contract.

## Output

- Updated or proposed `tickets/TASK-XXXX/ticket.md` in canonical ticket-body
  shape, ready for approval and later `goal-advisor(ticket)` compilation when
  the work is Goal-backed.
- Compact `architecture_signatures` for material work, or a concrete
  `not_applicable` reason for tiny localized fixes.
- Concrete `Done` conditions and `QA Strategy` with proof weight, delegated
  lanes, goal-advisor inputs, final checkpoint, and required evidence.
- Run hints and links that let `goal-advisor(ticket)` create `program.md`,
  `progress.md`, and the native `/goal` prompt after approval, or a clear
  reason direct work is better than Goal mode.
- `Docs Strategy` naming whether durable docs change, which docs are targeted,
  why no docs are needed when applicable, and which validation proves the
  decision.
- Reviewer handoff or receipt for material plans, using the native `reviewer`
  lane and canonical review rubrics instead of a skill-local self-review note.
- `plan_qa` readiness note for material plans, or a blocker naming the missing
  objective, architecture boundary, code context, or proof route.
- One-shot approval handoff that keeps planning separate from implementation
  and names `goal-advisor` as the next owner when Goal execution is warranted.
