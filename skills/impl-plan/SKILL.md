---
name: impl-plan
description: "Turn one selected coding ticket or material implementation request into an approval-ready ticket plan, test strategy, and proof contract."
tier: 3
source: local
skill_template_version: "0.3.0"
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
review checks live in references and load only when drafting or checking a
material plan.

## Skill Signature

```text
impl_plan(ticket_or_request, proof_weight?) -> ticket_plan + test_strategy + proof_contract

state:
  reads(active ticket, linked PRD/specs/docs, relevant code,
        docs/MEMORY.md?, docs/TROUBLES.md?, docs/LESSONS.md?,
        optional design.md or Agent Testability Brief)
  writes(ticket.md updates, optional design.md recommendation,
         proof route, approval handoff)

gates:
  ticket_surface_exists; code_context_read; done_proof_concrete;
  minimal_plan_challenge_passed; proof_route_named;
  approval_before_build

routes:
  research:gap | research:parity | deep-system-design |
  goal-advisor | qa | visual-qa | agent-qa-test | review

fails:
  chat-only material plan; hidden architecture invention; vague "run tests";
  over-scoped new files/functions/parameters without reuse proof;
  self-certified QA/review for material work; implementation before approval
```

## Phase Boundary

This skill owns planning only. It may shape `Summary`, `Scope`, `Delta`,
`Program`, `Map`, `Done / Proof`, `State`, `Links`, `Notes`, `Agent Contract`,
`Run Hints`, or Goal Packet fields, but implementation, QA, visual judgment,
adversarial testing, demo, and final review are delegated to owner surfaces.

Call `research:*`, `deep-system-design`, `review`, or other workflow skills only
when the child scope is narrower than the selected ticket and the phase needs
its own artifact, independent judgment, or proof surface.

<!-- BEGIN FARPLANE_IMPORTANT_CHECKLIST -->
## Todo List

- [ ] 1. Bind or create the ticket surface.
  - [ ] For material work with no selected ticket, create or update
    `tickets/TASK-XXXX/ticket.md` before treating the plan as ready.
  - [ ] For tiny one-turn fixes, state why ticket-backed planning is not needed.
- [ ] 2. Read the minimum planning context.
  - [ ] Read the active ticket first, then linked PRD/specs/docs, memory,
    troubles, lessons, and nearby code.
  - [ ] Read enough code to name real files, seams, signatures, and typed data
    movement; do not plan from intuition.
  - [ ] Load [references/template.md](references/template.md) when drafting or
    rewriting the ticket body.
  - [ ] Load [references/review.md](references/review.md) before handoff.
- [ ] 3. Route unresolved scope.
  - [ ] Use [research:gap](../research/SKILL.md#researchgap) for missing or
    partial feature work whose production expectation is unclear.
  - [ ] Use [research:parity](../research/SKILL.md#researchparity) when peer
    norms determine scope.
  - [ ] Use [deep-system-design](../deep-system-design/SKILL.md) before
    planning if entities, storage ownership, runtime boundaries, or public API
    shape are still being invented.
- [ ] 4. Draft the ticket-as-program plan.
  - [ ] Keep the selected coherent ticket whole unless proof, reuse, blocker
    risk, external dependency, safety, or runtime ownership forces a split.
  - [ ] Use the canonical ticket-body shape: `Summary`, `Scope`, `Delta`,
    `Program`, `Map`, `Done / Proof`, `State`, `Links`, and sparse `Notes`.
  - [ ] Make `Delta`, `Program`, `Map`, and `Done / Proof` concrete enough that
    a builder can execute without inventing the order.
  - [ ] Include options only when a real material fork exists, then recommend
    one path and name the accepted tradeoff.
- [ ] 5. Make proof and test strategy observable.
  - [ ] Write or refine `Done / Proof` with done conditions, mechanical checks
    or `Metrics: none mechanical`, manual checks, review rubric/TAS gates, hard
    gates, human gates, and required evidence.
  - [ ] Name `Proof weight:` and `Delegated lanes:` for material work when QA,
    visual judgment, agent QA, demo, or reviewer evidence is required.
  - [ ] For UI/user-visible work, name the design baseline, key screens/states,
    expected screenshots, runtime entry path, capture lane, visual judgment lane,
    and final image evidence rule.
- [ ] 6. Run the minimality and quality gates.
  - [ ] Run [qa_checklist.md](qa_checklist.md) against material plans before
    accepting them, especially minimal version, reuse, least parameters,
    function/file necessity, split boundary, and proof-route checks.
  - [ ] Tighten any failed checklist or review item before presenting the plan;
    record explicit `revise` or `block` only when the issue cannot be resolved
    inside planning.
- [ ] 7. Handoff for approval, not implementation.
  - [ ] Leave material tickets in `review` until approval exists.
  - [ ] End with the decisive readiness call, remaining blocker if any, and the
    next owner surface such as `goal-advisor`, `qa`, `visual-qa`,
    `agent-qa-test`, or `review`.
<!-- END FARPLANE_IMPORTANT_CHECKLIST -->

## Templates

Use [references/template.md](references/template.md) for the ticket body. The
approval core is:

```text
Delta(before, after, why_now, first_principles_basis?)
Program(vars, ordered_operations, outputs)
Map(touch, inspect, seams?, typed_flow?)
DoneProof(done_when, checks, manual, review, evidence)
PlanQA(minimality, reuse, parameters, files_functions, proof_route)
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
- Do not bury the key code seams in prose when a compact map or signature list
  would prove understanding faster.
- Do not add optional ticket sections as decoration. `Gap Analysis`, `Run
  Hints`, `Agent Contract`, sidecar `plan.md`, and citations appear only when
  they reduce ambiguity or prove a decision.
- Do not treat tests alone as UI/user-visible proof when screenshots, logs,
  browser state, or visual judgment are required.

## Reference Map

- [references/template.md](references/template.md) - load when drafting or
  rewriting the ticket body.
- [references/review.md](references/review.md) - load before handoff to tighten
  the plan.
- [qa_checklist.md](qa_checklist.md) - run against material plans and against
  changes to this skill's planning behavior.
- [references/examples.md](references/examples.md) - load only when examples are
  needed to calibrate output shape.
- [prompts/plan.md](prompts/plan.md) - update when prompt wording must stay in
  sync with this contract.

## Output

- Updated or proposed `tickets/TASK-XXXX/ticket.md` in canonical ticket-body
  shape.
- Concrete test strategy and `Done / Proof` contract with proof weight,
  delegated lanes, and required evidence.
- `plan_qa` readiness note for material plans, or a blocker naming the missing
  objective, architecture boundary, code context, or proof route.
- Approval handoff that keeps planning separate from implementation.
