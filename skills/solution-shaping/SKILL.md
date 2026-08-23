---
name: solution-shaping
description: "Turn a reported problem or outreach target into a realistic solution brief, proof model, and PRD or ticket handoff for agency-style product work."
tier: 3
group: deals
source: local
template_uses:
  skill-template: "0.3.7"
allowed-tools: Read, Glob, Grep
---

# Solution Shaping

## Context

Use this for agency-style product work where a person, prospect, team, or client
has a likely operational problem and the desired output is a realistic solution
brief or MVP boundary they can review. The input may be a complaint, outreach
target, sales note, client context, or problem report.

This skill composes framing, grounding, solution-boundary selection, proof, and
handoff. It performs the framing step inline before proposing a solution.

## Skill Signature

```text
solution_shaping(problem_report_or_target, context?, audience?, evidence_budget?)
  -> solution_brief
   + proof_model
   + outreach_or_ticket_handoff
state: reads(supplied context, prospect notes, problem frames, research notes,
             existing tickets/docs when present);
       writes(solution brief or handoff only when caller owns an artifact)
gates: problem_frame_exists; realistic_solution_boundary; proof_model_named;
       risks_and_assumptions_section_present; decision_rights_permissions_named_for_system_mvp;
       mvp_walkthrough_present_for_operational_systems; assumptions_labeled; next_owner_named
routes: research:user-grounding | research:parity |
  demo-realism | prd | impl-plan | goal-advisor
fails: sends a feature pitch without problem proof; invents client facts;
  overbuilds the solution; creates autonomous tickets before reviewable scope
```

## Phase Boundary

Keep the full solution synthesis inline unless a child phase needs separate
evidence. Produce the problem frame inline, use `research:*` for user or
best-practice grounding, `demo-realism` when the MVP needs believable operating
examples, `prd` for product scope, and `impl-plan` or `goal-advisor` only after
the solution boundary is accepted. For material operational or demo-bound
solutions, read the first-load Todo List guardrails before shaping and apply it once more to the
completed brief. One QA owner should judge the whole solution; do not split the
checklist into a queue of tiny review tasks.

<!-- BEGIN FARPLANE_IMPORTANT_CHECKLIST -->
## Todo List

- [ ] 1. Bind the source and intent.
  - [ ] Identify whether the input is a complaint, outreach target, client note,
        existing problem frame, or accepted product direction.
  - [ ] Label facts as `supplied`, `observed`, `researched`, `inferred`, or
        `unknown`.
- [ ] 2. Produce or read the problem frame.
  - [ ] When the problem frame does not already exist, establish the actor,
        job, stakes, constraints, evidence status, and boundary options inline.
  - [ ] Do not proceed to MVP selection while the frame lacks actor, job,
        stakes, constraints, or boundary options.
- [ ] 3. Ground the opportunity enough for an honest solution.
  - [ ] Use `research:user-grounding` when the target user's job, friction, or
        success signal is uncertain.
  - [ ] Use `research:parity` when current practice or best-in-class workflow
        could change the MVP boundary.
  - [ ] For outreach targets, include an explicit correction ask that invites
        the prospect to reject or revise the inferred pain.
  - [ ] For inferred outreach targets, include a visible pre-implementation
        handoff such as `Next owner: research:user-grounding`, outreach review,
        or parity research before any build route.
  - [ ] Mark missing evidence instead of making a polished fake pitch.
- [ ] 4. Generate solution boundary options.
  - [ ] Compare at least two plausible shapes such as manual service, static
        tool, workflow assistant, dashboard, integration, automation, system of
        record, or platform.
  - [ ] Include why each option could be too small, too large, or just right.
  - [ ] When several reported problems share the same planning, allocation, or
        rebalance decision, synthesize the common operating loop before splitting
        them into separate modules.
  - [ ] For planning or allocation problems, test whether scoring, maps,
        calculators, and forecasts are inputs to a shared decision loop rather
        than separate products. Load the Mine-To-Margin reference standard for
        the full operational pattern.
  - [ ] For ERP-adjacent planning problems, state the system boundary: the MVP
        is a decision layer beside ERP, APS, GIS, mine-planning, or accounting
        systems, not a replacement system of record.
- [ ] 5. Recommend the smallest realistic solution.
  - [ ] Choose the solution boundary that solves the framed problem with the least false
        system commitment.
  - [ ] Name V1, deferred V2 scope, and explicit non-goals.
- [ ] 6. Define proof, demo, and review model.
  - [ ] Name what the prospect/client should be able to review.
  - [ ] Name success signal, guard metrics, anti-metrics, evidence to capture,
        and what would disprove the MVP.
  - [ ] Add an explicit `Risks and assumptions` section; do not scatter risks
        only inside prose.
  - [ ] Use `demo-realism` when believable data, workflow states, or operating
        examples are required before design/build.
  - [ ] For an operational decision system, use the Mine-To-Margin reference
        standard: one valuable decision loop, a deterministic mechanism,
        inspectable evidence, responsive scenarios, and an honest
        productionization boundary.
- [ ] 7. Produce the solution brief.
  - [ ] Include target/person, problem frame, current workflow hypothesis,
        first-principles insight, recommendation, V1/V2 split, proof model,
        risks, assumptions, and next owner.
  - [ ] For operational MVPs, include a concrete walkthrough: inputs, user
        steps, system decisions, core calculation or state transition, outputs,
        review cadence, and how actuals feed back into the next run.
  - [ ] For operational decision systems, include an ordinary case, a binding
        constraint or shortage, and a changed-market or changed-demand case so
        the client can see whether the decision responds correctly.
  - [ ] For system-heavy, regulated, safety-critical, or coordination-heavy
        solutions, explicitly name decision rights, permissions, records/entities,
        and workflow risks at a high level.
  - [ ] If the result is still speculative, hand off to research or review
        rather than implementation.
- [ ] 8. Route the handoff.
  - [ ] Route broad product scope to `prd`.
  - [ ] Route system/data-heavy MVPs to `deep-system-design` before
        implementation planning; name the data, permission, and decision-rights
        questions that design must settle.
  - [ ] Route UI/workflow-heavy MVPs to `functional-ui`.
  - [ ] Route inferred outreach hypotheses to `research:user-grounding`,
        outreach review, or parity research before implementation.
  - [ ] Route accepted build slices to `impl-plan`.
  - [ ] Route approved autonomous execution to `goal-advisor`.
  - [ ] Finish-check: a skeptical reviewer can see why this solution realistically
        solves the framed problem and what evidence would change the answer.
<!-- END FARPLANE_IMPORTANT_CHECKLIST -->

## Templates

Solution brief:

```text
Target / client:
Source status:
Reported problem or outreach signal:
Problem frame:
Actor / job / stakes:
Current workflow hypothesis:
First-principles insight:
Best-practice or user-grounding status:
Solution options:
Recommended solution:
V1 scope:
Deferred V2:
Non-goals:
Proof model:
Demo / review artifact:
MVP walkthrough:
Risks and assumptions:
Pre-implementation route:
Next owner:
```

Short example:

```text
Reported problem: Sales needs a static pricing calculator.
Problem frame: quoting is unreliable because pricing inputs, approvals, and
cost assumptions are scattered.
Recommended MVP: quote workflow slice that captures inputs, applies known
rules, flags approval cases, and records quote decisions.
Deferred V2: ERP integration, inventory/capacity ownership, automated order
lifecycle.
Proof model: prospect can review a realistic quote flow with representative
data and say whether it would reduce quote delay or quote errors.
Next owner: prd for product scope or impl-plan after MVP acceptance.
```

## Gotchas

- Do not sell a solution before the problem frame is coherent.
- Do not infer private facts about a prospect as truth; label outreach guesses.
- Do not leave inferred outreach angles with only a pitch or correction ask;
  name the pre-implementation route before any PRD, ticket, or build handoff.
- Do not make a slick prototype the proof if the real proof is workflow fit.
- Do not route to `goal-advisor` until the MVP boundary is accepted or the
  ticket explicitly says to execute.
- Do not reward exact labels such as "quote workflow" unless the reasoning also
  shows why a calculator is too small and an ERP/platform is too large.
- Do not stop at a list of modules when the real MVP is a planning or decision
  loop. Show how the operator would run the loop and what calculation or state
  transition makes the product valuable.
- Do not collapse an operational decision system into a scoring dashboard when
  the valuable behavior is allocation, scheduling, approval, or rebalance.

## Reference Map

- [examples/static-calculator-solution-brief/example.md](examples/static-calculator-solution-brief/example.md) - use as a quality reference for solution-shaping synthesis and V1/V2 restraint.
- [Mine-To-Margin reference standard](references/mine-to-margin-reference-standard.md) - load when shaping or reviewing an operational decision system or a use case intended for a customer-facing agent demo.
- the first-load Todo List guardrails - load before and after material operational or demo-bound shaping work; assign the complete review to one QA owner.

## Output

Return a solution brief and handoff. Write it to a PRD, outreach artifact,
ticket, or Goal Packet only when the caller has supplied or created that owner
surface.
