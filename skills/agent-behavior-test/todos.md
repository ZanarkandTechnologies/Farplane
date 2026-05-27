# Todos

- [ ] Define the exact behavior under test and the target persona or skill caller.
- [ ] Use [reference-grounding](../reference-grounding/SKILL.md) to inspect the
  owning skill, feature docs, ticket, existing tests, or prior artifacts before
  launching the child run.
- [ ] Confirm this is a run-capture/conformance probe; use `agent-qa-test` as
  the orchestrator when the operator wants adversarial proof or full readiness.
- [ ] Choose CLI JSONL, native subagent, or both, and name why that runner fits
  the proof target.
- [ ] Write the child prompt with visible checkpoints, forbidden shortcuts, and
  the final report shape.
- [ ] Save child-agent artifacts under the ticket, experiment, or declared run
  directory.
- [ ] Score only visible behavior: events, commands, file/artifact evidence,
  checkpoint ledger, and final output.
- [ ] Use [advise](../advise/SKILL.md) when runner choice, schema strictness, or
  pass threshold has real tradeoffs.
- [ ] Use [review](../review/SKILL.md) before treating a new behavior-test
  fixture or repeated workflow as trustworthy.
