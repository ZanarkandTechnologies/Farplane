# Harness Algebra

Status: draft contract

Date: 2026-06-09

## Purpose

Define harness engineering with math-like definitions, starting from the basic
model call and building up to context, skills, tools, memory, subagents,
verification, reward functions, and self-improvement.

The goal is to teach the harness as an optimization system:

> A prompt is not the product. The harness is the equation around the model.

## Response Notation Preference

Function signatures are also a response format, not only an internal spec
format. When an explanation introduces an important concept, standard, process,
skill, hook, eval, memory rule, or reusable abstraction, prefer a compact
signature that makes the input/output shape obvious.

```text
concept_name(inputs, optional_state?) -> outputs + evidence
```

Good signatures highlight:

- inputs consumed
- state or files read
- transformation applied
- outputs produced
- durable variables written
- evidence or reward signal used to judge success

Examples:

```text
artifact_first(result, owner?) -> file_ref + chat_summary

frontmatter(markdown_body, metadata) -> routable_markdown_file

skill(task, context, state) -> outputs + write_set + evidence

eval(candidate_output, rubric, fixtures) -> score + failure_modes
```

Do not force signatures into tiny status updates, purely emotional responses,
or cases where they would make the answer less clear. The purpose is intuition:
make the object manipulable by showing what flows in and what flows out.

## 1. Prompt Algebra

Start with the simplest model:

```text
Codex = f(input_prompt) -> reasoning -> text_output
```

A real interaction is multi-turn:

```text
Codex_N =
  f(input_prompt
    + text_output_1
    + ...
    + text_output_{N-1})
  -> text_output_N
```

Where:

- `N` is the turn number.
- Each turn changes the effective prompt by adding prior outputs, user
  responses, tool results, and accumulated context.
- The harness decides which variables enter the next prompt.

## 2. Prompt Size Is A Proxy, Not The Goal

A naive first approximation:

```text
prompt_size proportional_to (hallucination, cost_time_money)
```

This is useful intuition, but too simple.

Better:

```text
cost + latency ~= prompt_size + tool_calls + turns

hallucination ~= missing_context
               + noisy_context
               + contradictory_context
               + weak_verification
```

So the goal is not:

```text
min(prompt_size)
```

The goal is:

```text
minimize irrelevant_context
maximize useful_constraints
minimize turns + coordination_cost
subject to acceptable_output_quality
```

## 3. Context Definition

The model is better written as:

```text
Codex = M(context, task) -> output
```

Where:

```text
context =
  system_prompt
+ tool_descriptions
+ selected_skills
+ memory
+ conversation_history
+ task_input
```

And:

```text
input_prompt =
  system_prompt
+ mcp_tools_prompt
+ skills_prompt
+ user_prompt
```

With:

```text
skill = { skill_prompt, scripts, references, templates, evals? }
```

## 4. Harness Definition

A harness is the function that chooses the context and control loop around the
model:

```text
Harness H :=
  ContextBuilder
+ SkillSelector
+ ToolPolicy
+ MemoryPolicy
+ DelegationPolicy
+ VerificationPolicy
+ UpdatePolicy
+ BudgetPolicy
```

The harness turns a task and current state into model context:

```text
context_n = H_theta(task_n, state_n)
```

Then the model produces output:

```text
output_n = M(context_n, task_n)
```

Equivalently:

```text
y_n = M(H_theta(task_n, state_n), task_n)
```

Then the harness updates state:

```text
state_{n+1} = update(state_n, output_n, evidence_n)
```

And for the model-visible context:

```text
context_{n+1} = update(context_n, output_n, evidence_n)
```

So the full loop is:

```text
task_n -> H_theta(task_n, state_n) -> context_n
context_n + task_n -> M -> output_n
output_n + evidence_n -> update -> state_{n+1}
```

## 5. Harness Variables

The harness parameters are:

```text
theta =
  system_prompt
+ selected_skills
+ tool_set
+ memory_policy
+ subagent_topology
+ verification_tests
+ routing_policy
+ budget_limits
+ review_policy
+ update_policy
```

Equivalently:

```text
H_theta = {
  system_prompt,
  selected_skills,
  tool_set,
  memory_policy,
  subagent_topology,
  verification_tests,
  routing_policy,
  budget_limits
}
```

Harness engineering is choosing `theta`.

## 6. Skill Selection

Skill selection is a harness function:

```text
find_skills(task_x, skill_registry, state) -> selected_skills
```

A task run can be written as:

```text
task_x =
  (system_prompt + mcp_tools + user_prompt)
  -> find_skills(task_x)
  -> selected_skills
  -> N_turns
  -> output_x
```

The goal is not only to choose more skills. The goal is to choose the minimum
sufficient reusable skill context:

```text
goal -> min(skill_prompt_duplication)
goal -> max(reusable_behavior)
```

## 7. Turn Minimization

Turn count is a cost variable:

```text
goal -> min(N_turns)
```

But turn minimization is constrained:

```text
min(N_turns)
subject to:
  quality >= threshold
  verification_passes = true
  user_goal_satisfied = true
```

If reducing turns removes verification, the harness got faster but worse.

## 8. Delegation And Subagents

Delegation splits turn work across agents:

```text
N_turns -> subagent_a_turns + subagent_b_turns + ... + integration_turns
```

A subagent is:

```text
subagent = Codex(subagent_prompt, task_prompt)
```

More generally:

```text
subagent_i = M(context_i, task_i)
```

Where:

```text
context_i =
  subagent_prompt
+ task_prompt
+ selected_skills_i
+ tool_policy_i
+ evidence_requirements_i
```

The subagent optimization problem:

```text
goal -> min(subagent_prompt)
subject to:
  role_clarity >= threshold
  owned_output_defined = true
  integration_evidence_passes = true
```

Skills help because reusable skill variables prevent duplicating the same
instructions inside every subagent prompt.

## 9. CSP Versus Constrained Optimization

Pure CSP asks:

```text
Find assignments to variables such that all constraints are satisfied.
```

Harness engineering usually asks:

```text
Find the best harness configuration
minimizing cost / turns / context size / duplication
while satisfying quality / safety / reliability constraints.
```

So harness engineering is better described as constrained optimization:

```text
minimize:
  tokens
+ latency
+ turns
+ duplicated_instructions
+ failure_rate

subject to:
  quality >= threshold
  safety == acceptable
  tests == pass
  user_goal == satisfied
  cost <= budget
```

Compact thesis:

```text
Harness engineering =
  constrained optimization over context, tools, memory, skills,
  delegation, and verification.
```

## 10. Reward Function

For a task distribution `D`, define a harness score:

```text
S(H, D) =
  task_success
+ reliability
+ reusable_behavior
+ downstream_transfer
+ auditability
- token_cost
- latency
- turn_count
- duplicated_instruction
- failure_rate
- regression_rate
```

Weighted version:

```text
S(H, D) =
  w_success * TaskSuccess(H, D)
+ w_reliability * Reliability(H, D)
+ w_reuse * Reuse(H, D)
+ w_transfer * DownstreamTransfer(H, D)
+ w_audit * Auditability(H, D)
- w_token * TokenCost(H, D)
- w_latency * Latency(H, D)
- w_turns * Turns(H, D)
- w_dup * Duplication(H)
- w_fail * FailureRate(H, D)
- w_regress * RegressionRate(H, D)
```

In practice, Farplane should often use a Pareto frontier instead of one scalar:

```text
accept if:
  quality improves and cost does not increase
  OR cost decreases and quality does not regress
  OR downstream transfer improves with acceptable added cost
```

## 11. Task Distribution

Self-improvement needs a task distribution, not one anecdote:

```text
D = { task_i, expected_properties_i, constraints_i, eval_i }
```

Examples:

- coding tickets
- skill maintenance tasks
- review tasks
- eval-writing tasks
- research-to-ticket tasks
- correction recovery tasks

Without `D`, the agent optimizes for vibes or overfits a single example.

## 12. Harness Self-Improvement

Let:

```text
H_t = current_harness
Delta H_t = proposed_harness_change
S(H_t, D) = baseline_score
```

The loop:

```text
1. Define task distribution D
2. Define harness H
3. Define score function S(H, D)
4. Run baseline score
5. Agent proposes one change Delta H
6. Run evals again
7. Accept only if score improves and constraints still pass
8. Record lesson
9. Repeat
```

Update rule:

```text
H_{t+1} =
  H_t + Delta H_t  if Accept(Delta H_t)
  H_t              otherwise
```

Acceptance rule:

```text
Accept(Delta H) :=
  quality_improves
  AND cost <= budget
  AND prompt_size <= limit
  AND no_safety_regression
  AND no_test_regression
  AND heldout_score_does_not_regress
```

This is gradient-descent-like:

```text
loss(H) =
  bad_outputs
+ regressions
+ token_cost
+ latency
+ duplicated_instruction
+ drift
```

Then:

```text
H_{t+1} = H_t - alpha * estimated_gradient(loss)
```

But in Farplane the space is discrete. We do not usually have a real gradient.
So the practical optimizer is closer to coordinate descent or evolutionary
search:

```text
choose one coordinate:
  skill_prompt
  system_prompt
  tool_policy
  memory_policy
  eval_suite
  routing_rule
  subagent_prompt
  review_gate

change it
measure it
keep or revert
```

## 13. Failure Modes

Unconstrained optimization drifts:

```text
goal: improve reliability
agent action: add more instructions
result: prompt bloat, higher cost, more contradictions
```

```text
goal: reduce turns
agent action: skip verification
result: faster but less trustworthy
```

```text
goal: pass evals
agent action: overfit test cases
result: eval score improves, general behavior gets worse
```

```text
goal: make itself better
agent action: edit its own rules without stable benchmark
result: self-referential drift
```

The correction:

```text
Do not optimize "be better."
Optimize a bounded harness artifact against a fixed eval distribution.
```

## 14. Skills As Functions

Once the harness model is defined, each skill can be written as a function:

```text
skill_s(input, context, artifacts) -> output + evidence + write_set
```

For a Farplane skill:

```text
Skill_s :=
  skill_prompt
+ todo_list
+ references
+ scripts
+ templates
+ proof_contract
```

Function contract:

```text
skill_name: Inputs -> Outputs

Inputs:
  operator_intent
  required_context
  readable_artifacts
  optional_tools

Outputs:
  primary_response_or_artifact
  write_set
  evidence

Composition:
  upstream
  downstream
  transitive_effects
```

Do not add this section as decoration. Add it when it clarifies the variables
the skill consumes and produces.

## 15. Evals As Functions

An eval is a scoring function:

```text
Eval(candidate, task_distribution, judge) -> score + verdict + evidence
```

Or:

```text
E(H, D) -> S(H, D)
```

Good evals define:

- input candidate
- task cases
- expected properties
- judge or assertions
- score
- failure evidence
- heldout split

## 16. Files As Variables

The filesystem is the harness variable store:

```text
FileVariable :=
  path
+ semantic_name
+ owner
+ writer
+ readers
+ lifecycle
+ validation
```

Files are not just files. They are variables in the optimization system.

Examples:

- `README.md` is a public routing variable.
- `docs/specs/*.md` are durable contract variables.
- `docs/features/registry.jsonl` is a feature-state variable.
- `docs/skills/registry.jsonl` is a generated skill-inventory variable.
- `tickets/TASK-*/ticket.md` is a work-state variable.
- eval run JSON is reward/evidence state.

Weak harness behavior often comes from implicit variables: files that agents
write but later agents do not know to read, trust, update, drain, or delete.

## 17. Research Thesis

The core thesis:

```text
A self-improving agent harness is not an agent with a goal.
It is a constrained optimizer over its own context interface.
```

Without constraints, it drifts.

With evals, budgets, and rollback, it can learn better harness configurations.

Research framing:

```text
Agent harnesses are constrained self-optimizing systems.
```

## 18. Rollout

Use this spec as the canonical model. Then roll out function contracts in
samples:

1. `advise`
2. `reference-grounding`
3. `plan` or `execute`
4. `harness-advisor`
5. `skill-maintenance`
6. `eval`
7. one complex Tier 3 skill such as `landing-page` or `frontend-craft`

Do not bulk-edit every skill until the sample proves the notation improves
composition, eval design, or harness optimization.
