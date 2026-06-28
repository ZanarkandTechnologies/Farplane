# Impl Plan Examples

## Good

````md
## Summary
Make the ticket template approval-ready for `impl-plan(ticket)` and
`goal-advisor(ticket)` without duplicating execution details across separate
sections. The ticket keeps the human contract compact, while Goal sidecars own
loop configuration after approval.

## Scope
- `In:` `skills/impl-plan/SKILL.md`, `prompts/plan.md`,
  `references/template.md`, `references/review.md`, `references/examples.md`,
  `tickets/templates/ticket.md`, `tickets/README.md`
- `Out:` changing Goal runtime behavior, adding parser syntax, or migrating
  archived tickets

## Delta
- `Before:` tickets split executable intent across `Program`, `Map`, and
  body `State`, so builders cross-reference sections before acting.
- `After:` tickets use `Delta` for brief before/after framing and `Change Plan`
  units for local before/after, read/write surfaces, operation, routes, proof,
  and failure modes.
- `Why now:` `goal-advisor(ticket)` needs a clean approved contract to compile
  `program.md`, `progress.md`, and the native `/goal` prompt without transcript
  memory.

## Change Plan

### Change 1: Merge execution detail

```text
fixes:
  - Ticket templates teach separate executable sections.
before:
  - Readers cross-map execution order, file touches, and proof from different
    sections.
after:
  - Each change unit carries the local files, operation, routes, QA, and
    failure modes needed to execute without cross-section mapping.
read:
  - path: tickets/README.md
    reason: canonical body contract
  - path: skills/impl-plan/references/template.md
    reason: emitted plan shape
write:
  - path: tickets/templates/ticket.md
    change: replace old body defaults with Change Plan, Done, QA Strategy, and Links
  - path: skills/impl-plan/prompts/plan.md
    change: make Change Plan the required execution structure
operation:
  - Update template, README, prompt, checklist, and validators together.
signature_or_type_impact:
  - ticket_change_plan(delta, change_units, qa_strategy) ->
    artifact_delta + evidence + state_delta
routes:
  docs: doc-advisor
  qa: tests
  review: inline
qa:
  - Run ticket metadata, harness invariant, doc parity, and skill registry
    validators.
failure_modes:
  - Leaving examples or validators that still require old body sections.
```

## Done
- `done_when:` new tickets and impl-plan drafts use `Change Plan` as the
  executable program/map surface.

## QA Strategy
- `proof_weight:` tests
- `checks:` run `python3 skills/skill-maintenance/scripts/check_skills.py --write`
- `manual:` inspect the active ticket and impl-plan surfaces for stale default
  execution, file-map, body-state, and goal-preview sections.
- `review:` Change Plan locality, goal-advisor readiness, docs strategy, proof
  clarity.
- `goal_advisor_inputs:` proof route `tests + inline review`, final evidence
  `validator output`, final checkpoint `none`

## Notes
- `Blast radius:` future ticket plans become easier for `goal-advisor` to
  compile after approval.
- `Risks / rollback:` large architecture tickets may still need a linked
  `plan.md`; keep that as an escape hatch rather than bloating every ticket.
- `Citations:` `MEM-0061`, `MEM-0062`, `MEM-0086`
- `Blockers:` none
````

## Bad

```md
We should improve the plan a bit and maybe add some more detail about types later.
```

Why bad:

- no before/after delta
- no local change units or code seams
- no executable task program
- no concrete done/proof
- no rationale for optional sections
- still sounds like hand-wavy prose instead of a believable ticket plan
