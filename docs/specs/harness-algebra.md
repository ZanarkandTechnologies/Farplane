# Harness Algebra

Status: draft contract

Date: 2026-06-09

## Purpose

Define harness engineering as a mathematical optimization problem around a
model. The spec starts from the basic model call, defines the harness variables,
objective and reward functions, and update loop, then shows how skills, evals,
hooks, memory drains, tickets, and meta-skills become composable functions over
typed artifacts and state transitions.

This spec is the canonical place for the algebra thesis. Individual skills may
carry compact function contracts, but the system-wide notation belongs here.

## Decision

Farplane should teach harness engineering as constrained optimization over an
agent's context interface:

```text
Codex = M(context, task) -> output

context =
  system_prompt
+ tool_descriptions
+ selected_skills
+ memory
+ conversation_history
+ task_input

Harness H := policy for constructing, updating, verifying, and optimizing
that context for a class of tasks.
```

The real objective is not to make every prompt look mathematical. The objective
is to define the variables, reward function, constraints, and update rules that
let Farplane improve the harness without drifting into prompt bloat,
self-approval, or hidden state.

The process-function model still matters, but it sits under the optimization
model:

```text
Process := Inputs + ReadSet + Transform + WriteSet + Outputs + Evidence
```

Every reusable harness process should answer:

- what inputs it consumes
- what files, ledgers, tools, or runtime state it reads
- what transformation it applies
- what outputs it produces
- what durable variables it writes
- what evidence proves the transformation worked
- how it composes with upstream and downstream processes

## Advise Decision

The placement decision had three viable options:

1. Put full algebra blocks in every `SKILL.md` immediately.
   - Pros: maximum visibility and immediate pressure toward formal contracts.
   - Cons: noisy migration, high chance of generic filler, and too much churn
     before the notation is proven.
2. Create this canonical spec, add a compact skill-template `Function Contract`,
   and roll it out on contact or through representative samples.
   - Pros: gives the system one source of truth while letting skill contracts
     stay concise and useful.
   - Cons: slower adoption; early coverage will be uneven.
3. Build validators and schemas first, then require every process to conform.
   - Pros: strongest long-term enforcement.
   - Cons: premature until the model has passed real skill/template examples.

Recommendation: use option 2. The tradeoff accepted is uneven early adoption in
exchange for a model that can mature before it becomes a validator requirement.

## ML-Course Framing

Harness engineering is analogous to learning a policy around a frozen or
semi-fixed model.

```text
Base model:
  y = M(c, x)

where:
  x = task
  c = context
  y = output
```

A harness is the policy that chooses the context, tools, memory, skills,
delegation, and verification around the model:

```text
H_theta(x, s) -> c
```

Where:

- `theta` is the harness configuration: prompts, skill contracts, routing
  rules, tool policy, memory policy, evals, budgets, and review gates.
- `x` is the current task.
- `s` is current harness state: files, memory, conversation, runtime state,
  tool availability, and prior evidence.
- `c` is the context handed to the model.

The full agent behavior becomes:

```text
y = M(H_theta(x, s), x)
```

And the harness state updates after evidence:

```text
s_{t+1} = U(s_t, x_t, y_t, e_t)
```

Where `e_t` is evidence from tests, evals, review, user feedback, telemetry, or
runtime traces.

## Harness Definition

The harness is the set of functions that mediate between a user task and the
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

Each component is itself a function:

```text
ContextBuilder(task, state) -> context
SkillSelector(task, state, registry) -> selected_skills
ToolPolicy(task, state, tool_registry) -> allowed_tools
MemoryPolicy(task, ledgers, retrieval_rule) -> memory_slice
DelegationPolicy(task, constraints) -> subagent_plan | none
VerificationPolicy(output, proof_contract) -> evidence
UpdatePolicy(harness, evidence, constraints) -> harness_delta | reject
BudgetPolicy(task, constraints) -> token_turn_time_budget
```

The harness is useful when these functions compose into reliable behavior for a
task distribution, not merely one prompt.

## Task Distribution

Optimization needs a task distribution, not a single anecdote:

```text
D = { task_i, expected_properties_i, constraints_i, evaluation_i }
```

Examples:

- coding tickets
- skill maintenance tasks
- review tasks
- eval-writing tasks
- research-to-ticket tasks
- user correction recovery tasks

Without a distribution `D`, an agent can overfit one case and call that
self-improvement.

## Reward And Objective Functions

Define the reward of a harness configuration against a task distribution:

```text
R(H_theta, D) =
  w_success * TaskSuccess(H_theta, D)
+ w_reliability * Reliability(H_theta, D)
+ w_reuse * ReuseTransfer(H_theta, D)
+ w_audit * Auditability(H_theta, D)
- w_cost * Cost(H_theta, D)
- w_latency * Latency(H_theta, D)
- w_turns * Turns(H_theta, D)
- w_context * ContextTokens(H_theta, D)
- w_dup * DuplicatedInstruction(H_theta)
- w_regression * RegressionRate(H_theta, D)
```

The constrained form is often safer than a single scalar:

```text
minimize:
  context_tokens
+ turns
+ latency
+ duplicated_instruction
+ maintenance_cost

subject to:
  task_success >= baseline
  reliability >= threshold
  safety_constraints pass
  review/eval/proof gates pass
  regression_rate <= threshold
  user_boundaries are respected
```

This is the cleaner version of the original prompt-size intuition:

> Minimize irrelevant context and coordination cost, subject to quality,
> reliability, safety, and proof constraints.

## Error Model

Prompt size alone is not the hallucination variable.

Better approximation:

```text
cost + latency ~= context_tokens + tool_calls + turns

error_risk ~= missing_context
           + noisy_context
           + contradictory_instructions
           + weak_verification
           + bad_tool_or_skill_selection
```

So the harness should not optimize for the shortest prompt. It should optimize
for the minimum sufficient context and proof loop.

## Harness Update Rule

The self-improvement loop is:

```text
1. choose task distribution D
2. choose current harness H_theta
3. run baseline score R(H_theta, D)
4. propose one bounded change delta_theta
5. evaluate H_{theta + delta_theta}
6. accept only if reward improves and constraints still pass
7. record accepted and rejected lessons
8. repeat until plateau, budget, or blocked condition
```

In notation:

```text
theta_{t+1} =
  theta_t + delta_theta_t  if Accept(delta_theta_t)
  theta_t                  otherwise
```

Where:

```text
Accept(delta_theta) :=
  R(H_{theta + delta_theta}, D_eval) > R(H_theta, D_eval)
  and constraints(H_{theta + delta_theta}) pass
  and heldout_regressions(H_{theta + delta_theta}) = 0
```

This is gradient-descent-like, but Farplane usually does not have smooth
gradients. It uses heuristic search over discrete harness changes:

```text
delta_theta in {
  edit skill prompt,
  move detail to reference,
  add eval case,
  change tool policy,
  add proof gate,
  adjust routing rule,
  improve memory retrieval,
  add or remove delegation
}
```

The gradient analogy is useful for teaching:

```text
loss(H) = bad_outputs + regressions + cost + drift

delta_theta points toward lower loss.
```

But the implementation is closer to coordinate descent, evolutionary search,
or autoresearch:

- change one bounded coordinate
- measure
- keep or reject
- preserve the evidence trail

## Original Intuition, Formalized

The original simple model:

```text
Codex = f(input_prompt) -> text_output
```

Becomes:

```text
output_n = M(context_n, task_n)
context_n = H_theta(task_n, state_n)
state_{n+1} = U(state_n, output_n, evidence_n)
```

The harness optimization goal:

```text
theta* = argmax_theta R(H_theta, D)
```

Or constrained:

```text
theta* = argmin_theta Cost(H_theta, D)
subject to Quality(H_theta, D) >= threshold
```

Skills are reusable variables inside `theta`; tools are action variables;
subagents are parallel branches; memory is persistent state; evals and review
are constraints/reward estimators.

## Core Types

```text
Artifact :=
  path
+ owner
+ schema_or_shape
+ lifecycle
+ proof_status
```

An artifact is a visible variable in the harness. Files, ticket sections,
registry rows, eval run JSON, review receipts, generated graphs, and memory
ledger rows are all artifacts.

```text
HarnessState :=
  FilesystemState
+ RuntimeState
+ MemoryState
+ ExternalState
+ ConversationState
```

The filesystem is the most important state carrier because it can survive chat
compaction and fresh agents. Runtime state and external state are real, but they
must be named explicitly because they are easier to lose or mutate
accidentally.

```text
Process<I, O> :=
  input: I
  read_set: Artifact[]
  transform: I + read_set -> O
  write_set: Artifact[]
  evidence: Evidence
  state_delta: HarnessState -> HarnessState
```

Processes should be judged by whether another agent can replay or audit this
contract from repo files alone.

## Harness Primitives As Functions

### Skill

```text
Skill<I, O> :=
  Process<
    OperatorIntent + RequiredContext + Artifacts,
    ChatOutput | ArtifactOutput | HandoffOutput
  >
```

A skill is not just a prompt. A skill is a reusable function contract with:

- trigger conditions
- required context
- first-load todo list
- optional references, scripts, templates, and tools
- expected outputs
- proof obligations
- composition hints

### Eval

```text
Eval<Candidate, Verdict> :=
  Process<
    Candidate + TestCases + JudgeOrAssertions,
    Verdict + Score + EvidenceArtifacts
  >
```

An eval is a function from a candidate behavior or artifact to a verdict. Good
evals make the judge inputs, task cases, output shape, and failure evidence
explicit.

### Meta-Skill

```text
MetaSkill<SystemSurface, Change> :=
  Process<
    SystemSurface + ImprovementGoal + MetricOrRubric,
    Proposal | Patch | Ticket | ReviewArtifact
  >
```

Meta-skills operate on the harness itself. Examples include `skill-maintenance`,
`harness-advisor`, `self-improve`, `eval`, and `repent`.

### Hook

```text
Hook<Event, Decision> :=
  Process<
    Event + RuntimeState + VisibleArtifacts,
    GateDecision + Telemetry + OptionalHandoff
  >
```

Hooks should remain deterministic boundary functions. They can observe, block,
route, record, or hand off. They should not hide broad judgment or become a
background autonomy brain.

### Memory Drain

```text
MemoryDrain<RawLedger, DurableOutcome> :=
  Process<
    RawSignals + ExistingMemory + CurrentSpecs,
    Lessons | MemoryRules | Tickets | ArchiveActions
  >
```

Drain functions turn raw signals into smaller durable variables. They should
promote only the smallest rule, ticket, eval, or archive action needed.

### Ticket

```text
Ticket :=
  Task
+ Plan
+ ProofContract
+ AgentContract?
+ Evidence
+ State
```

A ticket is a work-package function waiting to execute. It defines the inputs,
expected state transition, proof function, and closeout path for one coherent
build loop.

## Composition Rules

### Sequential Composition

```text
B after A := B(A(input))
```

Sequential composition is valid when `A.output` satisfies `B.input` and the
artifact written by `A` is readable by `B`.

Example:

```text
reference-grounding -> advise -> harness-advisor -> ticket
```

### Parallel Composition

```text
A || B := Merge(A(input), B(input))
```

Parallel composition is valid only when the write sets do not conflict or when
there is an explicit merge function and proof surface.

Parallel work must name:

- independent read sets
- independent write sets
- merge owner
- integration proof
- rollback or conflict policy

### Transitive Composition

```text
if C depends on B and B depends on A, then C transitively depends on A
```

This is why lower-level skill improvements can compound. If `advise` improves,
every downstream process that depends on `advise` should be eligible for
rerun, regression checks, or score comparison.

### Fixed-Point Improvement

```text
H_{n+1} = Improve(H_n)
stop when Score(H_{n+1}) <= Score(H_n) or constraints fail
```

Self-improvement is a bounded search for a better harness state. It must have
a metric or rubric, guard checks, rollback or rejection rules, and a clear stop
condition.

## Process-Level Optimization Objective

At the process level, Farplane should still use Pareto reasoning instead of one
fake scalar. This is the implementation-facing version of the reward model
above:

```text
maximize:
  task_success
+ downstream_transfer
+ reuse
+ auditability

minimize:
  context_tokens
+ turns
+ duplicated_instruction
+ latency
+ regression_rate
+ maintenance_cost

subject to:
  safety_constraints
  proof_contract
  user_boundaries
  no hidden state
```

This turns the original prompt-size intuition into a safer rule:

> Find the minimum sufficient context and artifact contract that preserves or
> improves local and downstream behavior.

## Files As Variables

The filesystem is Farplane's main variable store.

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

A file should not merely exist; it should have an owner, a reason to be read,
and a known lifecycle. Weak harness behavior often comes from implicit
variables: files that agents write but later agents do not know to read, trust,
drain, or delete.

When a process writes a file, the process should name:

- the artifact path
- the shape or schema
- the intended readers
- the proof command or review surface
- whether the file is durable, runtime-only, generated, experimental, or
  archival

## Skill Function Contract

Use a compact `## Function Contract` in `SKILL.md` when a skill benefits from a
formal contract. Put it near the top, after `## Context` and before
`## Todo List`, so it informs execution without burying the first-load
checklist.

Recommended shape:

```text
## Function Contract

`skill_name: Inputs -> Outputs`

Inputs:
- operator intent:
- required context:
- readable artifacts:
- optional tools:

Outputs:
- primary response or artifact:
- write set:
- evidence:

Composition:
- upstream:
- downstream:
- transitive effects:
```

Do not add a function contract when it would only restate the todo list. Use it
when it clarifies inputs, outputs, files, method composition, eval boundaries,
or downstream reuse.

## Rollout

Start with representative high-leverage surfaces:

1. `advise`, `reference-grounding`, `plan`, `execute`, and `review`.
2. Meta-skills: `harness-advisor`, `skill-maintenance`, `skill-creator`,
   `self-improve`, `eval`, and `repent`.
3. One complex Tier 3 domain skill with methods and templates, such as
   `landing-page` or `frontend-craft`.
4. Ticket template and proof contract refinements if the sample proves useful.
5. Validator or registry fields only after the function-contract shape catches
   real failures.

Do not bulk-edit every skill before a representative sample proves the format.

## Open Questions

- Which parts of `Function Contract` should become template-required versus
  optional on-contact guidance?
- Should generated skill graph tooling derive inputs and outputs from the
  function contract, frontmatter, or separate fixtures?
- What is the smallest useful schema for `Artifact`, `EvalCase`, and
  `Process` without creating bureaucracy?
- Which metric best captures compounding ROI: success per context token,
  downstream pass-rate delta, reduced turns, fewer user corrections, or a
  Pareto frontier over all of them?

## Next Ticket Shape

The next implementation ticket should:

- add this spec to the README and spec index
- add `Function Contract` guidance to skill authoring docs and the skill
  template
- define a representative sample of skills for contract onboarding
- avoid a full registry-wide migration until the sample is reviewed
- decide whether a future validator should check only shape, only presence, or
  semantic consistency
