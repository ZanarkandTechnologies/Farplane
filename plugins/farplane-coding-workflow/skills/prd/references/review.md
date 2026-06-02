# PRD Review

Run this review before handing off the PRD.
If any answer is weak, tighten the PRD first.

## Must Pass

- Does the problem statement make sense in plain language?
- Does the PRD explain who the user is and what job they are trying to get done?
- Is the proposed slice actually helpful, not just interesting to build?
- Does the PRD explain why this is the right first slice instead of a bigger or different one?
- Are constraints, risks, and non-goals concrete enough to steer implementation decisions?
- Are metric candidates honest, mechanical, and useful when present, or does
  the PRD explicitly say no honest mechanical metric exists?
- Does `Autonomy Readiness` name the user inputs, credentials, compute, tools,
  QA risks, and human gates an agent would otherwise discover too late?

## Ask If Relevant

- Is this really the best way to help the user, or just the easiest thing to ship?
- Are we solving a real pain point or inventing unnecessary product surface?
- Is there a simpler path that would help the user sooner?
- Are there user assumptions here that still need confirmation?

## Fail If

- the audience or JTBD is vague
- the slice is too broad to guide the next step cleanly
- success is described only in technical terms, not user terms
- metric candidates are subjective proxies pretending to be mechanical proof
- the document reads like implementation notes instead of product intent
- autonomy-readiness questions are missing for a feature expected to run
  unattended or through `$ralph`
