# Harness Algebra

Status: draft research spec

Date: 2026-06-09

## Abstract

Harness engineering is the problem of choosing and optimizing the variables
around an agent so it can complete a class of tasks reliably.

The central object is:

```text
H_theta(task, state) -> output + evidence + state_delta
```

Where `theta` is the harness configuration: system prompts, skills, subagents,
hooks, MCP tools, memory, filesystem variables, evals, automations, routing,
verification, and budgets.

The purpose of this document is not to describe how an LLM works internally.
The purpose is to define the harness variables well enough that
`harness-advisor` can recommend what to change and future evals can measure
whether the change improved the harness.

## 1. Optimization Problem

A harness turn is:

```text
context = GatherContext(task, state, theta)
controls = SelectControls(task, context, state, theta)
output = Execute(task, context, controls)
evidence = Verify(output, task, controls)
state_delta = Update(state, output, evidence)
```

Composed:

```text
H_theta(task, state) -> output + evidence + state_delta
```

Harness engineering is choosing `theta`:

```text
theta =
  system_prompt_policy
+ skill_policy
+ subagent_policy
+ hook_policy
+ mcp_policy
+ memory_policy
+ filesystem_policy
+ eval_policy
+ automation_policy
+ routing_policy
+ verification_policy
+ budget_policy
```

Optimization requires a task distribution:

```text
D = { task_i, expected_properties_i, constraints_i, eval_i }
```

Without `D`, an agent can overfit one anecdote and call it improvement.

## 2. Reward And Loss

The main research question is:

```text
Find the best harness configuration theta
that maximizes task success, reliability, reuse, and auditability
while minimizing cost, latency, turns, duplication, failures, and regressions.
```

Reward form:

```text
S(H_theta, D) =
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

Loss form:

```text
L(H_theta, D) =
  bad_outputs
+ regressions
+ token_cost
+ latency
+ turn_count
+ duplicated_instruction
+ noisy_context
+ missing_context
+ weak_verification
+ drift
```

Optimization target:

```text
maximize S(H_theta, D)
```

Or equivalently:

```text
minimize L(H_theta, D)
```

Subject to constraints:

```text
quality >= threshold
safety == acceptable
tests == pass
user_goal == satisfied
cost <= budget
prompt_size <= limit
operator_control_is_preserved = true
```

Prompt size is only one cost term:

```text
cost + latency ~= prompt_size + tool_calls + turns

error_risk ~= missing_context
           + noisy_context
           + contradictory_context
           + weak_verification
```

So the goal is not simply `min(prompt_size)`. The goal is:

```text
minimize irrelevant_context
maximize useful_constraints
minimize turns + coordination_cost
subject to acceptable_output_quality
```

## 3. Harness Feature Tree

Use a tree, not a flat list. Flat lists hide ownership and make placement
decisions harder.

```text
Harness H = {
  InterfaceLayer,
  CapabilityLayer,
  ControlLayer,
  StateLayer,
  VerificationLayer
}
```

### Interface Layer

```text
InterfaceLayer = {
  system_prompt,
  user_task,
  conversation_slice
}
```

`instructions` is not a separate component. Instructions are represented by
`system_prompt` and selected `skills`.

### Capability Layer

```text
CapabilityLayer = {
  skills,
  subagents,
  mcp_tools
}
```

### Control Layer

```text
ControlLayer = {
  hooks,
  automations,
  routing_policy,
  budget_policy
}
```

### State Layer

```text
StateLayer = {
  memory,
  filesystem,
  runtime_state,
  conversation_state
}
```

`memory` is the broad retrieval/state interface. It may include vector stores,
databases, ledgers, summaries, or other retrieval systems.

`filesystem` is a separate first-class state store because it is addressable,
searchable, reviewable, easy for humans and agents to update, and durable
across tasks.

### Verification Layer

```text
VerificationLayer = {
  evals,
  proof_contracts,
  review_skills,
  review_subagents,
  completion_gates
}
```

Review loops are not one primitive component. They are verification workflows
implemented through skills, subagents, proof contracts, hooks, and evals.

Quality levers should be routed by proof type:

```text
judgment-heavy quality claim -> review
repeatable behavioral claim -> eval
task-local evidence obligation -> proof_contract
deterministic structure/invariant -> validator
deterministic boundary event -> hook
self-review or context-drift risk -> reviewer subagent
final sufficiency claim -> completion gate
```

Ownership boundaries:

```text
harness-algebra = coordinates, loss terms, score model, proof routing
harness-engineering-doctrine = placement doctrine and surface tradeoffs
harness-advisor = first-load decision procedure and recommendation output
skills/review = TAS meanings, rubric families, and review hard gates
skills/eval = eval setup, task cases, judge prompts, and run artifacts
agents/reviewer.toml = reviewer execution identity
tickets = task-local proof contracts and durable evidence handles
hooks/validators = deterministic checks and boundary gates
```

This keeps the algebra spec useful to `harness-advisor` without making it a
second review, eval, or placement manual.

## 4. Feature Functions

Each harness feature should have an input/output shape. These definitions are
the useful part for `harness-advisor`.

```text
system_prompt(task, state) -> global_constraints
Skill(input, context, artifacts) -> output + evidence + write_set
Subagent(task, context, controls) -> output + evidence
Hook(event, state, artifacts) -> gate_decision + evidence
McpTool(args) -> observation_or_side_effect
Memory(task, state) -> retrieved_context
Filesystem(query, state) -> typed_file_variables
Eval(candidate, cases, judge) -> score + verdict + evidence
Automation(trigger, schedule, state) -> task | no_op
ProofContract(task, state) -> required_evidence
ReviewWorkflow(claim, evidence) -> pass | revise | block
```

The placement distinction:

```text
system_prompt = always-loaded global constraint
skill = reusable workflow guidance
subagent = isolated execution ownership
hook = deterministic boundary decision
mcp_tool = external capability
filesystem = durable typed state
eval = scoring function
automation = trigger that creates or resumes work
```

Optimization effect matrix:

```text
feature                  improves                         can hurt
system_prompt_policy      global consistency               prompt_size, contradiction risk
skill_policy              reuse, progressive disclosure     stale or wrong skill routing
subagent_policy           context isolation, parallelism    coordination cost
hook_policy               deterministic boundary control    false blocks or false passes
mcp_policy                capability, fresh observation     latency, side effects
memory_policy             context reuse                     stale or noisy retrieval
filesystem_policy         resumability, auditability        stale files, context clutter
eval_policy               measurable accept/reject          overfit, eval burden
automation_policy         recurring updates and drains      hidden autonomy, noisy work
verification_policy       trust, reliability                latency, review overhead
```

The advisor surface is therefore:

```text
improvement_request
  -> failing_reward_or_loss_term
  -> candidate_feature_coordinate
  -> proof_plan
  -> accept_or_reject
```

## 5. Meta Processes As Harness Update Functions

Meta processes change the harness itself. They are higher-order functions over
`theta`, not normal task execution.

```text
MetaProcess(request, state, theta) -> Delta theta + evidence
```

Important meta processes:

```text
HarnessAdvisor(improvement_request, state) -> target_variable
                                             + rationale
                                             + proof_plan

SkillCreator(capability_gap, context) -> Skill_s + registry_delta

SkillMaintenance(skill_graph, rule) -> skill_delta
                                     + registry_delta
                                     + validation_evidence

EvalWriter(claim, target_variable, cases) -> eval_suite
                                           + judge
                                           + baseline_result

MemoryDrain(source_files, promotion_rule) -> memory_delta
                                            + possible_theta_delta
```

These processes matter because they compound. A normal Tier 3 skill improves
one workflow. A meta skill improves the machinery that creates, maintains, or
evaluates many workflows.

Tier leverage:

```text
ROI(Tier1_delta) >= ROI(Tier2_delta) >= ROI(Tier3_delta)
```

This is not always true for one urgent task, but it is a useful default prior.
Tier 1 primitives compound because Tier 2 and Tier 3 skills call them. Tier 2
interfaces compound because many Tier 3 skills inherit their planning,
execution, research, or review shape. Tier 3 skills compound inside their
domain, but usually have narrower blast radius.

Practical examples:

```text
update(review) -> improves every workflow that uses review gates
update(advise) -> improves every placement or tradeoff decision using options
update(skill-creator) -> improves future skill quality
update(skill-maintenance) -> improves skill graph health and registry accuracy
write_eval(skill_policy) -> makes future skill extraction safer
write_eval(harness-advisor) -> makes placement recommendations measurable
```

The high-ROI rule for `harness-advisor`:

```text
If a failure repeats across many skills or workflows,
prefer a meta-skill, Tier 1, Tier 2, validator, or template update.

If a failure is local to one domain,
prefer the owning Tier 3 skill, ticket contract, or reference.
```

## 6. Goals As Functions

A goal is a harness objective compiled into a measurable task contract.

```text
Goal := Task + Metric + Review + Resolve
```

Goal-crafter turns fuzzy operator intent into:

```text
Goal(intent, context) -> desired_end_state
                       + evidence
                       + constraints
                       + iteration_policy
                       + blocked_stop
```

Goals optimize the harness by making the reward or loss explicit before work
starts:

```text
goal -> metric -> accept_condition -> update_rule
```

Examples:

```text
goal: improve skill reliability
metric: skill_eval_pass_rate
accept: pass_rate improves and prompt_size does not exceed limit

goal: reduce prompt bloat
metric: duplicated_instruction_count + context_tokens
accept: duplication decreases and task_success does not regress
```

## 7. Skills As Functions

A skill is a reusable function package:

```text
Skill = {
  SKILL.md,
  references?,
  scripts?,
  templates?,
  evals?
}
```

A skill is most useful when it has a function signature:

```text
Skill_s(input, context, artifacts) -> output + evidence + write_set
```

Minimum useful skill contract:

```text
Skill_s = {
  trigger_boundary,
  input_contract,
  output_contract,
  required_artifacts,
  allowed_state_reads,
  allowed_state_writes,
  proof_command_or_review_gate,
  registry_metadata
}
```

Skills optimize the harness by moving workflow detail out of always-loaded
system prompts and into progressive disclosure:

```text
system_prompt_size decreases
reusable_behavior increases
duplicated_instruction decreases
```

Skills compose when output contracts match input contracts:

```text
(Skill_b . Skill_a)(x) = Skill_b(Skill_a(x))
```

Skills are also the most practical way to represent decomposed harnesses. A
task-specific harness can often be written as:

```text
H_A =
  system_prompt_global
+ selected_skills_A
+ tools_A
+ memory_A
+ proof_A
```

If `selected_skills_A` carries most of the reusable behavior, then optimizing
the skill is the highest-leverage way to optimize `H_A`.

For harness engineering, the practical point is stronger than the algebra:
skills should name their inputs, outputs, files, proof, and side effects so
other skills and subagents can reuse them without guessing.

Model skills as stateful functions:

```text
Skill_s(input, state) -> output + evidence + state_delta
```

Avoid pretending every skill is pure. Skills read files, call tools, delegate,
and update state.

## 8. Subagents As Functions

A subagent is scoped execution with isolated context:

```text
run_subagent(task, config) -> output + evidence

config = {
  subagent_prompt,
  skills,
  mcp_tools,
  allowed_files,
  output_contract,
  evidence_contract
}
```

Subagents optimize the harness by reducing context drift and ownership blur:

```text
context_drift decreases
parallelism increases
owned_output_clarity increases
coordination_cost may increase
```

Subagents can equip skills:

```text
run_subagent(task, {
  subagent_prompt: reviewer_prompt,
  skills: [review],
  mcp_tools: [],
  output_contract: review_verdict
})
```

The clean pattern is for subagents to write reusable outputs to files:

```text
subagent(task) -> artifact_path + evidence_path
```

That keeps the result inspectable, reusable, and available to later harness
updates.

## 9. Hooks And Automations As Update Functions

Hooks are deterministic boundary functions:

```text
Hook(event, state, artifacts) -> gate_decision + evidence
```

Hooks optimize by reducing hidden judgment and catching boundary failures:

```text
false_completion decreases
missing_evidence decreases
operator_control increases
```

Automations are scheduled or event-triggered update functions:

```text
Automation(trigger, schedule, state) -> task | no_op
```

Memory drains are automation-style update functions:

```text
Drain(source_file, target_file, rule) -> target_delta + evidence
```

Examples:

```text
behavior_gap -> gap_analysis -> optimize_harness
hardcase_signal -> eval_task[hardcase=true]
trouble_signal -> docs/TROUBLES.md -> docs/LESSONS.md
docs/LESSONS.md -> docs/MEMORY.md
docs/MEMORY.md -> project AGENTS.md
source_observation -> docs/features/registry.jsonl
skill_eval_failure -> skill_update_ticket
```

More generally:

```text
UpdateHarness(memory_signal, theta) -> Delta theta | reject
```

This is how file variables become harness configuration changes.

## 10. Evals As Scoring Functions

Evals are scoring functions over harness candidates:

```text
Eval(candidate, cases, judge) -> score + verdict + evidence
```

Important eval types:

```text
SystemPromptEval(system_prompt, tasks) -> score
SkillEval(skill, tasks) -> score
WorkflowEval(workflow, tasks) -> score
HarnessAdvisorEval(placement_decision, cases) -> score
```

For many practical improvements, do not optimize the whole harness at once.
Decompose the task distribution, then decompose the harness.

If:

```text
D = A + B
```

Then a useful approximation is:

```text
H_D ~= H_A + H_B + Compose(H_A, H_B)
```

Where:

```text
H_A =
  system_prompt_global
+ selected_skills_A
+ tools_A
+ memory_A
+ proof_A

H_B =
  system_prompt_global
+ selected_skills_B
+ tools_B
+ memory_B
+ proof_B
```

So the score also decomposes:

```text
Score(H_theta, D) ~=
  Score(system_prompt_policy, D_global)
+ Sum_i route_weight_i * Score(skill_i, D_skill_i)
+ Score(composition, D_workflow)
```

Where:

```text
SkillEval(skill_i, D_skill_i) -> skill_score_i
```

And each skill task distribution is a smaller task family:

```text
D_skill_i = {
  task_cases_requiring_skill_i,
  expected_outputs_i,
  required_evidence_i,
  failure_modes_i
}
```

Mini-harnesses make the decomposition testable:

```text
MiniHarness = {
  id,
  owner,
  task_family,
  task_slice,
  selected_skills,
  tools,
  state_files,
  proof_contract,
  eval_cases,
  review_families,
  composition_edges
}
```

The local test target is:

```text
MiniHarness(H_A, D_A) -> local_score + evidence
```

The composition test target is:

```text
Compose(H_A, H_B) -> workflow_score + integration_evidence
```

This decouples optimization. Instead of asking one huge question:

```text
How do we optimize H over A, B, C, and D all at once?
```

Ask smaller questions:

```text
How do we optimize H_A for task family A?
How do we optimize H_B for task family B?
How do we optimize theta_skill_i for the tasks skill_i owns?
How do we optimize system_prompt_policy for global constraints only?
How do we test Compose(H_A, H_B)?
```

The result is a cleaner coordinate:

```text
theta_skill_i
  -> SkillEval(skill_i, D_skill_i)
  -> score_delta
```

This is usually easier to improve than:

```text
theta_all -> HarnessEval(H_theta, D_all) -> score_delta
```

The caveat is interaction. A skill can pass its local eval and still fail in a
workflow if routing, composition, evidence handoff, or global constraints are
wrong. That is why skill evals should be paired with a smaller number of
workflow evals.

Do not decompose when the task is one-off, low-risk, or already fits in a
single context without pollution. Decomposition has coordination cost.

The leverage claim:

```text
If most harness behavior is represented through skills,
then optimizing skill contracts and skill evals is the dominant practical path
for optimizing decomposed harnesses.
```

Evals optimize the harness by making accept/reject decisions measurable:

```text
regression_rate decreases
overfitting risk becomes visible
heldout_score constrains self-improvement
```

Skill evals are especially powerful because they justify progressive
disclosure. If a skill eval passes, behavior can move out of the system prompt
and into a just-in-time skill:

```text
system_prompt_policy decreases
skill_policy increases
task_success is preserved
context_cost decreases
```

Automatic eval writing is itself a meta process:

```text
WriteEval(claim, target_variable, failure_examples) -> task_cases
                                                    + judge_prompt
                                                    + baseline_result
```

Use it when a harness change has a repeatable claim:

```text
"this skill reduces turns"
"this subagent prevents context drift"
"this hook blocks false completion"
"this memory drain reduces repeated mistakes"
```

No eval means the harness can still improve, but the improvement remains a
judgment call rather than a measured update.

`HarnessAdvisorEval` should use placement cases:

```text
HarnessAdvisorEvalCase = {
  improvement_request,
  local_evidence,
  expected_primary_surface,
  acceptable_alternatives,
  rejected_surfaces,
  required_proof_plan,
  known_trap,
  heldout_group
}
```

Scoring dimensions:

```text
primary_owner_correct
secondary_sync_points_valid
proof_plan_adequate
root_prompt_overreach_avoided
nondeterministic_hook_misuse_avoided
heldout_case_generalization
```

Seed cases should include review/evidence failures, eval/skill-contract
failures, deterministic guardrail failures, prompt bloat, stale memory, and
over-broad migrations.

## 11. Filesystem Variables As State

The filesystem is a first-class harness state store, not just storage.

Good filesystem structure mirrors good human project structure: searchable,
modular, purpose-driven, easy to update, easy to validate, and reusable across
future tasks.

```text
FileVariable(path) -> {
  purpose,
  owner,
  allowed_writers,
  expected_readers,
  schema_or_shape,
  retrieval_keys,
  freshness_rule,
  validation_command,
  archive_or_drain_rule
}
```

Typed filesystem variables:

```text
filesystem = {
  docs_specs,
  tickets,
  registries,
  artifacts,
  eval_runs,
  templates,
  ledgers,
  scripts
}
```

Examples:

- `README.md` is a public routing variable.
- `docs/specs/*.md` are durable contract variables.
- `tickets/TASK-*/ticket.md` is a work-state and proof-target variable.
- `docs/features/registry.jsonl` is a feature-state variable.
- `docs/skills/registry.jsonl` is a generated skill-inventory variable.
- `tickets/TASK-*/artifacts/*` are evidence variables.
- eval run JSON is reward/evidence state.

To minimize mistakes, file variables should be:

- easy to search
- easy to route to the right reader
- compartmentalized enough to fit context
- purpose-driven rather than a junk drawer
- appendable or patchable without rewriting unrelated state
- reusable by future tasks
- validated mechanically when possible

Weak harness behavior often comes from implicit variables: files that agents
write but later agents do not know to read, trust, update, drain, or delete.

The simplest memory system is one file:

```text
memory_file = memory.md

Agent(task, memory_file) -> output + memory_delta

memory_file_{t+1} =
  update(memory_file_t, memory_delta)
```

This is enough when the task family is narrow and context pollution is low.
For example:

```text
autoresearch_state = program.md

AutoresearchAgent(program.md) -> experiment_log
                              + metric_update
                              + next_iteration
```

Here `program.md` can hold the goal, metric, current hypothesis, experiment
log, and next action. The agent is iterating over one state file that already
contains the reward signal.

Another simple loop:

```text
ralph_state = progress.md + spec.md

RalphLoop(spec.md, progress.md) -> selected_work
                                + progress_delta
```

Here `spec.md` defines the target and `progress.md` tracks what has been done
or still needs doing.

One-file memory is good for bootstrapping:

```text
low_setup_cost increases
iteration_speed increases
coordination_cost decreases
```

But as the task family broadens, one file becomes noisy:

```text
context_pollution increases
retrieval_precision decreases
stale_state risk increases
specialized_task_focus decreases
```

That is when the harness should split state into modular files:

```text
memory.md -> {
  program.md,
  progress.md,
  spec.md,
  lessons.md,
  troubles.md,
  eval_results.json,
  artifacts/
}
```

The rule:

```text
Start with one state file when the loop is simple.
Split into typed variables when specialized tasks need cleaner context.
```

The RL-style view is:

```text
state_t = {
  task,
  ticket_file,
  progress_file,
  research_file,
  plan_file,
  implementation_files,
  review_file,
  eval_results,
  memory_files
}
```

An agent action reads a state slice and writes new state:

```text
action_t =
  run_agent(role, prompt, inputs=state_slice_t)

observation_t =
  read(action_t.output_files)

state_{t+1} =
  update(state_t, observation_t)
```

Example research-to-plan flow:

```text
state_0 = {
  task,
  ticket_file,
  progress_file
}

research_file =
  run_agent("researcher", research_prompt, inputs=[
    state_0.task,
    state_0.ticket_file,
    state_0.progress_file
  ])

state_1 =
  update(state_0, { research_file })

plan_file =
  run_agent("planner", plan_prompt, inputs=[
    state_1.task,
    state_1.research_file,
    state_1.ticket_file
  ])

state_2 =
  update(state_1, { plan_file })

review_file =
  run_agent("reviewer", review_prompt, inputs=[
    state_2.plan_file,
    state_2.research_file,
    state_2.ticket_file
  ])

state_3 =
  update(state_2, { review_file })
```

Example memory-drain flow:

```text
trouble_delta =
  drain(docs/TROUBLES.md, rule="repeated_or_structural")

lesson_delta =
  synthesize(trouble_delta, target=docs/LESSONS.md)

memory_delta =
  promote(lesson_delta, target=docs/MEMORY.md)

theta_delta =
  propose_harness_update(memory_delta, target=[
    system_prompt_policy,
    skill_policy,
    filesystem_policy
  ])
```

Reward can be evaluated over state:

```text
reward(state_t) =
  task_success
+ evidence_completeness
+ context_reuse
+ searchability
- duplicated_work
- stale_state
- coordination_cost
- missing_file_updates
```

This framing makes files more than artifacts. Files are the state representation
that lets the harness plan, resume, delegate, verify, drain memory, and update
its own configuration.

## 12. Coordinate Descent Over Harness Variables

A bounded harness improvement loop:

```text
theta_{t+1} =
  theta_t + Delta theta  if Accept(Delta theta)
  theta_t                otherwise
```

Operational acceptance rule:

```text
Accept(Delta theta) :=
  score_improves
  AND required_review_families_are_TAS_A
  AND eval_or_regression_evidence_supports_claim
  AND integration_readiness_is_TAS_A
  AND cost <= budget
  AND prompt_size <= limit
  AND no_safety_regression
  AND no_test_regression
  AND heldout_score_does_not_regress
  AND no_scope_overreach
```

Lifecycle rule:

```text
promote:
  repeated pass
  AND no hard-gate failures
  AND integration proof exists

hold:
  local pass
  AND workflow_or_composition_proof_missing

rollback:
  regression
  OR weak evidence
  OR composition failure
  OR safety regression
```

The harness search space is discrete. Practical optimization is usually
coordinate descent:

```text
choose one coordinate
change it
measure the relevant reward/loss terms
keep, revise, or revert
record the lesson
```

Useful coordinates:

```text
system_prompt_policy
skill_policy
skill_function_contract
subagent_policy
hook_policy
mcp_policy
memory_policy
filesystem_policy
eval_policy
automation_policy
verification_policy
ticket_contract
feature_registry
skill_registry
filesystem_lifecycle_rule
```

The repeated failure rule:

```text
If the same loss appears in many places, move up the tier graph.
If the loss is local, fix the local owner.
```

Escalate up the tier graph only when:

```text
repeated_failures_across_multiple_owners
OR registry_or_graph_evidence_shows_broad_duplication
OR local_fix_failed_and_failure_is_structural
OR one_high_severity_global_failure_requires_always_loaded_policy
```

Otherwise, keep the fix local. The `ROI(Tier1) >= ROI(Tier2) >= ROI(Tier3)`
prior is a leverage prior, not permission to expand blast radius.

## 13. Harness Advisor Use

`harness-advisor` should use this spec as a placement model.

Given:

```text
HarnessAdvisor(improvement_request, state, registries, specs)
```

Return:

```text
target_variable + rationale + proof_plan
```

Decision schema:

```text
HarnessAdvisorDecision = {
  improvement_request,
  failure_mode,
  loss_term,
  task_slice,
  candidate_coordinates,
  owner_surface,
  rejected_surfaces,
  quality_lever,
  proof_plan,
  accept_rule,
  rollback_rule,
  secondary_sync_points
}
```

Decision recipe:

```text
operator_complaint
  -> failure_mode
  -> loss_term
  -> task_slice_or_mini_harness
  -> candidate_coordinate
  -> owner_surface
  -> quality_lever
  -> proof_surface
  -> accept_or_hold_or_rollback
```

Advisor procedure:

```text
1. Translate the request into a failing reward or loss term.
2. Identify candidate coordinates in theta.
3. Check whether the problem is local, workflow-wide, or graph-wide.
4. Prefer the smallest coordinate change that can improve the objective.
5. Increase scope only when compounding leverage justifies the blast radius.
6. Define proof: eval, validator, review gate, representative tasks, or artifact check.
7. Accept only if the metric improves and constraints do not regress.
```

Placement examples:

```text
root-policy bloat
  -> skill_policy or system_prompt_policy
  -> proof: prompt_size decreases and task_success does not regress

skill contract gap repeated across many skills
  -> skill-creator or skill-maintenance
  -> proof: template/check_skills/eval cases improve future skill quality

bad placement recommendations
  -> harness-advisor
  -> proof: HarnessAdvisorEval improves on heldout placement cases

repeated false completion
  -> verification_policy, proof_contract, hook_policy
  -> proof: completion evidence gate catches representative misses

recurring lesson not being reused
  -> automation_policy, memory_policy, filesystem_lifecycle_rule
  -> proof: drain writes the right file and future tasks retrieve it
```

The advisor should be especially alert for compounding levers:

```text
Tier 1 primitive update
Tier 2 workflow-interface update
skill-creator template or standards update
skill-maintenance validation or registry update
eval-writer pattern
harness-advisor placement rubric update
global template update only when every project needs it
system prompt update only when the rule must be active every turn
```

Counterexamples to avoid:

```text
local skill bug
  -> wrong: root prompt update
  -> better: owning skill contract or skill eval

judgment-heavy review failure
  -> wrong: hook
  -> better: review rubric routing or proof contract

eval added without baseline or heldout cases
  -> wrong: claim improvement from one case
  -> better: baseline + representative cases + heldout split

local skill eval passes but workflow fails
  -> wrong: promote skill change globally
  -> better: hold until composition eval or integration review passes

reviewer returns TAS-B
  -> wrong: treat as pass
  -> better: revise or hold until required TAS gates pass

mini-harness split adds coordination cost without clearer proof
  -> wrong: over-decompose
  -> better: keep one state file or one workflow eval
```

That is the core thesis in operational form:

```text
A harness is a constrained optimizer over its own context, capability, control,
state, and verification variables.
```
