# Ensemble Lanes Template

Use this template when `ensemble.count` is set and the requested count can be
handled in one flat aggregation pass.

Ensemble spends budget on the caller skill's act phase. Each lane runs the
caller skill's base act phase independently, then the caller aggregates lane
outputs back into the original skill output contract.

## Inputs

```text
ensemble.count: number
ensemble.perspective_mode: "same" | "different"
ensemble.personas?: PersonaPrompt[]
ensemble.aggregation: "synthesize" | "score_then_synthesize" | "select"
caller_skill:
skill_input:
context_ref?:
output_contract:
```

## Persona Prompt Contract

Different-perspective lanes require complete persona prompts.

Good:

```text
name: "Evidence skeptic"
prompt: "You are an evidence skeptic reviewing this decision. Focus on claims
that depend on stale facts, unsupported assumptions, weak local evidence, or
scope mismatch. Do not optimize for novelty. Return the strongest reason to
hold, the evidence that would change your mind, and one concrete risk-reducing
next step."
focus:
  - unsupported claims
  - missing evidence
  - false confidence
avoid:
  - generic caution
  - repeating the base recommendation
output_shape: "Findings, dissent, evidence gap, next step"
```

Bad:

```text
"skeptic"
```

Two-word labels lose value because lanes need enough prompt context to think
along a specific axis while staying isolated from other lanes.

## Program: Same Perspective

```text
lane_outputs = []

for i in 1..ensemble.count:
  lane_outputs += run caller skill act phase with the same prompt and context

final = aggregate lane_outputs using ensemble.aggregation
return final in caller skill output contract
```

Use same-perspective lanes when sampling variance is useful and the caller does
not need role diversity.

## Program: Different Perspectives

```text
require complete PersonaPrompt for each lane
write or identify context_ref when prior context matters
copy complete PersonaPrompt objects into resolved_params.personas

for persona in ensemble.personas:
  lane_prompt = context_ref + persona.prompt + caller skill output contract
  lane_outputs += run isolated lane

final = aggregate lane_outputs using ensemble.aggregation
return final in caller skill output contract
```

Use different-perspective lanes when the task benefits from independent axes,
such as operator value, implementation risk, evidence skepticism, or systems
fit.

## Aggregation Choices

```text
synthesize
  -> combine complementary strengths and preserve important dissent
```

```text
score_then_synthesize
  -> score each candidate with a supplied rubric, keep the strongest ideas, and
     synthesize a final answer
```

```text
select
  -> choose one candidate only when the caller supplied a clear scoring
     function and a single winner is useful
```

For LLM advice, planning, and review, prefer synthesis over pure selection
because candidates often contain complementary useful pieces.

## Output Fragment

```text
ensemble_lanes_program:
  template_ref: skills/budget-advisor/references/ensemble-lanes.md
  source_refs:
    - skills/budget-advisor/SKILL.md
    - skills/budget-advisor/references/ensemble-lanes.md
  count:
  perspective_mode:
  personas: complete PersonaPrompt objects, not summaries
  context_ref:
  aggregation:
  final_output_contract:
```
