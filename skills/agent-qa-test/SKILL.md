---
name: agent-qa-test
description: "Turn an app, skill, prompt, or workflow claim into adversarial QA cases, tester evidence, critique, and rerun guidance."
tier: 2
source: local
eval: evals/evals.json
qa_checklist: qa_checklist.md
methods:
  - agent-qa-test:prompt
  - agent-qa-test:app
  - agent-qa-test:skill
  - agent-qa-test:regression
  - agent-qa-test:experiment
allowed-tools: Read, Glob, Grep, Bash
---

# Agent QA Test

## Context

`agent-qa-test` is the adversarial proof surface for app, skill, prompt, or
workflow claims. It is not normal ticket QA. Use it when a proof policy or
operator request needs a user-like tester plus a separate evidence-review lane
that attacks whether the artifacts prove the claim.

## Skill Signature

```text
agent_qa_test(claim, target, evidence_policy?) -> tester_report + evidence_review + verdict
state: reads(ticket/spec/skill/prompt/workflow, prior QA evidence, optional design.md); writes tester/evidence-review reports or prompt template
gates: claim_under_test_written; tester_lane_collects_artifacts; evidence_review_lane_independent; pass_requires_strong_artifacts
routes: eval:behavior-trace | qa | visual-qa | review
fails: replaces normal ticket QA; lets tester self-approve; reports narrow proof as broad pass; treats missing screenshots/logs as harmless
```

```text
agent_qa_test_experiment(claim, experiment_contract, result_bundle, rerun_budget?)
  -> diagnosis_receipt + scoped_verdict + scientific_audit_packet
gates: expectation_preregistered; observation_immutable; diagnosis_lane_independent;
       controls_and_fidelity_checked; reruns_within_budget; conclusion_scoped
routes: domain_executor | research:targeted | scientific-evidence review
fails: null_result_means_method_false; suspicious_success_auto_promoted;
  diagnosis_lane_becomes_experiment_controller; unbounded_rerun
```

### Experiment Profile Gate

For `agent-qa-test:experiment`, always return these minimum decisions:

1. `expectation_comparison`: compare the immutable observation with the
   preregistered expected observation, horizon, confidence, falsifier, and
   surprise trigger; explicitly mark a missing pre-result contract.
2. `validity_checks`: report observation integrity, baseline/controls,
   implementation fidelity, evaluator sensitivity/integrity, baseline
   comparability, equal budgets, and material alternative explanations.
3. `probe`: choose the cheapest discriminating probe inside remaining
   attempt/time/compute/spend authority. The domain executor runs it; the
   independent diagnosis lane does not control or self-approve the experiment.
4. `research`: use targeted external research only after local checks when
   source interpretation, expected mechanism/effect, or a domain assumption
   remains disputed.
5. `verdict`: return `invalid_experiment | inconclusive | method_challenged |
   method_refuted_in_scope | method_supported_in_scope`; material conclusions
   still require `scientific-evidence` review. Any refuted/supported verdict
   explicitly names the tested implementation, data, evaluator, conditions,
   and budget; never substitute vague “configuration” wording.

## Phase Boundary

This skill designs and reconciles adversarial proof. It may compose Eval
`behavior_trace` for instrumented CLI child-agent capture and hand final proof
bundles to `review`, but Goal mode remains the continuation owner.

<!-- BEGIN FARPLANE_IMPORTANT_CHECKLIST -->
## Todo List

- [ ] Identify the target behavior and whether the operator wants run mode or
  `agent-qa-test:prompt`.
- [ ] Confirm this is adversarial claim proof, not ordinary ticket QA. If the
  ticket only needs artifact collection, route to `qa`; if it only needs visual
  judgment over screenshots, route to `visual-qa`.
  - [ ] For ordinary UI proof, explicitly say `qa / qa-tester` owns artifacts,
    `visual-qa` owns screenshot judgment, and `agent-qa-test` is not the
    default.
- [ ] Use [reference-grounding](../reference-grounding/SKILL.md) to inspect the
  smallest relevant ticket, spec, skill, prompt, app files, or prior QA evidence.
- [ ] Design 2-4 focused test cases with explicit required evidence for each.
  - [ ] For user-facing or workflow claims, shape each case as a
    `HumanLikeQACase` with a user goal, expected workflow, likely confusion or
    wrong path, required proof artifacts, falsifier, reviewer attack questions,
    and instrumentation request.
- [ ] Write the claim under test and the evidence that would falsify it.
- [ ] For `agent-qa-test:experiment`, load
      [scientific claim review](references/scientific-claim-review.md), bind the
      preregistered expected observation, and compare it with the immutable
      result before selecting discriminating probes.
  - [ ] Return all five Experiment Profile Gate decisions by name even when the
        requested answer can be brief: expectation comparison; every validity
        check; bounded probe plus executor/diagnosis ownership; conditional
        research; scoped verdict plus scientific-evidence review.
- [ ] Decide whether the tester lane needs Eval `behavior_trace`
  instrumented run capture for child-agent logs, command events, or artifact
  conformance.
- [ ] Draft or run a tester lane that gathers concrete artifacts instead of
  self-certifying in prose.
- [ ] When `agent-qa-test` is used, state that the tester lane cannot
  self-approve proof; keep tester evidence and evidence-review critique
  separate.
- [ ] When answering a routing question about ordinary UI QA, include this
  literal rule: `The tester lane cannot self-approve proof.`
- [ ] Draft or run an evidence-review lane that attacks unsupported claims,
  scope mismatch, missing screenshots/logs/states, and weak artifacts.
- [ ] Reconcile both lane reports into pass, fail, blocked, fix, or rerun.
  - [ ] For experiment review, use only the scoped scientific verdicts defined
        in the reference; do not translate a failed run directly into a failed
        method.
- [ ] For serious readiness claims, reusable fixtures, or completion gates, run
  a final proof-bundle check through `review` or a dedicated reviewer lane.
- [ ] Use [advise](../advise/SKILL.md) when runner choice, evidence threshold,
  artifact location, or rerun-vs-fix policy has real tradeoffs.
- [ ] Use the [review protocol](../review/SKILL.md) before treating a new reusable test
  template or repeated workflow as trustworthy.
<!-- END FARPLANE_IMPORTANT_CHECKLIST -->

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

Inside a ticket proof route, use `agent-qa-test` only when `Proof weight` or
`Metric provider` says `agent_qa`, or when the operator asks for adversarial
agent testing. Normal UI tickets should run `qa` plus `visual-qa` first.

For ordinary UI ticket proof, say the default route explicitly:

```text
qa / qa-tester collects ticket artifacts, screenshots, logs, and result.json.
visual-qa judges screenshots against the ticket or design.md.
agent-qa-test is reserved for adversarial claim proof or an operator `$test`.
When agent-qa-test is used, keep tester and evidence-review lanes separate; the
tester lane cannot self-approve proof.
```

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

## Human-Like Case Shape

Use this compact shape for user-facing app, workflow, prompt, and skill claims
where a skeptical human product tester would try the thing rather than inspect
only implementation details:

```text
HumanLikeQACase:
  name: happy-path | confused-user | edge-error | regression-canary
  user_goal: what a real user is trying to accomplish
  expected_workflow: the intended path or state sequence
  likely_confusion_or_wrong_path: where a fresh user may hesitate, misread,
    click the wrong thing, or reach a misleading state
  required_proof_artifacts: screenshots, logs, command output, files, traces,
    snapshots, child-agent logs, or result.json required to prove this case
  falsifier: evidence that would make the pass claim false or too narrow
  reviewer_attack_questions: questions the evidence-review lane must ask before
    accepting the tester result
  instrumentation_request: the smallest shortcut, log, state mirror, fixture,
    seed, debug HUD, or selector needed when proof is weak
```

The confused-user case is not optional decoration when the claim is about a
workflow a human must understand. Treat confusion, dead ends, misleading states,
missing hooks, and weak observability as QA findings. A pass claim is valid only
when the evidence-review lane agrees that the artifacts answer the attack
questions for the original claim under test.

`goal-advisor` writes high-level native Goals. Eval `behavior_trace` owns
isolated CLI run capture and scoring. `agent-qa-test` composes that lower-level
capture when tester-lane evidence needs durable child-agent logs, command
events, final output, or scored artifact conformance. `agent-qa-test` sits
between high-level intent and raw run capture: it turns the operator's "test
this properly" instruction into an executable adversarial testing loop or a
paste-ready prompt.

When composed inside Goal Packet algebra, `agent-qa-test` is an `agent_qa`
metric or proof provider and supplies the fix/rerun evidence threshold. It
should not compete with Goal mode for continuation ownership: Goal mode owns
continuation and blocked stops; `agent-qa-test` owns the adversarial proof loop
for the claim under test.

For serious readiness claims, the proof stack is:

```text
agent-qa-test orchestrates
  -> tester lane gathers evidence
  -> Eval behavior trace records CLI child-agent behavior when useful
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
- **`agent-qa-test:experiment`:** independently diagnose a material deviation
  from a preregistered expected observation, authorize only bounded
  discriminating probes, and return a scoped scientific verdict.

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
4. Shape user-facing or workflow cases as `HumanLikeQACase` entries. Include
   the user goal, expected workflow, likely confusion or wrong path, required
   proof artifacts, falsifier, reviewer attack questions, and instrumentation
   request for each case.
5. Define required evidence for each case: screenshots, logs, commands, files,
   traces, browser state, skill todo list ledger, child-agent logs, or final
   JSON report. If the evidence cannot show what a human would need to trust,
   record the instrumentation request instead of hand-waving the gap.
6. Write the **claim under test** before running: one sentence naming what a
   pass would prove, plus the main evidence that would falsify it. Keep this
   claim stable unless the final verdict explicitly says the test narrowed.
7. Decide whether the tester lane needs **instrumented run capture**:
   - use Eval `behavior_trace` when testing skill/prompt conformance,
     child-agent behavior, artifact contracts, command logs, or regression
     canaries
   - plain tester-lane evidence is enough when manual screenshots/logs/files
     prove the feature path without needing a full child-agent event stream
8. Spawn or draft the **tester lane** prompt. The tester must use the product or
   skill, collect evidence, record confusion or wrong-path observations, and
   avoid broad self-certification.
9. Spawn or draft the **evidence-review lane** prompt. The reviewer must inspect
   the tester output adversarially and mark missing, weak, stale, irrelevant,
   misleading, or too-narrow evidence.
10. Reconcile both reports:
   - pass only when evidence-review says the proof is strong enough
   - fail when the evidence only proves a narrower behavior than the claim under
     test
   - rerun QA when the tester missed states or evidence
   - fix the app/skill/prompt when behavior is wrong
   - record a blocker only with evidence, attempted paths, and the missing input
11. For serious readiness claims, reusable fixtures, or completion gates, run a
    final proof-bundle check through `review` or a dedicated reviewer lane that
    judges the claim, tester artifacts, captured logs, evidence-review critique,
    and rerun/fix history together.
12. Write or return the result in the requested surface: chat summary, ticket QA
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
      "human_like_case": {
        "user_goal": "<what the user tried to do>",
        "expected_workflow": ["<intended step or state>"],
        "likely_confusion_or_wrong_path": ["<where a fresh user could get lost>"],
        "falsifier": "<evidence that would disprove this case>",
        "instrumentation_request": "<smallest hook needed if proof is weak>"
      },
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
  "human_confusion_findings": ["<confusion or wrong-path evidence the tester found>"],
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
- `prompts/experiment-loop.md` for independent first-principles experiment
  diagnosis and reconciliation

## Reference Map

- [`references/goal-composition.md`](references/goal-composition.md) - split
  between Goal lifecycle ownership and agent QA proof ownership.
- [`references/scientific-claim-review.md`](references/scientific-claim-review.md) -
  load only for `agent-qa-test:experiment`; it owns experiment contracts,
  diagnosis order, rerun authority, and scoped verdicts.

Keep generated prompts concrete: target, cases, evidence, lane prompts,
rerun/fix policy, and stop condition.

## Core Branches

- **App feature:** require user-like flows, screenshots for meaningful states,
  console/server logs when available, and visual or interaction evidence when
  UI changed.
- **Skill behavior:** require the tester to load the target skill, follow its
  first-load todo list, produce visible checkpoints, expose skipped steps, and
  usually use Eval `behavior_trace` artifacts.
- **Prompt/workflow behavior:** require phase checkpoints and compare the
  emitted report against the expected workflow sequence.
- **Composite workflow:** when one workflow promises to call another, the claim
  under test must include the downstream outcome, not only the upstream trigger.
- **Regression canary:** run the same test shape against the old expected
  behavior and current behavior; record the delta.
- **Experiment surprise:** check validity before inference. Audit both material
  negative surprise and implausibly positive results that may indicate leakage,
  contamination, evaluator failure, or baseline mismatch.
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
