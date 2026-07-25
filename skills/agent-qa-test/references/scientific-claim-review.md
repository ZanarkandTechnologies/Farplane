---
title: Scientific Claim Review
owner: agent-qa-test
status: active
kind: method-reference
---

# Scientific Claim Review

Load this only for `agent-qa-test:experiment`, when an experimental observation
materially violates a preregistered expectation or supports a high-impact
scientific conclusion.

```text
scientific_claim_review(experiment_contract, result_bundle, rerun_budget?)
  -> diagnosis_receipt + bounded_probe_receipts + scoped_verdict
```

## Input Contract

```yaml
experiment_contract:
  claim:
  hypothesis:
  expected_observation:
  observation_horizon:
  confidence: low | medium | high
  falsifier:
  surprise_trigger:
  mechanism:
  changed_boundary:
  controls: []
  invariants: []
  evaluator:
  baseline:
  frozen_surfaces: []
  rerun_budget:
    attempts:
    time:
    compute:
    spend:
result_bundle:
  immutable_artifacts: []
  observed_result:
  guards:
  command_environment:
```

Confidence is a vector of named judgments, not one numeric score: confidence in
source interpretation, implementation fidelity, evaluator validity, effect
sensitivity, and inference scope may differ.

## Diagnosis Order

Attack the causal chain from the cheapest upstream explanation first:

1. `observation integrity` — artifacts are immutable, complete, comparable,
   and not a parsing/reporting mistake.
2. `baseline and controls` — baseline reproduces, positive/negative controls
   behave, guards pass, and the task/data split is comparable.
3. `implementation fidelity` — the tested implementation matches the source
   method, configuration, preprocessing, seeds, and changed boundary.
4. `evaluator integrity and sensitivity` — metric direction is correct,
   evaluator can detect the expected effect, and no leakage, contamination,
   saturation, or grader drift explains the result.
5. `alternative explanations` — list competing causal explanations and choose
   the smallest probe that distinguishes them.
6. `inference` — only after the prior checks, state what the evidence supports
   inside the tested scope.

An implausibly strong positive result uses the same order. Treat sudden perfect
scores, impossible speedups, or guard-insensitive gains as possible integrity
failures before promotion.

## Bounded Probe Rule

```text
choose_probe(alternatives, remaining_budget)
  -> cheapest probe with highest discrimination
```

The diagnosis lane proposes probes; the domain owner executes them. Neither
lane may silently change the evaluator, dataset, frozen surfaces, spend limit,
or conclusion scope. Research is targeted and conditional: use it only when
source interpretation, expected mechanism/effect, or a domain assumption
remains disputed after local evidence inspection.

## Diagnosis Receipt

```yaml
diagnosis_receipt:
  expectation_comparison: expected | surprising_negative |
    implausibly_positive | unresolved
  confidence_vector: {}
  passed_checks: []
  failed_checks: []
  alternative_explanations: []
  selected_probe:
  probe_rationale:
  remaining_budget:
  source_gaps: []
  proposed_verdict:
```

## Scoped Verdicts

- `invalid_experiment`: setup, controls, artifacts, or evaluator cannot support
  the intended inference.
- `inconclusive`: valid enough to inspect, but sensitivity, alternatives, or
  bounded evidence cannot distinguish the claim.
- `method_challenged`: credible evidence conflicts with the claim but is not
  sufficient for scoped refutation.
- `method_refuted_in_scope`: controls, fidelity, evaluator sensitivity,
  alternatives, and rerun history support rejection only inside the named
  tested scope.
- `method_supported_in_scope`: evidence supports the method only inside the
  named tested scope.

Never emit `method_refuted_in_scope` when baseline/controls fail,
implementation fidelity is unresolved, evaluator sensitivity is unknown, or a
material alternative remains untested. Never promote `method_supported_in_scope`
from an implausibly positive result until integrity checks pass.

## Examples

Faulty reproduction:

```text
Expected: treatment improves the frozen metric while the positive control does.
Observed: neither treatment nor positive control moves.
Verdict: invalid_experiment; repair the evaluator or setup, then rerun within
budget. Do not conclude that the method fails.
```

Well-controlled negative:

```text
Expected: a minimum detectable improvement under the source configuration.
Observed: no improvement across bounded reruns; baseline and controls pass,
implementation matches, evaluator detects a synthetic effect, and alternatives
are tested.
Verdict: method_refuted_in_scope for the named implementation, data, and
evaluator only.
```

Suspicious success:

```text
Expected: one or two fewer misses.
Observed: every held-out case becomes perfect while guard tasks also change.
Verdict: implausibly_positive; audit leakage, grader drift, task contamination,
and baseline comparability before promotion.
```
