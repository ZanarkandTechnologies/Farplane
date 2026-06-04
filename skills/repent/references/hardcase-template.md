# Hardcase Template

Use this shape for `repent hardcase` artifacts.

```markdown
# <short title>

Captured: YYYY-MM-DD HH:mm Z
Privacy: local_only|redacted_shareable|training_candidate
Failure class: missed_instruction|failed_to_act|wrong_tool|premature_completion|checklist_drift|weak_review|other

## Original Task

<one paragraph>

## Observed Failure

<what the agent did wrong>

## User Correction

<what the operator said should have happened>

## Correct Behavior

<the behavior future agents should learn>

## Fixed Outcome

<what changed once the issue was fixed>

## Evidence Refs

- <path or bounded excerpt>

## Future Eval Idea

<one concrete eval assertion or task>

## Open Risks

- <privacy, ambiguity, or incompleteness caveat>
```
