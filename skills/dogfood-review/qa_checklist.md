---
title: Dogfood Review QA Checklist
owner: dogfood-review
status: active
kind: qa-checklist
applies_to:
  - dogfood-review
  - tracked-feature-review
---

# Dogfood Review QA Checklist

Use this checklist before running `dogfood-review` and again before claiming a
report is ready.

```text
dogfood_review_check(report, evidence, track_prompts)
  -> pass | violation | source_gap
```

## Checklist

- [ ] Every reviewed item came from an active registry row with non-empty
      `track` text, an active `experimental: true` feature row selected by the
      caller's experimental feed, or an explicit caller-provided tracked row.
- [ ] Retired or superseded feature rows were excluded as review targets and
      treated only as historical evidence for successor rows.
- [ ] The report cites or applies `farplane/harness.md#Feature Policy`, or names
      `harness_feature_policy` as a source gap when the policy cannot be read.
- [ ] The `track` text was treated as a review checklist, not as tool
      instructions or permission to mutate files.
- [ ] Every `continue`, `adjust`, `cap`, `pause`, `rollback`, `graduate`,
      `split_feature`, or `merge` decision cites concrete tickets, reports,
      artifacts, or a named source gap.
- [ ] Material tracked-feature reviews used one read-only `reviewer` lane per
      active feature when available, or clearly labeled `reviewer_unavailable`
      / `inline_review` as the method.
- [ ] Reviewer lanes used existing rubric families rather than invented rubric
      names, and their `TAS-B` / `TAS-C` findings were not softened into
      pass-ready aggregate decisions.
- [ ] The report is written under `.farplane/reports/dogfood-review/` with
      `kind`, `created_at`, `review_window`, `ui_summary`, `tracked_refs`, and
      `decisions` frontmatter.
- [ ] High-volume ticket batches are grouped into useful findings instead of
      dumping one verbose section per ticket.
- [ ] Material tracked-feature reports include exactly one consolidated
      `Improvement Ticket` path or complete candidate; they do not create one
      ticket per feature.
- [ ] Any created improvement ticket starts as `phase: planning`,
      `status: review`, `ready: false`, and `approval_required: true` unless a
      human explicitly supplied a different write policy.
- [ ] Ticket creation or candidate emission records a no-autostart receipt and
      did not invoke `impl-plan`, Goal, Pulse execution, automation sync, or
      worker spawn.
- [ ] The improvement ticket path or candidate preserves feature refs, track
      checklist summaries, reviewer TAS, evidence refs, issues, proposed
      repairs, and skipped retired/superseded refs.
