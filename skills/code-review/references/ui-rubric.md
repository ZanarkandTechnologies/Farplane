# UI Rubric

Use when the work package changes UI, interaction, layout, routing, or visible
product behavior.

Required dimensions:

- functionality correctness
- design intent fidelity
- interaction quality
- regression safety
- evidence adequacy

Questions:

- Does the feature behave correctly for the intended user flow?
- Does it match the declared design/spec intent closely enough?
- Are primary and edge states covered?
- Is there visible regression risk?
- Do screenshots/logs actually prove the claim?

Default threshold:

- weak or missing screenshots should force `revise`
- visible mismatch against design intent should force `revise`
