---
name: doc-advisor
description: "Turn ticket, plan, or durable doc changes into a docs strategy or grounded doc update with doc-quality checks."
tier: 2
source: local
template_uses:
  skill-template: "0.3.6"
  skill-qa-checklist: "0.1.0"
  skill-eval-task: "0.2.0"
methods:
  - id: doc-advisor:strategy
    class: internal
    output: docs-strategy
  - id: doc-advisor:doc-architecture
    class: internal
    output: docs-architecture
  - id: doc-advisor:metadata
    class: internal
    output: metadata-contract
  - id: doc-advisor:feature-system-spec
    class: internal
    output: feature-system-spec
  - id: doc-advisor:finish-gate
    class: internal
    output: docs-finish-verdict
eval: evals/evals.json
qa_checklist: qa_checklist.md
---

# Doc Advisor Skill

## Context

`doc-advisor` owns docs strategy, durable repo doc writing, and doc-quality
review. Use it for material tickets that need an explicit docs decision, and for
substantive Markdown docs, feature specs, system specs, runbooks, templates,
registry companions, and public guidance.

For material ticket planning, return a compact `Docs Strategy` decision:
`update_docs` with target docs and validation, or `no_docs` with a concrete
reason. Do not model routine ticket closure as a field; closing tickets remains
the lifecycle invariant owned by `close-ticket`.

Ground source claims through [reference-grounding](../reference-grounding/SKILL.md)
when they depend on local canonical files, official behavior, current facts, peer
norms, standards, or implementation examples. This skill turns grounded evidence
into docs with the right reader contract, owner surface, metadata, and proof path.

Documentation architecture lore belongs in [Documentation OS](../../docs/systems/documentation-os.md).
This skill owns the executable workflow and branch-loaded references.

## Skill Signature

```text
doc_advisor(doc_task, target_file?, evidence?, doc_type?) -> docs_strategy | doc_delta + doc_quality_result + review_route?
state: reads(ticket/plan/diff?, target doc?, nearest owner/index, source/evidence refs, qa_checklist.md, selected references); writes(Docs Strategy block, target doc, optional audit/proof notes)
gates: docs_strategy_decided; reader_contract_bound_when_writing; owner_surface_chosen; claims_grounded; metadata_checked; checklist_applied; material_review_routed_or_skipped
routes: reference-grounding | review
fails: stale or ungrounded docs; duplicate source-of-truth; wrong feature/system boundary; agent-facing prose in human docs; routine closeout expansion; no-docs decision without reason
```

## Phase Boundary

This skill follows Tier 0 phases inline. Call `review` only when the doc is
canonical, public, cross-surface, policy-bearing, or a completion claim that
needs independent judgment; name `documentation-quality` as the review family
when asking for a TAS verdict. When placement or feature-vs-system
classification has real tradeoffs, compare the viable choices inline and
recommend one.

<!-- BEGIN FARPLANE_IMPORTANT_CHECKLIST -->
## Todo List

- [ ] 1. Bind the reader, surface, and branch.
  - [ ] If the task is ticket or implementation planning, first produce
    `Docs Strategy` with `outcome`, `doc_targets`, `no_docs_reason`, and
    `validation`.
  - [ ] For durable doc writing, name audience, doc type, owning file, source
    of truth, intended next action, canonical terms, and proof surface.
  - [ ] If `qa_checklist.md` exists, read it now as preflight guardrails.
  - [ ] Choose exactly the needed branch references:
    [doc architecture](references/doc-architecture.md) for placement,
    [metadata](references/metadata-and-registries.md) for front matter or
    registries, [feature/system specs](references/feature-system-specs.md) for
    `FEAT-*` or `SYS-*` decisions, and [finish gate](references/finish-gate.md)
    before material doc closeout.
- [ ] 2. Ground claims.
  - [ ] Use `reference-grounding` for local, official, current, peer, or
    standard-dependent claims.
  - [ ] Keep task-local proof in tickets or artifacts until it is distilled into
    a durable owner.
- [ ] 3. Draft or revise for the reader's next action.
  - [ ] Put the current definition, decision, workflow, or task path near the top.
  - [ ] Use one canonical term per concept and link to the owner instead of
    copying long doctrine.
  - [ ] Keep examples current, complete enough to use, and matched to doc type.
- [ ] 4. Update metadata and generated views only when required.
  - [ ] Use the selected branch reference before changing front matter, feature
    refs, system refs, registries, or template metadata.
  - [ ] Treat generated registries as outputs: update source docs or front
    matter, then run the generator or validator; never hand-edit generated
    JSONL registry rows.
- [ ] 5. Finish-check and route review.
  - [ ] Apply `qa_checklist.md` again to the finished work.
  - [ ] Preserve failed checks, fixes made, deferrals, remaining risk, and the
    exact review route instead of collapsing readiness into a scalar score.
  - [ ] Run only relevant validators or focused searches.
  - [ ] Route material readiness through [review](../review/SKILL.md) with
    `documentation-quality` when checklist inspection is not enough.
<!-- END FARPLANE_IMPORTANT_CHECKLIST -->

## Templates

```text
docs_strategy = {
  outcome: update_docs | no_docs,
  doc_targets,
  no_docs_reason,
  validation
}
```

```text
doc_contract = {
  audience,
  doc_type,
  owning_file,
  source_of_truth,
  intended_next_action,
  canonical_terms,
  metadata_schema,
  proof_surface
}
```

## Gotchas

- Do not create a new doc when an existing owner has the same audience,
  lifecycle, and retrieval path.
- Do not promote a broad subsystem into a single feature doc; use a system spec
  when multiple capabilities or boundaries are being governed.
- When narrowing a feature doc after a system split, keep the capability
  behavior, surfaces, proof, limits, and maintenance path explicit.
- Do not treat skill references as canonical lore owners. System or feature
  docs own durable policy; skill references own executable branch workflow.
- Do not cite external best practices as Farplane policy unless the doc labels
  them as grounded synthesis or local policy.
- Do not use numeric doc scores as readiness proof; use failed checks, reasons,
  fixes, deferrals, remaining risk, evidence, and next action.
- Do not soften generated-registry ownership. Generated registry files are
  outputs, not sources of truth; update canonical docs and regenerate them.
- After moving feature/system boundaries, name concrete proof such as
  `python3 docs/features/validate_features.py`, `python3 bin/validators/check_doc_refs.py`,
  and `python3 skills/skill-maintenance/scripts/check_skills.py --write` when
  those surfaces changed.

## Reference Map

- [qa_checklist.md](qa_checklist.md) - read at preflight and finish for durable,
  canonical, public, or material documentation changes.
- [references/doc-architecture.md](references/doc-architecture.md) - read when
  owner surface, doc type, split/merge/delete, density, or lifecycle is unclear.
- [references/metadata-and-registries.md](references/metadata-and-registries.md)
  - read when front matter, feature refs, system refs, templates, or generated
  registries may change.
- [references/feature-system-specs.md](references/feature-system-specs.md) -
  read when deciding feature vs system vs local reference vs ticket artifact.
- [references/finish-gate.md](references/finish-gate.md) - read before claiming
  material docs are ready.
- [../reference-grounding/SKILL.md](../reference-grounding/SKILL.md) - compact
  evidence for local, official-doc, current-source, or peer claims.
- Compare placement, framing, terminology, or feature-vs-system choices inline
  when real tradeoffs remain.
- [../review/SKILL.md](../review/SKILL.md) - material durable docs, public
  guidance, cross-surface policy, or completion claims.

## Output

- Updated doc with reader contract, current examples, links, and metadata aligned
  to the owner surface.
- `docs_strategy` for ticket or implementation planning, including a no-docs
  reason when docs do not change.
- `doc_quality_result` with checks run, violations fixed or deferred, and review
  route, including remaining risk.
- Optional review handoff for material docs.
