# Agent QA Test Run Loop Prompt

Use this when the operator wants the testing loop executed, not merely drafted.

```text
Run an agent QA test for <target behavior>.

First, read the smallest relevant context: ticket/spec, changed files, target
skill/prompt, prior QA artifacts, and app launch instructions when available.

Design 2-4 test cases:
- happy path
- realistic confused-user path
- edge/error path
- regression/canary path when relevant

For user-facing or workflow claims, shape each test as a `HumanLikeQACase`:
- `user_goal`: what a real user is trying to accomplish
- `expected_workflow`: intended path or state sequence
- `likely_confusion_or_wrong_path`: where a fresh user may hesitate, misread,
  click wrong, or reach a misleading state
- `required_proof_artifacts`: screenshots, logs, command output, files, traces,
  snapshots, child-agent logs, or result.json needed to prove the case
- `falsifier`: evidence that would make the pass claim false or too narrow
- `reviewer_attack_questions`: questions the evidence-review lane must answer
- `instrumentation_request`: the smallest hook needed when proof is weak

Before running, write the claim under test:
- `Claim:` what this QA pass will prove if it passes
- `Would fail if:` the most important missing or contradictory evidence

For each test case, name the required evidence before running it. Treat
confusion, dead ends, misleading states, missing hooks, and weak observability
as QA findings. Do not let either lane silently narrow the claim. A narrow slice
can pass only for that slice, not for the original behavior.

Decide whether the tester lane needs instrumented child-agent run capture. Use
that shape when the target is skill/prompt conformance, artifact contracts,
command logs, or a regression canary where visible child-agent behavior matters.

Spawn or emulate a tester lane whose job is to use the app/skill/workflow like
the target user, collect concrete evidence, and return:
- actions taken
- HumanLikeQACase fields when applicable
- screenshots/logs/files/commands/artifacts
- user-visible observations
- confusion or wrong-path findings
- instrumentation request when proof is weak
- blockers

Spawn or emulate an evidence-review lane whose job is to attack the tester
output and return:
- the claim under test
- unsupported claims
- scope mismatch where evidence proves a narrower claim
- missing evidence
- weak or irrelevant artifacts
- human confusion findings
- exact rerun instructions
- likely app/skill/prompt fixes

As the main agent, reconcile both reports. If evidence is weak, rerun QA with
sharper instructions. If behavior is wrong, fix it and rerun the relevant test.
If a known gap falsifies the claim under test, mark the original behavior fail
or blocked. Stop only when evidence-review passes the claim or a blocker is
recorded with attempted paths, evidence gathered, and the single missing input.

For serious readiness claims, reusable fixtures, or completion gates, add a
final proof-bundle check that reviews the claim, tester artifacts, captured
run logs when present, evidence-review critique, and rerun/fix history together.
```
