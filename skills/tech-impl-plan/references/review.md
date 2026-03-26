# Tech Impl Plan Review

Run this review before handing off the plan.
If any answer is weak, tighten the plan first.

## Must Pass

- Is this still one commit, or should it be split?
- Did the plan actually use the right references: PRD, specs, ticket, memory, troubles, code?
- Does `B -> A` explain the change clearly near the top?
- Does `Core Flow` show the minimum code or pseudocode needed to make the approach believable?
- Are the proof points concrete and observable?
- Are risk and rollback clear enough for the size of the change?
- Is the plan concise enough for fast approval without hiding critical detail?

## Ask If Relevant

- Are we reusing the right modules and components?
- Are we introducing new files or abstractions without enough justification?
- Are we saying too much for a straightforward change?
- Are we saying too little for a risky or unfamiliar path?
- Would a reviewer understand how the change happens without reading an appendix?
- If the ticket depends on a `Test hook`, is that hook clearly good enough to support deterministic proof before build starts?

## Fail If

- multi-commit scope is hidden inside a "single" plan
- references were skipped without saying so
- proof is generic rather than observable
- the plan depends on tricky setup but never checks whether the ticket's `Test hook` is sufficient
- the plan explains everything except the actual delta
- the approval surface is bloated, vague, or unconvincing
