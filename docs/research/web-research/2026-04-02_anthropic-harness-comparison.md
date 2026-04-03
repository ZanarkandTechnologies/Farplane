# Research: Codexter Harness vs Anthropic's Long-Running Harness

Date: 2026-04-02

## Scope

Study the current `Codexter` harness, note how it works today, and compare it against Anthropic's March 24, 2026 article, "Harness design for long-running application development."

Note on workflow request:
- The requested `brainstorm` skill is not installed in this environment.
- I used direct repo analysis plus web research instead.
- One useful finding is that the harness already references "brainstorm/interview" behavior in `agents/planner-agent.toml`, but that workflow is not actually installed as a concrete skill.

## Executive Summary

Codexter already has many of the right primitives:
- artifact-driven planning
- a filesystem ticket board
- specialized agents and skills
- memory/history/troubles logs
- QA and visual-QA separation
- explicit testability requirements for UI work

What it does **not** yet have is Anthropic's main harness advantage: an integrated, autonomous, long-running **planner -> builder/generator -> evaluator** loop with explicit handoff artifacts, retry/fail thresholds, and a clear context-management strategy.

The current state of Codexter is best described as:

> a strong autonomous engineering protocol and reusable Codex home repo
> more than a fully wired long-running application-build harness

That means the opportunity is not "invent autonomy from scratch." The opportunity is to connect the existing pieces into a more explicit run loop.

## What Codexter Is Today

### 1. Portable Codex home harness

The repo is designed as a reusable, Git-backed `~/.codex` home:
- tracks `agents/`, `skills/`, `rules/`, `bin/`, repo docs, and ticket board
- excludes secrets, auth, session state, logs, sqlite state, and machine-local `config.toml`
- installs via symlink/bootstrap flow using `install.sh`

Evidence:
- `README.md`
- `PROJECT_RULES.md`
- `install.sh`
- `config.toml.example`
- `docs/MEMORY.md` (`MEM-0001`)

### 2. Governance-first autonomous workflow

The root `AGENTS.md` defines a strong operating contract:
- mandatory DoD
- planning/build modes
- memory and troubles logging
- delegation rules
- ticket state machine
- code standards
- module scaffolding rules

This is stronger than a bare prompt harness. It encodes process, not just personalities.

Evidence:
- `AGENTS.md`

### 3. Filesystem board as the main coordination surface

Codexter uses board lanes:
- `tickets/todo/`
- `tickets/review/`
- `tickets/building/`
- `tickets/done/`

The ticket template is not just a task note. It carries:
- pitch
- before/after state
- delta
- proof
- plan review
- delegation
- acceptance criteria
- evidence checklist

This is close in spirit to Anthropic's file-based handoff model.

Evidence:
- `tickets/templates/ticket.md`
- `tickets/INDEX.md`
- `AGENTS.md`

### 4. Specialized workflow skill library

Codexter ships a substantial skill catalog. The important harness-related ones are:
- `prd`
- `spec-to-ticket`
- `tech-impl-plan`
- `runtime-debugging`
- `testing`
- `visual-qa`
- `code-review`
- `documentation`
- `codebase-analysis`

This means the harness already has specialization surfaces, even if they are not yet composed into one top-level long-running app-build loop.

Evidence:
- `skills/*`

### 5. Specialized agent catalog

The repo contains dedicated agents for:
- planning
- exploring
- documentation search
- memory lookup
- QA
- code review
- library/pattern research
- domain-specific implementation

This maps well to Anthropic's insight that different harness roles should handle different failure modes.

Evidence:
- `config.toml.example`
- `agents/*.toml`

### 6. Strong UI proof/testability doctrine

This is one of Codexter's strongest areas.

For UI-bearing tickets, `spec-to-ticket` requires:
- `Agent Contract`
- `Test hook`
- `Stabilize`
- `Inspect`
- `Key screens/states`
- `Taste refs`
- `Expected artifacts`
- `Evidence checklist`

Then `qa-tester` and `visual-qa` use those artifacts to verify the implementation.

This is very close to Anthropic's sprint-contract idea, and in some ways more explicit for UI work.

Evidence:
- `skills/spec-to-ticket/SKILL.md`
- `agents/qa-tester.toml`
- `skills/visual-qa/SKILL.md`

### 7. Durable memory surfaces

Codexter has three durable memory layers:
- `docs/HISTORY.md` for append-only change history
- `docs/MEMORY.md` for curated durable constraints
- `docs/TROUBLES.md` for repeated misses and operator corrections

This is valuable because long-running autonomy depends on retaining lessons beyond one run.

Evidence:
- `AGENTS.md`
- `docs/HISTORY.md`
- `docs/MEMORY.md`
- `docs/TROUBLES.md`

## How Codexter Works Today

At a high level, the intended loop appears to be:

1. Define or refine requirements in `docs/prd.md`
2. Convert a spec slice into executable tickets
3. Move tickets through `review -> building -> done`
4. Implement against acceptance criteria and proof requirements
5. Run QA / visual QA / code review where appropriate
6. Update history/memory/troubles docs

For UI work, the intended loop is even more concrete:

1. planning writes a ticket with an `Agent Contract`
2. implementation follows the contract
3. `qa-tester` captures evidence
4. `visual-qa` judges screen quality
5. ticket is updated with proof and verdict

This is disciplined and auditable. It is already much better than "tell the model to keep going."

## The Most Important Current Gaps Inside Codexter

These are not theoretical. They show up directly in the repo.

### Gap 1: The harness primitives exist, but the top-level autonomous loop is not fully wired

There is no single explicit "run an app from short prompt through planner, builder, evaluator rounds" surface in this repo.

What exists:
- planning skills
- tickets
- QA roles
- memory
- specialized agents

What is missing:
- an integrated orchestrator contract that binds them into a long-running build loop

### Gap 2: Prompt expectations and actual repo artifacts are out of sync

Several agent prompts assume:
- `docs/progress.md`
- `docs/research/*`

But the repo currently ships:
- no `docs/progress.md`
- no `docs/research/` tree by default

This matters because it means the intended research/handoff architecture is only partially realized.

Examples:
- `agents/planner-agent.toml` requires `docs/progress.md`
- `agents/explore.toml` requires `docs/research/explorer/`
- `agents/documentation-searcher.toml` writes to `docs/research/remote-documentation/`
- `agents/deep-researcher.toml` writes to `docs/research/web-research/`
- `agents/documentation-maintainer.toml` assumes `docs/progress.md` rotation rules

### Gap 3: The requested brainstorm stage exists conceptually, but not as an installed workflow

`agents/planner-agent.toml` explicitly says:
- start with brainstorm/interview first

But there is no installed `brainstorm` skill in `skills/`.

That is a useful signal:
- the harness already wants a discovery-first mode
- the discovery layer is incomplete as a concrete reusable workflow

### Gap 4: Evaluator separation exists, but not as one unified scoring model

Anthropic's harness uses an evaluator with explicit criteria and hard thresholds.

Codexter has:
- `qa-tester`
- `visual-qa`
- `code-review`

This is strong role separation, but the evaluation surface is split across multiple tools and lacks a single normalized scorecard such as:
- product depth
- functionality
- visual quality
- code quality
- pass/fail thresholds by round

### Gap 5: No explicit long-context strategy

Anthropic makes context strategy a first-class harness concern:
- context resets in older harness
- compaction in newer harness
- structured handoffs between sessions

Codexter currently has durable artifacts, but not a clear written policy for:
- when to reset context
- when to compact
- what must be written before a reset
- how a resumed agent knows exact next actions

### Gap 6: No formal run metrics / harness experiment loop

Anthropic tracks:
- harness duration
- cost
- round structure
- where the evaluator added value

Codexter currently has process docs but no obvious standard for:
- per-run metrics
- defect counts
- number of evaluator rounds
- pass/fail by criterion
- cost/time by phase
- "which harness parts are still load-bearing?"

## Anthropic's New Harness: Key Ideas

Based on the March 24, 2026 post, the important ideas are:

### 1. The failure modes are structural, not just prompt-quality problems

Anthropic identifies two major failure modes:
- long-task coherence degrades as context fills
- models are too lenient when evaluating their own work

This is important because it argues for harness structure, not just longer prompts.

Source:
- Anthropic article, lines 27-35

### 2. Separate the doer from the judge

Anthropic's central move is separating:
- generator/builder
- evaluator

The evaluator is intentionally tuned to be more skeptical than the builder. This gives the system an external feedback loop instead of self-congratulating on weak output.

Source:
- Anthropic article, lines 31-35, 58-70, 121-123

### 3. Planner -> generator -> evaluator is the core loop

Their newer application harness uses:
- planner
- generator
- evaluator

The planner expands a short prompt into a richer spec.
The generator builds.
The evaluator tests and grades.

Source:
- Anthropic article, lines 62-70

### 4. File-based contracts are the handoff surface

Agents communicate through files. This makes:
- context handoffs durable
- sessions restartable
- responsibilities explicit

Source:
- Anthropic article, line 70

### 5. Contracts define "done" before coding starts

Before each sprint in the earlier version, the generator and evaluator negotiated a sprint contract that defined:
- what would be built
- how success would be verified

This is one of the most relevant ideas for Codexter because it maps directly onto ticket and testability design.

Source:
- Anthropic article, lines 68-70, 95-97, 115-121

### 6. Evaluator quality depends on criteria and thresholding

The evaluator does not just "look around." It grades against explicit criteria and can fail a round if thresholds are not met.

Source:
- Anthropic article, lines 40-48, 66-67, 115-123, 159-169

### 7. Harnesses should simplify when models improve

Anthropic explicitly removed scaffolding when newer models made it unnecessary:
- earlier harness: stronger chunking and context-reset structure
- later harness: dropped sprint construct, kept planner and evaluator

Their principle is not "more harness is always better."
It is:

> keep only the load-bearing scaffolding

Source:
- Anthropic article, lines 125-137, 177-180

## Comparison Matrix

| Area | Codexter today | Compared to Anthropic |
| --- | --- | --- |
| Portable harness repo | Strong | Different goal, but a solid foundation |
| Planning/spec discipline | Strong | Aligned |
| Small-slice execution | Strong | Aligned with sprint decomposition mindset |
| File-based artifacts | Strong | Strongly aligned |
| UI testability contracts | Very strong | Equivalent or stronger for UI tickets |
| QA / visual evaluation separation | Strong | Aligned in spirit |
| Unified planner -> builder -> evaluator runtime | Weak/implicit | Missing |
| Generator role | Weak/implicit | Missing as a named, explicit harness persona |
| Evaluator rubric with hard thresholds | Partial | Missing unified scorecard |
| Context reset/compaction policy | Weak | Missing |
| Run-level handoff artifact schema | Partial | Missing |
| Metrics/cost/round observability | Weak | Missing |
| Start from 1-line prompt and auto-spec | Weak | Missing |
| Harness simplification audit loop | Weak | Missing |
| Brainstorm/discovery stage | Intended but not installed | Missing concrete workflow |

## What Codexter Already Does Better Than Anthropic's Described Harness

There are at least three areas where Codexter is already notably strong:

### 1. UI QA testability is better specified

Anthropic describes sprint contracts and Playwright-driven QA, but Codexter goes deeper on agent testability:
- test hooks
- stabilize hooks
- inspect surfaces
- key states
- evidence checklists

That is excellent harness design and should be preserved.

### 2. Durable operational memory is more explicit

Anthropic's article emphasizes handoff files, but Codexter already has:
- curated memory
- history
- troubles/pattern logging

That gives Codexter a more durable institutional memory layer than many harnesses.

### 3. Repo governance is much clearer

Codexter's root `AGENTS.md` is stronger on:
- DoD
- board movement
- coding standards
- documentation duties
- delegation rules

Anthropic's article is stronger on experimental architecture; Codexter is stronger on engineering governance.

## What Anthropic's Harness Adds That Codexter Still Needs

### 1. A true autonomous runtime loop

Codexter needs a first-class surface that can do:

1. take a short prompt
2. produce/refresh a spec
3. derive the next executable contract
4. build
5. evaluate
6. fail or pass the round
7. loop until thresholds are met or budget is exhausted

Right now, Codexter has the pieces but not the single loop.

### 2. Builder/generator as a first-class role

The harness has planners, explorers, QA, research, and review roles.
It does not yet expose a clear "this agent owns implementation rounds for autonomous app building" role in the way Anthropic does with the generator.

### 3. Evaluator thresholding

Codexter should move from "run QA/review" to:
- explicit criteria
- explicit minimum score / pass conditions
- explicit fail reasons
- round-by-round deltas

### 4. Context and recovery policy

Codexter should explicitly decide:
- when to keep one long-running session
- when to compact
- when to hard reset and resume from handoff artifacts

That policy should be model-aware and budget-aware.

### 5. Harness observability

Codexter should make it easy to answer:
- how many rounds did this run take?
- what failed each round?
- what did QA catch that the builder missed?
- what was the cost/time tradeoff?
- which harness components actually mattered?

## Recommended Improvements

## Priority 1: Turn Codexter into an explicit planner -> builder -> evaluator harness

Add a dedicated autonomous app-build workflow, likely as either:
- a new skill, or
- a runbook plus dedicated orchestrator agent prompt

Suggested run shape:

1. **Brainstorm / discovery**
   - turn short prompt into clarified product intent
   - this can become the missing `brainstorm` skill

2. **Planner**
   - generate a high-level product spec
   - avoid over-specifying low-level implementation

3. **Contract phase**
   - builder proposes the next slice
   - evaluator reviews the slice and proof criteria
   - contract becomes the build target

4. **Build phase**
   - builder implements the agreed slice

5. **Evaluation phase**
   - QA + visual QA + code quality checks
   - score against a normalized rubric

6. **Loop control**
   - if below threshold, generate next-round feedback and retry
   - if above threshold, advance or close

## Priority 2: Standardize run artifacts

Codexter already likes files as contracts. Lean into that.

Suggested structure:

```text
docs/runs/<RUN_ID>/
  prompt.md
  spec.md
  run-state.json
  round-01/
    contract.md
    builder-report.md
    evaluator-report.md
    metrics.json
    handoff.md
  round-02/
    ...
  final-summary.md
```

This would make long runs:
- resumable
- auditable
- benchmarkable

## Priority 3: Create the missing brainstorm skill

This would close two gaps at once:
- the user's requested workflow
- the planner prompt's missing dependency

The brainstorm skill should own:
- short-prompt expansion
- product clarification
- non-goals
- constraints
- success criteria
- likely feature slices
- optional "should this include an embedded agent/tool surface?" heuristic

## Priority 4: Add a unified evaluator rubric

Suggested dimensions:
- product depth
- functionality
- visual quality
- code quality
- testability

Suggested policy:
- any criterion below threshold fails the round
- evaluator must emit actionable defects, not just a verdict

Codexter already has the ingredients:
- `qa-tester`
- `visual-qa`
- `code-review`

The missing part is normalization.

## Priority 5: Decide and document context strategy

Add a written policy for:
- continuous-session mode
- compact-and-continue mode
- reset-and-resume mode

The choice should depend on:
- model capability
- task duration
- context growth
- quality drift
- restart cost

This is one of the clearest missing pieces compared with Anthropic's article.

## Priority 6: Fix artifact drift between prompts and repo reality

Either:
- create and adopt `docs/progress.md` + `docs/research/*` as real first-class artifacts

or:
- rewrite the agent prompts to align with the ticket-board-first workflow already in the repo

Right now, there are two different implied operating systems:
- filesystem board in `tickets/`
- progress/research doc system in agent prompts

Those should be unified.

## Priority 7: Add harness metrics and simplification discipline

Anthropic's post is valuable partly because it shows disciplined simplification.

Codexter should log for each long-running app-build run:
- prompt
- model
- round count
- duration
- cost
- bugs found by evaluator
- final pass/fail
- which harness components were used

Then review:
- which parts still add lift
- which parts are stale overhead

## Suggested Implementation Roadmap

### Phase 1: Alignment and plumbing

- add `docs/research/` as a real tracked structure
- add `docs/progress.md` or remove prompt assumptions about it
- create `brainstorm` skill
- define a normalized evaluator rubric

### Phase 2: First autonomous run loop

- add an orchestrator skill/prompt for planner -> builder -> evaluator
- store per-round contracts and reports under `docs/runs/`
- make pass/fail thresholds explicit

### Phase 3: Context and metrics

- implement reset vs compaction policy
- add run metrics
- benchmark a few canonical prompts
- measure which harness pieces are load-bearing

### Phase 4: Adaptive harness behavior

- skip evaluator for tasks below a complexity threshold
- increase evaluation strictness for UI-heavy or edge-of-capability tasks
- choose decomposition depth by model/task difficulty

## Concrete Design Direction for Codexter

If the goal is "make Codexter more autonomous," the cleanest direction is:

### Keep

- ticket board
- PRD/spec discipline
- memory/history/troubles
- UI testability doctrine
- QA/visual-QA separation
- strong repo governance

### Add

- brainstorm skill
- explicit builder/generator role
- run artifact schema
- unified evaluator rubric
- context-management policy
- metrics / benchmark loop

### Simplify

- remove duplicated assumptions between prompts and repo docs
- reduce ambiguity between `docs/progress.md` and ticket-board ownership
- avoid adding more agent personas before the orchestration loop exists

## Bottom Line

Codexter is already a serious harness, but it is currently optimized more for:
- disciplined autonomous engineering inside a Codex home

than for:
- fully autonomous long-running application generation from a short prompt

Anthropic's article suggests the next step clearly:

> Codexter should stop being only a library of good autonomous parts and become a more explicit runtime system that coordinates those parts.

The highest-value next moves are:
- install the missing brainstorm/discovery layer
- formalize planner -> builder -> evaluator rounds
- standardize handoff/run artifacts
- add evaluator thresholds and context policy

## Sources

External:
- Anthropic, "Harness design for long-running application development," published March 24, 2026
  - https://www.anthropic.com/engineering/harness-design-long-running-apps

Local repo sources reviewed:
- `README.md`
- `PROJECT_RULES.md`
- `AGENTS.md`
- `install.sh`
- `config.toml.example`
- `docs/prd.md`
- `docs/MEMORY.md`
- `docs/HISTORY.md`
- `docs/TROUBLES.md`
- `docs/TASTE.md`
- `tickets/templates/ticket.md`
- `tickets/INDEX.md`
- `skills/tech-impl-plan/SKILL.md`
- `skills/spec-to-ticket/SKILL.md`
- `skills/prd/SKILL.md`
- `skills/runtime-debugging/SKILL.md`
- `skills/visual-qa/SKILL.md`
- `agents/planner-agent.toml`
- `agents/explore.toml`
- `agents/documentation-searcher.toml`
- `agents/qa-tester.toml`
- `agents/memory.toml`
