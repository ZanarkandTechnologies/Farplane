---
schema: farplane_project_automation
framework_template_version: 1.0.0
owner: automation-advisor
id: farplane-thread-sweep
name: Farplane Thread Sweep
kind: cron
status: active
runtime: claude
runtime_task: farplane-thread-sweep
target:
  workspace: /Users/kenjipcx/Zanarkand Technologies/projects/Farplane
schedule:
  type: daily
  timezone: Europe/London
  time: "07:36"
---
Close out Kenji's Claude desktop threads once a day so he starts the day with a
few open threads and one list of decisions, instead of many threads each
waiting on him.

1. **Snapshot.** Call `list_sessions` (limit 100, archived excluded) for titles,
   running state, last activity and links. For each listed session, read its
   status from `~/Library/Application Support/Claude/claude-code-sessions/*/*/<sessionId>.json`:
   the `postTurnSummary` fields `status_category`, `status_detail` and
   `needs_action`, plus `scheduledTaskId`. If a waiting thread's ask is unclear,
   read the last assistant message in its transcript
   (`~/.claude/projects/*/<cliSessionId>.jsonl`, tail only).
2. **Sort each thread into one group**, skipping this run's own session:
   - **Working:** running, or active in the last 60 minutes. Leave it alone.
   - **Done:** `status_category` is `completed` and `needs_action` is empty, or
     it is a finished scheduled-task run older than 12 hours (its output is on
     disk). Archive it.
   - **Waiting on Kenji:** `blocked` or `review_ready`, or a non-empty
     `needs_action`. Keep it open and put it in the decision list. If it has
     waited more than 3 days with no reply, archive it as parked instead and
     still list its question.
   - **Fold together:** waiting threads stuck on the same cause (the same
     repository change, ticket, or decision). Name one thread to keep and say
     what the others should hand to it. Don't send messages; Kenji does that.
3. **Decide what you can.** For each waiting item, give a recommended answer
   with a one-line reason, using the thread's own recommendation when it has
   one. Mark an item **Kenji's call** only when it spends money, publishes or
   messages people under his name, can't be undone, or reverses something he
   decided himself.
4. **Archive** the Done and parked threads with `archive_session` (reason
   "Thread Sweep: done" or "Thread Sweep: parked after 3 days"). Archiving can
   be undone from the Archived list. If a call is refused (pinned, open on
   screen, or still working), leave that thread and note it.
5. **Write** `.farplane/reports/thread-sweep/<YYYY-MM-DD>.md`.

Report and final reply, under ~300 words:

```text
**Threads: <before> open → <after> open** (<n> archived, <m> parked)

Decide today
1. <thread title (link)> — <the ask> → **<recommended answer>** (<reason>)
...

Fold together
- Keep <thread>; fold <thread>, <thread> into it: <shared cause>

Working (left alone): <titles>
Archived: <titles>
```

Use each session's `link` for thread links in the report file. Keep numbering
stable so Kenji can reply "1 yes, 2 freeze".

Rules: never delete a session, never unarchive one, and never send messages
or touch repositories, issues, or Notion. Archive only Done and parked
threads. If session tools aren't available in this run, write the report
without archiving and say so on the first line.

Config source:
farplane/automations/thread-sweep.md id="farplane-thread-sweep"
