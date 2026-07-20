---
name: ingest-world-data
description: "Turn selected transcript or research-call facts into resolved Markdown CRM entities and a compiled world projection when useful relationship knowledge should be retained."
tier: 3
source: local
group: research
skill_template_version: "0.3.8"
template_uses:
  skill-template: "0.3.8"
  skill-qa-checklist: "0.1.0"
  skill-surface-budget: "0.1.0"
eval: evals/evals.json
qa_checklist: qa_checklist.md
allowed-tools: Read, Write, Grep, Glob, Bash
---

# Ingest World Data

## Context

Use this skill after a useful call, transcript passage, report, or operator-
selected fact should become durable enterprise or supply-chain knowledge. It is
an intentional writeback workflow, not a transcript miner, watcher, bulk
extractor, or automatic enrichment system.

CRM entity Markdown under `.farplane/crm/entities/` is canonical. Generated
`.farplane/crm/entities.json` and `.farplane/crm/world.json` are disposable
read models. Follow the shared
[CRM contract](../../docs/farplane-framework/crm.md) for fields, links, and
compiler behavior.

## Skill Signature

```text
ingest_world_data(source_ref, selected_information?, question_context?, project_root?)
  -> created_entities[]
   + updated_entities[]
   + resolution_decisions[]
   + association_mentions[]
   + question_refs[]
   + skipped_claims[]
   + ambiguity_report[]
   + compiled_world_ref

state:
  reads(source_ref, selected_information?, question_context?, .farplane/crm/entities.json?,
        .farplane/crm/entities/**/*.md)
  writes(.farplane/crm/entities/**/*.md,
         .farplane/crm/entities.json, .farplane/crm/world.json)

gates:
  source_bound; durable_fact_only; duplicate_search_complete;
  ambiguous_merge_blocked; existing_prose_preserved; crm_links_resolve;
  question_refs_resolve; supplied_or_verified_coordinates_only; crm_compile_passes

routes: direct_writeback | ambiguity_report | source_gap
fails:
  mines_unspecified_transcripts; invents_entities_or_relationships;
  silently_merges_ambiguous_nodes; overwrites_entity_body;
  infers_relationship_predicate; geocodes_without_evidence;
  hand_edits_generated_json
```

## Phase Boundary

Run the bounded capture inline. Use a separate research or review workflow only
when entity identity, coordinates, or a material claim needs evidence beyond
the supplied source. Do not widen one capture into discovery across old calls.

<!-- BEGIN FARPLANE_IMPORTANT_CHECKLIST -->
## Todo List

- [ ] 1. Bind the capture and load guardrails.
  - [ ] Resolve `source_ref`, the operator-selected information or bounded
        source passage, optional current `question_context` (`question_id`,
        exact `question`, optional `session_id`), and `project_root`; read
        `qa_checklist.md` before any write.
  - [ ] Stop with `source_gap` when neither a readable source nor selected
        information is available. Do not search unrelated transcripts.
- [ ] 2. Identify only durable world facts.
  - [ ] Extract named people, organizations, facilities, products, places, and
        explicit associations that will remain useful after the call.
  - [ ] Keep tentative language tentative. Skip chatter, duplicate phrasing,
        speculative private facts, and claims with no supplied source basis.
- [ ] 3. Resolve each candidate against current CRM state.
  - [ ] Compile first when `entities.json` is absent or stale, then search exact
        ID, normalized name, aliases, kind, and location across the registry.
  - [ ] Update one strong match, create only when no plausible match exists,
        and return all plausible candidates in `ambiguity_report` instead of
        merging when identity remains ambiguous.
- [ ] 4. Apply bounded Markdown changes.
  - [ ] Preserve frontmatter fields and existing prose not owned by the new
        fact. Merge aliases without duplicates; add flat `location` and paired
        `latitude`/`longitude` only when supplied or verified.
  - [ ] Put durable claims in the nearest existing semantic section or add a
        concise `## Relationships` or `## Notes` section. Retain a Markdown
        source reference when the source has a stable path or URL.
  - [ ] When the capture answers an explicit bound question, cite every retained
        claim block with the same stable `[^q-*]` reference and add its exact
        definition under `## Question index`. Reuse an existing matching ID;
        otherwise choose the next unused `q-YYYYMMDD-NN` ID after searching the
        current CRM. Append ` | session=<id>` only when the session ID is
        supplied. Never add a turn ID or make session identity required.
- [ ] 5. Encode explicit associations.
  - [ ] Link a resolved target inside the original factual sentence as
        `[visible name](crm:entity-id)`. The containing entity and target form
        an undirected association; do not author a predicate, inverse edge, or
        separate edge record.
  - [ ] Do not emit a CRM link for unresolved, ambiguous, or self-referential
        targets. Avoid adding the same factual sentence twice.
- [ ] 6. Compile and repair the local projection.
  - [ ] Run `farplane crm compile --project-root <project_root>` after Markdown
        writes. Repair issues caused by this invocation; report pre-existing
        issues separately and do not hand-edit either generated JSON file.
- [ ] 7. Return the capture receipt.
  - [ ] List created and updated paths; for every candidate, include the exact
        ID/name/alias/kind/location matches considered and the resulting
        create, update, or ambiguity decision. Also list explicit associations,
        question refs, skipped claims, ambiguity candidates, compile issues,
        and the `world.json` path. If no durable delta exists, return a visible
        no-op reason.
- [ ] 8. Apply the finish gate.
  - [ ] Re-read `qa_checklist.md` and verify source fidelity, merge safety,
        prose preservation, link resolution, and successful deterministic
        compilation. Use independent review when the capture is material.
<!-- END FARPLANE_IMPORTANT_CHECKLIST -->

## Templates

```markdown
---
id: penang-castings
kind: company
name: Penang Castings
aliases:
  - PC Manufacturing
location: Penang, Malaysia
latitude: 5.4141
longitude: 100.3288
---

# Penang Castings

## Relationships

- Supplies aluminum housings to [Acme Motors](crm:acme-motors) from its Penang facility. [^q-20260720-01] Source: [Research call](../../../customer-research/reports/2026-07-13-supply-chain-call.md).

## Question index

[^q-20260720-01]: Which Malaysian suppliers can support Acme Motors? | session=019f7e88-6864-7f23-8dbb-5e058009e911
```

See the [representative transcript capture](examples/supply-call/example.md)
for update, create, association, and ambiguous-identity outcomes.

## Gotchas

- A shared name or approximate spelling is a candidate, not proof of identity.
- A location without coordinates remains searchable and valid but is not
  plotted; never invent coordinates to make the map look complete.
- `crm:` links create associations from the exact containing sentence only;
  ordinary Markdown links remain ordinary evidence links.
- Question definitions are local Markdown footnotes, not entities. Repeat the
  same exact question text in each entity file whose claims cite it; optional
  session suffixes may differ and compile into non-identity provenance.

## Reference Map

- [CRM contract](../../docs/farplane-framework/crm.md) - read on every
  invocation for canonical fields, generated projections, and validation.
- [representative transcript capture](examples/supply-call/example.md) - read
  when resolving a mixed create/update/ambiguity capture or reviewing output.
