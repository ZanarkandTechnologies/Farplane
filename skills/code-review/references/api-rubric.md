# API Rubric

Use when the work package changes API routes, payload contracts, validation, or
service boundaries.

Required dimensions:

- contract correctness
- validation and error handling
- backward / regression safety
- evidence adequacy

Questions:

- Are inputs and outputs correct and explicit?
- Are invalid inputs and failure paths handled properly?
- Does the change break existing callers or assumptions?
- Is there enough evidence that the contract actually works?

Default threshold:

- any contract ambiguity should force `revise`
- missing error-path proof should force `revise`
