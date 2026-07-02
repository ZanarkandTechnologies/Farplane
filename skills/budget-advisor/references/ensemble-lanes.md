# Persona Council Lanes

Use this template when `mode: plus`, `mode: max`, `persona_count`, or complete
`personas` asks for independent perspectives above the caller skill's base
reviewed path.

Persona councils spend budget on perspective coverage. Each lane runs the
caller skill's act or judgment phase independently, then the caller synthesizes
lane outputs back into the original skill output contract.

## Inputs

```text
persona_count: 1 | 3 | 5
personas: PersonaPrompt[]
caller_skill:
skill_input:
context_ref?:
output_contract:
synthesis: "synthesize"
```

## Persona Prompt Contract

Persona lanes require complete prompts.

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

## Program

```text
require complete PersonaPrompt for each lane
write or identify context_ref when prior context matters
copy complete PersonaPrompt objects into resolved_params.personas

for persona in selected personas:
  lane_prompt = context_ref + persona.prompt + caller skill output contract
  lane_outputs += run isolated lane

final = synthesize lane_outputs into caller skill output contract
return final in caller skill output contract
```

Use different-perspective lanes when the task benefits from independent axes,
such as operator value, implementation risk, evidence skepticism, systems fit,
or proof burden.

Use same-prompt clones only when sampling variance is explicitly the goal. Most
Farplane planning, advice, and review work should buy diverse coverage instead
of repeated copies of the same action.

## Synthesis

`synthesize` is the only public synthesis mode:

```text
synthesize(lane_outputs, output_contract)
  -> final output that preserves best ideas, meaningful dissent, risks,
     evidence gaps, accepted tradeoffs, and the caller skill's required shape
```

When a rubric exists, synthesis may score internally. When the caller's output
contract requires one answer, synthesis may choose internally. When context is
large, synthesis may group internally. These are implementation strategies, not
operator-facing budget choices.

## Output Fragment

```text
persona_council_program:
  template_ref: skills/budget-advisor/references/ensemble-lanes.md
  source_refs:
    - skills/budget-advisor/SKILL.md
    - skills/budget-advisor/references/ensemble-lanes.md
  count:
  personas: complete PersonaPrompt objects, not summaries
  context_ref:
  synthesis: synthesize
  child_budget_policy: child skills use base unless delegate_budget names them
  final_output_contract:
```
