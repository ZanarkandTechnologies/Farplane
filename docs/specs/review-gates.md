# Review Gates

Date: 2026-04-09

## Goal

Define the canonical review-gate model for the spec-first execution loop.

The system uses three distinct layers:

1. **QA** collects evidence
2. **Reviewer** scores the work against a rubric
3. **Stop hook** sanity-checks whether the evidence and review verdict justify
   completion or continuation

## Roles

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
- what should be fixed before completion?
- what neighboring repo surfaces were checked to rule out drift or hidden coupling?
- if continuation is required, what is the single best immediate next same-ticket step?

Reviewer produces the rubric score, evidence-gate judgment, and concrete next action.
For user-facing work, reviewer rubric selection may also include a dedicated
user-intent-satisfaction family so the system can judge "correct" separately
from "actually satisfying for the intended user."
For Stop-hook completion paths, reviewer should ground that judgment through the
live `$review` skill contract and then make one narrow `$consultant-thinking`
recommendation for the best immediate same-ticket next step when continuation is
required.

### Stop Hook

Stop hook answers:

- continue same work package
- block for human review
- mark complete

Stop hook should consume QA + reviewer outputs, not replace them.
It should not depend on a separate evidence-review-only role.
On completion paths, it should also require an explicit judgment about whether
the finished artifact would satisfy the saved user ask, not only whether the
ticket and evidence look internally coherent.
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
  "overall_score": 3.9,
  "overall_threshold": 4.0,
  "verdict": "pass|revise|block",
  "rerun_required": true,
  "evidence_quality": "pass|fail",
  "integration_readiness": "pass|fail",
  "traceability": "pass|fail",
  "freshness": "pass|fail",
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
      "score": 3.2,
      "threshold": 4.0,
      "pass": false,
      "dimension_scores": {
        "sufficiency": 3.0,
        "traceability": 3.0,
        "inspectability": 3.5
      },
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

## Anchored Review Scale

All review families use the same anchored `1.0`-to-`5.0` scale:

- `1.0`: failing, unsafe, contradictory, or largely absent
- `2.0`: partially relevant, but still weak enough that key claims depend on
  reviewer inference, thin proof, or unresolved defects
- `3.0`: acceptable and directionally correct, but still ordinary or caveated
- `4.0`: strong, trustworthy, and pass-worthy with only minor caveats
- `5.0`: exemplary, persuasive, and hard to improve materially within scope

Calibration rules:

- use `2.0` when there is some real work, but not enough trust to treat the
  result as close to review-ready
- use `4.0` only when a skeptical reviewer would defend the work as pass-worthy
  without major caveats
- reserve `5.0` for clearly above-bar work with positive evidence, not just
  lack of obvious defects

Detailed family references should add skeptic questions, evidence cues, and
family-specific score guidance so adjacent bands are easier to separate.

Detailed family anchors live in the per-family review references under:

- `skills/review/references/*.md`

## Threshold Policy

Default:

- `pass` only if every required dimension passes its threshold
- `pass` only if every required rubric family passes its threshold
- `revise` if work is directionally correct but needs another pass
- `block` if the work is materially off-target, underspecified, or unsafe
- `evidence-quality` below threshold forces non-pass overall
- `integration-readiness` below threshold forces non-pass overall
- `user_intent_impression` below threshold forces non-pass overall on completion paths
- `obvious_next_step_exists = true` forces non-pass overall on completion paths
- `user_would_expect_more = true` forces non-pass overall on completion paths

## Reviewer Search Discipline

For code, cleanup, integration, and evidence-heavy review, the reviewer should
not stop at the changed file when neighboring repo surfaces likely encode the
same rule. The expected path is:

1. changed files and ticket claims
2. directly related interfaces, types, constants, or config
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
- what pass threshold matters

For Ralph build/documenting completion paths, the ticket `Review Packet` is a
required completion-gate artifact. Missing, malformed, weak, contradictory,
stale, or untraceable packet state must prevent completion even when checklist
boxes are checked.

The ticket remains the place where that requirement is declared.
