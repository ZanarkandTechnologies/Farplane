# Backend Rubric

Use when the work package changes backend logic, persistence, jobs, or internal
state transitions.

Required dimensions:

- functionality correctness
- state / data correctness
- error handling
- regression safety
- evidence adequacy

Questions:

- Does the logic do the right thing?
- Are data and state transitions coherent and safe?
- Are failures handled and surfaced?
- Does the change introduce obvious regression risk?
- Is there enough proof to trust the result?

Default threshold:

- missing state/data proof should force `revise`
- unsafe error handling should force `revise`
