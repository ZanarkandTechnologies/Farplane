# Impl Plan Review

Run this review before handing off the plan.
If any answer is weak, tighten the plan first.

## Must Pass

- Is this still one coherent build-and-proof loop, or did a real split boundary emerge?
- Did the plan actually use the right references: PRD, specs, ticket, memory, troubles, lessons, code?
- Does the ticket stay in the canonical single-surface body shape instead of a
  parallel reviewer-versus-implementer document?
- Does the plan organize around `Summary`, `Scope`, `Delta`, `Change Plan`,
  `Done`, `QA Strategy`, `Docs Strategy`, `Links`, and sparse `Notes`, with
  `Agent Contract` or `Run Hints` only when warranted?
- Is the before/after delta clear enough to approve without reading an
  appendix?
- Does each material Change Plan unit carry local before/after, read/write
  surfaces, operations, routes, QA expectations, and failure modes?
- Is each material Change Plan unit in its own heading and fenced block, using
  plain `fixes:` text instead of synthetic labels unless anchors are truly
  needed?
- When a visual map would make material work easier to understand, does the
  plan include one compact Mermaid map inside `Change Plan`?
- If interface shape matters, are the key callable seams visible in the
  relevant Change Plan unit?
- If typed data flow matters, is a representative payload or state path visible
  in the relevant Change Plan unit or optional visual map?
- Are QA Strategy points concrete and observable?
- Are risk, rollback, and human gates clear enough for the size of the change?
- Is the Change Plan detailed enough to execute without inventing missing steps
  while still staying skimmable?
- If optional sections are present, are they concrete and distinct rather than
  duplicated filler?
- Is the recommendation phrased as a decision when a real decision exists?
- Are citations present only when they ground a claim, decision, or external
  expectation?
- Is planning evidence omitted unless the user explicitly requested audit
  detail?

## Ask If Relevant

- Are we reusing the right modules and components?
- Are we introducing new files or abstractions without enough justification?
- Are we saying too much for a straightforward change?
- Are we saying too little for a risky or unfamiliar path?
- Would a reviewer understand how the change happens from the Change Plan
  without reading a separate execution brief?
- Did we accidentally write an essay where one optional system map with inline
  seams and one numbered data-flow path would be clearer?
- Did we bury the trust-building code understanding below the fold instead of
  showing changed seams in the relevant change unit?
- Does the plan still sound timid even though the recommended path is already
  clear?
- If the ticket depends on a `Test hook`, is that hook clearly good enough to
  support deterministic proof before build starts?
- Is the top approval surface still short enough to skim quickly?
- If a split is proposed, is it because of proof, reuse, blocker risk, or runtime boundary rather than commit count?
- Are `Options considered`, `Gap Analysis`, `Run Hints`, `Agent Contract`, or
  sidecar `plan.md` present because the ticket truly needs them?

## Fail If

- the plan forces a split only because the work spans multiple commits
- multiple independent build loops are hidden inside a "single" plan without naming a boundary
- references were skipped without saying so
- QA Strategy is generic rather than observable
- the ticket invents `Human` / `Agent` lanes instead of using the canonical
  single-surface contract
- a material plan omits local Change Plan units and forces readers to
  cross-map separate sections
- a material plan omits a compact optional map even though the flow, ownership,
  changed seams, or typed data path would be easier to understand visually
- separate before/after diagrams are used even though one map would be clearer
- the plan changes interfaces or ownership seams but never names them in the
  relevant Change Plan unit
- the plan depends on typed payload continuity but never shows the state or
  payload path in the relevant Change Plan unit or optional map
- the ticket needs sequencing but omits `Change Plan`
- the plan depends on tricky setup but never checks whether the ticket's `Test hook` is sufficient
- the plan explains everything except the actual delta
- the plan hides behind tentative "maybe/could" language instead of making a
  recommendation and ordered execution call
- the approval surface is bloated, vague, or unconvincing
- optional sections are present only decoratively and do not improve implementation clarity
- `Evidence` appears as default planning boilerplate instead of explicit audit
  detail requested by the user
- `Refs` appears as a citation dump instead of inline or compact citations that
  ground the plan
