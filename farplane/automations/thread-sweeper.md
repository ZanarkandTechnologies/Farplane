---
schema: farplane_project_automation
framework_template_version: 1.0.0
owner: automation-advisor
id: farplane-thread-sweeper
name: Farplane Thread Sweeper
kind: cron
status: active
runtime: claude
runtime_task: farplane-thread-sweeper
target:
  workspace: /Users/kenjipcx/Zanarkand Technologies/projects/Farplane
schedule:
  type: active_hours_interval
  timezone: local
  active_hours: "08:00-22:00"
  interval_minutes: 120
---
Find agent threads in the Claude desktop app that went quiet before their work
was finished, get them moving again, and tell Kenji only what actually needs
him. The app already records each thread's last activity, so threads write
nothing for this job; the transcript is the source of truth.

Work in `/Users/kenjipcx/Zanarkand Technologies/projects/Farplane`.

Params:
idle_after = 3h
lookback = 72h (threads quiet longer than this are left alone)
max_nudges = 2
state = `.farplane/thread-sweeper/state.json`
report = `.farplane/reports/thread-sweeper/<YYYY-MM-DD>.md` (one section per run)

1. **List candidates.** Call `list_sessions` (session management tools) with
   limit 100. Keep sessions that are not archived, not running, and whose
   `lastActivityAt` is between `lookback` and `idle_after` ago. Drop this run's
   own session, any session whose `get_session` shows a `scheduledTaskId`
   (routine runs, including earlier sweeper runs), and any session in a sidebar
   group named `Parked`. Load `state` (missing file = empty). Skip a session
   whose `lastActivityAt` equals its `state.last_seen`: nothing has happened
   since the last verdict.

2. **Classify the last turn.** For each remaining session read the end of its
   transcript with `list_events` (limit 15) and give one verdict:
   - `done`: the thread reports its work finished or verified, or ends with a
     line starting `Done:`, and nothing it promised is still pending.
   - `waiting`: it ends on a decision, approval, input, physical action, or a
     platform-only step (password, account creation, CAPTCHA, OAuth, payment)
     that only Kenji can give, or with a line starting `Waiting on Kenji:`.
   - `stopped`: it ended mid-work: it says it will continue or names a next
     step it could run itself, it hit an error, tool failure, interrupt or
     context limit, it was waiting on a background job, or its last turn is
     only a progress update. A question the thread could answer itself under
     the standing permissions in `~/.farplane/USER.md` counts as `stopped`.
   Write a one-line reason in plain words for each verdict.

3. **Act on the verdict.**
   - `done`: record it; no action.
   - `stopped` with `state.nudges < max_nudges`: send the thread one message
     with `send_message`, then add 1 to `nudges`:
     `Thread Sweeper: this thread has been quiet for <h> hours and its last
     turn looks unfinished (<reason>). Continue from where you stopped. If you
     are truly blocked on Kenji, end your turn with one line "Waiting on Kenji:
     <exact question>"; if the work is finished, end with "Done: <result>".`
   - `stopped` with `nudges >= max_nudges`: treat it as `waiting`, with the
     reason `still stalled after <n> nudges: <reason>`.
   - `waiting`: add it to this run's Kenji list unless `state.notified_at`
     already equals this `lastActivityAt` (he has already been told).
   Reset `nudges` to 0 when the latest user turn in the transcript is Kenji's
   own message rather than a Thread Sweeper message. If `send_message` is
   refused, record `nudge refused` as the action and add the thread to the
   Kenji list with the reason `stalled; tap to restart: <reason>`.

4. **Tell Kenji once.** If the Kenji list is not empty, send one Telegram
   message with `$notify` (intent `blocker`, title `Thread Sweeper`, no thread
   route). For each thread: its title, hours idle, the exact question or
   blocker in at most 25 words, and its `link`. End with: `Reply in the
   thread itself (tap its link).` Then set `notified_at` for those threads.
   Send nothing when the list is empty.

5. **Write state and report.** Save `state` as
   `{session_id: {title, last_seen, verdict, nudges, notified_at}}`, dropping
   sessions outside `lookback`. Append a run section to `report`: the run time,
   then a table `thread | idle h | verdict | action | reason`, with each thread
   linked by its `link`, then the counts.

Boundaries: never archive, delete, stop, rename, regroup, or mark sessions;
never change their model, effort, or permissions; never do a thread's work
yourself; message only threads inside `lookback` and only Kenji on Telegram.
Quote at most short fragments of transcripts and never copy secrets from them.
If `list_sessions` or `list_events` is unavailable, write the report with
that gap and stop.

Final response:
- Counts: candidates, skipped unchanged, done, waiting, stopped, nudged,
  escalated, Telegram sent or not (with the delivery receipt).
- The report path.
- Receipt: no session archived, stopped, or changed; no work done on a
  thread's behalf.

Config source:
farplane/automations/thread-sweeper.md id="farplane-thread-sweeper"
