# Impl Plan Review

Run this review before handing off the plan.
If any answer is weak, tighten the plan first.

## Must Pass

- Is this still one commit, or should it be split?
- Did the plan actually use the right references: PRD, specs, ticket, memory, troubles, code?
- For material work, does the top of the plan include a useful Mermaid delta diagram with a clear legend?
- Does `B -> A` explain the change clearly near the top?
- Does `Core Flow` show the minimum data-flow or pseudocode needed to make the approach believable?
- If interface shape matters, are the key signatures embedded directly in the diagram nodes?
- Are the proof points concrete and observable?
- Are risk and rollback clear enough for the size of the change?
- Is the plan concise enough for fast approval without hiding critical detail?
- If narrative sections are present, are they concrete and distinct rather than duplicated filler?
- If the work is material or ambiguous, did the plan actually include the required story/example sections?

## Ask If Relevant

- Are we reusing the right modules and components?
- Are we introducing new files or abstractions without enough justification?
- Are we saying too much for a straightforward change?
- Are we saying too little for a risky or unfamiliar path?
- Would a reviewer understand how the change happens without reading an appendix?
- Did we accidentally write an essay where one compact system map plus one data-flow view would be clearer?
- If the ticket depends on a `Test hook`, is that hook clearly good enough to support deterministic proof before build starts?
- Is the top approval surface still short enough to skim quickly?

## Fail If

- multi-commit scope is hidden inside a "single" plan
- references were skipped without saying so
- proof is generic rather than observable
- a material plan is prose-only when a compact diagram would obviously clarify the change
- separate before/after diagrams are used even though one delta map would be clearer
- the plan depends on tricky setup but never checks whether the ticket's `Test hook` is sufficient
- the plan explains everything except the actual delta
- the approval surface is bloated, vague, or unconvincing
- `User Story` restates the title without actor, need, and outcome
- `High-Fidelity Example` is placeholder text, generic boilerplate, or duplicates `Summary`
- narrative sections are present only decoratively and do not improve implementation clarity
