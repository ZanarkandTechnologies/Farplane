---
name: instagram-account
description: "Turn Instagram account posting or insights requests into validated artifacts, normalized KPI snapshots, or gated API actions."
tier: 3
group: marketing
source: local
methods:
  - id: instagram-account:validate
    class: integration
    output: instagram-draft-validation
  - id: instagram-account:publish
    class: integration
    output: instagram-publish-receipt
  - id: instagram-account:measure
    class: integration
    output: instagram-metrics-snapshot
template_uses:
  skill-template: "0.3.7"
  skill-eval-task: "0.2.0"
  skill-qa-checklist: "0.1.0"
eval: evals/evals.json
allowed-tools: Read, Grep, Glob, Bash
qa_checklist: qa_checklist.md
---

# Instagram Account

## Context

Use this skill for Farplane-owned Instagram account integration: profile/media
insights, caption/carousel/reel validation, export normalization, and
explicitly approved publishing. `social-content` owns creative drafting;
`apify` or `feed-scout` owns broad scraping/listening.

Secrets never live in tracked files. Project aliases and non-secret policy live
in `farplane/bindings.yaml`; credentials come from runtime env first, normally
via `farplane run -- <command>` / Doppler using the `FARPLANE_INSTAGRAM_` and
`FARPLANE_META_` prefixes. Local TOML is not a credential source. Metrics use
Instagram Login credentials against `graph.instagram.com`; Facebook Page
ownership belongs in a separate future Facebook Pages skill if needed.

## Skill Signature

```text
instagram_account(action, artifact?, account_binding?, date_window?, source_file?)
  -> draft_validation | publish_result | metrics_snapshot | blocked_report
state:
  reads(farplane/bindings.yaml, ~/.codex/private/docs/social.md?,
        runtime env, source_file?)
  writes(.farplane/metrics/manual/instagram_account.json when normalizing exports,
         .farplane/content/ledger.jsonl after confirmed publishing)
gates:
  professional_account_confirmed; account_binding_resolved;
  publish_approval_explicit; credential_source_private;
  no_secret_echo; metric_snapshot_shape_valid
routes:
  social-content | apify | feed-scout | metric-advisor | review
fails:
  publishing without explicit approval; using personal-account assumptions for
  Graph API work; copying tokens into tracked files; inventing metrics
```

## Phase Boundary

Keep validation and normalization inline. Use `social-content` for creative
drafts, `apify` or `feed-scout` for broad reads, and `review` before first live
publishing.

<!-- BEGIN FARPLANE_IMPORTANT_CHECKLIST -->
## Todo List

- [ ] 1. Bind the requested action.
  - [ ] Allowed actions: `validate_caption`, `validate_carousel`,
        `validate_reel`, `publish_post`, `publish_reel`,
        `get_profile_metrics`, `get_media_metrics`,
        `import_metrics_export`, `normalize_metrics_snapshot`.
  - [ ] Resolve the account alias from `farplane/bindings.yaml`.
- [ ] 2. Check safety gates.
  - [ ] Confirm the account/API mode supports Instagram professional account
        insights or content publishing before promising live API behavior.
  - [ ] For publish actions, require explicit approval naming the exact
        artifact, account alias, and publish boundary.
  - [ ] Run `scripts/check_config.py` once before live API work; it checks read
        and publish readiness together without a capability selector.
  - [ ] If it is not ready, return `blocked_report` with the reported missing
        key names and setup steps; never expose values.
- [ ] 3. Choose the execution branch.
  - [ ] 1. Validation branch: check caption, media, carousel, reel, and publish
        boundary requirements. Use this before a publish request, before
        asking for review on an Instagram-specific artifact, or when the caller
        only wants platform fit feedback.
  - [ ] 2. Metrics branch: fetch or import profile/media insights and normalize
        to Farplane KPI observations.
  - [ ] 3. Publish branch: run only after explicit approval and final artifact
        validation; record media IDs and evidence.
  - [ ] 4. Broad-read branch: route to `apify` or `feed-scout`.
- [ ] 4. Execute the selected branch.
  - [ ] For validation, return blocking issues, warnings, and suggested fixes;
        do not mutate account state. Use `scripts/validate_media_payload.py`
        for JSON post/reel/carousel payloads.
  - [ ] For metrics, write observations compatible with daily Farplane KPI
        readings consumed by `.farplane/project/ui/latest.json`:
        `instagram_followers`, `instagram_views`, `instagram_likes`, and
        optional post counts. Use
        `scripts/fetch_metrics.py` for live read-only Graph API metrics
        (`--latest`, `--latest-reel`, `--yesterday`, `--since-date`, and
        `--until-date` for review windows; `--media-id` for exact media
        metrics; `--deep` for Reels retention fields) or
        `scripts/normalize_metrics.py` for local JSON/CSV exports.
  - [ ] For metrics, run `scripts/validate_metrics.py` against the produced
        snapshot before treating the skill-local contract as proven.
  - [ ] For metrics, use `source_gap` when a metric is unavailable; do not
        write zero unless the platform actually returned zero.
  - [ ] For publishing, record media IDs/URLs only after the API confirms the
        mutation, then append/update the local content ledger with
        `farplane content add --platform instagram --external-id <media_id>
        --url <url> --status posted --approval approved
        --published-at <timestamp> --campaign <campaign>
        --kpis instagram_views,instagram_likes,evidence_distribution_reach
        --approval-ref <ticket_or_report_ref>`.
- [ ] 5. Finish with proof.
  - [ ] Apply `qa_checklist.md`: Universal QA plus only the selected branch QA.
  - [ ] For live API/posting work, record endpoint, account alias, timestamp,
        output IDs, and redacted credential source.
  - [ ] For export normalization, record source file and output snapshot path.
<!-- END FARPLANE_IMPORTANT_CHECKLIST -->

## Templates

Normalized metric snapshot:

```json
{
  "source_id": "manual_instagram_account",
  "date": "2026-06-30",
  "status": "available",
  "observations": [
    {"metric_id": "instagram_followers", "date": "2026-06-30", "value": 1234, "status": "available"},
    {"metric_id": "instagram_views", "date": "2026-06-30", "value": 5600, "status": "available"},
    {"metric_id": "instagram_likes", "date": "2026-06-30", "value": 430, "status": "available"}
  ]
}
```

## Gotchas

- Instagram Graph/API publishing and insights generally require professional
  account setup, app permissions, and review-sensitive access.
- Facebook Page ownership, `/me/accounts`, and Page-linked assets are not part
  of this skill; route that to a future Facebook Pages skill if needed.
- Posting is an external mutation and always needs explicit approval.
- Broad scraping/listening belongs to `apify` or `feed-scout`, not account API.

## Reference Map

- `references/api.md` - load for Instagram API endpoint/auth grounding before live API work.
- `references/metrics-snapshot.md` - load when importing or normalizing account metrics.
- `scripts/check_config.py` - check complete read-and-publish private env
  readiness in one redacted report.
- `scripts/fetch_metrics.py` - fetch read-only profile/media metrics and write KPI observations.
  Use no media IDs for account snapshot mode; repeat `--media-id` for exact media metrics.
  Use `--latest`, `--latest-reel`, `--yesterday`, `--since-date`, or
  `--until-date` to select media for content review while preserving aggregate
  KPI observations. When `--deep` is set, Reel-only watch-time metrics are
  requested only for selected media whose `media_type` is `REELS`; non-Reel
  media records a retention source gap instead of fake zero.
  Add `--deep --duration-seconds <seconds>` for Reels watch-time observations
  and normalized `instagram_retention_score` when the API returns watch-time
  insights.
- `scripts/publish_media.py` - dry-run or publish an approved Instagram image,
  carousel, video, or Reel payload from public `image_url` / `video_url`
  sources. Defaults to dry-run; live mutation requires `--execute`,
  `--account-alias`, and `--approval-ref`. Creates/polls the publishing
  container, publishes it, fetches the permalink when available, then writes
  `.farplane/content/ledger.jsonl` after confirmed publish.
- `scripts/validate_metrics.py` - validate Instagram metric snapshot shape,
  metric IDs, redaction, and blocked/source-gap semantics without external API calls.
- `scripts/validate_media_payload.py` - validate post/reel/carousel JSON without account mutation.
- `scripts/normalize_metrics.py` - normalize JSON/CSV metric exports to Farplane KPI observations.
- `farplane content add` - append/update `.farplane/content/ledger.jsonl` after
  a confirmed publish so interval refresh can fetch owned-content metrics.
- `evals/evals.json` - agent-behavior eval rows for live metrics and missing-credential flows.

## Output

- `draft_validation`: platform-fit verdict, blocking issues, and fixed draft suggestions.
- `metrics_snapshot`: normalized observations and output path.
- `publish_result`: media IDs, URLs, timestamp, and redacted credential source.
- `blocked_report`: missing binding, missing credential, missing approval, or API/source gap.
