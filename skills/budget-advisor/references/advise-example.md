# Advise Budget Example

This toy example shows how `budget-advisor` resolves budget params for
`advise`.

Base `advise` output contract:

```text
Decision
Options: exactly 3 viable options
Recommendation: one clear recommendation
Tradeoff accepted
Next step
```

## Base Call

```text
advise(decision)
```

Program:

```text
frame decision
name criteria
compare exactly 3 viable options
recommend 1
name tradeoff
name next step
```

## Review Depth

```text
advise(decision, budget={review_depth: 2})
```

Budget advisor returns:

```text
template_ref: skills/budget-advisor/references/review-depth.md
review_depth: 2
review_route: self-check or review protocol depending on stakes
```

Program:

```text
result = advise_base(decision)
review result
revise result
review result
revise result
return final advice output
```

## Same-Perspective Ensemble

```text
advise(decision, budget={
  ensemble: {
    count: 5,
    perspective_mode: "same",
    aggregation: "synthesize"
  }
})
```

Budget advisor returns:

```text
source_refs:
  - skills/budget-advisor/SKILL.md
  - skills/budget-advisor/references/ensemble-lanes.md
template_ref: skills/budget-advisor/references/ensemble-lanes.md
count: 5
perspective_mode: same
aggregation: synthesize
```

Program:

```text
run five independent advice passes with the same prompt
synthesize the best option framing, evidence gaps, dissent, and next step
return one normal advise output
```

## Different-Perspective Ensemble

```text
advise(decision, budget={
  ensemble: {
    count: 4,
    perspective_mode: "different",
    personas: [
      {
        name: "Operator value",
        prompt: "You are optimizing for the operator's time, taste, leverage,
        and opportunity cost. Identify which option makes the user's future
        work easier, where extra ceremony would be annoying, and what next
        action would create momentum without overbuilding.",
        focus: ["operator happiness", "speed to useful outcome", "taste"],
        avoid: ["abstract architecture for its own sake"],
        output_shape: "Best option, tradeoff, operator-facing risk, next step"
      },
      {
        name: "Engineering risk",
        prompt: "You are reviewing implementation and maintenance risk. Focus
        on dependency cost, migration risk, unclear ownership, brittle
        abstractions, and proof requirements. Prefer the smallest durable
        surface that can work.",
        focus: ["maintenance", "ownership", "blast radius", "proof"],
        avoid: ["generic caution"],
        output_shape: "Best option, failure mode, proof needed, next step"
      }
    ],
    aggregation: "synthesize"
  }
})
```

Program:

```text
require complete persona prompts
run one advice lane per persona
synthesize into the normal advise output
preserve meaningful dissent
```

## Large Ensemble

```text
advise(decision, budget={
  ensemble: {
    count: 40,
    perspective_mode: "different",
    personas: [...],
    aggregation: "hierarchical_synthesis",
    tournament: { group_size: 4 }
  },
  review_depth: 1
})
```

Budget advisor returns:

```text
source_refs:
  - skills/budget-advisor/SKILL.md
  - skills/budget-advisor/references/tournament-aggregation.md
  - skills/budget-advisor/references/review-depth.md
template_ref: skills/budget-advisor/references/tournament-aggregation.md
count: 40
group_size: 4
aggregation: hierarchical_synthesis
then: skills/budget-advisor/references/review-depth.md
review_depth: 1
```

Program:

```text
run 40 advice lanes
group by 4
synthesize each group into best ideas, dissent, gaps, and candidate answer
synthesize group summaries into one normal advise output
review final once
return final advice output
```

## Deliberative Advice Preset

`deliberative-advice` can be represented as a named preset over `advise`, while
remaining useful as a user-facing wrapper:

```text
deliberative_advice(decision, personas?)
  = advise(decision, budget={
      budget_mode: "deep",
      ensemble: {
        count: len(personas or default_personas),
        perspective_mode: "different",
        personas: personas or default_personas,
        aggregation: "synthesize"
      },
      review_depth: 1
    })
```

The wrapper remains valuable because users remember "deliberative advice"
better than a full budget object.
