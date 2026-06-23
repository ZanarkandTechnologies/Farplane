---
name: budget-advisor
description: "Resolve a budget-aware skill call into concrete execution template refs, parameters, and guardrails when effort changes workflow shape."
tier: 2
source: local
template_uses:
  skill-template: "0.3.0"
  skill-eval-task: "0.1.0"
eval: eval_task.json
allowed-tools: Read, Glob, Grep

---

# Budget Advisor

## Context

`budget-advisor` is a reusable workflow interface for skills that expose an
optional `budget` parameter. It does not run subagents, review artifacts, or
own another skill's domain logic. It turns a budget request into an intuitive
program that the caller can execute while preserving the original skill's
output contract.

Use it when a budget-aware skill receives parameters such as `review_depth`,
`ensemble`, `lanes`, `coverage`, `budget_mode`, or available time/cost, and the
caller needs to know which execution template to follow.

## Skill Signature

```text
budget_advisor(skill_contract, skill_input, budget_request, context?)
  -> budget_program + template_refs + resolved_params + guardrails
state: reads(skill contract, budget request, relevant context packet?); writes(none by default)
gates: output_contract_preserved; templates_named; recursion_bounded; persona_prompts_specific
routes: caller-owned skill | review | best-of-worlds | agent-qa-test | goal-advisor
fails: vague "try harder"; thin perspective labels; recursive budget expansion; hidden subagent orchestration
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
  budget_mode?: "none" | "light" | "normal" | "deep" | "max",
  available_time?: string,
  review_depth?: 0 | 1 | 2 | 3,
  ensemble?: {
    count: number,
    perspective_mode?: "same" | "different",
    personas?: PersonaPrompt[],
    aggregation?: "synthesize" | "score_then_synthesize" | "select" | "hierarchical_synthesis",
    tournament?: { group_size: number }
  },
  coverage?: "smoke" | "focused" | "broad",
  evidence_depth?: "none" | "light" | "strong",
  max_budget_depth?: 0 | 1
}
```

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
   - [ ] Identify the caller skill's output contract, base phases, supported
     budget fields, and any domain-provided persona prompts.
   - [ ] Set `max_budget_depth`; default to `0` for subskill calls and `1` only
     when the caller explicitly allows one budget expansion.
- [ ] 2. Choose the budget route.
   - [ ] 1. `none_or_base`: no template; call the base skill directly.
   - [ ] 2. `review_depth`: use
     [review-depth](references/review-depth.md) when review passes are requested.
   - [ ] 3. `ensemble_lanes`: use
     [ensemble-lanes](references/ensemble-lanes.md) when `ensemble.count` is set.
   - [ ] 4. `large_ensemble`: use
     [tournament-aggregation](references/tournament-aggregation.md) when the
     ensemble is too large for one flat synthesis.
   - [ ] 5. `mode_or_time_mapping`: use
     [budget-modes](references/budget-modes.md) when the caller provided only
     `budget_mode`, available time, cost, or an effort phrase.
- [ ] 3. Resolve missing parameters conservatively.
   - [ ] If `perspective_mode: different`, require complete persona prompts from
     the caller skill, user, or context; otherwise return a blocker or a
     request to use a default persona set owned by the caller skill.
   - [ ] If aggregation is missing, default to `synthesize` for small ensembles
     and `hierarchical_synthesis` for large ensembles.
   - [ ] If a scoring function is missing, do not use pure `select`; use
     synthesis or ask for a rubric.
- [ ] 4. Return a concrete budget program.
   - [ ] Include ordered steps, template refs, resolved params, expected
     artifacts, aggregation method, stop condition, and recursion guard.
   - [ ] Include `skills/budget-advisor/SKILL.md` plus every loaded reference
     file in `source_refs`.
   - [ ] When persona lanes are used, copy the complete `PersonaPrompt` objects
     into `resolved_params`; do not summarize them in the executable program.
   - [ ] State how the final output must preserve the caller skill's output
     contract.
- [ ] 5. Review before completion.
   - [ ] No hidden subagent execution is implied by the advisor result.
   - [ ] Every referenced template is specific enough for the caller to follow.
   - [ ] Persona prompts are concrete when different-perspective lanes are used.
   - [ ] Large-N aggregation names scoring and synthesis behavior explicitly.
<!-- END FARPLANE_IMPORTANT_CHECKLIST -->

## Core Rules

- Budget resolution returns instructions; it does not execute them.
- The caller skill owns domain-specific persona defaults, output format, and
  final answer quality.
- `budget-advisor` owns reusable budget routes, template refs, aggregation
  defaults, and guardrails against vague effort escalation.
- Preserve the caller skill's output contract. A budgeted `advise` still
  returns advice; a budgeted `review` still returns a review verdict.
- Preserve executable lane prompts. The Budget Program may summarize why a
  persona exists, but `resolved_params` must keep the full `PersonaPrompt`
  object so a later agent can run the lane without rediscovering the prompt.
- Prefer synthesis over winner-take-all selection unless the caller supplies a
  clear scoring rubric and selection rule.
- Large ensembles should use hierarchical aggregation to reduce context load,
  not pretend that bracket winners are the only valuable outputs.

## Reference Map

- [budget-modes](references/budget-modes.md) - map `budget_mode`, available
  time, and vague effort requests to concrete fields.
- [review-depth](references/review-depth.md) - repeat a caller skill's review
  phase or external review step.
- [ensemble-lanes](references/ensemble-lanes.md) - run same or
  different-perspective lanes with full persona prompts.
- [tournament-aggregation](references/tournament-aggregation.md) - aggregate
  large ensembles through grouped synthesis, scoring, or selection.
- [advise-example](references/advise-example.md) - toy example showing how
  `advise` evolves under review depth, small ensembles, and large ensembles.

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
- aggregation:
- output contract:
- stop condition:
- guardrails:
- blockers:
```
