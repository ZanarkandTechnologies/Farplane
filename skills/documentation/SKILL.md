---
name: documentation
description: "Turn durable doc-writing or doc-revision work into grounded, metadata-aware, human-usable docs with doc-quality checks."
tier: 2
source: local
template_uses:
  skill-template: "0.3.0"
  skill-qa-checklist: "0.1.0"
methods: ["documentation:doc-quality"]
qa_checklist: qa_checklist.md

---

# Documentation Skill

## Context

`documentation` owns durable repo doc writing and doc-quality review. Use it
for human-facing docs such as `README.md`, `ARCHITECTURE.md`, concrete feature
specs under `docs/features/`, system specs under `docs/systems/`,
`docs/fundamentals/*`, `docs/skills/*`, runbooks, templates, and public
guidance. Use `close-ticket` for routine final ticket writeback; call this
skill only when the work includes substantive durable doc writing or revision.

Doc search is not the core job here. Ground claims through
[reference-grounding](../reference-grounding/SKILL.md) when they depend on
local canonical files, official docs, current facts, peer norms, standards, or
implementation examples. This skill turns that evidence into clear docs with
the right metadata, reader contract, and verification.

Farplane docs follow docs-as-code habits: durable Markdown normally has YAML
front matter, ownership/version/status fields where relevant, semantic links to
canonical sources, and validator-backed reference checks. Use
`docs/features/FEAT-0060-registry-backed-documentation-os.md` for artifact-first writing and front matter
standards. Feature specs must use the reader-first shape in
`docs/features/TEMPLATE.md`: problem, behavior, user stories, operating
contract, surfaces, proof, rollout, limits, alternatives, and change history.

Farplane's docs strategy is minimal surface area with high reader quality.
System metadata belongs in `docs/systems/*.md` front matter. Feature metadata
belongs in feature-page front matter under `docs/features/`. Generated system
and feature registries must not be hand-edited. Stale or superseded docs should be deleted
after live truth is promoted into an active owner; tracked archives are not a
default destination for new work.

## Skill Signature

```text
documentation(doc_task, target_file?, evidence?, doc_type?) -> doc_delta + doc_quality_result + review_route?

state:
  reads(target doc, nearest README/AGENTS, docs/features/FEAT-0060-registry-backed-documentation-os.md,
        docs/features/TEMPLATE.md when editing feature specs,
        docs/systems/README.md when editing system specs, relevant canonical
        docs, source/evidence refs, qa_checklist.md)
  writes(target doc, optional doc-quality note, updated links/metadata)

gates:
  reader_contract_bound; doc_surface_chosen; source_of_truth_named;
  split_merge_density_decided; metadata_checked; claims_grounded; doc_quality_passed;
  material_review_routed_or_skipped_with_reason

routes:
  reference-grounding | advise | review

fails:
  writes stale or ungrounded docs; skips required front matter/metadata;
  creates files without a distinct owner/reader/lifecycle/retrieval path;
  duplicates canonical truth; preserves stale examples; writes for agents
  instead of readers; treats routine ticket writeback as documentation work
```

## Phase Boundary

This skill owns doc drafting, revision, and doc-quality verification. It does
not own implementation, ticket closeout, commits, or broad research synthesis.
Call `review` only when the doc is material, canonical, public guidance,
cross-surface policy, or a completion claim that needs independent judgment.

<!-- BEGIN FARPLANE_IMPORTANT_CHECKLIST -->
## Todo List

- [ ] 1. Bind the reader and surface.
  - [ ] Name audience, doc type, owning file, source of truth, intended next
    action, canonical terms, proof surface, and whether this is new or revised.
  - [ ] Classify the doc type as tutorial, how-to, reference, explanation,
    spec, doctrine, runbook, checklist, decision note, README, or registry
    companion.
  - [ ] Ask only for blocking missing inputs such as audience, owner, canonical
    source, or publication/review gate.
- [ ] 2. Run the doc architecture gate before writing.
  - [ ] Read `docs/features/FEAT-0060-registry-backed-documentation-os.md` for durable artifact and YAML
    front matter rules.
  - [ ] Read `docs/features/TEMPLATE.md` before creating or substantially
    rewriting a feature spec.
  - [ ] Read `docs/systems/README.md` before creating or substantially
    rewriting a system spec.
  - [ ] Read `docs/features/FEAT-0060-registry-backed-documentation-os.md` when
    placement, split/merge, density, lifecycle, archive, duplication, or
    canonical ownership is in question.
  - [ ] Read the nearest index or owner file: top-level `README.md`,
    `ARCHITECTURE.md`, relevant `docs/*/README.md`, nearest `AGENTS.md`,
    registry README, or template.
  - [ ] Decide whether the content belongs in the existing file, a new file, a
    split file, a ticket artifact, generated metadata source, or a skill-local
    surface.
  - [ ] Choose the density mode for the surface: navigational, executable,
    contractual, reference, conceptual, or archival.
  - [ ] Check whether the target file already has front matter, version/status,
    owner, created/updated dates, refs, feature IDs, source IDs, or template
    metadata that must be preserved or updated.
- [ ] 3. Ground claims with the smallest evidence move.
  - [ ] Use [reference-grounding](../reference-grounding/SKILL.md) when claims
    depend on local code/docs, official behavior, current facts, peer norms,
    standards, or implementation examples.
  - [ ] Use [advise](../advise/SKILL.md) when placement, framing, terminology,
    or doc type has real tradeoffs.
- [ ] 4. Draft or revise for the reader's next action.
  - [ ] Put the current definition, decision, workflow, or task path near the
    top.
  - [ ] For feature specs, make the first paragraph answer what the feature
    does, who or what uses it, and why it earns a stable `FEAT-*` handle.
  - [ ] For system specs, make the first paragraph answer what product layer
    the system owns, how its feature specs fit together, and what belongs
    elsewhere.
  - [ ] Use one canonical term per concept and link to the owner instead of
    duplicating long doctrine.
  - [ ] Keep examples current, complete enough to use, and matched to the doc
    type.
  - [ ] Keep agent-facing process notes in skills, tickets, prompts, or
    implementation docs rather than human-facing docs.
- [ ] 5. Update metadata, versioning, and indexes when required.
  - [ ] Add YAML front matter to new durable Markdown unless the owner surface
    forbids it, such as raw prompt-loaded files.
  - [ ] Update `updated_at`, `status`, `owner`, `refs`, `template_version`,
    `feature_refs`, `source_refs`, or registry/index links when the owning
    schema uses them.
  - [ ] When changing system or feature metadata, update the owning
    `docs/systems/*.md` file or feature page in `docs/features/` and run
    `python3 docs/features/validate_features.py --write`; do not hand-edit
    `docs/systems/registry.jsonl` or `docs/features/registry.jsonl`.
  - [ ] Do not invent version fields for ordinary docs; preserve or update
    versioning only when the local owner already defines it.
- [ ] 6. Run the doc-quality finish gate.
  - [ ] Run [qa_checklist.md](qa_checklist.md) against durable, canonical, or
    material docs.
  - [ ] For material docs or migrations, include the 0-12 documentation quality
    score from `qa_checklist.md` or explain why scoring would be fake.
  - [ ] Run only relevant searches and validators, usually
    `python3 bin/validators/check_doc_refs.py` when links/refs changed.
  - [ ] Fix violations before completion, or record explicit deferrals.
- [ ] 7. Route material review or handoff.
  - [ ] Use [review](../review/SKILL.md) for material canonical docs, public
    guidance, cross-surface policy, or completion claims.
  - [ ] For routine final ticket writeback, return the result to the ticket
    closeout owner instead of continuing doc expansion inside this skill.
<!-- END FARPLANE_IMPORTANT_CHECKLIST -->

## Templates

Reader contract:

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

Default durable Markdown front matter:

```yaml
---
title: "Short Human Title"
status: draft
owner: documentation
created_at: YYYY-MM-DD
updated_at: YYYY-MM-DD
tags: []
refs: []
---
```

Use local schemas when they exist, for example `template_version`,
`feature_refs`, `source_refs`, `framework_template_version`, or ticket metadata.

## Gotchas

- Do not turn routine ticket closeout into a documentation task; `close-ticket`
  owns final writeback.
- Do not add front matter to raw prompt-loaded files unless that loader is known
  to strip it.
- Do not preserve stale examples, old names, or duplicate definitions just
  because they existed before.
- Do not create tracked archive docs as the default cleanup move; promote live
  truth to an active owner or delete stale material.
- Do not cite external best practices as Farplane policy unless the doc labels
  them as grounded synthesis or local policy.
- Do not create new version fields without a local owner schema.

## Reference Map

- [qa_checklist.md](qa_checklist.md) - run for durable, canonical, public, or
  material documentation changes.
- [docs/features/FEAT-0060-registry-backed-documentation-os.md](../../docs/features/FEAT-0060-registry-backed-documentation-os.md)
  - front matter, artifact-first writing, lifecycle, keep/delete rules, and
    placement/archive/duplication decisions.
- [docs/features/TEMPLATE.md](../../docs/features/TEMPLATE.md) - required
  reader-first shape for feature specs.
- [docs/systems/README.md](../../docs/systems/README.md) - system spec owner
  model and generated registry flow.
- [../reference-grounding/SKILL.md](../reference-grounding/SKILL.md) - use for
  compact local, official-doc, current-source, or peer evidence.
- [../advise/SKILL.md](../advise/SKILL.md) - use when doc type, framing,
  placement, or terminology has real tradeoffs.
- [../review/SKILL.md](../review/SKILL.md) - use only for material durable docs,
  public guidance, cross-surface policy, or completion claims.
- `close-ticket` - owns final ticket writeback and routine closeout; do not
  invoke it from this Tier 2 checklist path.

## Output

- Updated doc with reader contract, current examples, links, and metadata
  aligned to the owner surface.
- `doc_quality_result` with searches/checks run, optional 0-12 quality score,
  violations fixed or deferred, and review route.
- Optional review handoff when the doc is material, canonical, public, or
  cross-surface policy.
