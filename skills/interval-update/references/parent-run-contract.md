---
title: "Interval Parent Run Contract"
status: active
owner: interval-update
kind: reference
---

# Interval Parent Run Contract

This reference restates the non-optional parent orchestration contract in a
shareable shape for audits, workflow refs, and future compaction passes. The
first-load authority remains `SKILL.md`.

```text
interval_parent_run(config, context_refs, workflow_flags)
  -> context_bundle(summary_context, raw_evidence_pointers)
   + isolated_workflow_lanes
   + workflow_findings
   + dated_interval_report
   + allowed_post_report_deltas
```

Parent responsibilities:

- Resolve defaults and configured refs.
- Build `summary_context` plus `raw_evidence_pointers`.
- Spawn one isolated read-only subagent lane for each enabled report workflow.
- Run deterministic helper scripts inline only for mechanical discovery.
- Collect workflow findings and run final synthesis.
- Write the dated report before durable ticket, product, or goals mutation.
- Apply only explicitly allowed post-report deltas.

Lane rules:

- Workflow lanes consume `summary_context` first.
- Workflow lanes open `raw_evidence_pointers` only for cited proof, source-gap
  classification, or an explicit workflow exception.
- Analysis lanes are read-only by default and must not edit tickets, goals,
  product files, automation state, or external systems.
- `reward_checkins` is the gated exception and may propose only the ticket
  Reward actual and score fields named by its workflow contract. The parent
  applies those patches only after the dated report records them as allowed
  post-report deltas.
