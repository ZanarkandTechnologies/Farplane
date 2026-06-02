# Spec-To-Ticket Review

Run this review before handing off the ticket set.
If any answer is weak, tighten the tickets first.

## Must Pass

- Is each ticket one coherent self-contained feature-sized build loop rather than an architectural layer slice?
- If one feature was split, is the split justified by a real trigger instead of habit or neatness?
- Is overflow scope split into follow-up tickets instead of hidden in prose?
- Are dependencies explicit and ordered cleanly?
- If a ticket uses a library, package, service, or tool, is that dependency named where relevant?
- Do acceptance criteria explain the minimum necessary change clearly?
- Does each material ticket include a `Proof Contract` that separates metrics,
  caller-declared rubric families, required TAS gates, reviewer handoff fields,
  and required evidence?
- If no honest metric exists, does the ticket say `Metrics: none mechanical`
  instead of inventing a proxy?
- For UI-bearing tickets, do `Agent Contract` and `Evidence checklist` make QA realistic?
- Does each non-trivial ticket declare a usable `Test hook`, not just vague “verify manually” language?
- If bootstrap testability defaults exist, did we actually carry them into the
  first UI-bearing or agentically hard ticket instead of making the operator
  restate them?
- If delegation is expected, does `Delegate with` point to the exact ticket path/section and write-back target?
- For UI-bearing tickets, is the intended layout or screen structure clear enough to review later without guessing?

## Ask If Relevant

- Are we trying to do too much in one ticket, or are we over-splitting one coherent feature?
- Did we include the minimum amount of code or interface detail needed to explain the change?
- Are the tickets convincing enough for approval without becoming bloated?
- Are we saying too much, or too little, for an agent to execute reliably?
- Did we call out any instrumentation work needed for difficult UI or runtime verification?
- Are we defining proof in the cheapest deterministic way, for example a CLI check, seed path, debug route, or sanity script?
- If an `Agent Testability Brief` exists, did we actually preserve its surfaces in the ticket contract instead of re-deriving them inconsistently?
- If the repo has `qa/cookbook/`, did we seed or update the matching workflow
  entry for the slice instead of leaving QA to rediscover the flow from the
  ticket alone?
- For UI work, is the design intent readable for a human reviewer rather than only executable by an agent?
- Are we reusing existing shared UI patterns/libraries where possible instead of silently inventing another one?
- Did we keep backend and frontend together when they are part of one human-testable capability?
- If a split happened, was it because of shared platform work, migration/backfill, external dependency, or unresolved feasibility?
- For a complex system, does the first ticket create a reusable proof surface plus one minimal happy path instead of empty scaffolding?
- Are CRUD-style workflows still whole unless a real hard trigger forced a split?
- If a service split happened, is it a real ownership/runtime boundary instead of planning neatness?
- Are follow-up tickets grouped by shared proof surface or adjacent operator value instead of one internal stage each?

## Fail If

- one ticket clearly hides multiple build loops
- one coherent feature was split only into schema/backend/UI/integration layers
- dependency order is implied instead of stated
- a UI ticket says "verify in browser" without access/stabilization details
- a non-trivial ticket needs deterministic setup but has no usable `Test hook`
- acceptance criteria are generic, fluffy, or not observable
- a material ticket omits the `Proof Contract`
- a ticket invents subjective metrics instead of using rubric/evidence gates
- important dependencies or packages are assumed but never named
- delegated work is described only in prose without an exact ticket reference
- a split claims to be necessary but no real hard trigger is named
- an `Agent Testability Brief` exists, but the resulting ticket never turns it into concrete `Test hook`, `Stabilize`, `Inspect`, or proof expectations
- bootstrap `Agent Experience / Testability` defaults exist, but the first
  UI-bearing or agentically hard ticket ignores them
- the repo has `qa/cookbook/`, but the planning output never seeds a matching
  workflow entry for the ticket's proof path
- a complex pipeline is split into parse/chunk/embed/index-style microtickets without a true boundary trigger
- the first ticket ships only scaffolding and no usable proof path
- a CRUD workflow is split into multiple tickets without a real blocker or shared-platform reason
