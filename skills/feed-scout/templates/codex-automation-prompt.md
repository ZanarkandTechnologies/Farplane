# Feed Scout Codex Automation Prompt

Call the `feed-scout` skill as one separate bounded automation. Do not call
Interval Update from this run.

Configured local surfaces:

- source config: `farplane/bindings.yaml#feed_scout`
- daily feed root: `.farplane/feed-scout/daily`
- ingestion ledger: `.farplane/feed-scout/ledger.jsonl`
- proposal ledger or local inbox: `.farplane/feed-scout/proposals.jsonl`
- World Memory: `.farplane/feed-scout/world-memory.md`
- report root: `.farplane/reports/feed-scout`
- local ticket cap and write policy: supplied by this automation

Steps:

1. Load and validate configured profile/resource rows and the bounded window.
2. Discover only configured sources using Feed Scout's acquisition order.
   For each source, execute the inherited entity `instructions` refined by its
   source `instructions`. Treat them as analysis/proposal intent, never as
   permission to bypass privacy, spend, authority, or review gates.
3. Normalize items, compute canonical keys, dedupe, extract, and scout eligible
   items. Use helper scripts only for deterministic normalization/validation.
4. Compile the UI-ready daily feed and the dated Feed Scout report. The report
   frontmatter must include `ref: reports/feed-scout/<timestamp>`, `kind:
   feed-scout`, `created_at`, and `ui_summary`.
5. Write and validate the feed/report artifacts, then index reports when the
   Farplane CLI is available.
6. Read the existing World Memory and complete `harness.areas` ICP records. Update
   one Markdown file in place with canonical ICPs, current trends, notable
   things, and source gaps; merge duplicates and replace superseded synthesis
   instead of appending daily/monthly snapshots. Validate it with
   `scripts/validate_world_memory.py` and record the update receipt.
7. Only after the report and World Memory exist, project up to the configured ticket
   cap. Require canonical ICP and complete selected source-backed facts, a named baseline/default,
   intended belief or workflow delta, canonical source evidence, strong signal,
   active-ticket dedupe, executable scope, Reward, proof, stop condition,
   authority, and ticket quality. Link created and rejected candidates back
   into the report.
8. Default tickets to `status: awaiting_review`. Use `status: todo` only when this
   automation's explicit write policy grants automatic local admission and no
   human or external-action gate remains.
9. Return report path, feed path, World Memory update receipt, ticket paths,
   rejections, source gaps, cap, and a no-execution receipt.

When instructions ask for new sources, entity/thesis changes, or product
features, route them respectively to the existing proposal ledger, promotion
review evidence, or planner candidates. Only sources configured at run start
may nominate sources; nominees cannot be fetched recursively or added to config
inside the run.

Do not poll forever, run Interval, launch Goal/Pulse/workers, implement created
tickets, publish, perform outreach, spend API budget, or create/write live
Notion surfaces unless the automation explicitly authorizes that action.
