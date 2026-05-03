---
name: demo-realism
description: Use when an MVP, prototype, or client demo feels fake and needs believable operational workflows, realistic demo data, and a presentation-worthiness rubric before design or implementation begins.
---

# Demo Realism

Use this before design/build when the missing problem is not "what screens exist"
but "what would make this feel believable to a client in an operational business
context?"

## Job

1. Infer a plausible client operating model from the industry, user, and adjacent tools.
2. Choose the pitch-worthy MVP slice that best shows the future-state value.
3. Decompose that slice from app -> workflow -> screen/state.
4. Derive realistic entities, records, timelines, edge cases, and empty/error states.
5. Produce a demo-realism pack the next skill can build from.
6. Score the result with a realism and presentation-worthiness rubric.
7. Hand off to `functional-ui`, `visual-design`, `frontend-craft`, `impl-plan`, or `impl`.

## Use When

- the app or prototype feels fake even if the UI is polished
- the demo data is generic and does not reflect believable day-to-day operations
- you need realistic examples before final design/build
- the user wants to pitch the potential of the product, not reconstruct the client's exact current tooling
- the workflow should feel like something the client could plausibly already be doing or want to do soon

## Do Not Use When

- the workflow is already believable and only visual execution remains
- the task is exact customer research or factual discovery; use research/documentation paths
- the task is final UI implementation; use `frontend-craft`
- the task is visual taste/system direction; use `visual-design`
- the task is already narrowed to interaction structure only; use `functional-ui`
- the task is final quality judgment after implementation; use `review`

## First-Load Checklist

Ensure an agent can execute the core path after only reading this file.

- Trigger conditions:
  - MVP/demo feels fake or too generic
  - product needs believable operational examples and demo data
  - the user wants a pitch-worthy future-state slice before build
- Workflow:
  1. identify the client type, operator, and operating context
  2. infer a plausible day-in-the-life model and adjacent tooling baseline
  3. choose the strongest demo-worthy MVP slice
  4. break it into workflows, screens/states, and data needs
  5. write the demo-realism pack
  6. score it with the realism rubric
  7. hand off to the next build/design skill
- Core decision branches:
  - missing operating reality -> stay on operating model inference
  - workflow believable but data weak -> stay on entities/records/timelines
  - realism pack strong enough -> hand off before final design/build
- Top 3 gotchas:
  - do not stop at generic mock data labels
  - do not claim exact client truth; this is pitch-potential synthesis
  - do not own final UI/design or implementation here
- Outcome contract:
  - one demo-realism pack exists in the current response, ticket, or spec artifact
  - the pack contains operating hypothesis, MVP slice, workflow ladder, screen/state ladder, demo-data pack, and realism rubric

## Output Contract

Produce one compact realism pack with:

- `Client operating hypothesis`
- `Pitch-worthy MVP slice`
- `Workflow ladder`
- `Screen/state ladder`
- `Demo-data pack`
- `Realism rubric`
- `Assumption ledger`
- `Recommended handoff`

## Workflow

1. Capture the client type, operator, and business context.
2. Infer the likely day-to-day operating loop and adjacent tools.
3. Name the highest-value MVP slice for a believable demo.
4. Decompose that slice:
   - app/story level
   - workflow/feature level
   - screen/state level
5. Derive the data pack:
   - core entities
   - realistic records
   - timelines and statuses
   - edge cases and failure states
6. Score the result using the realism rubric in [`references/rubric.md`](references/rubric.md).
7. Hand off:
   - `functional-ui` if workflow shape still needs product/UI planning
   - `visual-design` if realism is settled and visual direction should start
   - `frontend-craft` if realism is settled and implementation should start
   - `impl-plan` if the realism pack should become a scoped execution plan
   - `impl` if a ticket already exists and build can start directly

## Decision Branches

- **Branch A: context is thin**
  - infer aggressively from industry norms and adjacent tools
  - optimize for believable pitch potential rather than exact client truth
- **Branch B: context is rich**
  - preserve user-provided operator details and only fill the obvious gaps
- **Branch C: product shape is still too abstract**
  - stay at app/workflow decomposition until the demo slice is concrete
- **Branch D: product shape is believable but data still feels fake**
  - stay on the demo-data pack and realism rubric before handing off

## Guardrails

- infer aggressively, but do not pretend the result is verified client truth
- optimize for believable operational plausibility, not perfect factual reconstruction
- keep the pack concrete enough that downstream skills can build from it immediately
- do not let the output collapse into generic lorem-ipsum data
- do not stop at screens; tie every screen back to a workflow and operator need
- hand off before final UI/design/build execution

## Documentation Index

- Core rationale: [`references/architecture.md`](references/architecture.md)
- Detailed workflow: [`references/workflows.md`](references/workflows.md)
- Failure modes: [`references/gotchas.md`](references/gotchas.md)
- Scoring rubric: [`references/rubric.md`](references/rubric.md)
