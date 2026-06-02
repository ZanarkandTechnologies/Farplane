# User Intent Satisfaction

Use when reviewing whether a user-facing artifact actually satisfies the user
ask, not merely whether it is technically correct.

Required TAS: `TAS-A`

## Family TAS Guide

- `TAS-C`: the result clearly misses the user ask, solves the wrong problem, or is
  so underpowered that it would feel like a failure to the intended user
- `TAS-B`: some useful work exists, but the result still undershoots the ask badly
  enough that a user would feel the main promise was not met
- `TAS-B`: directionally satisfies the ask, but still feels ordinary, incomplete,
  or weaker than the ticket/user framing implied
- `TAS-A`: clearly satisfies the ask and feels worth the user’s effort, with only
  minor caveats
- `TAS-A`: strongly satisfies or impresses the user ask and is hard to improve
  materially within scope

## Dimensions

- `ask-fidelity`
- `outcome-completeness`
- `worth-it-feel`
- `impressiveness`
- `evidence-confidence`

### `ask-fidelity`

Inspect: whether the delivered artifact actually matches what the user asked
for, not just what the implementer happened to build.

Ask:

- Does this solve the user’s stated problem or only an adjacent technical one?
- What part of the user ask is still missing, diluted, or misread?

### `outcome-completeness`

Inspect: whether the important promised outcome is fully delivered rather than
partially gestured at.

Ask:

- Would the user feel the main job was completed?
- Is the result technically valid but still missing the key payoff?

### `worth-it-feel`

Inspect: whether the result would feel meaningfully useful or worthwhile to the
intended user given the ticket’s framing.

Ask:

- Does this materially reduce friction or create meaningful value for the user?
- Would a reasonable user feel this change was worth having, not just nice in theory?

### `impressiveness`

Inspect: whether the result merely clears a correctness bar or also meets the
strength, boldness, or quality level implied by the ask.

Ask:

- Is this just acceptable, or does it actually feel like the response the ask
  called for?
- If the ticket or user asked for something high-leverage, bold, polished, or
  user-delighting, did we actually get there?

### `evidence-confidence`

Inspect: whether the review has enough ticket/evidence/output context to make a
strong satisfaction judgment without bluffing.

Ask:

- Do we have enough evidence to say this satisfies the ask, or are we filling
  gaps with intuition?
- Are stronger market or willingness-to-pay claims being made without explicit
  ticket evidence for user segment, alternatives, or pricing?

## Evidence and Finding Cues

- Weak evidence usually looks like a technically working result that still feels
  too small, too generic, or too off-center for the ask.
- Ordinary evidence usually solves the problem in a basic way but leaves clear
  value or polish on the table.
- Strong evidence shows the result directly mapping to the ask, with meaningful
  user payoff rather than just implementation cleanliness.
- Exceptional evidence makes it obvious why the user would feel the request was
  satisfied and why the outcome feels notably strong within scope.
- Findings should name the exact ask mismatch or underdelivered payoff instead
  of using vague phrases like "not compelling enough."

## Guardrail on Market Claims

This family is about user-intent satisfaction first.

Do **not** turn it into a generic pricing or market-viability rubric unless the
ticket/spec already contains:

- explicit user segment
- explicit alternatives or substitutes
- explicit price-point or willingness-to-pay evidence

Without that evidence, TAS `evidence-confidence` lower and keep the judgment
at the user-ask level instead of bluffing market truth.

## Example Judgments

- `TAS-B` example:
  the change technically works, but the user asked for a high-leverage workflow
  improvement and the result is only a small cleanup that does not noticeably
  change the user experience.
- `TAS-B` example:
  the result addresses the stated ask and would help somewhat, but it still
  feels ordinary or incomplete relative to the user-facing promise.
- `TAS-A` example:
  the result clearly delivers the requested outcome and feels worth shipping to
  the intended user, with only minor caveats in polish or edge scope.
- `TAS-A` example:
  the result not only fulfills the ask but feels especially strong, satisfying,
  or high-leverage within the ticket’s scope and evidence.

## Review Artifact Attachment

Attach this rubric in the linked review artifact when used:

- `tas`
- `required_tas`
- `pass`
- `dimension_tas`
- `findings`
- `next_action`
