# Review Gates

Date: 2026-04-07

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

Reviewer produces a rubric score and feedback.

### Stop Hook

Stop hook answers:

- continue same work package
- block for human review
- mark complete

Stop hook should consume QA + reviewer outputs, not replace them.

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
  "rubrics_used": ["ui-rubric", "api-rubric"],
  "summary": "short verdict summary",
  "overall_score": 82,
  "overall_threshold": 85,
  "verdict": "pass|revise|block",
  "rerun_required": true,
  "dimensions": [
    {
      "name": "functionality_correctness",
      "score": 78,
      "threshold": 85,
      "pass": false,
      "feedback": "Specific failure reason"
    }
  ],
  "blocking_findings": [
    "Specific issue that must be addressed"
  ],
  "next_action": "one concrete next step"
}
```

## Rubric Dimensions

All work should be scored against:

- functionality correctness
- regression / integration safety
- evidence adequacy

Additional work-type-specific dimensions may be added by rubric.

## Threshold Policy

Default:

- `pass` only if every required dimension passes its threshold
- `revise` if work is directionally correct but needs another pass
- `block` if the work is materially off-target, underspecified, or unsafe

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

The ticket remains the place where that requirement is declared.
