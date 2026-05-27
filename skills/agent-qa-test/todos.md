# Todos

- [ ] Identify the target behavior and whether the operator wants run mode or
  `agent-qa-test:prompt`.
- [ ] Use [reference-grounding](../reference-grounding/SKILL.md) to inspect the
  smallest relevant ticket, spec, skill, prompt, app files, or prior QA evidence.
- [ ] Design 2-4 focused test cases with explicit required evidence for each.
- [ ] Write the claim under test and the evidence that would falsify it.
- [ ] Decide whether the tester lane needs `agent-behavior-test`-style
  instrumented run capture for child-agent logs, command events, or artifact
  conformance.
- [ ] Draft or run a tester lane that gathers concrete artifacts instead of
  self-certifying in prose.
- [ ] Draft or run an evidence-review lane that attacks unsupported claims,
  scope mismatch, missing screenshots/logs/states, and weak artifacts.
- [ ] Reconcile both lane reports into pass, fail, blocked, fix, or rerun.
- [ ] For serious readiness claims, reusable fixtures, or completion gates, run
  a final proof-bundle check through `review` or a dedicated reviewer lane.
- [ ] Use [advise](../advise/SKILL.md) when runner choice, evidence threshold,
  artifact location, or rerun-vs-fix policy has real tradeoffs.
- [ ] Use [review](../review/SKILL.md) before treating a new reusable test
  template or repeated workflow as trustworthy.
