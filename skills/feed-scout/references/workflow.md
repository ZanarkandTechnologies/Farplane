# Feed Scout Workflow

## Configure

1. Accept a list of profile URLs or handles.
2. When the target is a person, organization, repo, or skill package, create or
   reuse a tracked entity before adding the resource.
3. Infer `platform`, `resource_type`, and default `fetch_method`.
4. Apply defaults for cadence, tags, and signal threshold.
5. Validate the resulting tracked-profile rows and resource/entity references.
6. Return setup steps and human gates for credentials, Notion, or automation.

## Run

1. Load enabled tracked profiles and enabled tracked harness resources.
2. Validate entity/resource references before discovery.
3. Discover new content from each profile or resource.
4. Normalize raw output into `ContentItem` rows.
5. Compute canonical URL keys.
6. Skip seen items; queue new or changed items.
7. Extract content with `summarize`, repo inspection, or existing thread text.
8. For book-summary videos, articles, blogs, public notes, app pages, and
   author interviews, extract key takeaways with `summarize`, then keep only
   workflow-shaped signals: triggers, inputs, steps, decision points,
   exercises, prompts, stop conditions, outputs, and proof ideas.
9. Compare related summary sources when available. Label takeaway workflows as
   `converged`, `single-source`, `conflicting`, or `weak` before proposing a
   skill delta.
10. Route each summary-source item by output type:
   - reusable skill behavior -> `skill-creator` with
     `skills/skill-creator/references/book-to-skill.md`
   - broader harness technique -> `harness-scout`
   - repeated pattern across several items -> `best-of-worlds`
   - generic motivation or weak recap -> ledger only
11. Run `harness-scout` on eligible content items, carrying `entity_ids` into
   source-run provenance.
12. Update the ingestion ledger with scout, skill-creator handoff, or proposal
    links.
13. When writing to a live Notion Tasks database, resolve `Project` and `Areas`
    from explicit request context, parent project/task context, or private
    Notion handles under `~/.codex/private/`. If either relation is unresolved,
    keep the proposal in the ledger or local inbox with `routing_missing`.
14. After live Tasks writeback, fetch the page and record whether `Project` and
    `Areas` are present.

## Review

1. Load pending proposals.
2. Group by tags, profile, or repeated decision pattern.
3. Use `best-of-worlds` for related proposals when several sources converge.
4. Recommend accept, reject, defer, or ticket.
5. Route accepted implementation work to `impl-plan`.
6. Before creating or updating a live Tasks ticket, verify the
   `NotionTaskProjection`:
   - `routing_status=resolved`
   - `project_relation` present
   - one or more `areas_relations` present
   - readback required after write

## Status

Report:

- tracked profile count
- enabled/disabled count
- last run time
- unseen content count
- pending proposal count
- credential or Notion blockers
- latest local evidence path

## Judgement Questions

Use `advise` when these cannot be decided mechanically:

- Is a profile valuable enough to track daily?
- Should a profile default to high, medium, or low signal?
- Should a repeated pattern create one proposal or several narrower proposals?
- Is an item useful enough to promote into `docs/sources/registry.jsonl`?
- Is live API/Apify spend justified, or should the run stay fixture/dry-run
  only?
