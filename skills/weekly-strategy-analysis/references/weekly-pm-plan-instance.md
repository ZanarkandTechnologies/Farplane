---
title: Weekly Strategy Analysis As Horizon Update Instance
owner: weekly-strategy-analysis
kind: reference
---

# Horizon Update Instance

Represent Kenji's weekly strategy automation as:

```text
horizon_update(
  project_root = "/Users/kenjipcx/life",
  lane_policy = weekly_horizon_lane_policy,
  goals = kenji_weekly_context_refs.goals_ref,
  reports = kenji_weekly_context_refs.report_refs,
  tickets = kenji_weekly_context_refs.task_refs,
  memory = kenji_weekly_context_refs.memory_refs,
  interval_policy = monday_to_sunday_or_run_timestamp,
  phase_hooks = {
    init_prompt,
    context_gathering_prompt,
    synthesis_prompt,
    reporting_prompt
  }
) -> horizon_report + rhythm_guidance + memory_update_candidates
```

## Context Refs

```text
kenji_weekly_context_refs = {
  goals_ref: "/Users/kenjipcx/life/docs/MEMORY.md",
  memory_refs: [
    "/Users/kenjipcx/life/docs/MEMORY.md",
    "/Users/kenjipcx/life/docs/TROUBLES.md",
    "/Users/kenjipcx/life/docs/LESSONS.md",
    "/Users/kenjipcx/life/docs/HISTORY.md"
  ],
  private_context_refs: [
    "/Users/kenjipcx/.codex/private/TOOLS.md"
  ],
  task_refs: "notion-context: Plan Week, Tasks, Projects, Goals",
  meeting_refs: "notion-context: meeting notes for review window",
  metrics_refs: [
    "Farplane-UI session usage / telemetry export when supplied",
    "Codex app-server session timeline usageSummary when accessible"
  ],
  thread_index_ref: "Codex/Farplane-UI thread/session timeline source",
  opportunity_sources: [
    "feed-scout tracked profiles/entities/resources when configured",
    "bounded public web search from lane prompt otherwise"
  ],
  output_bundle_dir: "/Users/kenjipcx/life/docs/strategy-automation/runs/"
}
```

## Phase Hooks

`init_prompt`:

- Use recommendation-first weekly planning.
- Read durable memory near the start.
- Define the review window and label source/tool availability.
- Do not mutate Notion, CRM, public pages, or external systems.

`context_gathering_prompt`:

- Fetch Plan Week, pinned planning pages, done tasks, not-done tasks, active
  projects/goals, meetings, people/org signals, Codex/Farplane-UI telemetry,
  and opportunity seeds.
- Normalize rows and write a bounded context bundle before analysis lanes.
- Load lane references only when constructing subagent prompts.

`synthesis_prompt`:

- Run lane workers from file refs, preferably in parallel.
- Synthesize from lane outputs, not hidden chat state.
- Convert changed insight to implication to action.
- Separate priority changes, depriorities, daily guidance, and memory
  writeback candidates.

`reporting_prompt`:

- Return a chat-ready weekly report in this order: `Recommended focus`, `Last
  week: progress vs drag`, `Codex drift`, `Grand-plan delta`, `Priority /
  deprioritize with dates`, `Opportunity scan`, `Follow-up agenda`.
- Mention context bundle and lane output paths.
- Propose memory/trouble/lesson/history deltas without writing secrets,
  private IDs, raw page dumps, or unsanitized personal data.
