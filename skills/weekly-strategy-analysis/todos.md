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
      `/Users/kenjipcx/coding-harness/Codexter/.harness/state/notion-context/latest-status-context.md`.
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
