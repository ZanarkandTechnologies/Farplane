---
title: Agent QA Test Runtime Checklist
owner: agent-qa-test
status: active
kind: qa-checklist
created_at: 2026-06-22
updated_at: 2026-06-22
applies_to:
  - agent-qa-test
  - adversarial-proof
---

# Agent QA Test Runtime Checklist

Use this after changing `agent-qa-test` or before accepting an adversarial proof
bundle.

## Checks

1. `adversarial-scope`
   - Question: Is the target a claim, skill, prompt, app, workflow, or
     regression that needs adversarial proof?
   - Violation: The skill is used as ordinary ticket QA.

2. `claim-under-test`
   - Question: Is the claim under test written before the run?
   - Violation: The tester can narrow scope without calling that out.

3. `tester-evidence`
   - Question: Does the tester lane gather concrete artifacts?
   - Violation: Tester confidence or prose substitutes for screenshots/logs/files.

4. `independent-evidence-review`
   - Question: Does a separate evidence-review lane attack the tester artifacts?
   - Violation: The tester self-approves.

5. `verdict-scope`
   - Question: Does the final verdict match the evidence scope?
   - Violation: A narrow pass is reported as proof of the broader claim.

## Experiment Profile

Apply these additional checks only for `agent-qa-test:experiment`:

6. `expectation-preregistered`
   - Question: Were expected observation, horizon, confidence, falsifier, and
     surprise trigger recorded before results were read?
   - Violation: The expectation is reverse-engineered from the observation.

7. `validity-before-inference`
   - Question: Were observation integrity, baseline/controls, implementation
     fidelity, evaluator sensitivity, and material alternatives checked before
     the conclusion?
   - Violation: A failed run is treated as a failed method.

8. `two-sided-surprise`
   - Question: Does the review audit both material negative surprise and
     implausibly positive results?
   - Violation: Suspicious success is promoted without leakage, contamination,
     evaluator-drift, or baseline-comparability checks.

9. `bounded-discriminating-probe`
   - Question: Is each proposed rerun the cheapest probe that distinguishes
     leading alternatives within declared attempt/time/compute/spend limits?
   - Violation: The review requests broad research or unbounded reruns.

10. `owner-and-verdict-boundary`
   - Question: Does the domain owner execute while Agent QA diagnoses, and is
     the verdict one of the scoped scientific verdicts?
   - Violation: Agent QA becomes a second experiment controller or emits a
     universal method claim.
