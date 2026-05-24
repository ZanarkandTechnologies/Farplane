# Impl Plan Review

Run this review before handing off the plan.
If any answer is weak, tighten the plan first.

## Must Pass

- Is this still one coherent build-and-proof loop, or did a real split boundary emerge?
- Did the plan actually use the right references: PRD, specs, ticket, memory, troubles, code?
- Does the ticket stay in the canonical single-surface body shape instead of a
  parallel reviewer-versus-implementer document?
- When the flow, ownership, or typed data path is not obvious from the file
  map alone, does the plan include a useful Mermaid delta diagram with a clear
  legend?
- Is the `Signature delta` present when interface shape or ownership boundaries matter?
- If typed data flow matters, are `Type Sketch` and `Typed flow example`
  present and believable?
- If interface shape matters, are the key signatures either embedded in the
  diagram nodes or captured in the `Signature delta`?
- Are the proof points concrete and observable?
- Are risk and rollback clear enough for the size of the change?
- Is the plan detailed enough to execute without inventing missing steps while
  still staying skimmable?
- If optional sections are present, are they concrete and distinct rather than duplicated filler?
- If the work is material or ambiguous, did the plan actually include the
  required type-flow detail?
- If sequencing matters, do `Execution steps` tell the builder what to do
  first, next, and last?
- Is the recommendation phrased as a decision, not a hedge?

## Ask If Relevant

- Are we reusing the right modules and components?
- Are we introducing new files or abstractions without enough justification?
- Are we saying too much for a straightforward change?
- Are we saying too little for a risky or unfamiliar path?
- Would a reviewer understand how the change happens without reading an appendix?
- Did we accidentally write an essay where one system map plus one data-flow
  view would be clearer?
- Did we bury the trust-building code understanding below the fold instead of
  showing compact callable seams and type shapes in the `Plan` section?
- Does the plan still sound timid even though the recommended path is already
  clear?
- If the ticket depends on a `Test hook`, is that hook clearly good enough to support deterministic proof before build starts?
- Is the top approval surface still short enough to skim quickly?
- If a split is proposed, is it because of proof, reuse, blocker risk, or runtime boundary rather than commit count?

## Fail If

- the plan forces a split only because the work spans multiple commits
- multiple independent build loops are hidden inside a "single" plan without naming a boundary
- references were skipped without saying so
- proof is generic rather than observable
- the ticket invents `Human` / `Agent` lanes instead of using the canonical
  single-surface contract
- a material plan omits a compact diagram even though the flow, ownership, or
  typed data path is not obvious from the file map alone
- separate before/after diagrams are used even though one delta map would be clearer
- the plan changes interfaces or ownership seams but never names them in a
  compact `Signature delta`
- the plan depends on typed payload continuity but never names the structs or
  data evolution with a `Type Sketch` and `Typed flow example`
- the ticket needs sequencing but omits `Execution steps`
- the plan depends on tricky setup but never checks whether the ticket's `Test hook` is sufficient
- the plan explains everything except the actual delta
- the plan hides behind tentative "maybe/could" language instead of making a
  recommendation and ordered execution call
- the approval surface is bloated, vague, or unconvincing
- the typed example is placeholder text, generic boilerplate, or a schema dump
- optional sections are present only decoratively and do not improve implementation clarity
