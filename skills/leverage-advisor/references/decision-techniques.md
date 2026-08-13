---
template_id: skill-method-reference
template_version: "0.1.0"
consumer_scope: skill-reference
applies_to:
  - skills/leverage-advisor/references/decision-techniques.md
template_uses:
  skill-method-reference: "0.1.0"
---

# Decision Techniques

Load this reference when a leverage decision is material, outcome uncertainty
is high, or the evidence plan could spend meaningful time, money, or attention.
It anchors three named methods without replacing the normal first-load contract
or becoming a book summary.

```text
decision_record(frontier, objective, evidence)
  -> diagnosis + policy + bet_thesis + decision_changing_test + replan_rule
state: reads(grounded subject, objective, constraints, candidate frontier,
             evidence); writes(leverage-plan decision record only)
gates: bottleneck_named; pre_outcome_thesis_named; test_changes_decision
fails: numeric-score theater; book-summary substitution; outcome-resulting;
       easy but non-decisive measurement
```

## Use When

- The choice is material, outcome uncertainty is high, or the evidence plan
  spends meaningful time, money, or attention.
- The normal leverage frontier is known, but the reason to choose one move or
  test needs a more disciplined decision record.

## Inputs

```text
decision_techniques_input:
  required:
    objective:
    grounded_subject:
    candidate_frontier:
    current_evidence:
  optional:
    constraints:
    prior_outcome_or_progress:
  source_refs:
    - current evidence references
    - source links below
```

## Workflow

1. **Diagnose the obstacle.** Identify the evidence-supported constraint that
   limits the objective, then state a policy that excludes distractor moves.
2. **Pre-commit the bet.** State what must be true, downside, and falsifier
   before seeing a result; use a confidence range only when evidence permits.
3. **Design decisive evidence.** Choose the smallest observation whose positive
   and negative outcomes produce different next actions; reject every test that
   cannot alter the decision.

## Output Shape

```text
decision_techniques_output:
  diagnosis:
  guiding_policy:
  coherent_move:
  bet_thesis:
  confidence_range_or_uncalibrated:
  downside:
  falsifier:
  decision_changing_test:
  decision_if_positive:
  decision_if_negative:
  source_refs:
```

## Quality Gates

- Every field traces to the active objective and grounded evidence, not a book
  label or generic ambition.
- Positive and negative test outcomes change the next action; otherwise the
  test is rejected as non-decisive.
- The record evaluates later outcomes against its pre-outcome thesis rather
  than claiming that success proves skill or failure proves error.

## Bad Output

- A reading list or book recap with no diagnosis, bet thesis, or test.
- A confidence percentage that has no calibrated evidence.
- A survey, dashboard, or metric collected despite both outcomes yielding the
  same next move.

## Adopted Techniques

| Method | Transferable technique | Required decision artifact | Source |
| --- | --- | --- | --- |
| Richard Rumelt — *Good Strategy/Bad Strategy* | Diagnose the critical obstacle, choose a guiding policy, then make coherent action rather than treating an ambition as strategy. | `diagnosis`, `guiding_policy`, `coherent_move` | [Publisher page](https://www.penguinrandomhouse.com/books/208668/good-strategy-bad-strategy-by-richard-rumelt/) |
| Annie Duke — *Thinking in Bets* | Treat a choice under uncertainty as a bet; assess the decision from its pre-outcome reasoning instead of resulting from luck. | `thesis`, `confidence_range_or_uncalibrated`, `downside`, `falsifier` | [Author page](https://www.annieduke.com/thinking-in-bets-2/) · [publisher page](https://www.penguinrandomhouse.com/books/552885/thinking-in-bets-by-annie-duke/) |
| Douglas Hubbard — *How to Measure Anything* | Measure the uncertainty whose reduction can change the decision; prefer the smallest useful observation over indiscriminate data collection. | `decision_changing_test`, `decision_if_positive`, `decision_if_negative` | [Wiley overview](https://onlinelibrary.wiley.com/doi/book/10.1002/9781118983836) · [value-of-information chapter](https://onlinelibrary.wiley.com/doi/abs/10.1002/9781118983836.ch7) |

## Decision Record

For a material choice, render these fields in the leverage plan:

```text
Diagnosis:
  Critical obstacle or constraint supported by current evidence.
Guiding policy:
  The principle that narrows which moves are eligible now.
Coherent move:
  The next move that follows from the policy.
Bet thesis:
  What must be true for this move to create the expected leverage.
Confidence range or uncalibrated:
  A calibrated qualitative or numeric range only when evidence supports one.
Downside:
  What is lost if the thesis is false, including time, capital, and option loss.
Falsifier:
  Observation that makes the move no longer preferred.
Decision-changing test:
  Cheapest honest observation whose positive and negative results lead to
  different actions. If neither branch changes the action, do not run it.
If positive -> next action:
  The bounded action justified by a confirming result.
If negative -> next action:
  The bounded action justified by a disconfirming result.
```

## Adoption Boundaries

- These techniques improve the decision record; they do not introduce a numeric
  score, a new selection algorithm, or a guarantee about outcomes.
- Use ordinal judgement for the frontier. Report confidence as a range only
  when the evidence can support calibration; otherwise state `uncalibrated`.
- A failed bet does not alone prove a poor decision. Compare the observed result
  with the pre-committed thesis, falsifier, and alternative explanations before
  replanning.
- A test is valuable only if its result can alter selection, spending, scope,
  or the outside option. Collect no metric merely because it is easy.
- These are source-attributed adaptations, not excerpts or substitutes for the
  original books.
