## AI App Testing (Cheat Sheet)

### Reality check: non-determinism
LLM outputs vary. You need tests that tolerate variation while still enforcing quality.

### What to test (minimum)
- **Input/output contract**: schema validation, tool-call constraints, safety filters.
- **Regression set**: a small frozen set of prompts with expected properties.
- **Failure modes**: refusal behavior, error handling, missing context, hallucination hotspots.
- **Latency/cost**: budgets for key flows (p95 latency, token usage ceilings).

### Recommended backpressure
- **Deterministic unit/integration** around everything *except* the model call.
- **Evals** for model behavior:\n
  - Property-based assertions (“mentions required fields”, “does not leak secrets”).\n
  - Golden outputs only for tightly constrained tasks.\n
- **Human/LLM judge** tests for subjective criteria (tone, helpfulness), documented as repeatable criteria.\n

### Evidence to capture
- Prompt + tool traces (inputs/outputs) stored as fixtures.
- A small changelog of prompt/system-instruction changes (so regressions are explainable).

