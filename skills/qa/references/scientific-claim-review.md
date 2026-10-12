# Scientific Claim Review

Load from [adversarial mode](adversarial.md) only when an experimental
observation materially violates a preregistered expectation, or supports a
high-impact conclusion. Experiment design and preregistration belong to
[eval](../../eval/SKILL.md); this reference owns the independent diagnosis.

```text
scientific_claim_review(experiment_contract, result_bundle, rerun_budget?)
  -> diagnosis_receipt + bounded_probe_request + scoped_verdict
```

## Inputs

`experiment_contract`: claim, hypothesis, expected observation, horizon,
confidence, falsifier, surprise trigger, mechanism, changed boundary,
controls, invariants, evaluator, baseline, frozen surfaces, and rerun budget
(attempts, time, compute, spend). `result_bundle`: immutable artifacts,
observed result, guards, command environment.

If expectation, horizon, falsifier, controls, evaluator, baseline, or budget is
missing, mark the inference `blocked` or `inconclusive`; never write the
expectation after seeing results. Confidence is a vector (source
interpretation, implementation fidelity, evaluator validity, effect
sensitivity, inference scope), not one score.

## Diagnosis Order

Compare observed with expected as `expected | surprising_negative |
implausibly_positive | unresolved`, then attack the chain from the cheapest
upstream cause:

1. **Observation integrity:** immutable, complete, comparable; not a parsing or
   reporting mistake.
2. **Baseline and controls:** baseline reproduces, positive/negative controls
   behave, guards pass, splits comparable.
3. **Implementation fidelity:** method, configuration, preprocessing, and seeds
   match the source.
4. **Evaluator integrity and sensitivity:** metric direction correct, effect
   detectable, no leakage, contamination, saturation, or grader drift.
5. **Alternative explanations:** list them; pick the probe that separates them.
6. **Inference:** only now state what the evidence supports, inside scope.

An implausibly strong positive (sudden perfect scores, impossible speedups,
guard-insensitive gains) goes through the same order before promotion.

## Bounded Probe

Choose the cheapest probe with the highest discrimination inside the remaining
budget. The diagnosis lane proposes; the domain executor runs it. Neither may
change the evaluator, dataset, frozen surfaces, spend limit, or conclusion
scope, and the diagnosis lane never approves its own evidence. Use targeted
external research only when source interpretation or a domain assumption is
still disputed after local checks.

## Receipt and Verdicts

```yaml
diagnosis_receipt:
  expectation_comparison:
  confidence_vector: {}
  passed_checks: []
  failed_checks: []
  alternative_explanations: []
  selected_probe:
  remaining_budget:
  source_gaps: []
  proposed_verdict:
```

- `invalid_experiment`: setup, controls, artifacts, or evaluator cannot support
  the inference.
- `inconclusive`: valid to inspect, but cannot distinguish the claim.
- `method_challenged`: credible conflict, not enough for scoped refutation.
- `method_refuted_in_scope` / `method_supported_in_scope`: name the tested
  implementation, data, evaluator, conditions, and budget.

Never refute while controls fail, fidelity or evaluator sensitivity is
unresolved, or a material alternative is untested. Never promote an
implausibly positive result before integrity checks pass. Material conclusions
go to the `scientific-evidence` review rubric.

## Examples

- Positive control also failed, preprocessing unchecked -> `invalid_experiment`;
  repair setup and rerun within budget. Not "the method fails".
- Controls pass, fidelity matched, evaluator detects a synthetic effect, no
  gain across bounded reruns -> `method_refuted_in_scope` for that scope only.
- Expected one or two fewer misses, every held-out case became perfect ->
  `implausibly_positive`; audit leakage, grader drift, and comparability first.
