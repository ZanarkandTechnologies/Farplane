---
name: agent-qa-test
description: Design or run the adversarial testing prompt bundle for an app feature, skill, prompt, or workflow. Use when the operator appends "$test", says "please test", or wants the main agent to design tests, spawn a QA/tester lane to gather evidence, spawn an evidence-review lane to attack that evidence, optionally use agent-behavior-test-style run capture for child-agent logs, and iterate until the behavior is proved, fixed, or honestly blocked. Use agent-qa-test:prompt when the operator only wants the reusable prompt instead of execution.
tier: 2
source: local
methods:
  - agent-qa-test:prompt
  - agent-qa-test:app
  - agent-qa-test:skill
  - agent-qa-test:regression
allowed-tools: Read, Glob, Grep, Bash
---

# Agent QA Test

<!-- BEGIN CODEXTER_IMPORTANT_CHECKLIST -->
## Important Checklist

Source: `SKILL.md`

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
<!-- END CODEXTER_IMPORTANT_CHECKLIST -->

`agent-qa-test` is the chat-invoked surface for adversarial agent testing. Treat
`$test` as a user shorthand that injects this whole testing contract into the
request, for example: "build feature X, please $test."

Use it when the operator says things like:

- "test this feature with agents"
- "build feature X, please $test"
- "spawn someone to use the app and someone to check the evidence"
- "make sure the screenshots/logs actually prove this works"
- "write me the prompt for an agent test session"
- "go adversarially until the app is fixed"

This skill is not a replacement for normal tests. It is for behavior proof that
needs a user-like tester, screenshots/logs/artifacts, and a skeptical
evidence-review pass.

## Mental Model

```text
AgentQATest :=
  TargetBehavior
+ TestCases
+ TesterLane
+ OptionalInstrumentedRunCapture
+ EvidenceReviewLane
+ MainReconcileLoop
+ FixOrRerunDecision
+ FinalProofBundleReview
+ PassFailBlockedVerdict
```

The main agent owns test design, orchestration, fixes, and the final decision.
The tester lane owns using the app, skill, prompt, or workflow and collecting
evidence. The evidence-review lane owns attacking whether the tester's evidence
actually proves the behavior.

`goal-crafter` writes high-level native Goals. `agent-behavior-test` owns
isolated run capture and scoring. `agent-qa-test` composes that lower-level
capture when tester-lane evidence needs durable child-agent logs, command
events, final output, or scored artifact conformance. `agent-qa-test` sits
between high-level intent and raw run capture: it turns the operator's "test
this properly" instruction into an executable adversarial testing loop or a
paste-ready prompt.

For serious readiness claims, the proof stack is:

```text
agent-qa-test orchestrates
  -> tester lane gathers evidence
  -> agent-behavior-test-style capture records child-agent behavior when useful
  -> evidence-review lane attacks the tester artifacts
  -> main agent fixes, reruns, or reconciles
  -> review/final proof-bundle check judges whether the whole evidence package
     supports the claim
```

## Modes

- **Default / run mode:** execute the agent QA loop in the current thread.
- **`agent-qa-test:prompt`:** return the reusable prompt/template only.
- **`agent-qa-test:app`:** bias tests toward app usage, screenshots, console
  logs, route/state coverage, and visual/user evidence.
- **`agent-qa-test:skill`:** bias tests toward fresh skill invocation, checklist
  adherence, required context loading, and final output shape.
- **`agent-qa-test:regression`:** rerun a known scenario before and after a fix
  or compare current behavior against an expected report.

## First-Load Workflow

1. Identify the target behavior: app feature, skill, prompt, workflow, or ticket
   behavior.
2. Read the smallest relevant context: ticket/spec, feature docs, changed files,
   skill instructions, prior QA artifacts, or the operator's target prompt.
3. Design 2-4 test cases:
   - happy path
   - realistic confused-user path
   - edge/error path
   - regression/canary path when relevant
4. Define required evidence for each case: screenshots, logs, commands, files,
   traces, browser state, skill checklist ledger, or final JSON report.
5. Write the **claim under test** before running: one sentence naming what a
   pass would prove, plus the main evidence that would falsify it. Keep this
   claim stable unless the final verdict explicitly says the test narrowed.
6. Decide whether the tester lane needs **instrumented run capture**:
   - use `agent-behavior-test` shape when testing skill/prompt conformance,
     child-agent behavior, artifact contracts, command logs, or regression
     canaries
   - plain tester-lane evidence is enough when manual screenshots/logs/files
     prove the feature path without needing a full child-agent event stream
7. Spawn or draft the **tester lane** prompt. The tester must use the product or
   skill, collect evidence, and avoid broad self-certification.
8. Spawn or draft the **evidence-review lane** prompt. The reviewer must inspect
   the tester output adversarially and mark missing, weak, stale, irrelevant, or
   misleading evidence.
9. Reconcile both reports:
   - pass only when evidence-review says the proof is strong enough
   - fail when the evidence only proves a narrower behavior than the claim under
     test
   - rerun QA when the tester missed states or evidence
   - fix the app/skill/prompt when behavior is wrong
   - record a blocker only with evidence, attempted paths, and the missing input
10. For serious readiness claims, reusable fixtures, or completion gates, run a
    final proof-bundle check through `review` or a dedicated reviewer lane that
    judges the claim, tester artifacts, captured logs, evidence-review critique,
    and rerun/fix history together.
11. Write or return the result in the requested surface: chat summary, ticket QA
    artifact, experiment folder, or paste-ready prompt.

## Claim Under Test

Before testing, write:

```text
Claim: <what this QA pass will prove if it passes>
Would fail if: <the most important missing or contradictory evidence>
```

Use this as the shared contract for both lanes. A tester may discover that only
a narrower slice can be tested, but that narrower result cannot be reported as a
pass for the original claim. If the tester records a known gap that would falsify
the claim, evidence-review must return `fail` or `blocked`, not `pass`.

## Lane Contracts

### Tester Lane

The tester behaves like a target user or fresh skill caller.

Required output:

```json
{
  "lane": "tester",
  "target": "<feature|skill|prompt|workflow>",
  "test_cases": [
    {
      "name": "<case>",
      "status": "pass|fail|blocked",
      "actions": ["<what was tried>"],
      "evidence": ["<screenshot/log/file/command path>"],
      "observations": ["<user-visible result or confusion>"]
    }
  ],
  "artifacts": ["<paths>"],
  "blockers": ["<missing access, seed data, tooling, etc>"]
}
```

The tester must not mark a case as pass without concrete evidence.

### Evidence-Review Lane

The reviewer judges the tester's artifacts, not the tester's confidence.

Required output:

```json
{
  "lane": "evidence-review",
  "verdict": "pass|fail|blocked",
  "claim_under_test": "<claim being reviewed>",
  "unsupported_claims": ["<claims not proved by artifacts>"],
  "scope_mismatch": ["<places where the evidence proves a narrower claim>"],
  "missing_evidence": ["<screenshots/logs/states not captured>"],
  "weak_artifacts": ["<artifact and why it is weak>"],
  "rerun_instructions": ["<specific tester rerun instructions>"],
  "fix_candidates": ["<likely app/skill/prompt fixes>"]
}
```

The reviewer should be skeptical about screenshots, logs, and final prose. A
screenshot is useful only when it shows the state needed to prove the case.
Known gaps are not harmless caveats when they falsify the claim under test.

## Prompt Templates

Use these templates when the operator wants prompt output instead of direct
execution:

- `prompts/run-loop.md` for the default adversarial testing loop
- `prompts/prompt-only.md` for a compact paste-ready instruction block

Keep generated prompts concrete: target, cases, evidence, lane prompts,
rerun/fix policy, and stop condition.

## Core Branches

- **App feature:** require user-like flows, screenshots for meaningful states,
  console/server logs when available, and visual or interaction evidence when
  UI changed.
- **Skill behavior:** require the tester to load the target skill, follow its
  first-load checklist, produce visible checkpoints, expose skipped steps, and
  usually use `agent-behavior-test`-style captured run artifacts.
- **Prompt/workflow behavior:** require phase checkpoints and compare the
  emitted report against the expected workflow sequence.
- **Composite workflow:** when one workflow promises to call another, the claim
  under test must include the downstream outcome, not only the upstream trigger.
- **Regression canary:** run the same test shape against the old expected
  behavior and current behavior; record the delta.
- **Prompt-only request:** do not run tools or spawn lanes; return the compact
  prompt with lane contracts and stop condition.

## Gotchas

1. Do not let the tester be the only judge. The tester gathers evidence; the
   evidence-review lane attacks whether that evidence proves anything.
2. Do not treat screenshots as magic. Name the state each screenshot must show,
   and reject screenshots that do not prove the claim.
3. Do not spin forever. Iterate through fix or rerun only while each pass
   produces new evidence or a plausible correction.
4. Do not let "pass for a narrow slice" read as "pass for the operator's
   requested behavior." If scope narrows, say so in the verdict.

## Judgment Questions

Use `advise` when these choices materially affect cost or confidence:

- whether to run the loop now or return a prompt
- native subagent lanes vs `codex exec --json`
- how many test cases are enough for the risk
- ticket artifact vs experiment artifact vs chat-only result
- whether weak evidence means rerun QA, fix the product, or improve
  instrumentation

## Outcome Contract

A completed `agent-qa-test` produces one of:

- an executed agent QA result with tester output, evidence-review output,
  optional captured-run output, pass/fail/blocked verdict, artifacts, and next
  action
- a paste-ready prompt that instructs another agent to run the same loop

The final verdict must say:

- target behavior tested
- claim under test and whether it was proved
- test cases attempted
- best evidence gathered
- evidence-review verdict
- final proof-bundle check when required
- fixes or reruns performed
- remaining blocker, if any
