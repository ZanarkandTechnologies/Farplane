---
title: Feedback Primitive Implementation Loop
owner: harness-creator
status: accepted
kind: skill-audit
created_at: 2026-06-30
source_ticket: TASK-0249
---

# Feedback Primitive Implementation Loop

## Trigger

While wiring Farplane social KPIs, the harness had enough strategy shape to
name metrics such as X/Instagram followers, views, likes, and retention, but it
did not force the missing feedback capability to become a runnable primitive.
The work had to be discovered manually: create account skills, private env
setup, bindings, fetch scripts, normalization scripts, eval rows, QA checklists,
proof plan, and KPI registry rows.

## Delta

`harness-creator` now treats missing feedback/KPI instrumentation as a
first-class implementation plan, not a vague unblock ticket.

The checklist requires:

- `metric_binding(metric_id, source, fetch_skill, auth_status, storage_path,
  display, proof_command)` for live or missing KPI sources.
- feedback primitive plans with source grounding, private env keys,
  non-secret bindings, KPI rows, storage path, scripts, evals, QA, blocked-mode
  proof, and live proof commands.
- routing through project-local skills for project-specific primitives, or
  `skill-creator` for reusable root skill packages.

## Example

```text
feedback_primitive_implementation_plan {
  capability: instagram_reels_retention_metrics
  owner_surface: root_skill
  trigger: "Need KPI-ready Reels retention score"
  input_ids_or_export_shape: "media_id + duration_seconds"
  official_or_source_grounding: "Instagram media insights docs"
  private_env_keys: FARPLANE_INSTAGRAM_ACCESS_TOKEN, FARPLANE_INSTAGRAM_BUSINESS_ACCOUNT_ID
  non_secret_bindings: farplane/bindings.yaml Social Account + Metric Source rows
  kpi_rows: instagram_retention_score
  storage_path: .farplane/metrics/manual/instagram_account.json
  scripts: check_config.py, fetch_metrics.py, normalize_metrics.py
  eval_rows: branch choice + blocked credentials + retention request
  qa_checklist_branches: Universal, Metrics
  blocked_mode_proof: fetch script reports missing keys only
  live_proof_command: fetch_metrics.py --media-id <id> --deep --duration-seconds <s>
}
```

## Verification

Run:

```bash
python3 skills/skill-maintenance/scripts/check_skills.py --write
```
