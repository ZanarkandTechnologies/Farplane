---
name: weekly-strategy-analysis
description: "Turn weekly plans, tasks, meetings, people signals, Codex threads, and opportunities into priorities, due dates, and drift analysis."
tier: 3
group: personal-ops
source: local
allowed-tools: Read, Glob, Grep, Bash
---

# Weekly Strategy Analysis

Use this skill for Kenji's weekly strategy automation and any manual weekly
review that needs to reconcile planned goals with actual Notion tasks,
meeting notes, people signals, Codex threads, and opportunity research.

<!-- BEGIN FARPLANE_IMPORTANT_CHECKLIST -->
## Todo List

- [ ] Use a direct, high-agency planning stance: recommendation first,
      tradeoffs explicit, no passive status digest.
- [ ] Load private tool context before fetching user-specific handles: start
      with `/Users/kenjipcx/.codex/private/TOOLS.md` when it exists, then any
      focused Notion docs it references.
- [ ] Define and state the exact review window in Asia/Kuala_Lumpur time before
      querying data.
- [ ] Use Monday 00:00 through the Sunday run timestamp by default, or the
      previous Monday-Sunday week when run after the week fully closes.
- [ ] If a canonical Notion view has stale hard-coded dates, update or
      approximate the review-window query and label the approximation.
- [ ] Fetch the latest pinned `Plan Week` page through `notion-context`.
- [ ] Read the selected `Plan Week` page body, not just its row properties.
- [ ] Read required recent pinned planning pages through the pinned-read
      discipline from `notion-context`.
- [ ] Fetch this week's Tasks view for forward-looking planning context.
- [ ] Fetch review-window completed tasks separately and locally keep only
      rows with `Status: Done`.
- [ ] Fetch review-window unfinished tasks separately where `Status != Done`,
      including `Not started`, `In progress`, `Review`, `Failed`, and planned
      backlog rows inside the week.
- [ ] Normalize done and not-done task rows to `Name`, `Status`, `Act Time`,
      `Task Due Date`, `Project`, `Projects`, `Goals`, `Description`,
      `Attention Required`, `Pinned`, `Tags`, `Related Entities`,
      `execution_context`, `context_gap`, and `url`.
- [ ] Drop raw formulas, formula result URLs, counters, and noisy fields unless
      they are needed for diagnostics.
- [ ] Fetch not-done projects and active goals.
- [ ] Enrich both task groups with project and active-goal context before
      judging impact.
- [ ] Fetch Notion meeting notes from the same review window before strategy
      reasoning.
- [ ] Prefer the dedicated meeting-notes query surface when available; label
      the connector/view gap if meeting notes cannot be queried.
- [ ] Normalize meeting notes to title, date, attendees/people, creator,
      decisions, opportunities, commitments, blockers, follow-ups, related
      projects/goals/tasks, and URL.
- [ ] Group meeting insights by person or organization when useful.
- [ ] Identify repeated people, high-leverage relationships, promised
      follow-ups, and emerging opportunity clusters.
- [ ] Do not expose private contact details such as emails or phone numbers.
- [ ] Fetch Codex thread evidence from `/Users/kenjipcx/.codex/session_index.jsonl`
      for the same review window.
- [ ] Resolve matching session files under `~/.codex/sessions/**` and
      `~/.codex/archived_sessions/**` only when deeper evidence is needed.
- [ ] Parse Codex session JSONL conservatively: keep metadata, user intent,
      final summaries, useful commands/results, and artifact paths.
- [ ] Ignore system/developer/base instructions, encrypted reasoning, secrets,
      auth files, sqlite databases, huge prompts, and unrelated logs.
- [ ] Normalize each Codex thread to id, name, update time, cwd, intent, actual
      work, artifacts, project/goal guess, status, and evidence path.
- [ ] Classify each thread as `aligned execution`, `useful detour`,
      `strategic discovery`, `maintenance`, or `drift`.
- [ ] Do not count automation/system maintenance as strategic progress unless
      it directly supported a live project or goal.
- [ ] Refresh the compact Notion status cache at
      `/Users/kenjipcx/coding-harness/Farplane/.farplane/state/notion-context/latest-status-context.md`.
- [ ] If Notion status refresh fails, preserve the previous cache and write a
      clear error note when possible.
- [ ] Write the bounded local context bundle before deep synthesis.
- [ ] Include source/tool status, Plan Week summary, pinned pages, done tasks,
      not-done tasks, projects, goals, meeting notes, people signals, Codex
      threads, opportunity seeds, gaps, and raw evidence pointers in the bundle.
- [ ] Keep raw dumps bounded; use normalized rows, short excerpts, and source
      pointers instead of dumping whole sessions or page bodies.
- [ ] Split deep analysis into bounded lanes, preferably native subagents, each
      reading the context bundle instead of refetching source data.
- [ ] Run a task-progress lane for done vs not-done impact, drag, blockers,
      stale work, carry-forward calls, delegation, and kill decisions.
- [ ] Run a meeting-people lane for relationship leverage, commitments, new
      directions, follow-ups, and people/org opportunity clusters.
- [ ] Run a Codex-thread-drift lane comparing actual agent work against Plan
      Week, tasks, projects, and goals.
- [ ] Run a grand-plan-priority lane for changed assumptions, strategic
      implications, priorities, depriorities, due dates, and proof checks.
- [ ] Run an opportunity-scan lane using public sources aligned with the
      current Notion, meeting, people, and Codex-thread evidence.
- [ ] Require every lane to cite bundle evidence or raw source pointers; reject
      generic strategy prose.
- [ ] Produce a separated retro with `Done work`, `Not-done / carried work`,
      `Meetings / people signals`, and `Codex thread drift`.
- [ ] Answer whether projects/goals saw meaningful needle-moving progress.
- [ ] Label done-work clusters as `needle-mover`, `maintenance`,
      `exploration`, or `noise`.
- [ ] Label not-done work as `still important`, `blocked`, `stale`,
      `should delegate`, or `should kill`.
- [ ] Name the 3-7 highest-leverage completed tasks or clusters and the
      project/goal each advanced.
- [ ] Name the 3-7 most important unfinished tasks or commitments and whether
      each should carry forward.
- [ ] Use meeting notes to explain when unfinished work is reasonable because
      calls changed the plan.
- [ ] Use Codex drift to explain what agent energy actually went toward versus
      what the plan said should matter.
- [ ] Name repeat/kill/delegate/artifact patterns from tasks, meetings, and
      Codex threads.
- [ ] Separate grand-plan evidence from tasks, meetings/people, Codex threads,
      and public opportunity scan.
- [ ] Identify new directions that emerged, old directions that weakened, and
      assumptions that changed.
- [ ] Label grand-plan signals as `strong signal`, `weak signal`, or
      `needs one more proof point`.
- [ ] Convert each changed insight into implication and action.
- [ ] Recommend the top 3-5 directions for the coming week with owner/context,
      why it matters, next action, due date, related goal/project, and proof of
      progress.
- [ ] Recommend 3-7 deprioritized or killed directions with reasons and revisit
      dates only when useful.
- [ ] Use existing `Act Time`, `Task Due Date`, meeting commitments, Codex
      drift, project focus, and active-goal urgency when setting dates.
- [ ] Mark inferred due dates as inferred.
- [ ] Separate solo work, people-facing follow-ups, and background-agent tasks.
- [ ] Fold in public opportunity research with links for cited events, orgs,
      grants, companies, and ecosystem signals.
- [ ] Prioritize industrial and healthcare AI deployment, Malaysia/SEA
      manufacturing and medical-device operations, factory automation, edge
      computer vision, smart glasses/perception, robotics/VLA deployment,
      knowledge graphs/business data, coding agents, and finance/ops AI.
- [ ] Explain why each opportunity fits or does not fit current strengths,
      relationships, meeting signals, actual Codex work, and constraints.
- [ ] Produce the final report in this order: `Recommended focus`,
      `Last week: progress vs drag`, `Codex drift`, `Grand-plan delta`,
      `Priority / deprioritize with dates`, `Opportunity scan`,
      `Follow-up agenda`.
- [ ] Mention the local context bundle path used for evidence.
- [ ] Name every source gap explicitly instead of fabricating missing tasks,
      meetings, calls, thread outcomes, or opportunities.
<!-- END FARPLANE_IMPORTANT_CHECKLIST -->

## Job

Produce one evidence-backed weekly operating review and plan:

1. Show whether completed and unfinished work moved Kenji's active goals.
2. Explain what changed in the grand plan based on tasks, meetings, people,
   Codex threads, and public opportunities.
3. Recommend what to prioritize and deprioritize next, with dates and proof of
   progress.
4. Detect drift between Plan Week / Notion intent and actual Codex thread work.

## Inputs

- Review window: default to the just-finished or finishing planning week.
  When the automation runs on Sunday, use Monday 00:00 through the run
  timestamp unless the latest Plan Week page clearly defines a different
  planning window. When run after the week closes, use the previous
  Monday-Sunday week.
- Notion context:
  - latest pinned `Plan Week` task page
  - recent pinned planning pages required by `notion-context`
  - review-window tasks where `Status: Done`
  - review-window tasks where `Status != Done`
  - not-done projects
  - active goals
  - meeting notes in the same date range
- Codex context:
  - `/Users/kenjipcx/.codex/session_index.jsonl`
  - matching files under `/Users/kenjipcx/.codex/sessions/**/rollout-*.jsonl`
    and `/Users/kenjipcx/.codex/archived_sessions/rollout-*.jsonl`
- Public opportunity scan:
  - current public events, companies, grants, markets, and ecosystem signals
    relevant to active goals and meeting signals.

## Context Bundle

Before synthesis, write:

```text
/Users/kenjipcx/life/docs/strategy-automation/runs/<YYYY-MM-DD>-weekly-strategy-context.md
```

When useful, also write:

```text
/Users/kenjipcx/life/docs/strategy-automation/runs/<YYYY-MM-DD>-weekly-strategy-context.json
```

Use [templates/context-bundle.md](templates/context-bundle.md) as the shape.

The bundle must include:

- review window
- source/tool status
- Plan Week summary
- pinned page summaries
- done tasks
- not-done tasks
- projects
- goals
- meeting notes and people signals
- Codex thread summaries
- opportunity scan seeds
- source gaps
- raw evidence pointers

Keep raw dumps bounded. Include normalized rows, short excerpts, and pointers to
raw pages or session files. Do not paste secrets, auth tokens, full system
prompts, base instructions, encrypted reasoning, private contact details, sqlite
database contents, or large unrelated logs.

## Source Collection Rules

### Notion

- Use `notion-context` for canonical task, project, and goal views.
- Load private Notion handles from private docs when `notion-context` requires
  user-specific database or saved-view identifiers.
- If a saved view has a stale date range, update the query or approximate the
  review window and label the approximation.
- Normalize task rows to:
  `Name`, `Status`, `Act Time`, `Task Due Date`, `Project`, `Projects`,
  `Goals`, `Description`, `Attention Required`, `Pinned`, `Tags`,
  `Related Entities`, `execution_context`, `context_gap`, and `url`.
- Keep `Done` and `not Done` task groups separate through synthesis.

### Meeting Notes And People

- Prefer the dedicated Notion meeting-notes query surface when available.
- Normalize each meeting note to:
  `title`, `date`, `attendees`, `people_or_orgs`, `decisions`,
  `opportunities`, `commitments`, `blockers`, `follow_ups`,
  `related_projects`, `related_goals`, and `url`.
- Group signals by person or organization when useful.
- Use meeting notes to explain why an unfinished task may be correct because
  the plan changed.

### Codex Threads

- Start with `~/.codex/session_index.jsonl`; filter rows by `updated_at`.
- Resolve matching session files by thread id only when the index is too thin
  for drift classification.
- Keep:
  `session_meta` cwd/source/model, user messages, explicit final assistant
  summaries, visible tool commands/results when useful, and artifact/file paths.
- Ignore:
  system/developer/base instructions, encrypted reasoning, huge raw prompts,
  secrets, auth files, sqlite databases, and unrelated logs.
- Normalize each thread to:
  `id`, `thread_name`, `updated_at`, `cwd`, `user_intent`,
  `actual_work_summary`, `artifacts_or_files`, `project_or_goal_guess`,
  `status`, and `evidence_path`.
- Classify against Plan Week/tasks/goals as:
  `aligned execution`, `useful detour`, `strategic discovery`, `maintenance`,
  or `drift`.
- Do not count automation/system maintenance as strategic progress unless it
  directly supports a live goal or project.

### Notion Status Cache

Refresh the compact local status cache inside this weekly run:

```text
/Users/kenjipcx/coding-harness/Farplane/.farplane/state/notion-context/latest-status-context.md
```

Include generated timestamp, source queries/pages used, current project/goal
aliases, and a factual status summary. If Notion access fails, preserve the
previous file and write a failure note beside it when possible.

## Analysis Lanes

Use native subagents when available. If not available, run the same lanes
sequentially against the context bundle and write lane outputs before final
synthesis. Each lane must reference evidence in the bundle or raw pointers.

1. `task-progress-analyst`: done vs not-done progress against projects/goals,
   needle-movers, drag, blocked/stale work, and carry-forward calls.
2. `meeting-people-analyst`: people/org signals, commitments, relationship
   leverage, new directions, and follow-up obligations.
3. `codex-thread-drift-analyst`: actual Codex threads vs Plan Week/tasks/goals,
   aligned work, useful detours, strategic discoveries, maintenance, and drift.
4. `grand-plan-priority-analyst`: grand-plan deltas, prioritized directions,
   deprioritized directions, due dates, and proof-of-progress checks.
5. `opportunity-scan-analyst`: public opportunity scan with links, grounded in
   current Notion, meeting, people, and Codex-thread evidence.

Do not accept generic strategy prose from a lane. Ask for evidence-backed
claims, confidence labels, and concrete next actions.

## Output Shape

Return one chat-ready report:

1. `Recommended focus`
2. `Last week: progress vs drag`
   - `Done`
   - `Not done`
   - `Meetings / people`
3. `Codex drift`
4. `Grand-plan delta`
5. `Priority / deprioritize with dates`
6. `Opportunity scan`
7. `Follow-up agenda`

Rules:

- Put the recommendation above the fold.
- In `Codex drift`, compare actual threads against planned tasks/goals.
- In `Grand-plan delta`, use `changed insight -> implication -> action`.
- In `Priority / deprioritize with dates`, distinguish solo work,
  people-facing follow-ups, and background-agent work.
- Mark inferred dates as inferred.
- Mention the local context bundle path used for evidence.

## Hard Gates

- Do not mutate Notion task status, publish, deploy, spend money, scrape private
  contact details, or perform destructive cleanup.
- Do not make public claims from private meeting notes.
- Do not fabricate unavailable tasks, meetings, threads, or people context.
- Do not let the public opportunity scan dominate the plan when tasks,
  meetings, or actual Codex work show a stronger near-term obligation.
