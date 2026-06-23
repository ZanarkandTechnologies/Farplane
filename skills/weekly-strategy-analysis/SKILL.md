---
name: weekly-strategy-analysis
description: "Turn Kenji's weekly plans, Notion tasks, meetings, Codex threads, and opportunities into priorities, dates, drift analysis, and follow-up agenda."
tier: 3
group: personal-ops
source: local
skill_template_version: "0.2.0"
eval: eval_task.json
allowed-tools: Read, Glob, Grep, Bash
---

# Weekly Strategy Analysis

## Context

Use this skill for Kenji's weekly strategy and opportunity planning automation.
It is a Kenji/life-specific wrapper over the generic
[horizon-update](../horizon-update/SKILL.md) shape. The generic horizon skill
owns the reusable strategy/report/goals-delta contract; this skill owns Kenji's
source collection, private context lookup, lane handoffs, and chat-ready report
order.

## Skill Signature

```text
weekly_strategy_analysis(
  project_root = "/Users/kenjipcx/life",
  memory_ref = "docs/MEMORY.md",
  private_tools_ref = "/Users/kenjipcx/.codex/private/TOOLS.md",
  codex_telemetry_ref? = "Farplane-UI session usage / telemetry export",
  output_dir = "docs/strategy-automation/runs/",
  phase_hooks?
) -> context_bundle
   + lane_outputs
   + weekly_strategy_report
   + memory_update_candidates
   + source_gaps

state:
  reads(memory_ref, private_tools_ref?, notion-context views,
        codex_telemetry_ref?, Farplane-UI session usage when supplied,
        feed-scout config or public opportunity sources)
  writes(output_dir/<date>-weekly-strategy-context.md,
         output_dir/<date>-weekly-strategy-lanes/*.md,
         optional output_dir/<date>-weekly-strategy-context.json,
         proposed docs/MEMORY.md, docs/TROUBLES.md, docs/LESSONS.md,
         docs/HISTORY.md deltas)

gates:
  review_window_defined; private_tools_loaded_or_labeled; sources_normalized;
  context_bundle_written_before_lanes; lane_handoffs_use_file_refs;
  lane_outputs_written_before_final_report; source_gaps_named;
  private_data_redacted; no_notion_mutation; no_publish_deploy_spend

routes:
  horizon-update | notion-context | feed-scout | summarize |
  review

fails:
  vague status digest; lanes reading hidden chat instead of bundle files;
  lanes refetching all source data; generic strategy prose without evidence;
  raw private dumps in memory/report; fabricated missing tasks, meetings,
  threads, or opportunities
```

Cadence, target thread, live automation name, and exact schedule are supplied by
the automation wrapper. This skill only needs to know the project root, source
refs, output directory, evidence rules, and writeback gates.

<!-- BEGIN FARPLANE_IMPORTANT_CHECKLIST -->
## Todo List

- [ ] 1. Initialize the weekly run.
  - [ ] Use a recommendation-first, high-agency planning stance; no passive
        status digest.
  - [ ] Read `/Users/kenjipcx/life/docs/MEMORY.md` near the start.
  - [ ] Load `/Users/kenjipcx/.codex/private/TOOLS.md` when present before
        using user-specific Notion handles.
  - [ ] Define the review window in Asia/Kuala_Lumpur time: Monday 00:00 to
        the Sunday run timestamp by default, or the previous Monday-Sunday week
        when run after the week closes.
- [ ] 2. Gather and normalize context.
  - [ ] Fetch latest pinned `Plan Week` page and body through `notion-context`.
  - [ ] Fetch pinned planning pages, this week's forward-looking tasks,
        review-window `Done` tasks, review-window `Status != Done` tasks,
        not-done projects, active goals, and meeting notes.
  - [ ] Normalize tasks, meetings, projects/goals, and people/org signals into
        compact rows with source URLs or evidence pointers.
  - [ ] Fetch Codex drift evidence from Farplane-UI / Codex app-server
        telemetry when supplied; otherwise label the telemetry gap and use the
        fallback path in
        [references/lane-codex-drift.md](references/lane-codex-drift.md).
  - [ ] Refresh the compact Notion status cache when possible; preserve the
        previous cache and label failure when refresh is unavailable.
  - [ ] Gather public opportunity seeds by calling `feed-scout` when configured;
        otherwise use the bounded search strategy in
        [references/lane-opportunity-scan.md](references/lane-opportunity-scan.md).
- [ ] 3. Write the context bundle.
  - [ ] Write `docs/strategy-automation/runs/<YYYY-MM-DD>-weekly-strategy-context.md`
        before analysis lanes run.
  - [ ] Include review window, source/tool status, Plan Week, pinned pages,
        done tasks, not-done tasks, projects, goals, meeting notes, people
        signals, Codex thread summaries, opportunity seeds, source gaps, and
        raw evidence pointers.
  - [ ] Keep raw dumps bounded; use normalized rows, short excerpts, and
        evidence pointers instead of full page/session dumps.
- [ ] 4. Run analysis lanes from file refs.
  - [ ] Create lane handoffs that list the context bundle path, lane output
        path, evidence rules, and exact lane question.
  - [ ] Run lanes in native subagents in parallel when available; otherwise run
        them sequentially. Every lane reads the context bundle and writes its
        own file under `docs/strategy-automation/runs/<YYYY-MM-DD>-weekly-strategy-lanes/`.
  - [ ] Run `plan-progress` using
        [references/lane-plan-progress.md](references/lane-plan-progress.md).
  - [ ] Run `meeting-people` using
        [references/lane-meeting-people.md](references/lane-meeting-people.md).
  - [ ] Run `codex-drift` using
        [references/lane-codex-drift.md](references/lane-codex-drift.md).
  - [ ] Run `opportunity-scan` using
        [references/lane-opportunity-scan.md](references/lane-opportunity-scan.md).
  - [ ] Reject lane outputs that do not cite context bundle evidence or raw
        pointers.
- [ ] 5. Synthesize the weekly strategy report.
  - [ ] Produce separated retro: `Done`, `Not done`, `Meetings / people`, and
        `Codex drift`.
  - [ ] Label completed work as `needle-mover`, `maintenance`, `exploration`,
        or `noise`; label unfinished work as `still important`, `blocked`,
        `stale`, `should delegate`, or `should kill`.
  - [ ] Convert changed insight to implication to action; label signals as
        `strong signal`, `weak signal`, or `needs one more proof point`.
  - [ ] Recommend top 3-5 directions for the coming week and 3-7 deprioritized
        or killed directions when useful, with dates and proof expectations.
  - [ ] Separate solo work, people-facing follow-ups, and background-agent
        work. Mark inferred due dates as inferred.
- [ ] 6. Finish and write back.
  - [ ] Produce the final report in this order: `Recommended focus`, `Last
        week: progress vs drag`, `Codex drift`, `Grand-plan delta`, `Priority /
        deprioritize with dates`, `Opportunity scan`, `Follow-up agenda`.
  - [ ] Mention the context bundle path and lane output paths used for
        evidence.
  - [ ] Propose durable updates for `docs/MEMORY.md`, `docs/TROUBLES.md`,
        `docs/LESSONS.md`, and `docs/HISTORY.md`; do not store secrets, raw
        Notion IDs, saved-view URLs, private page dumps, or unsanitized
        personal data.
<!-- END FARPLANE_IMPORTANT_CHECKLIST -->

## Source Normalization

- Task rows: `Name`, `Status`, `Act Time`, `Task Due Date`, `Project`,
  `Projects`, `Goals`, `Description`, `Attention Required`, `Pinned`, `Tags`,
  `Related Entities`, `execution_context`, `context_gap`, `url`.
- Meeting rows: `title`, `date`, `attendees_or_orgs`, `decisions`,
  `opportunities`, `commitments`, `blockers`, `follow_ups`,
  `related_projects`, `related_goals`, `url`.
- Codex thread rows: `id`, `thread_name`, `updated_at`, `cwd`, `user_intent`,
  `actual_work_summary`, `artifacts_or_files`, `project_or_goal_guess`,
  `status`, `tokens_used`, `turn_count`, `created_at`, `closed_at_or_updated_at`,
  `duration_proxy`, `attention_proxy`, `evidence_path`, `drift_class`.

Drop raw formulas, formula URLs, counters, system/developer/base instructions,
encrypted reasoning, secrets, auth files, sqlite databases, huge prompts, full
private contact details, and unrelated logs unless needed for diagnostics.

## Lane Contract

Each lane receives a handoff like:

```text
lane_task(
  context_bundle = "<path>",
  lane_output = "<path>",
  lane_question = "<specific question>",
  evidence_rule = "cite bundle rows or raw evidence pointers",
  stop_rule = "write findings, confidence, source gaps, and next actions"
)
```

Lane outputs must include findings with evidence pointers, confidence labels,
source gaps, concrete next actions, and claims rejected for lack of evidence.

## Hard Gates

- Do not mutate Notion task status.
- Do not publish, deploy, spend money, scrape private contact details, or
  perform destructive cleanup.
- Do not make public claims from private meeting notes.
- Do not fabricate unavailable tasks, meetings, people context, threads, or
  opportunities.
- Do not let public opportunity scanning dominate stronger obligations from
  tasks, meetings, or actual Codex work.

## Reference Map

- [templates/context-bundle.md](templates/context-bundle.md) - use for the
  weekly context bundle shape.
- [references/weekly-pm-plan-instance.md](references/weekly-pm-plan-instance.md)
  - compile this wrapper as a `horizon_update(...)` call with phase hooks.
- [references/lane-plan-progress.md](references/lane-plan-progress.md) - read
  before spawning the `plan-progress` lane.
- [references/lane-meeting-people.md](references/lane-meeting-people.md) -
  read before spawning the `meeting-people` lane.
- [references/lane-codex-drift.md](references/lane-codex-drift.md) - read
  before spawning the `codex-drift` lane.
- [references/lane-opportunity-scan.md](references/lane-opportunity-scan.md) -
  read before spawning the `opportunity-scan` lane.
- [../horizon-update/SKILL.md](../horizon-update/SKILL.md) - generic horizon
  contract this wrapper configures.
