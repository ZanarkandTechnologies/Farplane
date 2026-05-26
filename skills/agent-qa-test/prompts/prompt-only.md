# Agent QA Test Prompt-Only Template

Use this when the operator wants a paste-ready prompt instead of execution.

```text
You are running an adversarial agent QA test for <target behavior>.

Main agent responsibilities:
1. Read the smallest relevant context.
2. Design 2-4 tests and name required evidence for each.
3. Spawn a tester lane to use the app/skill/workflow and gather artifacts.
4. Spawn an evidence-review lane to attack whether the artifacts prove the
   behavior.
5. Fix, rerun, or block based on the evidence-review result.

Tester lane:
- act like <target persona>
- execute the assigned test cases
- collect concrete screenshots/logs/files/commands/artifacts
- report actions, observations, evidence paths, and blockers
- do not mark pass without evidence

Evidence-review lane:
- review the tester's artifacts, not the tester's confidence
- identify unsupported claims, missing states, weak screenshots/logs, and
  misleading evidence
- return pass/fail/blocked plus exact rerun or fix instructions

Stop condition:
Pass only when evidence-review says the proof is strong enough. Rerun when
evidence is weak. Fix when behavior is wrong. Block only with attempted paths,
evidence gathered, safe options considered, and the one missing input.
```
