---
title: Harness Algebra
status: active
owner: harness-advisor
created_at: 2026-06-09
updated_at: 2026-06-13
refs:
  - docs/fundamentals/harness-engineering-doctrine.md
  - docs/fundamentals/prompt-engineering.md
  - docs/specs/filesystem-lifecycle.md
  - docs/specs/goal-loop-contract.md
  - docs/skills/README.md
  - templates/global/AGENTS.md
  - agents/skill-opportunity-applier.toml
  - skills/optimize-harness/SKILL.md
  - skills/goal-advisor/SKILL.md
---

# Harness Algebra

## Purpose

This is Farplane's quick guide to harness engineering. It defines the core
objects, functions, and levers for making agents more reliable without turning
every fix into more always-loaded prompt.

The guide is structured like a course:

```text
model -> levers -> prompt -> skills -> phases/budget -> context/state
      -> verification -> hooks/goals -> optimization
```

Use `docs/fundamentals/harness-engineering-doctrine.md` as the concise field
guide for deciding which concrete lever to pull.

## 1. Harness Engineering

Traditional prompt algebra treats the next model call as a constructed input
prompt plus history. That is context engineering. It matters for retrieval,
packing, and prompt construction, but it is not the harness-engineering model
Farplane needs here.

Harness engineering asks which system surface owns behavior, budget, proof,
lane responsibility, control, and writeback. It starts from grounded context:
local source search for repo truth, and web/source search when real-world,
current, or comparable-product context changes the answer.

The useful harness model is:

```text
H(task, state) -> output + evidence + state_delta
```

Use one standard harness vector. Do not introduce alternate symbols,
`Harness`, or prompt-input decompositions elsewhere in this doc.

```text
H = {
  policy_surfaces,
  project_instructions,
  skill_contracts,
  subagent_prompts,
  tool_surfaces,
  memory_and_lesson_files,
  ticket_or_goal_state,
  verification_surfaces,
  hooks_and_automations,
  phase_and_ensemble_budget
}
```

The canonical term is `H`.

A harness turn:

```text
context = gather_context(task, state, H)
controls = select_controls(task, context, H)
output = execute(task, context, controls)
evidence = verify(output, task, controls)
state_delta = write_back(state, output, evidence)
```

Harness engineering changes one or more levers:

```text
Delta H -> changed_behavior + evidence
```

The core DNA is priority-ordered constrained optimization over quality targets
and costs:

```text
choose context, tools, skills, agents, state, and verification
to minimize:
  incorrectness
+ hallucination_or_ungrounded_claims
+ unusable_output
+ unnecessary_response_length
+ tokens
+ latency
+ turns
+ duplicated_instruction
+ coordination_cost
+ failure_rate
while maximizing:
  groundedness
+ correctness
+ usability
+ appropriate_detail
+ task_success
+ reliability
+ reusable_behavior
+ auditability
```

Hard constraints come first:

```text
user_goal_satisfied == true
groundedness_sufficient == true
correctness_regression == false
safety_regression == false
proof_exists == true
operator_control_preserved == true
```

Then optimize in priority order:

```text
1. Preserve correctness, safety, proof, and operator control.
2. Ground the answer in local repo evidence and real-world/current context when
   that context changes the decision.
3. Make the output usable for the operator's actual next action.
4. Match response length to the task: complete enough to act, no padding.
5. Load always-needed constraints where they are cheapest to retrieve.
6. Minimize irrelevant always-loaded prompt.
7. Minimize turns and coordination cost.
8. Add control loops only when the failure mode justifies them.
```

Prompt size is only one cost term:

```text
total_cost ~= prompt_tokens + tool_calls + turns + coordination_cost

error_risk ~= missing_context
           + noisy_context
           + contradictory_context
           + weak_verification
           + unclear_owner
           + missing_real_world_context
```

Promotion rules:

```text
promote_to_system_prompt(context)
  iff always_needed(D, context) is high
  AND omission_cost(context) is high
  AND contradiction_or_bloat_risk(context) is low

promote_to_skill(context)
  iff needed_for_task_family(D_i, context)
  AND not globally_needed(context)

keep_in_file_or_memory(context)
  iff durable(context)
  AND not always_needed(context)

use_tool_or_search(context)
  iff freshness_required(context)
  OR context_too_large_to_preload(context)
  OR real_world_or_comparable_context_changes_the_decision(context)
```

## 2. Harness Decomposition

Use the same `H` vector when decomposing a harness. A decomposed harness is not
a new definition; it is the same vector restricted to a task family, skill, or
workflow.

For a task family `A`:

```text
H_A =
  policy_surfaces_A
+ project_instructions_A
+ skill_contracts_A
+ tools_A
+ subagents_A
+ memory_A
+ ticket_or_goal_state_A
+ verification_A
+ hooks_A
+ budget_A
```

A skill is the default mini-harness:

```text
SkillHarness_s =
  skill_contract_s
+ required_references_s
+ allowed_tools_s
+ optional_subagent_lanes_s
+ state_reads_s
+ state_writes_s
+ proof_contract_s
+ budget_s
```

This is why skills compose. Each skill works toward one task family or outcome,
has its own proof surface, and can be optimized independently before being
tested inside larger workflows.

For two task families:

```text
D = A + B
H_D ~= H_A + H_B + Compose(H_A, H_B)
```

Composition must be tested:

```text
local_score = Score(H_A, D_A)
workflow_score = Score(Compose(H_A, H_B), D_workflow)
```

Harness composition is not perfectly associative because context windows,
side effects, and tools are finite. A good harness tries to make composition
behave as if it were associative across explicit contracts:

```text
(H_C . H_B) . H_A ~= H_C . (H_B . H_A)
```

This works when each component has:

```text
input_contract
output_contract
state_reads
state_writes
proof_contract
owner_boundary
```

If contracts are vague:

```text
ambiguous_output + hidden_state + weak_proof
  -> brittle_workflow
```

Mini-harnesses make decomposition concrete. Most mini-harnesses should be
skills; use a ticket, goal packet, or workflow mini-harness only when the unit
is task-local, long-running, or crosses several skills.

```text
MiniHarness = {
  id,
  owner,
  task_family,
  skill_contract?,
  skill_budget,
  ensemble_budget,
  tools,
  subagents,
  state_files,
  proof_contract,
  eval_cases,
  composition_edges
}
```

## 3. Prompt Engineering Is All We Need

The slogan is intentionally provocative. Farplane has skills, tickets,
subagents, evals, hooks, automations, and Goal Packets, but most of those
surfaces are prompt-shaped contracts.

```text
prompt_contract(job, context, rules, examples, output, proof)
  -> reliable_model_behavior
```

Every reusable harness surface answers the same questions:

```text
job: what should the model do?
context: what facts and files does it need?
rules: what constraints and procedures matter?
examples: what does good or bad look like?
output: what artifact or response should exist?
proof: how do we know it worked?
```

Mapping:

```text
SKILL.md              ~= reusable prompt contract
ticket.md             ~= task-local prompt and proof contract
subagent prompt       ~= role and ownership contract
reviewer handoff      ~= judgment prompt with rubric and evidence
eval judge            ~= scoring prompt
Goal prompt           ~= runtime prompt derived from state files
hook message          ~= deterministic control prompt or event contract
```

Good prompt contracts reduce variance:

```text
clear_job + relevant_context + sharp_output + proof
  -> lower_ambiguity + lower_turn_count + higher_reliability
```

Bad prompt contracts create hidden loss:

```text
vague_job + noisy_context + missing_examples + no_proof
  -> drift + false_completion + repeated_corrections
```

Prompt engineering is not only prose quality. It is the discipline of making
model behavior inspectable, reusable, and testable.

## 4. Skill Engineering

A skill is a packaged reusable workflow. It moves procedure out of
always-loaded prompt text and into just-in-time context.

```text
Skill_s(input, state) -> output + evidence + state_delta
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

Skill package:

```text
SkillPackage = {
  SKILL.md,
  references?,
  scripts?,
  templates?,
  eval_task?,
  audits?,
  self_improve?
}
```

Standard `SKILL.md` shape:

```text
frontmatter
Context
Skill Signature
Phase Contract?
Phase Boundary?
Todo List
Templates
Gotchas
Reference Map
Output
```

Skill tier system:

```text
Tier 0 = native phase protocol, inherited by every skill invocation
Tier 1 = primitive behavior moves such as advise, grounding, prototyping
Tier 2 = workflow interfaces such as plan, research, review, eval
Tier 3 = domain/application skills such as goal-advisor or optimize-harness
```

Tiered first-load rule:

```text
Tier3.todo -> Tier2 or peer Tier3
Tier2.todo -> Tier1 or local references
Tier1.todo -> direct primitive procedure
```

Tier 0 phases are not skill links. They are the native lifecycle that can stay
inline or become separate artifacts when needed.

Skill frontmatter makes the package discoverable:

```text
frontmatter -> registry_row -> generated_skill_graph -> selection_context
```

Skill todo lists make invocation inspectable:

```text
skill_first_load(skill, task)
  -> active_todo_list + required_references + proof_target
```

Skill composition:

```text
(Skill_b . Skill_a)(x) = Skill_b(Skill_a(x))
```

Composition is valid when:

```text
Skill_a.output_contract compatible_with Skill_b.input_contract
AND Skill_a.state_delta does_not_violate Skill_b.assumptions
AND proof_handoff is explicit
```

Skill optimization:

```text
Delta Skill_s
  -> less_root_prompt
   + more_reusable_behavior
   + lower_turn_count
   + fewer_repeated_misses
```

Skill losses:

```text
stale_trigger
wrong_skill_selection
missing_input_contract
hidden_side_effects
too_much_ceremony
no_eval_or_review_path
```

Skill eval target:

```text
SkillEval(skill, task_cases, judge)
  -> score + verdict + evidence
```

Skill evals compound from lower tiers:

```text
improve(Tier1 primitive)
  -> improves Tier2 workflows that call it
  -> improves Tier3 domain skills that depend on those workflows
  -> improves e2e workflows that compose the domain skills
```

Default optimization direction:

```text
primitive behavior -> workflow skill -> domain skill -> e2e workflow
```

Climb upward only when the lower-tier contract is already sharp and the
remaining failure is genuinely compositional.

Use skill engineering when behavior should repeat across tasks. Use a ticket or
one-off prompt when the workflow is local, unstable, or not worth packaging.

## 5. Phase And Budget Engineering

Every serious skill invocation inherits the Tier 0 phase protocol:

```text
phase_protocol(task, state)
  -> grounded_inputs
   + path_choice
   + plan_or_direct_action
   + execution
   + proof
   + review_if_material
   + state_delta
```

Typical phase order:

```text
ground -> choose_path -> plan? -> execute -> verify -> review? -> write_back
```

Externalize a phase only when the extra artifact or independent judgment is
worth the coordination cost:

```text
external_phase(phase, task, scope, budget)
  -> artifact + evidence

externalize_phase = true
  iff value(artifact_or_independent_judgment) > coordination_cost
```

The anti-recursion rule:

```text
valid_external_phase_call(parent_scope, child_scope)
  iff child_scope < parent_scope
```

Budget is compute allocation across phases:

```text
PhaseBudget = {
  effort,
  context_depth,
  search_breadth,
  tool_call_limit,
  subagent_count,
  review_depth,
  eval_depth,
  time_limit,
  token_limit
}
```

Phase budget belongs inside the skill or workflow that spends it. Do not make a
global phase-budget table when only a few skills need the knob.

Budgeted skills include:

| Skill family | Budget fields |
| --- | --- |
| `plan`, `impl-plan`, `goal-advisor` | planning depth, ambiguity gates, decomposition depth |
| `research`, `reference-grounding` | source count, search breadth, recency/currentness, citation depth |
| `advise`, `deliberative-advice` | option count, independent lanes, critique depth |
| `review`, `visual-qa`, `agent-qa-test` | rubric depth, evidence depth, reviewer/QA lanes |
| `eval`, `eval-onboarding` | case count, fixture depth, judge strictness, heldout coverage |
| `optimize-harness`, `self-improve` | candidate count, iteration count, metric budget, rollback gate |
| `impl`, `work`, `batch-work` | execution scope, proof rows, QA/review depth |

Budget is not a standalone lever. It modulates the other levers:

```text
budget(task, risk)
  -> plan_depth
   + research_depth
   + execution_depth
   + verification_depth
   + review_depth
   + ensemble_depth
```

Example:

```text
tiny_fix -> inline_ground + direct_execute + narrow_check
material_doc_change -> ground + plan + edit + validators + review
ticketed_impl -> ground + plan + implement + QA + review + closeout
goal_loop -> ground + execute_leaf + progress_write + drift_check
```

## 6. Context, Memory, And Tickets

Context engineering chooses what state the model sees, what it does not see,
and how new state is written back.

```text
select_context(task, state, budget) -> selected_context
```

The goal:

```text
maximize useful_context
minimize irrelevant_context + stale_context + missing_context
```

A file is a state variable when future agents are expected to read, trust,
update, validate, archive, or drain it.

```text
FileVariable(path) -> {
  purpose,
  owner,
  allowed_writers,
  expected_readers,
  shape,
  freshness_rule,
  validation_command,
  archive_or_drain_rule
}
```

Core Farplane state variables:

```text
README.md                  = public routing variable
ARCHITECTURE.md            = whole-system map
docs/fundamentals/*.md     = conceptual model and doctrine
docs/specs/*.md            = buildable contracts
docs/MEMORY.md             = durable invariants
docs/TROUBLES.md           = repeated raw misses
docs/LESSONS.md            = distilled prevention rules
docs/features/registry     = feature inventory
docs/skills/registry       = skill inventory
tickets/TASK-*/ticket.md   = task contract and proof target
tickets/TASK-*/program.md  = loop configuration when needed
tickets/TASK-*/progress.md = append-only observed progress
tickets/TASK-*/artifacts   = evidence
```

Ticket as task memory:

```text
TicketProgram :=
  Summary
+ Scope
+ Delta
+ Program
+ Map
+ DoneProof
+ State
+ Links
```

Ticket execution:

```text
ticket.md + skill_contract + implementation_files
  -> artifact + evidence + ticket_state_delta
```

Context pollution:

```text
context_pollution =
  irrelevant_files
+ stale_memory
+ duplicated_rules
+ contradictory_instructions
+ unowned_artifacts
```

Context starvation:

```text
context_starvation =
  missing_ticket
+ missing_spec
+ missing_examples
+ missing_current_state
+ missing_proof_contract
```

Hook-backed learning:

```text
message_window(session)
  -> skill_opportunity_applier
  -> docs/TROUBLES.md? + docs/LESSONS.md?
```

The learning reviewer writes only strong, compact local rows. It does not run
`optimize-harness`. Later drains decide whether those rows should become skill,
prompt, ticket, eval, or doctrine changes.

Drain flow:

```text
trouble_delta =
  drain(docs/TROUBLES.md, rule="repeated_or_structural")

lesson_delta =
  synthesize(trouble_delta, target=docs/LESSONS.md)

memory_delta =
  promote(lesson_delta, target=docs/MEMORY.md)

h_delta =
  propose_harness_update(memory_delta, target=[
    policy_surfaces,
    skill_contracts,
    memory_files,
    verification_surfaces
  ])
```

If a lesson stays only in chat, it is not part of the harness.

## 7. Verification Engineering

Verification engineering chooses the right proof signal for a claim.

```text
verify(output, claim, proof_surface) -> pass | revise | block + evidence
```

Proof routing:

```text
judgment-heavy quality claim -> review
repeatable behavior claim -> eval
user-visible workflow claim -> QA or browser proof
deterministic invariant -> validator or hook fixture
state drift claim -> drift review
human taste or ranking -> human_feedback
market result -> market_signal
artifact presence claim -> file/path check plus review when judgment matters
```

Eval layers:

```text
agent_or_policy_eval -> checks always-loaded instructions, AGENTS.md behavior,
                        and native phase protocol

skill_eval -> checks one SkillHarness in isolation

e2e_workflow_eval -> checks composed skills, tickets, tools, subagents,
                     state, and review gates together
```

Use the cheapest layer that can falsify the claim. If a skill eval fails, fix
the skill before blaming the e2e workflow. If a primitive skill fails, fix the
primitive before patching every caller.

### Todo, Eval, QA, And Benchmark Symmetry

Todos, evals, QA checklists, reviews, and benchmarks are different projections
of one latent behavior contract. They feel like separate systems because the
contract is usually incomplete, disputed, or easier to see from examples than
from procedure.

```text
BehaviorContract :=
  reference_points
+ procedure
+ evidence_shape
+ verdict_rule
+ owner_surface

todo(BehaviorContract)
  -> ordered actions expected to produce the behavior

eval(BehaviorContract)
  -> repeatable input/context whose answer should satisfy reference_points

qa_checklist(BehaviorContract)
  -> runtime or final checks applied to one concrete artifact or run

review(BehaviorContract, evidence)
  -> judgment over whether the evidence satisfies the contract

benchmark(eval_cases[])
  -> aggregate comparison signal across cases, variants, or agents
```

At the fixed point, the projections converge:

```text
perfect_contract:
  todo_list.reference_points
  == eval.reference_points
  == qa_checklist.items
  == review.rubric.required_points

qa_check =
  apply(todo_list)
  AND verify(todo_list_executed_against_evidence)
```

In that perfect world, an eval is just an executable todo list, and QA is the
same todo list checking its own execution. The distinction exists because real
harness work starts before the best todo shape is known.

Discovery loop:

```text
unknown_contract
  -> write expected answers or failure cases faster than full procedure
  -> eval.reference_points reveal missing or noisy todos
  -> todo_list becomes a better production procedure
  -> qa_checklist derives the reusable runtime guardrails
  -> review handles judgment that is still too contextual for a validator
  -> benchmark aggregates enough evals to compare variants
```

This is why evals and checklists should compete until they converge. When the
reference points are easier to state as expected outputs, start with evals.
When the procedure is clearer than the examples, start with todos. When the
same reference point becomes reusable during real execution, promote it into a
QA checklist, validator, review rubric, or hook depending on its determinism and
cost.

Ownership:

```text
eval owns:
  eval_task.json, example cases, reference_points, run artifacts

skill-maintenance owns:
  skill-local checklist references, first-load todo shape, skill audit writeback

agent-qa-test or reviewer owns:
  adversarial or independent application of the checklist to real behavior

qa owns:
  ticket-scoped proof artifacts and Done / Proof reconciliation

benchmark owns:
  aggregate comparison across eval cases, agents, variants, or releases
```

Sync rule:

```text
after_update(eval_task.json):
  for each new_or_changed reference_point:
    if reusable_runtime_guardrail(reference_point):
      update owning skill checklist/reference through skill-maintenance
    if deterministic_invariant(reference_point):
      consider validator or hook fixture
    if judgment_heavy(reference_point):
      keep review or QA checklist wording explicit
```

Do not force every eval reference point into a checklist. Some reference points
exist only to preserve a hardcase, compare variants, or test a boundary that is
too rare to load on every invocation. The useful move is convergence, not
duplication.

Do not use hooks for judgment-heavy work. Do not use review prose for
deterministic invariants that a validator can check. Do not invent numeric
metrics when the honest signal is a review verdict, human decision, or artifact
presence.

Acceptance:

```text
Accept(Delta H) :=
  named_loss_reduced
  AND proof_signal_supports_claim
  AND required_review_gates_pass
  AND no_safety_regression
  AND no_test_regression
  AND no_scope_overreach
  AND cost <= budget
```

Hold:

```text
hold:
  local proof passes
  AND workflow_or_composition_proof_missing
```

Rollback:

```text
rollback:
  regression
  OR weak evidence
  OR composition failure
  OR safety regression
  OR owner_surface_was_wrong
```

For review-gated work, `TAS-B` is not accepted. Revise or hold until the
required gate passes.

## 8. Hooks, Automations, And Goal Control

Control decides when work starts, pauses, resumes, blocks, or completes.

```text
control(event, state, artifacts)
  -> continue | block | complete | wait | start_child_work
```

Real control levers:

```text
Stop hook          = end-of-turn gate and continuation/completion control
UserPrompt hook    = turn-start intent capture
learning sidecar   = bounded-window trouble/lesson writer
validators         = mechanical invariants
automations/cron   = scheduled or event-triggered checks
heartbeat          = delayed inspection of existing state
native Goal        = continuation for one executable leaf
drift reviewer     = read-only alignment check
```

Hook:

```text
Hook(event, state, artifacts) -> gate_decision + evidence
```

Automation:

```text
Automation(trigger, schedule, state) -> task | no_op
```

Heartbeat:

```text
heartbeat(ticket, program, progress, trigger)
  -> inspect_state + action | no_op + progress_entry
```

Cron can call `goal-advisor` to prepare a Goal Packet for a ticket:

```text
cron_goal_run(schedule, ticket)
  -> goal_advisor(ticket, state)
  -> GoalPacket?
  -> native_goal_prompt?
```

Goal Packet:

```text
GoalPacket :=
  ticket.md
+ program.md
+ progress.md
+ generated_goal_prompt
+ drift_check_contract

goal_loop(ticket.md, program.md, progress.md, trigger)
  -> next_turn + evidence + drift_verdict + state_delta
```

Goal prompt:

```text
native_goal_prompt(ticket.md, program.md)
  -> Task + Logging + Metric + AfterEachTurn + Budget?
```

The prompt is generated runtime text. `ticket.md`, `program.md`, and
`progress.md` are the state.

After each Goal turn:

```text
after_goal_turn(ticket, program, progress, current_claim)
  -> append_progress
   + drift_check?
   + continue | wait | complete | blocked
```

Material or self-approval-prone Goal loops use a read-only drift reviewer:

```text
drift_check(ticket, program, progress_tail, current_claim)
  -> aligned | drifting | blocked | complete_candidate
   + reason
   + evidence_refs
   + recovery_action
```

Long-term goal hierarchy:

```text
goal -> project[] -> task[]

portfolio.md = long-horizon goal graph + current_frontier
ticket.md = executable leaf contract + Done / Proof
program.md = loop configuration + metric + stop policy
progress.md = append-only observed execution
artifacts/ = evidence
```

Portfolio heartbeat:

```text
portfolio_heartbeat(portfolio.md, program.md, progress.md)
  -> no_op | start_child_goal | resume_child_goal | request_feedback | replan
```

Leaf execution:

```text
leaf_native_goal(ticket.md, program.md, progress.md)
  -> artifact + evidence + completion_entry
```

Completion transition:

```text
complete_child_goal(child_packet, portfolio, parent_program)
  -> progress_entry + portfolio_state_delta + next_trigger
```

Rollout:

```text
rollout_goal(pattern, sample_results, target_set)
  -> child_ticket[] | staged_checkpoints + rollout_progress
```

The parent portfolio chooses the next frontier. Native Goal mode executes one
leaf. Completion updates portfolio memory before the next heartbeat or replan.

Control improves reliability only when trigger, state, stop condition, and
proof are explicit:

```text
control_lever improves reliability
  iff trigger + state + stop_condition + proof are explicit

control_lever becomes hidden_autonomy
  iff trigger or state or stop_condition is implicit
```

## 9. Harness Optimization

Optimization turns observed behavior gaps into accepted harness changes.

```text
ObservedFailure -> LossTerm -> HarnessLever
                -> Intervention -> Evidence -> AcceptRule
```

Farplane's applied operator is `optimize-harness`:

```text
optimize_harness(observed_behavior, expected_behavior?, metric?, evidence?)
  -> accepted_change | experiment_plan | blocked_report
```

Expanded:

```text
observed_behavior
  -> expected_behavior
  -> gap
  -> loss_term
  -> candidate_lever
  -> owner_surface
  -> proof_signal
  -> Delta H
  -> accept | hold | rollback
```

Decision record:

```text
HarnessDelta = {
  observed_behavior,
  expected_behavior,
  loss_term,
  lever,
  owner_surface,
  rejected_surfaces,
  proof_signal,
  delta_H,
  accept_rule,
  rollback_rule
}
```

Loss map:

| Observed Loss | Likely Lever | First Proof |
| --- | --- | --- |
| Agent ignores a reusable workflow. | Skill or skill contract | Skill eval or transcript replay. |
| Agent asks broad unnecessary questions. | Prompt, skill contract, or ticket contract | Behavior test on correction cases. |
| Agent completes without evidence. | Verification, ticket contract, hook, or review | Review receipt, hook fixture, done-proof check. |
| Agent bloats every reply with policy. | System prompt or skill | Prompt/token diff plus regression check. |
| Agent loses long-running state. | Ticket/program/progress or Goal Packet | Resume from files without transcript context. |
| Agent self-approves material work. | Subagent or review gate | Reviewer-lane proof. |
| Agent misses repeated lessons. | Learning sidecar, drain, memory, or skill update | Retrieval/drain test. |
| Deterministic invariant keeps breaking. | Validator or hook | Validator or fixture. |
| Skill changes regress workflows. | Skill eval or skill-maintenance | Heldout skill/workflow eval. |
| Goal loops drift or become prompt-only. | Goal Packet or drift review | Drift review over ticket/program/progress. |

Escalate scope only when:

```text
repeated_failures_across_multiple_owners
OR registry_or_graph_evidence_shows_broad_duplication
OR local_fix_failed_and_failure_is_structural
OR one_high_severity_global_failure_requires_always_loaded_policy
```

Otherwise, fix the local owner.

Use a direct patch when the gap, owner, proof, and accept rule are clear:

```text
direct_patch(gap, lever, owner, proof)
  -> Delta H + verification
```

Use `self-improve` or an experiment when there is a real search space:

```text
self_improve(target_surface, metric, baseline, candidates)
  -> best_candidate | no_improvement | blocked
```

Do not use `self-improve` for ordinary implementation or doc cleanup.
