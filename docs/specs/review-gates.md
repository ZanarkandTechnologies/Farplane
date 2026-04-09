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

Reviewer produces the rubric score, evidence-gate judgment, and concrete next action.

### Stop Hook

Stop hook answers:

- continue same work package
- block for human review
- mark complete

Stop hook should consume QA + reviewer outputs, not replace them.
It should not depend on a separate evidence-review-only role.

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
  "hard_gate_failures": ["evidence-quality"],
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
