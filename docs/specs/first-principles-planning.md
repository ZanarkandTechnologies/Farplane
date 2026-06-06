# First-Principles Planning

Use this contract when writing PRDs, specs, tickets, and implementation plans.
The goal is to reduce a request to the durable reasons, constraints, and proof
that make the chosen build path obviously correct.

This is a planning/spec contract, not a standalone skill. Keep the compact
reminder in generated project `AGENTS.md`; keep the detailed method here; wire
the operational checks into `prd`, `spec-to-ticket`, and `impl-plan`.

## Algebra

```text
FirstPrinciplesPlan :=
  Objective
+ UserOrSystemNeed
+ Constraints
+ Assumptions
+ RootCause
+ FirstViableSlice
+ ProofOrFalsification
+ Tradeoffs
+ NonGoals

FirstViableSlice :=
  smallest complete valuable outcome
+ proof that removes the highest uncertainty
+ explicit follow-up boundary
```

## Required Questions

Ask only the questions that change the plan, but make sure the final artifact
can answer these:

- `Objective`: what exact outcome should exist after this work?
- `Need`: whose problem or system failure does it solve?
- `Root cause`: what underlying constraint or failure creates the need?
- `Assumptions`: what must be true for the chosen path to work?
- `Constraints`: what limits the solution space: users, stack, time, budget,
  privacy, performance, tools, data, design, compute, or deployment?
- `First viable slice`: what is the smallest complete result that is useful
  and proves the riskiest assumption?
- `Proof`: what observable artifact, command, QA result, or review would
  falsify or validate the plan?
- `Tradeoffs`: which viable option is chosen and what cost is accepted?
- `Non-goals`: what tempting adjacent work is explicitly out of scope?

## Anti-Patterns

- Starting from implementation preference before naming the real objective.
- Treating symptoms as root cause.
- Splitting by technical layer instead of by useful, proofable outcome.
- Inventing fake mechanical metrics for judgment-heavy work.
- Letting a plan proceed when its riskiest assumption has no proof surface.
- Adding broad agent instructions to always-loaded prompts when a progressive
  skill, reference, or ticket contract can carry the detail.

## Policy Extraction

When a planning discussion reveals a reusable rule, extract it to the smallest
owning surface:

```text
PolicyExtraction :=
  repeated lesson
+ owning surface
+ context cost
+ proof or drift check
+ durable reference
```

Use this routing:

- `AGENTS.md`: compact always-loaded routing or invariant.
- Generated project `AGENTS.md`: compact project-local operating rule.
- `PROJECT_RULES.md`: stack, commands, runtime, QA paths, and technical
  conventions.
- `docs/specs/*`: canonical contract, equation, lifecycle, or planning model.
- `docs/policies/README.md`: index of where policy lives, not the policy body.
- `skills/*`: repeated procedure or domain method.
- `agents/*.toml`: independent context and owned output.
- hooks/scripts/validators: deterministic drift checks.
- tickets: scoped work, proof, blockers, and closeout.
- `docs/MEMORY.md`: durable invariant only after the rule is reusable.
- `docs/TROUBLES.md`: repeated miss, blocker, or correction before promotion.
- `docs/LESSONS.md`: distilled reusable prevention rule after a fix, repent pass, or drain.

## Artifact Expectations

- PRDs should include first-principles basis before requirements: objective,
  need, constraints, assumptions, first slice, proof, and non-goals.
- Specs should preserve the same basis when they deepen architecture or
  behavior.
- Tickets should carry the basis into `Plan`, `Gap Analysis`, `Verification`,
  and `Proof Contract` without duplicating the whole PRD.
- Implementation plans should challenge whether the ticket's basis is still
  valid against local code, docs, and proof surfaces before execution.
