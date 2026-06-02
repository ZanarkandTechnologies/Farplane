# Agent QA Test Prompt-Only Template

Use this when the operator wants a paste-ready prompt instead of execution.

```text
You are running an adversarial agent QA test for <target behavior>.

Main agent responsibilities:
1. Read the smallest relevant context.
2. Design 2-4 tests and name required evidence for each.
3. Write the claim under test and the evidence that would falsify it.
4. Decide whether tester evidence needs instrumented child-agent run capture
   for skill/prompt conformance, command logs, artifact contracts, or canaries.
5. Spawn a tester lane to use the app/skill/workflow and gather artifacts.
6. Spawn an evidence-review lane to attack whether the artifacts prove the
   behavior.
7. Fix, rerun, or block based on the evidence-review result.
8. For serious readiness claims, reusable fixtures, or completion gates, run a
   final proof-bundle check over the claim, tester artifacts, captured logs when
   present, evidence-review critique, and rerun/fix history.

Tester lane:
- act like <target persona>
- execute the assigned test cases
- collect concrete screenshots/logs/files/commands/artifacts
- report actions, observations, evidence paths, and blockers
- do not mark pass without evidence

Evidence-review lane:
- review the tester's artifacts, not the tester's confidence
- restate the claim under test before judging pass/fail
- identify unsupported claims, missing states, weak screenshots/logs, and
  misleading evidence
- identify scope mismatch where the evidence proves a narrower behavior than
  the operator asked for
- return pass/fail/blocked plus exact rerun or fix instructions

Stop condition:
Pass only when evidence-review says the proof is strong enough. Rerun when
evidence is weak. Fix when behavior is wrong. Block only with attempted paths,
evidence gathered, safe options considered, and the one missing input.
If a known gap falsifies the claim under test, the original behavior is fail or
blocked, even if a narrower slice passed.
```
