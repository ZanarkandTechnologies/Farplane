---
name: x-account
description: "Turn X account posting or metrics requests into validated drafts, normalized KPI snapshots, or gated API actions."
tier: 3
group: content-social
source: local
template_uses:
  skill-template: "0.3.7"
  skill-qa-checklist: "0.1.0"
allowed-tools: Read, Grep, Glob, Bash
qa_checklist: qa_checklist.md
---

# X Account

## Context

Use this skill for Farplane-owned X account integration: account metrics,
post/thread validation, export normalization, and explicitly approved posting.
`social-content` owns drafting; this skill owns platform/account boundaries.
Broad listening, competitor scraping, and attention-graph reads route through
`feed-scout` or `apify`, not this skill.

Secrets never live in tracked files. Project aliases and non-secret policy live
in `farplane/bindings.yaml`; credentials live under local private
`~/.farplane/config.toml` `[social.x]` or explicit runtime environment
overrides using the `FARPLANE_X_` prefix. Prefer current X OAuth 2.0 user
tokens for account timeline/deep reads; OAuth 1.0a credentials are kept as
fallback/legacy support.

## Skill Signature

```text
x_account(action, artifact?, account_binding?, date_window?, source_file?)
  -> draft_validation | publish_result | metrics_snapshot | blocked_report
state:
  reads(farplane/bindings.yaml, ~/.codex/private/docs/social.md?,
        ~/.farplane/config.toml [social.x]?, source_file?)
  writes(.farplane/metrics/manual/x_account.json when normalizing exports,
         .farplane/content/ledger.jsonl after confirmed publishing)
gates:
  account_binding_resolved; publish_approval_explicit;
  credential_source_private; no_secret_echo; metric_snapshot_shape_valid
routes:
  social-content | apify | feed-scout | metric-advisor | review
fails:
  publishing without explicit approval; treating broad scraping as account API;
  copying tokens into tracked files; inventing metrics when API/export is absent
```

## Phase Boundary

Keep validation and normalization inline. Use `social-content` for copy
creation, `apify` or `feed-scout` for broad reads, and `review` before any
first live posting branch.

<!-- BEGIN FARPLANE_IMPORTANT_CHECKLIST -->
## Todo List

- [ ] 1. Bind the requested action.
  - [ ] Allowed actions: `validate_post`, `validate_thread`,
        `publish_post`, `publish_thread`, `get_profile_metrics`,
        `get_post_metrics`, `import_metrics_export`,
        `normalize_metrics_snapshot`.
  - [ ] Resolve the account alias from `farplane/bindings.yaml`.
- [ ] 2. Check safety gates before touching account state.
  - [ ] For publish actions, require explicit user or ticket approval naming
        the exact draft, account alias, and publish boundary.
  - [ ] For API actions, require credentials from private env only; never print
        tokens or paste them into artifacts.
  - [ ] Use `scripts/check_config.py` when credential readiness is unclear.
  - [ ] If credentials are missing, return `blocked_report` with setup steps.
- [ ] 3. Choose the execution branch.
  - [ ] 1. Validation branch: check X character/thread/media constraints and
        return `draft_validation`. Use this before a publish request, before
        asking for review on an X-specific draft, or when the caller only wants
        platform fit feedback.
  - [ ] 2. Metrics branch: fetch or import account/post metrics, then normalize
        to Farplane KPI observations.
  - [ ] 3. Publish branch: run only after explicit approval and final draft
        validation; record the resulting post IDs and evidence.
  - [ ] 4. Broad-read branch: route to `apify` or `feed-scout` instead of using
        account credentials for discovery.
- [ ] 4. Execute the selected branch.
  - [ ] For validation, return blocking issues, warnings, and suggested fixes;
        do not mutate account state. Use `scripts/validate_post_payload.py`
        for JSON post/thread payloads.
  - [ ] For metrics, write observations compatible with daily Farplane KPI
        readings consumed by `.farplane/project/ui/latest.json`:
        `x_followers`, `x_views`, `x_likes`, and optional post counts. Use
        `scripts/fetch_metrics.py` for live read-only account API metrics
        (`--latest`, `--yesterday`, `--since-date`, and `--until-date` for
        review windows; `--tweet-id` for exact post metrics; `--deep` for
        retention/click fields when authorized) or
        `scripts/normalize_metrics.py` for local JSON/CSV exports.
  - [ ] For metrics, run `scripts/validate_metrics.py` against the produced
        snapshot before treating the skill-local contract as proven.
  - [ ] For metrics, use `source_gap` when a metric is unavailable; do not
        write zero unless the platform actually returned zero.
  - [ ] For publishing, record post IDs/URLs only after the API confirms the
        mutation, then append/update the local content ledger with
        `farplane content add --platform x --external-id <post_id> --url <url>
        --status posted --approval approved --published-at <timestamp>
        --campaign <campaign> --kpis x_views,x_likes,evidence_distribution_reach
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
  "source_id": "manual_x_account",
  "date": "2026-06-30",
  "status": "available",
  "observations": [
    {"metric_id": "x_followers", "date": "2026-06-30", "value": 1234, "status": "available"},
    {"metric_id": "x_views", "date": "2026-06-30", "value": 5600, "status": "available"},
    {"metric_id": "x_likes", "date": "2026-06-30", "value": 430, "status": "available"}
  ]
}
```

## Gotchas

- X API access is paid/rate-limited; do not run live calls unless budget and
  credentials are explicit.
- User-context metrics can require stronger auth than public profile reads.
- Posting is an external mutation and always needs explicit approval.

## Reference Map

- `references/api.md` - load for X API endpoint/auth grounding before live API work.
- `references/metrics-snapshot.md` - load when importing or normalizing account metrics.
- `scripts/check_config.py` - check private env readiness without printing secrets.
- `scripts/fetch_metrics.py` - fetch read-only account/profile/post metrics and write KPI observations.
  Use no post IDs for account snapshot mode; repeat `--tweet-id` for exact post metrics.
  Use `--latest`, `--yesterday`, `--since-date`, or `--until-date` to select
  posts for content review while preserving the aggregate KPI observation
  output.
  Add `--deep` for retention/click observations such as `x_retention_score`,
  `x_video_completions`, `x_profile_clicks`, and `x_url_clicks` when the API
  returns owned-content analytics.
- `scripts/publish_post.py` - dry-run or publish an approved X post/thread
  from JSON using OAuth 2.0 user auth. If the stored OAuth 2.0 access token is
  unauthorized and refresh credentials exist, the script refreshes OAuth 2.0
  and saves the refreshed token back to private `~/.farplane/config.toml`
  before retrying, unless `--no-save-refreshed-token` is set. It falls back to
  OAuth 1.0a user-context for text-only posts if refresh/retry fails. Defaults
  to dry-run; live mutation requires `--execute`, `--account-alias`, and
  `--approval-ref`. Supports local image upload and chunked video/GIF upload
  before `POST /2/tweets` when OAuth 2.0 user auth is valid or refreshable.
  Dry-run writes a stable `draft` row to `.farplane/content/ledger.jsonl` by
  default; confirmed publish updates that row to `posted` with the returned
  tweet ID and URL.
- `scripts/validate_metrics.py` - validate X metric snapshot shape, metric IDs,
  redaction, and blocked/source-gap semantics without external API calls.
- `scripts/validate_post_payload.py` - validate post/thread JSON without account mutation.
- `scripts/normalize_metrics.py` - normalize JSON/CSV metric exports to Farplane KPI observations.
- `farplane content add` - append/update `.farplane/content/ledger.jsonl` after
  a confirmed publish so interval refresh can fetch owned-content metrics.
- `eval_task.json` - agent-behavior eval rows for live metrics and missing-credential flows.

## Output

- `draft_validation`: platform-fit verdict, blocking issues, and fixed draft suggestions.
- `metrics_snapshot`: normalized observations and output path.
- `publish_result`: post IDs, URLs, timestamp, and redacted credential source.
- `blocked_report`: missing binding, missing credential, missing approval, or API/source gap.
