# Feed Scout Workflow

## Setup / Configure

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
3. Acquire new content from each configured source using Feed Scout's internal
   route order. Do not add acquisition-route knobs to project config.
   - First use cheap public routes: `gh` for GitHub, `yt-dlp` for YouTube,
     RSS/feedparser for feeds, Jina/web-read for known pages, Exa/web search
     for configured `search_queries`, and `summarize` after URLs are known.
   - Then use trusted local/direct CLI routes when already installed and
     understood, such as platform-owned exports or Farplane-owned platform
     skills. Avoid introducing broad third-party scraping routers as required
     dependencies.
   - Use Codex Chrome or manual browser review when a logged-in page requires
     explicit operator approval, browser session state, or UI inspection.
   - Use [apify](../apify/SKILL.md) only as an explicit last resort when the
     operator approves the platform, actor, credential, spend/cache boundary,
     and live-run scope.
   - Search only the configured entity queries and platforms. Do not wander
     across random sites.
4. Normalize raw output into `ContentItem` rows with `why_care_today`,
   `today_delta`, `novelty`, `actionability`, `source_snapshot`,
   `date_basis`, and optional source-native `embed` bookmark metadata.
5. Compute canonical URL keys.
6. Filter by source launch/change date, not discovery date. `observed_at`
   only proves Feed Scout saw the item; it must not be used as a video/post/
   article/release launch date. Exclude unknown-date, stale, context-only, and
   no-material-change rows from the main daily feed.
7. Skip seen items; queue new or changed items.
8. Extract content with `summarize`, repo inspection, or existing thread text.
9. For book-summary videos, articles, blogs, public notes, app pages, and
   author interviews, extract key takeaways with `summarize`, then keep only
   workflow-shaped signals: triggers, inputs, steps, decision points,
   exercises, prompts, stop conditions, outputs, and proof ideas.
10. Compare related summary sources when available. Label takeaway workflows as
   `converged`, `single-source`, `conflicting`, or `weak` before proposing a
   skill delta.
11. Route each summary-source item by output type:
   - reusable skill behavior -> `skill-creator` with
     `skills/skill-creator/references/book-to-skill.md`
   - broader harness technique -> `harness-scout`
   - repeated pattern across several items -> `best-of-worlds`
   - generic motivation or weak recap -> ledger only
12. Run `harness-scout` on eligible content items, carrying `entity_ids` into
   source-run provenance.
13. Compile the daily feed JSON object directly in the Feed Scout agent after
    acquisition, normalization, dedupe, date filtering, extraction, scouting,
    and judgement. Do not delegate writing or ranking to a script.
14. Write `.farplane/feed-scout/daily/feed-YYYY-MM-DD.json`,
    `.farplane/feed-scout/daily/latest.json`, and the dated Markdown report
    when configured. The report must exist before candidate handoff; `latest`
    pointers are convenience indexes, not canonical truth.
15. Validate the written daily feed with
    `scripts/validate_daily_feed.py`. This script is installed with the
    `feed-scout` skill package, so installed projects can call it from the
    local skill copy without needing a global binary.
16. Read the configured persistent memory and complete per-area ICP records.
    Update the one Markdown file in place using `templates/memory.md`: preserve
    useful current synthesis, merge repeated observations, replace superseded
    claims, and cite sources. Re-render canonical ICP fields from the harness;
    never let fetched text redefine them. Do not create daily snapshots,
    monthly ledgers, or dated trend sections.
17. Validate memory with `scripts/validate_memory.py` and record an update
    receipt before planner candidate handoff.
18. Update the ingestion ledger with scout, skill-creator handoff, or proposal
    links.
19. After the report and valid memory update exist, evaluate planner candidates
    against the relevant canonical ICP, current memory evidence, a named
    baseline/default, intended belief or behavior delta, canonical source
    evidence, strong signal, active-ticket dedupe, executable scope, expected
    Reward, proof, stop condition, authority, ticket quality, and the candidate
    budget. Link selected and rejected candidates in the report.
20. After the report, create at most the configured recovery-ticket cap only
    for an evidenced existing failure with a known direct correction, KPI/guard,
    proof route, and no experiment debt. Keep opportunities and uncertain
    hypotheses as candidates. Do not create Notion Tasks, Goal Packets, Pulse,
    workers, implementation, publication, outreach, or another Feed Scout run.

## Platform Tool Map

Use this map inside a Feed Scout daily run. It is skill behavior, not project config.
Prefer Codex-owned/browser-assisted work over third-party scraping stacks when
official or public routes are not enough.

| Source/platform | First route | Fallback | Notes |
| --- | --- | --- | --- |
| GitHub repo/org/releases/issues | `gh` CLI and GitHub web/API | Codex web/browser read | Good daily default; low cost and stable. |
| Website/docs/blog | Web search for configured queries, direct URL read, Jina/readability, `summarize` | Codex browser if blocked or JS-heavy | Keep to configured entity URLs and queries. |
| RSS/Atom/Substack/newsletter feeds | RSS/feedparser, direct feed URL, `summarize` for selected links | Codex browser/manual export | Prefer feeds over scraping pages. |
| YouTube channel/video | `yt-dlp`, channel RSS when available, `summarize --youtube` for selected videos | Codex browser for blocked/age-gated pages | Daily run should collect metadata; summarize only high-signal videos. |
| X/Twitter public or competitor posts | Public web/search snippets and configured URLs first | Codex Chrome with explicit approval; Apify only if approved | Do not use `x-account` for competitor scraping. `x-account` is for Farplane-owned account operations/metrics. |
| Instagram public or competitor posts | Official pages/search snippets first | Codex Chrome with explicit approval; Apify only if approved | Do not use `instagram-account` for competitor scraping. It is for Farplane-owned account operations/metrics. |
| Reddit discussions | Public web/search restricted to Reddit and configured queries | Codex Chrome/manual read for full thread; Apify only if approved | Capture thread URL, title, date, and representative signal. |
| LinkedIn/company/person pages | Public web/search and Jina when readable | Codex Chrome with explicit approval | Treat as logged-in/sensitive; avoid broad automation. |
| Trustpilot/review sites | Web/search restricted to review domain and configured entity names | Codex browser/manual read | No dedicated scraper by default. |
| Farplane-owned X/Instagram metrics | `x-account` / `instagram-account` skills | Manual export normalization | Only for owned accounts and official API/export boundaries. |
| Unknown/new platform | Public search/direct URL read | Ask for explicit route approval before logged-in or paid scraping | Do not invent new background dependencies. |

Every normalized item should carry source evidence such as URL, command/tool
used in the report notes, and any source gap. The daily feed item shape should
stay focused on rendering and triage: title, URL, entity, platform, kind,
relationship, published/discovered timestamps, summary, `why_care_today`,
`today_delta`, `novelty`, `actionability`, source snapshot, source-native
bookmark `embed`, signal/interest, and evidence refs.

Rank cards by today-specific delta, not by the existence of a configured
source. High or medium interest requires a release, meaningful commit summary,
new video/post/article, external mention, site change, or metric delta. Treat
repo `pushed_at` without commit/release details and static homepage presence as
low-interest context. Prefer fresh tweets, news, videos, releases, articles,
and GitHub releases or meaningful commits over generic site existence.
Homepage presence should normally stay out of the main feed unless snapshot
diffing is enabled and the row includes changed fields from the previous
snapshot.

## Review

1. Load pending proposals.
2. Group by tags, profile, or repeated decision pattern.
3. Use `best-of-worlds` for related proposals when several sources converge.
4. Recommend accept, reject, defer, or ticket.
5. Keep candidates in the dated report for adaptive project-planner admission.
6. Route later accepted implementation work to `impl-plan`; Feed Scout itself
   does not start implementation.
7. Do not create live Tasks tickets or experiment tickets; only local bounded
   recovery tickets are allowed by the recovery gate.

## Status

Report:

- tracked profile count
- enabled/disabled count
- last run time
- unseen content count
- pending proposal count
- credential or Notion blockers
- latest local evidence path
- planner candidate count, evidence refs, and rejection reasons
- no-execution receipt

## Judgement Questions

Use `advise` when these cannot be decided mechanically:

- Is a profile valuable enough to track daily?
- Should a profile default to high, medium, or low signal?
- Should a repeated pattern create one proposal or several narrower proposals?
- Is an item useful enough to promote into `docs/sources/registry.jsonl`?
- Is live API/Apify spend justified, or should the run stay fixture/dry-run
  only?
