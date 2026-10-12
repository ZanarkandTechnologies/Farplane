# Adversarial Mode

Load this for `qa(target, mode: adversarial)`: an app, skill, prompt, or
workflow claim that needs a user-like tester plus a separate evidence-review
lane attacking whether the artifacts prove the claim. It is not ordinary
issue QA; use it when the proof policy says `agent_qa`, the operator asks to
"try to break it" or `$test`, or a readiness claim is serious.

```text
adversarial(claim, target, evidence_policy?)
  -> claim_under_test + cases + tester_report + evidence_review + verdict
```

## Builder ≠ Tester ≠ Judge

The builder (main agent) designs cases, fixes, and reconciles. The tester lane
uses the target and collects artifacts. The evidence-review lane judges those
artifacts, not the tester's confidence. **The tester lane cannot self-approve
proof**, and the builder cannot approve its own fix; serious readiness claims,
reusable fixtures, and completion gates also get a final proof-bundle check by
`review` or a dedicated reviewer lane.

Ordinary UI proof stays functional + visual mode: functional/`qa-tester`
collects artifacts and `result.json`; visual mode judges screenshots against
`design.md`. Adversarial mode is reserved for claim attacks.

## Claim Under Test

Write before running and keep stable:

```text
Claim: <what this pass proves if it passes>
Would fail if: <the most important missing or contradictory evidence>
```

A narrower slice that passes is reported as that slice; it cannot pass the
original claim. A known gap that falsifies the claim makes the verdict `fail`
or `blocked`, never `pass`. For a composite workflow, the claim includes the
downstream outcome, not only the upstream trigger.

## Cases

Design 2-4: happy path, realistic confused user, edge/error, and a
regression canary when relevant. For user-facing or workflow claims each case
is a `HumanLikeQACase`:

```text
name: happy-path | confused-user | edge-error | regression-canary
user_goal; expected_workflow; likely_confusion_or_wrong_path;
required_proof_artifacts; falsifier; reviewer_attack_questions;
instrumentation_request   # smallest hook when proof is weak
```

Every case names its claim and its falsifier. Confusion, dead ends,
misleading states, missing hooks, and weak observability are findings.
Use `../../eval/references/proof-cases.md` when the case matrix itself is not
settled, and [eval](../../eval/SKILL.md) `behavior_trace` when the tester needs
instrumented child-agent logs, command events, or artifact-conformance scoring.

## Branch Bias

- **App:** user-like flows, a screenshot per meaningful state, console/server
  logs, interaction evidence.
- **Skill:** fresh invocation, first-load todo adherence, visible checkpoints,
  skipped steps exposed; usually `behavior_trace`.
- **Prompt/workflow:** phase checkpoints compared with the expected sequence.
- **Regression:** same case before and after; record the delta.
- **Experiment claim:** load [scientific claim review](scientific-claim-review.md);
  experiment design and preregistration stay in [eval](../../eval/SKILL.md).

## Lane Outputs

Tester (one entry per case; no `pass` without concrete evidence):

```json
{"lane": "tester", "target": "", "test_cases": [{"name": "", "human_like_case": {},
  "status": "pass|fail|blocked", "actions": [], "evidence": [], "observations": []}],
 "artifacts": [], "blockers": []}
```

Evidence review:

```json
{"lane": "evidence-review", "verdict": "pass|fail|blocked", "claim_under_test": "",
 "unsupported_claims": [], "scope_mismatch": [], "missing_evidence": [],
 "weak_artifacts": [], "human_confusion_findings": [],
 "rerun_instructions": [], "fix_candidates": []}
```

A screenshot counts only when it shows the state the case needs.

## Reconcile and Rerun

- Pass only when evidence review passes the original claim.
- Weak or missing evidence: rerun the tester with sharper, named instructions.
- Wrong behavior: fix, then rerun the affected case (regression canary too).
- Iterate only while each loop yields new evidence or a plausible correction;
  stop with a blocker naming attempted paths, evidence, and the one missing
  input.
- Inside a Goal, Goal mode owns continuation and budget; adversarial mode owns
  the proof loop and the fix/rerun threshold for its claim.

## Prompt Templates

Run loop (execute now):

```text
Run an adversarial QA test for <target>. Read the smallest context (issue,
changed files, target skill/prompt, prior QA evidence, launch instructions).
Write Claim / Would fail if. Design 2-4 HumanLikeQACases with required
evidence and a falsifier each. Decide whether the tester needs behavior_trace.
Spawn a tester lane that uses <target> as <persona>, collects concrete
artifacts, and reports actions, observations, confusion, instrumentation
requests, and blockers without self-certifying. Spawn a separate
evidence-review lane that restates the claim and returns unsupported claims,
scope mismatch, missing evidence, weak artifacts, rerun instructions, and fix
candidates. Reconcile: pass only on evidence-review pass; rerun on weak
evidence; fix on wrong behavior; block with the single missing input. For
serious readiness claims add a final proof-bundle check.
```

Prompt-only: return that block filled in for the target, with the two lane
JSON shapes above and the stop condition; do not run tools or spawn lanes.

## Output

Verdict lists target, claim and whether it was proved, cases attempted, best
evidence, evidence-review verdict, proof-bundle check when required, fixes or
reruns performed, and the remaining blocker. Store lane reports under
`.farplane/qa/<issue>/<run>/adversarial/` and post the verdict on the issue.
