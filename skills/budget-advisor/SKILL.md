---
name: budget-advisor
description: "Resolve a budget-aware skill call into a base reviewed path plus optional persona-council lanes when effort changes workflow shape."
tier: 2
source: local
template_uses:
  skill-template: "0.3.0"
  skill-eval-task: "0.2.0"
eval: evals/evals.json
allowed-tools: Read, Glob, Grep

---

# Budget Advisor

## Context

`budget-advisor` is a reusable workflow interface for skills that expose an
optional `budget` parameter. It does not run subagents, review artifacts, or
own another skill's domain logic. It turns a budget request into a concrete
program that the caller can execute while preserving the original skill's
output contract.

Every material skill already has a base reviewed path: the main agent makes or
uses a plan, a peer reviews the plan to TAS A or no material findings, the
caller executes, and the work/output receives a peer review to TAS A before a
material completion claim. Budget does not decide whether review exists. Budget
decides whether to add independent persona perspectives above that base path.

Use it when a budget-aware skill receives a request such as `base`, `plus`,
`max`, `persona_count`, `personas`, available time/cost, or an explicit child
skill budget allocation, and the caller needs to know which execution program
to follow.

## Skill Signature

```text
budget_advisor(skill_contract, skill_input, budget_request, context?)
  -> budget_program + template_refs + resolved_params + guardrails
state: reads(skill contract, budget request, relevant context packet?); writes(none by default)
gates: output_contract_preserved; base_reviewed_path_preserved; persona_prompts_specific; child_budget_not_inherited_by_default
routes: caller-owned skill | review | best-of-worlds | agent-qa-test | goal-advisor
fails: vague "try harder"; thin perspective labels; budget-as-no-review; recursive budget fanout; hidden subagent orchestration
```

Budget-aware skills should keep their normal signature:

```text
skill(input, context?, budget?) -> output + evidence? + state_delta?
```

When `budget` is present, the caller may invoke `budget-advisor` to resolve the
budget into a concrete program. The caller still executes the program and owns
the final output.

## Budget Request Shape

Use only the fields that matter for the current skill. Do not add all fields to
every budget-aware skill.

```text
BudgetRequest = {
  mode?: "base" | "plus" | "max",
  available_time?: string,
  persona_count?: 1 | 3 | 5,
  personas?: PersonaPrompt[],
  coverage?: "smoke" | "focused" | "broad",
  evidence_depth?: "light" | "strong",
  delegate_budget?: Record<skill_name, BudgetRequest>
}
```

`base` is the default reviewed skill path, not "no budget". `plus` adds a small
diverse council when the skill benefits from independent perspectives. `max`
uses a bounded five-persona council plus synthesis; it is not unbounded fanout,
large-batch sampling, or repeated clones of the same action.

Do not normalize `base` to an unreviewed route. Budget Programs must use only
the current public fields: `mode`, `persona_count`, `personas`, `synthesis`,
and `child budget policy`.

Child skills inherit `base` unless `delegate_budget` explicitly allocates more
budget to a named child skill. This prevents a high-level council from
accidentally multiplying every nested skill call.

`PersonaPrompt` must be a complete role/perspective prompt, not a two-word
label:

```text
PersonaPrompt = {
  name: string,
  prompt: string,
  focus: string[],
  avoid?: string[],
  output_shape?: string
}
```

<!-- BEGIN FARPLANE_IMPORTANT_CHECKLIST -->
## Todo List

- [ ] 1. Bind the budget request and caller skill contract.
   - [ ] Identify the caller skill's output contract, base reviewed path,
     supported budget fields, and any domain-provided persona prompts.
   - [ ] Treat missing `mode` as `base` unless the user's effort phrase or
     available time clearly asks for `plus` or `max`.
- [ ] 2. Choose the budget route.
   - [ ] `base_reviewed`: call the caller skill's normal reviewed path; do not
     remove plan/work review for material work, and state this explicitly in
     the Budget Program.
   - [ ] `persona_council`: use
     [ensemble-lanes](references/ensemble-lanes.md) when `plus`, `max`, or
     `persona_count` asks for independent perspectives.
   - [ ] `mode_or_time_mapping`: use
     [budget-modes](references/budget-modes.md) when the caller provided
     available time, cost, or an effort phrase.
   - [ ] `delegate_budget`: pass extra budget to child skills only when the
     request explicitly names that child skill.
- [ ] 3. Resolve missing parameters conservatively.
   - [ ] If persona lanes are used, require complete persona prompts from the
     caller skill, user, or context; otherwise return a blocker and state that
     the caller can still use the base reviewed path without persona lanes.
   - [ ] If `persona_count` is missing, default `base -> 1`, `plus -> 3`, and
     `max -> 5`, capped by the number of complete useful persona prompts.
   - [ ] Prefer different perspectives over repeated clones unless sampling
     variance is the explicit reason for extra budget.
- [ ] 4. Return a concrete budget program.
   - [ ] Include ordered steps, template refs, resolved params, expected
     artifacts, synthesis rule, stop condition, and child-budget inheritance.
   - [ ] Include an explicit `child budget policy` line for every program:
     child skills use base unless `delegate_budget` names them.
   - [ ] Include `skills/budget-advisor/SKILL.md` plus every loaded reference
     file in `source_refs`.
   - [ ] When persona lanes are used, copy the complete `PersonaPrompt` objects
     into `resolved_params`; do not summarize them in the executable program.
   - [ ] State how the final output must preserve the caller skill's output
     contract.
- [ ] 5. Review before completion.
   - [ ] No hidden subagent execution is implied by the advisor result.
   - [ ] Every referenced template is specific enough for the caller to follow.
   - [ ] Persona prompts are concrete when persona lanes are used.
   - [ ] Synthesis preserves the strongest ideas, dissent, risks, evidence
     gaps, and the caller skill's final output contract.
<!-- END FARPLANE_IMPORTANT_CHECKLIST -->

## Core Rules

- Budget resolution returns instructions; it does not execute them.
- The caller skill owns domain-specific persona defaults, output format, proof,
  and final answer quality.
- `budget-advisor` owns reusable budget routes, persona-count defaults,
  synthesis defaults, and guardrails against vague effort escalation.
- Preserve the caller skill's output contract. A budgeted `advise` still
  returns advice; a budgeted `review` still returns a review verdict.
- Preserve executable lane prompts. The Budget Program may summarize why a
  persona exists, but `resolved_params` must keep the full `PersonaPrompt`
  object so a later agent can run the lane without rediscovering the prompt.
- Use one public synthesis concept: `synthesize`. Internally, synthesis may
  score, group, or choose when the caller's output contract requires it, but
  those are implementation details rather than user-facing modes.
- Do not spawn several agents to perform the same action unless variance is the
  explicit goal. Diverse personas usually buy more value than cloned lanes.
- A high-level budget does not copy to child skills by default. Child skills run
  their own base reviewed path unless `delegate_budget` explicitly names them.
- If `plus` or `max` lacks complete `PersonaPrompt` objects and the caller skill
  has no defaults, do not fall back to same-prompt clones. Return a blocker for
  persona lanes and name `base_reviewed` as the executable fallback.
- Every Budget Program, including `base_reviewed`, must state that
  `budget-advisor` itself does not spawn agents, execute lanes, review outputs,
  or edit files; the caller skill owns execution.

## Reference Map

- [budget-modes](references/budget-modes.md) - map available time and vague
  effort requests to `base`, `plus`, or `max`.
- [ensemble-lanes](references/ensemble-lanes.md) - run persona council lanes
  with full persona prompts and a single public synthesis step.
- [advise-example](references/advise-example.md) - toy example showing how
  `advise` evolves under base, plus, max, and child-budget defaults.

## Output

Return:

```text
Budget Program:
- caller skill:
- budget route:
- template refs:
- source refs:
- resolved params:
- steps:
- synthesis:
- output contract:
- child budget policy:
- stop condition:
- guardrails:
- blockers:
```

The `guardrails` block must include:

```text
- Budget Advisor returns this program only; it does not spawn agents, execute
  lanes, review outputs, or edit files.
```
