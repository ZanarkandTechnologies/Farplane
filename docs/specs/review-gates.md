# Review Gates

Date: 2026-04-09

## Goal

Define the canonical review-gate model for the spec-first execution loop.

The system uses three distinct layers:

1. **Ticket Proof Contract** declares metrics, reviewer handoff, rubric gates,
   and required evidence
2. **QA** collects evidence
3. **Reviewer** judges the work against the declared and inferred rubrics
4. **Stop hook** sanity-checks whether the evidence and review verdict justify
   completion or continuation

## Roles

### Ticket Proof Contract

The ticket answers before build starts:

- what mechanical metric, if any, should move or pass
- which review rubric families and TAS gates are required
- which rubric families are hard gates
- which reviewer handoff fields should be passed to the `reviewer` lane:
  task path, review focus, changed files, evidence, rubric families,
  required TAS gates, hard gates, and expected output path
- which evidence artifacts must exist before completion
- whether an `autoresearch` session exists for repeated metric experiments

The calling skill or ticket owns rubric routing. The contract carries handles,
reviewer handoff fields, and TAS gates, not full specialist bodies. Rubric
details remain in `skills/review/references/*`; the reusable handoff template
lives in `skills/review/references/reviewer-handoff.md`; autoresearch session
details remain in `autoresearch.md`, `autoresearch.sh`, and
`autoresearch.jsonl`.

When no honest metric exists, the contract should say `Metrics: none
mechanical` rather than rewarding a fake proxy.

### QA

QA answers:

- what did we run?
- what happened?
- what artifacts prove it?

QA collects:

- logs
- screenshots for UI-bearing work
- commands run
- observed outcomes
- mismatch notes

QA does not decide implementation quality.

### Reviewer

Reviewer answers:

- does the implementation satisfy the work package?
- is the evidence strong enough?
- do ticket-declared metrics trace to real command output, artifacts, or
  autoresearch logs?
- what should be fixed before completion?
- what neighboring repo surfaces were checked to rule out drift or hidden coupling?
- if continuation is required, what is the single best immediate next same-ticket step?

Reviewer is the generic independent review lane, not a code-only specialist.
The coordinating lane should pass a durable task pointer, changed files,
evidence artifacts, review focus, caller-declared rubric families, required TAS
gates, hard gates, and expected output path. The reviewer then executes the
live `review` skill contract, validates the declared routing against the
changed surface, adds any obvious missing hard-gate family with explanation,
and produces TAS rubric judgments, metric-traceability judgment,
evidence-gate judgment, and concrete next action.
For user-facing work, reviewer rubric selection may also include a dedicated
user-intent-satisfaction family so the system can judge "correct" separately
from "actually satisfying for the intended user."
For Stop-hook completion paths, reviewer should ground that judgment through the
live `$review` skill contract in the visible `reviewer` lane, write a linked
completion-review receipt when final completion is being judged, and make one
narrow same-ticket next-step recommendation when continuation is required.

### Stop Hook

Stop hook answers:

- continue same work package
- block for human review
- mark complete

Stop hook should consume QA + reviewer outputs, not replace them.
It should not depend on a separate evidence-review-only role.
On build paths, it should first check the active execution phase contract
mechanically: `impl`, `qa`, and `demo` may each require distinct artifacts
before completion review is even eligible.
On completion paths, it should keep the final sufficiency gate inspectable:
when mechanical artifact gates pass, Stop hook should request one visible
completion-review receipt keyed by a nonce, then validate that linked receipt
instead of hiding the final judgment in another background review pass.
That nonce should be issued only inside an active ticket-backed `impl` loop,
returned to the live lane through the Stop-hook continuation message, and
echoed back in the next final assistant response as
`COMPLETION_PASSWORD: <nonce>` before completion may pass.
On completion paths, it should also require an explicit judgment about whether
the finished artifact would satisfy the saved user ask, not only whether the
ticket and evidence look internally coherent.
For user-facing QA and demo paths, completion review should also judge whether
the final output is presentation-ready enough to show upward to a PM or CEO,
not merely technically valid.
On completion paths, the main model's "done" claim is only a candidate stop.
Reviewer judgment is the authority for whether one obvious in-scope next step
still remains before orchestrator routing is allowed.

## Work Types

The review system should support at least these work types:

- `planning`
- `ui`
- `api`
- `backend`

One review pass can use more than one rubric when a ticket spans multiple
surfaces.

## Normalized Review Output

Reviewer output should use one normalized shape:

```json
{
  "work_type": ["ui", "api"],
  "search_scope": {
    "changed_files": ["src/example.ts"],
    "related_files": ["src/exampleTypes.ts", "docs/specs/example.md"],
    "invariants_checked": ["MEM-0006"],
    "docs_checked": ["skills/review/references/code-quality.md"]
  },
  "rubrics_used": ["ui-quality", "code-quality", "evidence-quality"],
  "summary": "short verdict summary",
  "overall_tas": "TAS-A|TAS-B|TAS-C|TAS-D",
  "verdict": "pass|revise|block|invalid",
  "rerun_required": true,
  "evidence_quality": "pass|fail",
  "integration_readiness": "pass|fail",
  "metric_traceability": "pass|fail|not_applicable",
  "traceability": "pass|fail",
  "freshness": "pass|fail",
  "qa_quality": "pass|fail",
  "demo_quality": "pass|fail",
  "stakeholder_readiness": "pass|fail",
  "stakeholder_readiness_reason": "",
  "best_demo_artifact": "",
  "storyline_gaps": [],
  "user_intent_impression": "pass|fail",
  "user_intent_mismatch_reason": "",
  "obvious_next_step_exists": false,
  "next_step_safe": false,
  "obvious_next_step": "",
  "user_would_expect_more": false,
  "hard_gate_failures": ["evidence-quality"],
  "finding_log": [
    {
      "severity": "high",
      "confidence": "high",
      "rubric": "integration-readiness",
      "summary": "Specific issue that must be addressed",
      "file_refs": ["src/example.ts", "src/exampleTypes.ts"],
      "evidence": ["Short reason grounded in inspected code or artifacts"],
      "next_action": "one concrete remediation step"
    }
  ],
  "rubric_sections": [
    {
      "name": "evidence-quality",
      "tas": "TAS-B",
      "pass": false,
      "checks": {
        "main-claim-proven": true,
        "important-edge-claims-proven": false,
        "claim-artifact-map": false
      },
      "failed_checks": [
        "important-edge-claims-proven",
        "claim-artifact-map"
      ],
      "findings": [
        "Main flow evidence exists, but the packet does not prove the edge-state claims."
      ],
      "next_action": "Capture traceable proof for the missing edge states and rerun review."
    }
  ],
  "blocking_findings": [
    "Specific issue that must be addressed"
  ],
  "next_action": "one concrete next step"
}
```

`search_scope` should stay compact and explain which neighboring surfaces the
review checked beyond the changed file. `finding_log` should stay high-signal:
severity-ranked, evidence-backed, and concrete enough for a builder to act on.
For completion routing, this structured review output should live in the linked
review artifact that the completion receipt points at; Stop hook should validate
the linked receipt plus artifact freshness, not require a second hidden copy of
these fields from an internal role response.

## TAS Review Contract

All review families use the same TAS contract:

- `TAS-A`: pass. Required checks pass, blocker checks do not fail, and evidence
  supports the claim with only minor caveats.
- `TAS-B`: revise. Directionally correct, but one or more repairable required
  checks fail or evidence remains too thin for pass.
- `TAS-C`: block. A blocker check fails, wrong scope or unsafe behavior appears,
  contradictions are material, or core proof is missing.
- `TAS-D`: invalid review. The provided context or evidence is insufficient to
  judge honestly.

Calibration rules:

- use `TAS-A` only when a skeptical reviewer would defend the work as
  pass-worthy without major caveats
- use `TAS-B` for near-miss work that needs a focused repair pass
- use `TAS-C` for material trust failures, unsafe work, wrong-scope work, or
  missing core proof
- use `TAS-D` when review context is insufficient, not when the work is merely
  low quality

Detailed family references should expose modular binary checklist groups, evidence
cues, finding cues, and family-specific TAS guidance so verdicts are easier to
separate. Checklist groups guide inspection; each selected family returns one
TAS verdict and must not average or assign TAS per dimension.

Detailed family anchors live in the per-family review references under:

- `skills/review/references/*.md`

## Threshold Policy

Default:

- `pass` only if every required checklist module passes for each required
  rubric family
- `pass` only if every required rubric family is `TAS-A`
- `pass` only if required ticket metrics are traceable to fresh evidence
- `revise` if work is directionally correct but needs another pass
- `block` if the work is materially off-target, underspecified, or unsafe
- `evidence-quality` below `TAS-A` forces non-pass overall
- `integration-readiness` below `TAS-A` forces non-pass overall
- `qa_quality = fail` forces non-pass overall on completion paths that required QA
- `demo_quality = fail` forces non-pass overall on completion paths that required demo
- `stakeholder_readiness = fail` forces non-pass overall on user-facing completion paths
- `user_intent_impression = fail` forces non-pass overall on completion paths
- `obvious_next_step_exists = true` forces non-pass overall on completion paths
- `user_would_expect_more = true` forces non-pass overall on completion paths

## Reviewer Search Discipline

For code, cleanup, integration, skill, prompt, eval, and evidence-heavy review,
the reviewer should not stop at the changed file when neighboring repo surfaces
likely encode the same rule. The expected path is:

1. changed files and ticket claims
2. directly related interfaces, types, constants, prompts, templates,
   references, or config
3. canonical docs or memory entries for the same invariant
4. nearby tests or evidence artifacts that should prove the claim

This is a targeted search discipline, not permission to wander the whole repo
without a hypothesis.

## Evidence Requirements

### Planning

- plan summary
- data flow / execution flow
- touched areas
- key risks

### UI

- screenshots
- user flow steps
- visible diffs vs intent/design
- supporting logs when relevant

### API

- request/response expectations
- validation / error path proof
- contract/regression evidence

### Backend

- state/data correctness
- error handling
- regression evidence
- logs/tests where relevant

## Integration Rule

Every active feature work package should define:

- which review rubrics apply
- what QA must collect
- what TAS gate matters

For build/documenting completion paths, a fresh review result plus a traceable
evidence pack are required completion-gate artifacts. Missing, malformed, weak,
contradictory, stale, or untraceable review output or evidence must prevent
completion even when checklist boxes are checked.
When Stop hook requests visible completion review, the ticket must also link a
fresh `completion-review` receipt artifact under `tickets/TASK-XXXX/artifacts/review/`
that includes the requested nonce, the artifacts reviewed, the verdict, and the
user-query satisfaction judgment.
The next final assistant response must also include
`COMPLETION_PASSWORD: <nonce>` matching that same receipt; password text alone
is not sufficient without the linked receipt artifact.

The ticket should link those artifacts from `Evidence`; it should not prefill an
empty review-output stub in advance.
