---
name: agent-qa-test
description: Design or run the adversarial testing prompt bundle for an app feature, skill, prompt, or workflow. Use when the operator appends "$test", says "please test", or wants the main agent to design tests, spawn a QA/tester lane to gather evidence, spawn an evidence-review lane to attack that evidence, and iterate until the behavior is proved, fixed, or honestly blocked. Use agent-qa-test:prompt when the operator only wants the reusable prompt instead of execution.
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
+ EvidenceReviewLane
+ MainReconcileLoop
+ FixOrRerunDecision
+ PassFailBlockedVerdict
```

The main agent owns test design, orchestration, fixes, and the final decision.
The tester lane owns using the app, skill, prompt, or workflow and collecting
evidence. The evidence-review lane owns attacking whether the tester's evidence
actually proves the behavior.

`goal-crafter` writes high-level native Goals. `agent-behavior-test` owns
isolated run capture and scoring. `agent-qa-test` sits between them: it turns the
operator's "test this properly" instruction into an executable adversarial
testing loop or a paste-ready prompt.

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
5. Spawn or draft the **tester lane** prompt. The tester must use the product or
   skill, collect evidence, and avoid broad self-certification.
6. Spawn or draft the **evidence-review lane** prompt. The reviewer must inspect
   the tester output adversarially and mark missing, weak, stale, irrelevant, or
   misleading evidence.
7. Reconcile both reports:
   - pass only when evidence-review says the proof is strong enough
   - rerun QA when the tester missed states or evidence
   - fix the app/skill/prompt when behavior is wrong
   - record a blocker only with evidence, attempted paths, and the missing input
8. Write or return the result in the requested surface: chat summary, ticket QA
   artifact, experiment folder, or paste-ready prompt.

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
  "unsupported_claims": ["<claims not proved by artifacts>"],
  "missing_evidence": ["<screenshots/logs/states not captured>"],
  "weak_artifacts": ["<artifact and why it is weak>"],
  "rerun_instructions": ["<specific tester rerun instructions>"],
  "fix_candidates": ["<likely app/skill/prompt fixes>"]
}
```

The reviewer should be skeptical about screenshots, logs, and final prose. A
screenshot is useful only when it shows the state needed to prove the case.

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
  first-load checklist, produce visible checkpoints, and expose skipped steps.
- **Prompt/workflow behavior:** require phase checkpoints and compare the
  emitted report against the expected workflow sequence.
- **Regression canary:** run the same test shape against the old expected
  behavior and current behavior; record the delta.
- **Prompt-only request:** do not run tools or spawn lanes; return the compact
  prompt with lane contracts and stop condition.

## Top 3 Gotchas

1. Do not let the tester be the only judge. The tester gathers evidence; the
   evidence-review lane attacks whether that evidence proves anything.
2. Do not treat screenshots as magic. Name the state each screenshot must show,
   and reject screenshots that do not prove the claim.
3. Do not spin forever. Iterate through fix or rerun only while each pass
   produces new evidence or a plausible correction.

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
  pass/fail/blocked verdict, artifacts, and next action
- a paste-ready prompt that instructs another agent to run the same loop

The final verdict must say:

- target behavior tested
- test cases attempted
- best evidence gathered
- evidence-review verdict
- fixes or reruns performed
- remaining blocker, if any
