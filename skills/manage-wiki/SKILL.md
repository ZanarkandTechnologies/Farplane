---
name: manage-wiki
description: "Turn sourced facts or page deltas into resolved canonical Wiki articles, entity links, and validated local search and graph projections."
tier: 3
source: local
capability:
  kind: integration
group: intelligence
skill_template_version: "0.3.8"
template_uses:
  skill-template: "0.3.8"
  skill-surface-budget: "0.1.0"
allowed-tools: Read, Write, Grep, Glob, Bash
---

# Manage Wiki

## Context

Use this skill when sourced facts, ingestion output, or explicit page deltas
should create or update project-local Wiki articles and their entity links. It
owns the staged resolve/create/link workflow, not source discovery, transcript
mining, or direct graph/database editing.

Markdown under `.farplane/entities/<id>.md` is canonical. Generated
`.farplane/wiki/wiki.sqlite`, `.farplane/entities/index.json`,
`.farplane/entities/graph.json`, `.farplane/entities/crm.json`, and typed views
are disposable projections. Use
`farplane wiki search` for candidate retrieval, then read candidate Markdown
before making a contextual identity decision. Follow the shared
[Wiki storage contract](../../docs/farplane-framework/entities.md) and
[authoring notation](../../docs/farplane-framework/entity-markdown-authoring.md).

## Skill Signature

```text
manage_wiki(source_ref, page_deltas?, entity_scope?, project_root?,
            publication_intent = preview)
  -> staged_pages + changed_pages + resolution_receipt + projection_refs

publication_intent = preview | apply
publication_result = previewed | applied | no_op | ambiguity | blocked

resolution_outcome = link | update_existing | create_new | ambiguity |
  skip_source_gap | blocked

state: reads(source_ref, page_deltas?, project context, canonical Markdown,
             generated Wiki search index);
       writes(.farplane/entities/*.md and disposable Wiki/JSON projections)
gates: source_bound; publication_intent_bound; privacy_safe;
       wiki_doctor_passes; touched_pages_staged;
       unique_exact_match_only_auto_links; candidate_markdown_read;
       ambiguous_merge_blocked; unrelated_prose_preserved;
       all_links_resolve; staged_changeset_valid; wiki_sync_passes
routes: direct_changeset | research:* | ambiguity_receipt | source_gap
fails: unbounded_source_mining; invented_identity_or_claim; silent_merge;
       unresolved_or_self_link; inferred_predicate; direct_projection_edit;
       partial_publish_before_validation; cross_project_identity_merge;
       private_or_sensitive_dossiering; conflicting_publication_intent
```

## Phase Boundary

Keep bounded page authoring and resolution inline. Use `research:*` only when a
specific identity or material claim needs evidence beyond the bound source; do
not widen a Wiki update into general discovery. Normal Wiki authoring does not
need `impl-plan`; use that only for a software or schema change to the system.

<!-- BEGIN FARPLANE_IMPORTANT_CHECKLIST -->
## Todo List

- [ ] 1. Bind the Wiki changeset or return its exact blocker.
  - [ ] Read the first-load Todo List guardrails; resolve `project_root`, `source_ref`, optional
        `page_deltas`, and the active `entity_scope` from the caller or project
        operating context. Do not treat every capitalized noun as an entity.
  - [ ] Bind `publication_intent`. Explicit save, add, update, write, or publish
        **to Wiki**, or “apply these Wiki changes,” means `apply`; explicit
        preview, propose, draft, or do-not-write means `preview`. Missing Wiki
        write direction defaults to `preview`; conflicting directions block
        publication and return a preview with the conflict named.
  - [ ] Run `farplane wiki doctor --project-root <project_root>` before any
        canonical write. Return `skip_source_gap` when no readable source or
        selected facts exist; do not search unrelated calls or notes.
- [ ] 2. Stage sourced article deltas and extract unresolved mentions.
  - [ ] Select the affected existing articles and any required new entity pages
        from the durable facts; callers need not supply filenames or IDs.
  - [ ] Build a diff-shaped changeset without writing it. Preserve existing
        frontmatter, unrelated prose, uncertainty, source links, and question
        references; retain only durable facts supported by the bound source.
        Make each replacement diff directly applicable: remove the old sentence
        when adding its linked replacement instead of displaying both as additions.
  - [ ] Scan only touched article prose for durable in-scope people,
        organizations, facilities, products, and places. Exclude existing
        `entity:` links, ordinary URLs, code, citation definitions, generic
        nouns, and mentions whose identity is irrelevant to the article.
- [ ] 3. Resolve every retained mention through deterministic hybrid search.
  - [ ] Run `farplane wiki search --project-root <project_root> "<mention>"`.
        Only one unique exact ID, normalized name, or alias match may auto-link.
  - [ ] Treat FTS5, prefix, and trigram results only as candidates. Read each
        plausible candidate's canonical Markdown and compare kind, location,
        nearby entities, aliases, and source evidence before choosing an
        outcome. Record those contrasts candidate by candidate, not as one
        collective “checked” statement.
  - [ ] Choose `link` when an existing article needs no factual update,
        `update_existing` when the source adds durable facts, and `create_new`
        only when no plausible match exists and the source establishes a stable
        identity. Multiple plausible matches always produce `ambiguity` and
        block the changeset; missing evidence produces `skip_source_gap`.
- [ ] 4. Validate, then preview or apply the complete changeset.
  - [ ] Add `[visible label](entity:resolved-id)` inside the supported factual
        sentence; never author an inverse link, predicate, self-link, unresolved
        link, or separate edge record. Create required new articles in the same
        changeset before linking them.
  - [ ] Apply the first-load Todo List guardrails to the staged diff. Publish canonical Markdown
        only when every required resolution is non-ambiguous and all IDs,
        sources, notation, question refs, and links validate.
  - [ ] For `preview`, finish resolution and validation but write nothing; show
        the exact applicable diffs and expected sync commands. For `apply`, a
        direct Wiki write instruction is sufficient—do not request a second
        exact-delta approval—then publish all canonical pages and run
        one `farplane wiki sync --project-root <project_root> --path <page-a>
        --path <page-b>` command containing every changed article. Source,
        privacy, ambiguity, and validation gates still block the entire apply.
        Never edit SQLite/JSON directly.
- [ ] 5. Return the Wiki receipt and projection proof.
  - [ ] List changed article paths and every mention's outcome, candidate IDs,
        match evidence, decision rationale, skipped claims, ambiguities, and
        blockers. Include search/database and JSON projection refs plus sync
        diagnostics; return a visible no-op reason when nothing durable changed.
        In a read-only preview, label commands and diagnostics as expected—not
        executed—and still name `.farplane/wiki/wiki.sqlite` and the explicit
        `.farplane/entities/{index,graph,crm}.json` paths. Name typed-view paths from known
        view config; otherwise report them as unknown rather than inventing a
        wildcard path or claiming observed projection effects.
<!-- END FARPLANE_IMPORTANT_CHECKLIST -->

## Templates

```text
Source sentence: Georgia Power is working with OpenAI on energy planning.
Search: OpenAI -> unique exact alias/name candidate `openai`.
Result: Georgia Power is working with [OpenAI](entity:openai) on energy planning.
Outcome: link; originating page: georgia-power; one bounded sync replaces only that page's claims.
Intent: preview stages this result; apply writes it and runs the bounded sync.
```

See the [mixed resolution example](examples/supply-call/example.md) when one
changeset contains update, create, link, ambiguity, and question provenance.

## Gotchas

- Similar spelling is retrieval evidence, not identity proof.
- Replace generated edge claims by originating article; never delete all edges
  touching an endpoint entity.
- A Wiki article may hold sourced narrative context; generated search rows and
  graph edges never become a second canonical record.

## Reference Map

- [Wiki storage contract](../../docs/farplane-framework/entities.md) — read on
  every invocation for canonical fields, search state, and projection behavior.
- [Wiki authoring notation](../../docs/farplane-framework/entity-markdown-authoring.md)
  — read before staging or reviewing Markdown.
- [mixed resolution example](examples/supply-call/example.md) — read for a
  multi-outcome changeset or ambiguity review.

## Output

Return `changed_pages`, one `resolution_receipt` row per retained mention with
candidate-by-candidate evidence and intended link placement, the bound
`publication_intent` and `publication_result`, plus explicit `projection_refs`. Preview returns
`staged_pages` and `changed_pages: []`; apply returns the written pages. An
ambiguity, privacy failure, intent conflict, or failed validation returns the applicable
staged diff and blocker without publishing canonical Markdown or mutating
projections. Always emit an explicit `resolution_outcome`; missing or unbounded
source input is `skip_source_gap`, not the generic `blocked` outcome.
