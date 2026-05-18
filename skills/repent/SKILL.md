---
name: repent
description: Operator-forced recovery mode for when the assistant missed something obvious, got defensive, or explained instead of acting. Use when the user explicitly says `repent` or otherwise clearly asks for audit-then-fix behavior on the current task after the default correction-recovery behavior was not enough.
tier: 2
---

# Repent

`repent` is an operator-visible recovery skill.

Use it when the assistant has likely missed an obvious requirement and the user
wants the agent to stop defending itself, verify the complaint, and recover
immediately, with an explicit operator-forced audit-then-fix posture.

Do not use it for broad new work, destructive requests, or ambiguous direction
changes. This is a same-task recovery skill, not a replacement for planning.
Ordinary complaint-shaped follow-ups such as "why are we not doing that" should
already be handled by the default global correction-recovery contract; `repent`
is for when the operator explicitly wants a stricter audit-then-fix pass.

## Recovery Workflow

1. Read the active ticket, current artifact, and the user complaint first.
2. Check whether the complaint is actually true before apologizing or acting.
3. Classify the situation into one of three buckets:
   - `true_miss`: the assistant really missed or failed to complete requested work
   - `false_alarm`: the work is already done or the complaint is based on stale context
   - `ambiguous`: the complaint is plausible, but the exact target or expected action is unclear
4. If `true_miss` and the recovery is safe and same-scope:
   - acknowledge briefly
   - do the fix now
   - report the concrete action taken
5. If `false_alarm`:
   - do not perform fake repentance
   - respond briefly with concrete evidence of what is already done
6. If `ambiguous`:
   - ask the minimum blocking question
   - do not launch into a long postmortem

## Response Contract

- Preferred recovery opener when the complaint is real:
  - `Sorry, I'll do that now.`
- Avoid:
  - long explanations of why the miss happened before checking or fixing it
  - defensive tone
  - pretending a miss happened when it did not
  - converting the complaint into a new planning exercise unless the request is actually branching

## Safe Boundary

`repent` may auto-recover only when all of these are true:

- the complaint is about the current task or immediately preceding requested work
- the target artifact or missing action is clear
- the recovery is reversible and non-destructive
- no new material product, architecture, or workflow decision is required

Stop and ask instead when:

- the complaint would require deleting or publishing something
- the requested recovery changes scope materially
- multiple plausible recovery targets exist
- the user is actually disputing direction, not just a missed action

## Deterministic Fixtures

Read [references/fixtures.md](references/fixtures.md) and apply the matching
fixture before responding. The fixtures cover:

- direct missed action
- missing tests
- missing docs
- false alarm
- unsafe branching complaint

## Output Shape

Keep the first response compact:

- `Reality check:` true miss, false alarm, or ambiguous
- `Action:` what you are doing now, or the minimum blocking question
- `Result:` what changed, or what evidence shows the complaint was false

## Notes

- This skill is an operator escape hatch. The default global contract should
  already behave proactively; `repent` exists for when it does not.
- When the complaint is real, action beats explanation.
- When the complaint is false, evidence beats apology.
