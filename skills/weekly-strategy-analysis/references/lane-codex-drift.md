---
title: Codex Drift Lane
owner: weekly-strategy-analysis
kind: lane-reference
---

# Codex Drift Lane

```text
codex_drift_lane(context_bundle, lane_output, telemetry_ref?)
  -> attention_map + alignment_buckets + calibration_note
```

Question: where did Codex attention actually go, and what does that say about
planning accuracy?

## Preferred Data

Use Farplane-UI / Codex app-server telemetry when supplied in the context
bundle:

- session timeline `usageSummary`.
- per-thread token totals, cost totals, model/provider, last response time, and
  available 24h/7d aggregates.
- thread/session timeline items, status, title, project mapping, and artifacts.
- parent/child spawned-thread lineage when available.

If the weekly automation supplies a Farplane-UI telemetry export or report, use
that as the primary evidence. Do not scrape raw local Codex files when a clean
telemetry projection is available.

## Fallback Data

When Farplane-UI telemetry is missing or incomplete, label the source gap and
use local raw sources in this order:

1. `~/.codex/state_*.sqlite` `threads`: `id`, `rollout_path`, timestamps,
   `cwd`, `title`, `first_user_message`, `preview`, `tokens_used`, source,
   model, archive status.
2. `~/.codex/state_*.sqlite` `thread_spawn_edges`: parent/child lineage.
3. `/Users/kenjipcx/.codex/session_index.jsonl`: thread IDs, names, updates.
4. `/Users/kenjipcx/.codex/history.jsonl`: user-turn counts per session.
5. Selected rollout JSONL files only for high-impact or ambiguous threads.
6. `~/.codex/logs_*.sqlite` only for activity timing or failure diagnostics.

## Metrics

Attention is a proxy, not exact wall-clock time. Prefer:

- Farplane-UI `usageSummary` totals.
- total tokens and estimated cost.
- turn count.
- elapsed thread window.
- spawned child thread count.
- artifact/output count.
- manual classification from title, preview, intent, and summary.

Classify each cluster as:

- `planned execution`
- `necessary unplanned work`
- `strategic discovery`
- `maintenance`
- `avoidable drift`
- `unclear`

Output:

- `attention_map`: cluster, threads, usage/attention proxy, project/goal.
- `alignment_buckets`: bucket, evidence, why it belongs there.
- `drift_causes`: unrealistic plan, underspecified task, new evidence, tool
  failure, dependency, curiosity spiral, or genuine leverage.
- `calibration_note`: what to plan differently next week.
- source gaps and rejected claims.
