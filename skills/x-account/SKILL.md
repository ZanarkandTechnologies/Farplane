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
in `farplane/bindings.md`; credentials live under `~/.codex/private/social.env`
or the runtime environment using the `FARPLANE_X_` prefix.

## Skill Signature

```text
x_account(action, artifact?, account_binding?, date_window?, source_file?)
  -> draft_validation | publish_result | metrics_snapshot | blocked_report
state:
  reads(farplane/bindings.md, ~/.codex/private/docs/social.md?,
        ~/.codex/private/social.env?, source_file?)
  writes(.farplane/metrics/manual/x_account.json when normalizing exports)
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
  - [ ] Resolve the account alias from `farplane/bindings.md`.
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
  - [ ] For metrics, write observations compatible with
        `.farplane/metrics/ui/latest.json` inputs: `x_followers`, `x_views`,
        `x_likes`, and optional post counts. Use
        `scripts/fetch_metrics.py` for live read-only account API metrics
        (`--tweet-id` for exact post metrics, `--deep` for retention/click
        fields when authorized) or
        `scripts/normalize_metrics.py` for local JSON/CSV exports.
  - [ ] For metrics, use `source_gap` when a metric is unavailable; do not
        write zero unless the platform actually returned zero.
  - [ ] For publishing, record post IDs/URLs only after the API confirms the
        mutation.
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
  Add `--deep` for retention/click observations such as `x_retention_score`,
  `x_video_completions`, `x_profile_clicks`, and `x_url_clicks` when the API
  returns owned-content analytics.
- `scripts/validate_post_payload.py` - validate post/thread JSON without account mutation.
- `scripts/normalize_metrics.py` - normalize JSON/CSV metric exports to Farplane KPI observations.
- `eval_task.json` - agent-behavior eval rows for live metrics and missing-credential flows.

## Output

- `draft_validation`: platform-fit verdict, blocking issues, and fixed draft suggestions.
- `metrics_snapshot`: normalized observations and output path.
- `publish_result`: post IDs, URLs, timestamp, and redacted credential source.
- `blocked_report`: missing binding, missing credential, missing approval, or API/source gap.
