---
artifact_type: plan_review
ticket_id: TASK-0396
reviewer_lane: adversarial_plan_review
reviewed_at: 2026-07-20T19:04:00+08:00
verdict: revise
tas: TAS-B
---

# Adversarial plan review — pass 1

## Scope

- `work_type:` material implementation-plan review
- `context_ref:` `tickets/TASK-0396/ticket.md`
- `rubrics:` spec-contract, implementation-plan, architecture,
  skill-contract, integration-readiness, prompt-quality, evidence-quality
- `required_tas:` TAS-A
- `verdict:` revise
- `rerun_required:` yes

## Evidence inspected

- The ticket and its validation result.
- Reviewer handoff, review skill, rubric index, and declared rubric files.
- `impl-plan`, `content-impl-plan`, `goal-advisor`, `brainstorm`, and
  `harness-advisor` contracts.
- Ticket template, FEAT-0007/0008/0032, and proof-review documentation.

## Rubric verdicts

| Rubric | TAS | Verdict |
|---|---:|---|
| spec-contract | TAS-B | revise |
| implementation-plan | TAS-B | revise |
| architecture | TAS-B | revise |
| skill-contract | TAS-B | revise |
| integration-readiness | TAS-B | revise |
| prompt-quality | TAS-B | revise |
| evidence-quality | TAS-B | revise |

## Hard gates

- `One ticket / one canonical target artifact:` fail. The ticket asserts this,
  but its six change groups span multiple output contracts; the required visual
  companion is also not yet generated.
- `No unsupported lean/minimal claim:` fail. The claim has no concrete
  subtractive comparison across the proposed change groups.
- `No new scalar metric/rubric family/runtime/per-metric Goal:` pass.
- `Executable convergence and stop/block semantics:` revise. The intent is
  clear but the acceptance mechanics need to be concrete.
- `Observed backtracking failure closed:` fail. A session ID and summary are
  not a replayable sanitized fixture.
- `Smallest coherent change surface:` fail. Content planning, exploration
  ingress, docs, Goal Advisor, evals, and the core planner/reviewer loop are
  bundled before the core path is proved.

## Findings

1. `High — unsupported minimality claim.` Add a compact subtractive receipt
   comparing core-only, core+Goal, core+ingress, and the six-change plan. Retain
   only changes that uniquely protect a named invariant.
2. `High — artifact/validation contradiction.` Generate and link the required
   `diagrams.md` before planning approval; do not call it non-blocking while
   planning validation blocks on its absence.
3. `High — bundled scope.` Keep the first ticket to the implementation-plan
   rubric, `impl-plan`, focused hardcases, and the smallest required contract
   wording. Content planning and exploration ingress have different artifact
   owners and should not ride this ticket.
4. `Medium — unreplayable failure.` Record sanitized input, failed proposal,
   operator challenge, and expected pre-challenge rejection.

## Subtractive counterplan

Keep this ticket to:

- `docs/review/rubrics/implementation-plan.md`
- `skills/impl-plan/SKILL.md`
- `skills/impl-plan/qa_checklist.md`
- `skills/impl-plan/prompts/plan.md`
- focused `impl-plan` and `review` eval cases
- the smallest required ticket/template/proof-review wording

Defer `content-impl-plan`, `brainstorm`, `harness-advisor`, and
`goal-advisor` changes unless a focused fixture proves the core loop cannot
close without them.

## Final verdict

`revise / TAS-B`. Repair the ticket, generate the visual companion, pass
planning validation, and rerun adversarial review.

---

# Adversarial plan review — pass 2 clean review

## Scope and evidence

- `work_type:` material implementation-plan clean review
- `evidence:` revised `ticket.md`, `diagrams.md`, pass-1 receipt, passing
  planning validation, declared rubrics, and review skill contract
- `overall_tas:` TAS-A
- `verdict:` pass
- `material_delta_found:` no
- `rerun_required:` no for plan approval

## Rubric verdicts

| Rubric | TAS | Rationale |
|---|---:|---|
| spec-contract | TAS-A | Scope is one coherent coding-plan contract; content and exploration surfaces are out. |
| implementation-plan | TAS-A | Ordered changes, proof route, hardcases, stop/block semantics, and subtractive receipt are concrete. |
| architecture | TAS-A | Rubric, reviewer, and planner responsibilities remain separate without a new metric, runtime, or rubric family. |
| skill-contract | TAS-A | Work is bounded to `impl-plan`, existing review judgment, and focused eval coverage. |
| integration-readiness | TAS-A | Companion exists, planning validation passes, and Goal Advisor is composed rather than modified. |
| prompt-quality | TAS-A | Prompt changes have durable context, output boundaries, qualitative judgment, and no recursive delegation. |
| evidence-quality | TAS-A | Pass-1 findings are traceably repaired; the sanitized coding-plan hardcase is sufficient. |

## Hard gates

- `One ticket / one canonical target artifact:` pass.
- `No unsupported lean/minimal claim:` pass; the subtractive receipt supports
  retained scope.
- `No scalar metric/rubric family/runtime/per-metric Goal:` pass.
- `Executable convergence and stop/block semantics:` pass.
- `Observed backtracking failure closed for this artifact:` pass.
- `Smallest coherent change surface:` pass; content planning, exploration
  ingress, Goal Advisor implementation, and feature/system docs are removed or
  explicitly deferred.

## Clean-pass decision

No material subtraction remains. Ticket-template wording is the future-plan
materialization point, review evals prove the judgment path, and Goal language
only composes the existing continuation route.

Non-blocking implementation caution: keep the `prompts/plan.md` edit narrow to
the fixed-point contract; do not expand it into general prompt-style guidance.

Final verdict: `pass / TAS-A`.

---

# Adversarial plan review — pass 3 conditional-placement review

## Scope and verdict

- `work_type:` adversarial material implementation-plan review
- `change_reviewed:` conditional existing Harness Advisor composition
- `rubrics:` spec-contract, implementation-plan, architecture, skill-contract,
  integration-readiness, prompt-quality, evidence-quality
- `overall_tas:` TAS-A
- `verdict:` pass
- `material_delta_found:` no
- `hard_gate_failures:` none
- `rerun_required:` no

## Evidence and hard gates

- The trigger is limited to material Farplane harness changes with unresolved
  ownership or proposed new/moved durable harness surfaces.
- Ordinary, tiny, and already-reviewed-placement plans explicitly skip the
  advisor.
- Placement output stays in existing ticket Notes or subtractive receipt; no
  new field, sidecar, or canonical artifact is introduced.
- Harness Advisor remains placement owner, `impl-plan` remains plan owner, and
  the reviewer independently attempts a better placement and smaller plan.
- Goal Advisor remains unchanged and is used only for bounded continuation over
  the same ticket.
- The revised companion and planning validation pass.

## Rubric TAS

| Rubric | TAS | Finding |
|---|---:|---|
| spec-contract | TAS-A | One coherent coding-plan ticket with conditional placement reuse. |
| implementation-plan | TAS-A | Trigger, skip path, counter-placement, proof cases, and stop/block loop are concrete. |
| architecture | TAS-A | Placement, planning, review, and continuation responsibilities remain separate. |
| skill-contract | TAS-A | Existing Harness Advisor is composed without implementation changes. |
| integration-readiness | TAS-A | No new runtime, schema, field, sidecar, or canonical artifact. |
| prompt-quality | TAS-A | Planned prompt/checklist changes use a narrow predicate and explicit skip behavior. |
| evidence-quality | TAS-A | Triggered and skipped hardcases can falsify over-broad routing. |

No smaller valid plan was found. Final verdict: `pass / TAS-A`.
