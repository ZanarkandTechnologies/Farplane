# Advise Budget Example

This toy example shows how `budget-advisor` resolves budget params for
`advise`.

Important boundary: `advise` stays the simple base skill. It takes a decision,
compares exactly three viable options when three exist, recommends one, names
the accepted tradeoff, and names the next step. Budget fields, persona prompts,
child budget allocation, and synthesis belong to `budget-advisor` and the
caller's resolved Budget Program, not to `advise/SKILL.md`.

Base `advise` output contract:

```text
Decision
Options: exactly 3 viable options when three exist
Recommendation: one clear recommendation
Tradeoff accepted
Next step
```

## Base Call

```text
advise(decision, budget={mode:"base"})
```

Program:

```text
run advise base program
use the caller's normal material review gates when the decision note is material
return final advice output
```

## Plus Persona Council

```text
advise(decision, budget={
  mode: "plus",
  personas: [
    {
      name: "Operator ergonomics",
      prompt: "You are optimizing for the operator experience. Focus on whether the interface is memorable, easy to invoke, and avoids making simple advice feel bureaucratic.",
      focus: ["operator memory", "friction", "syntax"],
      avoid: ["abstract taxonomy"],
      output_shape: "Best option, tradeoff, operator-facing risk, next step"
    },
    {
      name: "Skill-system maintainer",
      prompt: "You maintain the Farplane skill system. Focus on source ownership, duplicate logic, eval/proof surface, and avoiding root-prompt bloat.",
      focus: ["ownership", "duplication", "proof"],
      avoid: ["new global rules before proof"],
      output_shape: "Best option, owner-surface risk, proof needed, next step"
    },
    {
      name: "Evidence skeptic",
      prompt: "You are testing whether the recommendation is actually supported. Focus on missing evidence, false confidence, and the behavior test or eval that would change the decision.",
      focus: ["evidence gap", "failure mode", "testability"],
      avoid: ["generic caution"],
      output_shape: "Best option, weakest assumption, evidence gap, next step"
    }
  ]
})
```

Budget advisor returns:

```text
source_refs:
  - skills/budget-advisor/SKILL.md
  - skills/budget-advisor/references/ensemble-lanes.md
template_ref: skills/budget-advisor/references/ensemble-lanes.md
mode: plus
persona_count: 3
synthesis: synthesize
child_budget_policy: child skills use base unless delegate_budget names them
```

Program:

```text
require complete persona prompts
run one advice lane per persona
synthesize into the normal advise output
preserve meaningful dissent and evidence gaps
```

## Max Persona Council

```text
advise(decision, budget={
  mode: "max",
  personas: [OperatorValue, EngineeringRisk, EvidenceSkeptic, SystemsFit, Chair]
})
```

Program:

```text
run five independent advice lanes with complete prompts
synthesize strongest ideas, dissent, risks, and evidence gaps
return one normal advise output
use the caller's material review gate on the final note
```

## Child Skill Default

```text
deliberative_advice(decision, budget={mode:"max"})
  -> budget-advisor resolves the deliberative council
  -> any child reference-grounding or review call uses base unless:

delegate_budget: {
  "reference-grounding": { mode: "plus", personas: [...] }
}
```

This prevents a high-level budget from multiplying every nested call.

## Deliberative Advice Preset

`deliberative-advice` can be represented as a named preset over `advise`, while
remaining useful as a user-facing wrapper:

```text
deliberative_advice(decision, personas?)
  = advise(decision, budget={
      mode: "max",
      personas: personas or default_personas
    })
```

The wrapper remains valuable because users remember "deliberative advice"
better than a full budget object.
