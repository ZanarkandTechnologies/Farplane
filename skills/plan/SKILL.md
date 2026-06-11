---
name: plan
version: 0.2.0
description: "Turn a goal, context, invoked skills, and budget into composed todos, proof targets, and handoff when planning can reduce wasted work."
tier: 2
source: local
skill_template_version: "0.2.0"
allowed-tools: Read, Glob, Grep
---

# Plan

## Context

`plan` is a Tier 2 planning prompt-template function. It is not the universal
Tier 0 planning phase itself. Use it when the next phase would waste time
without a better task-specific todo list, grounding budget, composition order,
proof target, or handoff shape.

Most skills already contain reusable workflow taste in their todo lists. `plan`
binds the current task into those todos, composes multiple skill workflows when
needed, and decides how much grounding, advice, prototyping, review, or
delegated search is worth paying for.

## Skill Signature

```text
plan(task, context?, active_skills?, phase?, budget?) -> plan_packet + composed_todos + proof_target + handoff + review_request?
state: reads(task request, relevant files/docs, active skill todo lists, constraints, prior evidence); writes(plan artifact?)
gates: grounding_budget_explicit; skill_todos_composed; proof_before_execution; handoff_owner_named
routes: reference-grounding | research:* | advise | deliberative-advice | prototyping | review | domain skill
fails: strategy prose only; unbounded search; duplicated todos; hidden skill composition; proof invented after execution
```

Budget parameters should be explicit when the work is material:

```text
PlanBudget = {
  grounding: "none" | "skim" | "targeted" | "deep",
  search: "direct" | "limited" | "broad",
  compute: "single-agent" | "parallel-subagents" | "council",
  time: "tiny" | "normal" | "extended",
  review_request?: PlanReviewRequest,
  max_phase_depth?: 0 | 1 | 2
}

PlanReviewRequest = {
  needed: true | false,
  depth: "none" | "self-check" | "review-protocol" | "council",
  loops: 0 | 1 | 2 | "until-blocked",
  stop_condition: "no-material-findings" | "proof-defined" | "user-approved" | "budget-spent",
  rubric: "implementation-plan" | "skill-contract" | "evidence-quality" | "custom",
  child_scope: "smaller" | "specialized"
}
```

Subagents are a planning parameter, not a default. Use them only when the
runtime supports delegation, the user permits it, and independent search or
perspective lanes are worth the added coordination cost.

## Phase Contract

```text
planning_phase(task, context, budget)
  -> grounded_context
   + selected_workflows
   + composed_todos
   + strategy_decisions
   + proof_target
   + handoff
```

Use Codex native planning behavior for tiny or obvious tasks. Invoke this skill
when the plan itself needs a reusable prompt template, skill-todo composition,
or budgeted strategy choice.

## Phase Boundary

`plan` owns decomposition, todo composition, proof targets, handoff shape, and
optional review requests for plan artifacts. It does not own review judgment.
When a plan needs review, emit a `PlanReviewRequest`; the `review` skill or
reviewer actor owns the verdict.

`plan` may call another phase-like skill only when that call shrinks or
specializes the current planning scope. Do not plan a same-scope review of a
same-scope plan.

<!-- BEGIN FARPLANE_IMPORTANT_CHECKLIST -->
## Todo List

- [ ] 1. Bind the planning inputs.
   - [ ] Identify task, phase, expected artifact, constraints, active skills,
     available context, and `PlanBudget`.
   - [ ] Set `PlanReviewRequest` explicitly for material plans: usually
     `needed: false` for tiny work, `self-check` for normal material work, and
     `review-protocol` or `council` only when review cost is lower than
     execution risk.
   - [ ] Set `max_phase_depth`; default to `0` for inline phases, `1` for one
     externalized phase, and `2` only when the child scope clearly shrinks.
   - [ ] If the required context is missing, resolve it from local state or ask
     one narrow blocking question.
- [ ] 2. Choose the planning mode.
   - [ ] `direct_binding`: one skill todo list already fits the task.
   - [ ] `composition_plan`: multiple skill todo lists must be merged.
   - [ ] `advice_plan`: real options or tradeoffs must be compared.
   - [ ] `research_plan`: missing knowledge drives the risk.
   - [ ] `prototype_plan`: premature scale or broad change is the risk.
   - [ ] `review_plan`: the next phase is judgment over evidence.
- [ ] 3. Ground only what the plan needs.
   - [ ] Ground local state, current artifacts, and invoked skill contracts
     before external examples.
   - [ ] Use [reference-grounding](../reference-grounding/SKILL.md) for compact
     evidence checks.
   - [ ] Name the needed `research:*` method when a full parity, gap,
     official-docs, code-pattern, competitor, user-grounding, or
     source-synthesis pass is required.
- [ ] 4. Compose skill todos into task-specific todos.
   - [ ] Load only the active skill todo lists needed for this plan.
   - [ ] Select, merge, reorder, or skip todo items based on the task, budget,
     constraints, and proof target.
   - [ ] Remove duplicated or conflicting steps and explain material omissions.
- [ ] 5. Choose strategy only where strategy is actually needed.
   - [ ] Use [advise](../advise/SKILL.md) when there are real options to compare.
   - [ ] Use `deliberative-advice` or parallel subagents only when stakes,
     ambiguity, search breadth, or operator cost justifies the budget.
   - [ ] Use [prototyping](../prototyping/SKILL.md) when the main risk is scale,
     automation breadth, data volume, or blast radius.
- [ ] 6. Define proof before execution starts.
   - [ ] Name the verification command, evidence artifact, review gate, or
     explicit proof gap.
   - [ ] Set a stop condition so planning does not become open-ended search.
- [ ] 7. Return a plan packet that a human can scan and an agent can execute.
   - [ ] Include goal, grounding used, planning mode, selected workflows,
     composed todos, decision points, proof target, handoff owner, and skipped
     work.
- [ ] 8. Apply the configured review loop.
   - [ ] Skip review when `PlanReviewRequest.needed` is `false` or
     `PlanReviewRequest.depth` is `none`.
   - [ ] Use self-check for normal material plans.
   - [ ] Use the [review protocol](../review/SKILL.md) or `deliberative-advice`
     only for high-blast-radius, delegated, strategic, or disagreement-heavy
     plans.
   - [ ] Do not call review at the same scope if `max_phase_depth` is already
     spent or the review would not shrink or specialize the task.
   - [ ] Stop when the configured stop condition is met, findings repeat, or
     the next improvement requires execution evidence.
<!-- END FARPLANE_IMPORTANT_CHECKLIST -->

## Use When

- The user explicitly asks for `$plan` or a plan.
- Multiple skills, workflows, or todo lists need to be composed.
- A phase needs a better task-specific todo list before work begins.
- The next phase has expensive search, high ambiguity, broad blast radius, or
  unclear proof.
- The agent needs to choose grounding depth, search breadth, subagent/council
  budget, or review depth before acting.

## Do Not Use When

- A tiny reversible task can be done directly.
- A domain-specific planner owns the artifact, such as `impl-plan` for coding
  tickets, unless `plan` is being used to compose that planner with other
  workflows.
- The user wants pure option comparison with no executable plan; use `advise`.
- The task is still broad product discovery; use `brainstorm`, `deep-interview`,
  `prd`, or the relevant research method first.

## Planning Modes

### Direct Binding

Use when one skill already carries the right workflow.

```text
instantiate_todos(skill_todos, task_context) -> task_specific_todos
```

### Composition Plan

Use when several workflows apply and their todo lists must be merged.

```text
compose_todos(goal, skill_todos[], context, budget)
  -> selected_steps + order + skipped_steps + proof
```

### Advice Plan

Use when order, owner, scope, or strategy has real alternatives.

```text
advise(options, criteria) -> recommendation + tradeoff
plan(...) -> recommendation_bound_todos + proof
```

### Research Plan

Use when missing knowledge is the bottleneck.

```text
plan_research(question, known_context, uncertainty, budget)
  -> targets + source_strategy + stop_condition + synthesis_shape
```

### Prototype Plan

Use when scale is the risk.

```text
prototype_plan(goal, blast_radius, sample_unit)
  -> 1 -> 10 -> 100 path + guard + expansion_condition
```

### Review Plan

Use when the next phase is judgment over evidence.

```text
plan_review(claim, evidence, rubric_family, risk)
  -> review_focus + hard_gates + sampling_strategy + verdict_shape
```

### Review Loop

Use when a draft plan itself needs critique before execution.

```text
review_plan(draft_plan, review_budget)
  -> accept | revised_plan + findings + remaining_risk
```

Review loops should be bounded. A useful loss proxy is:

```text
plan_loss = ambiguity + missing_grounding + proof_gap + dependency_risk + user_misalignment + wasted_search_risk
```

Run another review loop only while expected loss reduction is greater than
review cost and the next loop shrinks or specializes the remaining scope.

## Good vs Bad Plans

Good plans are:

- grounded enough for the next decision
- bounded by budget and stop condition
- composed from actual skill contracts when skills are active
- ordered around dependency and risk
- proof-first
- easy for a human to skim and an agent to execute

Bad plans are:

- ungrounded confidence
- broad research without a stop condition
- strategy prose without executable todos
- copied skill checklists with no task binding
- duplicated or conflicting workflow steps
- proof deferred until after execution

## Output

Return a compact plan packet:

```markdown
Goal:
Planning Mode:
Budget:
Review Request:
Grounding:
Selected Workflows:
Composed Todos:
Decision Points:
Proof Target:
Handoff:
Skipped / Deferred:
```

When writing to a durable artifact, use the owning ticket, spec, skill audit,
or docs surface rather than inventing a separate plan file.

## Guardrails

- Do not make `plan` a mandatory dependency of every skill. Tier 0 already owns
  the universal phase expectation.
- Do not call `plan` only to paraphrase a skill's todo list. Add value by
  binding, composing, budgeting, or defining proof.
- Do not use external/world grounding by default. Start with local state and
  invoked skill contracts; add external grounding only when it can change the
  plan.
- Do not turn planning into hidden execution. Stop after the plan packet unless
  the user or workflow explicitly asks to continue.
- Do not use subagents, council, or broad research when a single-agent direct
  binding plan is enough.
- Do not run review loops by reflex. Use them when expected plan-loss reduction
  is greater than review cost, and stop on repeated findings or budget spent.
