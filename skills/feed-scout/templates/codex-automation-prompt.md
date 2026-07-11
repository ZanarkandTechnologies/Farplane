# Feed Scout Codex Automation Prompt

Call the `feed-scout` skill as one separate bounded automation. Do not call
Interval Update from this run.

Configured local surfaces:

- source config: `farplane/bindings.yaml#feed_scout`
- daily feed root: `.farplane/feed-scout/daily`
- ingestion ledger: `.farplane/feed-scout/ledger.jsonl`
- proposal ledger or local inbox: `.farplane/feed-scout/proposals.jsonl`
- report root: `.farplane/reports/feed-scout`
- local ticket cap and write policy: supplied by this automation

Steps:

1. Load and validate configured profile/resource rows and the bounded window.
2. Discover only configured sources using Feed Scout's acquisition order.
3. Normalize items, compute canonical keys, dedupe, extract, and scout eligible
   items. Use helper scripts only for deterministic normalization/validation.
4. Compile the UI-ready daily feed and the dated Feed Scout report. The report
   frontmatter must include `ref: reports/feed-scout/<timestamp>`, `kind:
   feed-scout`, `created_at`, and `ui_summary`.
5. Write and validate the feed/report artifacts, then index reports when the
   Farplane CLI is available.
6. Only after the report exists, project up to the configured ticket cap.
   Require canonical source evidence, strong signal, active-ticket dedupe,
   executable scope, Reward, proof, stop condition, authority, and ticket
   quality. Link created and rejected candidates back into the report.
7. Default tickets to `status: awaiting_review`. Use `status: todo` only when this
   automation's explicit write policy grants automatic local admission and no
   human or external-action gate remains.
8. Return report path, feed path, ticket paths, rejections, source gaps, cap,
   and a no-execution receipt.

Do not poll forever, run Interval, launch Goal/Pulse/workers, implement created
tickets, publish, perform outreach, spend API budget, or create/write live
Notion surfaces unless the automation explicitly authorizes that action.
