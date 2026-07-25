# Agent QA Experiment Loop Prompt

```text
Independently review the experimental conclusion in <experiment artifacts>.

Read the preregistered ExperimentContract and immutable result bundle first.
If expected observation, horizon, confidence, falsifier, surprise trigger,
controls, evaluator, baseline, or rerun budget is missing, mark the inference
blocked or inconclusive instead of inventing it after seeing results.

Compare observed versus expected behavior as:
expected | surprising_negative | implausibly_positive | unresolved.

Build a first-principles failure tree in this order:
1. observation integrity
2. baseline and controls
3. implementation fidelity
4. evaluator integrity and sensitivity, including leakage or contamination
5. alternative causal explanations
6. scoped inference

Choose only the cheapest probe that distinguishes the leading alternatives and
fits the declared attempt, time, compute, and spend budget. The domain executor
runs the probe; this diagnosis lane must not mutate frozen surfaces, become the
experiment controller, or approve its own evidence.

Return a DiagnosisReceipt, probe/rerun request if justified, confidence vector,
source gaps, and exactly one scoped verdict:
invalid_experiment | inconclusive | method_challenged |
method_refuted_in_scope | method_supported_in_scope.

Do not refute a method when controls, fidelity, evaluator sensitivity, or
material alternatives remain unresolved. Do not promote an implausibly strong
positive result before leakage, contamination, evaluator drift, and baseline
comparability are checked. Hand material final conclusions to the
scientific-evidence reviewer gate.
```
