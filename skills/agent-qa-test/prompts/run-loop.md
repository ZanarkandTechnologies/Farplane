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

For each test case, name the required evidence before running it.

Spawn or emulate a tester lane whose job is to use the app/skill/workflow like
the target user, collect concrete evidence, and return:
- actions taken
- screenshots/logs/files/commands/artifacts
- user-visible observations
- blockers

Spawn or emulate an evidence-review lane whose job is to attack the tester
output and return:
- unsupported claims
- missing evidence
- weak or irrelevant artifacts
- exact rerun instructions
- likely app/skill/prompt fixes

As the main agent, reconcile both reports. If evidence is weak, rerun QA with
sharper instructions. If behavior is wrong, fix it and rerun the relevant test.
Stop only when evidence-review passes or a blocker is recorded with attempted
paths, evidence gathered, and the single missing input.
```
