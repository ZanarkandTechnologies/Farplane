# Goal Composition

When `agent-qa-test` is invoked inside a Goal, it owns proof for the claim under
test, not the Goal lifecycle.

Use this split:

- Goal mode owns continuation, iteration budget, and blocked-stop reporting.
- `agent-qa-test` owns test cases, tester evidence, evidence review, and
  fix/rerun recommendations.
- A pass only proves the original Goal claim when evidence review says the
  artifacts cover the full claim without scope narrowing.
