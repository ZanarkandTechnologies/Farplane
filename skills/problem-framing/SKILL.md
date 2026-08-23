---
name: problem-framing
description: "Turn a complaint or feature request into a clear problem frame, realistic constraints, product boundary, and next owner before MVP or ticket work."
tier: 2
source: local
capability:
  kind: shortcut
template_uses:
  skill-template: "0.3.7"
allowed-tools: Read, Glob, Grep
---

# Problem Framing

## Context

Use this before PRDs, MVP briefs, implementation plans, or system design when
the input is still a complaint, feature request, vague pain, outreach insight,
or symptom. The skill's job is to prevent the first named artifact from
becoming the product by default.

This is not general brainstorming. It converges messy input into a problem
frame that another workflow can use. It should preserve uncertainty instead of
inventing client truth.

## Skill Signature

```text
problem_framing(complaint, context?, audience?, current_workflow?, constraints?)
  -> problem_frame
   + realistic_parameters
   + product_boundary_options
   + recommended_next_owner
state: reads(supplied notes, tickets, docs, local context, source snippets);
       writes(problem frame or handoff artifact only when caller owns a file)
gates: symptom_problem_split; actor_named_or_unknown; constraints_labeled;
       product_boundary_not_assumed; next_owner_named
routes: research:user-grounding | research:parity | prd |
  deep-system-design | functional-ui | impl-plan | solution-shaping
fails: treats requested feature as the problem; overbuilds to a platform;
  hides assumptions; produces tickets before the problem is framed
```

## Phase Boundary

Run grounding, reasoning, and review inline by default. Call `research:*` only
when current practice, best-in-class practice, or user reality is needed before
the frame is trustworthy. Stop for operator clarification when the missing
input is a human answer rather than a research question.

<!-- BEGIN FARPLANE_IMPORTANT_CHECKLIST -->
## Todo List

- [ ] 1. Bind the raw input and source status.
  - [ ] Capture the complaint, requested feature, or observed pain literally.
  - [ ] Label source status as `reported`, `inferred`, `observed`, or
        `unknown`.
- [ ] 2. Split symptom from problem.
  - [ ] Name what the requester asked for.
  - [ ] Name the likely pain, decision, delay, risk, cost, or manual work that
        produced the request.
  - [ ] If the underlying problem is unclear, keep multiple candidate frames.
- [ ] 3. Identify actor, job, stakes, and realistic parameters.
  - [ ] Name who acts, what decision or workflow they own, and what happens if
        it fails.
  - [ ] Name known constraints such as permissions, data access, security,
        time, budget, politics, compliance, and changing requirements.
  - [ ] Mark unknowns instead of filling them with plausible fiction.
- [ ] 4. Map the current workflow enough to reason.
  - [ ] Capture current inputs, handoffs, decisions, tools, outputs, and
        bottlenecks when available.
  - [ ] Ask why the current workflow exists and classify constraints as
        `hard`, `soft`, `inherited`, `obsolete`, or `unknown`.
- [ ] 5. Rebuild from first principles.
  - [ ] Name the irreducible job or outcome if the inherited workflow were
        stripped back to zero.
  - [ ] Compare current workflow versus simplest plausible correct workflow.
- [ ] 6. Ground when the frame depends on external or user reality.
  - [ ] When user groups, jobs, context, friction, or success signals are not
        known, state the exact user-grounding evidence need and keep the frame
        provisional.
  - [ ] When best-in-class or current-practice evidence could change the frame,
        state the exact parity evidence handoff the operator must request.
- [ ] 7. Choose or preserve product boundary options.
  - [ ] Compare plausible boundaries such as manual service, static tool,
        workflow assistant, dashboard, system of record, automation, or platform.
  - [ ] Recommend the smallest boundary that solves the real problem, or keep a
        decision open with the exact evidence needed.
- [ ] 8. Produce the problem frame and route the next owner.
  - [ ] Include problem statement, actor, current workflow, why-chain,
        first-principles basis, constraints, boundary options, recommendation,
        assumptions, and next owner.
  - [ ] State one operator-visible next-owner need in plain language: system or
        data design, UI/workflow design, product requirements, implementation
        planning, or agency MVP synthesis.
  - [ ] Finish-check: the output must make the requested artifact look like
        evidence, not automatically like the solution.
<!-- END FARPLANE_IMPORTANT_CHECKLIST -->

## Templates

Problem frame:

```text
Raw complaint:
Requested artifact:
Source status:
Symptom:
Problem statement:
Actor / job:
Stakes:
Current workflow:
Why current workflow exists:
First-principles basis:
Realistic parameters:
Product boundary options:
Recommended boundary:
Assumptions and unknowns:
Evidence needed:
Next owner:
```

Short example:

```text
Raw complaint: "We need a static pricing calculator."
Requested artifact: static calculator.
Problem statement: Sales cannot produce reliable quotes because pricing inputs,
approvals, and cost assumptions are scattered across people and files.
Recommended boundary: quote workflow slice, not a standalone calculator and not
a full ERP until record-of-truth constraints are proven.
Next owner: solution-shaping or deep-system-design, depending on whether this is
an agency proposal or an approved system build.
```

## Gotchas

- A feature request is evidence. It is not automatically the problem.
- Do not turn every operational complaint into an ERP, dashboard, or AI agent.
- Do not erase uncertainty. A problem frame with honest unknowns is stronger
  than a confident fake brief.
- Do not start implementation planning until the actor, job, stakes, and
  product boundary are coherent.

## Reference Map

- [examples/static-calculator-problem-frame/example.md](examples/static-calculator-problem-frame/example.md) - use as a quality reference for symptom/problem split and product-boundary restraint.

## Output

Return a compact problem frame, or write it to the caller-owned ticket, PRD,
MVP brief, outreach packet, or product artifact when that owner already exists.
