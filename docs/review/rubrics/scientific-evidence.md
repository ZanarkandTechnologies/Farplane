# Scientific Evidence

Use when reviewing a material experimental conclusion, reproduction, ablation,
or causal claim after `agent-qa-test:experiment` has produced a diagnosis
receipt and any bounded probe/rerun receipts.

Required TAS: `TAS-A` for `method_refuted_in_scope`, material trust removal, or
promotion from an implausibly positive result.

This family judges inference readiness. Generic artifact traceability,
replayability, and organization remain owned by `evidence-quality`.

## Family TAS Guide

- `TAS-C`: the conclusion outruns failed controls, invalid setup, unresolved
  fidelity/sensitivity, or a material alternative
- `TAS-B`: the experiment is credible but one repairable inference gate or
  scope statement is missing
- `TAS-A`: validity, alternatives, rerun history, and scope support the stated
  conclusion with only minor caveats
- `TAS-D`: the experiment contract, result bundle, or diagnosis receipts are
  insufficient to judge

## Checklist Modules

### Required Checks

- [ ] `expectation-preregistered`: Expected observation, horizon, confidence,
  falsifier, and surprise trigger predate the observed result.
- [ ] `controls-pass`: Baseline and relevant positive/negative controls behave
  as required for the inference.
- [ ] `implementation-fidelity`: The tested implementation, configuration,
  preprocessing, and changed boundary match the stated method.
- [ ] `evaluator-valid-sensitive`: The evaluator direction is correct and can
  detect the expected effect without known leakage, contamination, or drift.
- [ ] `alternatives-discriminated`: Material alternative explanations were
  tested with bounded discriminating probes or explicitly constrain the verdict.
- [ ] `rerun-budget-honest`: Reruns and research stayed inside declared
  attempt/time/compute/spend authority.
- [ ] `conclusion-scoped`: The verdict names the implementation, data,
  evaluator, conditions, and uncertainty it actually covers.

### Blocker Checks

- [ ] `failed-run-equals-failed-method`: A negative observation is promoted to
  method refutation despite failed controls, unresolved fidelity, unknown
  sensitivity, or material alternatives.
- [ ] `suspicious-success-promoted`: An implausibly strong result is promoted
  before leakage, contamination, evaluator drift, and baseline comparability
  are checked.
- [ ] `posthoc-expectation`: The claimed expectation was authored or changed
  after observing results without being labeled exploratory.
- [ ] `unbounded-scope`: A scoped experiment is reported as universal truth.

## Evidence and Finding Cues

Look for the ExperimentContract, immutable result refs, DiagnosisReceipt,
probe/rerun receipts, control outcomes, fidelity evidence, evaluator
sensitivity evidence, confidence vector, and exact scoped verdict. Missing
generic replayability is an `evidence-quality` finding; missing causal validity
or scoped inference is a `scientific-evidence` finding.

## Review Artifact Attachment

- `tas`
- `required_tas`
- `pass`
- `checks`
- `failed_checks`
- `findings`
- `scoped_verdict`
- `next_action`
